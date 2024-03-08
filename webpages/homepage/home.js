function choose_a_deck() {
    var box = document.getElementById('box_decks');
    var container=document.getElementById('button-container')
    // 根据方框的当前状态切换类
    if (box.classList.contains('box_decks-visible')) {
            
            box.classList.remove('box_decks-visible');
            box.style.left="-20vw"
            
            box.style.borderBottomRightRadius = '0';
            box.style.borderTopRightRadius="0"
            
            
            container.classList.remove('blur');
    } else {
            box.classList.add('box_decks-visible');
            box.style.left="0"
            box.style.borderBottomRightRadius = "2vw";
            box.style.borderTopRightRadius="2vw"
            
            container.classList.add('blur');
            
    }
    }

class Home{

    constructor(decks){
        this.set_listener()
        this.decks=decks
    }

    set_listener(){
        const draw = document.getElementById('draw');
        draw.addEventListener('click',  function () {
            window.location.href = '/draw_card';
        });

        const deck_building = document.getElementById('deck');
        deck_building.addEventListener('click',  function () {
            window.location.href = '/deck_building';
        });


        document.getElementById('choose').addEventListener('click', choose_a_deck);
        
        const start_gaming = document.getElementById('start');
        start_gaming.addEventListener('click', (event)=> {
            console.log(this.decks.seleted_deck)
            if (this.decks.seleted_deck){
                this.start_matching()
            }
            else{
                choose_a_deck()
            }
            
        });
    }
    async start_matching(){
        
        var responseData =await this.send_match_request()
        while (responseData["state"]=="waiting"){
            await this.set_time()
            var responseData =await this.send_match_request()
            console.log(responseData)
        }

        if (responseData["state"]!="find!"){
            const response = await fetch('/matching_delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
        }else{
            window.location.href = '/gaming';
        }

        


    }
    set_time(){
        return new Promise(resolve => setTimeout(resolve, 3000));
    }

    async send_match_request(){
        
        const response = await fetch('/matching', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "id":this.decks.seleted_deck[0],"name":this.decks.seleted_deck[1] }) // 将数据转换为JSON字符串
        });
        const responseData =await response.json()
        return responseData
    }
}