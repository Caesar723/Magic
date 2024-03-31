

class Table_graph extends Block{
    constructor(WIDTH,HEIGHT,LENGTH,position, size,img_path) {
        super(position, size); // 调用基类的构造函数

        this.image = new Image();
        this.image.src=img_path;
        
        console.log(this.image);
        this.surface=NaN;
        this.planes=this.set_plane();

        this.corners=[//x y z
            [1*WIDTH,1*HEIGHT,1*LENGTH],
            [1*WIDTH,1*HEIGHT,-1*LENGTH],
            [1*WIDTH,-1*HEIGHT,1*LENGTH],
            [1*WIDTH,-1*HEIGHT,-1*LENGTH],
            [-1*WIDTH,1*HEIGHT,1*LENGTH],
            [-1*WIDTH,1*HEIGHT,-1*LENGTH],
            [-1*WIDTH,-1*HEIGHT,1*LENGTH],
            [-1*WIDTH,-1*HEIGHT,-1*LENGTH],

        ];
        this.points=this.get_org_position(size);

        

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
    update(camera){
        
        this.arr_poses=this.get_position_points(camera);
        for (const plane_index in this.planes){
            this.planes[plane_index].arr=this.arr_poses;
        
        }
    }
    set_plane(){
        const planes=[];
        for (const plane_index in plane_indexs){
            
            if (plane_index==3){
                const plane=new Table_surface(plane_indexs[plane_index],this.image);
                
                planes.push(plane);
                this.surface=plane;
                
            }
            // else{
            //     const plane=new Table_side(plane_indexs[plane_index]);
            //     planes.push(plane);
            // }
            
            
        }
        return planes;
    }
    get_position_in_screen(){
        return this.surface.position_in_screen;
    }
    draw(camera,canvas,ctx){
        this.planes.sort(function(a,b){
            const b_mid=b.mid_point();
            const a_mid=a.mid_point()
            
            const b_dis=Math.sqrt((camera.position[0]-b_mid[0])**2 + (camera.position[1]+b_mid[1])**2+ (camera.position[2]-b_mid[2])**2) 
            const a_dis=Math.sqrt((camera.position[0]-a_mid[0])**2 + (camera.position[1]+a_mid[1])**2+ (camera.position[2]-a_mid[2])**2) 
            
            return b_dis-a_dis;
        })
        
        for (const plane_index in this.planes){
            this.planes[plane_index].draw(camera,canvas,ctx);
        }
    }
    get_matrix_position(matrixA){
        
        const matrix_position=math.matrix([[this.position[0]],[this.position[1]],[this.position[2]]])
        const matrixExpanded = math.map(matrixA, (value, index, matrix)=> {
            return matrix_position.get([index[0], 0]); // Use the row index to access matrixB and repeat its values
        });
        return matrixExpanded
    }
}


class Table_side extends Plane{
    draw(camera,canvas,ctx){
        
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

            const end_x=cx + camera.similar_tri_2(x_start,z_start)
            const end_y=cy + camera.similar_tri_2(y_start,z_start)
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
class Table_surface extends Plane{
    constructor(indexs,image){
        super(indexs);
        this.image=image;
        this.position_in_screen=[[0,0],[0,0],[0,0],[0,0]]
        

    }
    draw_half_img_1(points_pos,new_points_pos,ctx){
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.save();
        ctx.beginPath();
        const p1=this.extendVert(points_pos[0][0], points_pos[0][1],points_pos[3][0], points_pos[3][1],points_pos[2][0], points_pos[2][1])
        const p2=this.extendVert(points_pos[3][0], points_pos[3][1],points_pos[0][0], points_pos[0][1],points_pos[2][0], points_pos[2][1])
        const p3=this.extendVert(points_pos[2][0], points_pos[2][1],points_pos[0][0], points_pos[0][1],points_pos[3][0], points_pos[3][1])
        ctx.moveTo(...p1); // 右下角
        ctx.lineTo(...p2); // 左下角
        ctx.lineTo(...p3); // 左上角
        //ctx.lineTo(points_pos[1][0], points_pos[1][1]);
        ctx.closePath();
        ctx.clip();
        ctx.setTransform(
            (points_pos[0][0] - points_pos[3][0]) / this.image.width,
            (points_pos[0][1] - points_pos[3][1]) / this.image.width,
            (points_pos[3][0] - points_pos[2][0]) / (this.image.height),
            (points_pos[3][1] - points_pos[2][1]) / (this.image.height),
            points_pos[2][0],
            points_pos[2][1]
        );
        ctx.drawImage(this.image,new_points_pos[0], new_points_pos[1], this.image.width/4, this.image.height/4, 0,0, this.image.width, this.image.height);
        //ctx.drawImage(this.image, 0, 0, this.image.width, this.image.height/4);
        ctx.restore();
    }
    draw_half_img_2(points_pos,new_points_pos,ctx){
        
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.save();
        ctx.beginPath();
        const p1=this.extendVert(points_pos[0][0], points_pos[0][1],points_pos[1][0], points_pos[1][1],points_pos[2][0], points_pos[2][1])
        const p2=this.extendVert(points_pos[1][0], points_pos[1][1],points_pos[0][0], points_pos[0][1],points_pos[2][0], points_pos[2][1])
        const p3=this.extendVert(points_pos[2][0], points_pos[2][1],points_pos[0][0], points_pos[0][1],points_pos[1][0], points_pos[1][1])
        ctx.moveTo(...p1); // 右下角
        ctx.lineTo(...p2); // 左下角
        ctx.lineTo(...p3); // 左上角
        // ctx.moveTo(points_pos[2][0], points_pos[2][1]); // 左上角
        // ctx.lineTo(points_pos[1][0], points_pos[1][1]); // 右上角
        // ctx.lineTo(points_pos[0][0], points_pos[0][1]); // 右下角
        
        ctx.closePath();
        ctx.clip();
        ctx.setTransform(
            (points_pos[1][0] - points_pos[2][0]) / this.image.width,
            (points_pos[1][1] - points_pos[2][1]) / this.image.width,
            (points_pos[0][0] - points_pos[1][0]) / this.image.height,
            (points_pos[0][1] - points_pos[1][1]) / this.image.height,
            points_pos[2][0],
            points_pos[2][1]
        );
        ctx.drawImage(this.image,new_points_pos[0], new_points_pos[1], this.image.width/4, this.image.height/4, 0,0, this.image.width, this.image.height);
        //ctx.drawImage(this.image, 0, 0, this.image.width, this.image.height);
        ctx.restore();
    }
    draw(camera,canvas,ctx){
        
        
        const new_points_pos=[];
        
        
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;       
        for (const index_plane in this.indexs_plane){
            const x_start=this.arr[this.indexs_plane[index_plane]][0]
            const y_start=this.arr[this.indexs_plane[index_plane]][1]
            const z_start=this.arr[this.indexs_plane[index_plane]][2]


            new_points_pos.push([x_start, y_start,z_start])
        }


        const COL=4;
        const ROW=4;

        let col_left_up=this.average_3D(new_points_pos[2],new_points_pos[3],COL-0,COL);
        let col_right_up=this.average_3D(new_points_pos[1],new_points_pos[0],COL-0,COL);
        
        for (let col=0;col<COL;col++){
            let col_left_down=this.average_3D(new_points_pos[2],new_points_pos[3],COL-col-1,COL);
            let col_right_down=this.average_3D(new_points_pos[1],new_points_pos[0],COL-col-1,COL);

            
            
            for (let row=0;row<ROW;row++){

                const point1=this.average_3D(col_left_down,col_right_down,ROW-row-1,ROW)
                const point2=this.average_3D(col_left_up,col_right_up,ROW-row-1,ROW)
                const point3=this.average_3D(col_left_up,col_right_up,ROW-row,ROW)
                const point4=this.average_3D(col_left_down,col_right_down,ROW-row,ROW)
                const new_points_pos_1=[
                    [cx + camera.similar_tri_2(point1[0],point1[2]),cy + camera.similar_tri_2(point1[1],point1[2])],
                    [cx + camera.similar_tri_2(point2[0],point2[2]),cy + camera.similar_tri_2(point2[1],point2[2])],
                    [cx + camera.similar_tri_2(point3[0],point3[2]),cy + camera.similar_tri_2(point3[1],point3[2])], 
                    [cx + camera.similar_tri_2(point4[0],point4[2]),cy + camera.similar_tri_2(point4[1],point4[2])], 
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

    average_3D(p_1,p_2,n,t){
        const x=p_2[0]+n*(p_1[0]-p_2[0])/t
        const y=p_2[1]+n*(p_1[1]-p_2[1])/t
        const z=p_2[2]+n*(p_1[2]-p_2[2])/t

        return [x,y,z]
    }

    extendVert(x0, y0, x1, y1, x2, y2) {
        const DRAW_IMAGE_EXTEND_EX = 3;
        var x = 2*x0 - x1 - x2, y = 2 * y0 - y1 - y2;
        var d = 30*Math.sqrt(DRAW_IMAGE_EXTEND_EX / (x * x + y * y));
        return [x0 + x * d, y0 + y * d];
    }
}




class Deck_battle extends Table_graph{
    constructor(WIDTH,HEIGHT,LENGTH,position, size,img_path){
        super(WIDTH,HEIGHT,LENGTH,position, size,img_path)
        this.height=HEIGHT
        this.number_of_cards=70
    }
    set_height_position(){
        this.height=this.number_of_cards*2/70
        this.position[1]=-(20+this.height*this.size)
        //console.log(this.position[1],this.size,this.height)
    }
    set_plane(){
        const planes=[];
        for (const plane_index in plane_indexs){
            
            if (plane_index==3){
                const plane=new Table_surface(plane_indexs[plane_index],this.image);
                
                planes.push(plane);
                this.surface=plane;
                
            }
            else{
                const plane=new Table_side(plane_indexs[plane_index]);
                planes.push(plane);
            }
        }
        return planes;
    }
    change_height(height){
        const arr_unit=[1,1,-1,-1,1,1,-1,-1]
        for (let i in arr_unit){
            this.corners[i][1]=arr_unit[i]*height
        }
        this.points=this.get_org_position(this.size);
    }
    update(camera){
        super.update(camera)
        this.set_height_position()
        this.change_height(this.height)
    }
}




