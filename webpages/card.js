function loadImage(src) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.src = src;
    });
}
function loadImage_normal(src) {
    const img = new Image();
    img.src = src;
    return img;
    
}

class Card{

    constructor(width,height,position,size,dynamic_canvas,color_fee,name){
        this.name=name
        this.corners=[//x y z
            [1*width,-1*height,0],
            [1*width,1*height,0],
            [-1*width,1*height,0],
            [-1*width,-1*height,0],

        ];
        this.position=position;
        this.angle_x=0;
        this.angle_y=0;
        this.angle_z=0;
        this.vel_x=0;
        this.vel_y=0;
        this.vel_z=0;
        this.arr_poses=NaN;
        this.size=size
        this.points=this.get_org_position(this.size);
        
        //Mana
        this.color_fee=color_fee
        this.dynamic_canvas=dynamic_canvas;
        this.back_img=new Image();
        this.back_img.src="webpages/image_source/card/back.png";
        this.image= this.dynamic_canvas[2]
        this.orginal_image=this.dynamic_canvas[3]
        this.color_fee_paths={
            "blue":"webpages/image_source/color_fee/blue.PNG",
            "red":"webpages/image_source/color_fee/red.PNG",
            "black":"webpages/image_source/color_fee/black.PNG",
            "gold":"webpages/image_source/color_fee/gold.PNG",
            "green":"webpages/image_source/color_fee/green.PNG",
            "colorless":"webpages/image_source/color_fee/colorless.PNG"
        }
        this.images_fee=[
            loadImage_normal(this.color_fee_paths["colorless"]),
            loadImage_normal(this.color_fee_paths["red"]),
            loadImage_normal(this.color_fee_paths["blue"]),
            loadImage_normal(this.color_fee_paths["green"]),
            loadImage_normal(this.color_fee_paths["gold"]),
            loadImage_normal(this.color_fee_paths["black"])
        ]

        this.final_image=this.dynamic_canvas[0]
        
        //this.image.src="webpages/image_source/card/red.PNG";

        this.draw_card_flag=false;
        this.move_enlarge_card_flag=false
        this.position_in_screen=[[0,0],[0,0],[0,0],[0,0]]
        
    }
    initinal_dynamic_space(){
        const canvas=document.createElement('canvas');
        canvas.width=this.image.width;
        canvas.height=this.image.height;
        
        return [canvas,canvas.getContext('2d')]
    }
    
    get_org_position(size){
        const arr_x=[];
        const arr_y=[];
        const arr_z=[];

        for (const i in this.corners){
            
            arr_x.push(this.corners[i][0]*size);
            arr_y.push(this.corners[i][1]*size);
            arr_z.push(this.corners[i][2]*size);
        }

        return math.matrix([arr_x,arr_y,arr_z,])
    }

    get_position_points(){
        const xy_rotate=math.multiply(rotateX(this.angle_x),rotateY(this.angle_y));
        const xyz_rotate=math.multiply(xy_rotate,rotateZ(this.angle_z));
        
        const pos_rotate=math.multiply(xyz_rotate,this.get_org_position(this.size));
        
        const final_points=[]
        for (let col = 0; col <= this.corners.length-1; col++){
            const final_point=[]
            for (let row = 0; row <= 2; row++){
                
                final_point.push(pos_rotate.get([row,col])+this.position[row]);
            }
            final_points.push(final_point);
            
        }
        return final_points;

    }
    check_surface(camera){//true: forward false: backward
        const vectorA=this.normal_vector()
        const vectorB=camera.get_vector()
        const dot = math.dot(vectorA, vectorB);
        

        // Calculate the magnitude (norm) of each vector
        const normA = math.norm(vectorA);
        const normB = math.norm(vectorB);

        // Calculate the cosine of the angle using the dot product and magnitudes
        const cosTheta = dot / (normA * normB);
        //console.log(cosTheta);
        return cosTheta<0
        // Use the acos function to find the angle in radians and then convert to degrees
        const angleRadians = math.acos(cosTheta);
        
        const angleDegrees = angleRadians * (180 / math.PI);

        return angleDegrees;
    }

