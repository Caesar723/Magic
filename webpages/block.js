const WIDTH=0.4;//x
const HEIGHT=0.562;//y
const LENGTH=0.05;//z
const corners=[//x y z
    [1*WIDTH,1*HEIGHT,1*LENGTH],
    [1*WIDTH,1*HEIGHT,-1*LENGTH],
    [1*WIDTH,-1*HEIGHT,1*LENGTH],
    [1*WIDTH,-1*HEIGHT,-1*LENGTH],
    [-1*WIDTH,1*HEIGHT,1*LENGTH],
    [-1*WIDTH,1*HEIGHT,-1*LENGTH],
    [-1*WIDTH,-1*HEIGHT,1*LENGTH],
    [-1*WIDTH,-1*HEIGHT,-1*LENGTH],

];
const connect_index=[
    [0,1],
    [2,3],
    [4,5],
    [6,7],
    [0,2],
    [1,3],
    [4,6],
    [5,7],
    [0,4],
    [1,5],
    [2,6],
    [3,7]
]
const plane_indexs=[
    [2,3,1,0],
    [4,5,7,6],
    [0,1,5,4],
    [6,7,3,2],
    [4,6,2,0],
    [1,3,7,5],
]

class Block{

    constructor(position,size){//position =[x,y,z]
        this.position=position;
        this.angle_x=0;
        this.angle_y=0;
        this.angle_z=0;
        this.vel_x=0;
        this.vel_y=0;
        this.vel_z=0;
        this.points=this.get_org_position(size);
        this.arr_poses=NaN;
        this.planes=this.set_plane()
        
        
    }

    get_org_position(size){
        const arr_x=[];
        const arr_y=[];
        const arr_z=[];

        for (const i in corners){
            
            arr_x.push(corners[i][0]*size);
            arr_y.push(corners[i][1]*size);
            arr_z.push(corners[i][2]*size);
        }

        return math.matrix([arr_x,arr_y,arr_z,])
    }

    get_position_points(){
        const xy_rotate=math.multiply(rotateX(this.angle_x),rotateY(this.angle_y));
        const xyz_rotate=math.multiply(xy_rotate,rotateZ(this.angle_z));
        
        const pos_rotate=math.multiply(xyz_rotate,this.points);

        const final_points=[]
        for (let col = 0; col <= corners.length-1; col++){
            const final_point=[]
            for (let row = 0; row <= 2; row++){
                
                final_point.push(pos_rotate.get([row,col])+this.position[row]);
            }
            final_points.push(final_point);
            
        }
        return final_points;

    }

    set_plane(){
        const planes=[];
        for (const plane_index in plane_indexs){
            const plane=new Plane(plane_indexs[plane_index]);
            planes.push(plane);
        }
        return planes;
    }

    update(){
        
        this.arr_poses=this.get_position_points();
        for (const plane_index in this.planes){
            this.planes[plane_index].arr=this.arr_poses;
        
        }
    }

    draw(camera){

        this.planes.sort(function(a,b){
            const b_mid=b.mid_point();
            const a_mid=a.mid_point()
            const b_dis=Math.sqrt((camera.position[0]-b_mid[0])**2 + (camera.position[1]-b_mid[1])**2+ (camera.position[2]-b_mid[2])**2) 
            const a_dis=Math.sqrt((camera.position[0]-a_mid[0])**2 + (camera.position[1]-a_mid[1])**2+ (camera.position[2]-a_mid[2])**2) 
            return b_dis-a_dis;
        })
        for (const plane_index in this.planes){
            this.planes[plane_index].draw(camera,this.arr_poses);
        }
        // const cx = canvas.width / 2;
        // const cy = canvas.height / 2;           
        
        
        // for (const points_index in connect_index){
            
        //     const x_start=this.arr_poses[connect_index[points_index][0]][0]
        //     const y_start=this.arr_poses[connect_index[points_index][0]][1]
        //     const z_start=this.arr_poses[connect_index[points_index][0]][2]
        //     const x_end=this.arr_poses[connect_index[points_index][1]][0]
        //     const y_end=this.arr_poses[connect_index[points_index][1]][1]
        //     const z_end=this.arr_poses[connect_index[points_index][1]][2]
        //     ctx.beginPath();
        //     ctx.moveTo(cx + camera.similar_tri(x_start,z_start), cy + camera.similar_tri(y_start,z_start));
        //     ctx.lineTo(cx + camera.similar_tri(x_end,z_end), cy + camera.similar_tri(y_end,z_end));
        //     ctx.stroke();
            

        // }
        
        
    }
}

class Plane{

    constructor(indexs){
        this.indexs_plane=indexs;
        this.arr=NaN;

    }

    get_point(index){
        return [this.arr[index][0],this.arr[index][1],this.arr[index][2]];
    }

