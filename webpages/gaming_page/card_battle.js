

class Card_Battle{
    constructor(width,height,position,size,card){
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

        this.image=card.dynamic_canvas[4]
       
        this.id=card.id;

        this.canvas=document.createElement('canvas');
        this.back_img=new Image();
        this.back_img.src="webpages/image_source/card/back.png";
        this.canvas.width=80*10
        this.canvas.height=60*10
        this.ctx=this.canvas.getContext('2d')
        
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
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.save()
        this.ctx.drawImage(this.image,0,0,this.canvas.width,this.canvas.height);
        this.ctx.restore()
        //this.create_fee(this.dynamic_canvas[1],this.color_fee,...Array.from({length: 6}, (_, i) => this.images_fee[i]));
        
        this.arr_poses=this.get_position_points(camera);

        
        
        
    }
    draw(camera,ctx,canvas){
        
        const new_points_pos=[];
        
        
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


}