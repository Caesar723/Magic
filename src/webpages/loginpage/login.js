(() => {
    const ui = Object.fromEntries([...document.querySelectorAll('[id]')].map(element => [element.id, element]));
    const form = ui.itemForm, panel = document.querySelector('.login-panel');
    const inputs = [ui.login__username, ui.login__password, ui.login__password_repeat];
    const toggles = [ui.togglePassword, ui.toggleConfirmation];
    let mode = 'login', busy = false, navigating = false, switching = false, request = 0, redirect = 0, transition = 0;
    let controller;
    const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches || document.body.classList.contains('motion-reduced');
    const navigate = path => window.PageTransition ? PageTransition.navigate(path) : window.location.assign(path);

    function showMessage(text, field, success = false) {
        ui.message_confirm.textContent = text;
        ui.message_confirm.dataset.state = success ? 'success' : '';
        for (const input of inputs) input.removeAttribute('aria-invalid');
        if (field) { field.setAttribute('aria-invalid', 'true'); field.focus(); }
    }
    function setBusy(kind = '') {
        busy = Boolean(kind); document.body.dataset.busy = kind;
        form.setAttribute('aria-busy', String(busy));
        for (const button of [ui.signIn, ui.demo, ...toggles]) button.disabled = busy;
        for (const input of inputs) input.readOnly = busy;
        ui.authSwitch.setAttribute('aria-disabled', String(busy || switching));
        ui.signInLabel.textContent = kind === 'signup' ? 'Creating account…' : kind === 'login' ? 'Signing in…' : mode === 'signup' ? 'Register' : 'Enter the Hall';
        ui.demoLabel.textContent = kind === 'demo' ? 'Starting demo…' : 'Try the Demo';
    }
    function applyMode(next) {
        mode = next;
        const signup = mode === 'signup';
        panel.classList.toggle('signup-panel', signup);
        ui.loginTitle.textContent = signup ? 'Create Account' : 'Sign In';
        document.title = ui.loginTitle.textContent + ' · Magic';
        ui.confirmationField.hidden = !signup;
        ui.login__password_repeat.disabled = !signup;
        ui.login__password_repeat.required = signup;
        ui.login__password_repeat.value = '';
        ui.login__password.autocomplete = signup ? 'new-password' : 'current-password';
        if (signup) ui.login__password.minLength = 6;
        else ui.login__password.removeAttribute('minlength');
        ui.login__password.placeholder = signup ? 'At least 6 characters' : 'Your password';
        ui.buttom_container.hidden = signup;
        ui.authSwitch.href = signup ? '/login' : '/signup';
        ui.authSwitch.firstChild.textContent = signup ? 'Back to Sign In ' : 'Create an account ';
        for (const toggle of toggles) {
            document.getElementById(toggle.getAttribute('aria-controls')).type = 'password';
            toggle.setAttribute('aria-pressed', 'false');
            toggle.setAttribute('aria-label', toggle === ui.togglePassword ? 'Show password' : 'Show confirmation password');
        }
        ui.capsLock.hidden = true; showMessage(''); setBusy();
    }
    async function switchMode(next, historyMode = 'push', message = '') {
        const version = ++transition;
        panel.getAnimations().forEach(animation => animation.cancel());
        switching = true; ++request; controller?.abort(); clearTimeout(redirect); redirect = 0; setBusy();
        const fade = !reduced();
        if (fade) await panel.animate([{opacity: 1}, {opacity: 0, transform: 'translateY(5px)'}], {duration: 160, fill: 'forwards'}).finished.catch(() => {});
        if (version !== transition) return;
        applyMode(next);
        if (historyMode) history[historyMode + 'State'](null, '', next === 'signup' ? '/signup' : '/login');
        if (message) showMessage(message, null, true);
        panel.getAnimations().forEach(animation => animation.cancel());
        if (fade) await panel.animate([{opacity: 0, transform: 'translateY(5px)'}, {opacity: 1, transform: 'translateY(0)'}], {duration: 240}).finished.catch(() => {});
        if (version !== transition) return;
        switching = false; ui.authSwitch.setAttribute('aria-disabled', 'false');
        ui.login__username.focus({preventScroll: true});
    }
    async function post(url, data) {
        const activeController = new AbortController(); controller = activeController;
        const timeout = setTimeout(() => activeController.abort(), 20000);
        try {
            const response = await fetch(url, {
                method: 'POST', signal: activeController.signal,
                ...(data === undefined ? {} : {headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)})
            });
            if (!response.ok) throw new Error('Request failed.');
            return await response.json();
        } finally { clearTimeout(timeout); }
    }
    form.addEventListener('submit', async event => {
        event.preventDefault();
        if (busy || switching || !form.reportValidity()) return;
        const data = Object.fromEntries(new FormData(form)), signup = mode === 'signup', id = ++request;
        if (signup && data.password !== data.password_confirmation) {
            showMessage('Passwords do not match.', ui.login__password_repeat); return;
        }
        showMessage(''); setBusy(mode);
        try {
            const {message} = await post(signup ? '/signup' : '/login', data);
            if (id !== request) return;
            if (signup && message === 'Sign up successful') {
                showMessage('Account created. You can now sign in.', null, true);
                ui.signInLabel.textContent = 'Account Created';
                redirect = setTimeout(() => { ui.login__password.value = ''; switchMode('login', 'replace', 'Account created. You can now sign in.'); }, 800);
                return;
            }
            if (!signup && message === 'Login successful') { navigating = true; navigate('/'); return; }
            if (signup && message === 'Sign up unsuccessful') showMessage('That username is already in use.', ui.login__username);
            else if (!signup && message === 'username error') showMessage('No account matches that username.', ui.login__username);
            else if (!signup && message === 'passward error') showMessage('Incorrect password. Please try again.', ui.login__password);
            else throw new Error('Unrecognized response.');
        } catch (_) {
            if (id === request) showMessage(signup ? 'Could not create the account. Please try again.' : 'Could not sign in. Please try again.');
        } finally { if (id === request && !navigating && !redirect) setBusy(); }
    });
    ui.demo.addEventListener('click', async () => {
        if (busy || switching) return;
        const id = ++request; showMessage(''); setBusy('demo');
        try {
            const result = await post('/matching_demo');
            if (id !== request) return;
            if (result.state !== 'find!') throw new Error('Demo unavailable.');
            navigating = true; navigate('/game_demo');
        } catch (_) { if (id === request) showMessage('Could not start the demo. Please try again.'); }
        finally { if (id === request && !navigating) setBusy(); }
    });
    ui.authSwitch.addEventListener('click', event => {
        if (event.button || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault(); if (!busy && !switching) switchMode(mode === 'login' ? 'signup' : 'login');
    });
    form.addEventListener('input', () => { if (!busy) showMessage(''); });
    for (const toggle of toggles) toggle.addEventListener('click', () => {
        const input = document.getElementById(toggle.getAttribute('aria-controls')), visible = input.type === 'password';
        input.type = visible ? 'text' : 'password'; toggle.setAttribute('aria-pressed', String(visible));
        toggle.setAttribute('aria-label', `${visible ? 'Hide' : 'Show'} ${input === ui.login__password ? '' : 'confirmation '}password`);
    });
    for (const input of inputs.slice(1)) {
        for (const event of ['keydown', 'keyup']) input.addEventListener(event, event => { ui.capsLock.hidden = !event.getModifierState('CapsLock'); });
        input.addEventListener('blur', () => { ui.capsLock.hidden = true; });
    }
    const routeMode = () => location.pathname === '/signup' ? 'signup' : 'login';
    window.addEventListener('popstate', () => switchMode(routeMode(), false));
    window.addEventListener('pagehide', () => { clearTimeout(redirect); redirect = 0; });
    window.addEventListener('pageshow', event => {
        if (event.persisted) {
            ++transition; ++request; controller?.abort();
            panel.getAnimations().forEach(animation => animation.cancel());
            switching = navigating = false; applyMode(routeMode());
        }
    });
    applyMode(routeMode());
})();