    normal_vector(){
        const vec1=[this.arr[this.indexs_plane[1]][0]-this.arr[this.indexs_plane[3]][0],this.arr[this.indexs_plane[1]][1]-this.arr[this.indexs_plane[3]][1],this.arr[this.indexs_plane[1]][2]-this.arr[this.indexs_plane[3]][2]];
        const vec2=[this.arr[this.indexs_plane[0]][0]-this.arr[this.indexs_plane[2]][0],this.arr[this.indexs_plane[0]][1]-this.arr[this.indexs_plane[2]][1],this.arr[this.indexs_plane[0]][2]-this.arr[this.indexs_plane[2]][2]];
        const vec_normal=(math.cross(vec1,vec2));
        return vec_normal;
    }

    mid_point(){
        const mid_p=[(this.arr[this.indexs_plane[1]][0]+this.arr[this.indexs_plane[3]][0])/2,(this.arr[this.indexs_plane[1]][1]+this.arr[this.indexs_plane[3]][1])/2,(this.arr[this.indexs_plane[1]][2]+this.arr[this.indexs_plane[3]][2])/2];
        return mid_p;
    }

    angle_from_cam(camera){
        const vectorA=this.normal_vector()
        const vectorB=camera.get_vector()
        const dot = math.dot(vectorA, vectorB);
        

        // Calculate the magnitude (norm) of each vector
        const normA = math.norm(vectorA);
        const normB = math.norm(vectorB);

        // Calculate the cosine of the angle using the dot product and magnitudes
        const cosTheta = dot / (normA * normB);
        // Use the acos function to find the angle in radians and then convert to degrees
        const angleRadians = math.acos(cosTheta);
        
        const angleDegrees = angleRadians * (180 / math.PI);

        return angleDegrees;
    }

    most_close_far_points(){
        const arr_indexs=[];
        for (const i in this.indexs_plane){
            arr_indexs.push([i,this.arr[this.indexs_plane[i]]]);
        }
        arr_indexs.sort(function(a,b){
            return a[1][2]-b[1][2];
        });
        
        return [arr_indexs[0],arr_indexs[3]]//max, min color


    }

    light_bright(pos_z){
        const new_pos=pos_z-POSITION[2];
        const max=(((SIZE*((2)**0.5))**2+SIZE**2)**0.5)*2;
        const min=-(((SIZE*((2)**0.5))**2+SIZE**2)**0.5);
        const diff=new_pos-min;
        const light=255-255*(diff/max);
        
        return light;
    }

    bright_min(max_light,light_middle){
        
        return light_middle-(max_light-light_middle)
    }
    draw(camera){
        const angle=this.angle_from_cam(camera);
        const light=(100-255*angle/360).toString();
        const new_points_pos=[];
        
        
        
        ctx.beginPath();
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;       
        for (const index_plane in this.indexs_plane){
            const x_start=this.arr[this.indexs_plane[index_plane]][0]
            const y_start=this.arr[this.indexs_plane[index_plane]][1]
            const z_start=this.arr[this.indexs_plane[index_plane]][2]

            const end_x=cx + camera.similar_tri(x_start,z_start)
            const end_y=cy + camera.similar_tri(y_start,z_start)
            if (index_plane==0) {
                ctx.moveTo(end_x, end_y); 
            }
            else{
                ctx.lineTo(end_x, end_y);    
            }
            new_points_pos.push([end_x, end_y])
        }
        ctx.closePath();  

        const max_min_points=this.most_close_far_points();
        
        var gradient = ctx.createLinearGradient(...new_points_pos[max_min_points[0][0]], ...new_points_pos[max_min_points[1][0]]);
        
        const light_max=this.light_bright(max_min_points[0][1][2]);
        const light_min=this.light_bright(max_min_points[1][1][2]);
        
        gradient.addColorStop(0, "rgb("+light+","+light+","+light+",1)");
        gradient.addColorStop(1, "rgb("+light+","+light+","+light+",1)");
        ctx.fillStyle = gradient;
        ctx.fill();
    }
}


//## Camera##//

class Camera{

    constructor(position){
        this.vector_x=0
        this.vector_y=0
        this.vector_z=1

        this.position=position

        this.dis_from_screen=900
    }

    get_vector(){
        return [this.vector_x,this.vector_y,this.vector_z]
    }

    set_vector(x,y,z){
        this.vector_x=x
        this.vector_y=y
        this.vector_z=z
    }

    similar_tri(x_or_y,z){
        return x_or_y*(this.dis_from_screen/(z-this.position[2]))
    }

    similar_tri_reverse(x_screen,y_screen,z_expect){
        return [x_screen*(z_expect-this.position[2])/this.dis_from_screen,y_screen*(z_expect-this.position[2])/this.dis_from_screen]
    }


}