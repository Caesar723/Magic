class Deck {
    constructor(name,content,Container,id) {
        this.Container=Container;this.id=id;this.name=name;
        this.cards=Array.isArray(content)?content:[];
        this.div_button_ini();
    }
    div_button_ini() {
        this.divbutton=document.createElement('button');
        this.divbutton.className='button_deck';this.divbutton.type='button';
        this.divbutton.setAttribute('aria-pressed','false');
        const text=document.createElement('span');text.className='text_deck';text.textContent=this.name;
        this.divbutton.append(text);
        this.divbutton.addEventListener('click',()=>{
            if(this.Container.deleting)return;
            this.Container.clear_child('button_process_deck_click');
            this.divbutton.classList.add('button_process_deck_click');this.divbutton.setAttribute('aria-pressed','true');
            document.getElementById('button_process').classList.add('show_button_process');
            this.Container.setActions(true);this.change_box();
        });
        document.getElementById('box_decks').append(this.divbutton);
    }
    change_box() {
        const boxes=[document.getElementById('box_cards_1'),document.getElementById('box_cards_2')];
        const target=boxes[0].classList.contains('box_cards_front')?boxes[1]:boxes[0];
        boxes.forEach(box=>box.classList.remove('box_cards_front'));
        target.classList.add('box_cards_front');target.replaceChildren();
        const list=document.createElement('ul');list.className='deck-card-list';
        this.cards.forEach(card=>{
            const row=document.createElement('li'),image=document.createElement('img'),name=document.createElement('span'),count=document.createElement('b');
            image.src=`/cards/${encodeURIComponent(card.type_card)}/${encodeURIComponent(card.name)}/compress_img.jpg`;image.alt='';image.loading='lazy';
            image.addEventListener('error',()=>image.hidden=true,{once:true});
            name.textContent=card.name;count.textContent=`× ${card.quantity}`;
            row.append(image,name,count);list.append(row);
        });
        if(!this.cards.length){const empty=document.createElement('p');empty.textContent='This deck has no cards.';list.append(empty);}
        target.append(list);document.getElementById('deck-preview-hint').hidden=true;
    }
}
