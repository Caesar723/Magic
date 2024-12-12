


class Pack extends Block{
    constructor(position, size,img_path,name,id,name_id) {
        super(position, size); // 调用基类的构造函数
        this.image = new Image();
        this.image.src=img_path;
        
        console.log(this.image);
        this.surface=NaN;
        this.planes=this.set_plane();

        this.name=name;
        this.name_id=name_id;
        this.id=id;
        
    }
    set_plane(){
        const planes=[];
        for (const plane_index in plane_indexs){
            
            if (plane_index==5){
                const plane=new Pack_surface(plane_indexs[plane_index],this.image);
                
                planes.push(plane);
                this.surface=plane;
                
            }
            else{
                const plane=new Plane(plane_indexs[plane_index]);
                planes.push(plane);
            }
            
            
        }
        return planes;
    }
    get_position_in_screen(){
        return this.surface.position_in_screen;
    }
    moving_by_mouse(mouse_pos,camera){
        
        const limit=0.4;
        const next_pos=camera.similar_tri_reverse(...mouse_pos,this.position[2])
        const x_diff=-(next_pos[0]-this.position[0])/100;
        const y_diff=(next_pos[1]-this.position[1])/100;
        

        this.angle_y = x_diff > limit ? limit : (x_diff < -limit ? -limit :x_diff);
        this.angle_x = y_diff > limit ? limit : (y_diff < -limit ? -limit :y_diff);

        this.position[0]=next_pos[0]
        this.position[1]=next_pos[1]
    }
    

}

class Pack_surface extends Plane{
    constructor(indexs,image){
        super(indexs);
        this.image=image;
        this.position_in_screen=[[0,0],[0,0],[0,0],[0,0]]
        

    }
    extendVert(x0, y0, x1, y1, x2, y2) {
        const DRAW_IMAGE_EXTEND_EX = 10000;
        var x = 2*x0 - x1 - x2, y = 2 * y0 - y1 - y2;
        var d = Math.sqrt(DRAW_IMAGE_EXTEND_EX / (x * x + y * y));
        return [x0 + x * d, y0 + y * d];
    }
    draw_half_img_1(points_pos,new_points_pos,ctx,canvas){
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.save();
        ctx.beginPath();
        const p1=this.extendVert(points_pos[0][0], points_pos[0][1],points_pos[2][0], points_pos[2][1],points_pos[3][0], points_pos[3][1])
        //console.log(p1,[points_pos[0][0], points_pos[0][1]])
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
    draw_half_img_2(points_pos,new_points_pos,ctx,canvas){
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.save();
        ctx.beginPath();
        const p1=this.extendVert(points_pos[0][0], points_pos[0][1],points_pos[1][0], points_pos[1][1],points_pos[2][0], points_pos[2][1])
        const p2=this.extendVert(points_pos[1][0], points_pos[1][1],points_pos[0][0], points_pos[0][1],points_pos[2][0], points_pos[2][1])
        const p3=this.extendVert(points_pos[2][0], points_pos[2][1],points_pos[1][0], points_pos[1][1],points_pos[0][0], points_pos[0][1])
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
    draw(camera,ctx,canvas){
        
        const new_points_pos=[];
        
        
        //ctx.beginPath();
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;       
        for (const index_plane in this.indexs_plane){
            const x_start=this.arr[this.indexs_plane[index_plane]][0]
            const y_start=this.arr[this.indexs_plane[index_plane]][1]
            const z_start=this.arr[this.indexs_plane[index_plane]][2]

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
                this.draw_half_img_1(new_points_pos_1,[row*this.image.width/ROW,col*this.image.height/COL],ctx,canvas);
                this.draw_half_img_2(new_points_pos_1,[row*this.image.width/ROW,col*this.image.height/COL],ctx,canvas);
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
}




