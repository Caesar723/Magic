const cardPlayers = [
  {
    name: "Gorbluk the Grumpy",
    age: 45,
    story: "Gorbluk is a seasoned orc who once led a fearsome horde. Now retired, he spends his time grumbling about how card games were better in the old days.",
    level: 12
  },
  {
    name: "Elowen the Enchanter",
    age: 120,
    story: "A mystical elf who loves to enchant her cards, often leaving her opponents confused and wondering if they lost because of skill or magic.",
    level: 18
  },
  {
    name: "Bramwell the Barkeep",
    age: 52,
    story: "Bramwell runs the most popular tavern in the land. He’s known for his quick wit, faster drinks, and surprisingly sharp card skills.",
    level: 10
  },
  {
    name: "Nugget the Gnome",
    age: 85,
    story: "Nugget may be small, but his luck is enormous. This gnome claims to have a golden touch, though most think it's just the shine of his personality.",
    level: 8
  },
  {
    name: "Vespera the Vexed",
    age: 203,
    story: "A dark sorceress with a wicked sense of humor, Vespera enjoys tormenting her opponents with cursed cards and bad puns.",
    level: 20
  },
  {
    name: "Hogarth the Hammer",
    age: 60,
    story: "A retired dwarf blacksmith, Hogarth has a heavy hand both in the forge and at the card table. His opponents fear his 'Hammer of Doom' card slam.",
    level: 14
  },
  {
    name: "Lilith the Lush",
    age: 33,
    story: "Lilith is a succubus who frequents card games to 'drain' the energy of those who lose to her. She's a notorious cheat but no one seems to mind.",
    level: 16
  },
  {
    name: "Rogar the Reluctant",
    age: 29,
    story: "A young warrior with a heart of gold and a head full of rocks. Rogar would rather be out slaying dragons, but he's surprisingly good at cards.",
    level: 9
  },
  {
    name: "Thornwick the Thief",
    age: 35,
    story: "A nimble rogue with sticky fingers and a quick smile. Thornwick is more interested in stealing your gold than winning the game, but often does both.",
    level: 17
  },
  {
    name: "Tilda the Tolerant",
    age: 67,
    story: "A kind-hearted cleric who plays to keep the peace among her often bickering companions. Her strategy is as patient as her demeanor.",
    level: 11
  },
  {
    name: "Snarl the Scribe",
    age: 300,
    story: "This ancient dragon once terrorized kingdoms, but now he enjoys the quiet life, meticulously recording every game in his massive ledger.",
    level: 22
  },
  {
    name: "Marvin the Muddler",
    age: 48,
    story: "A potion master who loves to mix drinks as much as he loves to mix up the rules. His concoctions often leave players seeing double… or worse.",
    level: 13
  },
  {
    name: "Flibber the Fey",
    age: 150,
    story: "A mischievous sprite who loves to mess with other players by 'innocently' switching their cards. His giggles give him away every time.",
    level: 10
  },
  {
    name: "Griselda the Gruff",
    age: 70,
    story: "An old hag who doesn’t suffer fools lightly. Griselda plays as ruthlessly as she brews her potions, often leaving her opponents in a foul mood.",
    level: 15
  },
  {
    name: "Balthazar the Bold",
    age: 38,
    story: "A swashbuckling pirate who’s as daring with his bets as he is with his blade. Balthazar has never met a risk he didn’t like… or lose.",
    level: 12
  },
  {
    name: "Fiona the Fickle",
    age: 105,
    story: "A shape-shifting witch whose mood—and appearance—changes with every card drawn. Her opponents never know who they’re playing against.",
    level: 19
  },
  {
    name: "Glimmer the Greedy",
    age: 90,
    story: "A treasure-hunting dwarf who values gold above all else. Glimmer’s only in it for the winnings, and she’ll do anything to get them.",
    level: 14
  },
  {
    name: "Sizzle the Salamander",
    age: 12,
    story: "A fire-breathing lizard who just discovered his love for cards. Sizzle is more likely to burn his hand than win a game, but he’s enthusiastic.",
    level: 7
  },
  {
    name: "Quinlan the Quirky",
    age: 42,
    story: "An eccentric wizard who insists on using his own, magical deck. Quinlan’s cards have a life of their own, much to his opponents' dismay.",
    level: 16
  },
  {
    name: "Belinda the Beastmaster",
    age: 50,
    story: "A ranger with a deep connection to animals, Belinda often has her furry and feathered friends 'help' her win. Her hawk has an uncanny eye for cards.",
    level: 15
  },
  {
    name: "Ulric the Unyielding",
    age: 36,
    story: "A stubborn knight who refuses to fold, even when his hand is terrible. Ulric’s honor is as unbending as his poker face.",
    level: 13
  },
  {
    name: "Zara the Zephyr",
    age: 125,
    story: "A graceful wind spirit who plays cards with a delicate touch. Zara’s movements are so swift that she often leaves her opponents in the dust.",
    level: 17
  },
  {
    name: "Pip the Plucky",
    age: 22,
    story: "A young adventurer with a heart full of dreams and a pocket full of bad cards. Pip’s optimism is his greatest weapon at the table.",
    level: 8
  },
  {
    name: "Mortimer the Morose",
    age: 65,
    story: "A necromancer who sees the world through a gloomy lens. Mortimer’s strategy is as grim as his outlook on life, but he’s always one step ahead.",
    level: 14
  },
  {
    name: "Seraphina the Serene",
    age: 101,
    story: "A high elf who approaches every game with calm and grace. Seraphina’s presence is so soothing that even losing to her feels like a win.",
    level: 18
  },
  {
    name: "Krognar the Crusher",
    age: 43,
    story: "A massive ogre who’s better at smashing things than playing cards. Krognar’s brute strength often intimidates his opponents into folding.",
    level: 11
  },
  {
    name: "Wendell the Wily",
    age: 72,
    story: "An old gnome with a sharp mind and a sharper tongue. Wendell loves to bluff, and his opponents never know if he’s being serious or just joking.",
    level: 16
  },
  {
    name: "Luna the Lunatic",
    age: 28,
    story: "A wild-eyed witch who plays with reckless abandon. Luna’s unpredictable nature makes her a wildcard—literally and figuratively.",
    level: 12
  },
  {
    name: "Borin the Blustery",
    age: 67,
    story: "A dwarven bard who’s always the loudest at the table. Borin’s boisterous personality is matched only by his love for dramatic wins.",
    level: 14
  },
  {
    name: "Eldrick the Eccentric",
    age: 93,
    story: "An ancient wizard with peculiar habits. Eldrick insists on reciting long-winded spells before every game, much to his companions' annoyance.",
    level: 19
  },
  {
    name: "Sasha the Shadow",
    age: 34,
    story: "A stealthy assassin who prefers to stay in the background, observing her opponents. Sasha’s quiet demeanor hides her deadly skills at cards.",
    level: 17
  },
  {
    name: "Bramble the Boisterous",
    age: 24,
    story: "A satyr who loves to party as much as he loves to play. Bramble’s infectious laughter and constant jokes keep the game lively, even when he’s losing.",
    level: 9
  },
  {
    name: "Grunthar the Grim",
    age: 58,
    story: "A grim-faced warrior who’s seen too much battle. Grunthar’s poker face is as unyielding as his sword, making him a formidable opponent.",
    level: 15
  },
  {
    name: "Flicker the Flame",
    age: 4,
    story: "A playful fire elemental who just wants to have fun. Flicker’s presence adds a bit of warmth to the table—sometimes literally.",
    level: 5
  },
  {
    name: "Violet the Viper",
    age: 30,
    story: "A sly rogue with a venomous wit. Violet enjoys toying with her opponents, often making cutting remarks that leave them second-guessing their plays.",
    level: 13
  },
  {
    name: "Thistle the Thorny",
    age: 92,
    story: "An old druid who’s more plant than man. Thistle’s connection to nature gives him an uncanny ability to read his opponents’ moves before they make them.",
    level: 16
  },
  {
    name: "Sprocket the Tinkerer",
    age: 37,
    story: "A goblin inventor who loves to build gadgets, even during a game. Sprocket’s contraptions often give him an unfair advantage—though he calls it 'creative'.",
    level: 10
  },
  {
    name: "Astrid the Astute",
    age: 29,
    story: "A young mage with a sharp intellect and sharper cards. Astrid’s strategy is so well-planned that she often wins before her opponents realize they’re playing.",
    level: 15
  },
  {
    name: "Blorg the Brash",
    age: 40,
    story: "An ogre with more brawn than brains. Blorg plays with sheer force, slamming down his cards with such enthusiasm that the table often shudders.",
    level: 11
  },
  {
    name: "Lysandra the Luminous",
    age: 108,
    story: "A radiant cleric whose light shines even at the card table. Lysandra’s benevolence is only matched by her fierce competitiveness.",
    level: 18
  },
  {
    name: "Drogo the Dour",
    age: 55,
    story: "A sour-faced dwarf who rarely speaks, letting his cards do the talking. Drogo’s strategy is simple and effective, leaving no room for mercy.",
    level: 13
  },
  {
    name: "Puff the Ponderous",
    age: 72,
    story: "A ponderous dragon who takes his time with every move. Puff’s slow, deliberate playstyle frustrates his opponents, but they can’t deny his wisdom.",
    level: 19
  },
  {
    name: "Fern the Fanciful",
    age: 60,
    story: "A fairy with a love for all things whimsical. Fern’s playstyle is as unpredictable as the wind, often leaving her opponents bewildered and amused.",
    level: 14
  },
  {
    name: "Grogmar the Gruff",
    age: 48,
    story: "A grizzled dwarf who’s seen too many battles and too many bad hands. Grogmar plays with the determination of a man who has nothing left to lose.",
    level: 12
  },
  {
    name: "Luna the Lost",
    age: 102,
    story: "An enigmatic moon elf who appears only on nights of the full moon. Luna’s cards are as mysterious as she is, and just as difficult to read.",
    level: 18
  },
  {
    name: "Thorn the Terrible",
    age: 33,
    story: "A menacing orc who enjoys intimidating his opponents. Thorn’s bark is worse than his bite, but no one’s brave enough to call his bluff.",
    level: 16
  },
  {
    name: "Willow the Wise",
    age: 250,
    story: "An ancient tree spirit who has seen the rise and fall of empires. Willow’s deep knowledge of the world makes her a formidable strategist.",
    level: 20
  },
  {
    name: "Gizelda the Ghastly",
    age: 68,
    story: "A ghostly figure who haunts the card table, Gizelda’s spectral presence sends chills down her opponents’ spines—literally.",
    level: 15
  }
];




