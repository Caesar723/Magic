(() => {
    const ui = Object.fromEntries([...document.querySelectorAll('[id]')].map(element => [element.id, element]));
    const form = ui.itemForm;
    const inputs = [ui.login__username, ui.login__password, ui.login__password_repeat];
    const toggles = [ui.togglePassword, ui.toggleConfirmation];
    let busy = false, created = false, redirect = 0;

    function showMessage(text, field, success = false) {
        ui.message_confirm.textContent = text;
        ui.message_confirm.dataset.state = success ? 'success' : '';
        for (const input of inputs) input.removeAttribute('aria-invalid');
        if (field) { field.setAttribute('aria-invalid', 'true'); field.focus(); }
    }
    function setBusy(value) {
        busy = value;
        document.body.dataset.busy = value && !created ? 'signup' : '';
        form.setAttribute('aria-busy', String(value && !created));
        for (const button of [ui.signUp, ...toggles]) button.disabled = value;
        for (const input of inputs) input.readOnly = value;
        ui.signUpLabel.textContent = created ? 'Account Created' : value ? 'Creating account…' : 'Register';
    }
    form.addEventListener('submit', async event => {
        event.preventDefault();
        if (busy || !form.reportValidity()) return;
        const data = Object.fromEntries(new FormData(form));
        if (data.password !== data.password_confirmation) {
            showMessage('Passwords do not match.', ui.login__password_repeat);
            return;
        }
        showMessage(''); setBusy(true);
        try {
            const response = await fetch('/signup', {
                method: 'POST', signal: AbortSignal.timeout(20000),
                headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Request failed.');
            const {message} = await response.json();
            if (message === 'Sign up successful') {
                created = true; setBusy(true);
                showMessage('Account created. Redirecting to sign in…', null, true);
                redirect = setTimeout(() => window.location.assign('/login'), 800);
                return;
            }
            if (message === 'Sign up unsuccessful') showMessage('That username is already in use.', ui.login__username);
            else showMessage('Could not create the account. Please try again.');
        } catch (_) { showMessage('Could not create the account. Please try again.'); }
        finally { if (!created) setBusy(false); }
    });
    form.addEventListener('input', () => { if (!busy) showMessage(''); });
    for (const toggle of toggles) toggle.addEventListener('click', () => {
        const input = document.getElementById(toggle.getAttribute('aria-controls'));
        const visible = input.type === 'password';
        input.type = visible ? 'text' : 'password';
        toggle.setAttribute('aria-pressed', String(visible));
        toggle.setAttribute('aria-label', `${visible ? 'Hide' : 'Show'} ${input === ui.login__password ? '' : 'confirmation '}password`);
    });
    for (const input of inputs.slice(1)) {
        for (const event of ['keydown', 'keyup']) input.addEventListener(event, event => { ui.capsLock.hidden = !event.getModifierState('CapsLock'); });
        input.addEventListener('blur', () => { ui.capsLock.hidden = true; });
    }
    window.addEventListener('pagehide', () => clearTimeout(redirect));
    window.addEventListener('pageshow', event => {
        if (event.persisted) { created = false; setBusy(false); showMessage(''); }
    });
})();
