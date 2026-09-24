(() => {
    const commonEvents = ['when_start_turn', 'when_end_turn', 'when_kill_creature', 'when_a_creature_die', 'when_an_object_hert', 'aura'];
    // Keep the existing API spellings, including attcak and hert.
    const cardEvents = {
        Creature: ['when_enter_battlefield', 'when_leave_battlefield', 'when_die', 'when_harm_is_done', 'when_being_treated', 'when_become_attacker', 'when_become_defender', 'when_start_attcak', 'when_start_defend', ...commonEvents],
        Land: ['when_enter_battlefield', 'when_clicked', ...commonEvents],
        Instant: ['card_ability', ...commonEvents],
        Sorcery: ['card_ability', ...commonEvents]
    };
    const eventLabels = {
        when_enter_battlefield: 'Enters the battlefield', when_leave_battlefield: 'Leaves the battlefield',
        when_die: 'Dies', when_harm_is_done: 'Deals damage', when_being_treated: 'Is healed',
        when_become_attacker: 'Becomes an attacker', when_become_defender: 'Becomes a defender',
        when_start_attcak: 'Starts attacking', when_start_defend: 'Starts defending',
        when_start_turn: 'Your turn begins', when_end_turn: 'Your turn ends',
        when_kill_creature: 'Kills a creature', when_a_creature_die: 'A creature dies',
        when_an_object_hert: 'An object takes damage', aura: 'Aura', when_clicked: 'Land is clicked',
        card_ability: 'Spell resolves'
    };
    const keywords = {
        Creature: ['reach', 'Trample', 'flying', 'haste', 'summoning_sickness', 'Flash', 'lifelink', 'Vigilance', 'Double strike', 'Menace', 'Hexproof'],
        Land: ['Flash', 'lifelink'], Instant: ['lifelink'], Sorcery: ['lifelink']
    };
    const effect = (method, target, amount, color) => 'await self.' + method + '(' + target + ', ' + amount + ', "' + color + '", "Missile_Hit")';
    const snippets = [
        { id: 'draw', name: 'Draw cards', note: 'Add cards to your hand', code: n => 'player.draw_card(' + n + ')' },
        { id: 'heal', name: 'Gain life', note: 'Restore your life', code: n => effect('cure_to_object', 'player', n, 'rgba(105, 175, 148, 0.9)') },
        { id: 'damage', name: 'Damage opponent', note: 'Hit the opposing player', code: n => effect('attact_to_object', 'opponent', n, 'rgba(182, 100, 80, 0.9)') },
        { id: 'target-damage', name: 'Damage target', note: 'Hit a creature or player', target: 'role', code: n => effect('attact_to_object', 'selected_object[0]', n, 'rgba(182, 100, 80, 0.9)') },
        { id: 'target-heal', name: 'Heal target', note: 'Heal a creature or player', target: 'role', code: n => effect('cure_to_object', 'selected_object[0]', n, 'rgba(105, 175, 148, 0.9)') },
        { id: 'destroy', name: 'Destroy creature', note: 'Remove the chosen creature', target: 'creature', code: () => 'await self.destroy_object(selected_object[0], "rgba(92, 117, 136, 0.9)", "Missile_Hit")' },
        { id: 'exile', name: 'Exile creature', note: 'Exile the chosen creature', target: 'creature', code: () => 'await self.exile_object(selected_object[0], "rgba(105, 175, 148, 0.9)", "Missile_Hit")' },
        { id: 'sweep', name: 'Damage all enemies', note: 'Hit each enemy creature', code: n => 'for target in opponent.battlefield:\n    ' + effect('attact_to_object', 'target', n, 'rgba(182, 100, 80, 0.9)') },
        { id: 'random', name: 'Random enemy', note: 'Hit a random enemy creature', code: n => 'if opponent.battlefield:\n    target = random.choice(opponent.battlefield)\n    ' + effect('attact_to_object', 'target', n, 'rgba(182, 100, 80, 0.9)') },
        { id: 'low-life', name: 'Low-life draw', note: 'Draw if your life is 10 or less', code: n => 'if player.life <= 10:\n    player.draw_card(' + n + ')' },
        { id: 'untap', name: 'Untap this card', note: 'Ready this creature or land', permanent: true, code: () => 'self.untap()' },
        { id: 'counter', name: 'Counter spell', note: 'Undo the top spell on the stack', counter: true, code: () => 'await self.undo_stack(player, opponent)' }
    ];
    const $ = id => document.getElementById(id);

    class Editor {
        constructor() {
            this.form = $('card-form');
            this.type = 'Creature';
            this.drafts = {};
            this.busy = false;
            this.fallbackHistory = new WeakMap();
            this.textarea = $('ability-code');
            if (window.CodeMirror?.fromTextArea) {
                this.code = CodeMirror.fromTextArea(this.textarea, {
                    mode: 'python', lineNumbers: true, indentUnit: 4, tabSize: 4, indentWithTabs: false,
                    extraKeys: { 'Ctrl-Enter': () => this.send(false), 'Cmd-Enter': () => this.send(false), Tab: cm => cm.replaceSelection('    ', 'end') }
                });
                this.code.getInputField().setAttribute('aria-label', 'Ability code');
                this.code.on('change', () => { if (!this.loading) this.changed(); });
            }
            this.textarea.addEventListener('input', () => {
                this.current.codes.set(this.current.event, this.textarea.value);
                this.changed();
            });
            this.form.addEventListener('submit', event => event.preventDefault());
            this.form.addEventListener('input', event => {
                const field = event.target;
                if (!field.name || ['selector_function', 'selector_target'].includes(field.name)) return;
                if (field.name === 'buff') this.current.buff = [...this.form.querySelectorAll('[name=buff]:checked')].map(input => input.value);
                else this.current[field.name] = field.type === 'checkbox' ? field.checked : field.value;
                this.changed();
                if (field.name === 'is_undo') this.renderSnippets();
            });
            for (const type of Object.keys(cardEvents)) {
                const button = document.createElement('button');
                button.type = 'button';
                button.textContent = type;
                button.dataset.type = type;
                button.addEventListener('click', () => this.selectType(type));
                $('card-types').append(button);
            }
            document.querySelectorAll('[data-panel]').forEach(button => button.addEventListener('click', () => this.showPanel(button.dataset.panel)));
            document.querySelectorAll('[data-next]').forEach(button => button.addEventListener('click', () => this.showPanel(button.dataset.next)));
            $('selector_function').addEventListener('change', event => this.selectEvent(event.target.value));
            $('selector_target').addEventListener('change', event => {
                this.current.target = event.target.value;
                this.changed();
                this.renderSnippets();
            });
            $('block-search').addEventListener('input', () => this.renderSnippets());
            $('block-amount').addEventListener('input', () => this.renderSnippets());
            $('expand-code').addEventListener('click', () => {
                window.StudioWorkspace?.setView('editor');
                this.code ? this.code.focus() : this.textarea.focus();
            });
            $('undo-code').addEventListener('click', () => {
                if (this.code) this.code.undo();
                else {
                    const history = this.fallbackHistory.get(this.current)?.get(this.current.event) || [];
                    const previous = history.pop();
                    if (previous) {
                        this.textarea.value = previous.value;
                        this.textarea.setSelectionRange(previous.cursor, previous.cursor);
                        this.current.codes.set(this.current.event, previous.value);
                        this.changed();
                    }
                }
            });
            $('test-card').addEventListener('click', () => this.send(false));
            $('submit-card').addEventListener('click', () => this.send(true));
            $('new-card').addEventListener('click', () => {
                if (!this.current.dirty) { this.reset(); return; }
                $('reset-card-type').textContent = this.type;
                $('new-card-dialog').returnValue = 'cancel';
                $('new-card-dialog').showModal();
            });
            $('new-card-dialog').addEventListener('close', () => {
                if ($('new-card-dialog').returnValue === 'reset') this.reset();
            });
            document.addEventListener('studio:resize', () => this.code?.refresh());
            new ResizeObserver(() => this.code?.refresh()).observe($('code-drop-zone'));
            this.bindDrop();
            this.bindArtwork();
            this.selectType('Creature');
        }

        get current() { return this.drafts[this.type]; }

        makeDraft(type) {
            return {
                name: '', mana: type === 'Land' ? '' : '1G', color: 'green', rarity: 'Common', type_creature: 'Wizard',
                attack: '2', health: '2', description: '', is_undo: false, buff: [], target: '',
                event: cardEvents[type][0], codes: new Map(), art: '', file: null, artVersion: 0, dirty: false
            };
        }

        selectType(type) {
            if (this.busy) return;
            this.type = type;
            this.drafts[type] ||= this.makeDraft(type);
            const draft = this.current;
            for (const name of ['name', 'mana', 'color', 'rarity', 'type_creature', 'attack', 'health', 'description', 'is_undo']) {
                const field = this.form.elements[name];
                if (field.type === 'checkbox') field.checked = draft[name];
                else field.value = draft[name];
            }
            $('creature-fields').hidden = type !== 'Creature';
            for (const name of ['type_creature', 'attack', 'health']) this.form.elements[name].disabled = type !== 'Creature';
            $('mana-field').hidden = type === 'Land';
            this.form.elements.mana.disabled = type === 'Land';
            $('undo-field').hidden = type !== 'Instant';
            this.form.elements.is_undo.disabled = type !== 'Instant';
            document.querySelectorAll('#card-types button').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.type === type)));
            $('keyword-list').replaceChildren();
            for (const keyword of keywords[type]) {
                const label = document.createElement('label');
                const input = document.createElement('input');
                input.type = 'checkbox';
                input.name = 'buff';
                input.value = keyword;
                input.checked = draft.buff.includes(keyword);
                label.append(input, keyword.replaceAll('_', ' ').replace(/^./, character => character.toUpperCase()));
                $('keyword-list').append(label);
            }
            $('selector_function').replaceChildren(...cardEvents[type].map(event => new Option(eventLabels[event], event)));
            $('selector_target').value = draft.target;
            this.selectEvent(draft.event);
            this.renderArtwork();
            this.updateHeading();
            this.status('Create a card, then try it on the battlefield.');
        }

        selectEvent(event) {
            this.current.event = event;
            $('selector_function').value = event;
            this.loading = true;
            if (this.code) {
                if (!this.current.codes.has(event)) this.current.codes.set(event, new CodeMirror.Doc('', 'python'));
                this.code.swapDoc(this.current.codes.get(event));
            } else this.textarea.value = this.current.codes.get(event) || '';
            this.loading = false;
            const targeted = this.isTargetEvent();
            $('selector_target').disabled = !targeted;
            $('target-note').textContent = targeted ? 'Access your chosen target with selected_object[0].' : 'Target selection applies when this card ' + (['Creature', 'Land'].includes(this.type) ? 'enters the battlefield.' : 'resolves.');
            $('event-label').textContent = eventLabels[event];
            $('code-status').textContent = 'Drag a block into the code, or click it to insert.';
            this.renderSnippets();
            this.updateHeading();
            this.code?.refresh();
        }

        isTargetEvent() { return ['when_enter_battlefield', 'card_ability'].includes(this.current.event); }

        codeValue(event) {
            const value = this.current.codes.get(event);
            return this.code ? value?.getValue() || '' : value || '';
        }

        showPanel(panel) {
            for (const name of ['details', 'abilities', 'artwork']) $('panel-' + name).hidden = name !== panel;
            document.querySelectorAll('[data-panel]').forEach(button => {
                if (button.dataset.panel === panel) button.setAttribute('aria-current', 'page');
                else button.removeAttribute('aria-current');
            });
            if (panel === 'abilities') this.code?.refresh();
        }

        changed() {
            this.current.dirty = true;
            this.updateHeading();
        }

        updateHeading() {
            $('editor-title').textContent = this.current.name.trim() || 'New Card';
            $('code-drop-zone').dataset.empty = String(!this.codeValue(this.current.event).trim());
            $('ability-count').textContent = cardEvents[this.type].filter(event => this.codeValue(event).trim()).length;
            for (const option of $('selector_function').options) {
                option.textContent = eventLabels[option.value] + (this.codeValue(option.value).trim() ? ' •' : '');
            }
        }

        reset() {
            this.drafts[this.type] = this.makeDraft(this.type);
            this.selectType(this.type);
            this.showPanel('details');
            this.form.elements.name.focus();
        }

        blockReason(snippet) {
            if (['damage', 'target-damage', 'sweep', 'random'].includes(snippet.id) && ['when_harm_is_done', 'when_an_object_hert'].includes(this.current.event)) return 'Use another event to avoid repeated damage triggering itself.';
            if (snippet.permanent && !['Creature', 'Land'].includes(this.type)) return 'Available for creatures and lands.';
            if (snippet.counter && (this.type !== 'Instant' || !this.current.is_undo)) return 'Enable Counter spell in Instant details.';
            if (!snippet.target) return '';
            if (!this.isTargetEvent()) return 'Choose the entry or spell resolution event first.';
            if (!this.current.target) return 'Choose a target above first.';
            if (snippet.target === 'creature' && !this.current.target.endsWith('creatures')) return 'Choose a creature-only target.';
            if (this.current.target.endsWith('lands')) return 'Choose a creature or player target.';
            return '';
        }

        renderSnippets() {
            const query = $('block-search').value.trim().toLowerCase();
            const amount = Math.max(1, Math.min(99, Number($('block-amount').value) || 2));
            $('snippet-list').replaceChildren();
            for (const snippet of snippets.filter(item => (item.name + ' ' + item.note).toLowerCase().includes(query))) {
                const reason = this.blockReason(snippet);
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'snippet';
                button.dataset.snippet = snippet.id;
                button.disabled = Boolean(reason);
                button.draggable = !reason;
                button.title = reason || snippet.code(amount);
                const content = document.createElement('span');
                const name = document.createElement('strong');
                name.textContent = snippet.name;
                const note = document.createElement('small');
                note.textContent = reason || snippet.note;
                content.append(name, note);
                button.append(content);
                button.addEventListener('click', () => this.insertSnippet(snippet));
                button.addEventListener('dragstart', event => {
                    event.dataTransfer.setData('application/x-magic-studio-block', snippet.id);
                    event.dataTransfer.effectAllowed = 'copy';
                });
                button.addEventListener('dragend', () => $('code-drop-zone').classList.remove('drag-over'));
                $('snippet-list').append(button);
            }
            if (!$('snippet-list').children.length) $('snippet-list').textContent = 'No matching effects.';
        }

        bindDrop() {
            const zone = $('code-drop-zone');
            const isBlock = event => [...event.dataTransfer.types].includes('application/x-magic-studio-block');
            zone.addEventListener('dragover', event => {
                if (!isBlock(event)) return;
                event.preventDefault();
                event.dataTransfer.dropEffect = 'copy';
                zone.classList.add('drag-over');
            });
            zone.addEventListener('dragleave', event => {
                if (!zone.contains(event.relatedTarget)) zone.classList.remove('drag-over');
            });
            zone.addEventListener('drop', event => {
                if (!isBlock(event)) return;
                event.preventDefault();
                event.stopPropagation();
                zone.classList.remove('drag-over');
                const snippet = snippets.find(item => item.id === event.dataTransfer.getData('application/x-magic-studio-block'));
                const position = this.code?.coordsChar({ left: event.clientX, top: event.clientY }, 'window');
                if (snippet) this.insertSnippet(snippet, position);
            }, true);
        }

        insertSnippet(snippet, position) {
            if (this.busy || this.blockReason(snippet)) return;
            const amountInput = $('block-amount');
            if (!amountInput.reportValidity()) return;
            const value = this.codeValue(this.current.event);
            const lines = value.split('\n');
            const lineNumber = this.code ? (position || this.code.getCursor()).line : value.slice(0, this.textarea.selectionStart).split('\n').length - 1;
            const line = lines[lineNumber] || '';
            const indent = (line.match(/^\s*/)[0] || '') + (line.trimEnd().endsWith(':') ? '    ' : '');
            const blank = !line.trim();
            const inserted = (blank ? '' : '\n') + snippet.code(Number(amountInput.value)).split('\n').map(text => indent + text).join('\n') + '\n' + indent;
            if (this.code) {
                const from = { line: lineNumber, ch: blank ? 0 : line.length };
                this.code.replaceRange(inserted, from, { line: lineNumber, ch: line.length }, 'studio-block');
                const end = this.code.posFromIndex(this.code.indexFromPos(from) + inserted.length);
                this.code.setCursor(end);
                this.code.focus();
                this.code.scrollIntoView(end, 30);
                if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
                    const mark = this.code.markText(from, end, { className: 'code-inserted' });
                    setTimeout(() => mark.clear(), 750);
                }
            } else {
                if (!this.fallbackHistory.has(this.current)) this.fallbackHistory.set(this.current, new Map());
                const history = this.fallbackHistory.get(this.current).get(this.current.event) || [];
                history.push({ value, cursor: this.textarea.selectionStart });
                this.fallbackHistory.get(this.current).set(this.current.event, history.slice(-50));
                const index = lines.slice(0, lineNumber).reduce((length, text) => length + text.length + 1, 0);
                const start = index + (blank ? 0 : line.length);
                this.textarea.setRangeText(inserted, start, index + line.length, 'end');
                this.current.codes.set(this.current.event, this.textarea.value);
                this.textarea.focus();
                this.changed();
            }
            $('code-status').textContent = snippet.name + ' inserted. Edit the code or use Undo.';
        }

        bindArtwork() {
            $('art-file').addEventListener('change', event => this.loadArtwork(event.target.files[0]));
            const zone = $('art-drop-zone');
            zone.addEventListener('keydown', event => {
                if (event.target === zone && ['Enter', ' '].includes(event.key)) {
                    event.preventDefault();
                    $('art-file').click();
                }
            });
            zone.addEventListener('dragover', event => {
                event.preventDefault();
                zone.classList.add('drag-over');
            });
            zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
            zone.addEventListener('drop', event => {
                event.preventDefault();
                zone.classList.remove('drag-over');
                this.loadArtwork(event.dataTransfer.files[0]);
            });
        }

        async loadArtwork(file) {
            if (!file || this.busy) return;
            if (!file.type.startsWith('image/')) {
                $('art-status').textContent = 'Choose an image file.';
                $('art-status').dataset.state = 'error';
                return;
            }
            const draft = this.current;
            const version = ++draft.artVersion;
            draft.artLoading = true;
            $('art-status').textContent = 'Preparing illustration…';
            $('art-status').dataset.state = '';
            const url = URL.createObjectURL(file);
            try {
                const image = new Image();
                image.src = url;
                await image.decode();
                const canvas = document.createElement('canvas');
                canvas.width = canvas.height = 1024;
                const scale = Math.max(1024 / image.naturalWidth, 1024 / image.naturalHeight);
                const width = image.naturalWidth * scale, height = image.naturalHeight * scale;
                canvas.getContext('2d').drawImage(image, (1024 - width) / 2, (1024 - height) / 2, width, height);
                if (version !== draft.artVersion) return;
                draft.art = canvas.toDataURL('image/jpeg');
                draft.file = file;
                draft.dirty = true;
                if (this.current === draft) this.renderArtwork();
            } catch {
                if (this.current === draft && version === draft.artVersion) {
                    $('art-status').textContent = 'This image could not be read. Choose another file.';
                    $('art-status').dataset.state = 'error';
                }
            } finally {
                URL.revokeObjectURL(url);
                if (version === draft.artVersion) draft.artLoading = false;
                $('art-file').value = '';
            }
        }

        renderArtwork() {
            $('art-preview').hidden = !this.current.art;
            if (this.current.art) $('art-preview').src = this.current.art;
            else $('art-preview').removeAttribute('src');
            $('art-status').textContent = this.current.file?.name || 'Add an illustration before testing or submitting.';
            $('art-status').dataset.state = '';
        }

        payload() {
            const draft = this.current;
            const data = {
                init_name: draft.name.trim(), init_type: this.type, init_mana_cost: this.type === 'Land' ? '' : draft.mana.trim(),
                init_color: draft.color, init_type_card: this.type === 'Creature' ? draft.type_creature.trim() : this.type,
                init_rarity: draft.rarity, init_content: draft.description.trim(), init_image_path: draft.art,
                init_keyword_list: draft.buff, select_object_range: draft.target
            };
            if (this.type === 'Creature') Object.assign(data, {
                init_actual_live: Number(draft.health), init_actual_power: Number(draft.attack), init_type_creature: draft.type_creature.trim()
            });
            if (this.type === 'Instant') data.is_undo = draft.is_undo;
            for (const event of cardEvents[this.type]) {
                const body = this.codeValue(event).replace(/\t/g, '    ');
                // The backend wraps this body in async def user_code().
                data[event + '_function'] = body.trim() ? body.split('\n').map(line => '    ' + line).join('\n') : '';
            }
            return data;
        }

        validate() {
            for (const field of this.form.querySelectorAll('[name]')) {
                if (field.disabled) continue;
                if (field.required && !field.value.trim()) field.setCustomValidity('Please fill out this field.');
                else field.setCustomValidity('');
                if (!field.checkValidity()) {
                    this.showPanel('details');
                    field.reportValidity();
                    this.status('Check the highlighted card detail.', 'error');
                    return false;
                }
            }
            if (this.current.artLoading || !this.current.art || !this.current.file) {
                this.showPanel('artwork');
                $('art-drop-zone').focus();
                this.status(this.current.artLoading ? 'Wait for your illustration to finish loading.' : 'Choose a card illustration before continuing.', 'error');
                return false;
            }
            for (const event of cardEvents[this.type]) {
                if (/\bselected_object\b/.test(this.codeValue(event)) && (!['when_enter_battlefield', 'card_ability'].includes(event) || !this.current.target)) {
                    this.showPanel('abilities');
                    this.selectEvent(event);
                    this.status('This code uses selected_object. Choose a target and use the entry or spell resolution event.', 'error');
                    return false;
                }
            }
            return true;
        }

        status(message, state = '') {
            $('editor-status').textContent = message;
            $('editor-status').dataset.state = state;
        }

        async send(submit) {
            if (this.busy || !this.validate()) return;
            if (!submit && !window.StudioWorkspace?.connected()) {
                this.status('The test room is not connected yet. Wait, or reload to reconnect.', 'error');
                return;
            }
            const data = this.payload();
            this.busy = true;
            const controls = [...document.querySelectorAll('#editor button, #card-form input, #card-form select, #card-form textarea')];
            const disabled = controls.map(control => control.disabled);
            controls.forEach(control => { control.disabled = true; });
            this.code?.setOption('readOnly', true);
            $('editor').setAttribute('aria-busy', 'true');
            const action = submit ? $('submit-card') : $('test-card');
            const oldLabel = action.textContent;
            action.textContent = submit ? 'Submitting…' : 'Adding to hand…';
            this.status(submit ? 'Submitting your card…' : 'Sending your card to the battlefield…');
            try {
                let body, headers;
                if (submit) {
                    body = new FormData();
                    body.append('json_data', JSON.stringify(data));
                    body.append('file', this.current.file);
                } else {
                    body = JSON.stringify(data);
                    headers = { 'Content-Type': 'application/json' };
                }
                const response = await fetch(submit ? '/submit_studio_card' : '/add_studio_card', { method: 'POST', headers, body });
                const result = await response.json().catch(() => { throw new Error('The server could not process this request. Please try again.'); });
                if (!response.ok || result.state !== 'successful') throw new Error(result.error || (result.state === 'no studio room found' ? 'The test room has expired. Reload to reconnect.' : 'The card could not be saved. Please try again.'));
                if (submit) {
                    this.current.dirty = false;
                    this.status('Card submitted successfully.', 'success');
                } else {
                    this.status(data.init_name + ' added to your hand. Play it on the battlefield.', 'success');
                    if (document.body.dataset.view === 'editor') window.StudioWorkspace.setView('split');
                    if (matchMedia('(max-width: 900px)').matches) $('canvasContainer').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
                }
            } catch (error) {
                this.status(error.message || 'The request failed. Please try again.', 'error');
            } finally {
                this.busy = false;
                controls.forEach((control, index) => { control.disabled = disabled[index]; });
                this.code?.setOption('readOnly', false);
                $('editor').removeAttribute('aria-busy');
                action.textContent = oldLabel;
            }
        }
    }

    document.addEventListener('DOMContentLoaded', () => new Editor());
})();
