class Card_Hand extends Card{
    constructor(width,height,position,size,dynamic_canvas,color_fee,name,id,player){
        super(width,height,position,size,dynamic_canvas,color_fee,name)
        this.player=player
        this.id=id

        this.moving=false;//用来移动卡牌的开关
        this.moving_precentage=0;
        this.moving_dict={
            "move_to_horizontal":[this.move_to_horizontal.bind(this),this.move_to_horizontal.bind(this),this.move_to_horizontal_finish.bind(this)],
            "move_to":[this.move_to.bind(this),this.move_to_prepared.bind(this),this.move_to_finish.bind(this)],
            "rotate_to_point":[this.rotate_to_point.bind(this),this.rotate_to_point_prepared.bind(this),this.rotate_to_finish.bind(this)],
            "disappear":[this.disappear.bind(this),this.disappear_prepared.bind(this),this.disappear_finish.bind(this)],
            "small":[this.small.bind(this),this.small_prepared.bind(this),this.small_finish.bind(this)],
            "enlarge":[this.enlarge.bind(this),this.enlarge_prepared.bind(this),this.enlarge_finish.bind(this)],
            "change_size_animation":[this.change_size_animation.bind(this),this.change_size_animation_prepared.bind(this),this.change_size_animation_finish.bind(this)]
        }
        console.log([this.move_to,this.move_to_prepared])
        this.current_moving=null;//this.move_to_horizontal.....
        this.finish_moving=null;
        this.moving_parameters=[];
        this.moving_store=[];
        this.min_distance_difference=0;



        this.moving_cache=[]//接收["名字"，target position]
        this.accurate_position=[0,position[1],0]//这个是通过table计算得出来的相对牌的位置
        this.orginal_angle=[0,0,1]//初始指向的方向
        this.TIME_INTERVAL=2
        this.card_hold=[false,false]//click_bool,move_bool
        this.enlarge_switch=false


        this.change_size_cache=undefined


        this.z_index=1;
    }


    change_size(size){
        this.size=size
        this.points=this.get_org_position(this.size);
    }

    check_change_size(){
        if (!(this.change_size_cache===undefined)){
            this.change_size(this.change_size_cache)
            this.change_size_cache=undefined
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
            else {
                this.pick_moving_function()
            }
        }
        else{
            this.moving=false
            this.moving_precentage=0
        }
        
    }

    start_moving(moving_type,parameters){
        //console.log(this.moving,parameters)
        if (this.moving==false && this.moving_precentage<100){
            this.moving_precentage=0;
            this.moving=true
            this.current_moving=this.moving_dict[moving_type][0]
            this.finish_moving=this.moving_dict[moving_type][2]
            
            this.moving_dict[moving_type][1](...parameters)
            
            
            this.moving_parameters=parameters;
            
        }
    }

