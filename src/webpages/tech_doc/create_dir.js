

function create_dir(){
  const titleList = document.getElementById('title_list');

  let types=("h1","h2","h3")
  let class_dic={"h1":"link","h2":"sublink","h3":"subsublink"}
  

  const headings = document.querySelectorAll('h1, h2, h3');
  console.log(headings)

  let div_current_sublink=document.createElement('div');
  let div_current_subsublink=document.createElement('div');
  for (const heading of headings){
    if (heading.id=="company_name"){continue}
    console.log(heading)
    const text = heading.textContent.trim();
    const id=text.replace(/\s+/g, '-').toLowerCase()
    const href = `#${id}`;
    heading.id=id;
    const link = document.createElement('a');

    const tag_name=heading.tagName.toLowerCase()
    const class_=class_dic[tag_name]
    link.className = class_;
    
    link.textContent = text; // 设置 a 标签的文本内容


    // 将新的 a 标签插入到标题后面
    if (tag_name=="h1"){
      const li = document.createElement('li');
      div_current_sublink = document.createElement('div');
      div_current_sublink.className="sublinks"

      li.appendChild(link)
      li.appendChild(div_current_sublink)
      titleList.appendChild(li)
      link.href = href;
      link.addEventListener('dblclick', function(event) {
        
        scrollToTarget(event)

      })
      link.addEventListener('click', function(event) {
          event.preventDefault();
          
      });




    }else if (tag_name=="h2"){
      div_current_subsublink=document.createElement('div');
      div_current_subsublink.className="sublinks"

      div_current_sublink.appendChild(link)
      div_current_sublink.appendChild(div_current_subsublink)
      link.href = href;
      //heading.preventDefault();
      //link.setAttribute('dblclick', 'scrollToTarget(event)');
      link.addEventListener('dblclick', function(event) {
        
        scrollToTarget(event)

      })
      link.addEventListener('click', function(event) {
          event.preventDefault();
          
      });


      

    }else if (tag_name=="h3"){
      div_current_subsublink.appendChild(link)
      link.href = href;
      link.setAttribute('onclick', 'scrollToTarget(event)');

    }


    // 为标题元素添加 id，便于 href 引用
    
  }


}

create_dir()