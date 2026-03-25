from flask import Flask, request, redirect, url_for, render_template_string
from datetime import datetime
import requests
import os
import html
import re

app = Flask(__name__)

# =========================
# НАСТРОЙКИ
# =========================
# Лучше потом вынести в Environment Variables на Render.
# Но пока можно оставить тут, чтобы все работало одним файлом.

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8799281877:AAE-9WAtLb5zrifnNLebL9Xiw6j1bn5RVeI")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "622522768")

# Ссылки на контакты
TELEGRAM_LINK = os.getenv("TELEGRAM_LINK", "https://t.me/Takhir_Zhanatovich")
WHATSAPP_LINK = os.getenv("WHATSAPP_LINK", "https://wa.me/77078340913")

SITE_TITLE = "VoiceScore"
SITE_SUBTITLE = "AI аналитика звонков"

# =========================
# ЛОГИКА
# =========================

def clean_text(value: str, max_len: int = 1000) -> str:
    value = (value or "").strip()
    value = value[:max_len]
    return value


def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    if digits.startswith("8") and len(digits) == 11:
        digits = "7" + digits[1:]
    if digits.startswith("7") and len(digits) == 11:
        return "+" + digits
    if phone.strip().startswith("+") and len(digits) >= 10:
        return "+" + digits
    return phone.strip()


def is_valid_phone(phone: str) -> bool:
    digits = re.sub(r"\D", "", phone or "")
    return len(digits) >= 10


def send_telegram(name: str, phone: str, service: str, comment: str) -> tuple[bool, str]:
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "8799281877:AAE-9WAtLb5zrifnNLebL9Xiw6j1bn5RVeI":
        return False, "Не задан TELEGRAM_TOKEN"

    if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "622522768":
        return False, "Не задан TELEGRAM_CHAT_ID"

    safe_name = html.escape(name)
    safe_phone = html.escape(phone)
    safe_service = html.escape(service)
    safe_comment = html.escape(comment) if comment else "-"

    text = (
        f"<b>Новая заявка с сайта {SITE_TITLE}</b>\n\n"
        f"<b>Имя:</b> {safe_name}\n"
        f"<b>Телефон:</b> {safe_phone}\n"
        f"<b>Услуга:</b> {safe_service}\n"
        f"<b>Комментарий:</b> {safe_comment}\n"
        f"<b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "HTML"
            },
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("ok"):
            return False, f"Telegram API вернул ok=false: {data}"

        return True, "ok"

    except Exception as e:
        return False, str(e)


