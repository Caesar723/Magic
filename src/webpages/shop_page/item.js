class Item{
    constructor(name,price,img_path,id){
        console.log(name,price,img_path,id);
        const size_rat=7/10;
        const SIZE=1000*size_rat;
        this.name=name;
        this.price=price;
        this.id=id;
        this.img_path=img_path;
        this.pack=new Pack([0,0,0],SIZE,img_path,name,id,-1);

        this.element=this.create_item();

        document.addEventListener("mousemove",(event)=>{
            this.change_pack_angle(event);
        });
    }
    draw(camera){
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.strokeStyle = 'white';
        this.pack.draw(camera,this.ctx,this.canvas);
    }
    update(){
        this.pack.update();
    }

    change_pack_angle(event){
        const mouseX=event.clientX;
        const mouseY=event.clientY;
        const canvasX=this.canvas.getBoundingClientRect().left + this.canvas.width/2;
        const canvasY=this.canvas.getBoundingClientRect().top + this.canvas.height/2;
        const dx = -(mouseX - canvasX)/1000;
        const dy = (mouseY - canvasY)/1000;
        //const angle = Math.atan2(dy, dx);
        this.pack.angle_y = dx > 0.4 ? 0.4 : (dx < -0.4 ? -0.4 : dx);
        this.pack.angle_x = dy > 0.4 ? 0.4 : (dy < -0.4 ? -0.4 : dy);
    }

    create_item(){
        const element=document.createElement("div");
        this.canvas=document.createElement("canvas");
        this.canvas.width=180;
        this.canvas.height=180;
        element.classList.add("shop_item");
        this.ctx=this.canvas.getContext("2d");


        this.element_img_container=document.createElement("div");
        this.element_img_container.classList.add("image_container");
        this.element_img_container.appendChild(this.canvas);
        element.appendChild(this.element_img_container);

        const element_info=document.createElement("div");
        element_info.classList.add("shop_item_info");
        element.appendChild(element_info);

        const element_name=document.createElement("div");
        element_name.classList.add("shop_item_name");
        element_name.textContent=this.name;
        element_info.appendChild(element_name);

        const element_price=document.createElement("div");
        element_price.classList.add("shop_item_price");
        element_price.textContent=this.price;
        element_info.appendChild(element_price);

        const element_buy=document.createElement("div");
        element_buy.classList.add("shop_item_buy");
        element_buy.textContent="Buy";
        element_buy.addEventListener("click",()=>{
            this.buy();
        });
        element_info.appendChild(element_buy);

        element.appendChild(element_info);
        return element;
    }
    buy(){
        console.log("buy");
        this.create_buy_small_page_element();
    }
    create_buy_small_page_element(){
        
        // if (document.querySelector('.dark-overlay')) {
        //     document.body.removeChild(document.querySelector('.dark-overlay'));
        // }

        const element_background=document.createElement("div");
        element_background.classList.add("dark-overlay");
        element_background.addEventListener("click",(event)=>{
            console.log("click");
            if (event.target === element_background) {
                document.body.removeChild(document.querySelector('.dark-overlay'));
                this.element_img_container.appendChild(this.canvas);
            }
        });
        const element=document.createElement("div");
        element.classList.add("buy_small_page");
        
        element.appendChild(this.canvas);

        const content=document.createElement("div");
        content.innerHTML=`
            <div class='buy_small_page_content_text'>Are you sure to buy this pack ${this.name}?</div>
            <div class='buy_small_page_content_button_container'>
                <svg class='buy_small_page_content_button yes_button' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 12.6111L8.92308 17.5L20 6.5" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg class='buy_small_page_content_button no_button' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 5L4.99998 19M5.00001 5L19 19" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                </svg>
            </div>
        `;
        content.querySelector('.yes_button').addEventListener('click', async (event) => {
            await this.correct_click(event);
        });
        content.querySelector('.no_button').addEventListener('click', async (event) => {
            await this.wrong_click(event);
        });
        content.classList.add("buy_small_page_content");
        element.appendChild(content);



        element_background.appendChild(element);
        document.body.appendChild(element_background);
        
    }
    async correct_click(event){
        console.log("correct");
        console.log(this.id,this.name);
        const response=await fetch("/shop/buy", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: this.id,
                name: this.name,
                name_id: -1
            })
        });
        const data=await response.json();
        console.log(data);
        if(data.status==200){
            const currency=data.currency;
            const element=document.getElementById('currency')
            const span=element.querySelector('.button-text')
            span.innerHTML=`<img src="webpages/homepage/coin.png" alt="Description" id="img_coin">${currency}`
            document.body.removeChild(document.querySelector('.dark-overlay'));
            this.element_img_container.appendChild(this.canvas);
        }else{
            alert(data.message);
        }
    }

    async wrong_click(event){
        document.body.removeChild(document.querySelector('.dark-overlay'));
        this.element_img_container.appendChild(this.canvas);
    }
}

