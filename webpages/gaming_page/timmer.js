class Ring_Record{
    constructor(position,size){
        this.position=position
        this.size=size
        const width=1
        const height=1
        this.corners=[//x y z
            [1*width,0,-1*height],
            [1*width,0,1*height],
            [-1*width,0,1*height],
            [-1*width,0,-1*height],

        ];
        this.canvas=document.createElement('canvas');
        this.canvas.width=width*150
        this.canvas.height=height*150
        this.ctx=this.canvas.getContext('2d')
        this.angle_x=0;
        this.angle_y=0;
        this.angle_z=0;
        this.points=this.get_org_position(this.size);


        this.text=""

        this.moving=false
        this.interval=2
    }

    animate_set(val,current_val){
        this.moving_precentage=0
        const different=val-current_val
        this.min_distance_difference=math.abs(different)
        const unit=(different/math.abs(different))
        const a=math.sqrt(math.abs(different)*2/math.pi)
        this.moving_store=[a,val,unit]
        this.moving=true
    }
    animate_move(){
        const a=this.moving_store[0];
        const unit=this.moving_store[2];
        const x=(a*math.pi/100)*this.moving_precentage
        const vel=unit*a*Math.pow(Math.sin(x/a),2)/((100/(this.interval))/(a*math.pi))
        this.moving_precentage+=this.interval
        return vel
    }
    
    check_move(){
        if (this.moving){
            this.val+=this.animate_move()

        }
    }

    check_distance(current_val){
        const val=this.moving_store[1]
        const difference=math.abs(val-current_val)
        if (difference<=this.min_distance_difference){
            this.min_distance_difference=difference
        }
        else{
            this.moving=false
            this.val=val
        }
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
    get_position_points(camera){
        const xy_rotate=math.multiply(rotateX(this.angle_x),rotateY(this.angle_y));
        const xyz_rotate=math.multiply(xy_rotate,rotateZ(this.angle_z));
        var pos_rotate=math.multiply(xyz_rotate,this.points);
        const posiiton_accurate=math.add(pos_rotate,this.get_matrix_position(pos_rotate))
        
        const camera_matrix=camera.get_matrix_position(pos_rotate)
        const position_by_camera=math.subtract(posiiton_accurate,camera_matrix);
        
        const xy_rotate_camera=math.multiply(rotateY(camera.angle_x),rotateX(camera.angle_y));
        const rotated=math.multiply(xy_rotate_camera,position_by_camera);
        //this.matrix_pos=rotated
        var pos_rotate=rotated;


        const final_points=[]
        for (let col = 0; col <= this.corners.length-1; col++){
            const final_point=[]
            for (let row = 0; row <= 2; row++){
                
                final_point.push(pos_rotate.get([row,col]));
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
        
        ctx.closePath();
        ctx.clip();
        ctx.setTransform(
            (points_pos[0][0] - points_pos[3][0]) / this.canvas.width,
            (points_pos[0][1] - points_pos[3][1]) / this.canvas.width,
            (points_pos[3][0] - points_pos[2][0]) / (this.canvas.height),
            (points_pos[3][1] - points_pos[2][1]) / (this.canvas.height),
            points_pos[2][0],
            points_pos[2][1]
        );
        
        ctx.drawImage(this.final_image,new_points_pos[0], new_points_pos[1], this.canvas.width/4, this.canvas.height/4, 0,0, this.canvas.width, this.canvas.height);
        //ctx.drawImage(this.image, 0, 0, this.image.width, this.image.height/4);
        ctx.restore();
    }
    draw_half_img_2(points_pos,new_points_pos,ctx){
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.save();
        ctx.beginPath();
        const p1=this.extendVert(points_pos[0][0], points_pos[0][1],points_pos[1][0], points_pos[1][1],points_pos[2][0], points_pos[2][1])
        const p2=this.extendVert(points_pos[1][0], points_pos[1][1],points_pos[0][0], points_pos[0][1],points_pos[2][0], points_pos[2][1])
        const p3=this.extendVert(points_pos[2][0], points_pos[2][1],points_pos[1][0], points_pos[1][1],points_pos[0][0], points_pos[0][1])
        ctx.moveTo(...p1); // 右下角
        ctx.lineTo(...p2); // 左下角
        ctx.lineTo(...p3); // 左上角
        
        ctx.closePath();
        ctx.clip();
        ctx.setTransform(
            (points_pos[1][0] - points_pos[2][0]) / this.canvas.width,
            (points_pos[1][1] - points_pos[2][1]) / this.canvas.width,
            (points_pos[0][0] - points_pos[1][0]) / this.canvas.height,
            (points_pos[0][1] - points_pos[1][1]) / this.canvas.height,
            points_pos[2][0],
            points_pos[2][1]
        );
        ctx.drawImage(this.final_image,new_points_pos[0], new_points_pos[1], this.canvas.width/4, this.canvas.height/4, 0,0, this.canvas.width, this.canvas.height);
        //ctx.drawImage(this.image, 0, 0, this.image.width, this.image.height);
        ctx.restore();
    }
    draw(camera,ctx,canvas){
        
        const new_points_pos=[];

        const new_points_z=[]
        
        
        this.final_image=this.canvas;
        
        //ctx.beginPath();
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;       
        for (let index_plane=0; index_plane<4;index_plane++){
            const x_start=this.arr_poses[index_plane][0]
            const y_start=this.arr_poses[index_plane][1]
            const z_start=this.arr_poses[index_plane][2]

            const end_x=cx + camera.similar_tri_2(x_start,z_start)
            const end_y=cy + camera.similar_tri_2(y_start,z_start)
            new_points_pos.push([end_x, end_y])
            new_points_z.push(z_start)
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
                
                this.draw_half_img_1(new_points_pos_1,[row*this.canvas.width/ROW,col*this.canvas.height/COL],ctx);
                this.draw_half_img_2(new_points_pos_1,[row*this.canvas.width/ROW,col*this.canvas.height/COL],ctx);
                //this.draw_half_img_1(new_points_pos_1,[row*this.canvas.width/ROW,col*this.canvas.height/COL],ctx);
            }
            col_left_up=col_left_down;
            col_right_up=col_right_down;
        }
        this.position_in_screen=new_points_pos;
        this.position_in_screen_z=(new_points_z[0]+new_points_z[2])/2
    }
    average_p(p_1,p_2,n,t){
        const x=p_2[0]+n*(p_1[0]-p_2[0])/t
        const y=p_2[1]+n*(p_1[1]-p_2[1])/t
        return [x,y]
    }


    get_matrix_position(matrixA){
        
        const matrix_position=math.matrix([[this.position[0]],[this.position[1]],[this.position[2]]])
        const matrixExpanded = math.map(matrixA, (value, index, matrix)=> {
            return matrix_position.get([index[0], 0]); // Use the row index to access matrixB and repeat its values
        });
        return matrixExpanded
    }
    extendVert(x0, y0, x1, y1, x2, y2) {
        const DRAW_IMAGE_EXTEND_EX = 3;
        var x = 2*x0 - x1 - x2, y = 2 * y0 - y1 - y2;
        var d = 50*Math.sqrt(DRAW_IMAGE_EXTEND_EX / (x * x + y * y));
        return [x0 + x * d, y0 + y * d];
    }

    check_inside(mouse_pos,position1,position2,position3,position4){//n shape of points
        
        return (
            this.create_function_x(mouse_pos,position2,position1)<0 &&
            this.create_function_y(mouse_pos,position4,position1)<0 &&
            this.create_function_x(mouse_pos,position4,position3)>0 &&
            this.create_function_y(mouse_pos,position3,position2)>0
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

}


class Timmer extends Ring_Record{


    constructor(max_time,position,size,name){
        super(position,size)
        this.max_time=max_time
        this.time=60
        this.name=name



        this.presentage=0

        

        this.text=""
        this.text_click="End"
        this.mode="time"//time, end

        this.changing_color=false
        this.changing_precentage=0
        this.rgb_yellow=[255,223,56]//yellow
        this.rgb_green=[66, 237, 57]//green

        this.current_color=[255,223,56]
        this.min_difference=[0,0,0]
    }
    animate_set(val,current_val){
        this.moving_precentage=0
        const different=val-current_val
        this.min_distance_difference=math.abs(different)
        const unit=(different/math.abs(different))
        const a=math.sqrt(math.abs(different)*2/math.pi)
        this.moving_store=[a,val,unit]
        this.moving=true
    }
    animate_move(){
        const a=this.moving_store[0];
        const unit=this.moving_store[2];
        const x=(a*math.pi/100)*this.moving_precentage
        const vel=unit*a*Math.pow(Math.sin(x/a),2)/((100/(this.interval))/(a*math.pi))
        this.moving_precentage+=this.interval
        return vel
    }
    
    check_move(){
        if (this.moving){
            this.time+=this.animate_move()
            this.check_distance(this.time)

        }
    }

    check_distance(current_val){
        const val=this.moving_store[1]
        const difference=math.abs(val-current_val)
        if (difference<=this.min_distance_difference){
            this.min_distance_difference=difference
        }
        else{
            this.moving=false
            this.time=val
        }
    }
    update_text(){
        if (this.mode=="time"){
            this.text=Math.round(this.time)
        }
        else{
            this.text=this.text_click
        }   
        
    }
   
    update(camera){
        //this.check_moving()
        
        // this.time=this.time+0.03
        this.check_move()
        if (this.changing_color){
            this.color_change()
        }
        
        this.presentage=100*this.time/this.max_time
        this.update_text()
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.save()
        this.print_ring(this.canvas,this.ctx,this.presentage)
        this.print_text(this.canvas,this.ctx)
        //this.ctx.drawImage(this.image,0,0,this.canvas.width,this.canvas.height);
        this.ctx.restore()
        //this.create_fee(this.dynamic_canvas[1],this.color_fee,...Array.from({length: 6}, (_, i) => this.images_fee[i]));
        
        this.arr_poses=this.get_position_points(camera);

        
        
        
    }
    

    print_ring(canvas,ctx,progress){
        const color=this.get_current_color()
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = 40;
        const startAngle = 0.5 * Math.PI; // 从顶部开始
        const endAngle =startAngle+ (progress/100)*2* Math.PI; // 计算结束角度
        //console.log(endAngle,startAngle)
        // ctx.beginPath();
        // ctx.arc(centerX, centerY, radius-1, 0, 2 * Math.PI);
        // ctx.fillStyle = '#e5e5e5';
        // ctx.fill();

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.lineWidth = 4; // 设置进度条的宽度
        ctx.lineCap = 'round';
        ctx.strokeStyle = color; // 进度条颜色
        // 设置阴影的颜色
        ctx.shadowColor = color; // 半透明的蓝色光晕
        // 设置阴影的模糊级别
        ctx.shadowBlur = 20;
        // 设置阴影的偏移量
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        ctx.stroke();

    }
    print_text(canvas,ctx){
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        ctx.font = '20px Arial';
        ctx.fillStyle = this.get_current_color();
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.text + '', centerX, centerY);
    }

    color_change_prepared(colors){
        //console.log(colors,this.current_color)
        const dif_r=math.abs(colors[0]-this.current_color[0])
        const dif_g=math.abs(colors[1]-this.current_color[1])
        const dif_b=math.abs(colors[2]-this.current_color[2])

        const unit_r=dif_r/(colors[0]-this.current_color[0])
        const unit_g=dif_g/(colors[1]-this.current_color[1])
        const unit_b=dif_b/(colors[2]-this.current_color[2])

        const a_r=math.sqrt(dif_r*2/math.pi)
        const a_g=math.sqrt(dif_g*2/math.pi)
        const a_b=math.sqrt(dif_b*2/math.pi)

        this.changing_store=[a_r,a_g,a_b,unit_r,unit_g,unit_b,colors]

        this.min_difference=[dif_r,dif_g,dif_b]

        this.changing_color=true
        this.changing_precentage=0
        this.check_target(colors)
    }
    color_change(){
        const time_consume=5
        const a_r= this.changing_store[0]
        const a_g= this.changing_store[1]
        const a_b= this.changing_store[2]
        const unit_r= this.changing_store[3]
        const unit_g= this.changing_store[4]
        const unit_b= this.changing_store[5]
        const x_r=(a_r*math.pi/100)*this.changing_precentage
        const x_g=(a_g*math.pi/100)*this.changing_precentage
        const x_b=(a_b*math.pi/100)*this.changing_precentage

        const dif_r=unit_r*a_r*Math.pow(Math.sin(x_r/a_r),2)/((100/(time_consume))/(a_r*math.pi))
        const dif_g=unit_g*a_g*Math.pow(Math.sin(x_g/a_g),2)/((100/(time_consume))/(a_g*math.pi))
        const dif_b=unit_b*a_b*Math.pow(Math.sin(x_b/a_b),2)/((100/(time_consume))/(a_b*math.pi))

        this.current_color[0]+=dif_r
        this.current_color[1]+=dif_g
        this.current_color[2]+=dif_b
        //console.log(this.current_color,a_r,a_g,a_b)
        this.changing_precentage+=time_consume
        this.check_target(this.changing_store[6])
    }
    color_change_finish(){
        this.current_color=[...this.changing_store[6]]
        this.changing_color=false
        this.changing_precentage=0
        //console.log(this.current_color)
    }
    check_target(colors){
        const dif_r=math.abs(colors[0]-this.current_color[0])
        const dif_g=math.abs(colors[1]-this.current_color[1])
        const dif_b=math.abs(colors[2]-this.current_color[2])
        
        if (dif_r<=this.min_difference[0] && dif_g<=this.min_difference[1] && dif_b<=this.min_difference[2]  && this.changing_precentage<100){
            this.min_difference=[dif_r,dif_g,dif_b]
        }
        else{
            this.color_change_finish()
        }
    }
    change_green(){
        this.color_change_prepared(this.rgb_green)
    }
    change_yellow(){
        this.color_change_prepared(this.rgb_yellow)
    }
    
    get_current_color(){
        return `rgb(${this.current_color[0]}, ${this.current_color[1]}, ${this.current_color[2]})`;
    }

    
}

class Player_Life extends Ring_Record{
    constructor(position,size,unit){
        
        super(position,size)

        this.max_life=20
        
        this.life=10

        this.angle=120*(Math.PI/180)

        this.text="10"

        this.unit=unit



        this.blue=[126,163,255]//'rgba(126,163,255)'
        this.orange=[255,96,0]//'rgba(255,96,0)'
        this.select_flag=false
        this.orginal_flag=false



        this.changing_color=false
        
        this.changing_precentage=0

        this.current_color=[255,96,0]
        this.min_difference=[0,0,0]


            
    }

    check_move(){
        if (this.moving){
            this.life+=this.animate_move()
            this.check_distance(this.life)

        }
    }

    check_distance(current_val){
        const val=this.moving_store[1]
        const difference=math.abs(val-current_val)
        if (difference<=this.min_distance_difference){
            this.min_distance_difference=difference
        }
        else{
            this.moving=false
            this.life=val
        }
    }
    print_ring(canvas,ctx){
        const color=this.get_current_color()
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = 40;
        var startAngle = (1+this.unit/2) * Math.PI-(this.angle/2); // 从顶部开始
        var endAngle =startAngle+ (this.angle)*this.life/this.max_life; // 计算结束角度
        // if (endAngle<startAngle){
        //     [startAngle,endAngle]=[endAngle,startAngle]
        // }
        //console.log(endAngle,startAngle)
        // ctx.beginPath();
        // ctx.arc(centerX, centerY, radius, startAngle, startAngle+Math.PI*2);//this.angle);
        // ctx.fillStyle = '#000000';
        // ctx.lineWidth = 4; // 设置进度条的宽度
        // ctx.lineCap = 'round';
        // //ctx.strokeStyle = '#8c8c8c'; 
        // ctx.fill();

        ctx.beginPath();
        
        ctx.arc(centerX, centerY, radius, startAngle, startAngle+this.angle);
        
        
        //ctx.fillStyle = '#e5e5e5';
        ctx.lineWidth = 4; // 设置进度条的宽度
        ctx.lineCap = 'round';
        ctx.strokeStyle = '#8c8c8c'; 
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.lineWidth = 7; // 设置进度条的宽度
        ctx.lineCap = 'round';
        ctx.strokeStyle = color; 
        ctx.shadowColor = color;
        ctx.shadowBlur = 20;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        ctx.stroke();

    }
    print_text(canvas,ctx){
        const color=this.get_current_color()
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        ctx.font = '30px Cinzel';
        ctx.fillStyle = color;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(Math.round(this.life) + '', centerX, centerY);
    }
    update_text(){
        
    }
   
    update(camera){
        //this.check_moving()
        this.check_move()
        this.update_text()
        this.check_select_bool()
        if (this.changing_color){
            this.color_change()
        }
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.save()
        this.print_ring(this.canvas,this.ctx,this.presentage)
        this.print_text(this.canvas,this.ctx)
        //this.ctx.drawImage(this.image,0,0,this.canvas.width,this.canvas.height);
        this.ctx.restore()
        //this.create_fee(this.dynamic_canvas[1],this.color_fee,...Array.from({length: 6}, (_, i) => this.images_fee[i]));
        
        this.arr_poses=this.get_position_points(camera);


    }
    get_copy(){
        const new_ring=new Player_Life([0,0,0],this.size+4,this.unit)
        new_ring.life=this.life
        new_ring.angle_x=math.pi/2
        return new_ring
    }

    // get_color(){
    //     if (this.select_flag){
    //         return this.blue
    //     }
    //     else{
    //         return this.orange
    //     }
    // }


    color_change_prepared(colors){
        //console.log(colors,this.current_color)
        const dif_r=math.abs(colors[0]-this.current_color[0])
        const dif_g=math.abs(colors[1]-this.current_color[1])
        const dif_b=math.abs(colors[2]-this.current_color[2])

        const unit_r=dif_r/(colors[0]-this.current_color[0])
        const unit_g=dif_g/(colors[1]-this.current_color[1])
        const unit_b=dif_b/(colors[2]-this.current_color[2])

        const a_r=math.sqrt(dif_r*2/math.pi)
        const a_g=math.sqrt(dif_g*2/math.pi)
        const a_b=math.sqrt(dif_b*2/math.pi)

        this.changing_store=[a_r,a_g,a_b,unit_r,unit_g,unit_b,colors]

        this.min_difference=[dif_r,dif_g,dif_b]

        this.changing_color=true
        this.changing_precentage=0
        this.check_target(colors)
    }
    color_change(){
        const time_consume=3
        const a_r= this.changing_store[0]
        const a_g= this.changing_store[1]
        const a_b= this.changing_store[2]
        const unit_r= this.changing_store[3]
        const unit_g= this.changing_store[4]
        const unit_b= this.changing_store[5]
        const x_r=(a_r*math.pi/100)*this.changing_precentage
        const x_g=(a_g*math.pi/100)*this.changing_precentage
        const x_b=(a_b*math.pi/100)*this.changing_precentage

        const dif_r=unit_r*a_r*Math.pow(Math.sin(x_r/a_r),2)/((100/(time_consume))/(a_r*math.pi))
        const dif_g=unit_g*a_g*Math.pow(Math.sin(x_g/a_g),2)/((100/(time_consume))/(a_g*math.pi))
        const dif_b=unit_b*a_b*Math.pow(Math.sin(x_b/a_b),2)/((100/(time_consume))/(a_b*math.pi))

        this.current_color[0]+=dif_r
        this.current_color[1]+=dif_g
        this.current_color[2]+=dif_b
        //console.log(this.current_color,a_r,a_g,a_b)
        this.changing_precentage+=time_consume
        this.check_target(this.changing_store[6])
    }
    color_change_finish(){
        this.current_color=[...this.changing_store[6]]
        this.changing_color=false
        this.changing_precentage=0
        //console.log(this.current_color)
    }
    check_target(colors){
        const dif_r=math.abs(colors[0]-this.current_color[0])
        const dif_g=math.abs(colors[1]-this.current_color[1])
        const dif_b=math.abs(colors[2]-this.current_color[2])
        
        if (dif_r<=this.min_difference[0] && dif_g<=this.min_difference[1] && dif_b<=this.min_difference[2]  && this.changing_precentage<100){
            this.min_difference=[dif_r,dif_g,dif_b]
        }
        else{
            this.color_change_finish()
        }
    }
    change_blue(){
        this.color_change_prepared(this.blue)
    }
    change_orange(){
        this.color_change_prepared(this.orange)
    }
    
    get_current_color(){
        return `rgb(${this.current_color[0]}, ${this.current_color[1]}, ${this.current_color[2]})`;
    }

    check_select_bool(){
        if (this.orginal_flag!=this.select_flag){
            if(this.select_flag){
                this.change_blue()
            }
            else{
                this.change_orange()
            }
            this.orginal_flag=this.select_flag
        }
    }
}