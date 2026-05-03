from fastapi import FastAPI
from duckduckgo_search import DDGS
import time
import random

app = FastAPI()

@app.get("/ask")
def ask_claude(question: str):
    # إضافة "ملح" (Salt) للسؤال لكسر الكاش والحظر
    # أضفنا مسافة عشوائية في نهاية السؤال ليبدو مختلفاً برمجياً
    shuffled_question = question + (" " * random.randint(1, 5))
    
    try:
        with DDGS() as ddgs:
            # المحاولة الأولى: الحصول على رد ذكي من Claude
            response = ddgs.chat(shuffled_question, model='claude-3-haiku')
            if response and "busy" not in response.lower():
                return {"answer": response, "status": "success"}
            
            # إذا كان الرد فارغاً أو يحتوي رسالة انشغال، ننتقل للخطة ب
            raise Exception("Rate limited or empty")

    except Exception:
        # الخطة ب: البحث النصي (أكثر استقراراً ولا يتم حظره بسهولة)
        try:
            with DDGS() as ddgs:
                results = ddgs.text(shuffled_question, max_results=1)
                if results:
                    return {"answer": results[0]['body'], "status": "fallback"}
                else:
                    return {"answer": "المحرك يحتاج استراحة، جرب بعد 30 ثانية", "status": "blocked"}
        except:
            return {"answer": "حدث خطأ في الاتصال، حاول لاحقاً", "status": "error"}