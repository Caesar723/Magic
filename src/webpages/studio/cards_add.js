class Card_Add {
    constructor(socket, feedback) {
        this.socket = socket;
        this.feedback = feedback;
        this.destination = 'hand';
        this.type = 'Creature';
        this.cards = {};
        this.list = document.getElementById('card_list');
        this.status = document.getElementById('library-status');
        this.search = document.getElementById('library-search');
        this.search.addEventListener('input', () => this.render());
        document.querySelectorAll('[data-dest]').forEach(button => button.addEventListener('click', () => {
            this.destination = button.dataset.dest;
            document.querySelectorAll('[data-dest]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
            document.getElementById('destination-hint').textContent = this.destination === 'library' ? 'Added to the bottom of your library.' : 'Added to your ' + this.destination + '.';
            this.render();
        }));
        this.ready = this.send_request();
        window.PageTransition?.wait(this.ready);
    }

    async send_request() {
        this.status.textContent = 'Loading cards…';
        try {
            const response = await fetch('/get_all_cards_name', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
            if (!response.ok) throw new Error('Could not load cards.');
            this.cards = (await response.json()).card_names;
            const types = document.getElementById('type_list');
            types.replaceChildren();
            for (const type of ['Creature', 'Instant', 'Land', 'Sorcery']) {
                const button = document.createElement('button');
                button.type = 'button';
                button.textContent = type;
                button.dataset.type = type;
                button.addEventListener('click', () => {
                    this.type = type;
                    this.render();
                });
                types.append(button);
            }
            this.render();
        } catch {
            this.status.textContent = 'Could not load the card library. ';
            const retry = document.createElement('button');
            retry.type = 'button';
            retry.textContent = 'Try again';
            retry.addEventListener('click', () => this.send_request());
            this.status.append(retry);
        }
    }

    render() {
        const paths = { Creature: 'creature', Instant: 'Instant', Land: 'land', Sorcery: 'sorcery' };
        const query = this.search.value.trim().toLowerCase();
        const names = (this.cards[this.type] || []).filter(name => name.toLowerCase().includes(query));
        document.querySelectorAll('#type_list button').forEach(button => {
            button.setAttribute('aria-pressed', String(button.dataset.type === this.type));
        });
        this.list.replaceChildren();
        for (const name of names) {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'library-card';
            button.title = 'Add ' + name + ' to your ' + this.destination;
            button.dataset.roomCommand = '';
            button.disabled = !window.StudioWorkspace?.connected();
            const image = document.createElement('img');
            image.loading = 'lazy';
            image.alt = '';
            image.src = '/cards/' + paths[this.type] + '/' + encodeURIComponent(name) + '/compress_img.jpg';
            const label = document.createElement('span');
            label.textContent = name;
            button.append(image, label);
            button.addEventListener('click', () => this.add_card(this.type, name));
            this.list.append(button);
        }
        this.status.textContent = names.length ? names.length + ' cards · click to add to your ' + this.destination : 'No cards found.';
    }

    add_card(type, name) {
        const quantity = document.getElementById('labCardQuantity');
        if (!quantity.reportValidity()) return;
        if (this.socket.readyState !== WebSocket.OPEN || !window.StudioWorkspace?.connected()) {
            this.status.textContent = 'The test room is not connected. Reload to reconnect.';
            this.feedback?.(this.status.textContent, 'error');
            return;
        }
        try {
            this.socket.send([window.dataFromBackend.self, 'add_card', [name, type, Number(quantity.value), this.destination].join('+')].join('|'));
            this.status.textContent = 'Sent: ' + Number(quantity.value) + ' × ' + name + ' → your ' + this.destination + '.';
            this.feedback?.(this.status.textContent);
        } catch {
            this.status.textContent = 'Could not send this card. Check the room connection.';
            this.feedback?.(this.status.textContent, 'error');
        }
    }
}
