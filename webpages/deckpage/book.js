class Book{

    constructor(camera,deck){
        this.deck=deck
        this.frame_generator= new Card_frame()

        this.camera=camera
        this.canvas = document.getElementById("myCanvas");
        this.ctx = this.canvas.getContext("2d");
        this.canvas.width = 1470;
        this.canvas.height = 742;
        this.background_canvas=this.initinal_book_background()
        this.ctx.save()

        this.page=this.initinal_page();
        this.page_ctx=this.page.getContext("2d");
        
        this.front_page=this.initinal_a_canvas();
        this.front_page_ctx=this.front_page.getContext("2d");
        

        this.back_page=this.initinal_a_canvas();
        this.back_page_ctx=this.back_page.getContext("2d");
        

        this.hide_page=this.initinal_a_canvas();
        this.hide_page_ctx=this.hide_page.getContext("2d");
        

        this.point_O=[-250+this.canvas.width*0.7,40+this.canvas.height*0.75]

        //this.i=550
        this.turing_flag=false;
        this.start_page_turing(1);

        this.front_page_cards=[];
        this.back_page_cards=[];

        this.current_color_mark="colorless";//"blue","gold","black","red","green","colorless"
        this.current_color_dict={
            "Blue":"blue",
            "White":"gold",
            "Black":"black",
            "Red":"red",
            "Green":"green"
        }
        this.current_type_mark="creature";//creature,sorcery,Instant,land
        this.current_type_dict={
            "Creature":"creature",
            "Sorcery":"sorcery",
            "Instant":"Instant",
            "Land":"land"
        }
        this.page_number=1
        this.page_dict={
            "creature":{"blue":{},"gold":{},"black":{},"red":{},"green":{},"colorless":{}},
            "sorcery":{"blue":{},"gold":{},"black":{},"red":{},"green":{},"colorless":{}},
            "Instant":{"blue":{},"gold":{},"black":{},"red":{},"green":{},"colorless":{}},
            "land":{"blue":{},"gold":{},"black":{},"red":{},"green":{},"colorless":{}}
        }
        

        this.set_book_mark_dict()
        this.set_lestener()
        this.startTime = performance.now();
        this.target_card=NaN;
        this.clicked_flag=false

        this.arrows_list=[
            new Arrow("rgb(231,141,51,0.9)",750,320,30,20,1),
            new Arrow("rgb(231,141,51,0.9)",20,320,30,20,-1)
        ]
        //this.send_page_request()

        
    }
    showBox(content) {
        const box = document.getElementById('box');
        var message = document.getElementById('text_box')
        message.textContent=content
        box.style.visibility = 'visible';
        box.style.opacity = 1;
        box.style.borderRadius = '10%'; // 变为无圆角
        box.style.transform = 'translate(-50%, -50%) scale(1)'; // 变为原始大小
        setTimeout(() => {
            box.style.opacity = 0;
            box.style.borderRadius = '50%'; // 再次变为圆形
            box.style.transform = 'translate(-50%, -50%) scale(0)'; // 缩小回0
            // 确保visibility的改变延迟执行，以便opacity渐变完成
            setTimeout(() => {
              box.style.visibility = 'hidden';
            }, 500); // 这里的延迟应与CSS中transition的持续时间相匹配
          }, 3000); // 3秒后开始淡出
        
    }
    set_lestener(){
        this.canvas.addEventListener('mousedown', (event) => {
            if (this.clicked_flag){
                this.target_card=NaN;
                this.clicked_flag=false;
            }
            else{
                const mouse_pos=this.get_mouse_pos(event,this.canvas)
                this.check_buttons(mouse_pos)

                const card_clicked=this.find_cards_by_mouse(mouse_pos)
                if (card_clicked){
                    this.target_card=card_clicked
                    
                }
                this.startTime = performance.now();
            }
            
            
        });

        this.canvas.addEventListener('mousemove', (event) => {
            if (this.target_card && this.clicked_flag==false){
                const mouse_position=this.get_mouse_pos(event,this.canvas);
                mouse_position[0]=mouse_position[0]-this.canvas.width/2;
                mouse_position[1]=mouse_position[1]-this.canvas.height/2;
                this.target_card.moving_by_mouse(mouse_position,this.camera)
            }
        });
        this.canvas.addEventListener('mouseup', (event) => {
            const mouse_pos=this.get_mouse_pos(event,this.canvas)
            if (this.target_card ){
                if (performance.now()-this.startTime<0.15*1000){
                    this.clicked_flag=true
                    
                    this.target_card.start_move_enlarge(5,0.1,[0,0,this.target_card.position[2]])
                }
                else{
                    console.log(this.target_card.position_in_screen[0],this.canvas.width*0.8)
                    if (this.target_card.position_in_screen[0][0]>this.canvas.width*0.8){
                        
                        if (this.target_card.quantity-1!=-1){
                            this.target_card.quantity--
                            this.deck.push_card(this.target_card);
                        }
                        
                        
                    }
                    this.target_card=NaN;
                }

                
            }
            else{
                
                if (performance.now()-this.startTime<0.15*1000){
                    
                    const checked_card=this.deck.check_mouse(mouse_pos);
                    
                }
            }
        });

        this.canvas.addEventListener('wheel', (event)=> {
            // 滚轮事件处理
            if (this.clicked_flag==false){
                
                this.deck.offset=this.deck.offset-event.deltaY;
                
                this.deck.offset=math.min(this.deck.offset,0)
                
            }
            event.preventDefault();
            
    
            // 可以根据需要在此处添加更多的逻辑
            // 例如，根据滚轮的方向缩放画布或者进行其他操作
        });

        document.getElementById('build').addEventListener('click', async()=>{
            
            const input = document.getElementById('deck_name');
            if (input.value.trim() === '') { // 检查输入框是否为空（忽略空格）
                
                input.classList.add('breath'); // 添加呼吸效果
            } 
            else if(this.deck.check_empty()){
                this.showBox("This deck is empty")
            }
            else {
                var inputValue = input.value.replace(/[|+]/g, '');;
                
                const encrypted_mess=await this.deck.settle_deck(inputValue)
                console.log(encrypted_mess)
                this.showBox("This deck is not available")
                
                const response = await fetch('/send_deck', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ "data": encrypted_mess }) // 将数据转换为JSON字符串
                    
                }).catch(error => console.error('Error fetching data:', error));
                const responseData =await response.json()

                if (responseData["state"]=="successful"){
                    window.location.href = '/';
                }
                else{
                    this.showBox("This deck is not available")
                }
                
                
               
            }
        });

        document.getElementById('deck_name').addEventListener('input', ()=>{
            const input = document.getElementById('deck_name');
            if (input.value.trim() !== '') {
                input.classList.remove('breath'); // 如果有内容输入，移除闪烁效果
            }
        });
        
    }

    update(){
        if (this.turing_flag){
            this.update_turing()
        }
        this.find_points_from_a(this.function_page_position(this.position_x))
        this.update_cards(this.back_page_cards)
        this.update_cards(this.front_page_cards)
        if (!this.target_card && !this.clicked_flag){
            this.update_cards_on_page(this.back_page_cards)
            this.update_cards_on_page(this.front_page_cards)
        }
        
    }
    draw(){
        
        this.clear_rect();
        this.save_page()
        this.ctx.strokeStyle = 'white';
        //this.front_page_ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)

        if (this.turing_flag || this.position_x<0){
            this.process_book_page_clip(this.front_page_ctx)
        }
        this.back_page_ctx.drawImage(this.page, -100, 40 ,this.canvas.width*0.7, this.canvas.height*0.75);
        this.front_page_ctx.drawImage(this.page, -100, 40 ,this.canvas.width*0.7, this.canvas.height*0.75);

        this.draw_cards_on_page(this.front_page_cards,this.front_page_ctx)
        this.draw_cards_on_page(this.back_page_cards,this.back_page_ctx)

        this.ctx.drawImage(this.background_canvas, -100, 40 ,this.canvas.width*0.8, this.canvas.height*0.8);
        this.draw_all_book_mark()
        
        this.ctx.drawImage(this.back_page, 0, 0 ,this.canvas.width, this.canvas.height);
        
        this.ctx.drawImage(this.front_page, 0, 0 ,this.canvas.width, this.canvas.height);

        if (!this.target_card && !this.clicked_flag){
            this.draw_arrow()
        }
        else{
            this.target_card.draw(this.camera,this.ctx,this.canvas)
            
        }
        this.fill_back_paper(this.ctx)
        
        if (this.clicked_flag){
            const blur_canvas=this.draw_blur_frame()
            this.ctx.drawImage(blur_canvas, 0, 0 );
        }
        
        
        
        //this.draw_points()
        this.restore_page();
        
        
    }
    draw_blur_frame(){
        const copied_canvas=document.createElement('canvas');
        copied_canvas.width=this.canvas.width;
        copied_canvas.height=this.canvas.height;
        const ctx=copied_canvas.getContext("2d");
        ctx.filter = 'blur(8px)';
        ctx.drawImage(this.canvas,0,0)
        ctx.clearRect(...this.target_card.position_in_screen[3],
            this.target_card.position_in_screen[1][0]-this.target_card.position_in_screen[3][0],
            this.target_card.position_in_screen[1][1]-this.target_card.position_in_screen[3][1]
            
            )
        return copied_canvas
    }
    clear_rect(){
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.front_page_ctx.clearRect(0, 0, this.front_page.width, this.front_page.height);
        
        this.back_page_ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.hide_page_ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
    initinal_a_canvas(){
        var canvas_2 = document.createElement('canvas');
        canvas_2.width = 1470;
        canvas_2.height = 742;
        return canvas_2
    }
    
    initinal_book_background(){
        
        var img = new Image();
        
        img.src = 'webpages/deckpage/book.PNG'; // 替换为你的图片路径
        var canvas_2 = document.createElement('canvas');
        canvas_2.width = 1470;
        canvas_2.height = 742;
        var ctx_2 = canvas_2.getContext("2d");
        img.onload = function() {
            ctx_2.drawImage(img, 0, 0, canvas_2.width, canvas_2.height);
        }
        
        return canvas_2;
    }
    initinal_page(){
        var img = new Image();
        
        img.src = 'webpages/deckpage/page.PNG'; // 替换为你的图片路径
        var canvas_2 = document.createElement('canvas');
        canvas_2.width = 1470;
        canvas_2.height = 742;
        var ctx_2 = canvas_2.getContext("2d");
        img.onload = function() {
            ctx_2.drawImage(img, 0, 0, canvas_2.width, canvas_2.height);
        }
        
        return canvas_2;
    }
    save_page(){
        this.front_page_ctx.save();
        this.back_page_ctx.save();
        this.hide_page_ctx.save();
        this.ctx.save();
    }
    restore_page(){
        this.front_page_ctx.restore();
        this.back_page_ctx.restore();
        this.hide_page_ctx.restore();
        this.ctx.restore();

    }
    find_points_from_a(a){
        this.point_A=a;
        this.point_B=[
            (a[0]+this.point_O[0])/2,
            (a[1]+this.point_O[1])/2,
        ]
        const gradient_ao=(this.point_O[1]-a[1])/(this.point_O[0]-a[0]);
        const gradient_cd=-1/gradient_ao
        const b=(this.point_B[1]-gradient_cd*this.point_B[0])
        this.point_D=[
            this.point_O[0],
            this.point_O[0]*gradient_cd+b//y=kx+b
        ]
        this.draw_line(gradient_cd,b)

        this.point_C=[
            (this.point_O[1]-(this.point_B[1]-gradient_cd*this.point_B[0]))/gradient_cd,
            this.point_O[1]
        ]

        this.point_J=[
            (a[0]+this.point_D[0])/2,
            (a[1]+this.point_D[1])/2,
        ]

        this.point_I=[
            (a[0]+this.point_C[0])/2,
            (a[1]+this.point_C[1])/2,
        ]

        const gradient_IJ=(this.point_J[1]-this.point_I[1])/(this.point_J[0]-this.point_I[0]);

        this.point_E=[
            (this.point_O[1]-(this.point_J[1]-gradient_IJ*this.point_J[0]))/gradient_IJ,
            this.point_O[1]
        ]
        this.point_F=[
            this.point_O[0],
            this.point_O[0]*gradient_IJ+(this.point_J[1]-gradient_IJ*this.point_J[0])//y=kx+b
        ]

        this.point_H=[
            (this.point_F[0]+this.point_D[0])/2,
            (this.point_F[1]+this.point_D[1])/2,
        ]
        this.point_G=[
            (this.point_C[0]+this.point_E[0])/2,
            (this.point_C[1]+this.point_E[1])/2,
        ]

        this.point_L=[
            (this.point_D[0]+this.point_J[0])/2,
            (this.point_D[1]+this.point_J[1])/2,
        ]
        this.point_K=[
            (this.point_C[0]+this.point_I[0])/2,
            (this.point_C[1]+this.point_I[1])/2,
        ]

        this.point_M=[
            (this.point_K[0]+this.point_G[0])/2,
            (this.point_K[1]+this.point_G[1])/2,
        ]
        this.point_N=[
            (this.point_H[0]+this.point_L[0])/2,
            (this.point_H[1]+this.point_L[1])/2,
        ]
    }
    draw_points(){
        this.ctx.font = "30px Arial";
        const points=[this.point_B,this.point_C,this.point_D,this.point_E,this.point_F,this.point_G,this.point_H,this.point_I,this.point_J,this.point_O,this.point_L,this.point_K,this.point_M,this.point_N];
        const text=['b','c','d','e','f','g','h','i','j','o','l','k','m','n']
        for (let i in points){
            this.ctx.beginPath(); // 开始路径
            this.ctx.arc(...points[i], 5, 0, 2 * Math.PI); // 画一个中心在(95,50)半径为5的圆来表示点
            this.ctx.fill(); // 填充颜色
            this.ctx.fillText(text[i], ...points[i]);
        }
        this.ctx.beginPath(); // 开始路径
        this.ctx.arc(550,400, 5, 0, 2 * Math.PI); // 画一个中心在(95,50)半径为5的圆来表示点
        this.ctx.fill(); // 填充颜色
        
    }
    draw_line(k,b){
        var x0 = 0;
        var y0 = k * x0 + b;
        var x1 = this.canvas.width;
        var y1 = k * x1 + b;

        // 画线
        this.ctx.beginPath();
        this.ctx.moveTo(x0, y0);
        this.ctx.lineTo(x1, y1);
        this.ctx.stroke();
    }

    process_book_page_clip(ctx){
        ctx.beginPath();
        
        ctx.moveTo(...this.point_A);
        ctx.lineTo(...this.point_I);
        ctx.quadraticCurveTo(...this.point_K, ...this.point_M);
        ctx.quadraticCurveTo(...this.point_G, ...this.point_E);
        ctx.lineTo(0,this.point_O[1]);
        ctx.lineTo(0,0);
        ctx.lineTo(this.point_O[0],0);
        ctx.lineTo(...this.point_F);

        ctx.quadraticCurveTo(...this.point_H, ...this.point_N);
        ctx.quadraticCurveTo(...this.point_L, ...this.point_J);
        ctx.clip();



    }

    fill_back_paper(ctx){
        ctx.beginPath();
        ctx.moveTo(...this.point_A);
        ctx.lineTo(...this.point_I);
        ctx.quadraticCurveTo(...this.point_K, ...this.point_M);
        ctx.lineTo(...this.point_N);
        ctx.quadraticCurveTo(...this.point_L, ...this.point_J);
        ctx.fillStyle = 'rgba(180, 170, 160, 1)';
        ctx.fill()
    }
    start_page_turing(unit){
        const acc_unit=unit;
        const position_x_unit=-unit;
        this.turing_flag=true;
        this.acceleration=acc_unit*4;
        this.velocity=0;
        this.position_x=position_x_unit*this.point_O[0];

    }
    update_turing(){
        this.velocity=this.velocity+this.acceleration;
        this.position_x=this.position_x+this.velocity
        if (this.position_x<-this.point_O[0]){
            this.position_x=-this.point_O[0];
            this.turing_flag=false;
        }
        else if (this.position_x>this.point_O[0]){
            this.position_x=this.point_O[0];
            this.turing_flag=false;
        }
    }
    function_page_position(x){
        const y =-100*math.log(-(x-this.point_O[0])/100+1)+this.point_O[1];
        return [x,y]
    }

    update_cards_on_page(cards){
        for (let i in cards){
            const card_col=math.floor(i/4);
            const card_row=i%4;
            cards[i].position[0]=-64+19*card_row
            cards[i].position[1]=-18+27*card_col
            cards[i].angle_y=0
            cards[i].size=2.2
            cards[i].angle_x=0
        }
    }

    draw_cards_on_page(cards,page_ctx){//cards[],this.page_front_back

        for (let i in cards){
            const card_col=math.floor(i/4);
            const card_row=i%4;
            this.draw_card_quantity(card_row,card_col,page_ctx,cards[i].quantity)
            cards[i].draw(this.camera,page_ctx,this.canvas)
        }
    }
    draw_card_quantity(card_row,card_col,ctx,quantity){
        const x=(card_row*190)+60;
        const y=card_col*270+50;
        const length=70;
        const color="rgb(31,31,31,1)"
        this.drawRoundedRect_quantity_show(ctx,x,y,length,20,10,color)
        ctx.font = '15px Georgia';
        ctx.fillStyle = "rgb(231,231,231,1)";
        const metrics = ctx.measureText(quantity);
        
        ctx.fillText(quantity, x+(length-metrics.width)/2, y+15);
        
    }
    draw_all_book_mark(){
        
        
        for (let typ in this.dict_list_type_book_mark){
            this.draw_book_mark(this.ctx,...this.dict_list_type_book_mark[typ].get_para())
        }
        
        for (let col in this.dict_list_color_book_mark){
            this.draw_book_mark(this.ctx,...this.dict_list_color_book_mark[col].get_para())
        }
        
    }
    update_cards(cards){
        for(let i in cards){
            
            cards[i].update()
        }
    }

    draw_book_mark(ctx, color,x,y,length,text,color_text){
        this.drawRoundedRect(ctx,x,y,length,40,10,color)
        ctx.font = '25px Georgia';
        ctx.fillStyle = color_text;
        const metrics = ctx.measureText(text);
        
        ctx.fillText(text, x+(length-metrics.width)/2, y+(25));
    }
    drawRoundedRect(ctx, x, y, width, height, borderRadius,color) {
        ctx.beginPath();
        ctx.moveTo(x + borderRadius, y);
        ctx.lineTo(x + width - borderRadius, y);
        ctx.quadraticCurveTo(x + width, y, x + width, y + borderRadius);
        ctx.lineTo(x + width, y + height - borderRadius);
        ctx.quadraticCurveTo(x + width, y + height, x + width - borderRadius, y + height);
        ctx.lineTo(x , y + height);
        //ctx.quadraticCurveTo(x, y + height, x, y + height - borderRadius);
        ctx.lineTo(x, y);
        //ctx.quadraticCurveTo(x, y, x + borderRadius, y);
        ctx.closePath();
    
        // 设置样式
        ctx.fillStyle = color; // 填充颜色
        ctx.fill();
        ctx.strokeStyle = color; // 边框颜色
        
        ctx.stroke();
    }
    drawRoundedRect_quantity_show(ctx, x, y, width, height, borderRadius,color) {
        ctx.beginPath();
        ctx.moveTo(x, y+borderRadius);
        ctx.quadraticCurveTo(x , y, x + borderRadius, y );
        ctx.lineTo(x + width - borderRadius, y);
        ctx.quadraticCurveTo(x + width, y, x + width, y + borderRadius);
        ctx.lineTo(x + width, y + height);
        ctx.lineTo(x , y + height);
        //ctx.quadraticCurveTo(x, y + height, x, y + height - borderRadius);
        ctx.lineTo(x, y+borderRadius);
        //ctx.quadraticCurveTo(x, y, x + borderRadius, y);
        ctx.closePath();
    
        // 设置样式
        ctx.fillStyle = color; // 填充颜色
        ctx.fill();
        ctx.strokeStyle = color; // 边框颜色
        
        ctx.stroke();
    }

    set_book_mark_dict(){
        this.dict_list_type_book_mark=[]
        this.dict_list_color_book_mark=[]
        const color_ini=["rgb(216,173,172,1)","rgb(186,197,183,1)","rgb(189,214,233,1)","rgb(233,227,198,1)","rgb(183,183,182,1)"]
        const color_clicked=["rgb(216,113,112,1)","rgb(136,197,133,1)","rgb(139,214,233,1)","rgb(233,227,138,1)","rgb(133,133,132,1)"]
        const type_name=["Creature","Instant","Land","Sorcery"]
        const color_name=["Red","Green","Blue","White","Black"]
        const over_all_pos_color=[873,90]
        const over_all_pos_type=[1000,140]

        for(let col in color_ini){
            this.dict_list_color_book_mark.push(new Book_Mark(
                color_ini[col],
                color_clicked[col],
                over_all_pos_color[0],
                over_all_pos_color[1]+100*col,
                150,
                40,
                color_name[col],
                "rgb(31,31,31,1)"
                ))
        }

        for (let typ in type_name){
            this.dict_list_type_book_mark.push(new Book_Mark(
                "rgb(31,31,31,1)",
                "rgb(81,81,81,1)",
                over_all_pos_type[0],
                over_all_pos_type[1]+100*typ,
                150,
                40,
                type_name[typ],
                "rgb(233,233,233,1)"
                ))
        }

    }

    async check_buttons(mouse_pos){
        for (let typ in this.dict_list_type_book_mark){
            if (this.dict_list_type_book_mark[typ].check_mouse(mouse_pos)){
                for (let i in this.dict_list_type_book_mark){
                    this.dict_list_type_book_mark[i].return_to_ini()
                }
                this.dict_list_type_book_mark[typ].clicked()
                this.current_type_mark=this.current_type_dict[this.dict_list_type_book_mark[typ].text]
                this.page_number=1;
                await this.change_type(this.page_number,this.current_type_mark,this.current_color_mark)
                //console.log(await this.get_page(this.page_number,this.current_type_mark,this.current_color_mark))
                
            }
        }
        
        for (let col in this.dict_list_color_book_mark){
            if (this.dict_list_color_book_mark[col].check_mouse(mouse_pos)){
                for (let i in this.dict_list_color_book_mark){
                    this.dict_list_color_book_mark[i].return_to_ini()
                }
                this.dict_list_color_book_mark[col].clicked()
                this.current_color_mark=this.current_color_dict[this.dict_list_color_book_mark[col].text]
                this.page_number=1;
                await this.change_type(this.page_number,this.current_type_mark,this.current_color_mark)
                //console.log(await this.get_page(this.page_number,this.current_type_mark,this.current_color_mark))
                
            }
        }
        for (let arraw in this.arrows_list){
            if (this.arrows_list[arraw].check_mouse(mouse_pos)){
                this.page_number=this.arrows_list[arraw].change_page(this.page_number)
                this.change_page(this.page_number,this.current_type_mark,this.current_color_mark,-this.arrows_list[arraw].unit_direction)
            }
        }
        
    }
    get_mouse_pos(event,canvas){
        var rect = canvas.getBoundingClientRect();
        // 计算鼠标相对于canvas的位置
        var mouseX = (event.clientX - rect.left)*canvas.width/rect.width;
        var mouseY = (event.clientY - rect.top)*canvas.height/rect.height;
        return [mouseX,mouseY]
    }

    async send_page_request(offset,current_type_mark,current_color_mark){
        
        const data = { 
            offset: offset, 
            type_card: current_type_mark,
            color_card:current_color_mark};
        console.log(data)
        const response = await fetch('/deck_page', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
            
        });
        const responseData =await response.json()
        
        

        const cards=this.process_response_cards(JSON.parse(responseData))
        
        return cards
    }

    get_offset(page_number){
        return (page_number-1)*8
    }

    process_response_cards(data){
        const cards=[]
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
                card=new Instant(4,5.62,[-35,0,40],2.2,image,data[card_i]['Cost'],data[card_i]["Name"])
            }
            else if(data[card_i]["Type_card"]=="land"){
                card=new Land(4,5.62,[-35,0,40],2.2,image,data[card_i]["Name"])
            }
            else if(data[card_i]["Type_card"]=="sorcery"){
                card=new Sorcery(4,5.62,[-35,0,40],2.2,image,data[card_i]['Cost'],data[card_i]["Name"])
            }
            else{
                card=new Creature(4,5.62,[-35,0,40],2.2,image,data[card_i]['Cost'],data[card_i]["Toughness"],data[card_i]["Power"],data[card_i]["Name"])
            }
            card.quantity=data[card_i]["quantity"]
            cards.push(card)
            
            
        }
        return cards
    }

    async get_page(page_number,current_type_mark,current_color_mark){
        
        if (this.page_dict[current_type_mark][current_color_mark][page_number]){
            return this.page_dict[current_type_mark][current_color_mark][page_number];
        }
        else{
            const cards=await this.send_page_request(this.get_offset(page_number),current_type_mark,current_color_mark)
            this.page_dict[current_type_mark][current_color_mark][page_number]=new Page(page_number,current_type_mark,current_color_mark,cards);
            return this.page_dict[current_type_mark][current_color_mark][page_number];
        }
    }
    async change_type(target_page,type_mark,color_mark){
        const turing_made=-1
        if (this.position_x<0){
            this.front_page_cards=this.back_page_cards;
            const page_1=await this.get_page(target_page,type_mark,color_mark);
            this.back_page_cards=page_1.cards;
            this.start_page_turing(turing_made);
        }
        else{
            const page_1=await this.get_page(target_page,type_mark,color_mark);
            this.back_page_cards=page_1.cards;
            this.start_page_turing(turing_made);
        }
    }
    async change_page(target_page,type_mark,color_mark,turing_made){
        if (turing_made==1){//翻回来
            if (this.position_x>0){
                const page_1=await this.get_page(target_page,type_mark,color_mark);
                
                if (page_1.check_this()){
                    this.front_page_cards=page_1.cards;
                    this.back_page_cards=front_page_cards;
                    this.start_page_turing(turing_made);

                }
            }
            else{
                const page_1=await this.get_page(target_page,type_mark,color_mark);
                if (page_1.check_this()){
                    this.front_page_cards=page_1.cards;
                    this.start_page_turing(turing_made);
                }
                
            }
        }
        else{//翻一页
           
            if (this.position_x<0){
                const page_1=await this.get_page(target_page,type_mark,color_mark);
                
                if (page_1.check_this()){
                    this.front_page_cards=this.back_page_cards;
                    this.back_page_cards=page_1.cards;
                    this.start_page_turing(turing_made);

                }

                
                
            }
            else{
                const page_1=await this.get_page(target_page,type_mark,color_mark);
                if (page_1.check_this()){
                    this.back_page_cards=page_1.cards;
                    this.start_page_turing(turing_made);
                }
                
            }
        }
    }

    draw_arrow(){
        for (let i in this.arrows_list){
            this.arrows_list[i].draw(this.ctx)
        }
    }

    get_current_cards_we_see(){
        if (this.position_x>0){
            
            return this.front_page_cards;
        }
        else{
            return this.back_page_cards;
        }
    }

    find_cards_by_mouse(mouse_pos){
        const cards=this.get_current_cards_we_see()
        for (let i in cards){
            
            if (cards[i].check_inside(mouse_pos,...cards[i].position_in_screen)){
                return cards[i]
            }
        }
        return NaN
    }
}



