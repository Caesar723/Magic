if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/webpages/service-worker.js').catch(() => {});
}

// Shared battle renderer constants; the battlefield itself remains unchanged.
const size_rat = 7 / 10;
var SIZE = 1000 * size_rat;
var POSITION = [2000, -700, 3000];
var TIME_INTERVAL = 2;

(() => {
    const canvas = document.getElementById('myCanvas');
    const viewport = document.getElementById('battle-viewport');
    const workspace = document.querySelector('.studio-workspace');
    const divider = document.getElementById('workspace-divider');
    const roomStatus = document.getElementById('room-status');
    const testPanel = new StudioTestPanel();
    let client, frame = 0, lastTime = 0, roomCreated = false;

    function resizeCanvas() {
        if (!client || !viewport.clientWidth || !viewport.clientHeight) return;
        const scale = Math.min(viewport.clientWidth / (canvas.width * .841), viewport.clientHeight / canvas.height);
        canvas.style.transformOrigin = 'top left';
        canvas.style.transform = 'scale(' + scale * .841 + ', ' + scale + ')';
        canvas.style.left = (viewport.clientWidth - canvas.width * scale * .841) / 2 + 'px';
        canvas.style.top = (viewport.clientHeight - canvas.height * scale) / 2 + 'px';
        if (document.body.dataset.view === 'split' && divider.offsetWidth) {
            const total = document.getElementById('canvasContainer').offsetWidth + document.getElementById('editor').offsetWidth;
            divider.setAttribute('aria-valuenow', String(Math.round(document.getElementById('canvasContainer').offsetWidth / total * 100)));
        }
    }

    function render(time) {
        frame = 0;
        TIME_INTERVAL = lastTime ? Math.min((time - lastTime) / 16.67, 3) * 2 : 2;
        lastTime = time;
        client.ctx_table.clearRect(0, 0, canvas.width, canvas.height);
        client.update();
        client.draw();
        frame = requestAnimationFrame(render);
    }

    function updatePlayback() {
        cancelAnimationFrame(frame);
        frame = 0;
        lastTime = 0;
        if (client && !document.hidden && document.hasFocus() && document.body.dataset.view !== 'editor') {
            frame = requestAnimationFrame(render);
        }
    }

    function setView(view) {
        if (!['split', 'battle', 'editor'].includes(view)) return;
        document.body.dataset.view = view;
        document.querySelectorAll('.view-switch button').forEach(button => {
            button.setAttribute('aria-pressed', String(button.dataset.view === view));
        });
        resizeCanvas();
        updatePlayback();
        document.dispatchEvent(new Event('studio:resize'));
    }

    document.querySelectorAll('.view-switch button').forEach(button => {
        button.addEventListener('click', () => setView(button.dataset.view));
    });
    function splitBounds() {
        const style = getComputedStyle(workspace);
        const padding = parseFloat(style.paddingLeft);
        return { left: workspace.getBoundingClientRect().left + padding, width: workspace.clientWidth - padding - parseFloat(style.paddingRight) - divider.offsetWidth };
    }
    function resizeSplit(percent) {
        const available = splitBounds().width;
        const battlePercent = Math.max(30, Math.min(70, percent));
        const editorWidth = Math.max(360, available * (100 - battlePercent) / 100);
        workspace.style.setProperty('--editor-width', editorWidth + 'px');
        divider.setAttribute('aria-valuenow', String(Math.round(100 - editorWidth / available * 100)));
        document.dispatchEvent(new Event('studio:resize'));
    }
    divider.addEventListener('pointerdown', event => {
        if (event.button !== 0) return;
        divider.setPointerCapture(event.pointerId);
        document.body.classList.add('resizing');
    });
    divider.addEventListener('pointermove', event => {
        if (!divider.hasPointerCapture(event.pointerId)) return;
        const bounds = splitBounds();
        resizeSplit((event.clientX - bounds.left) / bounds.width * 100);
    });
    divider.addEventListener('lostpointercapture', () => document.body.classList.remove('resizing'));
    divider.addEventListener('pointerup', event => divider.releasePointerCapture(event.pointerId));
    divider.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        let value = Number(divider.getAttribute('aria-valuenow'));
        value = event.key === 'Home' ? 30 : event.key === 'End' ? 70 : value + (event.key === 'ArrowRight' ? 5 : -5);
        resizeSplit(value);
    });
    new ResizeObserver(resizeCanvas).observe(viewport);
    window.addEventListener('blur', updatePlayback);
    window.addEventListener('focus', updatePlayback);
    document.addEventListener('visibilitychange', updatePlayback);
    window.addEventListener('pagehide', () => {
        cancelAnimationFrame(frame);
        if (!roomCreated) return;
        roomCreated = false;
        fetch('/delete_studio_room', { method: 'POST', keepalive: true }).catch(() => {});
        client?.socket_main?.close();
        client?.socket_select?.close();
    });
    window.addEventListener('pageshow', event => { if (event.persisted) location.reload(); });

    async function initialize() {
        const response = await fetch('/matching_studio', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
        if (!response.ok) throw new Error('Could not create the studio room.');
        window.dataFromBackend = await response.json();
        roomCreated = true;
        client = new Game_Client();
        testPanel.socket = client.socket_main;
        new Card_Add(client.socket_main, (message, state) => testPanel.feedback(message, state));
        const updateConnection = () => {
            const connected = client.socket_main.readyState === WebSocket.OPEN && client.socket_select.readyState === WebSocket.OPEN;
            roomStatus.textContent = connected ? 'Live test room' : 'Disconnected · reload to reconnect';
            roomStatus.dataset.state = connected ? 'ready' : 'error';
            testPanel.setConnected(connected);
        };
        for (const socket of [client.socket_main, client.socket_select]) {
            socket.addEventListener('open', updateConnection);
            socket.addEventListener('close', updateConnection);
            socket.addEventListener('error', updateConnection);
        }
        if (client.socket_main.readyState === WebSocket.OPEN && client.socket_select.readyState === WebSocket.OPEN) updateConnection();
        resizeCanvas();
        updatePlayback();
    }
    window.StudioWorkspace = {
        setView,
        connected: () => client?.socket_main?.readyState === WebSocket.OPEN && client?.socket_select?.readyState === WebSocket.OPEN,
        ready: initialize()
    };
    window.PageTransition?.wait(window.StudioWorkspace.ready);
    window.StudioWorkspace.ready.catch(() => {
        roomStatus.textContent = 'Connection failed · reload to retry';
        roomStatus.dataset.state = 'error';
        testPanel.setConnected(false);
    });
})();