function page_build(name,age,storage,level,matching){
  const page = document.createElement("div");
  
  page.innerHTML = `
  <h2>${name}</h2>
  <br><br>
  <p><strong>Age:</strong> ${age}</p>
  <p><strong>Story:</strong> ${storage}</p>
  <p><strong>Level:</strong> ${level}</p>
  <p style="text-align: center; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);">${matching}</p>
  
  `;
  return page;
}

class Book{
  constructor(cross){
     this.cross=cross;
     this.book_html=document.createElement("div");
     this.book_html.classList.add("book");
     this.book_html.id="test-book";
     this.book_html.innerHTML = `
      <div class="pages-container">
          <div class="page" id="page_left">
          </div>
          <div class="page duplex leaf-left" id="test-duplex">
              <div class="page front" id="page_front">
                  
              </div>
              <div class="page back" id="page_back">
                  
              </div>
          </div>
          <div class="page" id="page_right">
          </div>
      </div>
     `


     
    
     //this.init()
  }

  init(){

    this.page_left=document.getElementById("page_left");
    this.page_front=document.getElementById("page_front");
    this.page_back=document.getElementById("page_back");
    this.page_right=document.getElementById("page_right");
    this.duplex = document.getElementById("test-duplex");

    this.curr_left=this.generate_page()
    this.curr_front=this.generate_page()

    const left=this.generate_page()
    left.appendChild(this.cross)
    this.curr_left.appendChild(this.cross.cloneNode(true))
    
    this.change_content(this.page_left,left)
    this.change_content(this.page_front,this.generate_page())
    this.change_content(this.page_back,this.curr_left)
    this.change_content(this.page_right,this.curr_front)

    this.duplex.classList.remove("leaf-right");
    this.duplex.classList.remove("leaf-left");
   // this.duplex.offsetWidth = this.duplex.offsetWidth;
    this.duplex.classList.add("leaf-left");
    

  }
  change_content(page,content){
    page.innerHTML = '';
    page.appendChild(content);
  }
  generate_page(){
    const randomPlayer = cardPlayers[Math.floor(Math.random() * cardPlayers.length)];
    const page = page_build(randomPlayer.name, randomPlayer.age, randomPlayer.story, randomPlayer.level,"Matching");
    return page;
  }
  generate_match_page(){
    
    const page = page_build("Stranger", "???", "It comes through the door and walks right up to you", "???" ,"Find");
    return page;
  }

  turn_page(is_matching){
    
    
    if(is_matching){
      var page_1=this.generate_page()
      var page_2=this.generate_match_page()
    }
    else{
      var page_1=this.generate_page()
      var page_2=this.generate_page()
    }
    this.duplex.classList.remove("leaf-left");
    this.duplex.classList.remove("leaf-right");
    this.duplex.classList.add("leaf-right");


    page_1.appendChild(this.cross)
    this.curr_left.appendChild(this.cross.cloneNode(true))
    this.change_content(this.page_left,this.curr_left)
    this.change_content(this.page_front,this.curr_front)
    this.change_content(this.page_back,page_1)
    this.change_content(this.page_right,page_2)

    this.duplex.classList.remove("leaf-right");
    this.duplex.classList.remove("leaf-left");
    
    const forceReflow = this.duplex.offsetWidth;
    this.duplex.classList.add("leaf-left");

    this.curr_left=page_1
    this.curr_front=page_2
  }
  
  
}
// const book=new Book();


// document.getElementById("test-book").addEventListener(
//   "click",
//   (function () {
//     var state = 1;

//     return function () {
//       book.turn_page(true)
      
//     };
//   })()
// );