// var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
//   lineNumbers: true,
//   mode: "python",
//   theme: "dracula",
//   indentUnit: 4,
//   tabSize: 4,
//   autoCloseBrackets: true,
//   matchBrackets: true,
//   showCursorWhenSelecting: true
// });
// document.getElementById('card-image').addEventListener('change', function(e) {
//   var file = e.target.files[0];
//   var reader = new FileReader();
//   reader.onload = function(event) {
//       var img = document.getElementById('image-preview');
//       img.src = event.target.result;
//       img.style.display = 'block';
//   }
//   reader.readAsDataURL(file);
// });

// document.getElementById('card-form').addEventListener('submit', function(e) {
//   e.preventDefault();
//   // 这里可以添加发送表单数据的逻辑
//   console.log('表单提交');
// });
function handleDrop(e) {
  e.preventDefault();
  e.stopPropagation();
  
  const files = e.dataTransfer.files;
  if(files.length) {
      handleFiles(files[0]);
  }
  
  e.target.classList.remove('drag-over');
}

function handleDragOver(e) {
  e.preventDefault();
  e.stopPropagation();
  e.target.classList.add('drag-over');
}

function handleDragLeave(e) {
  e.preventDefault();
  e.stopPropagation(); 
  e.target.classList.remove('drag-over');
}

function handleFileSelect(e) {
  const files = e.target.files;
  if(files.length) {
      handleFiles(files[0]);
  }
}

function handleFiles(file) {
  if(!file.type.startsWith('image/')) {
      alert('请上传图片文件!');
      return;
  }

  const reader = new FileReader();
  reader.onload = function(e) {
      const preview = document.getElementById('preview-image');
      preview.src = e.target.result;
      preview.style.display = 'block';
      
      document.querySelector('.drop-zone-content').style.display = 'none';
  }
  reader.readAsDataURL(file);
}





class Editor{
  constructor(){
    this.current_type="creature"

    this.creature_json={
      "init_name":"",
      "init_actual_live":0,
      "init_actual_power":0,
      "init_type_creature":"",
      "init_type":"",
      "init_mana_cost":"",
      "init_color":"",
      "init_type_card":"",
      "init_rarity":"",
      "init_content":"",
      "init_image_path":"",
      "init_keyword_list":[],
      "select_object_range":"",
      "when_enter_battlefield_function":"",
      "when_leave_battlefield_function":"",
      "when_die_function":"",
      "when_start_turn_function":"",
      "when_end_turn_function":"",
      "when_harm_is_done_function":"",
      "when_being_treated_function":"",
      "when_become_attacker_function":"",
      "when_become_defender_function":"",
      "when_kill_creature_function":"",
      "when_start_attcak_function":"",
      "when_start_defend_function":"",
      "when_a_creature_die_function":"",
      "when_an_object_hert_function":"",
      "aura_function":"",
    }
    this.land_json={
      "init_name":"",
      "init_type":"",
      "init_mana_cost":"",
      "init_color":"",
      "init_type_card":"",
      "init_rarity":"",
      "init_content":"",
      "init_image_path":"",
      "init_keyword_list":[],
      "select_object_range":"",
      "when_enter_battlefield_function":"",
      "when_clicked_function":"",
      "when_a_creature_die_function":"",
      "when_an_object_hert_function":"",
      "when_kill_creature_function":"",
      "when_start_turn_function":"",
      "when_end_turn_function":"",
      "aura_function":"",
    }
    this.instant_json={
      "init_name":"",
      "init_type":"",
      "init_mana_cost":"",
      "init_color":"",
      "init_type_card":"",
      "init_rarity":"",
      "init_content":"",
      "init_image_path":"",
      "init_keyword_list":[],
      "select_object_range":"",
      "is_undo":false,
      "card_ability_function":"",
      "when_a_creature_die_function":"",
      "when_an_object_hert_function":"",
      "when_kill_creature_function":"",
      "when_start_turn_function":"",
      "when_end_turn_function":"",
      "aura_function":"",
    }
  
    this.sorcery_json={
      "init_name":"",
      "init_type":"",
      "init_mana_cost":"",
      "init_color":"",
      "init_type_card":"",
      "init_rarity":"",
      "init_content":"",
      "init_image_path":"",
      "init_keyword_list":[],
      "select_object_range":"",
      "card_ability_function":"",
      "when_a_creature_die_function":"",
      "when_an_object_hert_function":"",
      "when_kill_creature_function":"",
      "when_start_turn_function":"",
      "when_end_turn_function":"",
      "aura_function":"",
    }
  }
  
