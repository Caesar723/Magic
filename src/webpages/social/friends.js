const pages = new Set(['/', '/draw_card', '/deck_building', '/shop', '/task', '/studio', '/rogue/rogue_map', '/gaming', '/gaming_ai', '/gaming_rogue', '/game_replay']);
const battlePages = new Set(['/gaming', '/gaming_ai', '/gaming_rogue']);
const errors = {
    authentication_required: 'Sign in to use Friends.', invalid_authentication: 'Your session expired. Sign in again.',
    cannot_add_self: 'You cannot add yourself.', user_not_found: 'This player is no longer available.',
    already_friends: 'You are already friends.', incoming_request_exists: 'This player has already sent you a request. Open Requests.',
    stale_request: 'This request changed. The list has been refreshed.', request_already_processed: 'This request was already handled.',
    request_not_found: 'This request is no longer available.', not_friends: 'You need to be friends first.', friend_not_found: 'This friendship is no longer available.',
    player_busy: 'One of you is in a match or matchmaking. Try again when both are free.', invalid_deck: 'Choose a saved, nonempty deck.',
    pending_invitation_exists: 'A challenge between you is already waiting. Open Duels.', invitation_already_processed: 'This challenge was already handled.',
    invitation_not_found: 'This challenge is no longer available.', cannot_process_invitation: 'This challenge is not available to you.',
    invalid_message: 'Write a message of 1–2,000 characters.', client_id_conflict: 'This message could not be retried.',
    invitation_id_conflict: 'This challenge changed. Close it and try again.', accepted_deck_conflict: 'This challenge was already accepted with another deck.'
};
const element = (tag, className, text) => Object.assign(document.createElement(tag), {className, ...(text === undefined ? {} : {textContent: text})});
const time = value => Date.parse(/[zZ]$|[+-]\d\d:\d\d$/.test(value || '') ? value : `${value}Z`);
const uuid = () => {
    if (crypto.randomUUID) return crypto.randomUUID();
    const bytes = crypto.getRandomValues(new Uint8Array(16)); bytes[6] = bytes[6] & 15 | 64; bytes[8] = bytes[8] & 63 | 128;
    return [...bytes].map((value, index) => `${[4, 6, 8, 10].includes(index) ? '-' : ''}${value.toString(16).padStart(2, '0')}`).join('');
};

const glyphs = {
    friends: '<path d="M4 26V10l12-5 12 5v16l-12-4zM16 5v17M4 10l12 5 12-5"/><path d="m10 7 6-4 6 4M9 18l3 1m8 0 3-1"/>',
    requests: '<path d="M3 9h26v17H3zM3 9l13 10L29 9M9 5h14"/>',
    find: '<circle cx="13" cy="13" r="8"/><path d="m19 19 9 9M13 9v8m-4-4h8"/>',
    duels: '<path d="m5 3 7 3 12 18m-9-5 6-4M27 3l-7 3L8 24m9-5-6-4M4 28l6-7m18 7-6-7"/>',
    crest: '<path d="m16 2 4 10 10 4-10 4-4 10-4-10-10-4 10-4zM16 9v14M9 16h14"/><circle cx="16" cy="16" r="10"/>',
    refresh: '<path d="M26 12a11 11 0 0 0-19-5L3 11m0-8v8h8M6 20a11 11 0 0 0 19 5l4-4m0 8v-8h-8"/>'
};
const glyph = name => `<svg viewBox="0 0 32 32" aria-hidden="true">${glyphs[name]}</svg>`;

