

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

        this._half_width = width;
        this._half_height = height;
        this._three_card = null;
        this._three_card_initialized = false;
        this._three_shadow = null;
        this._three_select_ring = null;

        // Performance: only re-bake the battle canvas (and re-upload the
        // texture) when something visual actually changes. The CSS filter
        // applied here only depends on `activated` and the presence of a
        // "frozen" buff, so we cache that signature.
        this._battle_baked = false;
        this._battle_buff_sig = null;
        this._three_needs_upload = false;
    }
    _ensureThreeCard(){
        if (this._three_card_initialized) return;
        if (!window.THREE_STAGE) return;
        // Lying-flat battle cards never reveal their back, and the table
        // camera may end up on either side of the plane normal depending on
        // perspective. Use a single double-sided mesh so the front-face
        // canvas is always shown.
        this._three_card = new CardPlane(
            window.THREE_STAGE,
            this._half_width,
            this._half_height,
            this.canvas,
            this.back_img,
            { flat: true }
        );
        this._three_card.setRenderOrder(1);
        this._three_shadow = new ShadowQuad(window.THREE_STAGE);
        this._three_initialized = true;
        this._three_card_initialized = true;
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
        // Hand-rolled equivalent of:
        //   R    = Rx(ax) * Ry(ay) * Rz(az)
        //   posW = R * (corner * size) + position
        //   posC = Ry(cam.angle_x) * Rx(cam.angle_y) * (posW - cam.position)
        // Replaces ~7 mathjs matrix multiplies/frame/card. Same result as
        // the legacy version but ~10x faster (mathjs allocates a Matrix
        // object for every multiply, which is the dominant CPU cost when
        // there are many battle cards on the field).
        const ax = this.angle_x, ay = this.angle_y, az = this.angle_z;
        const cx = Math.cos(ax), sx = Math.sin(ax);
        const cy = Math.cos(ay), sy = Math.sin(ay);
        const cz = Math.cos(az), sz = Math.sin(az);
        // Rx*Ry
        const m00 = cy,        m01 = 0,    m02 = sy;
        const m10 = sx * sy,   m11 = cx,   m12 = -sx * cy;
        const m20 = -cx * sy,  m21 = sx,   m22 = cx * cy;
        // R = (Rx*Ry)*Rz
        const r00 = m00 * cz + m01 * sz, r01 = -m00 * sz + m01 * cz, r02 = m02;
        const r10 = m10 * cz + m11 * sz, r11 = -m10 * sz + m11 * cz, r12 = m12;
        const r20 = m20 * cz + m21 * sz, r21 = -m20 * sz + m21 * cz, r22 = m22;

        // Camera rotation: C = Ry(cam.angle_x) * Rx(cam.angle_y)
        const cax = camera.angle_x, cay = camera.angle_y;
        const ccax = Math.cos(cax), scax = Math.sin(cax);
        const ccay = Math.cos(cay), scay = Math.sin(cay);
        const c00 = ccax,  c01 = scax * scay,  c02 = scax * ccay;
        const c10 = 0,     c11 = ccay,         c12 = -scay;
        const c20 = -scax, c21 = ccax * scay,  c22 = ccax * ccay;

        const s = this.size;
        const px = this.position[0], py = this.position[1], pz = this.position[2];
        const cpx = camera.position[0], cpy = camera.position[1], cpz = camera.position[2];
        const corners = this.corners;
        const final_points = [];
        for (let i = 0; i < corners.length; i++){
            const lx = corners[i][0] * s;
            const ly = corners[i][1] * s;
            const lz = corners[i][2] * s;
            // R * v
            const wx = r00 * lx + r01 * ly + r02 * lz;
            const wy = r10 * lx + r11 * ly + r12 * lz;
            const wz = r20 * lx + r21 * ly + r22 * lz;
            // (R*v + pos) - cam.pos
            const ex = wx + px - cpx;
            const ey = wy + py - cpy;
            const ez = wz + pz - cpz;
            // C * (...)
            final_points.push([
                c00 * ex + c01 * ey + c02 * ez,
                c10 * ex + c11 * ey + c12 * ez,
                c20 * ex + c21 * ey + c22 * ez,
            ]);
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
    // Subclasses (e.g. Creature_Battle) override these two to layer extra
    // content on top of the baked battle face (life/damage text, etc.).
    // See the matching hooks on `Card` for the full pattern.
    get_visual_signature(){
        const frozen = (this.buff_list && this.buff_list.some && this.buff_list.some(b => b && b.content == "frozen"));
        return (this.activated ? "A" : "_") + (frozen ? "F" : "_");
    }
    draw_extra_overlay(ctx){ /* no-op for plain battle cards */ }

    update(camera){
        this.check_moving()

        // Re-bake the battle canvas only when its visible state actually
        // changed. The base material depends on `activated` and the
        // "frozen" buff; subclasses extend the signature with their own
        // dynamic content (life/damage). Skipping the redundant
        // clearRect+drawImage saves substantial CPU + GPU upload bandwidth
        // when many cards are on the field.
        if (this.image && this.image.width > 0){
            const sig = this.get_visual_signature();
            if (!this._battle_baked || this._battle_buff_sig !== sig){
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.ctx.save();
                let filter = '';
                if (this.activated) filter += "brightness(50%) ";
                const frozen = (this.buff_list && this.buff_list.some && this.buff_list.some(b => b && b.content == "frozen"));
                if (frozen) filter += "hue-rotate(180deg) saturate(1.2)";
                this.ctx.filter = filter;
                this.ctx.drawImage(this.image, 0, 0, this.canvas.width, this.canvas.height);
                this.ctx.filter = '';
                this.ctx.restore();
                this.draw_extra_overlay(this.ctx);
                this._battle_baked = true;
                this._battle_buff_sig = sig;
                this._three_needs_upload = true;
            }
        }

        this.arr_poses = this.get_position_points(camera);
    }
    draw(camera,ctx,canvas){
        // Project the four corners (already in camera space from update())
        // back to screen for hit testing. Same math as the legacy renderer.
        const [screenQuad, zs] = window.project_quad_to_screen(this.arr_poses, camera, canvas.width, canvas.height);
        this.position_in_screen = screenQuad;
        this.position_in_screen_z = (zs[0] + zs[2]) / 2;

        if (this.select_flag){
            this.draw_blur_ring(ctx)
            this.draw_blur_ring(ctx)
        }

        this._ensureThreeCard();
        if (this._three_card){
            if (this._three_needs_upload){
                this._three_card.markFrontDirty();
                this._three_needs_upload = false;
            }
            this._three_card.setTransform(
                this.position,
                this.angle_x,
                this.angle_y,
                this.angle_z,
                this.size
            );
        }
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
        this._ensureThreeCard();
        if (!this._three_shadow) return;
        if (this.position[1] == -20){
            this._three_shadow.setVisible(false);
            return;
        }
        // Compute the shadow polygon in WORLD space by projecting each card
        // corner onto the table plane (y = height_table) along the sun
        // direction. We then hand the four world-space corners to a Three.js
        // BufferGeometry quad which gets rendered with a translucent dark
        // material - same visual intent as the original 2D fill.
        const xy_rotate=math.multiply(rotateX(this.angle_x),rotateY(this.angle_y));
        const xyz_rotate=math.multiply(xy_rotate,rotateZ(this.angle_z));
        var pos_rotate=math.multiply(xyz_rotate,this.points);
        const posiiton_accurate=math.add(pos_rotate,this.get_matrix_position(pos_rotate));

        const Sun_light=math.matrix([[-0.5],[-1.2],[-0.6]]);
        const [rows, cols] = posiiton_accurate.size();
        const height = math.zeros(rows, cols);
        for (let i=0;i<cols;i++){
            height.subset(math.index(rows-2, i), height_table);
        }
        const t=math.multiply(math.matrix([[0,1/Sun_light.get([1,0]),0]]), math.subtract(posiiton_accurate, height));
        const change=math.multiply(Sun_light, t);
        const sun_result=math.subtract(posiiton_accurate, change);

        const corners4=[];
        for (let col=0; col<this.corners.length; col++){
            corners4.push([
                sun_result.get([0,col]),
                sun_result.get([1,col]),
                sun_result.get([2,col]),
            ]);
        }
        // Slightly lift the shadow so it doesn't z-fight with the table top.
        const lift = -0.02;
        for (let i=0; i<4; i++) corners4[i][1] += lift;
        this._three_shadow.setVisible(true);
        this._three_shadow.setCorners(corners4);
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