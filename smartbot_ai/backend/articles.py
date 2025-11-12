from .llm import ai_chat

TEMPLATES = {
    "ar": "اكتب مقالة SEO منظمة بعناوين فرعية عن: {topic}. مقدمة قصيرة وخاتمة بنصيحة عملية.",
    "en": "Write an SEO-structured article with subheadings about: {topic}. Short intro and a practical conclusion.",
    "hi": "विषय {topic} पर SEO लेख लिखें, उपशीर्षकों सहित। छोटा परिचय और व्यावहारिक निष्कर्ष दें。",
    "ja": "テーマ「{topic}」について、見出しを備えたSEO記事を書いてください。短い導入と実践的な結論を含めてください。",
}

async def generate_article(topic: str, lang: str = "en", outline_only: bool = False):
    try:
        if outline_only:
            prompt = ("أعطني مخطط نقاط لمقال عن: " + topic) if lang == "ar" else ("Give me a bullet-point outline for: " + topic)
        else:
            prompt = TEMPLATES.get(lang, TEMPLATES["en"]).format(topic=topic)
        content = await ai_chat(prompt, lang)
        if not content:
            return {"error": "Failed to generate content", "title": topic.title(), "content": "", "tags": []}
        tags_prompt = f"اعطني 5 كلمات مفتاحية SEO عن: {topic}" if lang == "ar" else f"Give me 5 SEO keywords for: {topic}"
        tags_text = await ai_chat(tags_prompt, lang)
        tags = [t.strip() for t in tags_text.split(",") if t.strip()]
        title = content.splitlines()[0][:80] if content else topic.title()
        return {"title": title, "content": content, "tags": tags}
    except Exception as e:
        return {"error": str(e), "title": topic.title(), "content": "", "tags": []}
                                   