    normal_vector(){
        const vec1=[this.arr_poses[1][0]-this.arr_poses[3][0],this.arr_poses[1][1]-this.arr_poses[3][1],this.arr_poses[1][2]-this.arr_poses[3][2]];
        const vec2=[this.arr_poses[0][0]-this.arr_poses[2][0],this.arr_poses[0][1]-this.arr_poses[2][1],this.arr_poses[0][2]-this.arr_poses[2][2]];
        const vec_normal=(math.cross(vec1,vec2));
        return vec_normal;
    }

    mid_point(){
        const mid_p=[(this.arr_poses[1][0]+this.arr_poses[3][0])/2,(this.arr_poses[1][1]+this.arr_poses[3][1])/2,(this.arr_poses[1][2]+this.arr_poses[3][2])/2];
        return mid_p;
    }


    update(){
        this.dynamic_canvas[1].clearRect(0, 0, this.dynamic_canvas[0].width, this.dynamic_canvas[0].height);
        this.dynamic_canvas[1].drawImage(this.dynamic_canvas[2],0,0,this.dynamic_canvas[2].width,this.dynamic_canvas[2].height);
        
        this.create_fee(this.dynamic_canvas[1],this.color_fee,...Array.from({length: 6}, (_, i) => this.images_fee[i]));
        
        this.arr_poses=this.get_position_points();

        if (this.draw_card_flag){
            this.draw_card_animation()
        }
        if (this.move_enlarge_card_flag){
            this.card_move_enlarge_animation()
        }
        
        
    }