  create_page_creature(){
    const form=document.createElement("form")
    form.innerHTML=`
    <label for="name">Name:</label>
    <input type="text" name="name" required>
    <label for="mana">Mana:</label>
    <input type="number" name="mana" min="0" required>
    <label for="color">Color:</label>
    <select id="color" name="color">
      <option value="red">red</option>
      <option value="blue">blue</option>
      <option value="green">green</option>
      <option value="white">white</option>
      <option value="black">black</option>
    </select>
    
    <label for="type_creature">Type Creature:</label>
    <input type="text" name="type_creature" required>
    <label for="attack">Attack:</label>
    <input type="number" name="attack" min="0" required>
    <label for="health">Health:</label>
    <input type="number" name="health" min="1" required>
    <label for="description">Description:</label>
    <textarea name="description" required></textarea>
    <label>Buff Selector</label>
    <div class="buff-options">
      <span class="buff-option">
        <input type="checkbox" name="reach">
        <label for="reach">Reach</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="trample">
        <label for="trample">Trample</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="flying">
        <label for="flying">Flying</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="haste">
        <label for="haste">Haste</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="summoning_sickness">
        <label for="summoning_sickness">Summoning Sickness</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="flash">
        <label for="flash">Flash</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="lifelink">
        <label for="lifelink">Lifelink</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="vigilance">
        <label for="vigilance">Vigilance</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="double_strike">
        <label for="double_strike">Double Strike</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="menace">
        <label for="menace">Menace</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="hexproof">
        <label for="hexproof">Hexproof</label>
      </span>
    </div>
    <label for="selector_target">Selector Target:</label>
    <select id="selector_target" name="selector_target">
      <option value="">none</option>
      <option value="all_roles">all_roles</option>
      <option value="opponent_roles">opponent_roles</option>
      <option value="your_roles">your_roles</option>
      <option value="all_creatures">all_creatures</option>
      <option value="opponent_creatures">opponent_creatures</option>
      <option value="your_creatures">your_creatures</option>
      <option value="all_lands">all_lands</option>
      <option value="opponent_lands">opponent_lands</option>
      <option value="your_lands">your_lands</option>
    </select>
    `
    const label_function=document.createElement("label")
    label_function.textContent="Event Function:"
    form.appendChild(label_function)
    const code_area=document.createElement("div")
    code_area.classList.add("code-editor")
    
    const selector_function=document.createElement("select")
    selector_function.id="selector_function"
    selector_function.name="selector_function"
    form.appendChild(selector_function)
    form.appendChild(code_area)
    const functions=["when_enter_battlefield_function","when_leave_battlefield_function","when_die_function","when_start_turn_function","when_end_turn_function","when_harm_is_done_function","when_being_treated_function","when_become_attacker_function","when_become_defender_function","when_kill_creature_function","when_start_attcak_function","when_start_defend_function","when_a_creature_die_function","when_an_object_hert_function","aura_function"]
    const code_editor=new Code_Editor(functions)
    code_editor.element_create()
    for (const function_name of functions){
      const option=document.createElement("option")
      option.value=function_name
      option.textContent=function_name
      selector_function.appendChild(option)
    }
    selector_function.addEventListener("change",()=>{

      const element = code_editor.element_dict[selector_function.value][0];
      const editor=code_editor.element_dict[selector_function.value][1]
      editor.refresh();
      code_area.innerHTML = "";
      console.log(code_editor.element_dict[selector_function.value])
      code_area.appendChild(element);
    })
    
    
    

    return form
  }
}

