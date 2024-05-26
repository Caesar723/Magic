/*

不管是什么操作，只要是card都按照这个来
card(flying,active,player,id,name,type(blue),type_card(Creature),rarity,content,image_path)
    Creature-(fee,Org_Life,Life,Org_Damage,Damage )
    Sorcery-（fee  ）
    Instant-（fee ）
    Land-（）
    Opponent-()
    ## 先find card 然后再create card

create_new(card)

find_card(card)

int(number)

player(name,(Opponent,Self))

state(1，2，3...)

action(action name,parameter)

    
action_list(action,action,action,.....)


Initinal_all(
    parameters(card1,card2),//self hand 
    parameters(card1,card2),//oppo hand 
    parameters(card1,card2),//self battle 
    parameters(card1,card2),//oppo battle
    parameters(card1,card2),//self lands 
    parameters(card1,card2),//oppo lands
    parameters(action1,action2),//create actions
    parameters(int(0),int(0),int(0),int(0),int(0)),//[blue,white,black,red,green]
    
    29,//time turn
    29,//time bullet
    15,//life self
    25,//life oppo
    40,//length of deck self
    40,//length of deck oppo
)

parameters() return [....]


showOBJ() return this.show2d
*/
class Message_Processor{
    constructor(client){
        
        this.client=client
        
        this.card_frame=client.card_frame


        this.action_diction={
            "Creature_Start_Attack":Creature_Start_Attack,
            "Creature_Prepare_Attack":Creature_Prepare_Attack,
            "Play_Cards":Play_Cards,
            "Creature_Prepare_Defense":Creature_Prepare_Defense,
            "Activate_Ability":Activate_Ability,
            "Reset_Ability":Reset_Ability,
            "Select_Object":Select_Object,
            "Add_Buff":Add_Buff,
            "Attack_To_Object":Attack_To_Object,
            "Cure_To_Object":Cure_To_Object,
            "Gain_Card":Gain_Card,
            "Lose_Card":Lose_Card,
            "Die":Die,
            "Summon":Summon,
            "Turn":Turn,
            "Change_Mana":Change_Mana,

        }


        this.function_diction={
            "Creature":this.Creature.bind(this),
            "Sorcery":this.Sorcery.bind(this),
            "Instant":this.Instant.bind(this),
            "Land":this.Land.bind(this),
            "Opponent":this.Opponent.bind(this),
            "player":this.player.bind(this),
            "action":this.action.bind(this),
            "action_list":this.action_list.bind(this),
            "Initinal_all":this.initinal_all.bind(this),
            "state":this.state.bind(this),
            "int":this.int.bind(this),
            "parameters":this.parameters.bind(this),
            "string":this.string.bind(this),
            "showOBJ":this.showOBJ.bind(this),
            
        }
        this.state(1,2,3,4,5)
        // console.log(this.extractParts("Creature(player(CC,Self),int(11334),Xuanpei,blue,Creature,Uncommon,string(a,b,c,d()),cards/creature/Angelic Protector/image.jpg)"))
        // console.log(this.extractParts("player(CC,Self)"))
        //console.log(this.extractParts("action_list(action(Gain_Card,parameters(player(CC,Self),player(CC,Self),Land(1,1,player(CC,Self),int(11334),Xuanpei,blue,Creature,Uncommon,string(a,b,c,d()),cards/creature/Angelic Protector/image.jpg))),action(Gain_Card,parameters(player(CC,Self),player(CC,Self),Land(1,1,player(CC,Self),int(11334),Xuanpei,blue,Creature,Uncommon,string(a,b,c,d()),cards/creature/Angelic Protector/image.jpg))),action(Gain_Card,parameters(player(CC,Self),player(CC,Self),Land(1,1,player(CC,Self),int(11334),Xuanpei,blue,Creature,Uncommon,string(a,b,c,d()),cards/creature/Angelic Protector/image.jpg))))"))
        //this.extractParts("action_list(action(Gain_Card,parameters(player(t,Self),player(t,Self),Land(0,0,player(t,Self),int(4319679728),string(Island),blue,Land,Uncommon,string(),cards/land/Island/image.jpg))))")
        //this.extractParts("action_list(action(Play_Cards,parameters(Land(0,0,player(CC,Self),int(4327028048),string(Island),blue,Land,Uncommon,string(),cards/land/Island/image.jpg),player(CC,Self),Land(0,0,player(CC,Self),int(4327028048),string(Island),blue,Land,Uncommon,string(),cards/land/Island/image.jpg),showOBJ())),action(Lose_Card,parameters(player(CC,Self),player(CC,Self),Land(0,0,player(CC,Self),int(4327028048),string(Island),blue,Land,Uncommon,string(),cards/land/Island/image.jpg))),action(Summon,parameters(Land(0,0,player(CC,Self),int(4327028048),string(Island),blue,Land,Uncommon,string(),cards/land/Island/image.jpg),player(CC,Self))))")
    }
    countOccurrencesLoop(str, char) {
        let count = 0;
        for (let i = 0; i < str.length; i++) {
            if (str[i] === char) {
                count++;
            }
        }
        return count;
    }
    processage_message(text){

    }