    draw_half_img_1(points_pos,new_points_pos,ctx){
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.save();
        ctx.beginPath();
        const p1=this.extendVert(points_pos[0][0], points_pos[0][1],points_pos[2][0], points_pos[2][1],points_pos[3][0], points_pos[3][1])
        const p2=this.extendVert(points_pos[2][0], points_pos[2][1],points_pos[0][0], points_pos[0][1],points_pos[3][0], points_pos[3][1])
        const p3=this.extendVert(points_pos[3][0], points_pos[3][1],points_pos[2][0], points_pos[2][1],points_pos[0][0], points_pos[0][1])

        
        ctx.moveTo(...p1); // 右下角
        ctx.lineTo(...p2); // 左下角
        ctx.lineTo(...p3); // 左上角
        // ctx.moveTo(points_pos[0][0], points_pos[0][1]); // 右下角
        // ctx.lineTo(points_pos[3][0], points_pos[3][1]); // 右上角
        // ctx.lineTo(points_pos[2][0], points_pos[2][1]); // 左上角
        // ctx.lineTo(points_pos[1][0], points_pos[1][1]);
        ctx.closePath();
        ctx.clip();
        ctx.setTransform(
            (points_pos[0][0] - points_pos[3][0]) / this.final_image.width,
            (points_pos[0][1] - points_pos[3][1]) / this.final_image.width,
            (points_pos[3][0] - points_pos[2][0]) / (this.final_image.height),
            (points_pos[3][1] - points_pos[2][1]) / (this.final_image.height),
            points_pos[2][0],
            points_pos[2][1]
        );
        ctx.drawImage(this.final_image,new_points_pos[0], new_points_pos[1], this.final_image.width/4, this.final_image.height/4, 0,0, this.final_image.width, this.final_image.height);
        //ctx.drawImage(this.image, 0, 0, this.image.width, this.image.height/4);
        ctx.restore();
    }
    draw_half_img_2(points_pos,new_points_pos,ctx){
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.save();
        ctx.beginPath();
        // ctx.moveTo(points_pos[2][0], points_pos[2][1]); // 左上角
        // ctx.lineTo(points_pos[1][0], points_pos[1][1]); // 右上角
        // ctx.lineTo(points_pos[0][0], points_pos[0][1]); // 右下角
        const p1=this.extendVert(points_pos[0][0], points_pos[0][1],points_pos[1][0], points_pos[1][1],points_pos[2][0], points_pos[2][1])
        const p2=this.extendVert(points_pos[1][0], points_pos[1][1],points_pos[0][0], points_pos[0][1],points_pos[2][0], points_pos[2][1])
        const p3=this.extendVert(points_pos[2][0], points_pos[2][1],points_pos[1][0], points_pos[1][1],points_pos[0][0], points_pos[0][1])
        ctx.moveTo(...p1); // 右下角
        ctx.lineTo(...p2); // 左下角
        ctx.lineTo(...p3); // 左上角
        
        ctx.closePath();
        ctx.clip();
        ctx.setTransform(
            (points_pos[1][0] - points_pos[2][0]) / this.final_image.width,
            (points_pos[1][1] - points_pos[2][1]) / this.final_image.width,
            (points_pos[0][0] - points_pos[1][0]) / this.final_image.height,
            (points_pos[0][1] - points_pos[1][1]) / this.final_image.height,
            points_pos[2][0],
            points_pos[2][1]
        );
        ctx.drawImage(this.final_image,new_points_pos[0], new_points_pos[1], this.final_image.width/4, this.final_image.height/4, 0,0, this.final_image.width, this.final_image.height);
        //ctx.drawImage(this.image, 0, 0, this.image.width, this.image.height);
        ctx.restore();
    }
    draw(camera,ctx,canvas){
        
        const new_points_pos=[];
        
        if (this.check_surface(camera)){
            this.final_image=this.dynamic_canvas[0];
        }
        else{
            this.final_image=this.back_img;
        }
        //ctx.beginPath();
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;       
        for (let index_plane=0; index_plane<4;index_plane++){
            const x_start=this.arr_poses[index_plane][0]
            const y_start=this.arr_poses[index_plane][1]
            const z_start=this.arr_poses[index_plane][2]

            const end_x=cx + camera.similar_tri(x_start,z_start)
            const end_y=cy + camera.similar_tri(y_start,z_start)
            new_points_pos.push([end_x, end_y])
        }
        //ctx.closePath();
        const COL=4;
        const ROW=4;

        let col_left_up=this.average_p(new_points_pos[2],new_points_pos[3],COL-0,COL);
        let col_right_up=this.average_p(new_points_pos[1],new_points_pos[0],COL-0,COL);
        
        for (let col=0;col<COL;col++){
            let col_left_down=this.average_p(new_points_pos[2],new_points_pos[3],COL-col-1,COL);
            let col_right_down=this.average_p(new_points_pos[1],new_points_pos[0],COL-col-1,COL);

            
            
            for (let row=0;row<ROW;row++){
                const new_points_pos_1=[
                    this.average_p(col_left_down,col_right_down,ROW-row-1,ROW),
                    this.average_p(col_left_up,col_right_up,ROW-row-1,ROW),
                    this.average_p(col_left_up,col_right_up,ROW-row,ROW), 
                    this.average_p(col_left_down,col_right_down,ROW-row,ROW), 
                ]
                this.draw_half_img_1(new_points_pos_1,[row*this.image.width/ROW,col*this.image.height/COL],ctx);
                this.draw_half_img_2(new_points_pos_1,[row*this.image.width/ROW,col*this.image.height/COL],ctx);
            }
            col_left_up=col_left_down;
            col_right_up=col_right_down;
        }
        this.position_in_screen=new_points_pos;
    }
    average_p(p_1,p_2,n,t){
        const x=p_2[0]+n*(p_1[0]-p_2[0])/t
        const y=p_2[1]+n*(p_1[1]-p_2[1])/t
        return [x,y]
    }
    
