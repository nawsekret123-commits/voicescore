from flask import Flask, request, redirect, url_for, render_template_string
from datetime import datetime
import requests
import re

app = Flask(__name__)

# =========================
# НАСТРОЙКИ
# =========================
TELEGRAM_TOKEN = "8799281877:AAHuImnbo4676epEZKKmRuMRR5skmR-0F2g"
TELEGRAM_CHAT_ID = "622522768"

TELEGRAM_LINK = "https://t.me/Mussayev_Yermurat"
WHATSAPP_LINK = "https://wa.me/77001199771"

SITE_TITLE = "VoiceScore"
SITE_SUBTITLE = "AI аналитика звонков"


# =========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================
def clean_text(value, max_len=1000):
    if value is None:
        return ""
    value = str(value).strip()
    return value[:max_len]


def normalize_phone(phone):
    digits = re.sub(r"\D", "", phone or "")

    if digits.startswith("8") and len(digits) == 11:
        digits = "7" + digits[1:]

    if digits.startswith("7") and len(digits) == 11:
        return "+" + digits

    if phone.strip().startswith("+") and len(digits) >= 10:
        return "+" + digits

    return phone.strip()


def is_valid_phone(phone):
    digits = re.sub(r"\D", "", phone or "")
    return len(digits) >= 10


def send_telegram(name, phone, service, comment):
    text = (
        f"Новая заявка с сайта {SITE_TITLE}\n\n"
        f"Имя: {name}\n"
        f"Телефон: {phone}\n"
        f"Услуга: {service}\n"
        f"Комментарий: {comment if comment else '-'}\n"
        f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text
            },
            timeout=15
        )

        if response.status_code != 200:
            print("TELEGRAM HTTP ERROR:", response.text)
            return False

        data = response.json()
        if not data.get("ok"):
            print("TELEGRAM API ERROR:", data)
            return False

        return True

    except Exception as e:
        print("TELEGRAM EXCEPTION:", e)
        return False


# =========================
# HTML
# =========================
HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>VoiceScore — AI аналитика звонков</title>

<style>
* { box-sizing: border-box; scroll-behavior: smooth; }

body {
    margin:0;
    font-family: 'Inter', Arial;
    color:white;
    background:
        radial-gradient(circle at 20% 20%, rgba(0,255,255,0.15), transparent 40%),
        radial-gradient(circle at 80% 80%, rgba(0,120,255,0.15), transparent 40%),
        #05070d;
}

