class InteractiveMap {
    constructor() {
        this.request_processor = new Request_Processor();

        this.mapContainer = document.getElementById('mapContainer');
        this.mapContent = document.getElementById('mapContent');
        this.mapSvg = document.getElementById('mapSvg');
        this.infoPanel = document.getElementById('infoPanel');
        
        this.isDragging = false;
        this.startX = 0;
        this.currentX = 0;
        this.translateX = 0;

        this.currency = 0;
        
        this.nodes = [];
        this.paths = [];
        this.currentNode = null;
        this.init();
        this.initShop(); // 初始化商店系统
        this.initBattle(); // 初始化战斗系统
        this.initEvent(); // 初始化事件系统
        this.initInventory();
        this.initCardSystem(); // 初始化卡牌系统
    }
    setTheme(theme) {
        if (theme === 'default') {
            document.documentElement.removeAttribute('data-theme');
        } else {
            document.documentElement.setAttribute('data-theme', theme);
        }
        
        // 重新创建路径以应用新的颜色
        this.createPaths();
    }
    
    generateMapFromArray(mapArray) {
        this.nodes = [];
        this.paths = [];
        
        const baseX = 200; // 起始X位置
        const stepX = 400; // 每层之间的X间距
        const centerY = 400; // 中心Y位置
        const branchSpacing = 150; // 分支之间的Y间距
        
        let nodeId = 1;
        let currentX = baseX;
        
        // 存储每层的节点信息，用于连接路径
        const layerNodes = [];
        
        mapArray.forEach((layer, layerIndex) => {
            const currentLayerNodes = [];
            
            if (Array.isArray(layer)) {
                // 多个节点的分支层
                const nodeCount = layer.length;
                const startY = centerY - ((nodeCount - 1) * branchSpacing) / 2;
                
                layer.forEach((nodeData, nodeIndex) => {
                    const node = {
                        id: nodeId++,
                        x: currentX,
                        y: startY + (nodeIndex * branchSpacing),
                        type: nodeData.status,
                        title: nodeData.name,
                        description: nodeData.description || `${nodeData.name}的详细信息`,
                        node_extra:nodeData
                    };
                    
                    this.nodes.push(node);
                    currentLayerNodes.push(node);
                });
            } else {
                // 单个节点层
                const node = {
                    id: nodeId++,
                    x: currentX,
                    y: centerY,
                    type: layer.status,
                    title: layer.name,
                    description: layer.description || `${layer.name}的详细信息`,
                    node_extra:layer
                };
                
                this.nodes.push(node);
                currentLayerNodes.push(node);
            }
            
            layerNodes.push(currentLayerNodes);
            currentX += stepX;
        });
        
        // 生成路径连接
        for (let i = 0; i < layerNodes.length - 1; i++) {
            const currentLayer = layerNodes[i];
            const nextLayer = layerNodes[i + 1];
            
            // 如果当前层只有一个节点，连接到下一层的所有节点
            if (currentLayer.length === 1) {
                nextLayer.forEach(nextNode => {
                    this.paths.push({
                        from: currentLayer[0].id,
                        to: nextNode.id,
                        type: nextNode.type
                    });
                });
            }
            // 如果下一层只有一个节点，当前层的所有节点都连接到它
            else if (nextLayer.length === 1) {
                currentLayer.forEach(currentNode => {
                    this.paths.push({
                        from: currentNode.id,
                        to: nextLayer[0].id,
                        type: (nextLayer[0].type==="completed" && currentNode.type==="completed")||(nextLayer[0].type==="current" && currentNode.type==="completed") ? "completed" : "locked"
                    });
                });
            }
            // 如果两层都有多个节点，按索引对应连接
            else {
                const minLength = Math.min(currentLayer.length, nextLayer.length);
                for (let j = 0; j < minLength; j++) {
                    this.paths.push({
                        from: currentLayer[j].id,
                        to: nextLayer[j].id,
                        type: currentLayer[j].type=="completed"?"completed":"locked"
                    });
                }
            }
        }
        
        // 清除现有的地图内容
        this.clearMap();
        
        // 重新创建地图
        this.createPaths();
        this.createNodes();
        
        console.log('[v0] Generated map with', this.nodes.length, 'nodes and', this.paths.length, 'paths');
    }
    
