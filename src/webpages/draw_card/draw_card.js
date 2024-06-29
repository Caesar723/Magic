class Draw_card{

    constructor(camera,ctx){
        this.ctx=ctx;
        this.packs=[]
        this.click_stack=[];
        this.initinal_pack_position()
        this.moving_mouse_obj=0;
        
        this.isMouseDown=false;
        this.open_pack_flag=false;
        this.camera=camera;

        this.card_show=[];
        this.card_in_pack=[]

        this.packs_roll=0;//used in rolling the packs

        this.send_packs_request()

        this.frame_generator=new Card_frame()
    }
    set_listener(canvas){
        this.canvas=canvas;
        this.canvas.addEventListener('mousedown', (event) => {
            if (this.open_pack_flag==false){
                this.isMouseDown = true;
                for (let i in this.click_stack){
                    if (this.check_inside(this.get_mouse_pos(event,canvas),...this.click_stack[i].get_position_in_screen())){
                        this.moving_mouse_obj=this.click_stack[i]
                    }
                }
                console.log('mousedown')
            }
            else{
                if (this.check_inside(this.get_mouse_pos(event,canvas),...this.moving_mouse_obj.get_position_in_screen())){
                    if (this.card_in_pack.length===0){
                        
                        this.card_show=[];
                        this.packs=this.packs.filter(item => item !== this.moving_mouse_obj);
                        this.click_stack=this.click_stack.filter(item => item !== this.moving_mouse_obj);
                        this.moving_mouse_obj=0;
                        this.open_pack_flag=false;
                        this.initinal_pack_position();
                    }
                    else{
                        this.draw_a_card()
                    }
                    

                    console.log("draw")
                }
            }
            
        });

        this.canvas.addEventListener('mousemove', (event) => {
            if (this.open_pack_flag==false){
                if (this.moving_mouse_obj!=0){
                    console.log('mousemove')
                    const mouse_position=this.get_mouse_pos(event,canvas);
                    mouse_position[0]=mouse_position[0]-canvas.width/2;
                    mouse_position[1]=mouse_position[1]-canvas.height/2;
                    this.moving_mouse_obj.moving_by_mouse(mouse_position,this.camera)
                }
            }
            
            
        });
        this.canvas.addEventListener('mouseup', (event) => {
            if (this.open_pack_flag==false){
                if (this.moving_mouse_obj!=0){
                    const mouse_position=this.get_mouse_pos(event,canvas);
                    if (canvas.width*0.8>mouse_position[0] && mouse_position[0]>0){
                        this.open_pack_flag=true;
                        this.open_pack(this.moving_mouse_obj)
                        this.send_pack_detail()
                    }
                    else{
                        this.moving_mouse_obj=0
                        this.initinal_pack_position();
                    }
                    
                }
                // important !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!this.moving_mouse_obj=0
                console.log('mouseup')
            }
        });

        this.canvas.addEventListener('wheel', (event)=> {
            // 滚轮事件处理
            if (this.open_pack_flag==false){
                console.log('滚轮事件：', event);
                this.packs_roll=this.packs_roll-event.deltaY;
                console.log(this.packs_roll);
                this.packs_roll=math.min(this.packs_roll,0)
                this.initinal_pack_position();
            }
            // 防止页面滚动
            event.preventDefault();
            
    
            // 可以根据需要在此处添加更多的逻辑
            // 例如，根据滚轮的方向缩放画布或者进行其他操作
        });
    }
    

    get_mouse_pos(event,canvas){
        var rect = canvas.getBoundingClientRect();
        console.log(rect)
        // 计算鼠标相对于canvas的位置
        var mouseX = (event.clientX - rect.left)*canvas.width/rect.width;
        var mouseY = (event.clientY - rect.top)*canvas.height/rect.height;
        return [mouseX,mouseY]
    }

    check_inside(mouse_pos,position1,position2,position3,position4){//n shape of points
        
        return (
            this.create_function_x(mouse_pos,position1,position2)<0 &&
            this.create_function_y(mouse_pos,position3,position2)>0 &&
            this.create_function_x(mouse_pos,position3,position4)>0 &&
            this.create_function_y(mouse_pos,position4,position1)<0
        )

    }
    create_function_x(mouse_pos,position1,position2){// for x=... position1(lower x) x-...
        const k=(position2[0]-position1[0])/(position2[1]-position1[1]);
        console.log(k)
        const b=position1[0]-k*position1[1];
        return mouse_pos[0]-(mouse_pos[1])*k-b
    }
    create_function_y(mouse_pos,position1,position2){// for y=... position1(lower x) y-....
        const k=(position2[1]-position1[1])/(position2[0]-position1[0]);
        const b=position1[1]-k*position1[0];
        return mouse_pos[1]-(mouse_pos[0])*k-b
    }
    initinal_pack_position(){
        const POSITION_X=2000;
        const POSITION_Y=-700;
        const POSITION_Z=3000;
        const rate=1
        for(let i in this.packs){
            this.packs[i].position=[POSITION_X,POSITION_Y+900*i+this.packs_roll*rate,POSITION_Z];
            this.packs[i].angle_x=0;
            this.packs[i].angle_y=0;
        }
    }

    open_pack(pack){//pack [cards]
        pack.position=[-this.canvas.width*0.4,600,3000];
        pack.angle_x=0;
        pack.angle_y=0;
    }

    draw_a_card(){
        if (this.card_in_pack.length != 0){
            const card=this.card_in_pack.pop()
            card.draw_card()
            this.card_show.push(card)
        }

        
    }

    async send_pack_detail(){//return card detail
        
        const data = { id: this.moving_mouse_obj.id, name: this.moving_mouse_obj.name ,name_id:this.moving_mouse_obj.name_id};
        console.log()
        const response = await fetch('/send_pack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const responseData =await response.json()
        console.log(responseData)
        this.process_response_cards(JSON.parse(responseData));
    }
    process_response_cards(data){
        for(let card_i in data){
            const image=this.frame_generator.generate_card(
                data[card_i]["Background_url"],
                data[card_i]["Name"],
                data[card_i]["Type_card"],
                data[card_i]["Rarity"],
                data[card_i]["Ability"],
                data[card_i]["Image_url"]

            )
            var card=NaN;
            if (data[card_i]["Type_card"]=="Instant"){
                card=new Instant(4,5.62,[0,0,40],3,image,data[card_i]['Cost'],data[card_i]["Name"])
            }
            else if(data[card_i]["Type_card"]=="land"){
                card=new Land(4,5.62,[0,0,40],3,image,data[card_i]["Name"])
            }
            else if(data[card_i]["Type_card"]=="sorcery"){
                card=new Sorcery(4,5.62,[0,0,40],3,image,data[card_i]['Cost'],data[card_i]["Name"])
            }
            else{
                card=new Creature(4,5.62,[0,0,40],3,image,data[card_i]['Cost'],data[card_i]["Power"],data[card_i]["Toughness"],data[card_i]["Name"])
            }

            this.card_in_pack.push(card)
            
            
        }
    }

    async send_packs_request(){//return packs detail
        const data = { "message": 'get_packs_information'};
        const response = await fetch('/get_packs_information', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const responseData = await response.json();
        console.log(responseData);
        this.process_responseData(JSON.parse(responseData))
    }
    process_responseData(data){//[{"id": 1, "pack_url": "webpages/image_source/packs/pack_org.jpg", "name": "Original", "quantity": 3}, {"id": 5, "pack_url": "webpages/image_source/packs/green.png", "name": "Green", "quantity": 1}, {"id": 6, "pack_url": "webpages/image_source/packs/blue.png", "name": "Blue", "quantity": 1}]
        const size_rat=7/10;
        var SIZE=1000*size_rat;
        for (let i in data){
            console.log(data[i])
            for (let num=0;num<data[i]["quantity"];num++){
                console.log(data[i]["name"])
                const pack=new Pack([0,0,0],SIZE,data[i]["pack_url"],data[i]["name"],data[i]["id"],data[i]["name_id"])
                this.packs.push(pack);
                this.click_stack.push(pack);
            }
            
        }
        this.initinal_pack_position()
    }

    update(){
        
        for(let card in this.card_show){
            this.card_show[card].update()
        }
        for(let pack in this.packs){
            this.packs[pack].update()
        }
    }
    draw(){
        for(let card in this.card_show){
            this.card_show[card].draw(this.camera,this.ctx,this.canvas)
        }
        for(let pack in this.packs){
            this.packs[pack].draw(this.camera,this.ctx,this.canvas)
        }
    }

}