    pick_moving_function(){//FIFO
        if (this.moving_cache.length){
            
            const para=this.moving_cache.shift()
            
            this.start_moving(...para)
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
        
        //console.log(this.player, this.player.hand_delete)
        this.player.hand_delete.push(this);
        
        this.move_to_finish(target_position)
    }



    small_prepared(target_position){//target_position[x,y,z]
        this.move_to_prepared(target_position)
        this.moving_store.push(1.5)
        //console.log(this.size)

    }
    small(target_position){//target_position[x,y,z]
        //console.log(this.size)
        const size=this.moving_store[4]
        this.move_to(target_position)

        this.change_size(size-(1/3)*this.moving_precentage*size/100)
        
        //console.log(size-(1/3)*this.moving_precentage*size/100)
        
        
    }
    small_finish(target_position){//target_position[x,y,z]
        const size=this.moving_store[4]
        
        
        this.change_size(1)
        //console.log(this.size)
        
        this.move_to_finish(target_position)
    }



    enlarge_prepared(target_position){//target_position[x,y,z]
        this.move_to_prepared(target_position)
        this.moving_store.push(1)

    }
    enlarge(target_position){//target_position[x,y,z]
        const size=this.moving_store[4]
        this.move_to(target_position)

        this.change_size(size+0.5*this.moving_precentage*size/100)
        //console.log(size+0.5*this.moving_precentage*size/100)
        
    }
    enlarge_finish(target_position){//target_position[x,y,z]
        
        const size=this.moving_store[4]
        this.change_size(1.5)
        this.move_to_finish(target_position)
    }




    move_to_prepared(target_position){
        
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        this.min_distance_difference=distance;
        const a=math.sqrt(distance*2/math.pi)
        const time_consume=1/distance+2
        
        this.moving_store=[a,unitVector,time_consume,target_position]
        this.check_distance_to_target(target_position)
        //console.log(321)
    }
    move_to(target_position){//target_position[x,y]
        const a=this.moving_store[0];
        const unitVector=this.moving_store[1];
        const time_consume=this.moving_store[2];
        //console.log(time_consume)
        const x=(a*math.pi/100)*this.moving_precentage
        const vel=a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume))/(a*math.pi))
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=this.TIME_INTERVAL*time_consume
        this.check_distance_to_target(target_position)
        //console.log(this.position)
        
    }
    move_to_finish(target_position){
        const final_pos=this.moving_store[3];
        this.position[0]=final_pos[0]
        this.position[1]=final_pos[1]
        this.position[2]=final_pos[2]
        //console.log(123)
        this.pick_moving_function()
        
        
    }




    rotate_to_point_prepared(target_position){//让它指向目标点 x,y,z
        const direction_vector=this.get_vector_point()
        
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        
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
        const angle_change=a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume))/(Math.abs(a)*math.pi))
        this.angle_z=this.angle_z+angle_change
        this.moving_precentage+=this.TIME_INTERVAL*time_consume
        
    }
    rotate_to_finish(target_position){//让它指向目标点
        this.angle_z=this.moving_store[3]
        this.pick_moving_function()
        //console.log(this.angle_x,this.angle_y,this.angle_z)
    }

    change_size_animation_prepared(size_target){
        //console.log(size_target,this.size)
        const size_diff=math.abs(size_target-this.size)
        const a=math.sqrt(math.abs(size_diff)*2/math.pi)
        const time_consume=1/size_diff+2
        const unit=size_diff/(size_target-this.size)
        this.min_distance_difference=size_diff
        this.moving_store=[a,time_consume,this.size,size_target,unit]
        this.check_size_to_target(size_target)
    }
    change_size_animation(size_target){
        const a=this.moving_store[0];
        const unit=this.moving_store[4]
        const time_consume=this.moving_store[1];
        const org_size=this.moving_store[2];
        //console.log(time_consume)
        
        const x=(a*math.pi/100)*this.moving_precentage
        const dif_size=unit*a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume))/(a*math.pi))
        
        this.change_size(this.size+dif_size)
        //console.log(this.size,dif_size)
        
        this.moving_precentage+=this.TIME_INTERVAL*time_consume
        this.check_size_to_target(size_target)
    }
    change_size_animation_finish(size_target){
        
        this.change_size(this.moving_store[3])
        this.pick_moving_function()
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
            // this.moving=false
            // this.moving_precentage=0
            
            // this.finish_moving(...this.moving_parameters)
            // this.moving_store=[]
            this.moving_precentage=100
            
            
            
        }
        
    }
    check_size_to_target(target_size){

        const size_diff=math.abs(target_size-this.size)
        //console.log(target_size,this.size)
        if (size_diff<=this.min_distance_difference && this.size!=target_size){
            this.min_distance_difference=size_diff
        }
        else{
            //this.moving_precentage=100
            this.moving=false
            this.moving_precentage=0
            
            this.finish_moving(...this.moving_parameters)
            this.moving_store=[]
            
            
        }
    }

    get_vector_point(){
        const org_direction=math.matrix([[0],[0],[1]])
        //const xz_rotate=math.multiply(rotateX(this.angle_x),rotateZ(this.angle_z));
        //const xyz_rotate=math.multiply(xy_rotate,rotateZ(this.angle_z));
        
        var pos_rotate=math.multiply(rotateY(-this.angle_z),org_direction);
        
        return pos_rotate.toArray().flat();
    }

    update(){
        //console.log(this.size)
        super.update()
        //console.log(this.size)
        this.check_moving()
        this.check_change_size()
        
        //console.log(this.size)
    }
    moving_by_mouse(mouse_pos,camera){
        
        const limit=0.9;
        const next_pos=camera.similar_tri_reverse_middle(...mouse_pos,this.position[2]);
        const x_diff=-(next_pos[0]-this.position[0])/3;
        const y_diff=(next_pos[1]-this.position[1])/3;
        

        this.angle_y = x_diff > limit ? limit : (x_diff < -limit ? -limit :x_diff);
        this.angle_x = y_diff > limit ? limit : (y_diff < -limit ? -limit :y_diff);

        this.position[0]=next_pos[0]
        this.position[1]=next_pos[1]
        
    }
}


