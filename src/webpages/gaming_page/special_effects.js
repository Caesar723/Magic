class SpecialEffects{

    constructor(){
        this.particles=[]
        this.missiles=[]
        this.delete_missiles=[]

        //this.missiles.push(new Magic_Missile([0,-25,0],[30,-20,10],"rgba(0, 243, 0, 0.9)"))

        this.types={
            'Missile_Hit':Magic_Missile,
            'Cure':Cure,
            'Arrow':Arrow,
            'High_Missile':High_Missile
        }
    }

    create_missile(object_hold,attacked_obj,color,type,final_state){
        const missile=new this.types[type](object_hold,attacked_obj,color,final_state)
        this.missiles.push(missile)
        return missile
    }



    update(camera){
        
        for (let i in this.missiles){
            this.missiles[i].update(camera,this.delete_missiles)
        }
        this.missiles= this.missiles.filter(item => !(this.delete_missiles.includes(item)))
        this.delete_missiles=[]
        this.arr_poses=this.get_position_points(camera);
    }

    get_all_particles_pos(){
        const arr_x=[];
        const arr_y=[];
        const arr_z=[];
        this.particles=[]
        for (let i in this.missiles){
            this.particles.push(this.missiles[i]);
            this.particles=this.particles.concat(this.missiles[i].particles);
        }
        //console.log(this.missiles,this.particles)
        for (let part_i in this.particles){
            arr_x.push(this.particles[part_i].position[0]);
            arr_y.push(this.particles[part_i].position[1]);
            arr_z.push(this.particles[part_i].position[2]);
            //this.particles[part_i]
        }
        
        return math.matrix([arr_x,arr_y,arr_z,])
    }

    // draw(camera,ctx,canvas){
    //     for (let i in this.missiles){
    //         this.missiles[i].draw(camera,ctx,canvas)
    //     }
    // }


    get_position_points(camera){
        const posiiton_accurate=this.get_all_particles_pos()
        const camera_matrix=camera.get_matrix_position(posiiton_accurate)
        const position_by_camera=math.subtract(posiiton_accurate,camera_matrix);
        const xy_rotate_camera=math.multiply(rotateY(camera.angle_x),rotateX(camera.angle_y));
        const rotated=math.multiply(xy_rotate_camera,position_by_camera);
        //this.matrix_pos=rotated
        var pos_rotate=rotated;
        const final_points=[]
        //console.log(pos_rotate.size())
        for (let col = 0; col <= pos_rotate.size()[1]-1; col++){
            const final_point=[]
            for (let row = 0; row <= 2; row++){
                //console.log(row,col)
                final_point.push(pos_rotate.get([row,col]));
            }
            final_points.push(final_point);
            
        }
        return final_points;
        
    }
    draw(camera,ctx,canvas){
        const new_points_pos=[];

        const new_points_z=[]
        
        
        this.final_image=this.canvas;
        
        //ctx.beginPath();
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;  

        for (let index in this.arr_poses){
            const x_start=this.arr_poses[index][0]
            const y_start=this.arr_poses[index][1]
            const z_start=this.arr_poses[index][2]

            const end_x=cx + camera.similar_tri_2(x_start,z_start)
            const end_y=cy + camera.similar_tri_2(y_start,z_start)
            new_points_pos.push([end_x, end_y])
            new_points_z.push(z_start)
        }
        //console.log(new_points_pos)
        for (let i_real in new_points_pos){
            //console.log(this.particles,i_real)
            if (this.particles[i_real] instanceof Arrow || this.particles[i_real] instanceof Arrow_side){
                this.particles[i_real].draw(new_points_pos[i_real],ctx,canvas,camera)
            }
            else{
                const radius=this.calculate_radius(this.particles[i_real].radius,camera,this.particles[i_real].position)
                this.draw_ball(new_points_pos[i_real][0], new_points_pos[i_real][1],this.particles[i_real].color,radius,ctx)
            }
            
        }
        




    }
    draw_ball(x,y,color,radius,ctx){
        ctx.beginPath();
        ctx.arc(x,y, radius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.closePath();
    }
    calculate_radius(radius,camera,position){
        const dis=camera.distance_from_point(position)
        const rad=radius*camera.dis_from_screen/dis
        return rad
    }


}
class Magic_Missile{
    constructor(object_hold,attacked_obj,color,state_final){
        this.object_hold=object_hold
        this.attacked_obj=attacked_obj
        this.state_final=state_final
        if (object_hold instanceof Player){
            var startpos=object_hold.player_life_ring.position
        }
        else{
            var startpos=object_hold.battle.position
        }

        if (attacked_obj instanceof Player){
            var endpos=attacked_obj.player_life_ring.position
        }
        else{
            var endpos=attacked_obj.battle.position
        }

        //console.log(startpos,endpos)
        this.bezier_points=this.get_bezier_points(startpos,endpos)
        this.percentage=0
        this.position=startpos
        this.arr_poses=NaN;
        this.radius=0.7
        this.points=this.get_org_position()
        this.color=color

        this.particles=[]
        this.max_particle=20

        for (let i=0;i<this.max_particle;i++){
            this.create_particle()
        }
        this.delete_particles=[]

        this.speed=3

        this.disappear=false
        this.transparent=1
    }
    get_bezier_points(position,target_position){
        const new_pos=[
            (position[0]+target_position[0])/2,
            -35,
            (position[2]+target_position[2])/2
        ]
        const arr=[position,new_pos,target_position]
        return arr
    }
    when_hit(){
        if (this.attacked_obj instanceof Player){
            const ring=this.attacked_obj.player_life_ring
            ring.animate_set(this.state_final[0],ring.life)
        }
        else if (this.attacked_obj instanceof Card_Hand){
            this.attacked_obj.battle.mode="none"
            this.attacked_obj.battle.change_state(...this.state_final)
            // Life=state_attacted_obj[1]
            // attacted_obj.Damage=state_attacted_obj[0]
        }
    }

    get_org_position(){//也可能会有很多小particle
        const arr_x=[this.position[0]];
        const arr_y=[this.position[1]];
        const arr_z=[this.position[2]];

        for (const i in this.particles){
            
            arr_x.push(this.particles[i].position[0]);
            arr_y.push(this.particles[i].position[1]);
            arr_z.push(this.particles[i].position[2]);
        }

        return math.matrix([arr_x,arr_y,arr_z,])
        // return math.matrix([
        //     [this.position[0]],
        //     [this.position[1]],
        //     [this.position[2]]
        // ])
    }
    

    update(camera,delete_missiles){

        //this.position[0]+=0.05
        this.percentage+=this.speed*TIME_INTERVAL/2
        if (this.percentage>=100){
            if (this.disappear==false){
                this.disappear=true
                this.when_hit()
            }
            else if(this.particles.length==0 && this.transparent<=0){
                delete_missiles.push(this)
                
            }
            else{
                var parts = this.color.split(",");
                parts[3] = this.transparent+")";
                this.color= parts.join(",");
                this.transparent-=0.1*TIME_INTERVAL/2
                this.percentage=100
            }
            

            
            
        }
        this.update_position(this.bezier_points)
        // this.position[1]-=1.1
        this.update_particles()

        this.particles= this.particles.filter(item => !(this.delete_particles.includes(item)))
        this.delete_particles=[]


        for (let i=0;i<this.max_particle-this.particles.length;i++){
            if (this.disappear==false){
                this.create_particle()
            }
            
            //console.log(1)
        }
        //this.arr_poses=this.get_position_points(camera);

    }
    create_particle(){
        const pos_range=0.7/2//-3,3
        
        const radius_range=0.6
        const color_range=60
        const transparent=0.5

        const position=[
            this.position[0]+Math.random()*pos_range*2-pos_range,
            this.position[1]+Math.random()*pos_range*2-pos_range,
            this.position[2]+Math.random()*pos_range*2-pos_range,
        ]

        const radius=radius_range*Math.random()
        const col=Math.random()*color_range*2-color_range
        let color = this.color.replace(/(\d+(\.\d+)?)/g, function(match, p1, p2, offset, string) {
            if (offset === string.lastIndexOf(',')) {
                return 1; // 增加 0.1，并保留一位小数
            } else {
                //return parseFloat(p1) + 10; // 其他情况增加 10
            
                var new_col= Math.round(parseFloat(p1) + col);
                if (new_col>255){
                    new_col=255
                }
                else if (new_col<0){
                    new_col=0
                }
                return new_col
            }
        });
        
        const particle=new Particle(position,radius,0.5+Math.random()*transparent,color)
        this.particles.push(particle)
    }
    update_particles(){
        for (const i in this.particles){
            this.particles[i].update(this.delete_particles)
        }
    }

    update_position(bezier_points){
        const arr=[]
        
        for (let i=0 ;i<bezier_points.length-1;i++){
            const point=this.Bezier(bezier_points[i],bezier_points[i+1],this.percentage)
            arr.push(point)
            if (bezier_points.length-2==i){
                if (bezier_points.length==2){
                    console.log(point)
                    this.position=point
                }
                else{
                    this.update_position(arr)
                }
            }
        }
    }
    Bezier(point1,point2,percentage){
        const x=point1[0]+percentage*(point2[0]-point1[0])/100
        const y=point1[1]+percentage*(point2[1]-point1[1])/100
        const z=point1[2]+percentage*(point2[2]-point1[2])/100
        return [x,y,z]
    }
    
}

class Particle{
    constructor(position,radius,transparent,color){
        this.transparent=transparent
        this.position=position
        this.radius=radius
        this.color=color

        this.change_transparent()


        //var rgba = "rgba(1,2,3,0.5)";

        // 将 RGBA 值分割成数组
        
        // this.arr_poses=NaN;
        // this.points=this.get_org_position()
    }
    change_transparent(){
        var parts = this.color.split(",");
        parts[3] = this.transparent+")";
        this.color= parts.join(",");
    }

    update(delete_arr){//return whether it disappear
        this.transparent=this.transparent-0.01*TIME_INTERVAL
        this.radius=this.radius-0.01*TIME_INTERVAL
        if (this.radius<0 || this.transparent<0){
            delete_arr.push(this)
        }
        this.change_transparent()

    }
    draw(){

        
    }
}



class Cure extends Magic_Missile{
    constructor(object_hold,attacked_obj,color,state_final){
        super(object_hold,attacked_obj,color,state_final)
        this.speed=1
    }
    get_bezier_points(position,target_position){
        const new_pos_1=[
            (position[0]+target_position[0])/2+10,
            -20,
            (position[2]+target_position[2])/2
        ]
        const new_pos_2=[
            (position[0]+target_position[0])/2-10,
            -30,
            (position[2]+target_position[2])/2
        ]
        const arr=[position,new_pos_1,new_pos_2,target_position]
        return arr
    }
}
class High_Missile extends Magic_Missile{
    constructor(object_hold,attacked_obj,color,state_final){
        super(object_hold,attacked_obj,color,state_final)
        this.speed=3
    }
    get_bezier_points(position,target_position){
        const new_pos_1=[
            position[0]+(target_position[0]-position[0])/4,
            -40,
            position[2]+(target_position[2]-position[2])/4
        ]
        
        const arr=[position,new_pos_1,target_position]
        return arr
    }
}

class Arrow extends Magic_Missile{
    constructor(object_hold,attacked_obj){
        super(object_hold,attacked_obj,'rgba(253,197,84,0.8)',"")
        this.speed=3
        this.particles=[new Arrow_side(this.position,this),new Arrow_side(this.position,this)]
        this.position_list_orginal=[]//原始位置
        this.position_list=[]//实际位置

        this.preview_position=this.bezier_points[0].slice();
        this.preview_position[1]+=1
        this.direction_vector=this.initinal_direction_vector()
    }
    get_org_position(){//也可能会有很多小particle
        const arr_x=[]
        const arr_y=[]
        const arr_z=[]

        for (const i in this.position_list_orginal){
            
            arr_x.push(this.position_list_orginal[i][0]);
            arr_y.push(this.position_list_orginal[i][1]);
            arr_z.push(this.position_list_orginal[i][2]);
        }

        return math.matrix([arr_x,arr_y,arr_z])
        
    }
    get_bezier_points(position,target_position){
        const new_pos=[
            (position[0]+target_position[0])/2,
            -45,
            (position[2]+target_position[2])/2
        ]
        const arr=[position,new_pos,target_position]
        return arr
    }
    update(camera,delete_missiles){

        //this.position[0]+=0.05
        this.percentage+=this.speed*TIME_INTERVAL/2
        if (this.percentage>=100){
            if (this.disappear==false){
                this.disappear=true
                this.when_hit()
            }
            else if(this.position_list_orginal.length<=0 ){
                delete_missiles.push(this)
                //console.log(1)
                //this.particles=[]
                
            }
            else{

                this.position_list_orginal.shift()
                this.percentage=100
            }
            this.update_particles()
            this.update_position(this.bezier_points)
            this.arr_poses=this.get_position_points(camera)
        }
        else{
            this.update_particles()
            this.preview_position=this.position
            this.position_list_orginal.push(this.position.slice())
            this.update_position(this.bezier_points)

            this.arr_poses=this.get_position_points(camera)
        }
        

        

    }
    get_position_points(camera){
        const posiiton_accurate=this.get_org_position()
        const camera_matrix=camera.get_matrix_position(posiiton_accurate)
        const position_by_camera=math.subtract(posiiton_accurate,camera_matrix);
        const xy_rotate_camera=math.multiply(rotateY(camera.angle_x),rotateX(camera.angle_y));
        const rotated=math.multiply(xy_rotate_camera,position_by_camera);
        //this.matrix_pos=rotated
        var pos_rotate=rotated;
        const final_points=[]
        //console.log(pos_rotate.size())
        for (let col = 0; col <= pos_rotate.size()[1]-1; col++){
            const final_point=[]
            for (let row = 0; row <= 2; row++){
                //console.log(row,col)
                final_point.push(pos_rotate.get([row,col]));
            }
            final_points.push(final_point);
            
        }
        return final_points;
        
    }
    when_hit(){
       
    }
    initinal_direction_vector(){
        const direction_forward=[
            this.bezier_points[this.bezier_points.length-1][0]-this.bezier_points[0][0],
            this.bezier_points[this.bezier_points.length-1][1]-this.bezier_points[0][1],
            this.bezier_points[this.bezier_points.length-1][2]-this.bezier_points[0][2]
        ]
        const direction_upward=[
            0,-1,0
        ]
        const unitvector=math.cross(direction_forward, direction_upward);
        return math.divide(unitvector, math.norm(unitvector));
    }
    update_particles(){
        const height=2;
        const width=2;
        const new_direction=[
            this.position[0]-this.preview_position[0],
            this.position[1]-this.preview_position[1],
            this.position[2]-this.preview_position[2]
        ]
        const unit_vector=math.divide(new_direction, math.norm(new_direction));
        const point1=math.subtract(this.position, math.multiply(height, unit_vector));

        const side1=math.add(point1,math.multiply(width, this.direction_vector));
        const side2=math.add(point1,math.multiply(-width, this.direction_vector));
        this.particles[0].position=side1
        this.particles[1].position=side2

    }
    draw(position,ctx,canvas,camera){
        const new_points_pos=[];

        const cx = canvas.width / 2;
        const cy = canvas.height / 2;  

        for (let index in this.arr_poses){
            const x_start=this.arr_poses[index][0]
            const y_start=this.arr_poses[index][1]
            const z_start=this.arr_poses[index][2]

            const end_x=cx + camera.similar_tri_2(x_start,z_start)
            const end_y=cy + camera.similar_tri_2(y_start,z_start)
            new_points_pos.push([end_x, end_y])
            
        }
        this.position_list=new_points_pos
        this.position_list.push(position)

        ctx.shadowColor = 'rgba(253,197,84,1)';  // 光晕颜色
        ctx.shadowBlur = 20;                       // 光晕模糊度
        ctx.shadowOffsetX = 0;                     // 光晕水平偏移
        ctx.shadowOffsetY = 0;   

        ctx.beginPath();
        ctx.moveTo(this.position_list[0][0] ,this.position_list[0][1]);
        for (let i in this.position_list){
            if (i!=0){
                ctx.lineTo(this.position_list[i][0], this.position_list[i][1]);
            }
        }
        ctx.stroke();

        ctx.shadowColor = 'rgba(0,0,0,0)';  // 光晕颜色
        ctx.shadowBlur = 0;                       // 光晕模糊度
        ctx.shadowOffsetX = 0;                     // 光晕水平偏移
        ctx.shadowOffsetY = 0;  
    }
}

class Arrow_side {
    constructor(position,arrow){
        this.arrow=arrow
        this.position=position
        
    }
    update(delete_arr){//return whether it disappear
        

    }
    draw(position,ctx,canvas,camera){
        ctx.shadowColor = 'rgba(253,197,84,1)';  // 光晕颜色
        ctx.shadowBlur = 20;                       // 光晕模糊度
        ctx.shadowOffsetX = 0;                     // 光晕水平偏移
        ctx.shadowOffsetY = 0;   
        
        ctx.beginPath();
        ctx.moveTo(...position);
        ctx.lineTo(...this.arrow.position_list[this.arrow.position_list.length-1]);
        ctx.strokeStyle =  'rgba(253,197,84,0.5)'; // 线条颜色
        ctx.lineWidth = 8; // 线条宽度
        ctx.stroke();
        ctx.shadowColor = 'rgba(0,0,0,0)';  // 光晕颜色
        ctx.shadowBlur = 0;                       // 光晕模糊度
        ctx.shadowOffsetX = 0;                     // 光晕水平偏移
        ctx.shadowOffsetY = 0;   
        
    }
}

