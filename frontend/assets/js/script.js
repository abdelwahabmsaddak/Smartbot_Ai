// تحميل الأسعار من CoinGecko
async function loadSignals(){
  const el = document.getElementById("signals");
  try{
    const res = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,floki,pepe');
    const data = await res.json();
    let html = `<table style="margin:auto;width:80%;border-collapse:collapse;">
      <tr><th>العملة</th><th>السعر</th><th>تغير 24h</th><th>المخطط</th></tr>`;
    for(const c of data){
      const color = c.price_change_percentage_24h >= 0 ? '#00ff88' : '#ff4d4d';
      html += `
      <tr>
        <td>${c.name}</td>
        <td>$${c.current_price.toFixed(3)}</td>
        <td style="color:${color}">${c.price_change_percentage_24h.toFixed(2)}%</td>
        <td><canvas id="chart-${c.id}" width="100" height="40"></canvas></td>
      </tr>`;
    }
    html += '</table>';
    el.innerHTML = html;
    for(const c of data){
      const hist = await fetch(`https://api.coingecko.com/api/v3/coins/${c.id}/market_chart?vs_currency=usd&days=7`);
      const histData = await hist.json();
      drawMiniChart(`chart-${c.id}`, histData.prices.map(p => p[1]), c.price_change_percentage_24h >= 0);
    }
  }catch(e){
    el.innerHTML = "⚠️ خطأ أثناء تحميل البيانات";
  }
}

