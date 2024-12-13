class Card_Add{
    constructor(){
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
        const card_names=data
        console.log(card_names)
    }
}

const card_add=new Card_Add()