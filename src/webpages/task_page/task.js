const taskTemplates = [
  { title: "Complete Tutorial", description: "Finish the beginner's guide and earn gold rewards.", goldReward: 50, totalSteps: 5 },
  { title: "Collect Cards", description: "Gather 100 cards to unlock a new character.", goldReward: 100, totalSteps: 100 },
  { title: "Battle Opponents", description: "Participate in 5 battles to win a rare card pack.", goldReward: 75, totalSteps: 5 },
  { title: "Upgrade Headquarters", description: "Level up your HQ to 5 to unlock new features.", goldReward: 150, totalSteps: 5 },
  { title: "Daily Quests", description: "Complete daily missions for bonus rewards.", goldReward: 20, totalSteps: 1 },
  { title: "Join Guild", description: "Become a member of a guild and join guild events.", goldReward: 30, totalSteps: 1 },
  { title: "Defeat Boss", description: "Challenge the boss to obtain rare equipment.", goldReward: 200, totalSteps: 1 },
  { title: "Story Mode", description: "Complete the first chapter of the main storyline.", goldReward: 80, totalSteps: 1 },
];

async function generateTasks() {
  const tasks = new Request("/get_task",{
    method:"POST",
  });
  const response = await fetch(tasks);
  const data = await response.json();
  console.log(data);

  return data.task_data_list;
}

function createTaskElement(task) {
  const taskElement = document.createElement('div');
  taskElement.className = 'task';
  taskElement.innerHTML = `
      <div class="task-header">
          <span class="task-title">${task.name}</span>
          <button class="refresh-btn" data-task-id="${task.id}">Refresh</button>
      </div>
      <div class="task-description">${task.description}</div>
      <div class="task-reward">Gold Reward: ${task.gold_reward}</div>
      <div class="progress-bar">
          <div class="progress" style="width: ${(task.progress / task.total_steps) * 100}%;"></div>
      </div>
      <div class="progress-text">${task.progress}/${task.total_steps}</div>
  `;
  return taskElement;
}

async function renderTasks() {
  const taskBar = document.getElementById('taskBar');
  taskBar.innerHTML = '';
  const tasks = await generateTasks();
  tasks.forEach(task => {
      const taskElement = createTaskElement(task);
      taskBar.appendChild(taskElement);
  });
  document.getElementById('taskBar').addEventListener('click', handleRefresh);
}

async function refreshTasks(task_id) {
  const tasks = new Request("/refresh_task",{
    method:"POST",
    headers:{
      "Content-Type":"application/json"
    },
    body:JSON.stringify({
      task_id:task_id
    })
  });
  const response = await fetch(tasks);
  const data = await response.json();
  console.log(data);

  return data;
}
async function handleRefresh(event) {
  if (event.target.classList.contains('refresh-btn')) {
      const taskId = parseInt(event.target.getAttribute('data-task-id'));
      console.log(taskId);
      const taskElement = event.target.closest('.task');
      const newTask = await refreshTasks(taskId);
      
      taskElement.querySelector('.task-title').textContent = newTask.name;
      taskElement.querySelector('.task-description').textContent = newTask.description;
      taskElement.querySelector('.task-reward').textContent = `Gold Reward: ${newTask.gold_reward}`;
      taskElement.querySelector('.refresh-btn').setAttribute('data-task-id', newTask.id);
      taskElement.querySelector('.progress').style.width = `${(newTask.progress / newTask.total_steps) * 100}%`;
      taskElement.querySelector('.progress-text').textContent = `${newTask.progress}/${newTask.total_steps}`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderTasks();
  
});