# =========================
# 📂 FILE: api/services/llm.py
# =========================
import os, httpx, logging
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")

SYSTEM = {
    "en": "You are a senior fintech writer. Write clear, expert SEO articles for crypto traders.",
    "ar": "أنت كاتب تمويل خبير. اكتب مقالات SEO واضحة ومفيدة لمتداولي العملات الرقمية.",
    "hi": "आप एक फिनटेक लेखक हैं। क्रिप्टो ट्रेडर्स के लिए स्पष्ट SEO लेख लिखें।",
    "ja": "あなたはフィンテック分野の専門ライターです。暗号資産トレーダー向けに明確なSEO記事を書いてください。"
}

async def ai_generate_article(topic: str, lang: str="en"):
    if not OPENAI_API_KEY:
        # حالة بدون مفتاح — نرجّع مقال تجريبي
        return (f"{topic} (demo)", f"{topic}\n\nThis is a demo article content.", ["crypto","ai","trading"])

    prompt = {
        "role": "user",
        "content": (
            f"Write an SEO-structured article about: {topic}. "
            "Use H2/H3 headings, bullet points, and a practical conclusion. 700-900 words."
        )
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM.get(lang, SYSTEM["en"])},
            prompt
        ],
        "temperature": 0.4
    }
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"].strip()

    # العنوان = أول سطر، وإن لم يوجد نولّد عنوانًا مناسبًا
    title = content.splitlines()[0].strip("# ").strip()[:120] if content else topic[:120]

    # كلمات مفتاحية سريعة
    kw_prompt = {
        "model": MODEL,
        "messages": [
            {"role":"system","content":"Return 5 SEO keywords separated by comma."},
            {"role":"user","content": f"Topic: {topic}"}
        ],
        "temperature": 0.2
    }
    try:
        r2 = await c.post("https://api.openai.com/v1/chat/completions", headers=headers, json=kw_prompt)
        r2.raise_for_status()
        tags = [t.strip() for t in r2.json()["choices"][0]["message"]["content"].split(",") if t.strip()]
    except Exception:
        tags = ["crypto","trading","ai","signals","analysis"]

    return (title, content, tags)