/* NAV */
.navbar {
    position:sticky;
    top:0;
    backdrop-filter: blur(12px);
    background: rgba(0,0,0,0.6);
    padding:18px 40px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.logo { font-size:26px; font-weight:800; }
.logo span { color:#00f0ff; }

/* HERO */
.hero {
    position:relative;
    padding:80px 40px;
}

.hero::before {
    content:"";
    position:absolute;
    width:600px;
    height:600px;
    background: radial-gradient(circle, rgba(0,255,255,0.25), transparent);
    filter: blur(120px);
    top:-200px;
    left:-200px;
}

.hero::after {
    content:"";
    position:absolute;
    width:600px;
    height:600px;
    background: radial-gradient(circle, rgba(0,120,255,0.25), transparent);
    filter: blur(120px);
    bottom:-200px;
    right:-200px;
}

.hero-content {
    position:relative;
    z-index:1;
    max-width:1200px;
    margin:auto;
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:40px;
}

/* TEXT */
h1 {
    font-size:64px;
    margin:0 0 20px;
}

.gradient {
    background: linear-gradient(90deg,#00f0ff,#00aaff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* BUTTONS */
.btn {
    padding:14px 28px;
    border-radius:14px;
    font-weight:700;
    cursor:pointer;
}

.btn-primary {
    background: linear-gradient(135deg,#00f0ff,#00aaff);
    color:#001;
    box-shadow:0 0 30px rgba(0,255,255,0.5);
    transition:0.3s;
}

.btn-primary:hover {
    transform: translateY(-3px) scale(1.03);
}

/* DASHBOARD */
.dashboard {
    background: rgba(255,255,255,0.05);
    border-radius:24px;
    padding:20px;
    backdrop-filter: blur(10px);
    border:1px solid rgba(255,255,255,0.1);
}

.metric {
    margin-bottom:12px;
}

/* CARDS */
.cards {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:20px;
    padding:60px 40px;
}

.card {
    padding:20px;
    border-radius:20px;
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
    transition:0.3s;
    position:relative;
    overflow:hidden;
}

.card::before {
    content:"";
    position:absolute;
    width:200%;
    height:200%;
    background: radial-gradient(circle, rgba(0,255,255,0.2), transparent);
    top:-50%;
    left:-50%;
    opacity:0;
    transition:0.4s;
}

.card:hover::before { opacity:1; }
.card:hover { transform: translateY(-6px); }

/* ANIMATION */
.fade {
    opacity:0;
    transform:translateY(30px);
    transition:0.6s;
}

.fade.show {
    opacity:1;
    transform:translateY(0);
}

</style>
</head>

<body>

<div class="navbar">
    <div class="logo"><span>Voice</span>Score</div>
    <a href="#contact" class="btn btn-primary">Заявка</a>
</div>

<section class="hero">
    <div class="hero-content">
        <div>
            <h1 class="gradient">VoiceScore</h1>
            <p>AI анализ 100% звонков. Контроль, оценка и рост команды без ручной прослушки.</p>
            <br>
            <a href="#contact" class="btn btn-primary">Получить демо</a>
        </div>

        <div class="dashboard">
            <div class="metric">Проверено: <b>12 480</b></div>
            <div class="metric">Средняя оценка: <b>86%</b></div>
            <div class="metric">Ошибки: <b>143</b></div>
        </div>
    </div>
</section>

<section class="cards">
    <div class="card fade"><h3>100% анализ</h3><p>Проверяется каждый звонок</p></div>
    <div class="card fade"><h3>Оценка</h3><p>Автоматический скоринг</p></div>
    <div class="card fade"><h3>Ошибки</h3><p>Выявление нарушений</p></div>
    <div class="card fade"><h3>Отчеты</h3><p>Аналитика для руководителя</p></div>
</section>

<script>
const els = document.querySelectorAll('.fade');

window.addEventListener('scroll', () => {
    els.forEach(el => {
        if(el.getBoundingClientRect().top < window.innerHeight - 100){
            el.classList.add('show');
        }
    });
});
</script>

</body>
</html>
"""


# =========================
# ROUTE
# =========================
@app.route("/", methods=["GET", "POST"])
def home():
    success = request.args.get("success", "")
    error = request.args.get("error", "")

    message = ""

    if success == "1":
        message = """
        <div class="alert success">
            Заявка отправлена. Мы свяжемся с вами.
        </div>
        """

    elif error == "empty":
        message = """
        <div class="alert error">
            Заполните имя, телефон и выберите услугу.
        </div>
        """

    elif error == "phone":
        message = """
        <div class="alert error">
            Укажите корректный номер телефона.
        </div>
        """

    elif error == "spam":
        message = """
        <div class="alert error">
            Заявка отклонена.
        </div>
        """

    elif error == "telegram":
        message = """
        <div class="alert error">
            Не удалось отправить заявку. Проверьте token, chat id или доступ к Telegram API.
        </div>
        """

    if request.method == "POST":
        name = clean_text(request.form.get("name", ""), 100)
        phone = normalize_phone(clean_text(request.form.get("phone", ""), 50))
        service = clean_text(request.form.get("service", ""), 120)
        comment = clean_text(request.form.get("comment", ""), 1000)
        website = clean_text(request.form.get("website", ""), 200)

        if website:
            return redirect(url_for("home", error="spam"))

        if not (name and phone and service):
            return redirect(url_for("home", error="empty"))

        if not is_valid_phone(phone):
            return redirect(url_for("home", error="phone"))

        ok = send_telegram(name, phone, service, comment)
        if not ok:
            return redirect(url_for("home", error="telegram"))

        return redirect(url_for("home", success="1"))

    return render_template_string(
        HTML,
        message=message,
        site_title=SITE_TITLE,
        site_subtitle=SITE_SUBTITLE,
        telegram_link=TELEGRAM_LINK,
        whatsapp_link=WHATSAPP_LINK,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