// One isolated panel per document. All identity, permissions and game creation stay on the server.
class FriendsPanel {
    constructor() {
        this.host = document.createElement('magic-friends'); this.host.id = 'magic-friends';
        this.host.toggleAttribute('battle', battlePages.has(location.pathname) || location.pathname === '/game_replay');
        this.root = this.host.attachShadow({mode: 'open'}); this.$ = selector => this.root.querySelector(selector);
        this.account = document.querySelector('script[data-social-account]')?.dataset.socialAccount || window.dataFromBackend?.self || '';
        this.storageKey = `magic-friends:${this.account || 'session'}`;
        try { this.saved = JSON.parse(sessionStorage.getItem(this.storageKey)) || {}; } catch (_) { this.saved = {}; }
        this.open = Boolean(this.saved.open); this.tab = ['friends', 'requests', 'find', 'duels'].includes(this.saved.tab) ? this.saved.tab : 'friends';
        this.drafts = this.account ? this.saved.drafts || {} : {}; this.preferredDeck = this.saved.deck;
        this.friends = new Map(); this.people = new Map(); this.chats = new Map(); this.unread = new Map();
        this.incoming = []; this.outgoing = []; this.invitations = []; this.seenMessages = new Set(); this.controllers = new Set();
        this.authorized = true; this.attempt = 0; this.searchRun = 0; this.pending = new Set(); this.loading = true; this.inviteVersion = 0; this.readySeen = new Set(); this.friendLimit = 50;
        const style = document.createElement('link'); style.rel = 'stylesheet'; style.href = new URL('./friends.css', import.meta.url).href; this.root.append(style);
        const view = element('div', 'social-root');
        view.innerHTML = `<button class="launcher" aria-label="Open Friends" aria-expanded="false" aria-controls="friends-panel">${glyph('friends')}<span>Friends</span><b class="badge" hidden></b></button>
            <aside id="friends-panel" class="panel" role="dialog" aria-modal="false" aria-labelledby="friends-title" hidden>
                <header class="panel-heading"><span class="cover-seal">${glyph('crest')}</span><h2 id="friends-title">Friends</h2><div class="heading-tools"><button data-action="refresh" class="icon reconnect" aria-label="Reconnect" title="Reconnect" hidden>${glyph('refresh')}</button><button data-action="close" class="icon" aria-label="Close Friends">×</button></div></header>
                <div class="panel-body">
                <p class="notice" role="status" aria-live="polite" hidden></p>
                <div class="auth" hidden><p>Sign in to use Friends.</p><a href="/login">Sign in →</a></div>
                <section class="directory section" data-section="friends"><div class="friend-list"></div><button data-action="more-friends" class="text-button" hidden>More friends ↓</button><button data-tab="find" class="add-friend">${glyph('find')}<span>Add friend</span></button></section>
                <section class="requests section" data-section="requests" hidden><h3>Received</h3><div class="incoming-list"></div><h3>Sent</h3><div class="outgoing-list"></div></section>
                <section class="find section" data-section="find" hidden><form class="search-form"><label for="friend-search">Find a player</label><div><input id="friend-search" name="keyword" type="search" maxlength="64" placeholder="Player name" autocomplete="off"><button type="submit">Search</button></div></form><div class="search-results"><p class="empty">Search for a player.</p></div><button class="more-search text-button" data-action="more-search" hidden>More players ↓</button></section>
                <section class="duels section" data-section="duels" hidden><div class="invitation-list"></div><button data-action="more-duels" class="text-button" hidden>Older challenges ↓</button></section>
                <section class="chat" aria-label="Conversation" hidden><header class="chat-heading"><button data-action="back" class="icon" aria-label="Back to friends">←</button><div><h3></h3><small class="chat-relation" hidden></small></div><button data-action="challenge-peer" class="duel-button">${glyph('duels')}<span>Duel</span></button></header><button data-action="older" class="older text-button" hidden>Older messages ↑</button><div class="messages" role="log" aria-label="Messages" tabindex="0"></div><button data-action="latest" class="latest text-button" hidden>New messages ↓</button><form class="compose"><label class="sr-only" for="friend-message">Message</label><textarea id="friend-message" rows="2" maxlength="4000" placeholder="Write a message…"></textarea><div><small class="character-count" hidden>0 / 2,000</small><button type="submit">Send →</button></div></form></section>
                <section class="deck-picker section" aria-label="Choose challenge deck" hidden><button data-action="close-decks" class="text-button">← Back</button><h3></h3><label for="friend-deck">Your deck</label><select id="friend-deck"></select><p class="deck-summary"></p><a href="/deck_building">Build or edit a deck ↗</a><button data-action="confirm-duel" class="primary">Send challenge →</button></section>
                </div>
                <nav class="tabs" aria-label="Friends sections">${[['friends', 'Friends'], ['requests', 'Requests'], ['find', 'Find'], ['duels', 'Duels']].map(([id, label]) => `<button data-tab="${id}">${glyph(id)}<span>${label}</span><b hidden></b></button>`).join('')}</nav>
            </aside><button class="toast" hidden></button>`;
        this.root.append(view); document.body.append(this.host); this.bind(); this.selectTab(this.tab, false); this.show(this.open, false);
        (this.refreshing || this.refresh()).then(() => {
            const id = Number(this.saved.peer);
            if (this.open && this.tab === 'friends' && this.friends.has(id)) this.openChat(this.friends.get(id), false);
        });
        this.connect();
    }
    save() {
        try { sessionStorage.setItem(this.storageKey, JSON.stringify({open: this.open, tab: this.tab, peer: this.peer?.user_id, deck: this.preferredDeck, ...(this.account ? {drafts: this.drafts} : {})})); } catch (_) {}
    }
    bind() {
        this.$('.launcher').addEventListener('click', () => this.show(!this.open));
        this.root.addEventListener('click', event => {
            const link = event.target.closest('a[href]');
            if (link && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey && event.button === 0 && window.PageTransition) { event.preventDefault(); window.PageTransition.navigate(link.href); return; }
            const button = event.target.closest('button'); if (!button || button.disabled) return;
            if (button.dataset.tab) return this.selectTab(button.dataset.tab);
            if (button.dataset.action) this.act(button).catch(error => this.report(error));
        });
        this.root.addEventListener('keydown', event => {
            event.stopPropagation();
            if (event.key === 'Escape') { event.preventDefault(); this.show(false); }
        });
        this.$('.search-form').addEventListener('submit', event => { event.preventDefault(); clearTimeout(this.searchTimer); this.search(); });
        this.$('#friend-search').addEventListener('input', () => { clearTimeout(this.searchTimer); this.searchRun++; this.searchTimer = setTimeout(() => this.search(), 350); });
        this.$('.compose').addEventListener('submit', event => { event.preventDefault(); this.sendMessage(); });
        this.$('#friend-message').addEventListener('input', () => {
            if (this.peer) this.drafts[this.peer.user_id] = this.$('#friend-message').value;
            this.updateComposer(); this.save();
        });
        this.$('#friend-message').addEventListener('keydown', event => {
            if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); this.sendMessage(); }
        });
        this.$('.messages').addEventListener('scroll', () => { if (this.atBottom()) { this.$('.latest').hidden = true; this.markRead(); } });
        window.addEventListener('focus', () => { this.markRead(); if (!this.socket && !this.suspended) this.connect(); });
        document.addEventListener('visibilitychange', () => {
            this.tick(); if (!document.hidden) { this.connect(); this.refresh(); this.syncChat(); }
        });
        window.addEventListener('online', () => { this.attempt = 0; this.connect(); this.refresh(); this.syncChat(); });
        window.addEventListener('offline', () => { this.connection('offline'); this.closeSocket(); });
        window.addEventListener('pagehide', () => {
            this.save(); this.suspended = true; this.closeSocket();
            for (const timer of ['retryTimer', 'pollTimer', 'tickTimer', 'expiryTimer', 'refreshTimer', 'unreadTimer', 'toastTimer', 'searchTimer']) clearTimeout(this[timer]);
            for (const controller of this.controllers) controller.abort();
        });
        window.addEventListener('pageshow', event => { if (event.persisted) { this.suspended = false; this.connect(); this.refresh(); this.syncChat(); this.tick(); } });
        document.addEventListener('lobby:deck-selected', event => { this.preferredDeck = Number(event.detail[0]); this.save(); });
        const viewport = () => {
            const size = window.visualViewport; if (!size) return;
            this.host.toggleAttribute('keyboard', Boolean(this.root.activeElement?.matches('input, textarea, select') && size.height < innerHeight - 100));
            this.host.style.setProperty('--viewport-height', `${size.height}px`); this.host.style.setProperty('--viewport-top', `${size.offsetTop}px`);
        };
        window.visualViewport?.addEventListener('resize', viewport); this.root.addEventListener('focusin', viewport); this.root.addEventListener('focusout', () => setTimeout(viewport, 0));
    }
    async request(path, {method = 'GET', body, social = true} = {}) {
        const controller = new AbortController(); this.controllers.add(controller); const timeout = setTimeout(() => controller.abort(), 15000);
        try {
            const response = await fetch(`${social ? '/social' : ''}${path}`, {method, credentials: 'same-origin', redirect: 'error', signal: controller.signal,
                ...(body === undefined ? {} : {headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})});
            const data = await response.json().catch(() => null);
            if (!response.ok) {
                if (response.status === 401) { this.authorized = false; this.closeSocket(); this.$('.auth').hidden = false; this.connection('offline'); }
                const error = new Error(errors[data?.detail?.code] || (response.status === 422 ? 'Check the entered information and try again.' : 'Unable to complete this action. Please retry.'));
                error.code = data?.detail?.code; error.status = response.status; throw error;
            }
            if (data === null) throw new Error('Unexpected response. Refresh or sign in again.');
            return data;
        } catch (error) {
            if (error.name === 'AbortError' || error instanceof TypeError) throw new Error('Connection interrupted. Retry when you are online.');
            throw error;
        } finally { clearTimeout(timeout); this.controllers.delete(controller); }
    }
    async all(path, limit = 100) {
        const result = [];
        for (let offset = 0; ; offset += limit) {
            const page = await this.request(`${path}?offset=${offset}&limit=${limit}`);
            if (!Array.isArray(page)) throw new Error('Unable to read the friend list.');
            result.push(...page); if (page.length < limit) return result;
        }
    }
    async loadInvitations(older = false) {
        const rows = []; let page;
        do {
            page = await this.request(`/battle-invitations?offset=${(older ? this.inviteOffset || 0 : 0) + rows.length}&limit=30`);
            rows.push(...page);
        } while (page.length === 30 && time(page.at(-1).expires_at) > Date.now());
        this.inviteOffset = (older ? this.inviteOffset || 0 : 0) + rows.length; this.moreInvites = page.length === 30;
        return rows;
    }
    async refresh() {
        if (!this.authorized || this.suspended) return;
        if (this.refreshing) { this.refreshAgain = true; return this.refreshing; }
        this.refreshing = (async () => {
            const inviteVersion = this.inviteVersion;
            const results = await Promise.allSettled([this.all('/friends'), this.all('/friend-requests/incoming'), this.all('/friend-requests/outgoing'), this.request('/chats/unread'), this.loadInvitations()]);
            const names = ['friends', 'incoming', 'outgoing', 'unread', 'invitations'];
            results.forEach((result, index) => {
                if (result.status !== 'fulfilled') return;
                const value = result.value;
                if (index === 4 && inviteVersion !== this.inviteVersion) {
                    const current = new Map(this.invitations.map(row => [row.id, row]));
                    this.invitations = [...value.map(row => current.get(row.id) || row), ...this.invitations.filter(row => !value.some(fresh => fresh.id === row.id))];
                } else this[names[index]] = index === 0 ? new Map(value.map(user => [user.user_id, user])) : index === 3 ? new Map(value.map(row => [row.user_id, row.count])) : value;
            });
            for (const user of [...this.friends.values(), ...this.incoming, ...this.outgoing]) this.people.set(user.user_id, user);
            this.loading = false; this.renderLists(); this.renderInvitations(); this.updateBadge(); this.updateComposer();
            const failure = results.find(result => result.status === 'rejected');
            if (failure && this.open) this.report(failure.reason);
        })().finally(() => { this.refreshing = null; if (this.refreshAgain) { this.refreshAgain = false; this.scheduleRefresh(); } });
        return this.refreshing;
    }
    scheduleRefresh() { clearTimeout(this.refreshTimer); this.refreshTimer = setTimeout(() => this.refresh(), 200); }
    refreshUnread() {
        clearTimeout(this.unreadTimer); this.unreadTimer = setTimeout(async () => {
            try { const rows = await this.request('/chats/unread'); this.unread = new Map(rows.map(row => [row.user_id, row.count])); this.updateBadge(); this.renderFriends(); } catch (_) {}
        }, 200);
    }
    show(open, focus = true) {
        this.open = open; this.$('.panel').hidden = !open; this.$('.launcher').setAttribute('aria-expanded', String(open));
        this.$('.launcher').setAttribute('aria-label', open ? 'Close Friends' : 'Open Friends');
        if (open) { this.$('.toast').hidden = true; this.refresh(); if (focus) this.$('[data-action="close"]').focus(); this.syncChat(); }
        else if (focus) this.$('.launcher').focus();
        this.tick(); this.save();
    }
    selectTab(tab, focus = true) {
        this.tab = tab; this.peer = null; this.duel = null; this.$('.notice').hidden = true;
        for (const button of this.root.querySelectorAll('.friend-open')) button.setAttribute('aria-current', 'false');
        for (const section of this.root.querySelectorAll('[data-section]')) section.hidden = section.dataset.section !== tab;
        for (const button of this.root.querySelectorAll('.tabs button')) button.setAttribute('aria-current', String(button.dataset.tab === tab));
        this.$('.chat').hidden = this.$('.deck-picker').hidden = true; this.save();
        if (tab === 'find' && focus) this.$('#friend-search').focus();
        if (tab === 'duels') { for (const row of this.invitations) if (row.active) this.readySeen.add(row.id); this.updateBadge(); }
    }
    report(error) { if (this.suspended) return; this.$('.notice').textContent = error.message || 'Please try again.'; this.$('.notice').hidden = false; }
    connection(state) { this.$('.reconnect').hidden = state === 'live' || !this.authorized; }
    button(label, action, id, className = '') {
        const button = element('button', className, label); button.type = 'button'; button.dataset.action = action; if (id !== undefined) button.dataset.id = id; return button;
    }
    empty(container, text) { container.replaceChildren(element('p', 'empty', text)); }
    personRow(user, caption) {
        const row = element('article', 'person'), seal = element('span', 'person-seal', [...user.username].slice(0, 1).join('').toLocaleUpperCase());
        seal.setAttribute('aria-hidden', 'true'); seal.style.setProperty('--seal-tone', ['#637e77', '#a07460', '#6b7989', '#857f61'][user.user_id % 4]);
        const name = element('div', 'person-name'); name.append(element('strong', '', user.username)); if (caption) name.append(element('small', '', caption));
        row.append(seal, name); return row;
    }
    renderFriends() {
        const list = this.$('.friend-list'); list.replaceChildren();
        if (this.loading) return this.empty(list, 'Loading friends…');
        const users = [...this.friends.values(), ...[...this.unread.keys()].filter(id => !this.friends.has(id)).map(id => this.people.get(id) || {user_id: id, username: `Player #${id}`})];
        for (const user of users.slice(0, this.friendLimit)) {
            const count = this.unread.get(user.user_id) || 0, row = this.personRow(user, count ? `${count} new message${count === 1 ? '' : 's'}` : this.friends.has(user.user_id) ? '' : 'Previous conversation');
            const chat = this.button('', 'chat', user.user_id, 'friend-open'); chat.setAttribute('aria-label', `Message ${user.username}`); chat.setAttribute('aria-current', String(this.peer?.user_id === user.user_id)); chat.append(...row.childNodes); row.append(chat);
            if (this.friends.has(user.user_id)) {
                const actions = element('div', 'row-actions'), duel = this.button('', 'challenge', user.user_id, 'duel-button'); duel.innerHTML = `${glyph('duels')}<span>Duel</span>`; duel.title = `Challenge ${user.username}`; duel.disabled = battlePages.has(location.pathname);
                actions.append(duel, this.button('…', 'remove-confirm', user.user_id, 'remove')); actions.lastChild.setAttribute('aria-label', `Remove ${user.username} from friends`); row.append(actions);
            }
            list.append(row);
        }
        if (!users.length) this.empty(list, 'No friends yet.');
        this.$('[data-action="more-friends"]').hidden = users.length <= this.friendLimit;
    }
    renderLists() {
        this.renderFriends();
        for (const [kind, rows, actions] of [['incoming', this.incoming, [['Accept', 'accept'], ['Decline', 'reject']]], ['outgoing', this.outgoing, [['Cancel', 'cancel']]]]) {
            const list = this.$(`.${kind}-list`); list.replaceChildren();
            for (const user of rows) { const row = this.personRow(user), buttons = element('div', 'row-actions'); for (const [label, action] of actions) buttons.append(this.button(label, action, user.user_id)); row.append(buttons); list.append(row); }
            if (!rows.length) this.empty(list, this.loading ? 'Loading requests…' : kind === 'incoming' ? 'No new requests.' : 'No outgoing requests.');
        }
        if (this.searchResults) this.renderSearch();
        for (const button of this.root.querySelectorAll('.tabs button')) button.setAttribute('aria-current', String(button.dataset.tab === this.tab));
    }
    async search(more = false) {
        const query = this.$('#friend-search').value.trim(), run = ++this.searchRun;
        if (!query) { this.searchResults = null; this.$('.more-search').hidden = true; return this.empty(this.$('.search-results'), 'Search for a player.'); }
        const offset = more ? this.searchResults?.length || 0 : 0;
        if (!more) this.empty(this.$('.search-results'), 'Searching…');
        try {
            const rows = await this.request(`/users?keyword=${encodeURIComponent(query)}&offset=${offset}&limit=20`);
            if (run !== this.searchRun) return;
            this.searchResults = more ? [...this.searchResults, ...rows] : rows; this.searchMore = rows.length === 20;
            for (const user of rows) this.people.set(user.user_id, user);
            this.renderSearch();
        } catch (error) { if (run === this.searchRun) this.report(error); }
    }
    renderSearch() {
        const list = this.$('.search-results'); list.replaceChildren();
        for (const user of this.searchResults || []) {
            const state = this.friends.has(user.user_id) ? 'Friend' : this.incoming.some(row => row.user_id === user.user_id) ? 'Request received' : this.outgoing.some(row => row.user_id === user.user_id) ? 'Request sent' : '';
            const row = this.personRow(user, state), button = this.button(state === 'Friend' ? 'Message' : state === 'Request received' ? 'Review' : state === 'Request sent' ? 'Sent' : '+ Add', state === 'Friend' ? 'chat' : state === 'Request received' ? 'requests' : 'add', user.user_id);
            button.disabled = state === 'Request sent'; row.append(button); list.append(row);
        }
        if (!this.searchResults?.length) this.empty(list, 'No players found. Try another name.');
        this.$('.more-search').hidden = !this.searchMore;
    }
    async act(button) {
        const action = button.dataset.action, id = Number(button.dataset.id);
        if (action === 'close') return this.show(false);
        if (action === 'refresh') { this.$('.notice').hidden = true; this.attempt = 0; this.connect(); return this.refresh(); }
        if (action === 'requests') return this.selectTab('requests');
        if (action === 'chat') return this.openChat(this.people.get(id) || {user_id: id, username: `Player #${id}`});
        if (action === 'back') return this.selectTab('friends');
        if (action === 'older') return this.loadChat(true);
        if (action === 'latest') { this.$('.messages').scrollTop = this.$('.messages').scrollHeight; this.$('.latest').hidden = true; return this.markRead(); }
        if (action === 'more-search') return this.search(true);
        if (action === 'more-friends') { this.friendLimit += 50; return this.renderFriends(); }
        if (action === 'more-duels') {
            button.disabled = true;
            try { const rows = await this.loadInvitations(true); this.invitations.push(...rows.filter(row => !this.invitations.some(existing => existing.id === row.id))); this.renderInvitations(); }
            finally { button.disabled = false; }
            return;
        }
        if (action === 'retry-message') return this.deliver(this.peer.user_id, button.dataset.clientId);
        if (action === 'remove-confirm') {
            const row = button.closest('.person'); row.querySelector('.row-actions').replaceChildren(this.button('Remove friend?', 'remove', id, 'danger'), this.button('Keep', 'keep', id)); return;
        }
        if (action === 'keep') return this.renderFriends();
        if (action === 'challenge' || action === 'challenge-peer') return this.chooseDeck({target: action === 'challenge-peer' ? this.peer.user_id : id});
        if (action === 'close-decks') { this.duel = null; return this.selectTab('duels'); }
        if (action === 'confirm-duel') return this.confirmDuel(button);
        if (action === 'accept-duel') return this.chooseDeck({invitation: button.dataset.invitation});
        if (action === 'join') {
            const invitation = this.invitations.find(row => row.id === button.dataset.invitation);
            if (invitation?.active && invitation.game_url === '/gaming' && !battlePages.has(location.pathname)) (window.PageTransition?.navigate || (path => location.assign(path)))('/gaming');
            return;
        }
        const key = `${action}:${button.dataset.id || button.dataset.invitation || ''}`; if (this.pending.has(key)) return;
        this.pending.add(key); for (const sibling of button.closest('.person')?.querySelectorAll('button') || [button]) sibling.disabled = true; this.$('.notice').hidden = true;
        try {
            if (['accept', 'reject', 'cancel'].includes(action)) {
                const request = (action === 'cancel' ? this.outgoing : this.incoming).find(row => row.user_id === id); if (!request) return;
                await this.request(`/friend-requests/${id}/${action}`, {method: 'POST', body: {request_id: request.request_id}});
            } else if (action === 'add') {
                const relation = await this.request('/friend-requests', {method: 'POST', body: {target_user_id: id}});
                this.selfId = relation.user_low_id === id ? relation.user_high_id : relation.user_low_id;
            } else if (action === 'remove') await this.request(`/friends/${id}`, {method: 'DELETE'});
            else if (action === 'reject-duel' || action === 'cancel-duel') await this.request(`/battle-invitations/${encodeURIComponent(button.dataset.invitation)}/${action === 'reject-duel' ? 'reject' : 'cancel'}`, {method: 'POST'});
            await this.refresh();
        } catch (error) { await this.refresh(); throw error; }
        finally { this.pending.delete(key); button.disabled = false; }
    }
    chatState(id) {
        if (!this.chats.has(id)) this.chats.set(id, {messages: new Map(), hasOlder: false, loaded: false, readThrough: 0});
        return this.chats.get(id);
    }
    async openChat(user, focus = true) {
        this.selectTab('friends'); this.peer = user; this.renderFriends(); this.$('.chat').hidden = false;
        this.$('.chat-heading h3').textContent = user.username; this.renderMessages(true); this.$('#friend-message').value = this.drafts[user.user_id] || ''; this.updateComposer(); this.save();
        await this.loadChat(); if (focus && this.peer?.user_id === user.user_id) this.$('#friend-message').focus();
    }
    async loadChat(older = false) {
        if (!this.peer) return;
        const id = this.peer.user_id, chat = this.chatState(id); if (chat.loading) return;
        chat.loading = true;
        if (!chat.loaded) this.empty(this.$('.messages'), 'Opening conversation…');
        const list = this.$('.messages'), height = list.scrollHeight, top = list.scrollTop;
        const ids = [...chat.messages.values()].filter(message => message.id).map(message => message.id);
        try {
            const rows = await this.request(`/chats/${id}/messages?limit=30${older && ids.length ? `&before_id=${Math.min(...ids)}` : ''}`);
            for (const message of rows) { this.identify(message, id); chat.messages.set(message.client_id, message); }
            chat.loaded = true; chat.hasOlder = rows.length === 30;
            if (this.peer?.user_id === id) { this.renderMessages(!older); if (older) list.scrollTop = top + list.scrollHeight - height; }
        } catch (error) { this.report(error); }
        finally { chat.loading = false; }
    }
    identify(message, peer) { this.selfId = message.sender_id === peer ? message.receiver_id : message.sender_id; }
    peerFor(first, second) {
        if (this.selfId) return first === this.selfId ? second : first;
        const peer = this.friends.has(first) ? first : this.friends.has(second) ? second : null;
        if (peer) this.selfId = peer === first ? second : first;
        return peer;
    }
    atBottom() { const list = this.$('.messages'); return list.scrollHeight - list.scrollTop - list.clientHeight < 45; }
    renderMessages(bottom = false) {
        if (!this.peer || !this.open || this.$('.chat').hidden) return;
        const id = this.peer.user_id, chat = this.chatState(id), list = this.$('.messages'), oldTop = list.scrollTop;
        const rows = [...chat.messages.values()].sort((a, b) => a.id && b.id ? a.id - b.id : time(a.created_at) - time(b.created_at)); list.replaceChildren();
        for (const message of rows) {
            const own = message.local || message.sender_id !== id, row = element('article', `message ${own ? 'own' : 'received'}`); row.dataset.message = message.id || message.client_id;
            const body = element('p', '', message.content), meta = element('small', '', `${new Date(time(message.created_at)).toLocaleTimeString('en-GB', {hour: '2-digit', minute: '2-digit', timeZone: 'Europe/London'})}${own ? message.local ? message.failed ? ' · Not sent' : ' · Sending…' : message.read_at ? ' · Read' : ' · Sent' : ''}`);
            row.append(body, meta);
            if (message.failed) { const retry = this.button('Retry', 'retry-message'); retry.dataset.clientId = message.client_id; row.append(retry); }
            list.append(row);
        }
        if (!rows.length) this.empty(list, 'No messages yet. Send the first note.');
        this.$('.older').hidden = !chat.hasOlder;
        if (bottom) { list.scrollTop = list.scrollHeight; this.$('.latest').hidden = true; } else list.scrollTop = oldTop;
        this.markRead();
    }
    updateComposer() {
        if (!this.peer) return;
        const friend = this.friends.has(this.peer.user_id), length = [...this.$('#friend-message').value.trim()].length;
        this.$('.chat-relation').textContent = 'You are no longer friends'; this.$('.chat-relation').hidden = friend;
        this.$('#friend-message').disabled = !friend || !this.authorized;
        this.$('.compose button').disabled = !friend || !this.authorized || !length || length > 2000;
        this.$('.character-count').textContent = `${length.toLocaleString('en')} / 2,000`; this.$('.character-count').hidden = length < 1800;
        this.$('[data-action="challenge-peer"]').disabled = !friend || battlePages.has(location.pathname);
    }
    sendMessage() {
        const content = this.$('#friend-message').value.trim(), id = this.peer?.user_id;
        if (!id || !this.friends.has(id) || !content || [...content].length > 2000) return;
        const clientId = uuid(); this.chatState(id).messages.set(clientId, {client_id: clientId, content, created_at: new Date().toISOString(), local: true});
        this.$('#friend-message').value = ''; delete this.drafts[id]; this.updateComposer(); this.save(); this.renderMessages(true); this.deliver(id, clientId);
    }
    async deliver(id, clientId) {
        const chat = this.chatState(id), message = chat.messages.get(clientId); if (!message?.local || message.sending) return;
        message.sending = true; message.failed = false; if (this.peer?.user_id === id) this.renderMessages(this.atBottom());
        try {
            const result = await this.request(`/chats/${id}/messages`, {method: 'POST', body: {client_id: clientId, content: message.content}});
            this.identify(result, id); chat.messages.set(clientId, result);
        } catch (error) { if (chat.messages.get(clientId)?.local) { message.failed = true; this.report(error); } }
        finally { message.sending = false; if (this.peer?.user_id === id) this.renderMessages(this.atBottom()); }
    }
    async markRead() {
        if (!this.open || !this.peer || this.$('.chat').hidden || document.hidden || !document.hasFocus() || document.querySelector('dialog[open]') || !this.atBottom() || !this.authorized) return;
        const id = this.peer.user_id, chat = this.chatState(id), incoming = [...chat.messages.values()].filter(message => message.sender_id === id && message.id);
        const last = Math.max(0, ...incoming.map(message => message.id)); if (last <= chat.readThrough || chat.reading) return;
        chat.reading = true;
        try { await this.request(`/chats/${id}/read`, {method: 'POST', body: {last_message_id: last}}); chat.readThrough = last; this.refreshUnread(); }
        catch (_) {} finally { chat.reading = false; }
    }
    async syncChat() {
        if (!this.open || !this.peer || this.$('.chat').hidden || !this.authorized || this.suspended) return;
        const id = this.peer.user_id, chat = this.chatState(id); if (!chat.loaded) return this.loadChat();
        let after = Math.max(0, ...[...chat.messages.values()].map(message => message.id || 0)); const bottom = this.atBottom();
        try {
            for (;;) {
                const rows = await this.request(`/chats/${id}/messages?after_id=${after}&limit=100`);
                for (const message of rows) { this.identify(message, id); chat.messages.set(message.client_id, message); after = message.id; }
                if (rows.length < 100) break;
            }
            const recent = await this.request(`/chats/${id}/messages?limit=30`);
            for (const message of recent) chat.messages.set(message.client_id, message);
            if (this.peer?.user_id === id) this.renderMessages(bottom);
        } catch (_) {}
    }
    effective(invitation) { return invitation.status === 'pending' && time(invitation.expires_at) <= Date.now() ? 'expired' : invitation.status; }
    renderInvitations() {
        const list = this.$('.invitation-list'); list.replaceChildren();
        for (const invitation of this.invitations) {
            const peerId = this.peerFor(invitation.sender_id, invitation.receiver_id); if (!peerId) continue;
            const incoming = invitation.receiver_id === this.selfId, user = this.people.get(peerId) || {user_id: peerId, username: `Player #${peerId}`}, status = this.effective(invitation);
            const caption = status === 'pending' ? `${incoming ? 'Invites you' : 'Waiting for a reply'} · ${Math.max(0, Math.ceil((time(invitation.expires_at) - Date.now()) / 1000))}s` : invitation.active ? 'Battle ready' : {accepted: 'Finished', rejected: 'Declined', cancelled: 'Cancelled', expired: 'Expired'}[status] || status;
            const row = this.personRow(user, caption), actions = element('div', 'row-actions');
            if (status === 'pending') { const clock = row.querySelector('small'); clock.dataset.expiry = invitation.expires_at; clock.dataset.prefix = incoming ? 'Invites you' : 'Waiting for a reply'; }
            const add = (label, action) => { const button = this.button(label, action); button.dataset.invitation = invitation.id; actions.append(button); return button; };
            if (status === 'pending') {
                if (incoming) { add('Choose deck', 'accept-duel').disabled = battlePages.has(location.pathname); add('Decline', 'reject-duel'); }
                else add('Cancel', 'cancel-duel');
            } else if (invitation.active && !battlePages.has(location.pathname)) add('Join battle →', 'join');
            row.append(actions); list.append(row);
        }
        if (!list.children.length) this.empty(list, 'No challenges yet.');
        this.$('[data-action="more-duels"]').hidden = !this.moreInvites;
        clearTimeout(this.expiryTimer);
        const pending = this.invitations.filter(row => this.effective(row) === 'pending');
        if (pending.length) this.expiryTimer = setTimeout(() => { this.renderInvitations(); this.updateBadge(); }, Math.max(100, Math.min(...pending.map(row => time(row.expires_at))) - Date.now() + 20));
    }
    async chooseDeck({target, invitation}) {
        if (battlePages.has(location.pathname)) return this.report(new Error(errors.player_busy));
        const item = this.invitations.find(row => row.id === invitation);
        if (invitation && (!item || this.effective(item) !== 'pending')) return this.report(new Error('This invitation expired or changed. Refresh Duels.'));
        const peerId = target || this.peerFor(item.sender_id, item.receiver_id), user = this.people.get(peerId);
        const draft = {target: peerId, invitation, id: invitation || uuid()}; this.duel = draft;
        for (const section of this.root.querySelectorAll('[data-section]')) section.hidden = true;
        this.$('.chat').hidden = true; this.$('.deck-picker').hidden = false; this.$('.notice').hidden = true;
        this.$('.deck-picker h3').textContent = `${invitation ? 'Accept' : 'Challenge'} ${user?.username || `Player #${peerId}`}`;
        this.$('.deck-summary').textContent = 'Loading your decks…'; this.$('[data-action="confirm-duel"]').disabled = true;
        const select = this.$('#friend-deck'); select.replaceChildren(); select.disabled = false;
        try {
            const rows = await this.request('/get_decks_home', {method: 'POST', social: false});
            if (this.duel !== draft) return;
            this.decks = rows.filter(row => Number.isInteger(row.id) && row.id > 0 && row.content?.[1]?.length);
            for (const deck of this.decks) select.append(Object.assign(element('option', '', deck.content[0]), {value: deck.id}));
            if (this.decks.some(deck => deck.id === this.preferredDeck)) select.value = this.preferredDeck;
            const update = () => { const deck = this.decks.find(row => row.id === Number(select.value)); this.$('.deck-summary').textContent = deck ? `${deck.content[1].reduce((sum, card) => sum + Number(card.quantity || 0), 0)} cards` : 'No saved decks yet. Build a deck first.'; this.$('[data-action="confirm-duel"]').disabled = !deck; };
            select.onchange = update; update(); this.$('[data-action="confirm-duel"]').textContent = invitation ? 'Accept challenge →' : 'Send challenge →';
        } catch (error) { if (this.duel === draft) { this.report(error); this.$('.deck-summary').textContent = 'Unable to load decks. Close and retry.'; } }
    }
    async confirmDuel(button) {
        const draft = this.duel; if (!draft || draft.sending) return;
        const select = this.$('#friend-deck'), deckId = draft.deckId || Number(select.value); if (!this.decks?.some(deck => deck.id === deckId)) return;
        draft.deckId = deckId; draft.sending = true; button.disabled = select.disabled = true;
        try {
            const result = await this.request(draft.invitation ? `/battle-invitations/${draft.invitation}/accept` : '/battle-invitations', {method: 'POST', body: draft.invitation ? {deck_id: deckId} : {invitation_id: draft.id, target_user_id: draft.target, deck_id: deckId}});
            this.preferredDeck = deckId; this.upsertInvitation(result); if (this.duel === draft) this.selectTab('duels'); this.renderInvitations(); this.save();
        } catch (error) { if (error.status && error.status < 500) { draft.deckId = null; select.disabled = false; } await this.refresh(); this.report(error); }
        finally { draft.sending = false; button.disabled = false; }
    }
    upsertInvitation(value) { this.inviteVersion++; this.invitations = [value, ...this.invitations.filter(row => row.id !== value.id)]; }
    updateBadge() {
        const duelCount = this.invitations.filter(row => this.peerFor(row.sender_id, row.receiver_id) && (row.receiver_id === this.selfId && this.effective(row) === 'pending' || row.active && !this.readySeen.has(row.id) && !battlePages.has(location.pathname))).length;
        const count = [...this.unread.values()].reduce((sum, value) => sum + value, 0) + this.incoming.length + duelCount;
        const badge = this.$('.launcher .badge'); badge.hidden = !count; badge.textContent = count > 99 ? '99+' : count;
        this.$('.launcher').title = count ? `${count} unread messages, requests or challenges` : 'Friends';
        for (const [tab, total] of [['friends', 0], ['requests', this.incoming.length], ['duels', duelCount]]) { const badge = this.$(`.tabs [data-tab="${tab}"] b`); badge.hidden = !total; badge.textContent = total > 99 ? '99+' : total; }
    }
    notify(text, open) {
        if (this.open || battlePages.has(location.pathname) || document.hidden || document.querySelector('dialog[open]')) return;
        const toast = this.$('.toast'); toast.textContent = text; toast.hidden = false; toast.onclick = () => { this.show(true); open(); toast.hidden = true; };
        clearTimeout(this.toastTimer); this.toastTimer = setTimeout(() => toast.hidden = true, 7000);
    }
    tick() {
        clearTimeout(this.tickTimer);
        if (!this.open || document.hidden || this.suspended) return;
        for (const clock of this.root.querySelectorAll('[data-expiry]')) clock.textContent = `${clock.dataset.prefix} · ${Math.max(0, Math.ceil((time(clock.dataset.expiry) - Date.now()) / 1000))}s`;
        this.markRead();
        this.tickTimer = setTimeout(() => this.tick(), 1000);
    }
    closeSocket() {
        clearInterval(this.pingTimer); clearTimeout(this.retryTimer); const socket = this.socket; this.socket = null; socket?.close();
    }
    connect() {
        if (this.socket || !this.authorized || this.suspended || document.hidden || navigator.onLine === false) return;
        clearTimeout(this.retryTimer); let socket;
        try { socket = new WebSocket(`${location.protocol === 'https:' ? 'wss:' : 'ws:'}//${location.host}/social/ws`); }
        catch (_) { this.connection('offline'); this.poll(); return; }
        this.socket = socket;
        socket.onmessage = event => {
            if (this.socket !== socket) return;
            let message; try { message = JSON.parse(event.data); } catch (_) { return; }
            if (message.type === 'connected') {
                this.attempt = 0; this.lastPong = Date.now(); this.connection('live'); clearTimeout(this.pollTimer);
                clearInterval(this.pingTimer); this.pingTimer = setInterval(() => { if (Date.now() - this.lastPong > 45000) socket.close(); else if (socket.readyState === WebSocket.OPEN) socket.send(JSON.stringify({type: 'ping'})); }, 20000);
                if (this.connectedOnce) { this.refresh(); this.syncChat(); } this.connectedOnce = true;
            } else if (message.type === 'pong') this.lastPong = Date.now();
            else this.event(message);
        };
        socket.onclose = () => {
            if (this.socket !== socket) return;
            this.socket = null; clearInterval(this.pingTimer); this.connection('offline');
            if (!this.authorized || this.suspended) return;
            this.retryTimer = setTimeout(() => this.connect(), Math.min(30000, 1000 * 2 ** Math.min(this.attempt++, 5)) + Math.random() * 400); this.poll();
        };
        socket.onerror = () => socket.close();
    }
    poll() {
        clearTimeout(this.pollTimer);
        if (!this.authorized || this.suspended) return;
        this.pollTimer = setTimeout(() => { if (!document.hidden && navigator.onLine !== false) { this.refresh(); this.syncChat(); } this.poll(); }, 30000);
    }
    event(message) {
        if (message.type === 'friend.changed') this.scheduleRefresh();
        else if (message.type === 'chat.message') {
            const data = message.data, peerId = this.peerFor(data.sender_id, data.receiver_id);
            if (!peerId) { this.scheduleRefresh(); return; }
            const duplicate = this.seenMessages.has(data.id); this.seenMessages.add(data.id); if (this.seenMessages.size > 1000) this.seenMessages.delete(this.seenMessages.values().next().value);
            if (this.chats.has(peerId)) {
                const chat = this.chats.get(peerId), bottom = this.atBottom(); chat.messages.set(data.client_id, data);
                if (this.peer?.user_id === peerId) { this.renderMessages(bottom); if (!bottom) this.$('.latest').hidden = false; }
            }
            if (!duplicate && data.sender_id === peerId && (!this.open || this.peer?.user_id !== peerId)) this.notify(`New message from ${this.people.get(peerId)?.username || `Player #${peerId}`}`, () => this.openChat(this.people.get(peerId) || {user_id: peerId, username: `Player #${peerId}`}));
            this.refreshUnread();
        } else if (message.type === 'chat.read') {
            const data = message.data, peerId = this.peerFor(data.reader_id, data.peer_id), chat = this.chats.get(peerId);
            if (chat && data.reader_id === peerId) { for (const item of chat.messages.values()) if (item.id <= data.last_message_id && item.sender_id !== peerId) item.read_at = new Date().toISOString(); if (this.peer?.user_id === peerId) this.renderMessages(this.atBottom()); }
            this.refreshUnread();
        } else if (message.type === 'battle.invitation.changed' || message.type === 'battle.ready') {
            const data = message.data; this.upsertInvitation(data); this.renderInvitations(); this.updateBadge();
            if (this.open && this.tab === 'duels' && !this.duel && data.active) { this.readySeen.add(data.id); this.updateBadge(); }
            const peerId = this.peerFor(data.sender_id, data.receiver_id), name = this.people.get(peerId)?.username || 'A friend';
            if (message.type === 'battle.ready') this.notify(`${name}: your battle is ready`, () => this.selectTab('duels'));
            else if (data.receiver_id === this.selfId && this.effective(data) === 'pending') this.notify(`${name} sent a duel invitation`, () => this.selectTab('duels'));
        }
    }
}

if (window.top === window.self && pages.has(location.pathname) && !document.getElementById('magic-friends')) new FriendsPanel();