function drawMiniChart(id, data, positive){
  const c = document.getElementById(id);
  if(!c) return;
  const ctx = c.getContext("2d");
  const max = Math.max(...data);
  const min = Math.min(...data);
  ctx.strokeStyle = positive ? "#00ff88" : "#ff4d4d";
  ctx.beginPath();
  data.forEach((v,i)=>{
    const x = (i/(data.length-1))*c.width;
    const y = c.height - ((v-min)/(max-min))*c.height;
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.stroke();
}

// دردشة الذكاء الاصطناعي
function addMsg(txt, cls){
  const box = document.getElementById("chatBox");
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.textContent = txt;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

async function sendMsg(){
  const input = document.getElementById("userInput");
  const msg = input.value.trim();
  if(!msg) return;
  addMsg(msg, "user");
  input.value = "";
  addMsg("🤖 جارٍ التحليل...", "bot");

  setTimeout(()=>{
    const ans = simpleAnalyze(msg);
    addMsg(ans, "bot");
  }, 800);
}

function simpleAnalyze(text){
  const t = text.toLowerCase();
  if(t.includes("bitcoin")) return "تحليل Bitcoin 🟡:\nالسوق مستقر جزئيًا مع دعم قوي فوق 60k. إشارة شراء محتملة.";
  if(t.includes("floki")) return "تحليل Floki 🐶:\nنشاط مجتمعي متزايد، احتمال صعودي محدود بسبب ضعف السيولة.";
  if(t.includes("pepe")) return "تحليل Pepe 🐸:\nتذبذب عالٍ، يفضل المضاربة القصيرة فقط.";
  return "تحليل عام 📊:\nيرجى تحديد العملة بدقة للحصول على تحليل مخصص.";
}

if(document.getElementById("signals")) loadSignals();
/********************
 *  BLOG / ARTICLES *
 ********************/

// مسار باك-إند (اختياري). اتركه فارغًا ليعمل وضع المحاكاة.
// إن كان عندك FastAPI endpoint مثل /api/generate-article ضع قيمته هنا.
const BACKEND_URL = ""; // مثال: "http://localhost:8000"

function loadArticles(){
  // نحفظ ونقرأ من LocalStorage للمقالات
  const list = JSON.parse(localStorage.getItem("sb_articles") || "[]");
  window.__ARTS = list;
  renderArticles();
}

function saveArticles(arr){
  localStorage.setItem("sb_articles", JSON.stringify(arr));
  window.__ARTS = arr;
  renderArticles();
}

// إنشاء سلاگ بسيط
function slugify(s){
  return s.toLowerCase().replace(/[^\u0600-\u06FF\w]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'').slice(0,80);
}

// توليد مقال (إما عبر الباك-إند أو محاكاة محلية)
async function generateArticle(){
  const topic = document.getElementById("topic").value.trim();
  const lang = document.getElementById("lang").value;
  const status = document.getElementById("genStatus");
  if(!topic){ alert("اكتب موضوع المقال أولاً"); return; }

  status.textContent = "⏳ جارٍ توليد المقال بالذكاء الاصطناعي...";
  try{
    let result;
    if(BACKEND_URL){
      // استدعاء باك-إند (FastAPI مثلاً)
      const r = await fetch(`${BACKEND_URL}/api/generate-article?topic=${encodeURIComponent(topic)}&lang=${lang}`);
      result = await r.json();
    }else{
      // محاكاة محلية
      result = mockArticle(topic, lang);
    }

    if(result.error){
      status.textContent = "⚠️ فشل التوليد: " + result.error;
      return;
    }

    // بناء كائن المقال
    const title = (result.title && result.title.trim()) || topic;
    const content = (result.content && result.content.trim()) || "لم يتم إرجاع محتوى.";
    const tags = Array.isArray(result.tags) ? result.tags : [];
    const slug = slugify(title + "-" + Date.now());

    const item = { id: Date.now(), lang, title, slug, content, tags, created_at: new Date().toISOString() };
    const list = JSON.parse(localStorage.getItem("sb_articles") || "[]");
    list.unshift(item);
    saveArticles(list);

    status.textContent = "✅ تم إنشاء المقال وحفظه محليًا.";
    document.getElementById("topic").value = "";
  }catch(e){
    status.textContent = "⚠️ خطأ في التوليد: " + e.message;
  }
}

function renderArticles(){
  const wrap = document.getElementById("articles");
  if(!wrap) return;
  const q = (document.getElementById("search")?.value || "").toLowerCase();
  const fLang = document.getElementById("filterLang")?.value || "";
  let arr = window.__ARTS || [];
  if(fLang) arr = arr.filter(a=>a.lang===fLang);
  if(q) arr = arr.filter(a=> (a.title || "").toLowerCase().includes(q));

  if(arr.length === 0){
    wrap.innerHTML = `<p>لا توجد مقالات بعد.</p>`;
    return;
  }

  wrap.innerHTML = arr.map(a => `
    <div class="article-card">
      <h3>${escapeHTML(a.title)}</h3>
      <div class="meta">اللغة: ${a.lang.toUpperCase()} • ${formatDate(a.created_at)}</div>
      <div class="tags">${(a.tags||[]).map(t=>`#${escapeHTML(t)}`).join(' ')}</div>
      <div class="actions">
        <button onclick="openArticle('${a.slug}')">عرض</button>
        <button onclick="downloadHTML('${a.slug}')">تحميل HTML</button>
        <button onclick="deleteArticle('${a.slug}')">حذف</button>
      </div>
    </div>
  `).join('');
}

// عرض مقال داخل نافذة منبثقة
function openArticle(slug){
  const a = (window.__ARTS||[]).find(x=>x.slug===slug);
  if(!a) return;
  ensureModal();
  const box = document.querySelector('.modal .box');
  box.innerHTML = `
    <button class="close" onclick="closeModal()">إغلاق</button>
    <h2>${escapeHTML(a.title)}</h2>
    <div class="meta">اللغة: ${a.lang.toUpperCase()} • ${formatDate(a.created_at)}</div>
    <article style="white-space:pre-wrap;line-height:1.8;margin-top:12px;">
      ${escapeHTML(a.content)}
    </article>
  `;
  document.querySelector('.modal').style.display = 'flex';
}

function ensureModal(){
  if(document.querySelector('.modal')) return;
  const m = document.createElement('div');
  m.className = 'modal';
  m.innerHTML = `<div class="box"></div>`;
  document.body.appendChild(m);
  m.addEventListener('click', e => { if(e.target===m) closeModal(); });
}

function closeModal(){ document.querySelector('.modal').style.display = 'none'; }

function deleteArticle(slug){
  if(!confirm('هل أنت متأكد من حذف المقال؟')) return;
  let arr = window.__ARTS||[];
  arr = arr.filter(a=>a.slug!==slug);
  saveArticles(arr);
}

function downloadHTML(slug){
  const a = (window.__ARTS||[]).find(x=>x.slug===slug);
  if(!a) return;
  const html = `
<!DOCTYPE html>
<html lang="${a.lang}">
<head>
<meta charset="utf-8">
<title>${escapeHTML(a.title)}</title>
<meta name="description" content="${escapeHTML(a.title)}">
</head>
<body>
<article>
<h1>${escapeHTML(a.title)}</h1>
<small>${formatDate(a.created_at)}</small>
<pre style="white-space:pre-wrap;line-height:1.8;">${escapeHTML(a.content)}</pre>
</article>
</body></html>`;
  const blob = new Blob([html], {type:'text/html'});
  const url = URL.createObjectURL(blob);
  const aTag = document.createElement('a');
  aTag.href = url;
  aTag.download = `${a.slug}.html`;
  document.body.appendChild(aTag);
  aTag.click();
  aTag.remove();
  URL.revokeObjectURL(url);
}

// محاكاة توليد مقالة بدون خادم (لحين ربط باك-إند)
function mockArticle(topic, lang){
  const intro = {
    ar: `مقالة SEO عن: ${topic}\n\nمقدمة:\nفي هذه المقالة سنحلل ${topic} ونستعرض الاتجاهات والأفكار العملية.`,
    en: `SEO article about: ${topic}\n\nIntro:\nIn this article we analyze ${topic} and provide practical insights.`,
    hi: `SEO लेख: ${topic}\n\nपरिचय:\nइस लेख में हम ${topic} का विश्लेषण करेंगे और व्यावहारिक सुझाव देंगे।`,
    ja: `SEO記事: ${topic}\n\n導入:\n本記事では${topic}を分析し、実用的な示唆を提供します。`
  }[lang] || `SEO article about: ${topic}`;

  const body = `
العناوين:
1) نظرة عامة
2) المؤشرات المهمة
3) التوقعات قصيرة المدى
4) نصائح عملية

المحتوى:
- فقرة 1: سياق عام للسوق وتأثير الأخبار.
- فقرة 2: دعم ومقاومة، وزخم السيولة.
- فقرة 3: سيناريوهات محتملة وكيفية إدارة المخاطر.
- خاتمة: خطوات عملية بسيطة للمبتدئ والمتوسط.`;

  const content = (lang==='ar') ? `${intro}\n\n${body}` : `${intro}\n\n(Body sections in target language…)`;
  const tags = ["crypto","ai","trading","bitcoin","analysis"];
  return { title: topic, content, tags };
}

// أدوات مساعدة
function escapeHTML(s){ return (s||"").replace(/[&<>"']/g, m=>({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;" }[m])); }
function formatDate(iso){ try{ return new Date(iso).toLocaleString('ar'); }catch(_){ return iso; } }
