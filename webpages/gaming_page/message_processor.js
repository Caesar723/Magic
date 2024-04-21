/*

不管是什么操作，只要是card都按照这个来
card(player,id,name,type(blue),type_card(Creature),rarity,content,image_path)
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


Initinal_all()

parameters() return [....]
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
            // "create_new":this.create_new,
            // "find_card":this.find_card,
            "player":this.player.bind(this),
            "action":this.action.bind(this),
            "action_list":this.action_list.bind(this),
            "Initinal_all":this.initinal_all.bind(this),
            "state":this.state.bind(this),
            "int":this.int.bind(this),
            "parameters":this.parameters.bind(this),
            "string":this.string.bind(this),
        }
        this.state(1,2,3,4,5)
        // console.log(this.extractParts("Creature(player(CC,Self),int(11334),Xuanpei,blue,Creature,Uncommon,string(a,b,c,d()),cards/creature/Angelic Protector/image.jpg)"))
        // console.log(this.extractParts("player(CC,Self)"))
        console.log(this.extractParts("action_list(action(Gain_Card,parameters(player(CC,Self),player(CC,Self),Land(player(CC,Self),int(11334),Xuanpei,blue,Creature,Uncommon,string(a,b,c,d()),cards/creature/Angelic Protector/image.jpg))),action(Gain_Card,parameters(player(CC,Self),player(CC,Self),Land(player(CC,Self),int(11334),Xuanpei,blue,Creature,Uncommon,string(a,b,c,d()),cards/creature/Angelic Protector/image.jpg))),action(Gain_Card,parameters(player(CC,Self),player(CC,Self),Land(player(CC,Self),int(11334),Xuanpei,blue,Creature,Uncommon,string(a,b,c,d()),cards/creature/Angelic Protector/image.jpg))))"))

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
    find_card(id){//返回的为card hand
        console.log()
        return false
    }
    create_new(card){
        console.log(card)
        return 1
    }
    Creature(player,id,name,type,type_card,rarity,content,image_path,fee,Org_Life,Life,Org_Damage,Damage){
        const result=this.find_card(id)
        if (result){
            return result
        }
        console.log(player)
        const canvas=this.client.table.card_frame.generate_card(type,name,type_card,rarity,content,image_path)
        const card=new Creature_Hand(4,5.62,[0,60*player.unit,-20],1.5,canvas,fee,Org_Damage,Org_Life,name,id,player)
        return card

    }
    Sorcery(player,id,name,type,type_card,rarity,content,image_path,fee){
        const result=this.find_card(id)
        if (result){
            return result
        }
        const canvas=this.client.table.card_frame.generate_card(type,name,type_card,rarity,content,image_path)
        const card=new Sorcery_Hand(4,5.62,[0,60*player.unit,-20],1.5,canvas,fee,name,id,player)
        return card
    }
    Instant(player,id,name,type,type_card,rarity,content,image_path,fee){
        const result=this.find_card(id)
        if (result){
            return result
        }
        const canvas=this.client.table.card_frame.generate_card(type,name,type_card,rarity,content,image_path)
        const card=new Instant_Hand(4,5.62,[0,60*player.unit,-20],1.5,canvas,fee,name,id,player)
        return card
    }
    Land(player,id,name,type,type_card,rarity,content,image_path){
        const result=this.find_card(id)
        if (result){
            return result
        }
        const canvas=this.client.table.card_frame.generate_card(type,name,type_card,rarity,content,image_path)
        const card=new Land_Hand(4,5.62,[0,60*player.unit,-20],1.5,canvas,name,id,player)
        return card

    }
    Opponent(player,id){
        const card=new Card_Hand_Oppo(4,5.62,[0,60*player.unit,-20],0.7,id,player)
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
    initinal_all(){

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
            action.set_animate()
            this.client.action_bar.actions.push(action)
        }
        this.client.action_bar.actions.push(false)
    }
    parameters(){
        let result=[]
        console.log(arguments)
        for (let para of arguments){
            result.push(para)
        }
        return result
        //arguments
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
        console.log(inParenthesis)
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
        console.log(para)
        result_para.push(result)
        
        // for(let para of inParenthesis.split(",")){

        //     const result=this.extractParts(para)
        //     console.log(para,result)
        //     result_para.push(result)
        // }
        
        return this.function_diction[beforeParenthesis](...result_para)

    
    }
}