    string(){

    }
    showOBJ(){
        return this.client.show_2d
    }
    opponent_player(name){

    }
    find_card(id){//返回的为card hand 
        console.log()
        for (let card_oppo_hand of this.client.oppo_player.cards){
            if (card_oppo_hand.id==id){
                return card_oppo_hand
            }
        }
        for (let card_self_hand of this.client.self_player.cards){
            console.log(this.client.self_player.cards,this.client.self_player.cards[1],card_self_hand,card_self_hand.id,id)
            if (card_self_hand.id==id){
                return card_self_hand
            }
        }
        for (let card_oppo_battle of this.client.table.opponent_battlefield){
            if (card_oppo_battle.id==id){
                return card_oppo_battle
            }
        }
        for (let card_self_battle of this.client.table.self_battlefield){
            if (card_self_battle.id==id){
                return card_self_battle
            }
        }
        for (let card_oppo_land of this.client.table.opponent_landfield){
            if (card_oppo_land.id==id){
                return card_oppo_land
            }
        }
        for (let card_self_land of this.client.table.self_landfield){
            if (card_self_land.id==id){
                return card_self_land
            }
        }
        return false
    }
    create_new(card){
        console.log(card)
        return 1
    }
    Creature(flying,active,player,id,name,type,type_card,rarity,content,image_path,fee,Org_Life,Life,Org_Damage,Damage){
        const result=this.find_card(id)
        if (result){
            return result
        }
        //console.log(player)
        const canvas=this.client.table.card_frame.generate_card(type,name,type_card,rarity,content,image_path)
        const card=new Creature_Hand(4,5.62,[0,60*player.unit,-20],1.5,canvas,fee,Org_Damage,Org_Life,Life,Damage,name,id,player)
        return card

    }
    Sorcery(flying,active,player,id,name,type,type_card,rarity,content,image_path,fee){
        const result=this.find_card(id)
        if (result){
            return result
        }
        const canvas=this.client.table.card_frame.generate_card(type,name,type_card,rarity,content,image_path)
        const card=new Sorcery_Hand(4,5.62,[0,60*player.unit,-20],1.5,canvas,fee,name,id,player)
        return card
    }
    Instant(flying,active,player,id,name,type,type_card,rarity,content,image_path,fee){
        const result=this.find_card(id)
        if (result){
            return result
        }
        const canvas=this.client.table.card_frame.generate_card(type,name,type_card,rarity,content,image_path)
        const card=new Instant_Hand(4,5.62,[0,60*player.unit,-20],1.5,canvas,fee,name,id,player)
        return card
    }
    Land(flying,active,player,id,name,type,type_card,rarity,content,image_path,manas){
        const result=this.find_card(id)
        console.log(manas)
        if (result){
            return result
        }
        const canvas=this.client.table.card_frame.generate_card(type,name,type_card,rarity,content,image_path)
        const card=new Land_Hand(4,5.62,[0,60*player.unit,-20],1.5,canvas,name,id,player,manas)
        return card

    }
    Opponent(player,id){
        const result=this.find_card(id)
        //console.log(result)
        if (result){
            return result
        }
        const card=new Card_Hand_Oppo(4,5.62,[0,60*player.unit,-20],0.7,id,player)
        //console.log(card)
        return card
    }
    
    

    process_select_message(text){

    }

