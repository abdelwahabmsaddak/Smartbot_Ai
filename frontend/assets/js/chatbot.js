/* ==========================
   CHATBOT – SmartBot AI
   ========================== */

const chatBody = document.getElementById("chatBody");
const chatInput = document.getElementById("chatInput");

function sendMessage() {
    let msg = chatInput.value.trim();
    if (msg === "") return;

    // User message
    addMessage(msg, "user");
    chatInput.value = "";

    // Simulated AI response (later connected to backend)
    setTimeout(() => {
        botRespond(msg);
    }, 500);
}

/* ==========================
   Add Messages to Chat Box
   ========================== */
function addMessage(text, sender = "bot") {
    let box = document.createElement("div");
    box.classList.add("msg");

    if (sender === "user") {
        box.classList.add("user-msg");
        box.innerHTML = `<p><strong>أنت:</strong> ${text}</p>`;
    } else {
        box.classList.add("bot-msg");
        box.innerHTML = `<p><strong>SmartBot:</strong> ${text}</p>`;
    }

    chatBody.appendChild(box);
    chatBody.scrollTop = chatBody.scrollHeight;
}

/* ==========================
   BOT LOGIC (Static for now)
   ========================== */
function botRespond(userMsg) {

    // Later replaced by real AI (OpenAI API)
    let reply = "جارٍ تحليل سؤالك…";

    if (userMsg.includes("BTC") || userMsg.includes("بيتكوين")) {
        reply = "تحليل سريع للبيتكوين: الاتجاه الحالي صاعد، هناك دعم قوي عند 62,800$.";
    }

    else if (userMsg.includes("ETH") || userMsg.includes("ايثريوم")) {
        reply = "إيثريوم يظهر حركة إيجابية، احتمالية صعود بنسبة 4% خلال 24 ساعة.";
    }

    else if (userMsg.includes("ذهب") || userMsg.includes("Gold")) {
        reply = "الذهب يتحرك في قناة ضيقة، مقاومة عند 2330$ ودعم عند 2310$.";
    }

    else if (userMsg.includes("تحليل") || userMsg.includes("توقعات")) {
        reply = "أحتاج تفاصيل أكثر… اكتب اسم العملة أو السهم.";
    }

    else if (userMsg.includes("مرحبا") || userMsg.includes("سلام")) {
        reply = "مرحبا عبدالوهاب 🌟 أنا SmartBot، جاهز نعاونك في أي تحليل!";
    }

    else {
        reply = "استفسارك غير واضح… جرب كتابة اسم العملة أو السهم للحصول على تحليل.";
    }

    addMessage(reply, "bot");
}

/* ==========================
   Toggle Chat Window
   ========================== */
function toggleChat() {
    let box = document.getElementById("chatbot");
    box.style.display = box.style.display === "block" ? "none" : "block";
}
