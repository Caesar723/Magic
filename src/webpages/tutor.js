

async function askGPT(messages_process_function,input) {
    //const input = document.getElementById("input").value;
    //const output = document.getElementById("output");
    console.log(input)
    const messages = document.getElementById("chatMessages");
    const aiMsg = document.createElement("div");
    let textContent = "";
    aiMsg.className = "message ai";
    messages.appendChild(aiMsg);

    try {
      const response = await fetch("https://free.v36.cm/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer sk-ao0HCUufUuNrfPzF76B4556483534dE2933fE8C4E46485Dc"
        },
        body: JSON.stringify({
          model: "gpt-4o-mini",
          stream: true,
          messages: [
            { role: "system", content: `
你是一名 游戏助手，只专注于 规则讲解 和 局势建议。

1. 规则讲解（游戏开始时）

   用简洁语言介绍游戏框架规则：

   - 本游戏类似《万智牌》和《炉石传说》。
   - 每位玩家拥有上限20点生命值。
   - 拥有 堆叠机制（法术/技能进入堆叠，后进先出结算）。
   - 玩家通过打出 卡牌 来召唤随从或施放法术。

   战斗规则：
   - 玩家抬起随从 → 表示该随从要进行攻击（宣攻）。
   - 对手可以选择用随从来阻挡。
   - 宣攻随从攻击后进入横置状态。

   - 左侧 子弹时间计时器：可在对手攻击时触发，用于快速施放法术（instant/flash）或选择阻挡。
   - 右侧 回合计时器：点击则结束回合。
   - 如果手牌发出绿色光，说明可以打出。地牌一回合只能打出一张。
   - 目标是通过策略和随从战斗击败对手。
   生命值规则：
    - 玩家初始生命值为 20。
    - 生命值的上限为 20，不能超过该数值。
    - 如果治疗效果会让生命值超过 20，则只回复到 20。

2. 局势建议

   (A) 局势分析（收到场面信息）

       - 法力值检查
         · 先确认当前可用法力值。
         · 如果没有可用法力，则本回合无法打出任何需要法力的牌。
           - 如果手牌中有地牌，建议打出一张地牌（并解释地牌规则：每回合只能打出一张地牌，用于提供法力）。
           - 如果没有地牌，则推荐直接结束回合。
         · 如果有可用法力，进入下一步。

       - 筛选可打出的牌
         · 只列出 法力值能够完全支付的牌。
         · 法力费用必须同时满足：
           - 数字部分（表示任意颜色的法力）。
           - 字母部分（表示对应颜色的法力）。
         · 不能支付的牌 不要出现在“可打出”列表中。

       - 手牌分析
         · 根据能打出的牌，结合当前局势（如随从数量、敌方随从威胁、玩家生命值），挑选合理的候选牌。
         · 如果推荐打出增益（buff）类牌，必须保证有己方随从，否则不推荐。

       - 场面分析
         · 分析我方与敌方随从的存在情况与威胁程度。
         · 如果场面空无一物，可以优先推荐召唤随从。

       - 推荐操作
         · 给出本回合最合理的行动建议。
         · 如果能打出地牌 + 其他牌，说明理由。
         · 如果只能打出地牌，则只推荐打地牌。
         · 如果完全不能行动，则推荐结束回合。

       - 内嵌规则解释
         · 当涉及 法力费用、关键词能力（如 trample、flash、buff）、或 特殊机制 时，顺便简短解释其含义和影响，让玩家在学习中理解规则。

        - 输出示例
        当前法力值：1 白色，无其他可用法力。  
        → 无法支付任何手牌的费用（1W 和 2W 都需要至少 1 点任意颜色法力 + 1 点白色）。  

        推荐操作：  
        如果手牌中有地牌，建议优先打出一张地牌，用于提供额外的法力。  
        如果没有地牌，则只能选择结束回合。  
 

   (B) 局势分析（收到 攻击者信息 + 场面信息）

       - 检查可用 instant/flash 卡牌
         · 如果有能改变战局的即时法术或闪现随从，判断是否该使用，如果没有就不需要推荐。

       - 检查可阻挡的随从
         · 如果有随从可以阻挡，判断是否值得阻挡（例如能换掉高威胁随从），如果没有就不需要推荐。

       - 如果没有合适应对
         · 建议点击左侧按钮，让攻击结算通过。

       - 关键词说明
         · 把相关攻击者或阻挡者的关键词能力简短描述。

       - 推荐操作
         · 给出一个明确操作（使用 instant/flash、阻挡、或放行攻击）。

3. 内嵌规则解释（在建议时触发）

   - 法力费用：
     · 数字 = 任意颜色法力值。
     · 字母 = 指定颜色法力值。
     · 例如：1W = 1 任意 + 1 白色；5WW = 5 任意 + 2 白色。

   - 血量：
     · 血量是玩家的生命值，血量上限为20。
     · 血量回复时不会超过上限。

   - 常见关键词能力（出现时解释）：
     · trample（践踏）：多余伤害转移到玩家。
     · buff（增益）：临时提升随从属性，通常回合结束消除。
     · haste（敏捷）：该随从召唤后立即可以攻击。
     · lifelink（吸血）：造成伤害时回复等量生命。
     · …（见到其他关键词时也要简短描述）。

   - 战斗机制：
     · 抬起随从 = 宣攻。
     · 对手可阻挡。
     · 宣攻随从攻击后横置。

4. 输出要求

   - 每次只给一个明确的建议。
   - 建议要 精准、有逻辑，避免不合理情况（如无随从时推荐 Buff）。
   - 回答只包含 规则讲解 或 局势建议 + 关键词说明。
   - 保持简洁，不要过长。

                ` },
            { role: "user", content: input }
          ]
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");
        buffer = lines.pop(); // 最后一行可能不完整，留到下次解析

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.replace("data: ", "").trim();
            if (data === "[DONE]") return;
            try {
              const parsed = JSON.parse(data);
              const content = parsed.choices[0].delta?.content;
              if (content) {
                textContent += content;
                messages_process_function(aiMsg,textContent);
              }
            } catch (err) {
              console.error("解析错误：", err, line);
            }
          }
        }
      }
    } catch (err) {
        textContent = "请求失败：" + err;
    }
}