    create_fee(ctx,fee_text,color_less,red,blue,green,gold,black){//3UU
        
        const splited=fee_text.match(/\d+|\D/g);
        
        const color_selector={//B/U/G/R/W
            "U":blue,
            "R":red,
            "B":black,
            "W":gold,
            "G":green,
        }
        for (let i in splited.reverse()){
            ctx.save();
            if (/^[+-]?\d+$/.test(splited[i])){//check whether it is number
                
                ctx.setTransform(
                    (25) / color_less.width,
                    0,
                    0,
                    -(25) / color_less.height,
                    color_less.width*(20-1.5*i)/24,
                    color_less.height*3.95/3
                );
                
                ctx.drawImage(color_less,0,0,color_less.width,color_less.height);
                
                ctx.setTransform(1, 0, 0, -1, 
                    2,
                    1038);
                ctx.font = '20px Georgia';
                ctx.fillStyle = 'black';
                
                ctx.fillText(splited[i], color_less.width*(20-1.5*i)/24,color_less.height*3.95/3);
                
            }
            else{
                
                ctx.setTransform(
                    (25) / color_selector[splited[i]].width,
                    0,
                    0,
                    -(25) / color_selector[splited[i]].height,
                    color_selector[splited[i]].width*(20-1.5*i)/24,
                    color_selector[splited[i]].height*3.95/3
                );
                
                ctx.drawImage(color_selector[splited[i]],0,0,color_selector[splited[i]].width,color_selector[splited[i]].height);
                
    
            }
            ctx.restore();
        }
        
    }
    draw_card(){
        this.draw_card_flag=true;
        
        this.ini_angle_y=math.pi;
        this.ini_position=18
        this.ini_size=2;

        this.size=this.ini_size;
        this.angle_y=this.ini_angle_y;
        this.position=[-17.5,this.ini_position,40]



        this.largest_size=3.5;
        this.end_angle_y=math.pi*2;
        this.end_position=-18
        this.draw_time_duration_end=0.3 ;
        this.draw_time_duration=0;
    }
    draw_card_animation(){
        this.draw_time_duration=this.draw_time_duration+0.01;
        const rate=this.draw_time_duration/this.draw_time_duration_end;
        
        this.angle_y=this.ini_angle_y+(this.end_angle_y-this.ini_angle_y)*rate;
        this.position[1]=this.ini_position+(this.end_position-this.ini_position)*rate;
        this.size=this.ini_size+(this.largest_size-this.ini_size)*rate;

        if (this.draw_time_duration>=this.draw_time_duration_end){
            this.draw_card_flag=false;
        }
    }
    start_move_enlarge(largest_size,move_time_duration_end,target_position){
        
        
        this.ini_position=[...this.position];
        
        this.target_position=target_position
        this.largest_size=largest_size
        this.angle_x=0
        this.angle_y=0
        this.move_time_duration_end=move_time_duration_end;
        this.move_time_duration=0;
        this.move_enlarge_card_flag=true;
        this.ini_size=this.size
        
        
    }
    card_move_enlarge_animation(){
        
        this.move_time_duration=this.move_time_duration+0.01;
        const rate=this.move_time_duration/this.move_time_duration_end;
        this.size=this.ini_size+(this.largest_size-this.ini_size)*rate;
        for(let i=0;i<3;i++){
            
            this.position[i]=this.ini_position[i]+(this.target_position[i]-this.ini_position[i])*rate;
            
        }
        
        if (this.move_time_duration>=this.move_time_duration_end){
            this.move_enlarge_card_flag=false;
            this.position=this.target_position;
        }
        
    }
    moving_by_mouse(mouse_pos,camera){
        
        const limit=0.9;
        const next_pos=camera.similar_tri_reverse(...mouse_pos,this.position[2]);
        const x_diff=-(next_pos[0]-this.position[0])/3;
        const y_diff=(next_pos[1]-this.position[1])/3;
        

        this.angle_y = x_diff > limit ? limit : (x_diff < -limit ? -limit :x_diff);
        this.angle_x = y_diff > limit ? limit : (y_diff < -limit ? -limit :y_diff);

        this.position[0]=next_pos[0]
        this.position[1]=next_pos[1]
        console.log(1)
    }
    check_inside(mouse_pos,position1,position2,position3,position4){//n shape of points
        
        return (
            this.create_function_x(mouse_pos,position1,position2)<0 &&
            this.create_function_y(mouse_pos,position3,position2)<0 &&
            this.create_function_x(mouse_pos,position3,position4)>0 &&
            this.create_function_y(mouse_pos,position4,position1)>0
        )

    }
    create_function_x(mouse_pos,position1,position2){// for x=... position1(lower x) x-...
        const k=(position2[0]-position1[0])/(position2[1]-position1[1]);
        const b=position1[0]-k*position1[1];
        return mouse_pos[0]-(mouse_pos[1])*k-b
    }
    create_function_y(mouse_pos,position1,position2){// for y=... position1(lower x) y-....
        const k=(position2[1]-position1[1])/(position2[0]-position1[0]);
        const b=position1[1]-k*position1[0];
        return mouse_pos[1]-(mouse_pos[0])*k-b
    }
    extendVert(x0, y0, x1, y1, x2, y2) {
        const DRAW_IMAGE_EXTEND_EX = 3;
        var x = 2*x0 - x1 - x2, y = 2 * y0 - y1 - y2;
        var d = 70*Math.sqrt(DRAW_IMAGE_EXTEND_EX / (x * x + y * y));
        return [x0 + x * d, y0 + y * d];
    }

    
}

