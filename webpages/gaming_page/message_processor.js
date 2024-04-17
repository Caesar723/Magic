/*

不管是什么操作，只要是card都按照这个来
card(id,name,type(blue),type_card(Creature),rarity,content,image_path)
    Creature-(fee,Org_Life,Life,Org_Damage,Damage )
    Sorcery-（fee  ）
    Instant-（fee ）
    Land-（）

create_new(card)

find_card(card)

int(number)

player(name,(Opponent,Self))

state(1，2，3...)

action(action name,parameter)

    
action_list(action,action,action,.....)


Initinal_all()
*/
class Message_Processor{
    constructor(client){
        this.client=client
        this.card_frame=client.card_frame


        this.action_diction={}


        this.function_diction={
            "Creature":1,
            "Sorcery":1,
            "Instant":1,
            "Land":1,
            "create_new":this.create_new,
            "find_card":this.find_card,
            "player":1,
            "action":1,
            "action_list":1,
            "Initinal_all":1,
            "int":this.int
        }

        console.log(this.extractParts("int(find_card(67),create_new(2))"))

    }
    processage_message(text){

    }
    create_card(text){

    }
    create_action(text){

    }

    process_select_message(text){

    }

    get_message(text){

    }
    Creature(id,name,type,type_card,rarity,content,image_path,fee,Org_Life,Life,Org_Damage,Damage){

    }
    create_new(card){
        console.log(card)
        return 1
    }

    find_card(card){
        console.log(card)
        return 2
    }
    int(number,test){
        console.log(number,test)
        return number+test
    }
    extractParts(str) {
        const indexOfFirstParenthesis = str.indexOf('('); // 找到第一个 '(' 的索引
        if (indexOfFirstParenthesis === -1) return str; 

        const beforeParenthesis = str.substring(0, indexOfFirstParenthesis); // 获取 '(' 左边的内容
        
        const inParenthesis = str.substring(indexOfFirstParenthesis + 1, str.length-1); // 获取括号内的内容

        let result_para=[]
        
        for(let para of inParenthesis.split(",")){

            const result=this.extractParts(para)
            result_para.push(result)
        }
        return this.function_diction[beforeParenthesis](...result_para)

    
    }
}