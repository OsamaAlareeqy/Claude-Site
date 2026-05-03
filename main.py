from fastapi import FastAPI
from duckduckgo_search import DDGS

app = FastAPI()

@app.get("/ask")
def ask_claude(question: str):
    # المحاولة الأولى: مباشرة من جهازك (بدون بروكسي)
    try:
        with DDGS() as ddgs:
            response = ddgs.chat(question, model='claude-3-haiku')
            return {"answer": response, "method": "direct"}
    except Exception as e:
        # إذا فشل بسبب الحظر، يعطيك رسالة واضحة بدل الخطأ المبهم
        return {
            "answer": "جهازك لا يزال محظوراً مؤقتاً من محرك البحث.",
            "technical_error": str(e),
            "solution": "ارفع الكود على Render الآن لأن السيرفر هناك سيعطيك IP جديداً كلياً."
        }