class Card_frame{
    constructor(){
        
        // this.model= new Image();
        // this.model.src="webpages/image_source/card/blue.PNG";
       
        this.image_background={
            "blue":"webpages/image_source/card/blue.PNG",
            "red":"webpages/image_source/card/red.PNG",
            "black":"webpages/image_source/card/black.PNG",
            "gold":"webpages/image_source/card/gold.PNG",
            "green":"webpages/image_source/card/green.PNG",

        }
        this.image_rarity={
            "Common":"webpages/image_source/rarity/Common.png",
            "Mythic Rare":"webpages/image_source/rarity/Mythic Rare.png",
            "Rare":"webpages/image_source/rarity/Rare.png",
            "Uncommon":"webpages/image_source/rarity/Uncommon.png",

        }
        this.color_fee_paths={
            "blue":"webpages/image_source/color_fee/blue.PNG",
            "red":"webpages/image_source/color_fee/red.PNG",
            "black":"webpages/image_source/color_fee/black.PNG",
            "gold":"webpages/image_source/color_fee/gold.PNG",
            "green":"webpages/image_source/color_fee/green.PNG",
            "colorless":"webpages/image_source/color_fee/colorless.PNG"
        }
        
    }
    //"blue","Caesar","Creature","Uncommon","nothing nothing","cards/creature/Spectral Harbinger/image.jpg"
    generate_card(type,name,type_card,rarity,content,image_path){
        const background=this.image_background[type];
        const rar=this.image_rarity[rarity];

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        const canvas_dynamic = document.createElement('canvas');
        const ctx_dynamic = canvas_dynamic.getContext('2d');

        const canvas_orginal_image = document.createElement('canvas');
        const ctx_orginal_image = canvas_orginal_image.getContext('2d');

        const canvas_battle=document.createElement('canvas');
        
        const ctx_canvas_battle = canvas_battle.getContext('2d');
        
        
        Promise.all([
            loadImage(background),
            loadImage(image_path),
            loadImage(rar),
            loadImage(this.color_fee_paths["colorless"]),
            loadImage(this.color_fee_paths["red"]),
            loadImage(this.color_fee_paths["blue"]),
            loadImage(this.color_fee_paths["green"]),
            loadImage(this.color_fee_paths["gold"]),
            loadImage(this.color_fee_paths["black"]),

        ]).then(images => {
            const rato=0.1
            
            canvas_orginal_image.width = images[1].width*rato;
            canvas_orginal_image.height = images[1].height*rato;
            ctx_orginal_image.drawImage(images[1],0,20,images[1].width,images[1].height,0,0,canvas_orginal_image.width,canvas_orginal_image.height)
            
            canvas.width = images[0].width;  // 例如，500 像素宽
            canvas.height = images[0].height;
            canvas_dynamic.width = images[0].width;  // 例如，500 像素宽
            canvas_dynamic.height = images[0].height;
            
            ctx.drawImage(images[0],0,0,canvas.width,canvas.height);
            ctx.save();
            this.create_blank_space(canvas,ctx,canvas.width/8,canvas.height*7.1/8);
            ctx.restore();
            ctx.save();
            this.create_blank_space(canvas,ctx,canvas.width/8,canvas.height*2.9/8);
            ctx.restore();
            ctx.save();
            this.create_rec_white(canvas,ctx,canvas.width/8,canvas.height*0.4/8)
            ctx.restore();
            
            ctx.setTransform(
                (320) / images[1].width,
                0,
                0,
                -(320) / images[1].height,
                images[1].width*1/24,
                images[1].height*1.455/3
            );
            
            ctx.drawImage(images[1],0,0,images[1].width,images[1].height*4/5,0,0,images[1].width,images[1].height*4/5);

            ctx.setTransform(
                (5) / images[2].width,
                0,
                0,
                -(4) / images[2].height,
                images[1].width*0.32,
                images[2].height*3.1
            );
            ctx.drawImage(images[2],0,0,canvas.width,canvas.height);
            this.fill_text_type(type_card,ctx,canvas.width/8,canvas.height*4.4/8);
            this.fill_text_title(name,ctx,canvas.width/8,canvas.height*4.4/8);
            this.fill_text_body(canvas,content,ctx,canvas.width/8,canvas.height*4.4/8)

            
            this.create_canvas_battle(canvas_battle,ctx_canvas_battle,images[0],name,images[1])

            //this.create_fee(ctx,color_fee,...Array.from({length: 6}, (_, i) => images[3+i]));
            
        }).catch(error => {
            console.error('Image loading failed:', error);
        });
        
        
    
        return [canvas_dynamic,ctx_dynamic,canvas,canvas_orginal_image,canvas_battle]
    }
    fill_text_type(type,ctx,startX,startY){
        ctx.setTransform(1, 0, 0, -1, 
            0,
            525);
        ctx.font = '18px Georgia';
        ctx.fillStyle = 'black';
       
        ctx.fillText(type, startX, startY);
    }