class Code_Editor{
  function_dict={
    "when_enter_battlefield_function":`async def when_enter_battlefield(self,player,opponent,selected_object):\n\n`,
    "when_leave_battlefield_function":`async def when_leave_battlefield(self,player= None, opponent = None,name:str='battlefield'):\n\n`,
    "when_die_function":`async def when_die(self,player= None, opponent = None):\n\n`,
    "when_start_turn_function":`async def when_start_turn(self,player= None, opponent = None):\n\n`,
    "when_end_turn_function":`async def when_end_turn(self,player= None, opponent = None):\n\n`,
    "when_harm_is_done_function":`async def when_harm_is_done(self,card,value,player= None, opponent = None):\n\n`,
    "when_being_treated_function":`async def when_being_treated(self,card,value,player= None, opponent = None):\n\n`,
    "when_become_attacker_function":`async def when_become_attacker(self,player= None, opponent = None):\n\n`,
    "when_become_defender_function":`async def when_become_defender(self,player= None, opponent = None):\n\n`,
    "when_kill_creature_function":`async def when_kill_creature(self,player= None, opponent = None):\n\n`,
    "when_start_attcak_function":`async def when_start_attack(self,player= None, opponent = None):\n\n`,
    "when_start_defend_function":`async def when_start_defend(self,player= None, opponent = None):\n\n`,
    "when_a_creature_die_function":`async def when_a_creature_die(self,player= None, opponent = None):\n\n`,
    "when_an_object_hert_function":`async def when_an_object_hert(self,player= None, opponent = None):\n\n`,
    "aura_function":`async def aura(self,player= None, opponent = None):\n\n`,
    "card_ability_function":`async def card_ability(self,player,opponent,selected_object):\n\n`,
    "when_clicked_function":`async def when_clicked(self,player= None, opponent = None):\n\n`,
  }
  constructor(code_names){
    this.code_names=code_names
    
  }
  element_create(){
    this.element_dict={}
    this.code_names.forEach(name=>{
      const code_element=document.createElement("div")
      code_element.classList.add("code-editor")
      
      const textarea=document.createElement("textarea")
      code_element.appendChild(textarea)
      const editor = CodeMirror.fromTextArea(textarea, {
        lineNumbers: true,
        mode: "python",
        theme: "dracula",
        indentUnit: 4,
        tabSize: 4,
        autoCloseBrackets: true,
        matchBrackets: true,
        showCursorWhenSelecting: true,
        viewportMargin: Infinity // 确保代码镜像编辑器的高度自适应内容
      });
      
      console.log(editor,name)
      console.log(this.function_dict[name])
      // editor.setValue("");

      editor.replaceRange(this.function_dict[name], {line: 0, ch: 0}, {line: 0, ch: editor.getLine(0).length});
      editor.markText({line: 0, ch: 0}, {line: 0, ch: editor.getLine(0).length}, {
        readOnly: true,  // 标记为只读
        inclusiveLeft: true,
        inclusiveRight: true,
        indentUnit: 4,
        tabSize: 4,
        mode: "python",
        theme: "dracula",
        className: "readonly-line"  // 可选：为只读内容添加样式
      });
      editor.refresh();
      this.element_dict[name]=[code_element,editor]
    })
  }
  get_code_element(editor){
    const firstLineEnd = editor.getLine(0).length; // 第一行长度
    const totalLines = editor.lineCount(); // 总行数

    // 获取从第二行到最后一行的内容
    const afterFirstLineCode = editor.getRange(
        { line: 1, ch: 0 }, // 第二行开始
        { line: totalLines - 1, ch: editor.getLine(totalLines - 1).length } // 最后一行末尾
    );
    return afterFirstLineCode
  }
}


document.addEventListener('DOMContentLoaded', () => {
    // 页面加载完成后执行的初始化代码
    const editor = new Editor();
    const element=editor.create_page_creature();
    console.log(element)
    document.getElementById("editor").appendChild(element)
});
