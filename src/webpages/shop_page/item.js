// One catalog entry. Pack rules and prices are supplied by /shop/items.
class Item {
    constructor(name, price, img_path, id) {
        this.name = name;
        this.price = price;
        this.id = id;
        this.pack_url = img_path;
        this.art = getPackArt(this);
        this.element = this.create_item();
    }
    static node(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text != null) node.textContent = String(text);
        return node;
    }
    apply_art(element) {
        element.style.setProperty('--pack-color', this.art.color);
        element.style.setProperty('--pack-trim', this.art.trim);
        element.style.setProperty('--pack-depth', (12 + this.art.depth * 16) + 'px');
        element.dataset.shape = this.art.shape;
        const image = element.querySelector('img');
        image.hidden = false;
        image.alt = '';
        image.decoding = 'async';
        image.onerror = () => { image.onerror = () => { image.hidden = true; }; image.src = this.art.fallback; };
        image.src = this.art.image;
    }
    create_item() {
        const button = Item.node('button', 'shop_item');
        button.type = 'button';
        button.dataset.itemId = this.id;
        button.setAttribute('aria-pressed', 'false');
        button.setAttribute('aria-label', this.name + ' Pack, ' + this.price + ' coins');
        const display = Item.node('span', 'item-display');
        const pack = Item.node('span', 'pack-volume');
        pack.append(Item.node('img'), Item.node('span', 'pack-spine'));
        display.append(pack);
        const label = Item.node('span', 'shop_item_info');
        const price = Item.node('span', 'shop_item_price');
        const coin = Item.node('span', 'coin-mark', '✧'); coin.setAttribute('aria-hidden', 'true');
        price.append(coin, Item.node('span', '', this.price));
        label.append(Item.node('span', 'shop_item_name', this.name), price);
        button.append(display, label);
        this.apply_art(button);
        return button;
    }
}