    fill_text_title(name,ctx,startX,startY){
        ctx.setTransform(1, 0, 0, -1, 
            0,
            820);
        ctx.font = '20px Georgia';
        ctx.fillStyle = 'black';
       
        ctx.fillText(name, startX, startY);
    }
    fill_text_body(canvas,content,ctx,startX,startY){
        ctx.font = '16px Georgia';
        ctx.fillStyle = 'black';
        ctx.textAlign = 'left';

        // 要绘制的文本和行间距
        const text =content ;
        const lineHeight = 30; // 行间距

        // 将文本拆分为单词数组
        const words = text.split(' ');
        const lines = [];
        let currentLine = words[0];

        // 将单词组合成行
        for (let i = 1; i < words.length; i++) {
            let testLine = currentLine + ' ' + words[i];
            let metrics = ctx.measureText(testLine);
            let testWidth = metrics.width;
            if (testWidth > canvas.width-canvas.width*2/8 && i > 0) {
                lines.push(currentLine);
                currentLine = words[i];
            } else {
                currentLine = testLine;
            }
        }

        lines.push(currentLine); // 添加最后一行

        // 绘制每一行文本
        lines.forEach((line, index) => {
            ctx.setTransform(1, 0, 0, -1, 
                10,
                520);
            ctx.fillText(line, startX, startY+lineHeight * (index + 1));
        });
    }
    create_blank_space(canvas,ctx,startX,startY){
        const blank_color="rgb(233,233,233,0.7)"
        const squareSize_x = canvas.width-canvas.width*2/8; // 正方形的边长
        const squareSize_y = 35;
        const radius = squareSize_y / 2; // 半圆的半径

        // 计算绘制的起始位置
        // const startX = canvas.width/8; // Canvas 上的起始 X 坐标
        // const startY = canvas.height*7.1/8; // Canvas 上的起始 Y 坐标

        // 绘制左侧的半圆
        ctx.beginPath();
        ctx.fillStyle = blank_color; // 改变填充颜色为蓝色
        ctx.arc(startX, startY + radius, radius, 0.5 * Math.PI, 1.5 * Math.PI);
        
        ctx.fill();
        ctx.fillStyle = 'rgb(0,0,0,1)'; // 改变填充颜色为蓝色
        ctx.stroke(); // 绘制半圆的描边

        // 绘制正方形
        ctx.fillStyle = blank_color; // 改变填充颜色为蓝色
        ctx.fillRect(startX, startY, squareSize_x, squareSize_y);
        ctx.fillStyle = 'rgb(0,0,0,1)'; // 改变填充颜色为蓝色
        ctx.beginPath();

        // 绘制正方形的顶部边缘
        ctx.moveTo(startX, startY);
        ctx.lineTo(startX+squareSize_x, startY);

        // 绘制正方形的底部边缘
        ctx.moveTo(startX, startY + squareSize_y);
        ctx.lineTo(startX + squareSize_x, startY + squareSize_y);

        // 执行描边
        ctx.stroke()
        // 绘制右侧的半圆
        ctx.beginPath();
        ctx.fillStyle = blank_color; // 改变填充颜色为蓝色
        ctx.arc(startX + squareSize_x, startY + radius, radius, 1.5 * Math.PI, 0.5 * Math.PI);
        ctx.fill();
        ctx.fillStyle = 'rgb(0,0,0,1)'; // 改变填充颜色为蓝色
        ctx.stroke(); // 绘制半圆的描边
    }

