class Decks_Container{

    constructor(){
        this.get_all_decks()
        this.process_listener()
        this.seleted_deck=NaN//[id,name]
        this.all_decks=[]
        
        
    }

    async get_all_decks(){
        const response = await fetch('/get_decks_home', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const responseData =await response.json()
        console.log(responseData)
        this.process_data(responseData)
        console.log(this.all_decks)
    }

    process_data(data){
        for (let i in data){
            
            this.all_decks.push(new Deck(...data[i]["content"],this,data[i]["id"]))
        }
    }   

    draw(){
        const box_cards_1=document.getElementById('box_cards_1');
        const box_cards_2=document.getElementById('box_cards_2');
        this.check_box(box_cards_1)
        this.check_box(box_cards_2)
    }

    check_box(box_cards){
        if (box_cards.classList.contains('box_cards_front') && box_cards.hasChildNodes()) {
            
            const element=box_cards.firstChild
            for( let i in this.all_decks){
                if (this.all_decks[i].canvas===element){
                    this.all_decks[i].draw_canvas()

                }
            }
        }
    }

    process_listener(){
        const choose_deck=document.getElementById('choose_deck');
        const delete_deck=document.getElementById('delete_deck');

        choose_deck.addEventListener('click',(event)=> {
            const deck_seleted=this.find_child("button_process_deck_click")
            this.seleted_deck=[deck_seleted.id,deck_seleted.name]
            this.clear_child("button_process_deck_click")
            this.close_all()
            
        })
        delete_deck.addEventListener('click',async (event)=> {
            const deck_seleted=this.find_child("button_process_deck_click")
            await this.delete_deck(deck_seleted)
            this.clear_child("button_process_deck_click")
            this.close_all()
        })
    }
    async delete_deck(deck){
        const response = await fetch('/delete_deck', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "id":deck.id,"name":deck.name }) // 将数据转换为JSON字符串
        });
        const responseData =await response.json()
        console.log(responseData)
        if (responseData["state"]=="successful"){

            deck.divbutton.remove();
            const index=this.all_decks.indexOf(deck)
            if (index > -1) {
                this.all_decks.splice(index, 1); // 如果找到了，删除这个元素
            }
            
        }
        else{
            showBox("Error Occur, can not delete deck")
        }
    }
    close_all(){
        console.log(1)
        var box = document.getElementById('box_decks');
        var container=document.getElementById('button-container')
        var button_process=document.getElementById('button_process')
        var box_cards_1=document.getElementById('box_cards_1')
        var box_cards_2=document.getElementById('box_cards_2')
       
        // 根据方框的当前状态切换类
        
        button_process.classList.remove('show_button_process');
        box_cards_1.classList.remove('box_cards_front');
        box_cards_2.classList.remove('box_cards_front');
                
        box.classList.remove('box_decks-visible');
        box.style.left="-20vw"
        
        box.style.borderBottomRightRadius = '0';
        box.style.borderTopRightRadius="0"
        
        
        container.classList.remove('blur');
        
        
    }
    clear_child(class_name){
        for (let i in this.all_decks){
            const deck=this.all_decks[i];
            deck.divbutton.classList.remove(class_name);
        }
    }
    find_child(class_name){
        for (let i in this.all_decks){
            const deck=this.all_decks[i];
            if (deck.divbutton.classList.contains(class_name)) {
                return deck
            }
        }
        return false
    }

}

