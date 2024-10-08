

class Card_Battle{
    constructor(width,height,position,size,card,player,table){//player:self,opponent
        card.battle=this
        this.table=table
        this.player=player
        //console.log(player,table)
        this.corners=[//x y z
            [1*width,-1*height,0],
            [1*width,1*height,0],
            [-1*width,1*height,0],
            [-1*width,-1*height,0],

        ];
        this.position=position;
        this.angle_x=math.pi/2;
        this.angle_y=0;
        
        this.angle_z=0;
        
        
        this.vel_x=0;
        this.vel_y=0;
        this.vel_z=0;
        this.arr_poses=NaN;
        this.size=size
        this.points=this.get_org_position(this.size);
        this.card=card
        this.image=card.dynamic_canvas[4]
       
        this.id=card.id;

        this.canvas=document.createElement('canvas');
        this.back_img=new Image();
        this.back_img.src="webpages/image_source/card/back.png";
        this.canvas.width=80*10
        this.canvas.height=60*10
        this.ctx=this.canvas.getContext('2d')


        this.moving=false;//用来移动卡牌的开关
        this.moving_precentage=0;
        this.moving_dict={
            "move_to_horizontal":[this.move_to_horizontal.bind(this),this.move_to_horizontal.bind(this),this.move_to_horizontal_finish.bind(this)],
            "move_to":[this.move_to.bind(this),this.move_to_prepared.bind(this),this.move_to_finish.bind(this)],
            "attack_to":[this.attack_to.bind(this),this.attack_to_prepared.bind(this),this.attack_to_finish.bind(this)],
            "rotate_to_point":[this.rotate_to_point.bind(this),this.rotate_to_point_prepared.bind(this),this.rotate_to_finish.bind(this)],
            "back_to":[this.back_to.bind(this),this.back_to_prepared.bind(this),this.back_to_finish.bind(this)],
            "disappear":[this.disappear.bind(this),this.disappear_prepared.bind(this),this.disappear_finish.bind(this)]
        }
        //console.log([this.move_to,this.move_to_prepared])
        this.current_moving=null;//this.move_to_horizontal.....
        this.finish_moving=null;
        this.moving_parameters=[];
        this.moving_store=[];
        this.min_distance_difference=0;



        this.moving_cache=[]//接收["名字"，target position]
        this.accurate_position=[0,position[1],0]//这个是通过table计算得出来的相对牌的位置
        this.orginal_angle=[0,0,1]//初始指向的方向

        this.card_hold=[false,false]//click_bool,move_bool

        this.z_index=1;

        this.activated=false

        this.select_flag=false

        this.buff_list=card.buff_list
        this.flag_dict=card.flag_dict
        this.counter_dict=card.counter_dict
        
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
    change_size(size){
        this.size=size
        this.points=this.get_org_position(this.size);
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
        // ctx.moveTo(points_pos[0][0], points_pos[0][1]); // 右下角
        // ctx.lineTo(points_pos[3][0], points_pos[3][1]); // 左下角
        // ctx.lineTo(points_pos[2][0], points_pos[2][1]); // 左上角
        // ctx.lineTo(points_pos[1][0], points_pos[1][1]);
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
    update(camera){
        this.check_moving()
        //console.log(this,this.moving)
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.save()
        let filter= '';

        if(this.activated==true){
            
            filter =filter + "brightness(50%)"
            
        }

        for (const buff of this.buff_list){
            if (buff.content=="frozen"){
                filter=filter + " hue-rotate(180deg) saturate(1.2)"
                break
            }
        }
        

        // if(this.activated==true){
        //     this.ctx.filter = 'brightness(50%)';
        //     this.ctx.drawImage(this.image,0,0,this.canvas.width,this.canvas.height);
        //     this.ctx.filter = '';
        // }
        // else{
        
        this.ctx.filter=filter
        this.ctx.drawImage(this.image,0,0,this.canvas.width,this.canvas.height);
        // }
        this.ctx.filter = '';
        
        //this.ctx.drawImage(this.image,0,0,this.canvas.width,this.canvas.height);
        this.ctx.restore()
        //this.create_fee(this.dynamic_canvas[1],this.color_fee,...Array.from({length: 6}, (_, i) => this.images_fee[i]));
        
        this.arr_poses=this.get_position_points(camera);

        

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
        this.position_in_screen=new_points_pos;

        if (this.select_flag){
            this.draw_blur_ring(ctx)
            this.draw_blur_ring(ctx)
            //this.draw_blur_ring(ctx)
        }

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
        var d = Math.sqrt(DRAW_IMAGE_EXTEND_EX / (x * x + y * y));
        return [x0 + x * d, y0 + y * d];
    }

    draw_shade(height_table,camera,ctx,canvas){
        if (this.position[1]!=-20){
            const xy_rotate=math.multiply(rotateX(this.angle_x),rotateY(this.angle_y));
            const xyz_rotate=math.multiply(xy_rotate,rotateZ(this.angle_z));
            var pos_rotate=math.multiply(xyz_rotate,this.points);
            const posiiton_accurate=math.add(pos_rotate,this.get_matrix_position(pos_rotate))

            const Sun_light=math.matrix([[-0.5],[-1.2],[-0.6]])

            const [rows, cols] =posiiton_accurate.size();
            const height=math.zeros(rows, cols);

            for (let i=0;i<cols;i++){
                height.subset(math.index(rows-2, i), height_table);

                //height[rows-2][i]=height_table
            }
            const t=math.multiply(math.matrix([[0,1/Sun_light.get([1,0]),0]]),math.subtract(posiiton_accurate,height))
            const change=math.multiply(Sun_light,t)
            const sun_result=math.subtract(posiiton_accurate,change)


            const camera_matrix=camera.get_matrix_position(sun_result)
            const position_by_camera=math.subtract(sun_result,camera_matrix);
            const xy_rotate_camera=math.multiply(rotateY(camera.angle_x),rotateX(camera.angle_y));
            const rotated=math.multiply(xy_rotate_camera,position_by_camera);
            //this.matrix_pos=rotated
            var pos_rotate=rotated;



            ctx.beginPath();
            const final_points=[]
            const cx = canvas.width / 2;
            const cy = canvas.height / 2;      
            for (let col = 0; col <= this.corners.length-1; col++){
                const final_point=[]
                const x_start=pos_rotate.get([0,col])
                const y_start=pos_rotate.get([1,col])
                const z_start=pos_rotate.get([2,col])
                const end_x=cx + camera.similar_tri_2(x_start,z_start)
                const end_y=cy + camera.similar_tri_2(y_start,z_start)
                if (col==0) {
                    ctx.moveTo(end_x, end_y); 
                }
                else{
                    ctx.lineTo(end_x, end_y);    
                }
                final_points.push(final_point);
                
            }
            ctx.closePath();  
            ctx.fillStyle = "rgb(23,23,23,0.6)";
            ctx.fill();
        }

    }


    check_moving(){
        if (!this.card_hold[1]){
            if (this.moving && this.moving_precentage<100){
                this.current_moving(...this.moving_parameters)
                
            }
            else if(this.moving && this.moving_precentage>=100){
                this.moving=false
                this.moving_precentage=0
                this.finish_moving(...this.moving_parameters)
            }
            else  {//if (this.position==this.accurate_position)
                this.pick_moving_function()
            }
        }
        else{
            this.moving=false
            this.moving_precentage=0
        }
        
    }

    start_moving(moving_type,parameters){
        if (this.moving==false && this.moving_precentage<100){
            this.moving_precentage=0;
            this.moving=true
            this.current_moving=this.moving_dict[moving_type][0]
            this.finish_moving=this.moving_dict[moving_type][2]
            
            this.moving_dict[moving_type][1](...parameters)
            
            
            this.moving_parameters=parameters;
            this.check_moving()
            
            
        }
    }

    pick_moving_function(){//FIFO
        if (this.moving_cache.length){
            //console.log(this.moving_cache,this.moving_cache.length)
            const para=this.moving_cache.shift()
            //console.log(para,this.moving_cache,this.moving_cache.length)
            
            this.start_moving(...para)
        }
        else{
            this.moving=false
            this.moving_precentage=0
        }
        
    }
    move_to_horizontal(target_position){//target_position[x,y,z]
        

    }
    move_to_horizontal_prepared(target_position){//target_position[x,y,z]
        

    }
    move_to_horizontal_finish(target_position){//target_position[x,y,z]
        

    }
    
    disappear_prepared(target_position){//target_position[x,y,z]
        this.move_to_prepared(target_position)
        this.moving_store.push(this.size)

    }
    disappear(target_position){//target_position[x,y,z]
        const size=this.moving_store[4]
        this.move_to(target_position)

        this.change_size(size-this.moving_precentage*size/100)
        
    }
    disappear_finish(target_position){//target_position[x,y,z]
        //console.log(this.player)
        if (this.player=="opponent"){
            this.table.opponent_battlefield_delete.push(this);
            
        }
        else{
            this.table.self_battlefield_delete.push(this);
        }
        this.move_to_finish(target_position)
    }

    move_to_prepared(target_position){
        
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        this.min_distance_difference=distance;
        const a=math.sqrt(distance*2/math.pi)
        const time_consume=1/distance+2
        
        this.moving_store=[a,unitVector,time_consume,target_position]
        this.check_distance_to_target(target_position)
    }
    move_to(target_position){//target_position[x,y]
        const a=this.moving_store[0];
        const unitVector=this.moving_store[1];
        const time_consume=this.moving_store[2];
        //console.log(time_consume)
        const x=(a*math.pi/100)*this.moving_precentage
        const vel=a*Math.pow(Math.sin(x/a),2)/((100/(TIME_INTERVAL*time_consume))/(a*math.pi))
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=TIME_INTERVAL*time_consume
        this.check_distance_to_target(target_position)
        //console.log(this.position)
        
    }
    move_to_finish(target_position){
        const final_pos=this.moving_store[3];
        this.position[0]=final_pos[0]
        this.position[1]=final_pos[1]
        this.position[2]=final_pos[2]
        this.pick_moving_function()
        
    }



    attack_to_prepared(target_position){//target_position[x,y,z]  撞一下然后返回原来的位置
        //console.log(this,target_position,this.calculate_vector_move)
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        this.min_distance_difference=distance;
        const a=math.sqrt(distance*(4)/math.pi)
        const time_consume=2.5
        this.moving_store=[a,unitVector,time_consume]
    }
    attack_to(target_position){//target_position[x,y,z]  撞一下然后返回原来的位置
        const a=this.moving_store[0];
        const unitVector=this.moving_store[1];
        const time_consume=this.moving_store[2];
        
        //console.log(time_consume)
        const x=((a*math.pi/2)/100)*this.moving_precentage
        
        
        
        var vel=a*Math.pow(Math.sin(x/a),2)/((100/(TIME_INTERVAL*time_consume))/(a*math.pi/2))
        
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=TIME_INTERVAL*time_consume

        this.check_distance_to_target(target_position)
        //console.log(this.position)
    }
    attack_to_finish(target_position){//target_position[x,y,z]  撞一下然后返回原来的位置
        
        this.position[0]=target_position[0]
        this.position[1]=target_position[1]
        this.position[2]=target_position[2]
        //console.log(this.accurate_position)
        this.start_moving('back_to',[this.accurate_position])
    }


    back_to_prepared(target_position){
        //console.log(this,target_position,this.calculate_vector_move)
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        this.min_distance_difference=distance;
        const a=math.sqrt(distance*(4)/math.pi)
        const time_consume=2.5
        this.moving_store=[a,unitVector,time_consume]
    }
    back_to(target_position){
        const a=this.moving_store[0];
        const unitVector=this.moving_store[1];
        const time_consume=this.moving_store[2];
        
        //console.log(time_consume)
        const x=a*math.pi/2+((a*math.pi/2)/100)*this.moving_precentage
        
        var vel=a*Math.pow(Math.sin(x/a),2)/((100/(TIME_INTERVAL*time_consume))/(a*math.pi/2))
        
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=TIME_INTERVAL*time_consume

        this.check_distance_to_target(target_position)
        //console.log(this.position)
    }
    back_to_finish(target_position){
        this.position[0]=target_position[0]
        this.position[1]=target_position[1]
        this.position[2]=target_position[2]
        this.pick_moving_function()
        //this.start_moving('rotate_to_point',[this.orginal_angle])
    }



    rotate_to_point_prepared(target_position){//让它指向目标点 x,y,z  target_position position or tap
        //console.log(target_position,this.accurate_position,this.position)
        const direction_vector=this.get_vector_point()
        if (Array.isArray(target_position)) {
            var [unitVector,distance]=this.calculate_vector_move(target_position)
        }
        else{
            const radians=target_position * (Math.PI / 180);
            var [unitVector,distance]=this.calculate_vector_move(
                [
                    this.position[0]+Math.cos(radians),
                    this.position[1],
                    this.position[2]+Math.sin(radians),
                ]
            )
        }
        
        
        const a=[direction_vector[0],direction_vector[2]]
        const b=[unitVector[0],unitVector[2]]
        

        const angleA = math.atan2(a[1], a[0]);
        const angleB = math.atan2(b[1], b[0]);

        let angleDifference = angleB - angleA;

        // 标准化结果到 [-π, π] 区间，确定最短旋转路径
        angleDifference = math.mod(angleDifference + math.pi, 2 * math.pi) - math.pi;

        // 计算夹角（以弧度为单位）
        
        const thetaRadians = angleDifference;


        
        const abs_thetaRadians=Math.abs(thetaRadians)
        const A=(thetaRadians/abs_thetaRadians)*math.sqrt(abs_thetaRadians*(2)/math.pi)
        
        const target_angle=this.angle_z+thetaRadians
        const time_consume=2.5
        if (!A){
            this.moving_precentage=100
            this.moving_store=[thetaRadians,A,time_consume,this.angle_z]
            
        }
        else{
            this.moving_store=[thetaRadians,A,time_consume,target_angle]
        }
        

       
        
    }
    rotate_to_point(target_position){//让它指向目标点
        //console.log("rotate")
        const a=this.moving_store[1];
        const thetaRadians=this.moving_store[0];
        const time_consume=this.moving_store[2];
        
        
        const x=((a*math.pi/2)/100)*this.moving_precentage
        const angle_change=a*Math.pow(Math.sin(x/a),2)/((100/(TIME_INTERVAL*time_consume))/(Math.abs(a)*math.pi))
        this.angle_z=this.angle_z+angle_change
        this.moving_precentage+=TIME_INTERVAL*time_consume
        
    }
    rotate_to_finish(target_position){//让它指向目标点
        this.angle_z=this.moving_store[3]
        this.pick_moving_function()
        //console.log(this.angle_x,this.angle_y,this.angle_z)
    }

    calculate_vector_move(target_position){//返回一个unit vector, 总的distance
        const difference = math.subtract(target_position, this.position);
        const distance=math.norm(difference);
        const unitVector = math.divide(difference, distance);
        return [unitVector,distance]

    }
    check_distance_to_target(target_position){
        const [_,distance]=this.calculate_vector_move(target_position)
        
        if (distance<=this.min_distance_difference && math.abs(distance)){
            this.min_distance_difference=distance
        }
        else{
            this.moving_precentage=100
            
        }
        
    }

    get_vector_point(){
        const org_direction=math.matrix([[0],[0],[1]])
        //const xz_rotate=math.multiply(rotateX(this.angle_x),rotateZ(this.angle_z));
        //const xyz_rotate=math.multiply(xy_rotate,rotateZ(this.angle_z));
        
        var pos_rotate=math.multiply(rotateY(-this.angle_z),org_direction);
        
        return pos_rotate.toArray().flat();
    }
    check_inside(mouse_pos,position1,position2,position3,position4){//n shape of points
        //console.log(position1,position2,position3,position4)
        const positions=this.sortPositions([position1,position2,position3,position4])
        //console.log(positions)
        return (
            this.create_function_x(mouse_pos,positions[1],positions[0])<0 &&
            this.create_function_y(mouse_pos,positions[3],positions[0])<0 &&
            this.create_function_x(mouse_pos,positions[3],positions[2])>0 &&
            this.create_function_y(mouse_pos,positions[2],positions[1])>0
        )

    }


    sortPositions(positions) {
        // Calculate the center point
        let centerX = 0;
        let centerY = 0;
        positions.forEach(pos => {
            centerX += pos[0];
            centerY += pos[1];
        });
        centerX /= positions.length;
        centerY /= positions.length;
        //console.log(centerX, centerY);
    
        // Calculate angles for each position relative to center
        positions = positions.map(pos => ({
            x: pos[0],
            y: pos[1],
            angle: Math.atan2(pos[1] - centerY, pos[0] - centerX)
        }));
    
        // Adjust angles to start from the top right quadrant
        positions.forEach(pos => {
            pos.angle -= Math.PI*3/2 ; // Subtract 90 degrees
            if (pos.angle < -Math.PI) pos.angle += 2 * Math.PI; // Normalize angle between -π and π
        });
    
        // Sort positions by angle in clockwise order
        positions.sort((a, b) => b.angle - a.angle); // Reverse sort to make it clockwise
    
        // Extract sorted positions without angle
        const sortedPositions = positions.map(pos => [pos.x, pos.y]);
    
        return sortedPositions;
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

    moving_by_mouse(mouse_pos,camera){
        
        const limit=0.9;
        const next_pos=camera.similar_tri_reverse_2(...mouse_pos,this.position[1],this.position_in_screen_z);
        const x_diff=(next_pos[0]-this.position[0])/1;
        const y_diff=-(next_pos[2]-this.position[2])/1;
        

        this.angle_y = x_diff > limit ? limit : (x_diff < -limit ? -limit :x_diff);
        this.angle_x = math.pi/2+(y_diff > limit ? limit : (y_diff < -limit ? -limit :y_diff));

        this.position[0]=next_pos[0]
        this.position[2]=next_pos[2]
    }

    draw_blur_ring(ctx){
        ctx.save()
        
        
        ctx.beginPath();
            
        ctx.moveTo(this.position_in_screen[0][0], this.position_in_screen[0][1]);
        ctx.lineTo(this.position_in_screen[1][0], this.position_in_screen[1][1]);
        
        ctx.lineTo(this.position_in_screen[2][0], this.position_in_screen[2][1]);
        
        ctx.lineTo(this.position_in_screen[3][0], this.position_in_screen[3][1]);
        
        ctx.lineTo(this.position_in_screen[0][0], this.position_in_screen[0][1]);
        
        
        
        ctx.closePath();
        ctx.strokeStyle = 'rgba(126,163,255)';
        ctx.shadowColor = 'rgba(126,163,255)'; // 半透明的蓝色光晕
        ctx.fillStyle = 'rgba(126,163,255)';
        ctx.lineCap = 'round';
        ctx.shadowBlur = 20;
        // 设置阴影的偏移量
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        ctx.lineWidth = 1;
        ctx.fill(); // 描绘边框
        //ctx.stroke()
        ctx.restore()
        //ctx.restore()
        //ctx.stroke(); // 描绘边框

        // ctx.shadowColor = 'transparent';
        // ctx.shadowBlur = 0;
        // ctx.shadowOffsetX = 0;
        // ctx.shadowOffsetY = 0;
        
            

    }

    append_buff(buff){
        this.buff_list.push(buff)
        //this.card.buff_list.push(buff)
        //console.log(this.buff_list,this.card.buff_list)
    }
    remove_buff(buff){
        this.buff_list=this.buff_list.filter(item => item.id !== buff.id);
        this.card.buff_list=this.buff_list
    }


}