    get_message(text){

    }
    

    

    
    int(number){
        return +number
        // console.log(number,test)
        // return number+test
    }
    initinal_all(self_hand,oppo_hand,self_battle,oppo_battle,self_lands,oppo_lands,actions,manas,time_turn,time_bullet,life_self,life_oppo,len_deck_self,len_deck_oppo){
        console.log(self_hand,oppo_hand,self_battle,oppo_battle,self_lands,oppo_lands,actions,manas,time_turn,time_bullet,life_self,life_oppo,len_deck_self,len_deck_oppo)
        console.log(this.client,this.client.self_player)
        const self_player=this.client.self_player
        const oppo_player=this.client.oppo_player

        for (let card of self_hand){
            self_player.cards.push(card)
        }
        for (let card of oppo_hand){
            oppo_player.cards.push(card)
        }
        for (let card of self_battle){
            this.client.table.self_battlefield.push(Animation.check_battle(card,self_player))
        }
        for (let card of oppo_battle){
            this.client.table.opponent_battlefield.push(Animation.check_battle(card,oppo_player))
        }
        for (let card of self_lands){
            this.client.table.self_landfield.push(Animation.check_battle(card,self_player))
        }
        for (let card of oppo_lands){
            this.client.table.opponent_landfield.push(Animation.check_battle(card,oppo_player))
        }

        for (let action of actions){
            this.client.action_bar.actions.push(action)
        }
        self_player.mana_bar.set_mana(manas)
        this.client.table.timmer_turn.animate_set(time_turn,this.client.table.timmer_turn.time)
        this.client.table.timmer_bullet.animate_set(time_bullet,this.client.table.timmer_bullet.time)
        self_player.player_life_ring.animate_set(life_self,self_player.player_life_ring.life)
        oppo_player.player_life_ring.animate_set(life_oppo,oppo_player.player_life_ring.life)
        this.client.table.deck_self_graph.number_of_cards=len_deck_self
        this.client.table.deck_oppo_graph.number_of_cards=len_deck_oppo


    }
    player(name,type){
        if (type=="Opponent"){
            
            const player=this.client.oppo_player
            if (player.name==name){
                return player
            }
        }
        else{
            
            const player=this.client.self_player
            if (player.name==name){
                return player
            }
        }   
    }
    state(){
        let result=[]
        for (let num of arguments){
            result.push(+num)
        }
        return result
    }
    action(act_name,para){
        //console.log(this.action_diction[act_name],para)
        const action=new this.action_diction[act_name](...para)
        return action
    }
    action_list(){
        for (let action of arguments){
            //action.set_animate()
            // actions_cache
            //this.client.action_bar.actions.push(action)
            this.client.action_bar.actions_cache.push(action)
        }
        this.client.action_bar.actions_cache.push(false)
        this.client.action_bar.actions_finsihed=true
    }
    parameters(){
        let result=[]
        
        for (let para of arguments){

            result.push(para)
        }
        if (result.length==1 && result[0] == ''){
            return []
        }
        //console.log(arguments,result,result==[''])
        return result
        //arguments
    }
    time_turn(str){
        const timmer_turn=this.client.table.timmer_turn
        timmer_turn.animate_set(+str,timmer_turn.time)
    }
    time_bullet(str){
        const timmer_bullet=this.client.table.timmer_bullet
        timmer_bullet.animate_set(+str,timmer_bullet.time)
    }
    length_deck(player,height){
        if (player=="Self"){

        }
    }
    extractParts(str) {
        const indexOfFirstParenthesis = str.indexOf('('); // 找到第一个 '(' 的索引
        if (indexOfFirstParenthesis === -1) return str; 

        const beforeParenthesis = str.substring(0, indexOfFirstParenthesis); // 获取 '(' 左边的内容
        
        const inParenthesis = str.substring(indexOfFirstParenthesis + 1, str.length-1); // 获取括号内的内容
        if (beforeParenthesis=="string"){
            //console.log(inParenthesis)
            return inParenthesis
        }
        let result_para=[]

        let numBraL=0
        //let numBraR=0
        var para=""
        //console.log(inParenthesis)
        for (let char of inParenthesis){
            if (char=="("){
                numBraL++
                para+=char
            }
            else if (char==")"){
                numBraL--
                para+=char
            }
            else if (char=="," && numBraL==0){
                const result=this.extractParts(para)
                console.log(para)
                result_para.push(result)
                para=""
            }
            else {
                para+=char
            }
        }
        const result=this.extractParts(para)
        //sconsole.log(para)
        result_para.push(result)
        
        // for(let para of inParenthesis.split(",")){

        //     const result=this.extractParts(para)
        //     console.log(para,result)
        //     result_para.push(result)
        // }
        
        return this.function_diction[beforeParenthesis](...result_para)

    
    }
}