    clearMap() {
        // 清除所有节点
        const existingNodes = this.mapContent.querySelectorAll('.map-node');
        existingNodes.forEach(node => node.remove());
        
        // 清除所有路径
        while (this.mapSvg.firstChild) {
            this.mapSvg.removeChild(this.mapSvg.firstChild);
        }
    }

    // async init_map_info(){
        
    // }

    async update_map_info(){
        const map_info = await this.request_processor.get_map_info();
        console.log(map_info)
        console.log(this.mapArray)
        console.log(arraysEqual(map_info,this.mapArray))
        if(! arraysEqual(map_info,this.mapArray)){
            this.generateMapFromArray(map_info);
        }
        
        const treasure_info = await this.request_processor.get_treasure_info();
        console.log(treasure_info)
        console.log(this.inventory)
        console.log(arraysEqual(treasure_info,this.inventory))
        if(! arraysEqual(treasure_info,this.inventory)){
            this.inventory=treasure_info;
            this.renderInventory();
        }
        const profile_info = await this.request_processor.get_profile_info();
        const theme={
            0:"default",
            1:"purple",
            2:"gold",
        }
        this.setTheme(theme[profile_info.level]);
        this.renderControlsInfo(profile_info);

        
        const cards_info = (await this.request_processor.get_cards_info()).cards_info;
        console.log(cards_info)
        console.log(this.cards)
        console.log(arraysEqual(cards_info,this.cards))
        if(! arraysEqual(cards_info,this.cards)){
            this.cards=cards_info;
            this.renderCards();
        }

        this.updateCurrencyDisplay();
        
    }
    
    async init() {
        
        this.shopItems = [
            // {
            //     id: 1,
            //     name: '传说之剑',
            //     icon: '⚔️',
            //     description: '传说中的神器，拥有无与伦比的锋利度和魔法力量，攻击力+100',
            //     price: 500
            // },
            // {
            //     id: 2,
            //     name: '生命药水',
            //     icon: '🧪',
            //     description: '珍贵的治疗药水，能够瞬间恢复大量生命值，回复500HP',
            //     price: 150
            // },
            // {
            //     id: 3,
            //     name: '魔法护盾',
            //     icon: '🛡️',
            //     description: '强大的防护装备，能够抵挡大部分魔法攻击，防御力+80',
            //     price: 350
            // },
            // {
            //     id: 4,
            //     name: '速度之靴',
            //     icon: '👢',
            //     description: '轻盈的魔法靴子，大幅提升移动速度和敏捷度，速度+200%',
            //     price: 200
            // },
            // {
            //     id: 5,
            //     name: '智慧法杖',
            //     icon: '🪄',
            //     description: '蕴含古老智慧的法杖，增强魔法威力和法力值，魔力+150',
            //     price: 400
            // },
            // {
            //     id: 6,
            //     name: '隐身斗篷',
            //     icon: '🧥',
            //     description: '神秘的隐身装备，让穿戴者完全隐形，持续60秒',
            //     price: 300
            // }
        ];
       




        const map_info = await this.request_processor.get_map_info();
        const treasure_info = await this.request_processor.get_treasure_info();
        const profile_info = await this.request_processor.get_profile_info();
        this.inventory=treasure_info;
        this.renderInventory();
        this.renderControlsInfo(profile_info);
        this.initGiveUpButton();
        console.log(map_info)
        console.log(treasure_info)
        console.log(profile_info)

        this.mapArray=map_info;
        const mapContent = document.querySelector('.map-content');

        
        let newWidth = this.mapArray.length*500;
        mapContent.style.width = newWidth + "px";

        const theme={
            0:"default",
            1:"purple",
            2:"gold",
        }
        this.setTheme(theme[profile_info.level]);
        
        this.generateMapFromArray(map_info);
        
        this.bindEvents();
    }

