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
        this.set_image_video()
        
        this.decks=decks
    }

    set_listener(){
        const pages={
            "draw":"/draw_card",
            "deck":"/deck_building",
            "shop":"/shop",
            "studio":"/studio",
            "tasks":"/task",
        }
        for (let page in pages){
            document.getElementById(page).addEventListener('click', (event)=> {
                window.location.href = pages[page];
            });
        }


        document.getElementById('choose').addEventListener('click', choose_a_deck);
        
        const start_gaming_ai = document.getElementById('tutorial');
        start_gaming_ai.addEventListener('click', (event)=> {
            console.log(this.decks.seleted_deck)
            if (this.decks.seleted_deck){
                this.start_matching_ai()
            }
            else{
                choose_a_deck()
            }
            
        });
        const start_gaming_rogue = document.getElementById('rogue');
        start_gaming_rogue.addEventListener('click', (event)=> {
            if (this.decks.seleted_deck){
                this.start_matching_rogue()
            }
            else{
                choose_a_deck()
            }
        });
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

        document.getElementById('history').addEventListener('click', (event)=> {
            window.location.href = '/game_replay';
        });

        
    }
    async start_matching(){
        let cross_flag=true
        const cross = document.createElement('div');
        cross.classList.add('wrapper')
        const icon=document.createElement('div')
        icon.classList.add('icon')
        icon.classList.add('nav-icon')
        icon.innerHTML = `
            <span></span><span></span><span></span>
        `;

        icon.addEventListener('click', (event) =>
        {
            container.classList.remove('blur');
            document.body.removeChild(book.book_html);
            cross_flag=false
        });
        icon.addEventListener('mouseover', (event) =>
        {
            icon.classList.toggle("open");
        });
        icon.addEventListener('mouseout', (event) =>
        {
            icon.classList.toggle("open");
        });
        cross.appendChild(icon)

        const book=new Book(cross);
        document.body.appendChild(book.book_html);
        book.init()
        
        var responseData =await this.send_match_request('/matching')
        var container=document.getElementById('button-container')
        container.classList.add('blur');

        



        while (responseData["state"]=="waiting" && cross_flag){
            
            await this.set_time()
            book.turn_page(false)
            var responseData =await this.send_match_request('/matching')
            console.log(responseData)
        }

        if (responseData["state"]=="find!"){
            await this.set_time()
            book.turn_page(true)
            await this.set_time()
            window.location.href = '/gaming';
        }else{
            const response = await fetch('/matching_delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
            
        }

        


    }
    async start_matching_rogue(){
        const response = await this.send_match_request('/rogue/initinal_room');
        
        console.log(response)
        if (response["state"]=="success" || response["state"]=="already in room"){
            window.location.href = '/rogue/rogue_map';
        }
    }
    async start_matching_ai(){
        
        var responseData =await this.send_match_request("/matching_ai")
        

        if (responseData["state"]!="find!"){
            const response = await fetch('/matching_delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
        }else{
            window.location.href = '/gaming_ai';
        }
    }

    set_time(){
        return new Promise(resolve => setTimeout(resolve, 3000));
    }

    async send_match_request(name){
        
        const response = await fetch(name, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "id":this.decks.seleted_deck[0],"name":this.decks.seleted_deck[1] }) // 将数据转换为JSON字符串
        });
        const responseData =await response.json()
        return responseData
    }

    set_image_video(){
        var imageContainers = document.getElementsByClassName('image-container');
        for (var i = 0; i < imageContainers.length; i++) {
            // 在当前 'image-container' 中获取第一个 'img'
            let img = imageContainers[i].querySelector('img');
            // 在当前 'image-container' 中获取第一个 'video'
            
            let video = imageContainers[i].querySelector('video');
            
            imageContainers[i].addEventListener('mouseover', function() {
                video.style.display = 'block';
                video.currentTime = 0;
                img.style.display = 'none';
                
                video.play().then(() => {
                    //console.log('Playback initiated successfully.');
                }).catch(error => {
                    //console.error('Error attempting to play video:', error);
                });
                

            });
        
            imageContainers[i].addEventListener('mouseout', function() {
                video.pause();
                video.style.display = 'none';
                img.style.display = 'block';
                
            });
        
            
        }
        
    }
}