class Book_Mark extends Button{

    constructor(ini_color,click_color,x,y,length,height,text,text_color){
        super(x,y,height,length)
        this.initinal_color=ini_color;
        this.click_color=click_color;
        this.current_color=ini_color;
        this.text=text;
        this.text_color=text_color
    }

    clicked(){
        
        this.current_color=this.click_color
    }
    return_to_ini(){
        this.current_color=this.initinal_color
    }
    get_para(){
        return [this.current_color,this.x,this.y,this.length,this.text,this.text_color]
    }
    
}

class Arrow extends Button{
    constructor(ini_color,x,y,length,height,unit_direction){
        super(x,y,height,length)
        this.initinal_color=ini_color;
        
        this.unit_direction=unit_direction
        
        
        
        
    }
    change_page(current_page){
        console.log(current_page,this.unit_direction,current_page+this.unit_direction)
        if (current_page+this.unit_direction>=1){
            
            return current_page+this.unit_direction
        }
        else{
            return current_page
        }
        
    }
    draw(context){
        const width=7;
        var headlen = 10; // 箭头头部的长度
        if (this.unit_direction==1){//right
            var tox=this.x+this.length
            var toy=this.y
            var fromx=this.x
            var fromy=this.y
        }
        else{
            var tox=this.x
            var toy=this.y
            var fromx=this.x+this.length
            var fromy=this.y
        }
        
        var dx = tox - fromx;
        var dy = toy - fromy;
        var angle = math.atan2(dy, dx);
        context.strokeStyle = this.initinal_color;
        
        context.lineWidth = width
        context.beginPath();
        
        context.moveTo(fromx, fromy);
        context.lineTo(tox, toy);
        
        context.lineTo(tox - headlen * math.cos(angle - Math.PI / 6), toy - headlen );
        //context.moveTo(fromx, fromy+width);
        
        context.moveTo(fromx, fromy+width);
        
        context.lineTo(tox, toy+width);
        
        context.lineTo(tox - headlen * math.cos(angle + Math.PI / 6), toy + headlen+width );
        context.stroke();
    }

}

class Page{

    constructor(number,type,color,cards){
        this.page_number=number;
        this.type=type;
        this.color=color;
        this.cards=cards;
    }
    check_next(){
        if (this.cards.length==8){
            return true
        }
        else{
            return false
        }
    }
    check_last(){
        if (this.page_number==1){
            return false
        }
        else{
            return true
        }
    }
    check_this(){
        if (this.cards.length>0){
            return true
        }
        else{
            return false
        }
    }

}

