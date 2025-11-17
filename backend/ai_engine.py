# =========================================================
# SmartBot AI Trader – AI Engine
# =========================================================
"""
هذا الملف مسؤول عن:
- التواصل مع OpenAI
- توليد تحليل ذكي للعملات / الأسهم / الذهب
- توليد ردود للمحادثة (chat)
"""

import os
import openai

# مهم: يجب أن تضع مفتاح OpenAI في متغير البيئة:
# OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")


def _build_prompt(user_text: str) -> str:
    """
    تجهيز الـ Prompt للذكاء الاصطناعي.
    نحاول نفهم: هل المستخدم يسأل عن عملة، سهم، ذهب… إلخ.
    """
    base = """
أنت مساعد تداول ذكي اسمه SmartBot AI Trader.
مهمّتك:
- تحليل العملات الرقمية، الذهب، وبعض الأسهم الموثوقة.
- لا تعطي وعود ربح مضمونة.
- ركّز على التحليل الفني + الأساسي بشكل مبسط.
- أجب بالعربية الفصحى المبسّطة، في نقاط قصيرة.

صيغة الإجابة المطلوبة:
1. الاتجاه العام (صاعد / هابط / متذبذب)
2. أهم مستويات الدعم والمقاومة (تقريبية)
3. المخاطر والتنبيهات
4. هل يُفضّل الانتظار أو الدخول بحذر
5. تذكير أن هذا ليس نصيحة استثمارية مضمونة

نص المستخدم:
"""
    return base + "\n" + user_text.strip()


def analyze_with_ai(user_text: str) -> str:
    """
    دالة رئيسية يستعملها app.py:
    - في /analyze لتحليل أصل معيّن
    - في /chat للرد على المستخدم
    """
    if not user_text or user_text.strip() == "":
        return "من فضلك اكتب اسم العملة أو السهم أو سؤالك بشكل أوضح."

    prompt = _build_prompt(user_text)

    try:
        # استدعاء OpenAI – نموذج نصي خفيف (غيّر الاسم حسب حسابك)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد تداول ذكي."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=350,
            temperature=0.4
        )

        answer = response["choices"][0]["message"]["content"]
        return answer.strip()

    except Exception as e:
        print("AI Error:", e)
        return "حصل خطأ أثناء الاتصال بالذكاء الاصطناعي، جرّب مرة أخرى لاحقاً."