    create_rec_white(canvas,ctx,startX,startY){
       
        const blank_color="rgb(233,233,233,0.9)"
        const squareSize_x = canvas.width-canvas.width*2/8; // 正方形的边长
        const squareSize_y = 175;
        ctx.fillStyle = blank_color;
        ctx.fillRect(startX, startY, squareSize_x, squareSize_y);
        ctx.strokeRect(startX, startY, squareSize_x, squareSize_y);
    }

    
    initinal_background(){
        const blue= new Image();
        blue.src="webpages/image_source/card/blue.PNG";

        const red= new Image();
        red.src="webpages/image_source/card/red.PNG";

        const gold= new Image();
        gold.src="webpages/image_source/card/gold.PNG";

        const black= new Image();
        black.src="webpages/image_source/card/black.PNG";

        const green= new Image();
        green.src="webpages/image_source/card/green.PNG";
        
       
        return{
            "blue":blue,
            "red":red,
            "black":black,
            "gold":gold,
            "green":green,

        }
    }
    initinal_rarity(){
        const Common= new Image();
        Common.src="webpages/image_source/rarity/Common.png";

        const Mythic_Rare= new Image();
        Mythic_Rare.src="webpages/image_source/rarity/Mythic Rare.png";

        const Rare= new Image();
        Rare.src="webpages/image_source/rarity/Rare.png";

        const Uncommon= new Image();
        Uncommon.src="webpages/image_source/rarity/Uncommon.png";

        
       
        return{
            "Common":Common,
            "Mythic_Rare":Mythic_Rare,
            "Rare":Rare,
            "Uncommon":Uncommon,

        }
    }

    create_canvas_battle(canvas,ctx,background,name,image){
        
        const blank_color="rgb(233,233,233,0.8)"
        const startX=50
        const startY=40
        
        canvas.width = 700;  // 例如，500 像素宽
        canvas.height =500;
       
        // canvas.width=background.width;
        // canvas.height=background.height;
        
        const width_img=canvas.width*9.5/10;
        const height_img=canvas.height*4/5*0.97;
        

        const swidth=image.width
        const sheight=swidth*height_img/width_img
        this.draw_rect_smooth(ctx,0,0,canvas.width,canvas.height)

        
        ctx.drawImage(background,0,0,canvas.width,canvas.height);
        
        ctx.drawImage(image,0,canvas.height*1/5,swidth,sheight,canvas.width*0.5/20,canvas.height*1/5,width_img,height_img);
        
        // console.log(2)

        ctx.fillStyle = blank_color; 
        ctx.fillRect(canvas.width*0.5/20, 15, width_img, canvas.height*1/5-15);

        ctx.font = '60px Georgia';
        ctx.fillStyle = 'black';
        ctx.textAlign = 'left';
        const lineHeight = 30; // 行间距
        this.drawTextWithEllipsis(ctx,name,startX, startY+lineHeight,width_img)
        
    }
    drawTextWithEllipsis(ctx, text, x, y, maxWidth) {
        const metrics = ctx.measureText(text);
        if (metrics.width <= maxWidth) {
            ctx.fillText(text, x, y);
        } else {
            let adjustedText = text;
            while (ctx.measureText(adjustedText + '...').width > maxWidth) {
                adjustedText = adjustedText.slice(0, -1);
            }
            ctx.fillText(adjustedText + '...', x, y);
        }
    }

    draw_rect_smooth(ctx,x,y,width,height){
        
        
        var radius = 20; // 圆角半径

        // 绘制圆角长方形路径
        ctx.beginPath();
        ctx.moveTo(x + radius, y);
        ctx.lineTo(x + width - radius, y);
        ctx.arcTo(x + width, y, x + width, y + radius, radius);
        ctx.lineTo(x + width, y + height - radius);
        ctx.arcTo(x + width, y + height, x + width - radius, y + height, radius);
        ctx.lineTo(x + radius, y + height);
        ctx.arcTo(x, y + height, x, y + height - radius, radius);
        ctx.lineTo(x, y + radius);
        ctx.arcTo(x, y, x + radius, y, radius);
        ctx.closePath();
        // 应用裁剪
        ctx.clip();
    }
    
    
}