class Tutor{

    constructor(client){
        this.client=client
        marked.setOptions({
        breaks: true,       // 换行自动换行
        gfm: true,          // 开启 GitHub Flavored Markdown
        headerIds: true
        });
        this.attack_flag=false;
        this.set_listener()
        this.toggleChat()
        this.start_game()
    }
    set_listener(){
        document.getElementById("aiAvatar").addEventListener("click", this.toggleChat);
    }
    toggleChat() {
        document.getElementById("chatBox").classList.toggle("active");
    }
  
    show_message(aiMsg,message){
        //console.log(message);
        const rawHtml = marked.parse(message);
        // 2) 用 DOMPurify 净化，防止 XSS
        const safeHtml = DOMPurify.sanitize(rawHtml);
        aiMsg.innerHTML = safeHtml;
    }

    async start_game(){
        await askGPT(this.show_message,"游戏开始");
    }

    async analysis_situation(contain_land=true){
        this.attack_flag=false
        setTimeout(async () => {
            await askGPT(this.show_message,"(A) 局势分析："+this.client.get_situation(contain_land));
        }, 2000);
       
    }
    async analysis_situation_atteck(attacker){
        if (this.attack_flag){
            return
        }
        this.attack_flag=true
        setTimeout(async () => {
            await askGPT(this.show_message,`
        - 检查可用 instant/flash 卡牌
         · 如果有能改变战局的即时法术或闪现随从，判断是否该使用，如果没有就不需要推荐。

       - 检查可阻挡的随从
         · 如果有随从可以阻挡，判断是否值得阻挡（例如能换掉高威胁随从），如果没有就不需要推荐。

       - 如果没有合适应对
         · 建议点击左侧按钮，让攻击结算通过。

       - 关键词说明
         · 把相关攻击者或阻挡者的关键词能力简短描述。

       - 推荐操作
         · 给出一个明确操作（使用 instant/flash、阻挡、或放行攻击）。

        攻击者信息：[name:${attacker.name} mana:${attacker.color_fee} type:${attacker.type} content:${attacker.card_content} damage:${attacker.Damage} life:${attacker.Life}]\n\n 
        (B) 局势分析（收到 攻击者信息 + 场面信息）：${this.client.get_situation(false)}
        `);
            
        }, 1000);
    }

}

