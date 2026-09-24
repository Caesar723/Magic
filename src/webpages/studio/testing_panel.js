(() => {
    const KEYWORDS = ['flying', 'reach', 'trample', 'haste', 'lifelink', 'vigilance', 'flash'];
    const ACTIONS = {
        labManaSelfBtn: ['test_restore_mana', 'self', 'Refill your mana'],
        labManaAllBtn: ['test_restore_mana', 'all', 'Refill both sides’ mana'],
        labUntapAllBtn: ['test_untap_all', '', 'Untap both fields'],
        labResetLandCapBtn: ['test_reset_land_cap', '', 'Reset land drops for both players'],
        labClearHandBtn: ['test_clear_hand', '', 'Move your hand to your graveyard'],
        labWipeBtn: ['test_board_wipe', '', 'Destroy all creatures on both fields']
    };

    class StudioTestPanel {
        constructor() {
            this.socket = null;
            this.side = 'self';
            this.panel = null;
            this.bench = document.getElementById('test-bench');
            this.status = document.getElementById('lab-status');
            this.form = document.getElementById('labCreatureForm');
            this.power = document.getElementById('labPower');
            this.toughness = document.getElementById('labTough');
            this.buttons = [...this.bench.querySelectorAll('[data-tool]')];
            for (const button of this.buttons) {
                button.addEventListener('click', () => this.open(this.panel === button.dataset.tool ? null : button.dataset.tool));
            }
            document.getElementById('bench-close').addEventListener('click', () => this.close());
            this.bench.addEventListener('keydown', event => {
                if (event.key === 'Escape' && this.panel) {
                    event.preventDefault();
                    this.close();
                }
            });
            for (const key of KEYWORDS) {
                const label = document.createElement('label');
                const input = document.createElement('input');
                input.type = 'checkbox';
                input.value = key;
                label.append(input, key[0].toUpperCase() + key.slice(1));
                document.getElementById('labKeywords').append(label);
            }
            this.form.querySelectorAll('[data-side]').forEach(button => button.addEventListener('click', () => {
                this.side = button.dataset.side;
                this.form.querySelectorAll('[data-side]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
                this.updatePreview();
            }));
            this.form.addEventListener('input', () => this.updatePreview());
            this.form.addEventListener('submit', event => {
                event.preventDefault();
                this.spawn();
            });
            this.form.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
                const [power, toughness, keyword = ''] = button.dataset.preset.split(',');
                this.power.value = power;
                this.toughness.value = toughness;
                this.form.querySelectorAll('#labKeywords input').forEach(input => { input.checked = input.value === keyword; });
                this.updatePreview();
            }));
            for (const [id, action] of Object.entries(ACTIONS)) {
                document.getElementById(id).addEventListener('click', () => this.send(...action, document.getElementById(id)));
            }
        }

        open(panel) {
            this.panel = panel;
            this.buttons.forEach(button => {
                const active = button.dataset.tool === panel;
                button.setAttribute('aria-expanded', String(active));
                document.getElementById(button.dataset.tool).hidden = !active;
            });
            document.getElementById('bench-close').hidden = !panel;
            this.bench.dataset.open = String(Boolean(panel));
        }

        close() {
            const button = this.buttons.find(item => item.dataset.tool === this.panel);
            this.open(null);
            button?.focus();
        }

        keywords() {
            return [...this.form.querySelectorAll('#labKeywords input:checked')].map(input => input.value);
        }

        updatePreview() {
            this.power.setCustomValidity('');
            this.toughness.setCustomValidity('');
            document.getElementById('labPreviewStats').textContent = (this.power.value || '—') + ' / ' + (this.toughness.value || '—');
            const keys = this.keywords();
            document.getElementById('labPreviewKeywords').textContent = keys.length ? keys.map(key => key[0].toUpperCase() + key.slice(1)).join(' · ') : 'No keywords';
            document.getElementById('labTokenPreview').dataset.side = this.side;
        }

        spawn() {
            for (const input of [this.power, this.toughness]) {
                input.setCustomValidity(Number.isSafeInteger(Number(input.value)) ? '' : 'Enter a whole number within the supported range.');
            }
            if (!this.form.reportValidity()) return;
            const power = Number(this.power.value), toughness = Number(this.toughness.value);
            const content = [this.side, power, toughness, this.keywords().join(',')].join(';');
            this.send('test_spawn', content, 'Create a ' + power + '/' + toughness + ' creature on ' + (this.side === 'self' ? 'your field' : 'the opponent’s field'), document.getElementById('labSpawnBtn'));
        }

        setConnected(connected) {
            document.querySelectorAll('[data-room-command]').forEach(button => { button.disabled = !connected; });
            if (!connected) this.feedback('Test controls need a live room. Reload to reconnect.', 'error');
            else if (this.status.dataset.state === 'error') this.feedback('Test room connected. Choose a tool to begin.');
        }

        send(command, content, description, button) {
            if (this.socket?.readyState !== WebSocket.OPEN || !window.StudioWorkspace?.connected()) {
                this.feedback('The test room is not connected. Reload to reconnect.', 'error');
                return;
            }
            try {
                this.socket.send([window.dataFromBackend.self, command, content].join('|'));
                this.feedback('Sent: ' + description + '.');
                if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
                    button?.animate([{ boxShadow: '0 0 0 3px #a4c8ae' }, { boxShadow: '0 0 0 0 transparent' }], { duration: 500 });
                }
            } catch {
                this.feedback('The command could not be sent. Check the room connection.', 'error');
            }
        }

        feedback(message, state = '') {
            this.status.textContent = message;
            this.status.dataset.state = state;
        }
    }

    window.StudioTestPanel = StudioTestPanel;
})();
