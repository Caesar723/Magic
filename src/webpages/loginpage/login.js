(() => {
    const ui = Object.fromEntries([...document.querySelectorAll('[id]')].map(element => [element.id, element]));
    const form = ui.itemForm;
    let busy = false, navigating = false;

    function showMessage(text, field) {
        ui.message_confirm.textContent = text;
        for (const input of [ui.login__username, ui.login__password]) input.removeAttribute('aria-invalid');
        if (field) { field.setAttribute('aria-invalid', 'true'); field.focus(); }
    }
    function setBusy(kind = '') {
        busy = Boolean(kind); document.body.dataset.busy = kind;
        form.setAttribute('aria-busy', String(busy));
        ui.signIn.disabled = ui.demo.disabled = ui.togglePassword.disabled = busy;
        ui.login__username.readOnly = ui.login__password.readOnly = busy;
        ui.signInLabel.textContent = kind === 'login' ? 'Signing in…' : 'Enter the Hall';
        ui.demoLabel.textContent = kind === 'demo' ? 'Starting demo…' : 'Try the Demo';
    }
    async function post(url, data) {
        const response = await fetch(url, {
            method: 'POST', signal: AbortSignal.timeout(20000),
            ...(data === undefined ? {} : {headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)})
        });
        if (!response.ok) throw new Error('Request failed.');
        return response.json();
    }
    form.addEventListener('submit', async event => {
        event.preventDefault();
        if (busy || !form.reportValidity()) return;
        const data = Object.fromEntries(new FormData(form));
        showMessage(''); setBusy('login');
        try {
            const {message} = await post('/login', data);
            if (message === 'Login successful') {
                navigating = true; window.location.assign('/'); return;
            }
            if (message === 'username error') showMessage('No account matches that username.', ui.login__username);
            else if (message === 'passward error') showMessage('Incorrect password. Please try again.', ui.login__password);
            else showMessage('Could not sign in. Please try again.');
        } catch (_) { showMessage('Could not sign in. Please try again.'); }
        finally { if (!navigating) setBusy(); }
    });
    ui.demo.addEventListener('click', async () => {
        if (busy) return;
        showMessage(''); setBusy('demo');
        try {
            const result = await post('/matching_demo');
            if (result.state !== 'find!') throw new Error('Demo unavailable.');
            navigating = true; window.location.assign('/game_demo');
        } catch (_) { showMessage('Could not start the demo. Please try again.'); }
        finally { if (!navigating) setBusy(); }
    });
    form.addEventListener('input', () => { if (!busy) showMessage(''); });
    ui.togglePassword.addEventListener('click', () => {
        const visible = ui.login__password.type === 'password';
        ui.login__password.type = visible ? 'text' : 'password';
        ui.togglePassword.setAttribute('aria-pressed', String(visible));
        ui.togglePassword.setAttribute('aria-label', visible ? 'Hide password' : 'Show password');
    });
    for (const event of ['keydown', 'keyup']) ui.login__password.addEventListener(event, event => { ui.capsLock.hidden = !event.getModifierState('CapsLock'); });
    ui.login__password.addEventListener('blur', () => { ui.capsLock.hidden = true; });

    window.addEventListener('pageshow', event => {
        if (event.persisted) { navigating = false; setBusy(); }
    });
})();
