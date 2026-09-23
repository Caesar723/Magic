class InteractiveMap {
    constructor() {
        this.request_processor = new Request_Processor();
        this.ui = Object.fromEntries([...document.querySelectorAll('[id]')].map(element => [element.id, element]));
        this.mapContainer = this.ui.mapContainer; this.mapContent = this.ui.mapContent; this.mapSvg = this.ui.mapSvg;
        this.infoPanel = this.ui.infoPanel;
        this.nodes = []; this.paths = []; this.mapArray = []; this.inventory = []; this.cards = []; this.shopItems = [];
        this.currency = 0; this.currentNode = null; this.selectedNode = null;
        this.busy = false; this.stale = false; this.hasRun = false;
        this.zoom = 1;
        this.viewportWidth = this.mapContainer.clientWidth;
        this.motion = matchMedia('(prefers-reduced-motion: reduce)');
        this.bindEvents(); this.initMotion();
        this.ready = this.refreshJourney();
    }
    element(tag, className, text) {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (text != null) element.textContent = String(text);
        return element;
    }
    icon(name, className = '') {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('class', className); svg.setAttribute('aria-hidden', 'true');
        svg.setAttribute('viewBox', name === 'compass' ? '0 0 48 48' : '0 0 200 190');
        const use = document.createElementNS(svg.namespaceURI, 'use'); use.setAttribute('href', '#' + name); svg.append(use);
        return svg;
    }
    image(path, className = '') {
        const image = this.element('img', className); image.alt = ''; image.loading = 'lazy';
        image.src = '/' + String(path || '').replace(/^\/+/, '');
        image.addEventListener('error', () => { image.hidden = true; }, {once: true}); return image;
    }
    label(node) { return node.boss ? 'Boss' : {Start: 'Camp', battle: 'Battle', shop: 'Shop', event: 'Event'}[node.name] || 'Encounter'; }
    landmark(node) { return 'landmark-' + (node.boss ? 'boss' : node.name === 'Start' ? 'start' : node.name); }
    landmarkImage(node, className = '') { return this.image('webpages/rogue/art/' + this.landmark(node).replace('landmark-', 'island-') + '.webp', className); }
    check(response, state = 'success') {
        if (!response || response.state !== state) throw new Error('The action could not be confirmed.');
        return response;
    }
    status(message = '') {
        document.querySelectorAll('.request-status').forEach(element => { element.textContent = message; });
        document.querySelectorAll('.retry-request').forEach(button => { button.hidden = !this.stale; button.disabled = this.busy; });
    }
    setBusy() {
        const blocked = this.busy || this.stale || !this.hasRun;
        this.ui.routeEnter.disabled = blocked || this.selectedNode?.status !== 'current';
        this.ui.battleEnter.disabled = blocked || this.currentNode?.status !== 'current';
        this.ui.shopClose.disabled = blocked;
        this.ui.giveUpButton.disabled = this.ui.confirmYes.disabled = blocked;
        for (const id of ['cardButton', 'inventoryToggle', 'centerMap']) this.ui[id].disabled = !this.hasRun || this.busy;
        this.ui.zoomIn.disabled = !this.hasRun || this.zoom >= 1.4;
        this.ui.zoomOut.disabled = !this.hasRun || this.zoom <= .6;
        document.querySelectorAll('.buy-button').forEach(button => { button.disabled = blocked || button.dataset.available !== 'true'; });
        document.querySelectorAll('.event-option').forEach(button => { button.disabled = blocked || button.dataset.valid !== 'true'; });
        document.querySelectorAll('.retry-request').forEach(button => { button.disabled = this.busy; });
        document.querySelectorAll('.close-button, #confirmNo').forEach(button => { button.disabled = this.busy; });
        this.ui.routePanel.setAttribute('aria-busy', String(this.busy));
        this.ui.routeChoices.querySelectorAll('button').forEach(button => { button.disabled = this.busy; });
    }
    async perform(action) {
        if (this.busy || this.stale || !this.hasRun) return;
        this.busy = true; this.status(); this.setBusy();
        try { await action(); }
        catch (_) {
            // Refresh authoritative state before another mutation; never replay a purchase or event automatically.
            this.stale = true;
            this.status('The action could not be confirmed. Refresh your journey to check the result before continuing.');
        } finally { if (!this.navigating) this.busy = false; this.setBusy(); }
    }
    async refreshJourney() {
        if (this.busy) return;
        this.busy = true; this.setBusy(); this.ui.mapContainer.setAttribute('aria-busy', 'true');
        try {
            await this.update_map_info(true);
            this.stale = false; this.status();
        } catch (_) {
            this.stale = true; this.status('Unable to load your journey. Your progress has not been reset.');
        } finally { this.busy = false; this.ui.mapContainer.setAttribute('aria-busy', 'false'); this.setBusy(); }
    }
    async update_map_info(reconcile = false) {
        const map = await this.request_processor.get_map_info();
        if (this.disposed) return;
        if (map?.state === 'not in room') { this.endRun(); return; }
        if (!Array.isArray(map) || !map.length || map.some(layer => !(Array.isArray(layer) ? layer : [layer]).every(node => node && typeof node.id === 'string' && ['current', 'completed', 'locked'].includes(node.status) && ['Start', 'battle', 'event', 'shop'].includes(node.name)))) throw new Error('Invalid map.');
        const [treasures, profile, deck] = await Promise.all([
            this.request_processor.get_treasure_info(), this.request_processor.get_profile_info(), this.request_processor.get_cards_info()
        ]);
        if (this.disposed) return;
        if (!Array.isArray(treasures) || !Number.isFinite(profile?.currency) || !Number.isFinite(profile?.max_life) || !Number.isInteger(profile?.level) || deck?.state !== 'success' || !Array.isArray(deck.cards_info)) throw new Error('Invalid journey.');
        const oldProfile = this.profile, oldTreasures = this.inventory.length, oldCount = this.cardCount();
        const previousCurrent = this.nodes.filter(node => node.status === 'current').map(node => node.id).join();
        this.hasRun = true; this.ui.noRun.hidden = true;
        this.profile = profile; this.currency = profile.currency;
        this.inventory = treasures; this.cards = deck.cards_info;
        this.renderControlsInfo(profile); this.renderInventory();
        if (this.ui.cardModal.open) this.renderCards();
        if (!arraysEqual(map, this.mapArray)) this.generateMapFromArray(map);
        const nextCurrent = this.nodes.filter(node => node.status === 'current').map(node => node.id).join();
        if (previousCurrent !== nextCurrent) this.centerCurrent(Boolean(previousCurrent));
        if (oldProfile) {
            this.reward(this.ui.runCoins, profile.currency - oldProfile.currency);
            this.reward(this.ui.runLife, profile.max_life - oldProfile.max_life);
            if (oldTreasures !== treasures.length) this.reward(this.ui.inventoryToggle, treasures.length - oldTreasures);
            if (oldCount !== this.cardCount()) this.reward(this.ui.cardButton, this.cardCount() - oldCount);
        }
        if (reconcile && this.currentNode) {
            const current = this.nodes.find(node => node.id === this.currentNode.id);
            if (current?.status !== 'current') {
                for (const id of ['shopModal', 'eventModal', 'battleModal']) this.ui[id].close();
                this.currentNode = null;
            } else if (this.ui.shopModal.open) {
                const response = this.check(await this.request_processor.open_shop(current.id));
                this.currentNode = current; this.shopItems = response.shop_info.shop_items; this.renderShop();
            } else if (this.ui.eventModal.open) {
                const response = this.check(await this.request_processor.open_event(current.id));
                this.currentNode = current; this.renderEvent(response.event_info);
            } else if (this.ui.battleModal.open) this.openBattle(current);
        }
        this.setBusy();
    }
    endRun() {
        this.hasRun = false; this.nodes = []; this.paths = []; this.mapArray = [];
        this.currentNode = null; this.selectedNode = null; this.clearMap(); this.ui.routeOverview.replaceChildren();
        this.ui.routeChoices.replaceChildren(); this.ui.routeChoices.hidden = true;
        document.querySelectorAll('dialog[open]').forEach(dialog => dialog.close());
        this.ui.noRun.hidden = false; this.ui.journeyTitle.textContent = 'Journey ended'; this.ui.journeyProgress.textContent = '';
        this.ui.routeEnter.disabled = true; this.setBusy();
    }
    renderControlsInfo(profile) {
        this.ui.runCoins.textContent = this.ui.currencyAmount.textContent = profile.currency;
        this.ui.runLife.textContent = profile.max_life;
        this.ui.actLabel.textContent = 'Act ' + (['I', 'II', 'III'][profile.level] || profile.level + 1);
        const act = Math.max(0, Math.min(2, profile.level));
        if (this.act !== act) {
            this.act = act; document.body.dataset.act = String(act + 1);
            this.ui.actLabel.classList.remove('act-arrival');
            void this.ui.actLabel.offsetWidth; this.ui.actLabel.classList.add('act-arrival');
        }
        this.ui.treasureCount.textContent = this.inventory.length;
        this.ui.cardCount.textContent = this.cardCount();
        this.ui.deckSummary.textContent = this.cardCount() + ' cards · ' + this.cards.length + ' unique';
    }
    cardCount() { return this.cards.reduce((sum, card) => sum + Number(card.quantity || 0), 0); }
    generateMapFromArray(mapArray) {
        const selectedId = this.selectedNode?.id;
        this.mapArray = mapArray; this.nodes = []; this.paths = [];
        this.layers = mapArray.map((layer, index) => (Array.isArray(layer) ? layer : [layer]).map((data, branch) => {
            const node = {...data, layer: index, branch, boss: index === mapArray.length - 1 && data.name === 'battle'};
            this.nodes.push(node); return node;
        }));
        // Mirror the server graph: equal branch counts connect by index; other layers connect to every next node.
        this.layers.slice(0, -1).forEach((layer, index) => {
            const next = this.layers[index + 1];
            layer.forEach((from, branch) => (layer.length === next.length ? [next[branch]] : next).forEach(to => this.paths.push({from, to})));
        });
        this.clearMap();
        this.nodes.forEach(node => {
            const button = this.element('button', 'map-node node-' + node.status + (node.boss ? ' is-boss' : ''));
            button.type = 'button'; button.dataset.nodeId = node.id; button.setAttribute('aria-pressed', 'false');
            button.setAttribute('aria-label', this.label(node) + ', ' + node.status + (node.agent_name ? ', ' + node.agent_name : ''));
            button.style.setProperty('--delay', (-node.branch * 1.4 - node.layer * .3) + 's');
            const floating = this.element('span', 'node-float'); floating.append(this.icon(this.landmark(node), 'node-art node-fallback'));
            const art = this.landmarkImage(node, 'node-art node-illustration');
            art.addEventListener('load', () => floating.classList.add('has-illustration'), {once: true});
            floating.append(art, this.element('span', 'node-aura'));
            const route = this.layers[node.layer].length > 1 ? ['I', 'II', 'III'][node.branch] + ' · ' : '';
            button.append(floating, this.element('span', 'node-title', route + this.label(node)));
            button.addEventListener('click', () => { if (!this.suppressClick && !this.busy) this.showNodeInfo(node); });
            for (const event of ['pointerenter', 'focus']) button.addEventListener(event, () => { this.focusPaths(node.id); if (event === 'focus') this.viewedLayer = node.layer; });
            for (const event of ['pointerleave', 'blur']) button.addEventListener(event, () => this.focusPaths(this.selectedNode?.id));
            node.element = button; this.mapContent.append(button);
        });
        this.paths.forEach(path => {
            const element = document.createElementNS(this.mapSvg.namespaceURI, 'path');
            const state = path.from.status === 'completed' ? (path.to.status === 'current' ? 'current' : path.to.status === 'completed' ? 'completed' : 'locked') : 'locked';
            element.setAttribute('class', 'map-path path-' + state); this.mapSvg.append(element); path.element = element;
        });
        this.ui.routeOverview.replaceChildren(...this.layers.map((layer, index) => {
            const state = layer.some(node => node.status === 'current') ? 'current' : layer.some(node => node.status === 'completed') ? 'completed' : 'locked';
            const button = this.element('button', 'stage-' + state); button.dataset.layer = index;
            button.setAttribute('aria-label', 'Stage ' + (index + 1) + ', ' + state); button.title = 'Stage ' + (index + 1);
            button.addEventListener('click', () => this.centerLayer(index)); return button;
        }));
        const current = this.nodes.find(node => node.status === 'current');
        const available = current ? this.layers[current.layer].filter(node => node.status === 'current') : [];
        this.ui.routeChoices.hidden = available.length < 2;
        this.ui.routeChoices.replaceChildren(...available.map(node => {
            const button = this.element('button', 'route-choice'); button.dataset.routeId = node.id;
            button.append(this.element('span', 'route-number', ['I', 'II', 'III'][node.branch]), this.landmarkImage(node), this.element('span', '', this.label(node)));
            button.setAttribute('aria-label', 'Preview route ' + (node.branch + 1) + ': ' + this.label(node));
            button.addEventListener('click', () => {
                this.showNodeInfo(node);
                this.centerNode(node);
            });
            return button;
        }));
        this.layoutMap();
        this.showNodeInfo(this.nodes.find(node => node.id === selectedId && node.status === 'current') || current || this.nodes[0]);
        const choices = available.length;
        this.ui.journeyTitle.textContent = choices > 1 ? 'Choose your path' : 'Continue your journey';
        this.ui.journeyProgress.textContent = current ? 'Stage ' + (current.layer + 1) + ' of ' + this.layers.length + ' · ' + choices + (choices === 1 ? ' route available' : ' routes available') : 'All encounters visited';
    }
    clearMap() { this.mapContent.querySelectorAll('.map-node').forEach(node => node.remove()); this.mapSvg.replaceChildren(); }
    layoutMap() {
        if (!this.nodes.length || this.disposed) return;
        const z = this.zoom, nodeWidth = Math.min(innerWidth <= 620 ? 150 : 174, (this.mapContainer.clientWidth - 44) / 2) * z;
        // Stagger forks to fit the viewport while keeping labels at a readable size.
        const artHeight = Math.max(80, Math.min(155, (this.mapContainer.clientHeight - 52) / 2 - 30)) * z;
        const nodeHeight = artHeight + 30, gap = 20 * z;
        const hasFork = this.layers.some(layer => layer.length > 1);
        const height = Math.max(this.mapContainer.clientHeight, (hasFork ? nodeHeight * 2 + gap : nodeHeight) + 32);
        let offset = 45 * z;
        this.layers.forEach(layer => {
            const span = layer.length === 3 ? nodeWidth * 2 + gap : nodeWidth;
            const center = offset + span / 2;
            layer.forEach(node => {
                node.stageX = center; node.x = center;
                node.y = height / 2;
                if (layer.length === 2) node.y += (node.branch === 0 ? -1 : 1) * (nodeHeight + gap) / 2;
                if (layer.length === 3) {
                    node.y += (node.branch - 1) * (nodeHeight + gap) / 2;
                    node.x += (node.branch === 1 ? -1 : 1) * (nodeWidth + gap) / 2;
                }
            });
            offset += span + 145 * z;
        });
        const width = Math.max(this.mapContainer.clientWidth, offset - 100 * z);
        this.mapContent.style.width = width + 'px'; this.mapContent.style.height = height + 'px';
        this.mapContent.style.setProperty('--node-width', nodeWidth + 'px');
        this.mapContent.style.setProperty('--node-height', nodeHeight + 'px');
        this.mapContent.style.setProperty('--art-height', artHeight + 'px');
        this.mapSvg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
        this.nodes.forEach(node => {
            Object.assign(node.element.style, {left: node.x + 'px', top: node.y + 'px'});
        });
        this.paths.forEach(({from, to, element}) => {
            const dx = (to.x - from.x) * .48;
            const bendY = this.layers[to.layer].length === 3 && to.branch !== 1 ? to.y : from.y;
            element.setAttribute('d', `M ${from.x} ${from.y} C ${from.x + dx} ${bendY}, ${to.x - dx} ${to.y}, ${to.x} ${to.y}`);
        });
        this.ui.zoomLevel.textContent = Math.round(this.zoom * 100) + '%'; this.updateViewport(); this.setBusy();
    }
    changeZoom(delta) {
        if (!this.hasRun) return;
        const ratio = (this.mapContainer.scrollLeft + this.mapContainer.clientWidth / 2) / this.zoom;
        this.zoom = Math.max(.6, Math.min(1.4, Math.round((this.zoom + delta) * 10) / 10));
        this.layoutMap(); this.mapContainer.scrollLeft = ratio * this.zoom - this.mapContainer.clientWidth / 2;
        this.mapContainer.scrollTop = (this.mapContent.clientHeight - this.mapContainer.clientHeight) / 2;
    }
    centerLayer(index, smooth = true) {
        const node = this.layers?.[index]?.[0]; if (!node) return;
        this.viewedLayer = index;
        this.mapContainer.scrollTo({left: node.stageX - this.mapContainer.clientWidth / 2, top: (this.mapContent.clientHeight - this.mapContainer.clientHeight) / 2, behavior: smooth && !this.reduced ? 'smooth' : 'instant'});
    }
    centerCurrent(smooth = true) { const node = this.nodes.find(node => node.status === 'current'); if (node) this.centerLayer(node.layer, smooth); }
    centerNode(node, smooth = true) {
        this.viewedLayer = node.layer;
        if (this.zoom <= 1) { this.centerLayer(node.layer, smooth); return; }
        this.mapContainer.scrollTo({left: node.x - this.mapContainer.clientWidth / 2, top: node.y - this.mapContainer.clientHeight / 2, behavior: smooth && !this.reduced ? 'smooth' : 'instant'});
    }
    updateViewport() {
        const left = this.mapContainer.scrollLeft, width = this.mapContainer.clientWidth;
        const progress = Math.max(0, Math.min(1, left / Math.max(1, this.mapContent.clientWidth - width)));
        const blend = value => { const t = Math.max(0, Math.min(1, value)); return t * t * (3 - 2 * t); };
        this.ui.worldBackdrop.style.setProperty('--highlands', blend((progress - .08) / .47));
        this.ui.worldBackdrop.style.setProperty('--riftlands', blend((progress - .55) / .45));
        this.ui.worldBackdrop.style.setProperty('--drift', this.reduced ? '0px' : (-left / Math.max(1, this.mapContent.clientWidth) * 28) + 'px');
        this.ui.routeOverview.querySelectorAll('button').forEach(button => {
            const node = this.layers?.[Number(button.dataset.layer)]?.[0];
            button.classList.toggle('in-view', Boolean(node && node.stageX >= left && node.stageX <= left + width));
        });
    }
    focusPaths(id) { this.paths.forEach(path => path.element.classList.toggle('path-focus', path.from.id === id || path.to.id === id)); }
    showNodeInfo(node) {
        if (!node) return;
        this.selectedNode = node;
        this.nodes.forEach(entry => { entry.element.classList.toggle('is-selected', entry.id === node.id); entry.element.setAttribute('aria-pressed', String(entry.id === node.id)); });
        this.ui.routeChoices.querySelectorAll('button').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.routeId === node.id)));
        this.focusPaths(node.id);
        this.ui.routeMark.replaceChildren(this.landmarkImage(node));
        this.ui.routeState.textContent = {current: 'Available', completed: 'Visited', locked: 'Unexplored'}[node.status] + ' · Stage ' + (node.layer + 1);
        this.ui.routeTitle.textContent = node.agent_name || this.label(node);
        this.ui.routeDescription.textContent = node.status === 'locked' ? 'Complete your current encounter to continue along the map.'
            : node.status === 'completed' ? 'This stop has already been visited.'
            : node.name === 'battle' ? 'Inspect your opponent before entering battle.'
            : 'Entering this ' + node.name + ' chooses the route and closes the other paths at this stage.';
        this.ui.routeEnter.textContent = node.status === 'completed' ? 'Visited' : node.status === 'locked' ? 'Not yet available' : {battle: 'View Battle →', shop: 'Enter Shop →', event: 'Explore Event →'}[node.name];
        this.setBusy();
    }
    enterSelected() {
        const node = this.selectedNode;
        if (this.busy || this.stale || node?.status !== 'current') return;
        if (node.name === 'battle') this.openBattle(node);
        else if (node.name === 'shop') this.openShop(node);
        else if (node.name === 'event') this.openEvent(node);
    }
    showDialog(id) { if (!this.ui[id].open) this.ui[id].showModal(); }
    closeDialog(id) { if (!this.busy) this.ui[id].close(); }
    openShop(shop) {
        return this.perform(async () => {
            this.currentNode = shop;
            this.check(await this.request_processor.select_routine(shop.id));
            const response = this.check(await this.request_processor.open_shop(shop.id));
            if (!Array.isArray(response.shop_info?.shop_items)) throw new Error('Invalid shop.');
            this.shopItems = response.shop_info.shop_items;
            await this.update_map_info(); this.renderShop(); this.showDialog('shopModal');
        });
    }
    closeShop() {
        return this.perform(async () => {
            this.check(await this.request_processor.close_shop(this.currentNode.id));
            this.ui.shopModal.close(); this.currentNode = null;
            await this.update_map_info(); this.showSmallMessage('Journey continues', 'Choose your next stop.');
        });
    }
    renderShop() {
        const scene = '/webpages/rogue/art/merchant' + (this.act ? '-' + (this.act + 1) : '') + '.webp';
        if (this.ui.shopArt.getAttribute('src') !== scene) this.ui.shopArt.src = scene;
        this.ui.currencyAmount.textContent = this.currency;
        this.ui.shopGrid.replaceChildren(...this.shopItems.map(item => {
            const element = this.element('article', 'shop-item' + (item.is_selled ? ' sold' : ''));
            element.dataset.itemId = item.id;
            const art = this.element('div', 'shop-item-image'); art.append(this.image(item.image_path));
            const footer = this.element('div', 'shop-item-footer'), price = this.element('span', 'shop-item-price');
            const coin = this.element('span', 'coin-mark', '✧'); coin.setAttribute('aria-hidden', 'true'); price.append(coin, this.element('span', '', item.price));
            const buy = this.element('button', 'paper-button buy-button', item.is_selled ? 'Acquired' : this.currency < item.price ? 'Need coins' : 'Buy');
            buy.dataset.itemId = item.id; buy.dataset.available = String(!item.is_selled && this.currency >= item.price);
            buy.setAttribute('aria-label', 'Buy ' + item.name + ' for ' + item.price + ' coins');
            buy.addEventListener('click', () => this.purchaseItem(item)); footer.append(price, buy);
            element.append(art, this.element('h3', 'shop-item-name', item.name), this.element('p', 'shop-item-description', item.description), footer);
            return element;
        }));
        this.setBusy();
    }
    purchaseItem(item) {
        if (item.is_selled || this.currency < item.price || this.currentNode?.name !== 'shop') return;
        return this.perform(async () => {
            this.check(await this.request_processor.shop_buy(this.currentNode.id, item.id));
            item.is_selled = true; this.renderShop();
            await this.update_map_info(); this.renderShop();
            const element = [...this.ui.shopGrid.children].find(element => element.dataset.itemId === item.id);
            element?.classList.add('purchase-success');
            this.showSmallMessage('Acquired', item.name);
        });
    }
    openBattle(enemy) {
        this.currentNode = enemy;
        this.ui.enemyAvatar.replaceChildren(this.landmarkImage(enemy));
        this.ui.enemyName.textContent = enemy.agent_name || 'Unknown opponent';
        this.ui.enemyDescription.textContent = enemy.description || '';
        this.ui.battleKind.textContent = enemy.boss ? 'Boss encounter' : 'Battle';
        const life = enemy.status === 'current' ? enemy.agent_max_life : 0;
        this.ui.enemyHpFill.style.width = life > 0 ? '100%' : '0%';
        this.ui.enemyHpText.textContent = life + ' / ' + enemy.agent_max_life;
        this.ui.battleReward.textContent = 'Victory reward: ' + enemy.agent_win_price + ' coins';
        this.showDialog('battleModal'); this.setBusy();
    }
    enterBattle() {
        if (this.currentNode?.status !== 'current') return;
        return this.perform(async () => {
            const id = this.currentNode.id;
            this.check(await this.request_processor.select_routine(id));
            this.check(await this.request_processor.battle(id), 'find!');
            this.navigating = true;
            this.ui.battleModal.close(); this.ui.departure.classList.add('active');
            if (!this.reduced && !document.hidden && document.hasFocus()) await new Promise(resolve => setTimeout(resolve, 650));
            window.location.assign('/gaming_rogue');
        });
    }
    openEvent(event) {
        return this.perform(async () => {
            this.currentNode = event;
            this.check(await this.request_processor.select_routine(event.id));
            const response = this.check(await this.request_processor.open_event(event.id));
            await this.update_map_info(); this.renderEvent(response.event_info); this.showDialog('eventModal');
        });
    }
    renderEvent(event) {
        if (!Array.isArray(event?.options)) throw new Error('Invalid event.');
        this.event = event;
        const themes = [
            ['grove', /grove|root|bloom|colossus/i], ['rift', /rift|mirror|stellar/i],
            ['embers', /flame|burning|obsidian/i], ['reliquary', /tome|pact|inscription|stele|statue|throne|runic/i]
        ];
        const theme = themes.find(([, pattern]) => pattern.test(event.title))?.[0] || 'temple';
        this.ui.eventImage.dataset.theme = theme;
        this.ui.eventArt.src = '/webpages/rogue/art/' + theme + '.webp';
        this.ui.eventTitle.textContent = event.title; this.ui.eventDescription.textContent = event.description;
        this.ui.eventOptions.replaceChildren(...event.options.map((option, index) => {
            const button = this.element('button', 'event-option'); button.dataset.valid = String(Boolean(option.is_valid));
            button.append(this.element('strong', '', option.title), this.element('span', '', option.description));
            if (!option.is_valid) button.append(this.element('span', '', 'Unavailable'));
            button.addEventListener('click', () => this.selectEventOption(index)); return button;
        }));
        this.setBusy();
    }
    selectEventOption(index) {
        const option = this.event?.options[index];
        if (!option?.is_valid || this.currentNode?.name !== 'event') return;
        return this.perform(async () => {
            this.check(await this.request_processor.select_event_option(this.currentNode.id, index));
            this.ui.eventModal.close(); this.currentNode = null;
            await this.update_map_info(); this.showSmallMessage('Choice made', option.title);
        });
    }
    renderInventory() {
        this.ui.inventoryGrid.replaceChildren(...this.inventory.map(item => {
            const button = this.element('button', 'inventory-item'), copy = this.element('span');
            copy.append(this.element('strong', '', item.name), this.element('p', '', item.description));
            button.append(this.image(item.image_path), copy); button.addEventListener('click', () => this.showItemInfo(item)); return button;
        }));
        if (!this.inventory.length) this.ui.inventoryGrid.append(this.element('p', '', 'No treasures yet. Discover them through shops and encounters.'));
    }
    renderCards() {
        const query = this.ui.cardSearch.value.trim().toLowerCase();
        const cards = this.cards.filter(card => (card.name + ' ' + card.type + ' ' + card.description).toLowerCase().includes(query));
        this.ui.cardGrid.replaceChildren(...cards.map(card => {
            const button = this.element('button', 'magic-card');
            const copy = this.element('span', 'card-copy'); copy.append(this.element('strong', '', card.name), this.element('small', '', card.type));
            const mana = this.element('span', 'card-mana-cost'); mana.setAttribute('aria-label', 'Mana cost ' + (card.manaCost || '0'));
            for (const symbol of String(card.manaCost || '').match(/\d+|[WUBRG]/g) || []) {
                const token = this.element('span', 'mana-symbol');
                const color = {W: 'gold', U: 'blue', B: 'black', R: 'red', G: 'green'}[symbol];
                if (color) token.append(this.image('webpages/image_source/color_fee/' + color + '.PNG')); else token.textContent = symbol;
                mana.append(token);
            }
            copy.append(mana);
            button.append(this.image(card.image_path), copy, this.element('span', 'card-quantity', '× ' + card.quantity));
            button.addEventListener('click', () => this.showCardDetails(card)); return button;
        }));
        this.ui.cardEmpty.hidden = cards.length > 0;
    }
    showItemInfo(item) { this.showDetails(item.name, 'Treasure', item.image_path, item.description, ''); }
    showCardDetails(card) {
        const stats = (card.manaCost ? 'Mana cost: ' + card.manaCost + '\n' : '') + 'Copies: ' + card.quantity + ((card.attack || card.defense) ? '\nPower / Toughness: ' + card.attack + ' / ' + card.defense : '');
        this.showDetails(card.name, card.type, card.image_path, card.description, stats);
    }
    showDetails(name, type, path, description, stats) {
        this.ui.detailTitle.textContent = name; this.ui.detailType.textContent = type; this.ui.detailDescription.textContent = description; this.ui.detailStats.textContent = stats;
        this.ui.detailImage.hidden = false; this.ui.detailImage.src = '/' + String(path).replace(/^\/+/, ''); this.ui.detailImage.alt = name;
        this.ui.detailImage.onerror = () => { this.ui.detailImage.hidden = true; };
        this.showDialog('detailModal');
    }
    showSmallMessage(title, description) {
        clearTimeout(this.messageTimer);
        this.ui.infoTitle.textContent = title; this.ui.infoDescription.textContent = description;
        this.infoPanel.classList.add('show'); this.messageTimer = setTimeout(() => this.infoPanel.classList.remove('show'), 4000);
    }
    reward(target, delta) {
        if (!delta || this.reduced || document.hidden || !document.hasFocus()) return;
        const element = target.closest('.stat') || target;
        element.classList.remove('changed'); void element.offsetWidth; element.classList.add('changed');
        if (target.closest('.stat')) {
            element.querySelector('.reward-delta')?.remove();
            const number = this.element('span', 'reward-delta', (delta > 0 ? '+' : '') + delta);
            number.setAttribute('aria-hidden', 'true'); element.append(number); number.addEventListener('animationend', () => number.remove(), {once: true});
        }
    }
    initMotion() {
        const motes = document.createDocumentFragment();
        for (let i = 0; i < 26; i++) {
            const mote = this.element('span', 'mote');
            mote.style.setProperty('--x', (i * 37 % 100) + '%'); mote.style.setProperty('--y', (i * 19 % 100) + '%');
            mote.style.setProperty('--duration', (10 + i % 9) + 's'); mote.style.setProperty('--delay', (-i * 1.3) + 's'); motes.append(mote);
        }
        this.ui.motes.append(motes);
        document.querySelectorAll('.scene-particles').forEach(scene => {
            for (let i = 0; i < 9; i++) {
                const particle = this.element('span');
                particle.style.setProperty('--x', (12 + i * 23 % 76) + '%');
                particle.style.setProperty('--delay', (-i * .8) + 's'); scene.append(particle);
            }
        });
        for (const id of ['shopModal', 'eventModal']) {
            const dialog = this.ui[id];
            dialog.addEventListener('pointermove', event => {
                if (event.pointerType !== 'mouse' || this.reduced || document.hidden) return;
                const bounds = dialog.getBoundingClientRect();
                dialog.style.setProperty('--scene-x', ((event.clientX - bounds.left) / bounds.width - .5) * 12 + 'px');
                dialog.style.setProperty('--scene-y', ((event.clientY - bounds.top) / bounds.height - .5) * 8 + 'px');
            });
            dialog.addEventListener('pointerleave', () => {
                dialog.style.setProperty('--scene-x', '0px'); dialog.style.setProperty('--scene-y', '0px');
            });
        }
        this.applyMotion = () => {
            let reduced = false;
            try { const local = localStorage.getItem('rogue-reduced-motion'); reduced = local === null ? localStorage.getItem('lobby-reduced-motion') === 'true' : local === 'true'; } catch (_) {}
            this.reduced = this.motion.matches || reduced;
            document.body.classList.toggle('motion-reduced', this.reduced);
            this.ui.motionToggle.setAttribute('aria-pressed', String(this.reduced));
            this.ui.motionToggle.textContent = this.reduced ? 'Motion: Off' : 'Motion: On';
            this.ui.motionToggle.disabled = this.motion.matches;
            this.updateViewport();
        };
        const pause = () => { document.body.classList.toggle('motion-paused', document.hidden || !document.hasFocus()); };
        this.motion.addEventListener('change', this.applyMotion);
        window.addEventListener('storage', this.applyMotion);
        window.addEventListener('blur', () => document.body.classList.add('motion-paused'));
        window.addEventListener('focus', pause); document.addEventListener('visibilitychange', pause);
        this.ui.motionToggle.addEventListener('click', () => { try { localStorage.setItem('rogue-reduced-motion', String(!this.reduced)); } catch (_) {} this.applyMotion(); });
        this.applyMotion(); pause();
    }
    bindEvents() {
        this.ui.routeEnter.addEventListener('click', () => this.enterSelected());
        this.ui.centerMap.addEventListener('click', () => { this.zoom = 1; this.layoutMap(); this.centerCurrent(); });
        this.ui.zoomIn.addEventListener('click', () => this.changeZoom(.1)); this.ui.zoomOut.addEventListener('click', () => this.changeZoom(-.1));
        document.querySelectorAll('.retry-request').forEach(button => button.addEventListener('click', () => this.refreshJourney()));
        this.ui.shopClose.addEventListener('click', () => this.closeShop()); this.ui.battleEnter.addEventListener('click', () => this.enterBattle());
        this.ui.cardButton.addEventListener('click', () => { this.renderCards(); this.showDialog('cardModal'); });
        this.ui.inventoryToggle.addEventListener('click', () => this.showDialog('inventoryPanel'));
        this.ui.cardSearch.addEventListener('input', () => this.renderCards());
        this.ui.giveUpButton.addEventListener('click', () => this.showDialog('confirmModal'));
        this.ui.confirmYes.addEventListener('click', () => this.perform(async () => {
            this.check(await this.request_processor.give_up_rogue()); this.navigating = true; window.location.assign('/');
        }));
        for (const [button, dialog] of [['inventoryClose', 'inventoryPanel'], ['shopDismiss', 'shopModal'], ['battleClose', 'battleModal'], ['eventClose', 'eventModal'], ['cardClose', 'cardModal'], ['detailClose', 'detailModal'], ['confirmNo', 'confirmModal']]) this.ui[button].addEventListener('click', () => this.closeDialog(dialog));
        document.querySelectorAll('dialog').forEach(dialog => {
            dialog.addEventListener('cancel', event => { if (this.busy) event.preventDefault(); });
            dialog.addEventListener('click', event => {
                const bounds = dialog.getBoundingClientRect();
                if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) this.closeDialog(dialog.id);
            });
        });
        this.mapContainer.addEventListener('pointerdown', event => {
            this.viewedLayer = null;
            if (event.pointerType !== 'mouse' || event.button !== 0) return;
            this.drag = {x: event.clientX, y: event.clientY, left: this.mapContainer.scrollLeft, top: this.mapContainer.scrollTop, id: event.pointerId};
            this.suppressClick = false;
        });
        this.mapContainer.addEventListener('pointermove', event => {
            if (!this.drag || event.pointerId !== this.drag.id) return;
            const dx = event.clientX - this.drag.x, dy = event.clientY - this.drag.y;
            if (Math.abs(dx) + Math.abs(dy) > 6) {
                this.viewedLayer = null;
                this.suppressClick = true; this.mapContainer.classList.add('dragging'); this.mapContainer.setPointerCapture(event.pointerId);
                this.mapContainer.scrollLeft = this.drag.left - dx; this.mapContainer.scrollTop = this.drag.top - dy;
            }
        });
        const endDrag = () => { this.drag = null; this.mapContainer.classList.remove('dragging'); clearTimeout(this.dragTimer); this.dragTimer = setTimeout(() => { this.suppressClick = false; }, 0); };
        for (const event of ['pointerup', 'pointercancel', 'lostpointercapture']) this.mapContainer.addEventListener(event, endDrag);
        this.mapContainer.addEventListener('dragstart', event => event.preventDefault());
        this.mapContainer.addEventListener('wheel', event => {
            if (!event.ctrlKey && !event.metaKey) this.viewedLayer = null;
            if (event.ctrlKey || event.metaKey || Math.abs(event.deltaX) > Math.abs(event.deltaY)) return;
            const target = this.mapContainer.scrollLeft + event.deltaY;
            if (target >= 0 && target <= this.mapContent.clientWidth - this.mapContainer.clientWidth) { event.preventDefault(); this.mapContainer.scrollLeft = target; }
        }, {passive: false});
        this.mapContainer.addEventListener('keydown', event => {
            if (event.key.startsWith('Arrow')) this.viewedLayer = null;
            if (event.target !== this.mapContainer) return;
            if (event.key === 'Home') { event.preventDefault(); this.ui.centerMap.click(); }
            else if (event.key === '+' || event.key === '=') { event.preventDefault(); this.changeZoom(.1); }
            else if (event.key === '-') { event.preventDefault(); this.changeZoom(-.1); }
        });
        this.mapContainer.addEventListener('scroll', () => {
            if (this.scrollFrame) return;
            this.scrollFrame = requestAnimationFrame(() => { this.scrollFrame = 0; this.updateViewport(); });
        }, {passive: true});
        this.resize = new ResizeObserver(() => {
            cancelAnimationFrame(this.resizeFrame);
            this.resizeFrame = requestAnimationFrame(() => {
                const center = this.mapContainer.scrollLeft + this.viewportWidth / 2;
                const nearest = this.layers?.[this.viewedLayer]?.[0] || this.layers?.reduce((best, layer) => !best || Math.abs(layer[0].stageX - center) < Math.abs(best.stageX - center) ? layer[0] : best, null);
                this.viewportWidth = this.mapContainer.clientWidth;
                this.layoutMap();
                if (nearest) this.centerNode(this.selectedNode?.layer === nearest.layer ? this.selectedNode : nearest, false);
            });
        });
        this.resize.observe(this.mapContainer);
        window.addEventListener('pagehide', event => {
            document.body.classList.add('motion-paused');
            if (!event.persisted) { this.disposed = true; this.resize.disconnect(); clearTimeout(this.messageTimer); clearTimeout(this.dragTimer); cancelAnimationFrame(this.scrollFrame); cancelAnimationFrame(this.resizeFrame); }
        });
        window.addEventListener('pageshow', event => {
            document.body.classList.toggle('motion-paused', document.hidden || !document.hasFocus());
            if (event.persisted) {
                if (this.navigating) { this.navigating = false; this.busy = false; }
                this.ui.departure.classList.remove('active');
                this.refreshJourney();
            }
        });
    }
    // Existing page helpers remain available to callers; persistence still belongs to the server.
    addItem(item) { this.inventory.push(item); this.renderInventory(); }
    removeItem(name) { this.inventory = this.inventory.filter(item => item.name !== name); this.renderInventory(); }
    addCurrency(amount) { this.currency += amount; this.ui.runCoins.textContent = this.ui.currencyAmount.textContent = this.currency; }
}
function arraysEqual(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function generateMapFromArray(mapArray) { window.interactiveMap?.generateMapFromArray(mapArray); }
function addInventoryItem(name, icon, description) { window.interactiveMap?.addItem({name, icon, description}); }
function removeInventoryItem(name) { window.interactiveMap?.removeItem(name); }
function addCurrency(amount) { window.interactiveMap?.addCurrency(amount); }
function getCurrency() { return window.interactiveMap?.currency || 0; }
document.addEventListener('DOMContentLoaded', () => { window.interactiveMap = new InteractiveMap(); });