    renderControlsInfo(profile_info) {
        this.currency = profile_info.currency;
        console.log(profile_info)
        const controlsInfo = document.getElementById('controlsInfo');
        controlsInfo.innerHTML = `
            <div>💰 Currency: <span class="number_display">${profile_info.currency}</span></div>
            <div>🎯 Level: <span class="number_display">${profile_info.level}</span></div>
            <div>🫀 Max Life: <span class="number_display">${profile_info.max_life}</span></div>
        `;
    }
    
    createPaths() {
        this.paths.forEach(path => {
            const fromNode = this.nodes.find(n => n.id === path.from);
            const toNode = this.nodes.find(n => n.id === path.to);
            
            if (fromNode && toNode) {
                const pathElement = this.createCurvePath(fromNode, toNode, path.type);
                this.mapSvg.appendChild(pathElement);
            }
        });
    }
    
    createCurvePath(fromNode, toNode, type) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        
        // 计算控制点以创建平滑曲线
        const dx = toNode.x - fromNode.x;
        const dy = toNode.y - fromNode.y;
        
        // 根据路径方向调整控制点
        let cp1x, cp1y, cp2x, cp2y;
        
        if (Math.abs(dy) > 50) {
            // 有明显垂直偏移的分支路径
            cp1x = fromNode.x + dx * 0.3;
            cp1y = fromNode.y;
            cp2x = toNode.x - dx * 0.3;
            cp2y = toNode.y;
        } else {
            // 水平路径
            cp1x = fromNode.x + dx * 0.5;
            cp1y = fromNode.y + dy * 0.2;
            cp2x = toNode.x - dx * 0.5;
            cp2y = toNode.y - dy * 0.2;
        }
        
        const pathData = `M ${fromNode.x} ${fromNode.y} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${toNode.x} ${toNode.y}`;
        
        path.setAttribute('d', pathData);
        path.setAttribute('class', type === 'completed' || type === 'current' ? 'path-completed' : 'path-locked');
        
