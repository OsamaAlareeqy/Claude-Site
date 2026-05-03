from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from duckduckgo_search import DDGS
import requests
import random

app = FastAPI()

# دالة لجلب بروكسي لفك الحظر
def get_proxy():
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all"
        proxies = requests.get(url).text.strip().split('\r\n')
        return random.choice(proxies)
    except:
        return None

# واجهة مستخدم بسيطة في الرابط الرئيسي
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>Osama AI</title></head>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h1>Osama's AI Assistant</h1>
            <input type="text" id="quest" placeholder="Ask me anything..." style="width: 300px; padding: 10px;">
            <button onclick="ask()" style="padding: 10px;">Send</button>
            <div id="res" style="margin-top: 20px; font-weight: bold;"></div>
            <script>
                async function ask() {
                    const q = document.getElementById('quest').value;
                    const response = await fetch('/ask?question=' + q);
                    const data = await response.json();
                    document.getElementById('res').innerText = data.answer;
                }
            </script>
        </body>
    </html>
    """

@app.get("/ask")
def ask_claude(question: str):
    proxy = get_proxy()
    proxy_config = f"http://{proxy}" if proxy else None
    
    with DDGS(proxy=proxy_config) as ddgs:
        try:
            # محاولة جلب الرد من Claude
            response = ddgs.chat(question, model='claude-3-haiku')
            return {"answer": response}
        except Exception:
            try:
                # محاولة أخيرة عبر البحث النصي
                results = ddgs.text(question, max_results=1)
                return {"answer": results[0]['body'] if results else "لا يوجد نتائج حالياً"}
            except:
                return {"answer": "المحرك مشغول، يرجى المحاولة باستخدام سؤال مختلف قليلاً"}