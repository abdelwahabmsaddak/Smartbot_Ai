// شريط الأسعار
const ticker = document.getElementById("ticker");
const coins = ["BTC $68,200","ETH $3,050","BNB $590","FLOKI $0.00031","PEPE $0.0000012"];
ticker.textContent = coins.join(" | ");

// دردشة الذكاء الاصطناعي
const chatBody=document.getElementById("chat-body");
const input=document.getElementById("chat-input");
input.addEventListener("keypress",async e=>{
 if(e.key==="Enter"&&input.value.trim()!==""){
   const user=input.value;input.value="";
   const msg=document.createElement("div");
   msg.textContent="🧠 جاري التحليل...";
   chatBody.appendChild(msg);
   chatBody.scrollTop=chatBody.scrollHeight;
   const res=await fetch(`http://127.0.0.1:8000/api/ai/analyze/${user}`);
   const data=await res.json();
   const reply=document.createElement("div");
   reply.textContent=`📊 ${data.ai||"لا توجد بيانات حالياً."}`;
   chatBody.appendChild(reply);
 }
});

function startAI(){alert("جارٍ التحليل الذكي للعملات
