class Request_Processor {
    constructor() { this.base_url = '/rogue/'; }
    async send_request(link, data = {}) {
        const response = await fetch(this.base_url + link, {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data), signal: AbortSignal.timeout(20000)
        });
        if (!response.ok || response.redirected) throw new Error('The request could not be confirmed.');
        return response.json();
    }
    get_map_info() { return this.send_request('map_info'); }
    get_treasure_info() { return this.send_request('treasure_info'); }
    get_profile_info() { return this.send_request('get_profile_info'); }
    get_cards_info() { return this.send_request('get_cards_info'); }
    select_routine(node_id) { return this.send_request('select_routine', {node_id}); }
    close_shop(node_id) { return this.send_request('close_shop', {node_id}); }
    choose_event(node_id) { return this.send_request('choose_event', {node_id}); }
    open_shop(node_id) { return this.send_request('open_shop', {node_id}); }
    open_event(node_id) { return this.send_request('open_event', {node_id}); }
    select_event_option(event_id, option_index) { return this.send_request('select_event_option', {event_id, option_index}); }
    battle(node_id) { return this.send_request('battle', {node_id}); }
    shop_buy(shop_id, item_id) { return this.send_request('shop_buy', {shop_id, item_id}); }
    give_up_rogue() { return this.send_request('give_up_rogue'); }
}