HTML = r"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ site_title }} — AI аналитика звонков</title>
    <meta name="description" content="VoiceScore — AI-платформа для анализа 100% звонков, контроля качества, оценки сотрудников и управленческой отчетности.">

    <style>
        * {
            box-sizing: border-box;
            scroll-behavior: smooth;
        }

        :root {
            --bg-1: #031127;
            --bg-2: #071a36;
            --card: rgba(255,255,255,0.05);
            --card-2: rgba(255,255,255,0.07);
            --line: rgba(255,255,255,0.10);
            --text: #ffffff;
            --muted: #b8c7dc;
            --accent: #5eead4;
            --accent-2: #2dd4bf;
            --danger: #ef4444;
            --success: #22c55e;
            --shadow: 0 20px 60px rgba(0,0,0,0.35);
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at 15% 15%, rgba(45,212,191,0.12), transparent 24%),
                radial-gradient(circle at 85% 10%, rgba(94,234,212,0.10), transparent 22%),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
            overflow-x: hidden;
        }

        a {
            text-decoration: none;
            color: inherit;
        }

        .container {
            width: 100%;
            max-width: 1180px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .navbar {
            position: sticky;
            top: 0;
            z-index: 50;
            background: rgba(3, 17, 39, 0.82);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }

        .nav-inner {
            min-height: 76px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        .logo {
            font-size: 30px;
            font-weight: 800;
            letter-spacing: -0.04em;
        }

        .logo span {
            color: var(--accent);
        }

        .nav-links {
            display: flex;
            gap: 18px;
            align-items: center;
            flex-wrap: wrap;
        }

        .nav-links a {
            color: var(--muted);
            font-size: 15px;
        }

        .nav-links a:hover {
            color: #fff;
        }

        .btn {
            display: inline-flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            padding: 14px 22px;
            border-radius: 16px;
            font-weight: 700;
            border: 1px solid transparent;
            transition: 0.2s ease;
            cursor: pointer;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn-primary {
            background: linear-gradient(135deg, #5eead4 0%, #2dd4bf 100%);
            color: #042f2e;
            box-shadow: 0 10px 30px rgba(45,212,191,0.20);
        }

        .btn-secondary {
            background: rgba(255,255,255,0.05);
            border-color: rgba(255,255,255,0.10);
            color: #fff;
        }

        .hero {
            padding: 56px 0 30px;
        }

        .hero-box {
            border-radius: 30px;
            padding: 50px;
            background: linear-gradient(135deg, rgba(7,12,24,0.96), rgba(14,24,45,0.92));
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: var(--shadow);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.08fr 0.92fr;
            gap: 28px;
            align-items: center;
        }

        .badge {
            display: inline-block;
            padding: 10px 14px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.10);
            font-size: 13px;
            color: #dcfdf8;
            margin-bottom: 18px;
        }

        h1 {
            margin: 0 0 18px;
            font-size: 58px;
            line-height: 0.98;
            letter-spacing: -0.05em;
        }

        .hero p {
            color: var(--muted);
            line-height: 1.7;
            font-size: 17px;
            margin: 0 0 24px;
            max-width: 700px;
        }

        .hero-actions {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }

        .hero-points {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }

        .mini-pill {
            padding: 12px 14px;
            border-radius: 14px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            color: #e2e8f0;
            font-size: 14px;
        }

        .dashboard {
            border-radius: 26px;
            padding: 22px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
        }

        .dashboard-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 18px;
        }

        .dashboard-title {
            font-size: 20px;
            font-weight: 800;
        }

        .dashboard-badge {
            font-size: 12px;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            color: #dcfdf8;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }

        .metric {
            padding: 14px;
            border-radius: 18px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
        }

        .metric-label {
            color: #94a3b8;
            font-size: 12px;
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 24px;
            font-weight: 800;
        }

        .bars {
            display: grid;
            gap: 10px;
        }

        .bar-row {
            display: grid;
            grid-template-columns: 130px 1fr 44px;
            gap: 10px;
            align-items: center;
        }

        .bar-label {
            color: var(--muted);
            font-size: 13px;
        }

        .bar-track {
            height: 8px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.05);
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #14b8a6, #5eead4, #99f6e4);
        }

        .bar-value {
            color: var(--accent);
            font-weight: 700;
            font-size: 13px;
            text-align: right;
        }

        .section {
            padding: 36px 0;
        }

        .section-title {
            text-align: center;
            margin-bottom: 20px;
        }

        .section-title h2 {
            margin: 0 0 10px;
            font-size: 40px;
            letter-spacing: -0.04em;
        }

        .section-title p {
            margin: 0 auto;
            max-width: 820px;
            color: var(--muted);
            line-height: 1.7;
        }

        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .grid-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }

        .card {
            border-radius: 24px;
            padding: 24px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: var(--shadow);
        }

        .card h3 {
            margin: 0 0 12px;
            font-size: 22px;
        }

        .card p {
            margin: 0;
            color: var(--muted);
            line-height: 1.75;
        }

        .demo-list {
            list-style: none;
            padding: 0;
            margin: 14px 0 0;
        }

        .demo-list li {
            position: relative;
            padding-left: 18px;
            margin-bottom: 10px;
            color: var(--muted);
            line-height: 1.7;
        }

        .demo-list li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: var(--accent);
        }

        .form-wrap {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 22px;
            align-items: stretch;
        }

        .form-box {
            border-radius: 26px;
            padding: 28px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: var(--shadow);
        }

        .form-box h3 {
            margin: 0 0 14px;
            font-size: 28px;
        }

        .form-box p {
            margin: 0 0 22px;
            color: var(--muted);
            line-height: 1.7;
        }

        .field {
            margin-bottom: 14px;
        }

        .field input,
        .field select,
        .field textarea {
            width: 100%;
            padding: 15px 16px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.10);
            background: rgba(255,255,255,0.05);
            color: #fff;
            outline: none;
            font-size: 15px;
        }

        .field textarea {
            min-height: 120px;
            resize: vertical;
        }

        .field input::placeholder,
        .field textarea::placeholder {
            color: #94a3b8;
        }

        .field select option {
            color: #000;
        }

        .helper {
            color: #93c5fd;
            font-size: 13px;
            margin-top: 8px;
        }

        .contacts-list {
            display: grid;
            gap: 14px;
            margin-top: 20px;
        }

        .contact-item {
            display: flex;
            gap: 14px;
            align-items: center;
            padding: 16px;
            border-radius: 16px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
        }

        .contact-icon {
            width: 46px;
            height: 46px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            flex: 0 0 46px;
        }

        .contact-text strong {
            display: block;
            margin-bottom: 4px;
        }

        .contact-text span {
            color: var(--muted);
            font-size: 14px;
        }

        .alert {
            padding: 16px 18px;
            border-radius: 16px;
            margin-bottom: 18px;
            font-weight: 700;
        }

        .alert.success {
            background: rgba(34,197,94,0.12);
            border: 1px solid rgba(34,197,94,0.25);
            color: #bbf7d0;
        }

        .alert.error {
            background: rgba(239,68,68,0.12);
            border: 1px solid rgba(239,68,68,0.25);
            color: #fecaca;
        }

        .footer {
            padding: 30px 0 40px;
            color: var(--muted);
            text-align: center;
        }

        .floating-socials {
            position: fixed;
            right: 18px;
            bottom: 18px;
            z-index: 100;
            display: grid;
            gap: 12px;
        }

        .social-btn {
            width: 58px;
            height: 58px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(7, 18, 39, 0.92);
            border: 1px solid rgba(255,255,255,0.10);
            box-shadow: 0 10px 30px rgba(0,0,0,0.28);
            transition: 0.2s ease;
        }

        .social-btn:hover {
            transform: translateY(-3px);
        }

        .hidden-trap {
            position: absolute !important;
            left: -9999px !important;
            width: 1px !important;
            height: 1px !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        @media (max-width: 980px) {
            .hero-grid,
            .form-wrap,
            .grid-3,
            .grid-4 {
                grid-template-columns: 1fr;
            }

            .metric-grid {
                grid-template-columns: 1fr;
            }

            .hero-points {
                grid-template-columns: 1fr;
            }

            .hero-box {
                padding: 28px 22px;
            }

            h1 {
                font-size: 40px;
            }

            .section-title h2 {
                font-size: 32px;
            }

            .bar-row {
                grid-template-columns: 110px 1fr 44px;
            }
        }

        @media (max-width: 600px) {
            .nav-inner {
                padding: 12px 0;
            }

            .logo {
                font-size: 24px;
            }

            .nav-links {
                display: none;
            }

            h1 {
                font-size: 34px;
            }

            .hero p {
                font-size: 15px;
            }

            .floating-socials {
                right: 12px;
                bottom: 12px;
            }

            .social-btn {
                width: 54px;
                height: 54px;
            }
        }
    </style>
</head>
<body>

    <div class="navbar">
        <div class="container nav-inner">
            <div class="logo"><span>Voice</span>Score</div>
            <div class="nav-links">
                <a href="#features">Возможности</a>
                <a href="#benefits">Преимущества</a>
                <a href="#demo">Что показывает</a>
                <a href="#contact">Оставить заявку</a>
            </div>
            <a href="#contact" class="btn btn-primary">Оставить заявку</a>
        </div>
    </div>

    <section class="hero">
        <div class="container">
            <div class="hero-box">
                <div class="hero-grid">
                    <div>
                        <div class="badge">AI-контроль качества звонков</div>
                        <h1>{{ site_title }}</h1>
                        <p>
                            {{ site_subtitle }} для отделов продаж, взыскания и контакт-центров.
                            Система анализирует 100% разговоров, оценивает сотрудников,
                            показывает нарушения скрипта и формирует понятную отчетность для руководителя.
                        </p>

                        <div class="hero-actions">
                            <a href="#contact" class="btn btn-primary">Получить демо</a>
                            <a href="#features" class="btn btn-secondary">Посмотреть возможности</a>
                        </div>

                        <div class="hero-points">
                            <div class="mini-pill">Анализ 100% звонков</div>
                            <div class="mini-pill">Оценка по сотрудникам и отделам</div>
                            <div class="mini-pill">Контроль скриптов и ошибок</div>
                            <div class="mini-pill">Ежедневные отчеты для руководителя</div>
                        </div>
                    </div>

                    <div class="dashboard">
                        <div class="dashboard-top">
                            <div class="dashboard-title">AI Dashboard</div>
                            <div class="dashboard-badge">Live analytics</div>
                        </div>

                        <div class="metric-grid">
                            <div class="metric">
                                <div class="metric-label">Проверено звонков</div>
                                <div class="metric-value">12 480</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Средняя оценка</div>
                                <div class="metric-value">86%</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Нарушения</div>
                                <div class="metric-value">143</div>
                            </div>
                        </div>

                        <div class="bars">
                            <div class="bar-row">
                                <div class="bar-label">Скрипт</div>
                                <div class="bar-track"><div class="bar-fill" style="width: 91%;"></div></div>
                                <div class="bar-value">91%</div>
                            </div>
                            <div class="bar-row">
                                <div class="bar-label">Вежливость</div>
                                <div class="bar-track"><div class="bar-fill" style="width: 88%;"></div></div>
                                <div class="bar-value">88%</div>
                            </div>
                            <div class="bar-row">
                                <div class="bar-label">Дожим</div>
                                <div class="bar-track"><div class="bar-fill" style="width: 79%;"></div></div>
                                <div class="bar-value">79%</div>
                            </div>
                            <div class="bar-row">
                                <div class="bar-label">Ошибки</div>
                                <div class="bar-track"><div class="bar-fill" style="width: 32%;"></div></div>
                                <div class="bar-value">32%</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="features" class="section">
        <div class="container">
            <div class="section-title">
                <h2>Что умеет система</h2>
                <p>
                    Платформа помогает руководителю видеть реальную картину по отделу,
                    находить слабые места и быстро влиять на качество общения с клиентами.
                </p>
            </div>

            <div class="grid-4">
                <div class="card">
                    <h3>Анализ 100% звонков</h3>
                    <p>Проверяется не выборка, а весь поток разговоров. Можно задать фильтр, например от 1 минуты.</p>
                </div>
                <div class="card">
                    <h3>Оценка каждого диалога</h3>
                    <p>Каждый звонок получает балл по заданным критериям и правилам вашей компании.</p>
                </div>
                <div class="card">
                    <h3>Выявление нарушений</h3>
                    <p>Система показывает грубость, ошибки, отклонения от скрипта и спорные диалоги.</p>
                </div>
                <div class="card">
                    <h3>Отчеты для руководителя</h3>
                    <p>Ежедневная и периодическая аналитика по сотрудникам, группам и отделам.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="benefits" class="section">
        <div class="container">
            <div class="section-title">
                <h2>Зачем это бизнесу</h2>
                <p>
                    Меньше ручного прослушивания, быстрее контроль качества,
                    понятная оценка операторов и прозрачная аналитика для управленческих решений.
                </p>
            </div>

            <div class="grid-3">
                <div class="card">
                    <h3>Экономия времени</h3>
                    <p>Руководителям и ОКК не нужно вручную прослушивать огромный объем звонков.</p>
                </div>
                <div class="card">
                    <h3>Объективная оценка</h3>
                    <p>Единые правила оценки для всех сотрудников без человеческого фактора и выборочности.</p>
                </div>
                <div class="card">
                    <h3>Рост качества команды</h3>
                    <p>Быстро видно, кто проседает, где сотрудники теряют клиента и какие скрипты работают лучше.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="demo" class="section">
        <div class="container">
            <div class="section-title">
                <h2>Что видно в отчетах</h2>
                <p>
                    Система показывает не просто цифры, а конкретные точки роста:
                    качество диалога, ошибки, динамику по месяцам и результат по каждому сотруднику.
                </p>
            </div>

            <div class="grid-3">
                <div class="card">
                    <h3>По каждому сотруднику</h3>
                    <ul class="demo-list">
                        <li>Средний балл</li>
                        <li>Количество проверенных звонков</li>
                        <li>Главные ошибки</li>
                        <li>Динамика по периодам</li>
                    </ul>
                </div>

                <div class="card">
                    <h3>По отделу</h3>
                    <ul class="demo-list">
                        <li>Общий средний результат</li>
                        <li>Сравнение между группами</li>
                        <li>Сильные и слабые стороны команды</li>
                        <li>Процент выполнения скрипта</li>
                    </ul>
                </div>

                <div class="card">
                    <h3>По каждому звонку</h3>
                    <ul class="demo-list">
                        <li>Краткое резюме разговора</li>
                        <li>Оценка и комментарий</li>
                        <li>Фиксация нарушений</li>
                        <li>Причина плохого результата</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="section">
        <div class="container">
            <div class="form-wrap">
                <div class="form-box">
                    <h3>Оставить заявку</h3>
                    <p>
                        Заполните форму. Заявка сразу уйдет в Telegram.
                        Мы свяжемся с вами и покажем, как это можно внедрить под ваш процесс.
                    </p>

                    {{ message|safe }}

                    <form method="POST" action="/">
                        <input type="text" name="website" class="hidden-trap" autocomplete="off">

                        <div class="field">
                            <input type="text" name="name" placeholder="Ваше имя" required maxlength="100">
                        </div>

                        <div class="field">
                            <input type="text" name="phone" id="phone" placeholder="+7 (___) ___-__-__" required maxlength="25">
                            <div class="helper">Можно ввести номер в любом формате</div>
                        </div>

                        <div class="field">
                            <select name="service" required>
                                <option value="">Выберите услугу</option>
                                <option value="AI контроль качества звонков">AI контроль качества звонков</option>
                                <option value="Аналитика сотрудников">Аналитика сотрудников</option>
                                <option value="Отчеты для руководителя">Отчеты для руководителя</option>
                                <option value="Демо системы">Демо системы</option>
                            </select>
                        </div>

                        <div class="field">
                            <textarea name="comment" placeholder="Комментарий"></textarea>
                        </div>

                        <button type="submit" class="btn btn-primary" style="width:100%;">Отправить заявку</button>
                    </form>
                </div>

                <div class="form-box">
                    <h3>Контакты</h3>
                    <p>
                        Можно сразу написать нам напрямую.
                        Кнопки ниже открывают Telegram и WhatsApp.
                    </p>

                    <div class="contacts-list">
                        <a class="contact-item" href="{{ telegram_link }}" target="_blank" rel="noopener noreferrer">
                            <div class="contact-icon">
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                                    <path d="M21 4L3.9 10.6C2.7 11.1 2.7 11.8 3.7 12.1L8.1 13.5L18.3 7.1C18.8 6.8 19.3 7 18.9 7.4L10.6 14.9V19.1C10.6 19.7 10.9 20 11.4 20C11.8 20 12 19.8 12.2 19.5L14.3 16.9L18.7 20.2C19.5 20.6 20.1 20.4 20.3 19.5L23.2 5.7C23.5 4.6 22.8 4.1 21.9 4.5L21 4Z" fill="#5EEAD4"/>
                                </svg>
                            </div>
                            <div class="contact-text">
                                <strong>Telegram</strong>
                                <span>Написать в Telegram</span>
                            </div>
                        </a>

                        <a class="contact-item" href="{{ whatsapp_link }}" target="_blank" rel="noopener noreferrer">
                            <div class="contact-icon">
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                                    <path d="M20.5 3.5C18.3 1.3 15.4 0 12.2 0C5.6 0 0.3 5.3 0.3 11.9C0.3 14 0.8 16 1.9 17.8L0 24L6.4 22.1C8.1 23 10.1 23.5 12.1 23.5H12.2C18.8 23.5 24.1 18.2 24.1 11.6C24.1 8.4 22.8 5.7 20.5 3.5ZM12.2 21.5H12.1C10.3 21.5 8.6 21 7.1 20.1L6.7 19.9L3 21L4.1 17.4L3.9 17C2.9 15.4 2.4 13.7 2.4 11.9C2.4 6.5 6.8 2.1 12.2 2.1C14.8 2.1 17.2 3.1 19 4.9C20.8 6.7 21.9 9.1 21.8 11.7C21.8 17.1 17.5 21.5 12.2 21.5ZM17.5 14.2C17.2 14.1 15.8 13.4 15.5 13.3C15.2 13.2 15 13.1 14.8 13.4C14.6 13.7 14.1 14.3 13.9 14.5C13.7 14.7 13.5 14.8 13.2 14.6C11.4 13.7 10.2 12.9 9 10.8C8.7 10.3 9.3 10.4 9.8 9.3C9.9 9.1 9.9 8.9 9.8 8.7C9.7 8.5 9.1 7.1 8.8 6.4C8.5 5.7 8.2 5.8 7.9 5.8C7.7 5.8 7.5 5.8 7.2 5.8C7 5.8 6.6 5.9 6.3 6.2C6 6.5 5.2 7.2 5.2 8.7C5.2 10.2 6.3 11.7 6.4 11.9C6.6 12.1 8.6 15.2 11.6 16.5C13.5 17.3 14.2 17.4 15.2 17.3C15.8 17.2 17.1 16.6 17.4 15.8C17.7 15 17.7 14.4 17.5 14.2Z" fill="#5EEAD4"/>
                                </svg>
                            </div>
                            <div class="contact-text">
                                <strong>WhatsApp</strong>
                                <span>Написать в WhatsApp</span>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <div class="footer">
        <div class="container">
            © 2026 {{ site_title }} — AI аналитика звонков
        </div>
    </div>

    <div class="floating-socials">
        <a class="social-btn" href="{{ telegram_link }}" target="_blank" rel="noopener noreferrer" aria-label="Telegram">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M21 4L3.9 10.6C2.7 11.1 2.7 11.8 3.7 12.1L8.1 13.5L18.3 7.1C18.8 6.8 19.3 7 18.9 7.4L10.6 14.9V19.1C10.6 19.7 10.9 20 11.4 20C11.8 20 12 19.8 12.2 19.5L14.3 16.9L18.7 20.2C19.5 20.6 20.1 20.4 20.3 19.5L23.2 5.7C23.5 4.6 22.8 4.1 21.9 4.5L21 4Z" fill="#5EEAD4"/>
            </svg>
        </a>

        <a class="social-btn" href="{{ whatsapp_link }}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M20.5 3.5C18.3 1.3 15.4 0 12.2 0C5.6 0 0.3 5.3 0.3 11.9C0.3 14 0.8 16 1.9 17.8L0 24L6.4 22.1C8.1 23 10.1 23.5 12.1 23.5H12.2C18.8 23.5 24.1 18.2 24.1 11.6C24.1 8.4 22.8 5.7 20.5 3.5ZM12.2 21.5H12.1C10.3 21.5 8.6 21 7.1 20.1L6.7 19.9L3 21L4.1 17.4L3.9 17C2.9 15.4 2.4 13.7 2.4 11.9C2.4 6.5 6.8 2.1 12.2 2.1C14.8 2.1 17.2 3.1 19 4.9C20.8 6.7 21.9 9.1 21.8 11.7C21.8 17.1 17.5 21.5 12.2 21.5ZM17.5 14.2C17.2 14.1 15.8 13.4 15.5 13.3C15.2 13.2 15 13.1 14.8 13.4C14.6 13.7 14.1 14.3 13.9 14.5C13.7 14.7 13.5 14.8 13.2 14.6C11.4 13.7 10.2 12.9 9 10.8C8.7 10.3 9.3 10.4 9.8 9.3C9.9 9.1 9.9 8.9 9.8 8.7C9.7 8.5 9.1 7.1 8.8 6.4C8.5 5.7 8.2 5.8 7.9 5.8C7.7 5.8 7.5 5.8 7.2 5.8C7 5.8 6.6 5.9 6.3 6.2C6 6.5 5.2 7.2 5.2 8.7C5.2 10.2 6.3 11.7 6.4 11.9C6.6 12.1 8.6 15.2 11.6 16.5C13.5 17.3 14.2 17.4 15.2 17.3C15.8 17.2 17.1 16.6 17.4 15.8C17.7 15 17.7 14.4 17.5 14.2Z" fill="#5EEAD4"/>
            </svg>
        </a>
    </div>

    <script>
        const phoneInput = document.getElementById("phone");

        if (phoneInput) {
            phoneInput.addEventListener("input", function(e) {
                let x = e.target.value.replace(/\D/g, "");

                if (x.startsWith("8")) {
                    x = "7" + x.slice(1);
                }

                if (!x.startsWith("7") && x.length > 0) {
                    x = "7" + x;
                }

                x = x.substring(0, 11);

                let formatted = "";
                if (x.length > 0) formatted = "+7";
                if (x.length > 1) formatted += " (" + x.substring(1, 4);
                if (x.length >= 4) formatted += ") " + x.substring(4, 7);
                if (x.length >= 7) formatted += "-" + x.substring(7, 9);
                if (x.length >= 9) formatted += "-" + x.substring(9, 11);

                e.target.value = formatted;
            });
        }
    </script>

</body>
</html>
"""


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
            Не удалось отправить заявку. Проверьте Telegram token, chat id или настройки сервера.
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

        ok, info = send_telegram(name, phone, service, comment)
        if not ok:
            print("TELEGRAM ERROR:", info)
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
