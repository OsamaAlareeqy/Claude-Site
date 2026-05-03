from fastapi import FastAPI
from duckduckgo_search import DDGS
import time
import random

app = FastAPI()

# قائمة متصفحات وهمية لتبدو كأنك إنسان مختلف في كل مرة
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

@app.get("/ask")
def ask_claude(question: str):
    # إضافة تأخير عشوائي بسيط لكسر نظام الحماية (بين 1 لـ 3 ثواني)
    time.sleep(random.uniform(1, 3))
    
    # اختيار بصمة متصفح عشوائية
    random_ua = random.choice(USER_AGENTS)
    
    try:
        # نستخدم الكود المباشر الذي نجح معك في الصورة image_6b959c.png
        with DDGS() as ddgs:
            # نحدد الموديل بشكل صريح
            response = ddgs.chat(question, model='claude-3-haiku')
            if response:
                return {"answer": response}
            else:
                raise Exception("Empty response")
                
    except Exception:
        # إذا فشل، نحاول مرة أخيرة باستخدام البحث النصي كخطة بديلة
        try:
            with DDGS() as ddgs:
                results = ddgs.text(question, max_results=1)
                return {"answer": results[0]['body'] if results else "المحرك مشغول، حاول بعد ثوانٍ"}
        except:
            return {"answer": "يرجى الانتظار 10 ثواني وعمل Refresh مرة واحدة فقط"}