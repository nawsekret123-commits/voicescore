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
            data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
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
    <title>{{ site_title }} — AI контроль качества звонков</title>
    <meta name="description" content="VoiceScore — AI-платформа для анализа звонков, оценки сотрудников, контроля скриптов и управленческой отчетности.">

    <style>
        * {
            box-sizing: border-box;
            scroll-behavior: smooth;
        }

        :root {
            --bg: #060914;
            --bg2: #0a1120;
            --bg3: #0c1728;
            --card: rgba(255,255,255,0.055);
            --card-strong: rgba(255,255,255,0.07);
            --line: rgba(255,255,255,0.10);
            --text: #ffffff;
            --muted: #9fb2c9;
            --muted-2: #7d8fa6;
            --accent: #62f5d4;
            --accent-2: #48b8ff;
            --accent-3: #9b8cff;
            --success: #22c55e;
            --danger: #ef4444;
            --shadow: 0 24px 70px rgba(0, 0, 0, 0.30);
            --radius-xl: 32px;
            --radius-lg: 24px;
            --radius-md: 18px;
            --container: 1240px;
        }

        html, body {
            margin: 0;
            padding: 0;
            color: var(--text);
            font-family: Inter, Arial, sans-serif;
            background:
                radial-gradient(circle at 12% 14%, rgba(98,245,212,0.05), transparent 22%),
                radial-gradient(circle at 88% 10%, rgba(72,184,255,0.05), transparent 22%),
                radial-gradient(circle at 50% 80%, rgba(155,140,255,0.04), transparent 24%),
                linear-gradient(180deg, #050913 0%, #09111d 42%, #0b1523 100%);
            overflow-x: hidden;
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(255,255,255,0.018) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.018) 1px, transparent 1px);
            background-size: 48px 48px;
            mask-image: radial-gradient(circle at center, black 26%, transparent 82%);
            pointer-events: none;
            z-index: 0;
        }

        #network-bg {
            position: fixed;
            inset: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            pointer-events: none;
            opacity: 0.28;
        }

        body::after {
            content: "";
            position: fixed;
            inset: 0;
            background:
                radial-gradient(circle at center, transparent 0%, rgba(5,9,19,0.06) 58%, rgba(5,9,19,0.28) 100%);
            pointer-events: none;
            z-index: 2;
        }

        a {
            text-decoration: none;
            color: inherit;
        }

        img {
            max-width: 100%;
            display: block;
        }

        .container {
            width: 100%;
            max-width: var(--container);
            margin: 0 auto;
            padding: 0 24px;
            position: relative;
            z-index: 5;
        }

        .parallax {
            transition: transform 0.25s linear;
            will-change: transform;
        }

        .orb {
            position: absolute;
            border-radius: 999px;
            filter: blur(100px);
            opacity: 0.28;
            pointer-events: none;
            z-index: 3;
        }

        .orb-1 {
            width: 340px;
            height: 340px;
            background: rgba(98,245,212,0.14);
            top: 60px;
            left: -100px;
        }

        .orb-2 {
            width: 300px;
            height: 300px;
            background: rgba(72,184,255,0.12);
            top: 30px;
            right: -80px;
        }

        .orb-3 {
            width: 240px;
            height: 240px;
            background: rgba(155,140,255,0.10);
            bottom: 40px;
            left: 48%;
        }

        .navbar {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(6, 10, 20, 0.60);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }

        .nav-inner {
            min-height: 76px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 28px;
            font-weight: 900;
            letter-spacing: -0.05em;
        }

        .logo-mark {
            width: 36px;
            height: 36px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(98,245,212,0.14), rgba(72,184,255,0.12));
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 10px 24px rgba(98,245,212,0.08);
        }

        .logo span {
            background: linear-gradient(90deg, var(--accent), #8ef7e3 35%, #8fd6ff 70%, #c3bcff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 22px;
            flex-wrap: wrap;
        }

        .nav-links a {
            color: var(--muted);
            font-size: 15px;
            transition: 0.22s ease;
        }

        .nav-links a:hover {
            color: #fff;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 14px 22px;
            border-radius: 16px;
            font-weight: 800;
            font-size: 15px;
            border: 1px solid transparent;
            transition: transform 0.16s ease, box-shadow 0.25s ease, border-color 0.25s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            white-space: nowrap;
            will-change: transform;
        }

        .btn-primary {
            color: #03151c;
            background: linear-gradient(135deg, #7ff8df 0%, #62f5d4 34%, #5fd4ff 100%);
            box-shadow:
                0 12px 26px rgba(98,245,212,0.18),
                0 0 0 1px rgba(255,255,255,0.06) inset;
        }

        .btn-primary::after {
            content: "";
            position: absolute;
            inset: -60%;
            background: radial-gradient(circle, rgba(255,255,255,0.28), transparent 36%);
            opacity: 0;
            transition: 0.35s ease;
        }

        .btn-primary:hover::after {
            opacity: 1;
        }

        .btn-secondary {
            color: #fff;
            background: rgba(255,255,255,0.04);
            border-color: rgba(255,255,255,0.09);
        }

        .btn-secondary:hover {
            box-shadow: 0 14px 30px rgba(0,0,0,0.20);
        }

        .hero {
            position: relative;
            padding: 58px 0 30px;
        }

        .hero::before {
            content: "";
            position: absolute;
            width: 620px;
            height: 620px;
            background: radial-gradient(circle, rgba(98,245,212,0.09), transparent 68%);
            top: -190px;
            left: -160px;
            filter: blur(100px);
            z-index: 3;
            pointer-events: none;
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 560px;
            height: 560px;
            background: radial-gradient(circle, rgba(72,184,255,0.08), transparent 68%);
            top: -150px;
            right: -160px;
            filter: blur(100px);
            z-index: 3;
            pointer-events: none;
        }

        .hero-shell {
            position: relative;
            border-radius: 34px;
            padding: 34px;
            background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.018));
            border: 1px solid rgba(255,255,255,0.07);
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        .hero-shell::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.035), transparent 28%),
                radial-gradient(circle at 90% 0%, rgba(98,245,212,0.05), transparent 22%);
            pointer-events: none;
        }

        .hero-grid {
            position: relative;
            z-index: 6;
            display: grid;
            grid-template-columns: 1.08fr 0.92fr;
            gap: 26px;
            align-items: stretch;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 16px;
            border-radius: 999px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            color: #d9fff7;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 18px;
        }

        .badge-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 14px rgba(98,245,212,0.55);
        }

        h1 {
            margin: 0;
            font-size: 68px;
            line-height: 0.96;
            letter-spacing: -0.06em;
            max-width: 760px;
        }

        .gradient-text {
            background: linear-gradient(90deg, #ffffff 0%, #e6fff9 20%, #97f7ff 54%, #cec7ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            margin: 18px 0 0;
            font-size: 19px;
            line-height: 1.72;
            color: var(--muted);
            max-width: 720px;
        }

        .hero-actions {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            margin-top: 28px;
        }

        .hero-stats {
            margin-top: 24px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
        }

        .stat-chip {
            padding: 18px 18px;
            border-radius: 18px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.07);
            backdrop-filter: blur(12px);
        }

        .stat-chip strong {
            display: block;
            font-size: 28px;
            margin-bottom: 6px;
            letter-spacing: -0.04em;
        }

        .stat-chip span {
            color: var(--muted);
            font-size: 13px;
        }

        .hero-points {
            margin-top: 18px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }

        .mini-pill {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 14px 16px;
            border-radius: 16px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.07);
            color: #e4edf7;
            font-size: 14px;
        }

        .mini-pill::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            box-shadow: 0 0 10px rgba(98,245,212,0.40);
            flex: 0 0 8px;
        }

        .dashboard {
            position: relative;
            border-radius: 28px;
            padding: 22px;
            background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.025));
            border: 1px solid rgba(255,255,255,0.07);
            backdrop-filter: blur(16px);
            overflow: hidden;
            min-height: 100%;
        }

        .dashboard::before {
            content: "";
            position: absolute;
            width: 160%;
            height: 160%;
            top: -40%;
            left: -36%;
            background: radial-gradient(circle, rgba(98,245,212,0.06), transparent 36%);
            pointer-events: none;
        }

        .dashboard::after {
            content: "";
            position: absolute;
            width: 140%;
            height: 140%;
            bottom: -40%;
            right: -40%;
            background: radial-gradient(circle, rgba(72,184,255,0.05), transparent 36%);
            pointer-events: none;
        }

        .dashboard-inner {
            position: relative;
            z-index: 6;
        }

        .dashboard-head {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: center;
            margin-bottom: 16px;
        }

        .dashboard-title {
            font-size: 22px;
            font-weight: 900;
            letter-spacing: -0.04em;
        }

        .live-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.07);
            color: #d7fff7;
            font-size: 12px;
            font-weight: 700;
        }

        .live-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #34d399;
            box-shadow: 0 0 12px rgba(52,211,153,0.6);
            animation: pulse 1.8s infinite;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 14px;
        }

        .metric {
            padding: 16px;
            border-radius: 18px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
        }

        .metric-label {
            font-size: 12px;
            color: var(--muted-2);
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 28px;
            font-weight: 900;
            letter-spacing: -0.04em;
        }

        .chart-box {
            margin-top: 16px;
            padding: 18px;
            border-radius: 20px;
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.06);
        }

        .chart-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 14px;
        }

        .chart-top strong {
            font-size: 15px;
        }

        .chart-top span {
            font-size: 13px;
            color: var(--muted);
        }

        .bars {
            display: grid;
            gap: 12px;
        }

        .bar-row {
            display: grid;
            grid-template-columns: 120px 1fr 48px;
            gap: 10px;
            align-items: center;
        }

        .bar-label {
            color: var(--muted);
            font-size: 13px;
        }

        .bar-track {
            position: relative;
            height: 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.05);
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #62f5d4, #5fd4ff, #b6b0ff);
            box-shadow: 0 0 14px rgba(98,245,212,0.18);
        }

        .bar-value {
            text-align: right;
            color: #dbfff8;
            font-weight: 700;
            font-size: 13px;
        }

        .trend-card {
            margin-top: 14px;
            padding: 16px;
            border-radius: 18px;
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.06);
        }

        .trend-line {
            position: relative;
            height: 72px;
            margin-top: 14px;
            display: flex;
            align-items: end;
            gap: 12px;
        }

        .trend-col {
            flex: 1;
            position: relative;
            border-radius: 12px 12px 6px 6px;
            background: linear-gradient(180deg, rgba(98,245,212,0.85), rgba(95,212,255,0.35));
            min-height: 20px;
            box-shadow: 0 0 14px rgba(98,245,212,0.10);
        }

        .trend-col::after {
            content: attr(data-label);
            position: absolute;
            bottom: -24px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 11px;
            color: var(--muted-2);
        }

        .section {
            position: relative;
            padding: 44px 0;
        }

        .section-title {
            text-align: center;
            max-width: 860px;
            margin: 0 auto 24px;
        }

        .section-title h2 {
            margin: 0 0 12px;
            font-size: 46px;
            line-height: 1;
            letter-spacing: -0.05em;
        }

        .section-title p {
            margin: 0 auto;
            color: var(--muted);
            line-height: 1.75;
            font-size: 16px;
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
            position: relative;
            overflow: hidden;
            border-radius: 24px;
            padding: 24px;
            background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.025));
            border: 1px solid rgba(255,255,255,0.07);
            box-shadow: var(--shadow);
            transition: transform 0.28s ease, border-color 0.28s ease, box-shadow 0.28s ease;
        }

        .card::before {
            content: "";
            position: absolute;
            width: 220%;
            height: 220%;
            left: -60%;
            top: -70%;
            background: radial-gradient(circle, rgba(98,245,212,0.12), transparent 32%);
            opacity: 0;
            transition: 0.35s ease;
            pointer-events: none;
        }

        .card:hover::before {
            opacity: 1;
        }

        .card:hover {
            transform: translateY(-6px);
            border-color: rgba(98,245,212,0.14);
            box-shadow:
                0 0 0 1px rgba(98,245,212,0.14),
                0 20px 60px rgba(0,0,0,0.34),
                0 0 34px rgba(98,245,212,0.08);
        }

        .card-icon {
            width: 54px;
            height: 54px;
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
            background: linear-gradient(135deg, rgba(98,245,212,0.14), rgba(95,212,255,0.10));
            border: 1px solid rgba(255,255,255,0.07);
            box-shadow: 0 8px 20px rgba(98,245,212,0.06);
        }

        .card h3 {
            margin: 0 0 10px;
            font-size: 22px;
            letter-spacing: -0.03em;
        }

        .card p {
            margin: 0;
            color: var(--muted);
            line-height: 1.75;
            font-size: 15px;
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
            font-size: 15px;
        }

        .demo-list li::before {
            content: "";
            position: absolute;
            left: 0;
            top: 9px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            box-shadow: 0 0 10px rgba(98,245,212,0.35);
        }

        .steps-wrap {
            display: grid;
            grid-template-columns: 0.95fr 1.05fr;
            gap: 22px;
            align-items: stretch;
        }

        .steps-box,
        .preview-box,
        .form-box {
            border-radius: 28px;
            padding: 28px;
            background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.025));
            border: 1px solid rgba(255,255,255,0.07);
            box-shadow: var(--shadow);
        }

        .steps-box h3,
        .preview-box h3,
        .form-box h3 {
            margin: 0 0 14px;
            font-size: 30px;
            letter-spacing: -0.04em;
        }

        .steps-box p,
        .preview-box p,
        .form-box p {
            margin: 0 0 20px;
            color: var(--muted);
            line-height: 1.75;
        }

        .step-item {
            display: grid;
            grid-template-columns: 56px 1fr;
            gap: 14px;
            align-items: start;
            padding: 18px 0;
            border-top: 1px solid rgba(255,255,255,0.06);
        }

        .step-item:first-of-type {
            border-top: 0;
            padding-top: 0;
        }

        .step-num {
            width: 56px;
            height: 56px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 18px;
            color: #03141a;
            background: linear-gradient(135deg, #8af8e5, #60d6ff);
        }

        .step-text strong {
            display: block;
            margin-bottom: 6px;
            font-size: 17px;
        }

        .step-text span {
            color: var(--muted);
            line-height: 1.7;
            font-size: 15px;
        }

        .preview-window {
            border-radius: 22px;
            background: rgba(6,12,25,0.78);
            border: 1px solid rgba(255,255,255,0.06);
            overflow: hidden;
        }

        .preview-top {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 14px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            background: rgba(255,255,255,0.03);
        }

        .preview-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
        }

        .preview-dot:nth-child(1) { background: #ff5f57; }
        .preview-dot:nth-child(2) { background: #febc2e; }
        .preview-dot:nth-child(3) { background: #28c840; }

        .preview-body {
            padding: 18px;
        }

        .preview-row {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 14px;
            margin-bottom: 14px;
        }

        .preview-card {
            padding: 16px;
            border-radius: 18px;
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.055);
        }

        .preview-card strong {
            display: block;
            margin-bottom: 10px;
            font-size: 15px;
        }

        .score-big {
            font-size: 46px;
            font-weight: 900;
            letter-spacing: -0.05em;
            margin-bottom: 6px;
            background: linear-gradient(90deg, #ffffff, #84f5ff, #c7c2ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .small-muted {
            color: var(--muted-2);
            font-size: 13px;
        }

        .tiny-bars {
            display: grid;
            gap: 10px;
            margin-top: 8px;
        }

        .tiny-bar {
            height: 8px;
            border-radius: 999px;
            background: rgba(255,255,255,0.05);
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.04);
        }

        .tiny-bar > div {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #62f5d4, #60d6ff);
        }

        .pricing-grid {
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 22px;
            align-items: stretch;
        }

        .price-card {
            position: relative;
            overflow: hidden;
            border-radius: 30px;
            padding: 30px;
            background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.028));
            border: 1px solid rgba(255,255,255,0.07);
            box-shadow: var(--shadow);
        }

        .price-card.featured {
            border-color: rgba(98,245,212,0.16);
            box-shadow: 0 20px 60px rgba(0,0,0,0.32), 0 0 0 1px rgba(98,245,212,0.05) inset;
        }

        .price-card.featured::before {
            content: "";
            position: absolute;
            width: 220px;
            height: 220px;
            right: -60px;
            top: -60px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(98,245,212,0.12), transparent 60%);
            filter: blur(20px);
        }

        .price-label {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.07);
            color: #ddfff9;
            font-size: 12px;
            font-weight: 800;
        }

        .price-card h3 {
            margin: 0 0 10px;
            font-size: 28px;
            letter-spacing: -0.04em;
        }

        .price-desc {
            color: var(--muted);
            line-height: 1.75;
            margin-bottom: 20px;
        }

        .price-main {
            font-size: 52px;
            font-weight: 900;
            letter-spacing: -0.06em;
            line-height: 1;
            margin-bottom: 6px;
        }

        .price-note {
            color: var(--muted-2);
            font-size: 14px;
            margin-bottom: 18px;
        }

        .feature-list {
            display: grid;
            gap: 12px;
            margin: 18px 0 24px;
        }

        .feature-item {
            display: flex;
            align-items: start;
            gap: 12px;
            color: #e7eef7;
            font-size: 15px;
            line-height: 1.65;
        }

        .feature-item::before {
            content: "";
            width: 10px;
            height: 10px;
            margin-top: 7px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            box-shadow: 0 0 10px rgba(98,245,212,0.35);
            flex: 0 0 10px;
        }

        .pricing-side {
            display: grid;
            gap: 20px;
        }

        .info-card {
            border-radius: 24px;
            padding: 24px;
            background: linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.025));
            border: 1px solid rgba(255,255,255,0.07);
            box-shadow: var(--shadow);
        }

        .info-card h4 {
            margin: 0 0 10px;
            font-size: 20px;
            letter-spacing: -0.03em;
        }

        .info-card p {
            margin: 0;
            color: var(--muted);
            line-height: 1.75;
            font-size: 15px;
        }

        .form-wrap {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 22px;
            align-items: stretch;
        }

        .field {
            margin-bottom: 14px;
        }

        .field input,
        .field select,
        .field textarea {
            width: 100%;
            padding: 15px 16px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.09);
            background: rgba(255,255,255,0.045);
            color: #fff;
            outline: none;
            font-size: 15px;
            transition: 0.22s ease;
        }

        .field input:focus,
        .field select:focus,
        .field textarea:focus {
            border-color: rgba(98,245,212,0.24);
            box-shadow: 0 0 0 4px rgba(98,245,212,0.06);
        }

        .field textarea {
            min-height: 128px;
            resize: vertical;
        }

        .field input::placeholder,
        .field textarea::placeholder {
            color: #8ca1b7;
        }

        .field select option {
            color: #000;
        }

        .helper {
            margin-top: 8px;
            color: #8ad8ff;
            font-size: 13px;
        }

        .contacts-list {
            display: grid;
            gap: 14px;
            margin-top: 20px;
        }

        .contact-item {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 16px;
            border-radius: 18px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            transition: 0.24s ease;
        }

        .contact-item:hover {
            transform: translateY(-3px);
            border-color: rgba(98,245,212,0.14);
        }

        .contact-icon {
            width: 50px;
            height: 50px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(98,245,212,0.14), rgba(95,212,255,0.10));
            border: 1px solid rgba(255,255,255,0.07);
            flex: 0 0 50px;
        }

        .contact-text strong {
            display: block;
            margin-bottom: 4px;
            font-size: 15px;
        }

        .contact-text span {
            color: var(--muted);
            font-size: 14px;
        }

        .alert {
            padding: 16px 18px;
            border-radius: 16px;
            margin-bottom: 18px;
            font-weight: 800;
            font-size: 14px;
        }

        .alert.success {
            background: rgba(34,197,94,0.12);
            border: 1px solid rgba(34,197,94,0.24);
            color: #c7f9d4;
        }

        .alert.error {
            background: rgba(239,68,68,0.12);
            border: 1px solid rgba(239,68,68,0.22);
            color: #ffd0d0;
        }

        .footer {
            position: relative;
            padding: 26px 0 40px;
            text-align: center;
            color: var(--muted);
            font-size: 14px;
            z-index: 5;
        }

        .floating-socials {
            position: fixed;
            right: 18px;
            bottom: 18px;
            display: grid;
            gap: 12px;
            z-index: 120;
        }

        .social-btn {
            width: 58px;
            height: 58px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(7, 18, 39, 0.88);
            border: 1px solid rgba(255,255,255,0.09);
            box-shadow: 0 14px 30px rgba(0,0,0,0.24);
            transition: 0.22s ease;
            backdrop-filter: blur(14px);
        }

        .social-btn:hover {
            transform: translateY(-3px) scale(1.03);
        }

        .hidden-trap {
            position: absolute !important;
            left: -9999px !important;
            width: 1px !important;
            height: 1px !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        .fade-up {
            opacity: 0;
            transform: translateY(28px);
            transition: opacity 0.7s ease, transform 0.7s ease;
        }

        .fade-up.show {
            opacity: 1;
            transform: translateY(0);
        }

        .delay-1 { transition-delay: 0.05s; }
        .delay-2 { transition-delay: 0.12s; }
        .delay-3 { transition-delay: 0.18s; }
        .delay-4 { transition-delay: 0.24s; }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.16); opacity: 0.72; }
        }

        @media (max-width: 1100px) {
            .hero-grid,
            .steps-wrap,
            .pricing-grid,
            .form-wrap,
            .grid-4,
            .grid-3 {
                grid-template-columns: 1fr;
            }

            .hero-stats,
            .metric-grid,
            .hero-points {
                grid-template-columns: 1fr 1fr;
            }

            h1 {
                font-size: 54px;
            }

            .section-title h2 {
                font-size: 38px;
            }
        }

        @media (max-width: 760px) {
            .nav-links {
                display: none;
            }

            .hero-shell {
                padding: 24px;
            }

            h1 {
                font-size: 40px;
            }

            .hero-subtitle {
                font-size: 16px;
            }

            .hero-stats,
            .hero-points,
            .metric-grid {
                grid-template-columns: 1fr;
            }

            .section-title h2 {
                font-size: 32px;
            }

            .bar-row {
                grid-template-columns: 96px 1fr 42px;
            }

            .price-main {
                font-size: 40px;
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

        @media (max-width: 520px) {
            .container {
                padding: 0 16px;
            }

            .nav-inner {
                min-height: 68px;
            }

            .logo {
                font-size: 24px;
            }

            .btn {
                width: 100%;
            }

            .hero-actions {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>

    <canvas id="network-bg"></canvas>

    <section class="hero">
        <div class="orb orb-1 parallax" data-speed="16"></div>
        <div class="orb orb-2 parallax" data-speed="12"></div>

        <div class="navbar">
            <div class="container nav-inner">
                <div class="logo">
                    <div class="logo-mark">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                            <path d="M12 2L14.8 8.2L21 11L14.8 13.8L12 20L9.2 13.8L3 11L9.2 8.2L12 2Z" fill="#62F5D4"/>
                        </svg>
                    </div>
                    <div><span>Voice</span>Score</div>
                </div>

                <div class="nav-links">
                    <a href="#features">Возможности</a>
                    <a href="#how">Как это работает</a>
                    <a href="#reports">Что видно</a>
                    <a href="#pricing">Тариф</a>
                    <a href="#contact">Контакты</a>
                </div>

                <a href="#contact" class="btn btn-primary magnetic">Получить демо</a>
            </div>
        </div>

        <div class="container">
            <div class="hero-shell fade-up show parallax" data-speed="6">
                <div class="hero-grid">
                    <div>
                        <div class="badge">
                            <span class="badge-dot"></span>
                            AI-контроль качества звонков
                        </div>

                        <h1 class="gradient-text">
                            {{ site_title }} —
                            контролируйте 100% звонков без ручной прослушки
                        </h1>

                        <p class="hero-subtitle">
                            Платформа для отделов продаж, взыскания и контакт-центров.
                            Анализирует 100% разговоров, автоматически оценивает каждый диалог,
                            выявляет ошибки, нарушения и слабые места сотрудников,
                            а руководителю показывает понятную и наглядную аналитику.
                        </p>

                        <div class="hero-actions">
                            <a href="#contact" class="btn btn-primary magnetic">Оставить заявку</a>
                            <a href="#reports" class="btn btn-secondary magnetic">Посмотреть возможности</a>
                        </div>

                        <div class="hero-stats">
                            <div class="stat-chip">
                                <strong class="count-up" data-target="100" data-suffix="%">0</strong>
                                <span>анализ звонков, а не выборка</span>
                            </div>
                            <div class="stat-chip">
                                <strong class="count-up" data-target="5" data-prefix="до ">0</strong>
                                <span>до 5 учетных записей / ПК</span>
                            </div>
                            <div class="stat-chip">
                                <strong>ежедневно</strong>
                                <span>отчеты для руководителя</span>
                            </div>
                        </div>

                        <div class="hero-points">
                            <div class="mini-pill">Оценка по сотрудникам и отделам</div>
                            <div class="mini-pill">Контроль скриптов и нарушений</div>
                            <div class="mini-pill">Краткое резюме каждого звонка</div>
                            <div class="mini-pill">Сравнение по месяцам и периодам</div>
                        </div>
                    </div>

                    <div class="dashboard parallax" data-speed="10">
                        <div class="dashboard-inner">
                            <div class="dashboard-head">
                                <div class="dashboard-title">AI Dashboard</div>
                                <div class="live-badge">
                                    <span class="live-dot"></span>
                                    Live analytics
                                </div>
                            </div>

                            <div class="metric-grid">
                                <div class="metric">
                                    <div class="metric-label">Проверено звонков</div>
                                    <div class="metric-value count-up" data-target="12480">0</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Средняя оценка</div>
                                    <div class="metric-value count-up" data-target="86" data-suffix="%">0</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Нарушения</div>
                                    <div class="metric-value count-up" data-target="143">0</div>
                                </div>
                            </div>

                            <div class="chart-box">
                                <div class="chart-top">
                                    <strong>Качество по критериям</strong>
                                    <span>обновляется автоматически</span>
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

                            <div class="trend-card">
                                <strong>Динамика отдела за 6 месяцев</strong>
                                <div class="trend-line">
                                    <div class="trend-col" style="height:34px;" data-label="Окт"></div>
                                    <div class="trend-col" style="height:42px;" data-label="Ноя"></div>
                                    <div class="trend-col" style="height:48px;" data-label="Дек"></div>
                                    <div class="trend-col" style="height:52px;" data-label="Янв"></div>
                                    <div class="trend-col" style="height:60px;" data-label="Фев"></div>
                                    <div class="trend-col" style="height:66px;" data-label="Мар"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="orb orb-3 parallax" data-speed="20"></div>
    </section>

    <section id="features" class="section">
        <div class="container">
            <div class="section-title fade-up">
                <h2>Что умеет система</h2>
                <p>
                    Не просто считает звонки, а помогает руководителю видеть реальные точки роста:
                    качество общения, нарушения, средние оценки, слабых сотрудников и динамику команды.
                </p>
            </div>

            <div class="grid-4">
                <div class="card fade-up delay-1">
                    <div class="card-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M4 18V10M10 18V6M16 18V13M22 18V3" stroke="#62F5D4" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    </div>
                    <h3>Анализ 100% звонков</h3>
                    <p>Проверяется весь поток разговоров, а не случайная выборка. Можно задать фильтр по длительности, например от 1 минуты.</p>
                </div>

                <div class="card fade-up delay-2">
                    <div class="card-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M12 3L14.9 8.8L21 11.1L14.9 13.4L12 19.2L9.1 13.4L3 11.1L9.1 8.8L12 3Z" fill="#62F5D4"/>
                        </svg>
                    </div>
                    <h3>Оценка каждого диалога</h3>
                    <p>Каждый звонок получает балл по критериям вашей компании: скрипт, вежливость, работа с возражениями и результат разговора.</p>
                </div>

                <div class="card fade-up delay-3">
                    <div class="card-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M12 8V12L14.5 14.5M22 12C22 17.5 17.5 22 12 22C6.5 22 2 17.5 2 12C2 6.5 6.5 2 12 2C17.5 2 22 6.5 22 12Z" stroke="#62F5D4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <h3>Выявление ошибок</h3>
                    <p>Система фиксирует грубость, нарушения скрипта, спорные формулировки и отклонения, которые влияют на результат разговора.</p>
                </div>

                <div class="card fade-up delay-4">
                    <div class="card-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M4 19H20M7 16V10M12 16V6M17 16V12" stroke="#62F5D4" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    </div>
                    <h3>Отчеты для руководителя</h3>
                    <p>Показывает среднюю оценку, слабые зоны сотрудников, динамику по месяцам и наглядную аналитику по отделу в одном месте.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="how" class="section">
        <div class="container">
            <div class="steps-wrap">
                <div class="steps-box fade-up">
                    <h3>Как это работает</h3>
                    <p>
                        Внедрение простое: подключаем звонки, настраиваем критерии оценки под ваш процесс
                        и получаем понятную аналитику без лишней ручной работы.
                    </p>

                    <div class="step-item">
                        <div class="step-num">01</div>
                        <div class="step-text">
                            <strong>Подключаем звонки</strong>
                            <span>Загружаем или подключаем поток разговоров из вашей телефонии и начинаем собирать данные для анализа.</span>
                        </div>
                    </div>

                    <div class="step-item">
                        <div class="step-num">02</div>
                        <div class="step-text">
                            <strong>Настраиваем критерии</strong>
                            <span>Баллы, правила, нарушения, обязательные фразы и логика оценки подстраиваются под ваш бизнес-процесс.</span>
                        </div>
                    </div>

                    <div class="step-item">
                        <div class="step-num">03</div>
                        <div class="step-text">
                            <strong>Получаем отчеты</strong>
                            <span>Руководитель видит реальную картину: кто работает сильнее, где теряется клиент и как меняется качество команды.</span>
                        </div>
                    </div>
                </div>

                <div class="preview-box fade-up delay-2">
                    <h3>Как это выглядит внутри</h3>
                    <p>
                        Не просто красивый экран, а рабочий инструмент:
                        оценки, статистика, ошибки, резюме диалогов и динамика по людям и отделам.
                    </p>

                    <div class="preview-window">
                        <div class="preview-top">
                            <div class="preview-dot"></div>
                            <div class="preview-dot"></div>
                            <div class="preview-dot"></div>
                        </div>

                        <div class="preview-body">
                            <div class="preview-row">
                                <div class="preview-card">
                                    <strong>Средняя оценка оператора</strong>
                                    <div class="score-big">89%</div>
                                    <div class="small-muted">+6% к прошлому месяцу</div>
                                </div>

                                <div class="preview-card">
                                    <strong>Проблемные звонки</strong>
                                    <div class="score-big">17</div>
                                    <div class="small-muted">нужно проверить в первую очередь</div>
                                </div>
                            </div>

                            <div class="preview-card">
                                <strong>Соблюдение критериев</strong>
                                <div class="tiny-bars">
                                    <div class="tiny-bar"><div style="width:92%"></div></div>
                                    <div class="tiny-bar"><div style="width:84%"></div></div>
                                    <div class="tiny-bar"><div style="width:76%"></div></div>
                                    <div class="tiny-bar"><div style="width:68%"></div></div>
                                </div>
                            </div>

                            <div class="preview-row" style="margin-top:14px;">
                                <div class="preview-card">
                                    <strong>Резюме звонка</strong>
                                    <div class="small-muted" style="line-height:1.7;">
                                        Клиент сомневался по оплате. Оператор отработал часть возражений,
                                        но не зафиксировал следующий шаг и не закрыл разговор на действие.
                                    </div>
                                </div>

                                <div class="preview-card">
                                    <strong>Главная ошибка</strong>
                                    <div class="small-muted" style="line-height:1.7;">
                                        Не выполнен дожим клиента и не предложен четкий следующий шаг.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="container" style="margin-top:20px;">
            <div class="hero-points fade-up">
                <div class="mini-pill">Подходит для MFO и взыскания</div>
                <div class="mini-pill">Используется в call-центрах</div>
                <div class="mini-pill">Подходит для команд 20–50 человек</div>
                <div class="mini-pill">Настраивается под ваш процесс</div>
            </div>
        </div>
    </section>

    <section id="reports" class="section">
        <div class="container">
            <div class="section-title fade-up">
                <h2>Что видно в отчетах</h2>
                <p>
                    Система показывает не просто цифры, а конкретные причины,
                    почему сотрудник сработал хорошо или плохо, где проседает отдел
                    и какие действия нужно исправить.
                </p>
            </div>

            <div class="grid-3">
                <div class="card fade-up delay-1">
                    <h3>По каждому сотруднику</h3>
                    <ul class="demo-list">
                        <li>средний балл по качеству</li>
                        <li>количество проверенных звонков</li>
                        <li>главные ошибки и нарушения</li>
                        <li>динамика по периодам</li>
                        <li>слабые и сильные стороны</li>
                    </ul>
                </div>

                <div class="card fade-up delay-2">
                    <h3>По отделу</h3>
                    <ul class="demo-list">
                        <li>общий средний результат</li>
                        <li>сравнение между группами</li>
                        <li>выполнение скрипта по отделу</li>
                        <li>рост или просадка по месяцам</li>
                        <li>ключевые точки для руководителя</li>
                    </ul>
                </div>

                <div class="card fade-up delay-3">
                    <h3>По каждому звонку</h3>
                    <ul class="demo-list">
                        <li>краткое резюме разговора</li>
                        <li>оценка и пояснение по баллам</li>
                        <li>фиксация ошибок и грубости</li>
                        <li>причина плохого результата</li>
                        <li>что нужно исправить оператору</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <section id="pricing" class="section">
        <div class="container">
            <div class="section-title fade-up">
                <h2>Тариф и внедрение</h2>
                <p>
                    Подойдет для команд, которым нужен системный контроль качества звонков,
                    прозрачная оценка сотрудников и отчеты для руководителя без ручного прослушивания.
                </p>
            </div>

            <div class="pricing-grid">
                <div class="price-card featured fade-up delay-1">
                    <div class="price-label">Основной пакет</div>
                    <h3>VoiceScore для команды</h3>
                    <div class="price-desc">
                        Полноценное внедрение системы контроля качества звонков с настройкой критериев,
                        логики баллов и отчетов под ваш процесс.
                    </div>

                    <div class="price-main">300 000 ₸</div>
                    <div class="price-note">ежемесячно</div>

                    <div class="feature-list">
                        <div class="feature-item">анализ 100% звонков</div>
                        <div class="feature-item">оценка каждого диалога по вашим критериям</div>
                        <div class="feature-item">выявление нарушений, грубости и ошибок</div>
                        <div class="feature-item">резюме каждого звонка</div>
                        <div class="feature-item">ежедневные отчеты для руководителя</div>
                        <div class="feature-item">до 5 учетных записей / до 5 ПК</div>
                    </div>

                    <a href="#contact" class="btn btn-primary magnetic">Оставить заявку</a>
                </div>

                <div class="pricing-side">
                    <div class="info-card fade-up delay-2">
                        <h4>Разовая настройка</h4>
                        <p>
                            100 000 ₸ единоразово — настройка шаблонов, критериев,
                            средней оценки, базовой логики проверки и адаптация под ваш процесс.
                        </p>
                    </div>

                    <div class="info-card fade-up delay-3">
                        <h4>Что нужно с вашей стороны</h4>
                        <p>
                            Для работы программы обязательно потребуются API-ключи и доступы
                            к используемым сервисам ИИ и телефонии. Эти ключи нужны для того,
                            чтобы после покупки система могла анализировать звонки,
                            обрабатывать данные и формировать отчеты внутри вашего процесса.
                        </p>
                    </div>

                    <div class="info-card fade-up delay-4">
                        <h4>Итого на старт</h4>
                        <p>
                            400 000 ₸ на запуск:
                            300 000 ₸ первый месяц + 100 000 ₸ настройка.
                            Далее — 300 000 ₸ ежемесячно.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="section">
        <div class="container">
            <div class="form-wrap">
                <div class="form-box fade-up">
                    <h3>Оставить заявку</h3>
                    <p>
                        Заполните форму. Заявка сразу уйдет в Telegram.
                        Мы свяжемся с вами, покажем демо и обсудим,
                        как адаптировать систему под ваш процесс.
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

                        <button type="submit" class="btn btn-primary magnetic" style="width:100%;">Отправить заявку</button>
                    </form>
                </div>

                <div class="form-box fade-up delay-2">
                    <h3>Связаться напрямую</h3>
                    <p>
                        Можно не ждать форму и сразу написать нам.
                        Кнопки ниже открывают Telegram и WhatsApp.
                    </p>

                    <div class="contacts-list">
                        <a class="contact-item" href="{{ telegram_link }}" target="_blank" rel="noopener noreferrer">
                            <div class="contact-icon">
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                                    <path d="M21 4L3.9 10.6C2.7 11.1 2.7 11.8 3.7 12.1L8.1 13.5L18.3 7.1C18.8 6.8 19.3 7 18.9 7.4L10.6 14.9V19.1C10.6 19.7 10.9 20 11.4 20C11.8 20 12 19.8 12.2 19.5L14.3 16.9L18.7 20.2C19.5 20.6 20.1 20.4 20.3 19.5L23.2 5.7C23.5 4.6 22.8 4.1 21.9 4.5L21 4Z" fill="#62F5D4"/>
                                </svg>
                            </div>
                            <div class="contact-text">
                                <strong>Telegram</strong>
                                <span>@Mussayev_Yermurat</span>
                            </div>
                        </a>

                        <a class="contact-item" href="{{ whatsapp_link }}" target="_blank" rel="noopener noreferrer">
                            <div class="contact-icon">
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                                    <path d="M20.5 3.5C18.3 1.3 15.4 0 12.2 0C5.6 0 0.3 5.3 0.3 11.9C0.3 14 0.8 16 1.9 17.8L0 24L6.4 22.1C8.1 23 10.1 23.5 12.1 23.5H12.2C18.8 23.5 24.1 18.2 24.1 11.6C24.1 8.4 22.8 5.7 20.5 3.5ZM12.2 21.5H12.1C10.3 21.5 8.6 21 7.1 20.1L6.7 19.9L3 21L4.1 17.4L3.9 17C2.9 15.4 2.4 13.7 2.4 11.9C2.4 6.5 6.8 2.1 12.2 2.1C14.8 2.1 17.2 3.1 19 4.9C20.8 6.7 21.9 9.1 21.8 11.7C21.8 17.1 17.5 21.5 12.2 21.5ZM17.5 14.2C17.2 14.1 15.8 13.4 15.5 13.3C15.2 13.2 15 13.1 14.8 13.4C14.6 13.7 14.1 14.3 13.9 14.5C13.7 14.7 13.5 14.8 13.2 14.6C11.4 13.7 10.2 12.9 9 10.8C8.7 10.3 9.3 10.4 9.8 9.3C9.9 9.1 9.9 8.9 9.8 8.7C9.7 8.5 9.1 7.1 8.8 6.4C8.5 5.7 8.2 5.8 7.9 5.8C7.7 5.8 7.5 5.8 7.2 5.8C7 5.8 6.6 5.9 6.3 6.2C6 6.5 5.2 7.2 5.2 8.7C5.2 10.2 6.3 11.7 6.4 11.9C6.6 12.1 8.6 15.2 11.6 16.5C13.5 17.3 14.2 17.4 15.2 17.3C15.8 17.2 17.1 16.6 17.4 15.8C17.7 15 17.7 14.4 17.5 14.2Z" fill="#62F5D4"/>
                                </svg>
                            </div>
                            <div class="contact-text">
                                <strong>WhatsApp</strong>
                                <span>+7 700 119 9771</span>
                            </div>
                        </a>
                    </div>

                    <div style="margin-top:20px; padding:18px; border-radius:18px; background:rgba(255,255,255,0.035); border:1px solid rgba(255,255,255,0.06);">
                        <strong style="display:block; margin-bottom:8px;">Подходит для:</strong>
                        <div style="color: var(--muted); line-height:1.75; font-size:15px;">
                            отделов взыскания, продаж, call-центров, служб контроля качества и руководителей,
                            которым нужна реальная картина по звонкам, а не ручная выборка.
                        </div>
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
                <path d="M21 4L3.9 10.6C2.7 11.1 2.7 11.8 3.7 12.1L8.1 13.5L18.3 7.1C18.8 6.8 19.3 7 18.9 7.4L10.6 14.9V19.1C10.6 19.7 10.9 20 11.4 20C11.8 20 12 19.8 12.2 19.5L14.3 16.9L18.7 20.2C19.5 20.6 20.1 20.4 20.3 19.5L23.2 5.7C23.5 4.6 22.8 4.1 21.9 4.5L21 4Z" fill="#62F5D4"/>
            </svg>
        </a>

        <a class="social-btn" href="{{ whatsapp_link }}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M20.5 3.5C18.3 1.3 15.4 0 12.2 0C5.6 0 0.3 5.3 0.3 11.9C0.3 14 0.8 16 1.9 17.8L0 24L6.4 22.1C8.1 23 10.1 23.5 12.1 23.5H12.2C18.8 23.5 24.1 18.2 24.1 11.6C24.1 8.4 22.8 5.7 20.5 3.5ZM12.2 21.5H12.1C10.3 21.5 8.6 21 7.1 20.1L6.7 19.9L3 21L4.1 17.4L3.9 17C2.9 15.4 2.4 13.7 2.4 11.9C2.4 6.5 6.8 2.1 12.2 2.1C14.8 2.1 17.2 3.1 19 4.9C20.8 6.7 21.9 9.1 21.8 11.7C21.8 17.1 17.5 21.5 12.2 21.5ZM17.5 14.2C17.2 14.1 15.8 13.4 15.5 13.3C15.2 13.2 15 13.1 14.8 13.4C14.6 13.7 14.1 14.3 13.9 14.5C13.7 14.7 13.5 14.8 13.2 14.6C11.4 13.7 10.2 12.9 9 10.8C8.7 10.3 9.3 10.4 9.8 9.3C9.9 9.1 9.9 8.9 9.8 8.7C9.7 8.5 9.1 7.1 8.8 6.4C8.5 5.7 8.2 5.8 7.9 5.8C7.7 5.8 7.5 5.8 7.2 5.8C7 5.8 6.6 5.9 6.3 6.2C6 6.5 5.2 7.2 5.2 8.7C5.2 10.2 6.3 11.7 6.4 11.9C6.6 12.1 8.6 15.2 11.6 16.5C13.5 17.3 14.2 17.4 15.2 17.3C15.8 17.2 17.1 16.6 17.4 15.8C17.7 15 17.7 14.4 17.5 14.2Z" fill="#62F5D4"/>
            </svg>
        </a>
    </div>

    <script>
        const phoneInput = document.getElementById("phone");

        if (phoneInput) {
            phoneInput.addEventListener("input", function(e) {
                let x = e.target.value.replace(/\\D/g, "");

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

        const animated = document.querySelectorAll('.fade-up');

        const reveal = () => {
            animated.forEach(el => {
                const top = el.getBoundingClientRect().top;
                if (top < window.innerHeight - 80) {
                    el.classList.add('show');
                }
            });
        };

        reveal();
        window.addEventListener('scroll', reveal);

        function animateValue(el, start, end, duration, prefix = "", suffix = "") {
            let startTime = null;

            function step(timestamp) {
                if (!startTime) startTime = timestamp;
                const progress = Math.min((timestamp - startTime) / duration, 1);
                const current = Math.floor(progress * (end - start) + start);
                el.textContent = prefix + current.toLocaleString('ru-RU') + suffix;
                if (progress < 1) requestAnimationFrame(step);
            }

            requestAnimationFrame(step);
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;

                const el = entry.target;
                if (el.dataset.animated === "true") return;

                const target = parseInt(el.dataset.target || "0", 10);
                const prefix = el.dataset.prefix || "";
                const suffix = el.dataset.suffix || "";
                animateValue(el, 0, target, 1300, prefix, suffix);
                el.dataset.animated = "true";
            });
        }, { threshold: 0.45 });

        document.querySelectorAll(".count-up").forEach(el => observer.observe(el));

        document.querySelectorAll(".magnetic").forEach(btn => {
            btn.addEventListener("mousemove", e => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                btn.style.transform = `translate(${x * 0.14}px, ${y * 0.14}px)`;
            });

            btn.addEventListener("mouseleave", () => {
                btn.style.transform = "";
            });
        });

        document.addEventListener("mousemove", e => {
            const x = (e.clientX / window.innerWidth - 0.5);
            const y = (e.clientY / window.innerHeight - 0.5);

            document.querySelectorAll(".parallax").forEach(el => {
                const speed = parseFloat(el.dataset.speed || "10");
                el.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
            });
        });

        const canvas = document.getElementById("network-bg");
        const ctx = canvas.getContext("2d");

        let w, h, particles = [];
        let mouse = {
            x: null,
            y: null,
            radius: 160
        };

        function resizeCanvas() {
            w = canvas.width = window.innerWidth;
            h = canvas.height = window.innerHeight;

            const count = Math.min(85, Math.floor(w / 22));
            particles = [];

            for (let i = 0; i < count; i++) {
                particles.push({
                    x: Math.random() * w,
                    y: Math.random() * h,
                    vx: (Math.random() - 0.5) * 0.28,
                    vy: (Math.random() - 0.5) * 0.28,
                    r: Math.random() * 1.5 + 0.7
                });
            }
        }

        function drawGlow(x, y, size, color) {
            const g = ctx.createRadialGradient(x, y, 0, x, y, size);
            g.addColorStop(0, color);
            g.addColorStop(1, "rgba(0,0,0,0)");
            ctx.fillStyle = g;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
        }

        function animateBackground() {
            ctx.clearRect(0, 0, w, h);

            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];

                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > w) p.vx *= -1;
                if (p.y < 0 || p.y > h) p.vy *= -1;

                if (mouse.x !== null && mouse.y !== null) {
                    const dxm = p.x - mouse.x;
                    const dym = p.y - mouse.y;
                    const distm = Math.sqrt(dxm * dxm + dym * dym);

                    if (distm < mouse.radius) {
                        const force = (mouse.radius - distm) / mouse.radius;
                        p.x += (dxm / distm) * force * 0.9 || 0;
                        p.y += (dym / distm) * force * 0.9 || 0;
                    }
                }

                drawGlow(p.x, p.y, 7, "rgba(98,245,212,0.03)");

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = "rgba(120,245,230,0.55)";
                ctx.fill();
            }

            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 115) {
                        const alpha = (1 - dist / 115) * 0.14;
                        ctx.strokeStyle = `rgba(98,245,212,${alpha})`;
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }

            if (mouse.x !== null && mouse.y !== null) {
                drawGlow(mouse.x, mouse.y, 90, "rgba(72,184,255,0.035)");
            }

            requestAnimationFrame(animateBackground);
        }

        window.addEventListener("mousemove", (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        window.addEventListener("mouseout", () => {
            mouse.x = null;
            mouse.y = null;
        });

        window.addEventListener("resize", resizeCanvas);

        resizeCanvas();
        animateBackground();
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
