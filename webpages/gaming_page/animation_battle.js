class Animation_Battle{








    
    check_moving(){
        if (this.moving && this.moving_precentage<100){
            this.current_moving(this.moving_parameters)
            
        }
        else if(this.moving && this.moving_precentage>=100){
            this.moving=false
        }
    }

    start_moving(moving_type,parameters){
        if (this.moving==false && this.moving_precentage<100){
            this.current_moving=this.moving_dict[moving_type][0]
            console.log(this.moving_dict[moving_type],this.moving_dict[moving_type][1])
            this.moving_dict[moving_type][1](parameters)
            this.moving=true
            this.moving_precentage=0;
            this.moving_parameters=parameters;
        }
    }
    move_to_horizontal(target_position){//target_position[x,y,z]
        

    }
    move_to_horizontal_prepared(target_position){//target_position[x,y,z]
        

    }
    move_to_horizontal_finish(target_position){//target_position[x,y,z]
        

    }
    move_to_prepared(target_position){
        console.log(this,target_position,this.calculate_vector_move)
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        const a=math.sqrt(distance*2/math.pi)
        const time_consume=1.5
        this.moving_store=[a,unitVector,time_consume]
    }
    move_to(target_position){//target_position[x,y]
        const a=this.moving_store[0];
        const unitVector=this.moving_store[1];
        const time_consume=this.moving_store[2];
        console.log(time_consume)
        const x=(a*math.pi/100)*this.moving_precentage
        const vel=a*Math.pow(Math.sin(x/a),2)/((100/(TIME_INTERVAL*time_consume))/(a*math.pi))
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=TIME_INTERVAL*time_consume
        console.log(this.position)
        
    }
    move_to_finish(target_position){
        
    }
    attack_to_prepared(target_position){//target_position[x,y,z]  撞一下然后返回原来的位置
        console.log(this,target_position,this.calculate_vector_move)
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        const degree=10
        const a=math.sqrt(distance*(4/degree)/math.pi)
        const time_consume=1.5
        this.moving_store=[a,unitVector,time_consume,degree]
    }
    attack_to(target_position){//target_position[x,y,z]  撞一下然后返回原来的位置
        const a=this.moving_store[0];
        const unitVector=this.moving_store[1];
        const time_consume=this.moving_store[2];
        const degree=this.moving_store[3];
        console.log(time_consume)
        const x=(a*math.pi/100)*this.moving_precentage
        
        
        if (this.moving_precentage<50){
            var vel=degree*a*Math.pow(Math.sin(x/a),2)/((100/(TIME_INTERVAL*time_consume))/(a*math.pi))
        }
        else{
            var vel=-degree*a*Math.pow(Math.sin(x/a),2)/((100/(TIME_INTERVAL*time_consume))/(a*math.pi))
        }
        const new_vel=math.multiply(vel,unitVector)
        const new_pos=math.add(this.position,new_vel);
        this.position[0]=new_pos[0]
        this.position[1]=new_pos[1]
        this.position[2]=new_pos[2]
        this.moving_precentage+=TIME_INTERVAL*time_consume
        console.log(this.position)
    }
    attack_to_finish(target_position){//target_position[x,y,z]  撞一下然后返回原来的位置
        console.log(this,target_position,this.calculate_vector_move)
        const [unitVector,distance]=this.calculate_vector_move(target_position)
        const degree=10
        const a=math.sqrt(distance*(4/degree)/math.pi)
        const time_consume=1.5
        this.moving_store=[a,unitVector,time_consume,degree]
    }
    rotate_to_point_prepared(target_position){//让它指向目标点

    }
    rotate_to_point(target_position){//让它指向目标点

    }

    calculate_vector_move(target_position){//返回一个unit vector, 总的distance
        const difference = math.subtract(target_position, this.position);
        const distance=math.norm(difference);
        const unitVector = math.divide(difference, distance);
        return [unitVector,distance]

    }



}