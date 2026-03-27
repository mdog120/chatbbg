<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ChatBBG</title>

  <!-- fonts -->
  <link rel="preconAnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,600&display=swap" rel="stylesheet">

  <!-- math.js: numeric + expression parsing -->
  <script defer src="https://cdn.jsdelivr.net/npm/mathjs@12.4.2/lib/browser/math.js"></script>

  <!-- nerdamer: symbolic algebra -->
  <script defer src="https://cdn.jsdelivr.net/npm/nerdamer@1.1.13/all.min.js"></script>
  <!-- nerdamer calculus plugin (integrals/derivatives) -->
  <script defer src="https://cdn.jsdelivr.net/npm/nerdamer@1.1.13/Calculus.min.js"></script>

  <style>
    :root{
      --bg: #ffffff;
      --ink: #1f1a22;
      --muted: #6f6470;
      --line: rgba(31, 26, 34, .12);

      --pink: #ff5fb6;
      --pink2:#ff8ad0;
      --pinkWash: rgba(255, 95, 182, .10);

      --shadow: 0 18px 40px rgba(31, 26, 34, .10);
      --radius: 18px;
      --radius2: 28px;

      --serif: "Fraunces", ui-serif, Georgia, serif;
      --sans: "DM Sans", ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
    }

    *{ box-sizing:border-box; }
    html, body{ height:100%; }
    body{
      margin:0;
      background: var(--bg);
      color: var(--ink);
      font-family: var(--sans);
      overflow:hidden;
    }

    .page{
      height:100%;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:28px;
      background:
        radial-gradient(900px 520px at 15% 15%, rgba(255, 95, 182, .06), transparent 60%),
        radial-gradient(900px 520px at 85% 25%, rgba(255, 138, 208, .06), transparent 60%),
        radial-gradient(800px 460px at 55% 95%, rgba(255, 95, 182, .04), transparent 55%),
        #fff;
    }

    .shell{
      width: min(980px, 100%);
      height: min(780px, 100%);
      border: 1px solid var(--line);
      border-radius: var(--radius2);
      box-shadow: var(--shadow);
      background: rgba(255,255,255,.86);
      backdrop-filter: blur(10px);
      overflow:hidden;
      display:flex;
      flex-direction:column;
    }

    header{
      padding: 22px 22px 14px;
      border-bottom: 1px solid var(--line);
      display:flex;
      align-items:flex-end;
      justify-content:space-between;
      gap:16px;
      background: rgba(255,255,255,.82);
    }

    .title{
      min-width:0;
    }
    .title h1{
      margin:0;
      font-family: var(--serif);
      font-weight: 600;
      letter-spacing: .2px;
      font-size: 26px;
      line-height: 1.05;
    }
    .title p{
      margin:8px 0 0;
      font-size: 13px;
      color: var(--muted);
      max-width: 70ch;
    }

    .chat{
      flex:1;
      overflow:auto;
      padding: 22px;
      display:flex;
      flex-direction:column;
      gap:14px;
      scroll-behavior:smooth;
    }

    .row{
      display:flex;
      gap:10px;
      align-items:flex-end;
    }
    .row.you{ justify-content:flex-end; }

    .bubble{
      max-width: min(760px, 90%);
      padding: 12px 14px;
      border-radius: var(--radius);
      border: 1px solid var(--line);
      background: #fff;
      line-height: 1.5;
      font-size: 15px;
      white-space: pre-wrap;
      position:relative;
    }

    .bubble.bbg{
      background: linear-gradient(180deg, #fff, var(--pinkWash));
      border-color: rgba(255,95,182,.22);
    }

    .bubble.you{
      background: #fff;
      border-color: rgba(255,95,182,.45);
      box-shadow: 0 10px 18px rgba(255,95,182,.10);
    }

    .meta{
      margin-top: 8px;
      font-size: 12px;
      color: var(--muted);
      display:flex;
      gap:8px;
      align-items:center;
    }
    .dotsep{
      width:3px;height:3px;border-radius:50%;
      background: rgba(111,100,112,.7);
      display:inline-block;
    }

    .typing{
      display:inline-flex;
      gap:6px;
      align-items:center;
      padding:2px 0;
    }
    .td{
      width:7px;height:7px;border-radius:999px;
      background: var(--pink);
      opacity:.55;
      animation: bounce 1s infinite ease-in-out;
    }
    .td:nth-child(2){ animation-delay:.15s; }
    .td:nth-child(3){ animation-delay:.3s; }
    @keyframes bounce{
      0%,100%{ transform: translateY(0); opacity:.45; }
      50%{ transform: translateY(-4px); opacity:1; }
    }

    .composer{
      padding: 16px 22px 18px;
      border-top: 1px solid var(--line);
      background: rgba(255,255,255,.88);
    }
    .box{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 10px 10px 10px 14px;
      display:flex;
      gap:10px;
      align-items:flex-end;
      background: #fff;
      box-shadow: 0 14px 26px rgba(31,26,34,.08);
    }
    textarea{
      width:100%;
      border:none;
      outline:none;
      resize:none;
      font-family: var(--sans);
      font-size: 15px;
      line-height: 1.5;
      padding: 8px 4px;
      max-height: 150px;
      background: transparent;
    }
    .send{
      width: 46px;
      height: 46px;
      border:none;
      cursor:pointer;
      border-radius: 999px;
      background: linear-gradient(135deg, var(--pink), var(--pink2));
      color:#fff;
      font-weight: 800;
      box-shadow: 0 14px 24px rgba(255,95,182,.22);
      transition: transform .08s ease;
    }
    .send:active{ transform: translateY(1px); }

    .footerline{
      margin-top: 10px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      flex-wrap:wrap;
      font-size: 12px;
      color: var(--muted);
    }
    .disclaimer{
      text-align:center;
      width:100%;
      margin-top: 8px;
      font-size: 12px;
      color: var(--muted);
    }

    @media (max-width: 640px){
      .page{ padding:14px; }
      header{ padding:18px 16px 12px; }
      .chat{ padding:16px; }
      .composer{ padding:14px 16px 16px; }
      .title p{ max-width: 48ch; }
    }
  </style>
</head>

<body>
  <div class="page">
    <div class="shell">
      <header>
        <div class="title">
          <h1>ChatBBG</h1>
          <p>Ask me literally anything ✿ I’m cute, a bit sassy, and occasionally wrong (like all icons). Also yes, I do integrals now.</p>
        </div>
      </header>

      <section class="chat" id="chat"></section>

      <div class="composer">
        <div class="box">
          <textarea id="input" rows="1" placeholder="Message ChatBBG… (try: lol / bruh / bye / integral of 2x dx)"></textarea>
          <button class="send" id="sendBtn" title="Send">➤</button>
        </div>

        <div class="footerline">
          <span>Enter = send • Shift+Enter = new line</span>
          <span>No chat history saved</span>
        </div>

        <div class="disclaimer">ChatBBG can make mistakes. Check important info.</div>
      </div>
    </div>
  </div>

  <script>
    // -------- UI helpers --------
    const chat = document.getElementById("chat");
    const input = document.getElementById("input");
    const sendBtn = document.getElementById("sendBtn");

    function autoGrow(el){
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 150) + "px";
    }
    input.addEventListener("input", () => autoGrow(input));

    function addBubble(text, who="bbg"){
      const row = document.createElement("div");
      row.className = "row " + (who === "you" ? "you" : "bbg");

      const bubble = document.createElement("div");
      bubble.className = "bubble " + (who === "you" ? "you" : "bbg");
      bubble.textContent = text;

      const meta = document.createElement("div");
      meta.className = "meta";
      const name = document.createElement("span");
      name.textContent = who === "you" ? "You" : "ChatBBG";
      const sep = document.createElement("span");
      sep.className = "dotsep";
      const time = document.createElement("span");
      time.textContent = "just now";

      meta.appendChild(name); meta.appendChild(sep); meta.appendChild(time);
      bubble.appendChild(meta);

      row.appendChild(bubble);
      chat.appendChild(row);
      chat.scrollTop = chat.scrollHeight;
    }

    function addTyping(){
      const row = document.createElement("div");
      row.className = "row bbg";
      row.id = "typingRow";

      const bubble = document.createElement("div");
      bubble.className = "bubble bbg";
      bubble.innerHTML = `
        <span class="typing" aria-label="ChatBBG is typing">
          <span class="td"></span><span class="td"></span><span class="td"></span>
        </span>
        <div class="meta"><span>ChatBBG</span><span class="dotsep"></span><span>typing…</span></div>
      `;
      row.appendChild(bubble);
      chat.appendChild(row);
      chat.scrollTop = chat.scrollHeight;
    }

    function removeTyping(){
      document.getElementById("typingRow")?.remove();
    }

    // -------- Brain helpers --------
    const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
    const norm = (s) => (s || "").toLowerCase().trim();
    const words = (s) => (s.toLowerCase().match(/[a-z']+/g) || []);
    const wordSet = (s) => new Set(words(s));

    // Normalize common teen shorthand (tiny upgrades)
    function normalizeText(s){
      return norm(s)
        .replace(/\bim\b/g, "i'm")
        .replace(/\bu\b/g, "you")
        .replace(/\br\b/g, "are")
        .replace(/\bpls\b/g, "please")
        .replace(/\bplz\b/g, "please");
    }

    // -------- Teen Slang + Intent Pack --------
    // These run BEFORE categories so "bye" doesn't get ignored.
    const INTENTS = [
      {
        name: "goodbye",
        match: [
          "bye","goodbye","cya","see ya","see you","later","ttyl","gtg","gotta go","brb",
          "peace","im leaving","i'm leaving","good night","goodnight","gn"
        ],
        replies: [
          "bye bestie ✿ go be iconic 😌",
          "cya ✿ don’t forget me when you’re famous.",
          "ttyl ✿ and drink water. i’m serious.",
          "goodnight ✿ sleep like a princess (with boundaries)."
        ]
      },
      {
        name: "greeting",
        match: ["hi","hello","hey","hii","hiii","hiya","yo","sup","what's up","whats up"],
        replies: [
          "hi bestie ✿ what’s the vibe today?",
          "hey ✿ i’m here. i’m cute. i’m listening.",
          "hiii ✿ say less. what do we need?"
        ]
      },
      {
        name: "lol",
        match: ["lol","lmao","lmfao","haha","hehe","rofl","💀","😭"],
        replies: [
          "STOPPP 💀",
          "lol i’m screaming (silently).",
          "that’s actually funny… i’ll allow it.",
          "ur so real for that 😭"
        ]
      },
      {
        name: "bruh",
        match: ["bruh","bro","girl bye","pls","pleaseee"],
        replies: [
          "bruh… 💀",
          "bro i felt that in my soul.",
          "girl BYE 😭 (affectionate)",
          "pls… i’m trying to be mature but i can’t."
        ]
      },
      {
        name: "idk",
        match: ["idk","i don't know","i dont know","idc","i don't care","i dont care"],
        replies: [
          "idk either bestie 😭 but we can figure it out together.",
          "valid ✿ want me to give options?",
          "ok mood. give me context and i’ll guess responsibly."
        ]
      },
      {
        name: "ok_short",
        // exact short messages
        exact: ["k","kk","ok","okay","alr","aight","bet","sure"],
        replies: [
          "okie ✿",
          "bet 😌",
          "period.",
          "slay. next."
        ]
      },
      {
        name: "nah",
        match: ["nah","nope","nvm","never mind","nevermind"],
        replies: [
          "fair ✿ i respect the nah.",
          "ok mood.",
          "valid. do you wanna switch topics?"
        ]
      },
      {
        name: "terms_of_endearment",
        match: ["baby boo","babes","babe","bestie","pookie","boo","queen","girlie","girly"],
        replies: [
          "hey baby boo 😌 what’s the situation?",
          "hi bestie ✿ tell me everything.",
          "pookieeee ✿ i’m listening.",
          "ok queen ✿ what do you need?"
        ]
      },
      {
        name: "internet_slang",
        match: ["fr","ngl","lowkey","highkey","sus","cap","no cap","ikr","omg","yikes","oop","periodt","ate","slay"],
        replies: [
          "fr fr.",
          "ngl… you might be right.",
          "lowkey? highkey? i’m intrigued.",
          "no cap, that’s wild.",
          "ikr ✿ like hello??",
          "yikes… 😭",
          "oop—",
          "PERIODT."
        ]
      },
      {
        name: "compliment",
        match: ["cute","pretty","love you","smart","funny","icon","slay","ate"],
        replies: [
          "stoppp ✿ you’re gonna inflate my ego.",
          "aw thank you ✿ i’m blushing in hex codes.",
          "you’re sweet ✿ i’ll remember this… until you refresh."
        ]
      },
      {
        name: "thanks",
        match: ["thanks","thank you","thx","ty","appreciate it"],
        replies: [
          "of course ✿ i was coded for this.",
          "anytime bestie ✿ now go be iconic.",
          "period ✿ you’re welcome."
        ]
      },
      {
        name: "whoareyou",
        match: ["who are you","what are you","what can you do","help","commands"],
        replies: [
          "I can help with anything, but I do have limitations.\n\nTry:\n• hair / makeup / studying / boy tips\n• math like 2+2\n• calculus like integral of 2x dx",
          "I’m ChatBBG ✿ cute assistant energy.\nI can do advice + math + calculus.\nIf i glitch… blame JavaScript."
        ]
      }
    ];

    function detectIntent(text){
      const t = normalizeText(text);
      const stripped = t.replace(/[^\w\s']/g, "").trim();

      for(const intent of INTENTS){
        if(intent.exact && intent.exact.includes(stripped)) return intent;
        if(intent.match){
          for(const ph of intent.match){
            if(stripped === ph) return intent;
            if(t.includes(ph)) return intent;
          }
        }
      }
      return null;
    }

    // -------- Categories (advice) --------
    const routes = [
      { name: "hair tips",
        words: ["hair","frizz","curl","curly","coily","shampoo","conditioner","scalp","split","ends","heat","damage"],
        phrases: ["split ends","oily scalp","dry scalp","heat damage"]
      },
      { name: "makeup tips",
        words: ["makeup","foundation","concealer","blush","mascara","eyeliner","lip","brows","contour","highlighter","primer","powder","bronzer"],
        phrases: ["setting spray","under eye","soft glam","full glam"]
      },
      { name: "weight management",
        words: ["weight","lose","loss","fat","calorie","calories","diet","workout","gym","steps","protein","cardio"],
        phrases: ["weight loss","calorie deficit","lose weight"]
      },
      { name: "studying help",
        words: ["study","studying","homework","assignment","exam","test","quiz","notes","focus","procrastinate","revision"],
        phrases: ["study plan","practice questions"]
      },
      { name: "boy tips",
        words: ["boy","crush","dating","date","relationship","situationship","ghosting","text","red","flag","green"],
        phrases: ["text him","text her","talking stage","red flag","green flag"]
      },
    ];

    function detectCategory(text){
      const t = normalizeText(text);
      const ws = wordSet(t);

      let best = { name:"general", score:0 };
      for(const r of routes){
        let score = 0;
        for(const ph of (r.phrases || [])) if(t.includes(ph)) score += 3;
        for(const w of (r.words || [])) if(ws.has(w)) score += 1;
        if(score > best.score) best = { name:r.name, score };
      }
      return best.score >= 1 ? best.name : "general";
    }

    function replyByCategory(category){
      const safety = "If anything feels serious/unsafe, talk to a trusted adult or a professional 💗";

      if(category === "hair tips"){
        return pick([
          "Hair tips time ✿ let’s fix the drama.\n\nTell me your hair type + what’s happening.\n• frizz: microfiber towel + leave-in\n• dry ends: trim + oil only on ends\n• oily scalp: shampoo twice, condition mid-length to ends\n• heat: protectant + lower temp",
          "Ok hair bestie ✿ quick routine:\n1) shampoo scalp only\n2) conditioner ends only\n3) leave-in on damp hair\n4) air dry or low heat\n\nTell me: straight/wavy/curly/coily?"
        ]);
      }

      if(category === "makeup tips"){
        return pick([
          "Makeup moment ✿ what are we doing—natural, soft glam, or full glam?\n\nQuick wins:\n• blush higher = lifted\n• oily skin: set T-zone only\n• cakey base: use less + damp sponge\n• mascara smudges: tiny powder under eyes",
          "Ok pretty ✿ blush is the personality.\nTell me your skin type + vibe.\n\nAlso: cream blush for dewy, powder blush for staying power."
        ]);
      }

      if(category === "weight management"){
        return pick([
          "Gentle habits ✿ (not medical advice)\nIf you’re under 18: focus on strength + energy.\n\nBasics:\n• balanced plate\n• water + sleep\n• fun movement 3–5x/week\n• no extreme diets\n\n" + safety,
          "Bestie ✿ balance > extremes.\nThink: consistent meals, protein, steps, sleep.\nNo “punishment workouts.” We’re not doing that.\n\n" + safety
        ]);
      }

      if(category === "studying help"){
        return pick([
          "Study mode ✿ let’s cook.\nTell me: subject + due date + what’s confusing.\n\nFast plan:\n1) 25/5 timer x3\n2) active recall\n3) practice questions\n4) tiny checklist",
          "Ok scholar ✿ what class?\nIf you tell me the topic, I’ll make a mini study plan + practice questions."
        ]);
      }

      if(category === "boy tips"){
        return pick([
          "Ok bestie ✿ give me the tea. I’m seated.\n\nRules:\n• if they like you, it won’t be confusing 24/7\n• match energy\n• green flags: consistent + respectful\n• red flags: hot/cold + pressure\n\n" + safety,
          "Boy tips ✿ because someone has to be rational here.\nTell me what happened + what you want.\n\nAnd remember: you’re the prize. 😌"
        ]);
      }

      return null;
    }

    // -------- Calculator (numeric + symbolic) --------
    function libsReady(){
      return (typeof window.math !== "undefined") && (typeof window.nerdamer !== "undefined");
    }

    function cleanExpr(expr){
      return expr.replace(/\s+/g, " ").trim();
    }

    function parseCalculusPrompt(text){
      const t = text.trim();

      let m = t.match(/^(?:integral\s+of|integrate)\s+(.+?)\s+d([a-zA-Z])\s*$/i);
      if(m) return { kind:"integral", expr: cleanExpr(m[1]), variable: m[2] };

      m = t.match(/^(?:derivative\s+of|differentiate)\s+(.+?)(?:\s+(?:wrt|with\s+respect\s+to)\s+([a-zA-Z]))?\s*$/i);
      if(m) return { kind:"derivative", expr: cleanExpr(m[1]), variable: (m[2] || "x") };

      m = t.match(/^simplify\s+(.+)\s*$/i);
      if(m) return { kind:"simplify", expr: cleanExpr(m[1]) };

      return null;
    }

    function parseNumericPrompt(text){
      let t = text.trim();
      t = t.replace(/^what('?s| is)\s+/i, "");
      t = t.replace(/\?+$/g, "").trim();

      const hasDigit = /\d/.test(t);
      const hasMathWord = /\b(sin|cos|tan|sqrt|log|ln|pi|e)\b/i.test(t);
      const hasOperator = /[+\-*/^()]/.test(t);

      if(!(hasOperator && (hasDigit || hasMathWord))) return null;

      const allowed = /^[0-9a-zA-Z+\-*/^().,\s_]+$/;
      if(!allowed.test(t)) return null;

      return cleanExpr(t);
    }

    function formatCalcResult(label, inputExpr, outputExpr){
      const sass = pick([
        "Math served. ✿",
        "Calculator era. ✿",
        "Ok brainy bestie. ✿",
        "Numbers? I fear I ate. ✿"
      ]);
      return `${sass}\n\n${label}\n${inputExpr}\n\nResult\n${outputExpr}`;
    }

    function tryCalculator(userText){
      if(!libsReady()){
        return "Hold on bestie… my math libraries didn’t load 😭\nIf you’re on GitHub Pages, wait a sec and refresh.";
      }

      const calc = parseCalculusPrompt(userText);
      if(calc){
        try{
          if(calc.kind === "integral"){
            const res = window.nerdamer.integrate(calc.expr, calc.variable).toString();
            return formatCalcResult(`Integral (d${calc.variable})`, `∫ ${calc.expr} d${calc.variable}`, `${res} + C`);
          }
          if(calc.kind === "derivative"){
            const res = window.nerdamer.diff(calc.expr, calc.variable).toString();
            return formatCalcResult(`Derivative (wrt ${calc.variable})`, `d/d${calc.variable} [ ${calc.expr} ]`, res);
          }
          if(calc.kind === "simplify"){
            const res = window.nerdamer(calc.expr).simplify().toString();
            return formatCalcResult(`Simplify`, calc.expr, res);
          }
        } catch {
          return "I tried… and the math said “no.” 😭\nTry:\n• integral of 2*x dx\n• derivative of sin(x)\n• simplify (x^2 + 2x + 1)";
        }
      }

      const expr = parseNumericPrompt(userText);
      if(expr){
        try{
          const value = window.math.evaluate(expr);
          return formatCalcResult("Expression", expr, String(value));
        } catch {
          return "That expression is giving… confusing. 😭\nTry:\n• (2+2)*5\n• sqrt(16)\n• sin(pi/2)";
        }
      }

      return null;
    }

    // -------- General fallback --------
    function replyGeneral(){
      return pick([
        "I can help with anything, but I do have limitations due to being created by a 15 year old. ✿\n\nGive me context and i’ll try to be useful (and cute).",
        "ok bestie ✿ i’m listening. what’s the situation?",
        "say less ✿ details pls 👀"
      ]);
    }

    function generateReply(userText){
      // 1) calculator first
      const calc = tryCalculator(userText);
      if(calc) return calc;

      // 2) teen slang + intent pack
      const intent = detectIntent(userText);
      if(intent) return pick(intent.replies);

      // 3) categories
      const cat = detectCategory(userText);
      const catReply = replyByCategory(cat);
      if(catReply) return catReply;

      // 4) fallback
      return replyGeneral();
    }

    // -------- Send --------
    function send(){
      const text = input.value.trim();
      if(!text) return;

      addBubble(text, "you");
      input.value = "";
      autoGrow(input);

      addTyping();
      setTimeout(() => {
        removeTyping();
        addBubble(generateReply(text), "bbg");
      }, 420);
    }

    sendBtn.addEventListener("click", send);
    input.addEventListener("keydown", (e) => {
      if(e.key === "Enter" && !e.shiftKey){
        e.preventDefault();
        send();
      }
    });

    // intro
    addBubble(
      "hi bestie ✿ i’m ChatBBG.\nI can help with anything, but I do have limitations due to being created by a 15 year old.\n\nTry:\n• lol / bruh / idk / nah\n• baby boo\n• bye / ttyl / cya\n• integral of 2x dx\n• blush",
      "bbg"
    ); 
  </script>
</body>
</html> 
 
