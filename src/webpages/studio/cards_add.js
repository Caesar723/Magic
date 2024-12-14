class Card_Add{
    constructor(socket){
      this.socket=socket
      this.type_dict={
        "Creature":null,
        "Instant":null,
        "Land":null,
        "Sorcery":null,
      }
      this.send_request()
    }
    async send_request(){
        const response=await fetch("/get_all_cards_name",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            }
        })
        const data=await response.json()
        this.process_data(data.card_names)
    }
    process_data(data){
        const dict_mach={
          "Creature":"creature",
          "Instant":"Instant",
          "Land":"land",
          "Sorcery":"sorcery",
        }
        const card_names=data
        //console.log(card_names)
        const type_list=document.getElementById("type_list")
        for (let type in card_names){
            const type_element=document.createElement("div")
            type_element.classList.add("type_element")
            type_element.innerText=type
            type_list.appendChild(type_element)
            type_element.addEventListener("click",()=>{
                const element=document.getElementById("card_list")
                element.innerHTML=""
                element.appendChild(this.type_dict[type])
            })

            const cards_element=document.createElement("div")
            cards_element.classList.add("cards_element_holder")
            for (let name of card_names[type]){
                const img_path= `cards/${dict_mach[type]}/${name}/compress_img.jpg`
                const card_element=document.createElement("div")
                card_element.classList.add("card_element")
                card_element.innerHTML=`<img src="${img_path}" alt="${name}">${name}`
                card_element.addEventListener("click", async ()=>{
                    await this.add_card(type,name)
                })
                cards_element.appendChild(card_element)
            }
            this.type_dict[type]=cards_element
        }
    }
    async add_card(type,name){
        const player_name=window.dataFromBackend.self
        const values=[player_name,"add_card",`${name}+${type}+1`]
        await this.socket.send(values.join("|"))
    }

    
}