        return path;
    }
    
    createNodes() {
        this.nodes.forEach(node => {
            const nodeElement = document.createElement('div');
            nodeElement.className = `map-node node-${node.type}`;
            nodeElement.style.left = `${node.x}px`;
            nodeElement.style.top = `${node.y}px`;
            nodeElement.textContent = node.title;
            nodeElement.dataset.nodeId = node.id;
            
            
            nodeElement.addEventListener('click', async () => await this.showNodeInfo(node.node_extra));
            
            this.mapContent.appendChild(nodeElement);
        });
    }

    showSmallMessage(title,description) {
        document.getElementById('infoTitle').textContent = title;
        document.getElementById('infoDescription').textContent = description;
        this.infoPanel.classList.add('show');
        setTimeout(() => {
            this.infoPanel.classList.remove('show');
        }, 3000);
    }
    
    async showNodeInfo(node) {
        

        console.log(node)
        if(node.status!="locked" && node.name=="battle"){
            this.openBattle(node);
            this.showSmallMessage(node.agent_name,node.description);
        }else if (node.status=="current" && node.name=="shop"){
            await this.openShop(node);
        }else if (node.status=="current" && node.name=="event"){
            await this.openEvent(node);
        }
        
        
    }
    
    bindEvents() {
        // 鼠标事件
        this.mapContainer.addEventListener('mousedown', (e) => this.startDrag(e));
        document.addEventListener('mousemove', (e) => this.drag(e));
        document.addEventListener('mouseup', () => this.endDrag());
        
        // 触摸事件
        this.mapContainer.addEventListener('touchstart', (e) => this.startDrag(e.touches[0]));
        document.addEventListener('touchmove', (e) => {
            e.preventDefault();
            this.drag(e.touches[0]);
        });
        document.addEventListener('touchend', () => this.endDrag());
        
        // 防止默认的拖拽行为
        this.mapContainer.addEventListener('dragstart', (e) => e.preventDefault());
    }
    
    startDrag(e) {
        this.isDragging = true;
        this.startX = e.clientX - this.translateX;
        this.mapContainer.style.cursor = 'grabbing';
    }
    
    drag(e) {
        if (!this.isDragging) return;
        
        e.preventDefault();
        this.currentX = e.clientX - this.startX;
        
        // 限制拖拽范围，只允许横向移动
        const maxTranslate = 0;
        const minTranslate = -(500*this.mapArray.length - window.innerWidth);
        
        this.translateX = Math.max(minTranslate, Math.min(maxTranslate, this.currentX));
        
        this.mapContent.style.transform = `translateY(-50%) translateX(${this.translateX}px)`;
    }
    
    endDrag() {
        this.isDragging = false;
        this.mapContainer.style.cursor = 'grab';
    }
    initShop() {
        const shopModal = document.getElementById('shopModal');
        const shopClose = document.getElementById('shopClose');
        
        shopClose.addEventListener('click', () => {
            this.closeShop();
        });
        
        // 点击模态背景关闭商店
        shopModal.addEventListener('click', (e) => {
            if (e.target === shopModal) {
                this.closeShop();
            }
        });
        
        // ESC键关闭商店
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && shopModal.classList.contains('show')) {
                this.closeShop();
            }
        });
        
        this.renderShop();
    }
    
    async openShop(shop) {

        const response_select = await this.request_processor.select_routine(shop.id);
        this.update_map_info();
        if(response_select.state!="success"){
            this.showSmallMessage("shop","You can't select this shop");
            return 
        }


        const response = await this.request_processor.open_shop(shop.id);
        if(response.state!="success"){
            this.showSmallMessage("shop","You can't open this shop");
            return 
        }
        this.currentNode = shop;
        this.shopItems = response.shop_info.shop_items;
        this.renderShop();
        

        const shopModal = document.getElementById('shopModal');
        shopModal.classList.add('show');
        this.updateCurrencyDisplay();
        console.log('[v0] Opened shop with', this.currency, 'currency');
    }
    
    async closeShop() {
        const shopModal = document.getElementById('shopModal');
        shopModal.classList.remove('show');
        await this.request_processor.close_shop(this.currentNode.id);
        await this.update_map_info();
        this.currentNode = null;
        console.log('[v0] Closed shop');
    }
    
    renderShop() {
        const shopGrid = document.getElementById('shopGrid');
        shopGrid.innerHTML = '';
        
        this.shopItems.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'shop-item';
            itemElement.innerHTML = `
                <div class="shop-item-image">
                <img src="/${item.image_path}" alt="Image Description">
                </div>
                <div class="shop-item-name">${item.name}</div>
                <div class="shop-item-description">${item.description}</div>
                <div class="shop-item-footer">
                    <div class="shop-item-price">
                        <span class="currency-icon">💰</span>
                        ${item.price}
                    </div>
                    <button class="buy-button ${this.currency < item.price ? 'insufficient-funds' : ''}" 
                            data-item-id="${item.id}" 
                            ${this.currency < item.price || item.is_selled? 'disabled' : ''}>
                        ${this.currency < item.price || item.is_selled ? "Can't Buy" : 'Buy'}
                    </button>
                </div>
            `;
            
            const buyButton = itemElement.querySelector('.buy-button');
            buyButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.purchaseItem(item);
            });
            
            shopGrid.appendChild(itemElement);
        });
    }
    
    async purchaseItem(item) {
        if (this.currency< item.price){
            this.showSmallMessage(
                "Not enough currency",
                `Buy ${item.name} need ${item.price} coins ,You have ${this.currency}。`
            )
            
        }
        const response=await this.request_processor.shop_buy(this.currentNode.id,item.id)
        if(response.state=="success"){
            item.is_selled=true;
            
            
            await this.update_map_info();
            
            // 重新渲染商店以更新按钮状态
            this.renderShop();
            
            // 显示购买成功动画
            const shopItem = document.querySelector(`[data-item-id="${item.id}"]`).closest('.shop-item');
            shopItem.classList.add('purchase-success');
            setTimeout(() => {
                shopItem.classList.remove('purchase-success');
            }, 600);
            
            // 显示购买成功信息
            document.getElementById('infoTitle').textContent = 'Purchase Success!';
            document.getElementById('infoDescription').textContent = `You have successfully purchased ${item.name}, and it has been added to the道具背包中。`;
            this.infoPanel.classList.add('show');
            
            setTimeout(() => {
                this.infoPanel.classList.remove('show');
            }, 3000);
            
            console.log('[v0] Purchased item:', item.name, 'for', item.price, 'currency. Remaining:', this.currency);
        } else {
            this.showSmallMessage(
                "Failed",
                `You can't buy ${item.name}`
            )
            
        }
    }
    
    updateCurrencyDisplay() {
        document.getElementById('currencyAmount').textContent = this.currency;
    }
    
    addCurrency(amount) {
        this.currency += amount;
        this.updateCurrencyDisplay();
        console.log('[v0] Added', amount, 'currency. Total:', this.currency);
    }
    
    initInventory() {
        const inventoryToggle = document.getElementById('inventoryToggle');
        const inventoryPanel = document.getElementById('inventoryPanel');
        
        inventoryToggle.addEventListener('click', () => {
            inventoryPanel.classList.toggle('open');
        });
        
        // 点击面板外部关闭
        document.addEventListener('click', (e) => {
            if (!inventoryPanel.contains(e.target) && !inventoryToggle.contains(e.target)) {
                inventoryPanel.classList.remove('open');
            }
        });
        
        
    }
    
    renderInventory() {
        const inventoryGrid = document.getElementById('inventoryGrid');
        inventoryGrid.innerHTML = '';
        
        this.inventory.forEach((item, index) => {
            const itemElement = document.createElement('div');
            itemElement.className = 'inventory-item';
            itemElement.innerHTML = `
                <div class="item-image">
                <img src="/${item.image_path}" alt="Image Description">
                </div>
                <div class="item-name">${item.name}</div>
                <div class="item-description">${item.description}</div>
            `;
            
            itemElement.addEventListener('click', () => {
                this.showItemInfo(item);
            });
            
            inventoryGrid.appendChild(itemElement);
        });
    }
    
    showItemInfo(item) {
        document.getElementById('infoTitle').textContent = item.name;
        document.getElementById('infoDescription').textContent = item.description;
        this.infoPanel.classList.add('show');
        
        setTimeout(() => {
            this.infoPanel.classList.remove('show');
        }, 4000);
    }
    
    addItem(item) {
        this.inventory.push(item);
        this.renderInventory();
        console.log('[v0] Added item to inventory:', item.name);
    }
    
    removeItem(itemName) {
        const index = this.inventory.findIndex(item => item.name === itemName);
        if (index !== -1) {
            this.inventory.splice(index, 1);
            this.renderInventory();
            console.log('[v0] Removed item from inventory:', itemName);
        }
    }
    initBattle() {
        const battleModal = document.getElementById('battleModal');
        const battleClose = document.getElementById('battleClose');
        const battleEnter = document.getElementById('battleEnter');
        
        battleClose.addEventListener('click', () => {
            this.closeBattle();
        });
        
        battleEnter.addEventListener('click', async () => {
            await this.enterBattle();
        });
        
        // 点击模态背景关闭战斗
        battleModal.addEventListener('click', (e) => {
            if (e.target === battleModal) {
                this.closeBattle();
            }
        });
        
        // ESC键关闭战斗
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && battleModal.classList.contains('show')) {
                this.closeBattle();
            }
        });
    }
    
    openBattle(enemy) {
        const randomEnemy = enemy;
        this.currentNode = enemy;
        
        document.getElementById('enemyAvatar').textContent = randomEnemy.avatar;
        document.getElementById('enemyName').textContent = randomEnemy.agent_name;
        document.getElementById('enemyDescription').textContent = randomEnemy.description;
        
        let life=0
        if (enemy.status=="current"){
            life=randomEnemy.agent_max_life;
        }
        const hpPercentage = (life / randomEnemy.agent_max_life) * 100;
        document.getElementById('enemyHpFill').style.width = `${hpPercentage}%`;
        document.getElementById('enemyHpText').textContent = `${life} / ${randomEnemy.agent_max_life}`;
        
        const battleModal = document.getElementById('battleModal');
        battleModal.classList.add('show');
        
        console.log('[v0] Opened battle with enemy:', randomEnemy.agent_name);
    }
    
    closeBattle() {
        const battleModal = document.getElementById('battleModal');
        battleModal.classList.remove('show');
        console.log('[v0] Closed battle modal');
    }
    
    async enterBattle() {
        // 这里可以添加进入战斗的逻辑
        document.getElementById('infoTitle').textContent = 'Battle Start!';
        document.getElementById('infoDescription').textContent = 'You bravely face the strong enemy, and the battle is about to begin!';
        this.infoPanel.classList.add('show');
        
        setTimeout(() => {
            this.infoPanel.classList.remove('show');
        }, 3000);
        if(this.currentNode){
            await this.request_processor.select_routine(this.currentNode.id);
            const response=await this.request_processor.battle(this.currentNode.id);
            if(response.state=="find!"){
                await this.update_map_info();
                this.closeBattle();
                window.location.href = '/gaming_rogue';
            }
            
        }
        this.currentNode = null;
        
        console.log('[v0] Entered battle');


    }

    initEvent() {
        const eventModal = document.getElementById('eventModal');
        
        // 点击模态背景关闭事件
        eventModal.addEventListener('click', (e) => {
            if (e.target === eventModal) {
                this.closeEvent();
            }
        });
        
        // ESC键关闭事件
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && eventModal.classList.contains('show')) {
                this.closeEvent();
            }
        });
    }
    
    async openEvent(event) {
        const response_select = await this.request_processor.select_routine(event.id);
        this.update_map_info();
        if(response_select.state!="success"){
            this.showSmallMessage("event","You can't select this event");
            return 
        }

        const response = await this.request_processor.open_event(event.id);
        if(response.state!="success"){
            this.showSmallMessage("event","You can't open this event");
            return 
        }

        const randomEvent = response.event_info;
        
        document.getElementById('eventTitle').textContent = randomEvent.title;
        document.getElementById('eventImage').textContent = randomEvent.image;
        document.getElementById('eventDescription').textContent = randomEvent.description;
        
        const eventOptions = document.getElementById('eventOptions');
        eventOptions.innerHTML = '';
        
        randomEvent.options.forEach((option, index) => {
            const optionElement = document.createElement('div');
            if (option.is_valid){
                optionElement.className = 'event-option';
                
                optionElement.addEventListener('click', async () => {
                    await this.selectEventOption(index,event,option, randomEvent.title);
                });
            }else{
                optionElement.className = 'event-option-invalid';
            }
            optionElement.innerHTML = `
                <div class="event-option-title">${option.title}</div>
                <div class="event-option-description">${option.description}</div>
            `;
            
            
            
            eventOptions.appendChild(optionElement);
        });
        
        const eventModal = document.getElementById('eventModal');
        eventModal.classList.add('show');
        
        console.log('[v0] Opened event:', randomEvent.title);
    }
    
    closeEvent() {
        const eventModal = document.getElementById('eventModal');
        eventModal.classList.remove('show');
        console.log('[v0] Closed event modal');
    }
    
    async selectEventOption(index,event,option, eventTitle) {
        // 显示选择结果
        document.getElementById('infoTitle').textContent = `${eventTitle} - ${option.title}`;
        document.getElementById('infoDescription').textContent = option.description;
        this.infoPanel.classList.add('show');
        
        setTimeout(() => {
            this.infoPanel.classList.remove('show');
        }, 4000);
        
        this.closeEvent();
        const response = await this.request_processor.select_event_option(event.id,index);
        if(response.state!="success"){
            this.showSmallMessage("event","You can't select this event");
            return 
        }
        await this.update_map_info();
        console.log('[v0] Selected event option:', option.title);
    }
    async initCardSystem() {
        const cardButton = document.getElementById('cardButton');
        const cardModal = document.getElementById('cardModal');
        const cardClose = document.getElementById('cardClose');
        
        cardButton.addEventListener('click', () => {
            this.openCardCollection();
        });
        
        cardClose.addEventListener('click', () => {
            this.closeCardCollection();
        });
        
        // 点击模态背景关闭卡牌收藏
        cardModal.addEventListener('click', (e) => {
            if (e.target === cardModal) {
                this.closeCardCollection();
            }
        });
        
        // ESC键关闭卡牌收藏
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && cardModal.classList.contains('show')) {
                this.closeCardCollection();
            }
        });
        
        await this.initializeCardSystem(); // Call the new initialization method
        this.renderCards();
    }
    
    openCardCollection() {
        const cardModal = document.getElementById('cardModal');
        cardModal.classList.add('show');
        console.log('[v0] Opened card collection');
    }
    
    closeCardCollection() {
        const cardModal = document.getElementById('cardModal');
        cardModal.classList.remove('show');
        console.log('[v0] Closed card collection');
    }
    
    async initializeCardSystem() {
        const response = await this.request_processor.get_cards_info();
        if(response.state!="success"){
            this.showSmallMessage("card","You can't get card info");
            return 
        }
        this.cards = response.cards_info;
        console.log(this.cards)
        
    }
    
    renderCards() {
        const cardGrid = document.getElementById('cardGrid');
        cardGrid.innerHTML = '';
        
        this.cards.forEach(card => {
            const cardElement = document.createElement('div');
            cardElement.className = 'magic-card';
            
            // 解析法术力符号
            const manaSymbols = this.parseManaSymbols(card.manaCost);
            const manaHtml = manaSymbols.map(symbol => 
                `<div class="mana-symbol mana-${symbol.type}">${symbol.value}</div>`
            ).join('');
            
            // 只有生物才显示攻防
            const isCreature = card.attack!=0 && card.defense!=0;
            const statsHtml = isCreature ? `
                <div class="card-stats">
                    <div class="card-attack">
                        <div class="card-stat-icon attack-icon">⚔</div>
                        ${card.attack}
                    </div>
                    <div class="card-defense">
                        <div class="card-stat-icon defense-icon">🛡</div>
                        ${card.defense}
                    </div>
                </div>
            ` : '';
            
            cardElement.innerHTML = `
                <div class="card-quantity">${card.quantity}</div>
                <div class="card-mana-cost">${manaHtml}</div>
                <div class="card-image">
                    <img src="/${card.image_path}" alt="${card.name}">
                </div>
                <div class="card-name">
                    <h3>${card.name}</h3>
                    <div class="card-type">${card.type}</div>
                </div>
                <div class="card-description">
                    <div class="card-text">${card.description}</div>
                    ${statsHtml}
                </div>
            `;
            
            cardElement.addEventListener('click', () => {
                this.showCardDetails(card);
            });
            
            cardGrid.appendChild(cardElement);
        });
    }

    parseManaSymbols(manaCost) {
        const symbols = [];
        let i = 0;
        
        while (i < manaCost.length) {
            const char = manaCost[i];
            
            if (/\d/.test(char)) {
                // 数字法术力
                let num = '';
                while (i < manaCost.length && /\d/.test(manaCost[i])) {
                    num += manaCost[i];
                    i++;
                }
                if (num !== '0') {
                    symbols.push({ type: 'colorless', value: num });
                }
            } else {
                // 颜色法术力
                const colorMap = {
                    'W': 'white',
                    'U': 'blue', 
                    'B': 'black',
                    'R': 'red',
                    'G': 'green'
                };
                
                if (colorMap[char]) {
                    symbols.push({ type: colorMap[char], value: char });
                }
                i++;
            }
        }
        
        return symbols;
    }
    
    showCardDetails(card) {
        document.getElementById('infoTitle').textContent = `${card.name} (${card.type})`;
        document.getElementById('infoDescription').textContent = 
            `法力消耗: ${card.manaCost} | 攻击: ${card.attack} | 防御: ${card.defense} | 数量: ${card.quantity}\n\n${card.description}`;
        this.infoPanel.classList.add('show');
        
        setTimeout(() => {
            this.infoPanel.classList.remove('show');
        }, 4000);
        
        console.log('[v0] Showed card details for:', card.name);
    }
    
    addCard(name, manaCost, type, image, description, attack, defense, quantity = 1) {
        const existingCard = this.cards.find(card => card.name === name);
        if (existingCard) {
            existingCard.quantity += quantity;
        } else {
            this.cards.push({
                name, manaCost, type, image, description, attack, defense, quantity
            });
        }
        this.renderCards();
        console.log('[v0] Added card:', name, 'quantity:', quantity);
    }

    initGiveUpButton() {
        const giveUpButton = document.getElementById('giveUpButton');
        const confirmModal = document.getElementById('confirmModal');
        const confirmYes = document.getElementById('confirmYes');
        const confirmNo = document.getElementById('confirmNo');

        // 点击放弃按钮显示确认弹窗
        giveUpButton.addEventListener('click', () => {
            confirmModal.classList.add('show');
        });

        // 点击确认按钮
        confirmYes.addEventListener('click', async () => {
            confirmModal.classList.remove('show');
            // 这里可以添加重置游戏的逻辑
            const response = await this.request_processor.give_up_rogue();
            if(response.state!="success"){
                this.showSmallMessage("give up","You can't give up");
                return 
            }
            window.location.href = '/';
        });

        // 点击取消按钮
        confirmNo.addEventListener('click', () => {
            confirmModal.classList.remove('show');
        });

        // 点击背景关闭
        confirmModal.addEventListener('click', (e) => {
            if (e.target === confirmModal) {
                confirmModal.classList.remove('show');
            }
        });
    }

}

function generateMapFromArray(mapArray) {
    if (window.interactiveMap) {
        window.interactiveMap.generateMapFromArray(mapArray);
    }
}




function addInventoryItem(name, icon, description) {
    if (window.interactiveMap) {
        window.interactiveMap.addItem({ name, icon, description });
    }
}

function removeInventoryItem(itemName) {
    if (window.interactiveMap) {
        window.interactiveMap.removeItem(itemName);
    }
}
function addCurrency(amount) {
    if (window.interactiveMap) {
        window.interactiveMap.addCurrency(amount);
    }
}

function getCurrency() {
    return window.interactiveMap ? window.interactiveMap.currency : 0;
}

function arraysEqual(a, b) {
    return JSON.stringify(a) === JSON.stringify(b);
}
// function arraysEqual(a, b) {
//     if (a.length !== b.length) return false;
//     return a.every((item, idx) => normalize(item) === normalize(b[idx]));
// }


// function normalize(obj) {
// return JSON.stringify(
//     Object.keys(obj).sort().reduce((acc, key) => {
//     acc[key] = obj[key];
//     return acc;
//     }, {})
// );
// }
// 初始化地图
document.addEventListener('DOMContentLoaded', () => {
    window.interactiveMap = new InteractiveMap();
});