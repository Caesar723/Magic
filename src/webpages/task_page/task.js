// Task progress, replacement and rewards remain server-owned.
const taskUI = Object.fromEntries([...document.querySelectorAll('[id]')].map(node => [node.id, node]));
const taskState = {tasks: [], loading: false, busy: false, needsSync: false, selected: null, returnTarget: null};
const taskArt = {
    KillTask: ['Creature Hunt', 'hunt'], DrawTask: ['Draw Cards', 'draw'],
    PlayCardTask: ['Play Cards', 'play'], WinTask: ['Win Games', 'win'], Win5Task: ['Win Games', 'win'],
    UseSorceryTask: ['Cast Sorceries', 'sorcery'], SpendLandTask: ['Use Lands', 'land']
};
function taskPresentation(task) {
    const [title, kind] = Object.hasOwn(taskArt, task.name) ? taskArt[task.name] : [task.name.replace(/([a-z])([A-Z])/g, '$1 $2'), 'compass'];
    return {title: kind === 'win' && task.total_steps === 1 ? 'Win a Game' : title, kind};
}
function validTask(task) {
    return task && Number.isSafeInteger(task.id) && typeof task.name === 'string' && typeof task.description === 'string'
        && ['total_steps', 'progress', 'gold_reward'].every(key => Number.isFinite(task[key]) && task[key] >= 0);
}
async function taskRequest(path, body) {
    const options = {method: 'POST', signal: AbortSignal.timeout(20000)};
    if (body !== undefined) { options.headers = {'Content-Type': 'application/json'}; options.body = JSON.stringify(body); }
    const response = await fetch(path, options);
    if (!response.ok || response.redirected) throw new Error('Request could not be confirmed.');
    const data = await response.json();
    return typeof data === 'string' ? JSON.parse(data) : data;
}
async function generateTasks() {
    const data = await taskRequest('/get_task');
    if (!Array.isArray(data.task_data_list) || !data.task_data_list.every(validTask)) throw new Error('Invalid task list.');
    return data.task_data_list;
}
async function refreshTasks(task_id) {
    const task = await taskRequest('/refresh_task', {task_id});
    if (!validTask(task)) throw new Error('Invalid replacement.');
    return task;
}
function taskStatus(message, error = false) {
    taskUI['task-status'].textContent = message;
    taskUI['task-status'].dataset.error = String(error);
}
function updateTaskControls() {
    taskUI['reload-tasks'].disabled = taskState.busy || taskState.loading;
    taskUI.taskBar.querySelectorAll('.refresh-btn').forEach(button => {
        button.disabled = taskState.busy || taskState.loading || taskState.needsSync;
    });
    for (const id of ['close-replace', 'cancel-replace', 'confirm-replace']) taskUI[id].disabled = taskState.busy;
    taskUI['replace-dialog'].setAttribute('aria-busy', String(taskState.busy));
}
function createTaskElement(task, index = 0) {
    const {title, kind} = taskPresentation(task);
    const element = document.createElement('li');
    element.className = 'task';
    element.dataset.taskId = task.id;
    element.dataset.kind = kind;
    element.style.setProperty('--order', Math.min(index, 7));
    // Only static markup is parsed; all server text is assigned with textContent.
    element.innerHTML = '<div class="task-emblem" aria-hidden="true"><svg><use/></svg></div>'
        + '<div class="task-body"><h3 class="task-title"></h3><p class="task-description"></p>'
        + '<div class="progress-line"><div class="progress-bar" role="progressbar"><div class="progress"></div></div><span class="progress-text"></span></div>'
        + '<div class="task-bottom"><span class="task-reward"><span class="coin-mark" aria-hidden="true">✧</span><span></span></span>'
        + '<button class="refresh-btn"><span aria-hidden="true">↻</span> Replace</button></div></div>';
    element.querySelector('use').setAttribute('href', '#mark-' + kind);
    const heading = element.querySelector('.task-title');
    heading.textContent = title; heading.id = 'task-title-' + task.id;
    element.querySelector('.task-description').textContent = task.description;
    const progress = Math.min(task.progress, task.total_steps);
    const bar = element.querySelector('.progress-bar');
    bar.setAttribute('aria-labelledby', heading.id);
    bar.setAttribute('aria-valuemin', '0');
    bar.setAttribute('aria-valuemax', task.total_steps || 1);
    bar.setAttribute('aria-valuenow', progress);
    element.style.setProperty('--progress', (task.total_steps ? progress / task.total_steps * 100 : 0) + '%');
    element.querySelector('.progress-text').textContent = progress + ' / ' + task.total_steps;
    const reward = element.querySelector('.task-reward');
    reward.setAttribute('aria-label', task.gold_reward.toLocaleString('en-US') + ' coin reward');
    reward.lastElementChild.textContent = task.gold_reward.toLocaleString('en-US');
    const button = element.querySelector('.refresh-btn');
    button.dataset.taskId = task.id;
    button.setAttribute('aria-label', 'Replace ' + title);
    return element;
}
async function renderTasks() {
    if (taskState.busy || taskState.loading || taskUI['replace-dialog'].open) return;
    const focusedId = document.activeElement?.dataset.taskId;
    taskState.loading = true;
    taskUI.taskBar.setAttribute('aria-busy', 'true');
    taskUI['task-empty'].hidden = true;
    taskStatus('Updating tasks…'); updateTaskControls();
    try {
        const tasks = await generateTasks();
        taskState.tasks = tasks;
        taskState.needsSync = false;
        taskUI.taskBar.replaceChildren(...tasks.map(createTaskElement));
        taskUI.taskBar.style.setProperty('--rows', Math.max(1, Math.ceil(tasks.length / 2)));
        taskUI['task-count'].textContent = String(tasks.length).padStart(2, '0');
        taskUI['task-empty'].hidden = tasks.length > 0;
        taskStatus('');
    } catch (_) {
        taskState.needsSync = true;
        taskStatus('Unable to update tasks. Select Update Tasks to try again.', true);
    } finally {
        taskState.loading = false;
        taskUI.taskBar.setAttribute('aria-busy', 'false');
        updateTaskControls();
        if (focusedId) {
            const target = taskUI.taskBar.querySelector('[data-task-id="' + focusedId + '"] .refresh-btn');
            (target && !target.disabled ? target : taskUI['reload-tasks']).focus({preventScroll: true});
        }
    }
}
function handleRefresh(event) {
    const button = event.target.closest('.refresh-btn');
    if (!button || taskState.loading || taskState.busy || taskState.needsSync || taskUI['replace-dialog'].open) return;
    const task = taskState.tasks.find(entry => entry.id === Number(button.dataset.taskId));
    if (!task) return;
    taskState.selected = task;
    taskState.returnTarget = button;
    taskUI['replace-title'].textContent = 'Replace this task?';
    taskUI['replace-name'].textContent = taskPresentation(task).title + ' · ' + Math.min(task.progress, task.total_steps) + ' / ' + task.total_steps;
    taskUI['replace-status'].textContent = '';
    taskUI['confirm-replace'].textContent = 'Replace Task ↻';
    taskUI['cancel-replace'].textContent = 'Keep Task';
    taskUI['replace-dialog'].showModal();
    taskUI['cancel-replace'].focus();
}
function closeReplacement() {
    if (!taskState.busy) taskUI['replace-dialog'].close();
}
async function confirmReplacement() {
    if (taskState.busy || !taskState.selected || !taskUI['replace-dialog'].open) return;
    if (taskState.needsSync) {
        closeReplacement();
        await renderTasks();
        if (document.activeElement === document.body) taskUI['reload-tasks'].focus({preventScroll: true});
        return;
    }
    const task = taskState.selected;
    const element = taskState.returnTarget.closest('.task');
    taskState.busy = true;
    element.setAttribute('aria-busy', 'true');
    taskUI['confirm-replace'].textContent = 'Replacing…';
    taskUI['replace-status'].textContent = '';
    updateTaskControls();
    let replaced = false;
    try {
        const newTask = await refreshTasks(task.id);
        const index = taskState.tasks.findIndex(entry => entry.id === task.id);
        taskState.tasks[index] = newTask;
        const newElement = createTaskElement(newTask);
        if (newTask.id !== task.id) newElement.classList.add('is-new');
        element.replaceWith(newElement);
        taskState.returnTarget = newElement.querySelector('.refresh-btn');
        taskStatus(newTask.id === task.id ? 'No replacement is available right now.' : 'Task replaced.');
        replaced = true;
    } catch (_) {
        // The server may have replaced the task before the response failed. Reconcile first; never retry the mutation automatically.
        taskState.needsSync = true;
        taskUI['replace-title'].textContent = 'Update your tasks';
        taskUI['replace-status'].textContent = 'Replacement could not be confirmed. Update the task list before replacing another task.';
        taskUI['confirm-replace'].textContent = 'Update Tasks';
        taskUI['cancel-replace'].textContent = 'Close';
        taskStatus('Update the task list before replacing another task.', true);
    } finally {
        taskState.busy = false;
        element.removeAttribute('aria-busy');
        updateTaskControls();
        if (replaced) closeReplacement();
        else taskUI['confirm-replace'].focus();
    }
}
async function updateTaskCurrency() {
    const button = taskUI['refresh-balance'];
    if (button.disabled) return;
    button.disabled = true;
    try {
        const data = await taskRequest('/get_currency');
        if (!Number.isFinite(data.currency) || data.currency < 0) throw new Error('Invalid balance.');
        taskUI.currency.querySelector('.button-text').textContent = data.currency.toLocaleString('en-US');
        taskUI.currency.setAttribute('aria-label', 'Coins');
        button.title = 'Refresh coin balance';
    } catch (_) {
        taskUI.currency.querySelector('.button-text').textContent = '—';
        taskUI.currency.setAttribute('aria-label', 'Coin balance unavailable');
        button.title = 'Balance unavailable. Refresh to try again.';
    } finally { button.disabled = false; }
}

