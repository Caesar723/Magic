class Card_Hand extends Card{
    // Halo quad & texture both use this factor (>1). Smaller = tighter ring.
    static get HALO_OUTSET_SCALE(){ return 1.13; }

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
        this.enlarge_switch=false


        this.change_size_cache=undefined


        this.z_index=1;

        this._being_dragged = false;

        //this.battle
        this.used=false


        this.flag_dict={}
        this.counter_dict={}
        this.buff_list=[]
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
            //console.log(this.moving,this.moving_precentage,this.moving_cache)

            if (this.moving && this.moving_precentage<100){
                
                this.current_moving(...this.moving_parameters)
                
            }
            else if(this.moving && this.moving_precentage>=100){
                //console.log(this.moving,this.moving_precentage)
                this.moving=false
                this.moving_precentage=0
                
                this.finish_moving(...this.moving_parameters)
            }
            else {
                
                this.pick_moving_function()
            }
            //console.log(this.moving,this.current_moving)
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
            
        }
    }

    pick_moving_function(){//FIFO
        
        if (this.moving_cache.length){
            console.log(this.moving_cache,this.moving_cache.length)
            const para=this.moving_cache.shift()
            console.log(para,this.moving_cache,this.moving_cache.length)
            
            
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
        const vel=a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*TIME_INTERVAL*time_consume/2))/(a*math.pi))
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2
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
        const angle_change=a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2))/(Math.abs(a)*math.pi))
        this.angle_z=this.angle_z+angle_change
        this.moving_precentage+=this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2
        
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
        const dif_size=unit*a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2))/(a*math.pi))
        
        this.change_size(this.size+dif_size)
        //console.log(this.size,dif_size)
        
        this.moving_precentage+=this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2
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
            //console.log(this.moving_precentage)
            //this.check_moving()
            
            
            
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
    get_copy(){
        const card=new Card_Hand(4,5.62,[0,0,0],2,this.dynamic_canvas,this.color_fee,this.name,this.id,this.player)
        
        return card
    }

    check_weather_can_used(){
        const splited=this.color_fee.match(/\d+|\D/g);
        //console.log(this,this.player)
        const mana_dict={
            'U':this.player.total_manas[0],
            'W':this.player.total_manas[1],
            'B':this.player.total_manas[2],
            'R':this.player.total_manas[3],
            'G':this.player.total_manas[4],
        }
        //console.log(mana_dict)
        if (splited){
            for (let i in splited.reverse()){
                if (/^[+-]?\d+$/.test(splited[i])){
                    //console.log(+splited[i])
                    let rest_mana=+splited[i]
                    for (let mana_key in mana_dict){
                        rest_mana-=mana_dict[mana_key]
                    }
                    //console.log(rest_mana,this)
                    if (rest_mana>0){
                        return false
                    }

                
                }
                else{
                    // console.log(this.player,this)
                    
                    mana_dict[splited[i]]-=1;
                    //console.log(mana_dict,this)
                    if (mana_dict[splited[i]]<0){
                        return false
                    }
                    //console.log(splited[i])
                }
            }
        }
        
        return true
    }

    // Hand cards live in the owner's private camera space (Self/Opponent
    // each use their own `Camera([0,0,-50])`, independent of the shared
    // table camera). We give each player camera its own Three scene + Three
    // PerspectiveCamera (an "aux scene"), so hand cards render as real
    // Three meshes, perspective and all, while staying anchored to the
    // screen the way the original 2D renderer did.
    _ensureHandThreeCard(camera){
        if (this._three_card_initialized) return;
        if (!window.THREE_STAGE) return;
        const front = this.dynamic_canvas && this.dynamic_canvas[0];
        if (!(front instanceof HTMLCanvasElement) && !(front instanceof HTMLImageElement)) return;
        // Wait until the canvas has dimensions (filled in by the async
        // card-frame generator). See the matching check on Card.
        if (front instanceof HTMLCanvasElement && (front.width === 0 || front.height === 0)) return;
        // Defer creating the GPU texture until the front canvas has actually
        // been baked at least once by Card.update(). Creating the
        // CanvasTexture earlier — when the canvas is sized but still blank —
        // sometimes results in the GPU caching an empty texture and the
        // hand card stays invisible after a refresh, even though we later
        // call markFrontDirty(). Waiting for the first bake guarantees the
        // initial upload has the real card art.
        if (!this._canvas_baked) return;
        const aux = window.THREE_STAGE.getOrCreateAuxScene(camera);
        this._three_card = new CardPlane(
            window.THREE_STAGE,
            this._half_width,
            this._half_height,
            front,
            this.back_img,
            {
                parent: aux.scene,
                // Each aux scene clears depth before drawing, so no
                // polygon offset is needed against the table.
                polygonOffsetFactor: 0,
                polygonOffsetUnits: 0,
                handDepthMode: true,
            }
        );
        this._three_card_initialized = true;
        // First GPU upload must happen after the canvas has real pixels; some
        // drivers ignore the implicit first upload from `CanvasTexture`.
        this._three_card.markFrontDirty();
        this._three_needs_upload = false;
        this._ensureHandHalo();
    }

    // One soft green glow quad per card, parented to the same group as the
    // card mesh so it moves/rotates with the card. Placed on local **-Z**
    // (behind the card plane whose normal is +Z toward the hand camera),
    // drawn first (renderOrder) so the card face paints on top and only a
    // rim of glow remains visible around the edges.
    _ensureHandHalo(){
        if (this._three_halo || !this._three_card) return;
        const s = Card_Hand.HALO_OUTSET_SCALE;
        const halo_w = this._half_width * 2 * s;
        const halo_h = this._half_height * 2 * s;
        const tex = Card_Hand._createHandHaloTexture();
        const mat = new THREE.MeshBasicMaterial({
            map: tex,
            transparent: true,
            depthTest: false,
            depthWrite: false,
            side: THREE.DoubleSide,
            blending: THREE.AdditiveBlending,
        });
        const geo = new THREE.PlaneGeometry(halo_w, halo_h);
        const mesh = new THREE.Mesh(geo, mat);
        // Behind the card plane (see comment above). Quad is
        // `HALO_OUTSET_SCALE`× card size so a soft ring sits just outside the silhouette.
        mesh.position.set(0, 0, -0.12);
        mesh.renderOrder = -2;
        this._three_card.mesh.renderOrder = 0;

        const g = this._three_card.group;
        const cardMesh = this._three_card.mesh;
        g.remove(cardMesh);
        g.add(mesh);
        g.add(cardMesh);

        this._three_halo = { mesh, mat, geo, tex };
        this._three_halo.mesh.visible = false;
    }

    // Shared by hand (green) and battlefield selection (blue): same blur
    // passes and mesh layout, only `palette` / aspect change.
    static _createSilhouetteHaloTexture(aspectW, aspectDen, palette){
        const W = 256;
        const H = Math.round((W * aspectDen) / aspectW);
        const canvas = document.createElement("canvas");
        canvas.width = W;
        canvas.height = H;
        const g = canvas.getContext("2d");
        g.clearRect(0, 0, W, H);

        const scale = Card_Hand.HALO_OUTSET_SCALE;
        const cardW = W / scale;
        const cardH = H / scale;
        const mx = (W - cardW) / 2;
        const my = (H - cardH) / 2;
        const cornerR = Math.min(cardW, cardH) * 0.065;

        const traceOutline = (ctx, inset) => {
            const x = mx + inset;
            const y = my + inset;
            const w = cardW - 2 * inset;
            const h = cardH - 2 * inset;
            const r = Math.max(0, Math.min(cornerR, w / 2 - 0.5, h / 2 - 0.5));
            ctx.beginPath();
            ctx.moveTo(x + r, y);
            ctx.lineTo(x + w - r, y);
            ctx.quadraticCurveTo(x + w, y, x + w, y + r);
            ctx.lineTo(x + w, y + h - r);
            ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
            ctx.lineTo(x + r, y + h);
            ctx.quadraticCurveTo(x, y + h, x, y + h - r);
            ctx.lineTo(x, y + r);
            ctx.quadraticCurveTo(x, y, x + r, y);
            ctx.closePath();
        };

        const off = document.createElement("canvas");
        off.width = W;
        off.height = H;
        const og = off.getContext("2d");
        og.lineJoin = "round";
        og.lineCap = "round";
        traceOutline(og, 0);
        og.strokeStyle = palette.strokeInner;
        og.lineWidth = 3.5;
        og.shadowColor = palette.shadowInner;
        og.shadowBlur = 24;
        og.shadowOffsetX = 0;
        og.shadowOffsetY = 0;
        og.stroke();

        og.shadowBlur = 40;
        og.lineWidth = 2;
        og.strokeStyle = palette.strokeMid;
        og.stroke();

        g.save();
        g.filter = "blur(8px)";
        g.globalAlpha = 0.9;
        g.drawImage(off, 0, 0);
        g.restore();

        g.save();
        g.filter = "blur(3px)";
        g.globalAlpha = 0.45;
        g.drawImage(off, 0, 0);
        g.restore();

        traceOutline(g, 0);
        g.strokeStyle = palette.rim;
        g.lineWidth = 1.25;
        g.shadowBlur = 0;
        g.stroke();

        const tex = new THREE.CanvasTexture(canvas);
        tex.minFilter = THREE.LinearFilter;
        tex.magFilter = THREE.LinearFilter;
        tex.generateMipmaps = false;
        tex.flipY = true;
        if (THREE.sRGBEncoding) tex.encoding = THREE.sRGBEncoding;
        tex.needsUpdate = true;
        return tex;
    }

    static _createHandHaloTexture(){
        return Card_Hand._createSilhouetteHaloTexture(4, 5.62, {
            strokeInner: "rgba(100, 210, 95, 1)",
            shadowInner: "rgba(83, 158, 78, 0.98)",
            strokeMid: "rgba(140, 230, 125, 0.55)",
            rim: "rgba(210, 255, 200, 0.38)",
        });
    }

    _updateHaloVisibility(camera){
        if (!this._three_halo) return;
        const usable =
            (this.player instanceof Self) &&
            this.check_weather_can_used() &&
            (this.player.my_turn || this instanceof Instant_Hand || get_dict(this.flag_dict, "Flash"));
        // Only show the playable glow when the card front faces the camera
        // (same moment the front texture is shown).
        const frontTowardCamera = this.check_surface(camera);
        this._three_halo.mesh.visible = !!(usable && frontTowardCamera);
    }

    draw(camera,ctx,canvas){
        const new_points_pos=[];
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
        this.position_in_screen=new_points_pos;

        this._ensureHandThreeCard(camera);
        if (this._three_card){
            if (this._three_needs_upload){
                this._three_card.markFrontDirty();
                this._three_needs_upload = false;
            }
            // Show the card front when the plane normal opposes the
            // camera's forward vector (matches original `check_surface`).
            this._three_card.setFace(!this.check_surface(camera));
            this._three_card.setTransform(
                this.position,
                this.angle_x,
                this.angle_y,
                this.angle_z,
                this.size
            );
            this._applyHandDrawOrder();
            this._updateHaloVisibility(camera);
        }
    }

    // Fan order + hover + drag: higher `renderOrder` paints on top because
    // `handDepthMode` disables depth tests among hand quads.
    _applyHandDrawOrder(){
        if (!this._three_card || !this.player || !this.player.cards) return;
        const hand = this.player.cards;
        const si = hand.indexOf(this);
        const base = si < 0 ? 0 : si * 6;
        let ro = base + (this.z_index || 0) * 120;
        if ((this.z_index || 0) > 1) ro += 800;
        if (this._being_dragged) ro += 4000;
        this._three_card.setRenderOrder(ro);
        if (this._three_halo) this._three_halo.mesh.renderOrder = ro - 1;
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
        ctx.strokeStyle = 'rgb(83,158,78)';
        ctx.shadowColor = 'rgba(83,158,78)'; // 半透明的蓝色光晕
        ctx.fillStyle = 'rgba(83,158,78)';
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
    }
    remove_buff(buff){
        this.buff_list=this.buff_list.filter(item => item.id !== buff.id);
        
    }

    dispose_three(){
        if (this._three_halo){
            try {
                const m = this._three_halo.mesh;
                if (m && m.parent) m.parent.remove(m);
                this._three_halo.geo.dispose();
                this._three_halo.mat.dispose();
                if (this._three_halo.tex) this._three_halo.tex.dispose();
            } catch (e) {}
            this._three_halo = null;
        }
        super.dispose_three();
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


        this.orginal_image=this.back_img

    }

    update(){
        this.arr_poses=this.get_position_points();
        this.check_moving()

        
    }
    // Opponent hand cards never reveal their face. The `CardPlane` is
    // single-sided/DoubleSide and we only ever use the back image as its
    // active texture, so no back-texture allocation is needed.
    _ensureHandThreeCard(camera){
        if (this._three_card_initialized) return;
        if (!window.THREE_STAGE) return;
        const back = this.back_img;
        if (!(back instanceof HTMLImageElement)) return;
        // Wait until the back image is actually decoded. Creating the
        // texture earlier sometimes caches an empty GPU texture and the
        // opponent's hand stays blank on refresh.
        if (!back.complete || back.naturalWidth === 0) return;
        const aux = window.THREE_STAGE.getOrCreateAuxScene(camera);
        this._three_card = new CardPlane(
            window.THREE_STAGE,
            this._half_width,
            this._half_height,
            back,
            null,
            {
                parent: aux.scene,
                polygonOffsetFactor: 0,
                polygonOffsetUnits: 0,
                handDepthMode: true,
            }
        );
        this._three_card_initialized = true;
        this._three_card.markFrontDirty();
    }

    draw(camera,ctx,canvas){
        const new_points_pos=[];
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
        this.position_in_screen=new_points_pos;

        this._ensureHandThreeCard(camera);
        if (this._three_card){
            this._three_card.setTransform(
                this.position,
                this.angle_x,
                this.angle_y,
                this.angle_z,
                this.size
            );
            if (this.player && this.player.cards){
                const si = this.player.cards.indexOf(this);
                const ro = (si < 0 ? 0 : si * 6) + ((this.z_index || 0) * 120);
                this._three_card.setRenderOrder(ro);
            }
        }
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
        const vel=a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2))/(a*math.pi))
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2
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
        const angle_change=a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2))/(Math.abs(a)*math.pi))
        this.angle_z=this.angle_z+angle_change
        this.moving_precentage+=this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2
        
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
        const dif_size=unit*a*Math.pow(Math.sin(x/a),2)/((100/(this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2))/(a*math.pi))
        
        this.change_size(this.size+dif_size)
        //console.log(this.size,dif_size)
        
        this.moving_precentage+=this.TIME_INTERVAL*time_consume*TIME_INTERVAL/2
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

    get_copy(){
        const card=new Card_Hand_Oppo(4,5.62,[0,0,0],2,this.id,this.player)
        
        return card
    }

    
    append_buff(buff){
       
    }
}