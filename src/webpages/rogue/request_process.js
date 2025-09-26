



class Request_Processor{

    constructor(){
        this.base_url="/rogue/"
    }

    async send_request(link,data={}){
        const response = await fetch(this.base_url+link, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if(response.ok){
            return response.json()
        }else{
            return {"state":"error"}
        }
    }

    async get_map_info(){
         const data = await this.send_request("map_info")
         console.log(data)
         return data
    }
    async get_treasure_info(){
        const data = await this.send_request("treasure_info")
        console.log(data)
        return data
    }
    async get_profile_info(){
        const data = await this.send_request("get_profile_info")
        console.log(data)
        return data
    }

    async select_routine(node_id){
        const data = await this.send_request("select_routine",{node_id:node_id})
        console.log(data)
        return data
    }

    async close_shop(node_id){
        const data = await this.send_request("close_shop",{node_id:node_id})
        console.log(data)
        return data
    }

    async choose_event(event_id){
        const data = await this.send_request("choose_event",{node_id:event_id})
        console.log(data)
        return data
    }

    async open_shop(shop_id){
        const data = await this.send_request("open_shop",{node_id:shop_id})
        console.log(data)
        return data
    }   

    async open_event(event_id){
        const data = await this.send_request("open_event",{node_id:event_id})
        console.log(data)
        return data
    }

    async get_cards_info(){
        const data = await this.send_request("get_cards_info")
        console.log(data)
        return data
    }


    async select_event_option(event_id,option_index){
        const data = await this.send_request("select_event_option",{event_id:event_id,option_index:option_index})
        console.log(data)
        return data
    }

    async battle(node_id){
        const data = await this.send_request("battle",{node_id:node_id})
        console.log(data)
        return data
    }
    
    
}