taskUI.taskBar.addEventListener('click', handleRefresh);
for (const id of ['close-replace', 'cancel-replace']) taskUI[id].addEventListener('click', closeReplacement);
const replaceDialog = taskUI['replace-dialog'];
replaceDialog.addEventListener('cancel', event => { if (taskState.busy) event.preventDefault(); });
replaceDialog.addEventListener('close', () => {
    taskState.selected = null;
    const target = taskState.returnTarget;
    (target?.isConnected && !target.disabled ? target : taskUI['reload-tasks']).focus({preventScroll: true});
});
replaceDialog.addEventListener('click', event => {
    if (event.target !== replaceDialog) return;
    const rect = replaceDialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeReplacement();
});
taskUI['confirm-replace'].addEventListener('click', confirmReplacement);
taskUI['reload-tasks'].addEventListener('click', () => { renderTasks(); updateTaskCurrency(); });
taskUI['refresh-balance'].addEventListener('click', updateTaskCurrency);

const taskMotion = matchMedia('(prefers-reduced-motion: reduce)');
function taskMotionPreference() {
    let stored = false;
    try { stored = localStorage.getItem('lobby-reduced-motion') === 'true'; } catch (_) {}
    document.body.classList.toggle('motion-reduced', taskMotion.matches || stored);
}
function pauseTaskMotion() { document.body.classList.toggle('motion-paused', document.hidden || !document.hasFocus()); }
for (const type of ['focus', 'blur']) window.addEventListener(type, pauseTaskMotion);
document.addEventListener('visibilitychange', pauseTaskMotion);
taskMotion.addEventListener('change', taskMotionPreference);
window.addEventListener('storage', event => { if (event.key === 'lobby-reduced-motion') taskMotionPreference(); });
window.addEventListener('pageshow', event => {
    pauseTaskMotion();
    if (event.persisted) { renderTasks(); updateTaskCurrency(); }
});
const motes = document.createDocumentFragment();
for (let i = 0; i < 12; i++) {
    const mote = document.createElement('span'); mote.className = 'mote';
    mote.style.setProperty('--x', ((i * 37 + 3) % 100) + '%');
    mote.style.setProperty('--duration', (15 + i * .8) + 's');
    mote.style.setProperty('--delay', (-i * 2.3) + 's');
    motes.append(mote);
}
document.querySelector('.ambient').append(motes);
taskMotionPreference(); pauseTaskMotion();
const journalReady = Promise.all([renderTasks(), updateTaskCurrency()]);
window.PageTransition?.wait(journalReady);
