class SpecialEffects{

    constructor(){
        this.missiles=[]

        this.missiles.push(new Magic_Missile([0,-25,0],"rgba(0, 243, 0, 0.9)"))
    }

    update(camera){
        for (let i in this.missiles){
            this.missiles[i].update(camera)
        }
    }

    draw(camera,ctx,canvas){
        for (let i in this.missiles){
            this.missiles[i].draw(camera,ctx,canvas)
        }
    }


}
class Magic_Missile{
    constructor(position,color){
        this.position=position
        this.arr_poses=NaN;
        this.radius=0.7
        this.points=this.get_org_position()
        this.color=color

        this.particles=[]
        this.max_particle=20

        for (let i=0;i<this.max_particle;i++){
            this,this.create_particle()
        }
        this.delete_particles=[]
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
    // get_matrix_position(matrixA){
        
    //     const matrix_position=math.matrix([[this.position[0]],[this.position[1]],[this.position[2]]])
    //     const matrixExpanded = math.map(matrixA, (value, index, matrix)=> {
    //         return matrix_position.get([index[0], 0]); // Use the row index to access matrixB and repeat its values
    //     });
    //     return matrixExpanded
    // }

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

    update(camera){
        this.position[0]+=0.1
        this.update_particles()

        this.particles= this.particles.filter(item => !(this.delete_particles.includes(item)))
        this.delete_particles=[]


        for (let i=0;i<this.max_particle-this.particles.length;i++){
            this,this.create_particle()
        }
        this.arr_poses=this.get_position_points(camera);

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
        console.log(new_points_pos)
        for (let i_real in new_points_pos){
            
            if(i_real==0){
                const radius=this.calculate_radius(this.radius,camera,this.position)
                this.draw_ball(new_points_pos[0][0], new_points_pos[0][1],this.color,radius,ctx)
            }
            else{
                console.log(this.particles[i_real-1])
                const radius=this.calculate_radius(this.particles[i_real-1].radius,camera,this.particles[i_real-1].position)
                this.draw_ball(new_points_pos[i_real][0], new_points_pos[i_real][1],this.particles[i_real-1].color,radius,ctx)
                
            }
        }
        




    }
    calculate_radius(radius,camera,position){
        const dis=camera.distance_from_point(position)
        const rad=radius*camera.dis_from_screen/dis
        return rad
    }
    draw_ball(x,y,color,radius,ctx){
        ctx.beginPath();
        ctx.arc(x,y, radius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.closePath();
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