class Card_Hand_Oppo extends Card{
    constructor(width,height,position,size,id,player){
        super(width,height,position,size,[0,1,2,3,4,5],"","")
        this.angle_y=math.pi
        this.player=player
        this.id=id

        this.moving=false;//用来移动卡牌的开关
        this.moving_precentage=0;
        this.moving_dict={
            "move_to":[this.move_to.bind(this),this.move_to_prepared.bind(this),this.move_to_finish.bind(this)],
            "rotate_to_point":[this.rotate_to_point.bind(this),this.rotate_to_point_prepared.bind(this),this.rotate_to_finish.bind(this)],
            "disappear":[this.disappear.bind(this),this.disappear_prepared.bind(this),this.disappear_finish.bind(this)],
            "change_size_animation":[this.change_size_animation.bind(this),this.change_size_animation_prepared.bind(this),this.change_size_animation_finish.bind(this)]
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
        this.TIME_INTERVAL=2
        this.card_hold=[false,false]//click_bool,move_bool

    }

    update(){
        this.arr_poses=this.get_position_points();
        this.check_moving()

        
    }
    draw(camera,ctx,canvas){
        
        const new_points_pos=[];
        
        
        this.final_image=this.back_img;
        
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
                this.draw_half_img_1(new_points_pos_1,[row*this.final_image.width/ROW,col*this.final_image.height/COL],ctx);
                this.draw_half_img_2(new_points_pos_1,[row*this.final_image.width/ROW,col*this.final_image.height/COL],ctx);
                console.log(this.final_image.width,this.final_image.height)
            }
            col_left_up=col_left_down;
            col_right_up=col_right_down;
        }
        this.position_in_screen=new_points_pos;
    }
    change_size(size){
        this.size=size
        this.points=this.get_org_position(this.size);
    }

    check_change_size(){
        if (!(this.change_size_cache===undefined)){
            this.change_size(this.change_size_cache)
            this.change_size_cache=undefined
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
            else {
                this.pick_moving_function()
            }
        }
        else{
            this.moving=false
            this.moving_precentage=0
        }
        
    }

    start_moving(moving_type,parameters){
        //console.log(this.moving,parameters)
        if (this.moving==false && this.moving_precentage<100){
            this.moving_precentage=0;
            this.moving=true
            this.current_moving=this.moving_dict[moving_type][0]
            this.finish_moving=this.moving_dict[moving_type][2]
            
            this.moving_dict[moving_type][1](...parameters)
            
            
            this.moving_parameters=parameters;
            
        }
    }

    pick_moving_function(){//FIFO
        if (this.moving_cache.length){
            
            const para=this.moving_cache.shift()
            
            this.start_moving(...para)
        }
        
    }
    move_to_prepared(target_position){
        
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        this.min_distance_difference=distance;
        const a=math.sqrt(distance*2/math.pi)
        const time_consume=1/distance+2
        
        this.moving_store=[a,unitVector,time_consume,target_position]
        this.check_distance_to_target(target_position)
        //console.log(321)
    }
    move_to(target_position){//target_position[x,y]
        const a=this.moving_store[0];
        const unitVector=this.moving_store[1];
        const time_consume=this.moving_store[2];
        //console.log(time_consume)
        const x=(a*math.pi/100)*this.moving_precentage
        const vel=a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume))/(a*math.pi))
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=this.TIME_INTERVAL*time_consume
        this.check_distance_to_target(target_position)
        //console.log(this.position)
        
    }
    move_to_finish(target_position){
        const final_pos=this.moving_store[3];
        this.position[0]=final_pos[0]
        this.position[1]=final_pos[1]
        this.position[2]=final_pos[2]
        //console.log(123)
        this.pick_moving_function()
        
        
    }
    rotate_to_point_prepared(target_position){//让它指向目标点 x,y,z
        const direction_vector=this.get_vector_point()
        
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        
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
        const angle_change=a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume))/(Math.abs(a)*math.pi))
        this.angle_z=this.angle_z+angle_change
        this.moving_precentage+=this.TIME_INTERVAL*time_consume
        
    }
    rotate_to_finish(target_position){//让它指向目标点
        this.angle_z=this.moving_store[3]
        this.pick_moving_function()
        //console.log(this.angle_x,this.angle_y,this.angle_z)
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
        
        //console.log(this.player, this.player.hand_delete)
        this.player.hand_delete.push(this);
        
        this.move_to_finish(target_position)
    }

    change_size_animation_prepared(size_target){
        //console.log(size_target,this.size)
        const size_diff=math.abs(size_target-this.size)
        const a=math.sqrt(math.abs(size_diff)*2/math.pi)
        const time_consume=1/size_diff+2
        const unit=size_diff/(size_target-this.size)
        this.min_distance_difference=size_diff
        this.moving_store=[a,time_consume,this.size,size_target,unit]
        this.check_size_to_target(size_target)
    }
    change_size_animation(size_target){
        const a=this.moving_store[0];
        const unit=this.moving_store[4]
        const time_consume=this.moving_store[1];
        const org_size=this.moving_store[2];
        //console.log(time_consume)
        
        const x=(a*math.pi/100)*this.moving_precentage
        const dif_size=unit*a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume))/(a*math.pi))
        
        this.change_size(this.size+dif_size)
        //console.log(this.size,dif_size)
        
        this.moving_precentage+=this.TIME_INTERVAL*time_consume
        this.check_size_to_target(size_target)
    }
    change_size_animation_finish(size_target){
        
        this.change_size(this.moving_store[3])
        this.pick_moving_function()
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
            // this.moving=false
            // this.moving_precentage=0
            
            // this.finish_moving(...this.moving_parameters)
            // this.moving_store=[]
            this.moving_precentage=100
            
            
            
        }
        
    }
    check_size_to_target(target_size){

        const size_diff=math.abs(target_size-this.size)
        //console.log(target_size,this.size)
        if (size_diff<=this.min_distance_difference && this.size!=target_size){
            this.min_distance_difference=size_diff
        }
        else{
            //this.moving_precentage=100
            this.moving=false
            this.moving_precentage=0
            
            this.finish_moving(...this.moving_parameters)
            this.moving_store=[]
            
            
        }
    }

    get_vector_point(){
        const org_direction=math.matrix([[0],[0],[1]])
        //const xz_rotate=math.multiply(rotateX(this.angle_x),rotateZ(this.angle_z));
        //const xyz_rotate=math.multiply(xy_rotate,rotateZ(this.angle_z));
        
        var pos_rotate=math.multiply(rotateY(-this.angle_z),org_direction);
        
        return pos_rotate.toArray().flat();
    }
    
}