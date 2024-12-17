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
    <input type="text" name="mana" required>
    <label for="color">Color:</label>
    <select id="color" name="color">
      <option value="red">red</option>
      <option value="blue">blue</option>
      <option value="green">green</option>
      <option value="white">white</option>
      <option value="black">black</option>
    </select>

    <label for="rarity">Rarity:</label>
    <select id="rarity" name="rarity">
      <option value="Common">Common</option>
      <option value="Uncommon">Uncommon</option>
      <option value="Rare">Rare</option>
      <option value="Mythic Rare">Mythic Rare</option>
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
        <input type="checkbox" name="buff" value="reach">
        <label for="reach">Reach</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="trample">
        <label for="trample">Trample</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="flying">
        <label for="flying">Flying</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="haste">
        <label for="haste">Haste</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="summoning_sickness">
        <label for="summoning_sickness">Summoning Sickness</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="flash">
        <label for="flash">Flash</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="lifelink">
        <label for="lifelink">Lifelink</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="vigilance">
        <label for="vigilance">Vigilance</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="double_strike">
        <label for="double_strike">Double Strike</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="menace">
        <label for="menace">Menace</label>
      </span>
      <span class="buff-option">
        <input type="checkbox" name="buff" value="hexproof">
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

    const button_submit=document.createElement("button")
    button_submit.textContent="Submit"
    const [dropZone,preview]=this.create_image_input()
    button_submit.addEventListener("click",async (event)=>{
      event.preventDefault(); 
      const formData = new FormData(form);

      this.creature_json.init_name=formData.get("name")
      this.creature_json.init_mana_cost=formData.get("mana")
      this.creature_json.init_color=formData.get("color")
      this.creature_json.init_type_creature=formData.get("type_creature")
      this.creature_json.init_type_card=formData.get("type_creature")
      this.creature_json.init_actual_live=Number(formData.get("health"))
      this.creature_json.init_actual_power=Number(formData.get("attack"))
      this.creature_json.init_type="Creature"
      this.creature_json.init_rarity=formData.get("rarity")
      this.creature_json.init_content=formData.get("description")
      this.creature_json.init_image_path=preview.querySelector('img').src
      // for (let [key, value] of formData.entries()) {
      //   console.log(key, value);
      // }
      const selectedBuffs = formData.getAll("buff");
      this.creature_json.init_keyword_list=selectedBuffs
      // console.log(selectedBuffs)
      this.creature_json.select_object_range=formData.get("selector_target")

      for (const name in code_editor.element_dict) {
        const element=code_editor.element_dict[name][0]
        const editor=code_editor.element_dict[name][1]
        this.creature_json[name]=code_editor.get_code_element(editor)
        // console.log(code_editor.get_code_element(editor))
      }
      console.log(this.creature_json)

      const response=await fetch("/add_studio_card",{
        method:"POST",
        headers: { "Content-Type": "application/json" },
        body:JSON.stringify(this.creature_json)
      })
      const data=await response.json()
      console.log(data)
    })

    
    form.appendChild(dropZone)
    form.appendChild(preview)
    form.appendChild(button_submit)
    
    
    

    return form
  }


  create_image_input(){
    const dropZone = document.createElement('div');
    dropZone.classList.add("drop-zone")
    const preview = document.createElement('div');
    preview.classList.add("preview-image")
    // 阻止默认行为
    for (const eventName of ['dragenter', 'dragover', 'dragleave']){
        dropZone.addEventListener(eventName, e => e.preventDefault());
    }

    // 鼠标拖入时添加视觉提示
    dropZone.addEventListener('dragover', () => dropZone.classList.add('hover'));
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('hover'));

    // 处理图片拖放
    dropZone.addEventListener('drop', event => {
        event.preventDefault()
        dropZone.classList.remove('hover');

        const files = event.dataTransfer.files; // 获取拖放的文件
        console.log(files)
        
        if (files.length > 0) {
            const file = files[0];

            // 检查是否是图片文件
            if (!file.type.startsWith('image/')) {
                alert('Please drag and drop image file');
                return;
            }

            // 使用 FileReader 读取文件
            processImage(file, (processedImage) => {
                console.log("处理后的图片：", processedImage);
    
                // 示例：将处理后的图片显示到页面
                const img = document.createElement('img');
                //console.log(e.target.result)
                img.classList.add("preview-image-img")
                img.src = processedImage;
                preview.innerHTML = ''; // 清空之前的内容
                preview.appendChild(img);
            });
            // const reader = new FileReader();
            // reader.onload = e => {
            //     // 创建 img 元素显示图片
            //     const img = document.createElement('img');
            //     console.log(e.target.result)
            //     img.src = e.target.result;
            //     preview.innerHTML = ''; // 清空之前的内容
            //     preview.appendChild(img);
            // };
            // reader.readAsDataURL(file);
        }
    });
    return [dropZone,preview]
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
    return afterFirstLineCode.substring(1)
  }
}


document.addEventListener('DOMContentLoaded', () => {
    // 页面加载完成后执行的初始化代码
    const editor = new Editor();
    const element=editor.create_page_creature();
    console.log(element)
    document.getElementById("editor").appendChild(element)
});


function processImage(file, callback) {
  const reader = new FileReader();
  const img = new Image();

  reader.onload = function(event) {
      img.src = event.target.result; // 加载图片
  };

  img.onload = function() {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");

      // 设置目标大小为 1024x1024
      const targetSize = 1024;
      canvas.width = targetSize;
      canvas.height = targetSize;

      // 获取图片的原始宽高
      const { width: imgWidth, height: imgHeight } = img;

      // 计算缩放比例和偏移量（居中裁剪）
      const scale = Math.max(targetSize / imgWidth, targetSize / imgHeight);
      const scaledWidth = imgWidth * scale;
      const scaledHeight = imgHeight * scale;
      const offsetX = (targetSize - scaledWidth) / 2;
      const offsetY = (targetSize - scaledHeight) / 2;

      // 绘制缩放和裁剪后的图片到 canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, offsetX, offsetY, scaledWidth, scaledHeight);

      // 导出处理后的图片为 Base64 或 Blob
      callback(canvas.toDataURL("image/jpeg")); // Base64 格式
      // 如果需要 Blob，可以用 canvas.toBlob
  };

  reader.readAsDataURL(file); // 读取文件内容为 Base64
}