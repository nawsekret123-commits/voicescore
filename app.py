from flask import Flask, request, redirect, url_for, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = "8799281877:AAHuImnbo4676epEZKKmRuMRR5skmR-0F2g"
TELEGRAM_CHAT_ID = "622522768"


def send_telegram(name, phone, service, comment):
    text = f"""
Новая заявка AqylFlow

Имя: {name}
Телефон: {phone}
Услуга: {service}
Комментарий: {comment if comment else "-"}
Время: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}
"""
    url = f"https://api.telegram.org/bot{622522768}/sendMessage"
    requests.post(
        url,
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=10
    )


HTML = r"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AqylFlow — AI контроль качества звонков</title>
    <meta name="description" content="AqylFlow — AI-платформа для контроля качества звонков, dashboard, AI-поиска и управленческой отчётности.">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

    <style>
        * {
            box-sizing: border-box;
            scroll-behavior: smooth;
        }

        :root {
            --bg-1: #040816;
            --bg-2: #091120;
            --card: rgba(14, 22, 38, 0.58);
            --card-2: rgba(17, 28, 48, 0.64);
            --line: rgba(255,255,255,0.10);
            --line-soft: rgba(255,255,255,0.06);
            --text: #f8fafc;
            --muted: #cbd5e1;
            --muted-2: #94a3b8;
            --accent: #5eead4;
            --accent-2: #2dd4bf;
            --accent-3: #67e8f9;
            --green: #22c55e;
            --orange: #f59e0b;
            --red: #ef4444;
            --shadow: 0 30px 80px rgba(0,0,0,0.35);
        }

        body {
            margin: 0;
            font-family: "Inter", sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at 10% 15%, rgba(20,184,166,0.12), transparent 25%),
                radial-gradient(circle at 88% 8%, rgba(103,232,249,0.10), transparent 24%),
                radial-gradient(circle at 55% 90%, rgba(45,212,191,0.08), transparent 28%),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
            overflow-x: hidden;
            letter-spacing: -0.01em;
        }

        a {
            text-decoration: none;
            color: inherit;
        }

        #network-bg {
            position: fixed;
            inset: 0;
            width: 100%;
            height: 100%;
            z-index: -5;
            display: block;
        }

        .grid-noise {
            position: fixed;
            inset: 0;
            z-index: -4;
            opacity: 0.05;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
            background-size: 34px 34px;
            mask-image: radial-gradient(circle at center, black 40%, transparent 88%);
        }

        .bg-orb {
            position: fixed;
            width: 420px;
            height: 420px;
            border-radius: 50%;
            filter: blur(90px);
            pointer-events: none;
            z-index: -3;
            opacity: 0.18;
            transition: transform 0.2s linear;
            animation: drift 14s ease-in-out infinite;
        }

        .bg-orb-1 {
            left: -120px;
            top: 120px;
            background: radial-gradient(circle, rgba(94,234,212,0.7), transparent 65%);
        }

        .bg-orb-2 {
            right: -120px;
            top: 80px;
            background: radial-gradient(circle, rgba(45,212,191,0.45), transparent 65%);
            animation-delay: 2s;
        }

        .bg-orb-3 {
            left: 35%;
            bottom: -180px;
            width: 480px;
            height: 480px;
            background: radial-gradient(circle, rgba(103,232,249,0.18), transparent 70%);
            animation-delay: 4s;
        }

        @keyframes drift {
            0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
            50% { transform: translate3d(20px, -18px, 0) scale(1.04); }
        }

        .cursor-glow {
            position: fixed;
            width: 320px;
            height: 320px;
            left: 0;
            top: 0;
            border-radius: 50%;
            pointer-events: none;
            z-index: -2;
            background: radial-gradient(circle, rgba(94,234,212,0.12), transparent 65%);
            filter: blur(32px);
            transform: translate(-50%, -50%);
            opacity: 0.7;
        }

        .container {
            width: 100%;
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .glow-text {
            text-shadow:
                0 0 10px rgba(94,234,212,0.18),
                0 0 24px rgba(45,212,191,0.10);
        }

        .glass {
            background: var(--card);
            border: 1px solid var(--line);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            box-shadow: var(--shadow);
        }

        .gradient-border {
            position: relative;
        }

        .gradient-border::after {
            content: "";
            position: absolute;
            inset: 0;
            padding: 1px;
            border-radius: inherit;
            background: linear-gradient(
                135deg,
                rgba(94,234,212,0.34),
                rgba(103,232,249,0.12),
                rgba(255,255,255,0.04),
                rgba(45,212,191,0.24)
            );
            background-size: 220% 220%;
            animation: borderFlow 8s linear infinite;
            -webkit-mask:
                linear-gradient(#fff 0 0) content-box,
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
        }

        @keyframes borderFlow {
            0% { background-position: 0% 50%; }
            100% { background-position: 200% 50%; }
        }

        .navbar {
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(16px);
            background: rgba(4, 8, 20, 0.72);
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }

        .nav-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            padding: 18px 0;
        }

        .logo {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .logo-mark {
            width: 34px;
            height: 34px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(94,234,212,0.18), rgba(45,212,191,0.12));
            border: 1px solid rgba(94,234,212,0.16);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
        }

        .logo-mark svg {
            width: 18px;
            height: 18px;
            color: var(--accent);
        }

        .logo span {
            color: var(--accent);
        }

        .nav-links {
            display: flex;
            flex-wrap: wrap;
            gap: 18px;
            align-items: center;
        }

        .nav-links a {
            color: var(--muted);
            font-size: 15px;
            font-weight: 500;
            transition: 0.25s ease;
            position: relative;
        }

        .nav-links a::after {
            content: "";
            position: absolute;
            left: 0;
            bottom: -6px;
            width: 0;
            height: 2px;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--accent), var(--accent-3));
            transition: width 0.3s ease;
        }

        .nav-links a:hover {
            color: #fff;
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        .btn {
            display: inline-flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            padding: 14px 22px;
            border-radius: 16px;
            border: 1px solid transparent;
            font-weight: 700;
            font-size: 15px;
            cursor: pointer;
            transition: 0.25s ease;
            position: relative;
            overflow: hidden;
            will-change: transform;
        }

        .btn::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, transparent 20%, rgba(255,255,255,0.20), transparent 80%);
            transform: translateX(-130%);
            transition: 0.7s ease;
        }

        .btn:hover::before {
            transform: translateX(130%);
        }

        .btn-primary {
            color: #042f2e;
            background: linear-gradient(135deg, #5eead4 0%, #2dd4bf 100%);
            box-shadow:
                0 12px 30px rgba(20,184,166,0.22),
                0 0 22px rgba(94,234,212,0.14);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
        }

        .btn-secondary {
            color: #fff;
            background: rgba(255,255,255,0.05);
            border-color: rgba(255,255,255,0.10);
        }

        .btn-secondary:hover {
            transform: translateY(-3px);
            border-color: rgba(94,234,212,0.22);
            box-shadow: 0 0 26px rgba(94,234,212,0.08);
        }

        .hero {
            padding: 56px 0 28px;
        }

        .hero-box {
            position: relative;
            overflow: hidden;
            border-radius: 32px;
            padding: 58px;
            background: linear-gradient(135deg, rgba(7,12,24,0.96), rgba(16,22,41,0.90));
            border: 1px solid rgba(255,255,255,0.08);
        }

        .hero-box::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                radial-gradient(circle at 75% 15%, rgba(94,234,212,0.08), transparent 25%),
                linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
            pointer-events: none;
        }

        .hero-grid {
            position: relative;
            z-index: 2;
            display: grid;
            grid-template-columns: 1.02fr 0.98fr;
            gap: 28px;
            align-items: center;
        }

        .badge {
            display: inline-block;
            padding: 10px 15px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.10);
            color: #d9fffb;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 18px;
        }

        .hero h1 {
            margin: 0 0 18px;
            font-size: 58px;
            line-height: 0.98;
            letter-spacing: -0.05em;
            font-weight: 900;
        }

        .hero p {
            margin: 0 0 26px;
            max-width: 760px;
            color: var(--muted);
            line-height: 1.75;
            font-size: 17px;
            font-weight: 500;
        }

        .hero-actions {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            margin-bottom: 22px;
        }

        .hero-points {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-top: 20px;
        }

        .mini-pill {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            color: #e2e8f0;
            border-radius: 14px;
            padding: 12px 14px;
            font-size: 14px;
            font-weight: 500;
        }

        .hero-preview {
            position: relative;
            min-height: 540px;
        }

        .hero-dashboard {
            position: relative;
            z-index: 3;
            border-radius: 28px;
            padding: 22px;
        }

        .hero-dashboard-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 18px;
        }

        .hero-dashboard-title {
            font-size: 20px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .hero-dashboard-badge {
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            color: #d9fffb;
            font-size: 12px;
            font-weight: 600;
        }

        .hero-dashboard-grid {
            display: grid;
            gap: 14px;
        }

        .hero-metric {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }

        .hero-metric-box {
            padding: 14px;
            border-radius: 18px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
        }

        .hero-metric-label {
            font-size: 12px;
            color: var(--muted-2);
            margin-bottom: 8px;
            font-weight: 500;
        }

        .hero-metric-value {
            font-size: 24px;
            font-weight: 800;
            color: #fff;
            letter-spacing: -0.03em;
        }

        .typing-wrap {
            min-height: 58px;
            padding: 14px 16px;
            border-radius: 16px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            color: #e5e7eb;
            line-height: 1.6;
            font-size: 14px;
            font-weight: 500;
        }

        .typing-cursor {
            display: inline-block;
            width: 9px;
            animation: blink 1s infinite;
            color: var(--accent);
        }

        @keyframes blink {
            0%, 49% { opacity: 1; }
            50%, 100% { opacity: 0; }
        }

        .hero-bars {
            display: grid;
            gap: 10px;
        }

        .hero-bar-row {
            display: grid;
            grid-template-columns: 140px 1fr 46px;
            gap: 10px;
            align-items: center;
        }

        .hero-bar-label {
            color: var(--muted);
            font-size: 13px;
            font-weight: 500;
        }

        .hero-bar-track {
            height: 8px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .hero-bar-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #14b8a6, #5eead4, #99f6e4);
        }

        .hero-bar-value {
            color: var(--accent);
            font-weight: 800;
            font-size: 13px;
            text-align: right;
        }

        .float-card {
            position: absolute;
            z-index: 4;
            padding: 14px 16px;
            border-radius: 18px;
            background: rgba(11, 18, 33, 0.76);
            border: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(16px);
            box-shadow: 0 18px 40px rgba(0,0,0,0.25);
            animation: floatCard 5s ease-in-out infinite;
        }

        .float-card small {
            display: block;
            color: var(--muted-2);
            margin-bottom: 6px;
            font-size: 12px;
            font-weight: 500;
        }

        .float-card strong {
            display: block;
            font-size: 18px;
            font-weight: 800;
            color: #fff;
            letter-spacing: -0.03em;
        }

        .float-card-1 {
            top: 36px;
            right: -12px;
            animation-delay: 0s;
        }

        .float-card-2 {
            left: -14px;
            bottom: 100px;
            animation-delay: 1s;
        }

        .float-card-3 {
            right: 30px;
            bottom: -12px;
            animation-delay: 2s;
        }

        @keyframes floatCard {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }

        .section {
            padding: 38px 0;
        }

        .section-title {
            margin-bottom: 20px;
        }

        .section-title.center {
            text-align: center;
        }

        .section-title h2 {
            margin: 0 0 10px;
            font-size: 40px;
            line-height: 1.05;
            letter-spacing: -0.045em;
            font-weight: 800;
        }

        .section-title p {
            margin: 0;
            color: var(--muted-2);
            line-height: 1.75;
            max-width: 860px;
            font-size: 15px;
            font-weight: 500;
        }

        .section-title.center p {
            margin: 0 auto;
        }

        .feature,
        .demo-card,
        .faq-item,
        .dashboard-shell,
        .system-ui,
        .chat-search-card,
        .form-box,
        .report-hero,
        .report-card,
        .report-benefit {
            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;
            transform-style: preserve-3d;
            position: relative;
            overflow: hidden;
        }

        .feature::before,
        .demo-card::before,
        .faq-item::before,
        .dashboard-shell::before,
        .system-ui::before,
        .chat-search-card::before,
        .form-box::before,
        .report-hero::before,
        .report-card::before,
        .report-benefit::before {
            content: "";
            position: absolute;
            width: 240px;
            height: 240px;
            left: var(--mx, 50%);
            top: var(--my, 50%);
            transform: translate(-50%, -50%);
            background: radial-gradient(circle, rgba(94,234,212,0.12), transparent 62%);
            opacity: 0;
            transition: opacity 0.25s ease;
            pointer-events: none;
        }

        .feature:hover,
        .demo-card:hover,
        .faq-item:hover,
        .dashboard-shell:hover,
        .system-ui:hover,
        .chat-search-card:hover,
        .form-box:hover,
        .report-hero:hover,
        .report-card:hover,
        .report-benefit:hover {
            border-color: rgba(94,234,212,0.18);
            box-shadow:
                0 18px 40px rgba(0,0,0,0.2),
                0 0 24px rgba(94,234,212,0.06);
        }

        .feature:hover::before,
        .demo-card:hover::before,
        .faq-item:hover::before,
        .dashboard-shell:hover::before,
        .system-ui:hover::before,
        .chat-search-card:hover::before,
        .form-box:hover::before,
        .report-hero:hover::before,
        .report-card:hover::before,
        .report-benefit:hover::before {
            opacity: 1;
        }

        .grid-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }

        .feature,
        .demo-card,
        .faq-item,
        .report-card,
        .report-benefit {
            border-radius: 24px;
            padding: 24px;
        }

        .feature h3,
        .demo-card h3,
        .faq-item h3,
        .dashboard-card h3,
        .system-panel h3,
        .chat-search-card h3,
        .report-hero h3,
        .report-card h3,
        .report-benefit h3,
        .search-side-panel h3 {
            margin: 0 0 12px;
            color: #fff;
            position: relative;
            z-index: 2;
            font-size: 22px;
            line-height: 1.15;
            letter-spacing: -0.04em;
            font-weight: 800;
        }

        .feature p,
        .demo-card p,
        .faq-item p,
        .system-panel p,
        .chat-search-card p,
        .report-hero p,
        .report-card p,
        .report-benefit p,
        .search-side-panel p {
            margin: 0;
            color: var(--muted);
            line-height: 1.8;
            position: relative;
            z-index: 2;
            font-size: 15px;
            font-weight: 500;
        }

        .report-hero {
            border-radius: 30px;
            padding: 36px;
            background:
                linear-gradient(135deg, rgba(20,184,166,0.14), rgba(45,212,191,0.10)),
                rgba(255,255,255,0.04);
            border: 1px solid rgba(94,234,212,0.14);
        }

        .report-hero::after {
            content: "";
            position: absolute;
            right: -60px;
            top: -60px;
            width: 220px;
            height: 220px;
            background: radial-gradient(circle, rgba(94,234,212,0.16), transparent 68%);
            filter: blur(10px);
        }

        .report-hero-content {
            position: relative;
            z-index: 2;
        }

        .report-highlight {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-top: 22px;
        }

        .report-pill {
            padding: 14px 16px;
            border-radius: 16px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            color: #e5e7eb;
            font-size: 14px;
            font-weight: 700;
            min-height: 58px;
            display: flex;
            align-items: center;
            position: relative;
            z-index: 2;
        }

        .report-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 22px;
            align-items: stretch;
        }

        .report-card {
            min-height: 100%;
            display: flex;
            flex-direction: column;
        }

        .report-card h3 {
            min-height: 64px;
            display: flex;
            align-items: flex-start;
        }

        .report-list {
            display: grid;
            gap: 10px;
            margin-top: 14px;
            flex: 1;
            position: relative;
            z-index: 2;
        }

        .report-row {
            display: grid;
            grid-template-columns: 1.15fr 1fr;
            align-items: center;
            gap: 16px;
            padding: 14px 16px;
            border-radius: 16px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            color: #e5e7eb;
            min-height: 74px;
            font-size: 14px;
            font-weight: 500;
        }

        .report-row strong {
            color: var(--accent);
            line-height: 1.25;
            font-weight: 800;
            text-align: left;
            letter-spacing: -0.02em;
        }

        .report-benefits-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            margin-top: 22px;
        }

        .demo-wrap {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .score-box {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 14px;
            border-radius: 14px;
            background: rgba(34,197,94,0.12);
            border: 1px solid rgba(34,197,94,0.22);
            color: #86efac;
            font-weight: 700;
            margin: 10px 0 14px;
            position: relative;
            z-index: 2;
            font-size: 14px;
        }

        .demo-card ul {
            list-style: none;
            padding: 0;
            margin: 14px 0 0;
            position: relative;
            z-index: 2;
        }

        .demo-card li {
            position: relative;
            padding-left: 18px;
            margin-bottom: 10px;
            color: var(--muted);
            line-height: 1.7;
            font-size: 15px;
            font-weight: 500;
        }

        .demo-card li::before {
            content: "•";
            position: absolute;
            left: 0;
            color: var(--accent);
        }

        .error-row,
        .metric-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
            margin-bottom: 10px;
            padding: 12px 14px;
            border-radius: 14px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            position: relative;
            z-index: 2;
            font-size: 14px;
            font-weight: 600;
        }

        .error-row span:last-child,
        .metric-row span:last-child {
            color: var(--accent);
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .dashboard-shell {
            border-radius: 30px;
            padding: 22px;
            background:
                linear-gradient(180deg, rgba(10,16,30,0.96), rgba(10,16,30,0.86));
        }

        .dashboard-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 14px;
            margin-bottom: 18px;
            flex-wrap: wrap;
            position: relative;
            z-index: 2;
        }

        .dashboard-title {
            font-size: 20px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .dashboard-badge {
            padding: 10px 14px;
            border-radius: 999px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            color: #d9fffb;
            font-size: 13px;
            font-weight: 600;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 0.95fr 1.05fr;
            gap: 18px;
            position: relative;
            z-index: 2;
        }

        .dashboard-left,
        .dashboard-right {
            display: grid;
            gap: 18px;
        }

        .dashboard-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 22px;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .dashboard-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
            pointer-events: none;
        }

        .animated-score-wrap {
            display: flex;
            justify-content: space-between;
            align-items: end;
            gap: 14px;
            margin-bottom: 14px;
        }

        .animated-score {
            font-size: 56px;
            font-weight: 900;
            line-height: 1;
            color: var(--accent);
            text-shadow: 0 0 18px rgba(94,234,212,0.12);
            letter-spacing: -0.05em;
        }

        .score-status {
            padding: 8px 12px;
            border-radius: 12px;
            background: rgba(34,197,94,0.12);
            border: 1px solid rgba(34,197,94,0.22);
            color: #86efac;
            font-size: 13px;
            font-weight: 700;
        }

        .mini-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }

        .mini-stat {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 14px;
        }

        .mini-stat-label {
            color: var(--muted-2);
            font-size: 12px;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .mini-stat-value {
            font-size: 24px;
            font-weight: 800;
            color: #fff;
            letter-spacing: -0.03em;
        }

        .bars {
            display: grid;
            gap: 12px;
            margin-top: 14px;
        }

        .bar-row {
            display: grid;
            grid-template-columns: 170px 1fr 50px;
            gap: 12px;
            align-items: center;
        }

        .bar-label {
            color: var(--muted);
            font-size: 14px;
            font-weight: 500;
        }

        .bar-track {
            width: 100%;
            height: 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .bar-fill {
            height: 100%;
            width: 0;
            border-radius: 999px;
            background: linear-gradient(90deg, #14b8a6, #5eead4, #99f6e4);
            box-shadow: 0 0 16px rgba(94,234,212,0.18);
            transition: width 1.4s ease;
        }

        .bar-value {
            color: var(--accent);
            font-weight: 800;
            text-align: right;
            letter-spacing: -0.02em;
        }

        .line-chart {
            position: relative;
            height: 240px;
            background:
                linear-gradient(to top, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 100% 48px;
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.06);
        }

        .chart-svg {
            width: 100%;
            height: 100%;
            display: block;
        }

        .legend {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            margin-top: 14px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--muted);
            font-size: 13px;
            font-weight: 500;
        }

        .legend-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .search-wrap {
            display: grid;
            grid-template-columns: 1.08fr 0.92fr;
            gap: 20px;
        }

        .chat-search-card,
        .search-side-panel {
            border-radius: 26px;
            padding: 24px;
        }

        .search-input-wrap {
            display: flex;
            gap: 10px;
            margin-top: 16px;
            margin-bottom: 16px;
            position: relative;
            z-index: 2;
        }

        .search-input {
            flex: 1;
            padding: 14px 16px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.10);
            background: rgba(255,255,255,0.06);
            color: white;
            outline: none;
            font-family: "Inter", sans-serif;
            font-size: 14px;
            font-weight: 500;
        }

        .search-results {
            display: grid;
            gap: 12px;
            position: relative;
            z-index: 2;
        }

        .search-result {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 14px;
        }

        .search-result strong {
            display: block;
            margin-bottom: 6px;
            color: #fff;
            font-size: 15px;
            font-weight: 700;
        }

        .search-result .tag-row {
            margin-top: 10px;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .mini-tag {
            display: inline-flex;
            align-items: center;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            background: rgba(94,234,212,0.10);
            border: 1px solid rgba(94,234,212,0.18);
            color: #c8fff7;
        }

        .typing-log {
            display: grid;
            gap: 10px;
            margin-top: 14px;
        }

        .typing-row {
            padding: 12px 14px;
            border-radius: 14px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            font-size: 14px;
            color: #e5e7eb;
            min-height: 48px;
            display: flex;
            align-items: center;
        }

        .typing-row .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent);
            margin-right: 10px;
            box-shadow: 0 0 12px rgba(94,234,212,0.6);
            flex: 0 0 auto;
        }

        .system-ui {
            border-radius: 30px;
            padding: 0;
            overflow: hidden;
        }

        .system-topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 18px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.03);
        }

        .system-brand {
            font-weight: 800;
            color: #fff;
            letter-spacing: -0.03em;
        }

        .system-actions {
            display: flex;
            gap: 10px;
        }

        .system-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: rgba(255,255,255,0.22);
        }

        .system-body {
            display: grid;
            grid-template-columns: 240px 1fr;
            min-height: 540px;
        }

        .system-sidebar {
            padding: 18px;
            border-right: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.02);
        }

        .system-menu {
            display: grid;
            gap: 10px;
            margin-top: 16px;
        }

        .system-menu-item {
            padding: 12px 14px;
            border-radius: 14px;
            color: var(--muted);
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.04);
            font-size: 14px;
            font-weight: 500;
        }

        .system-menu-item.active {
            color: #fff;
            background: linear-gradient(135deg, rgba(20,184,166,0.18), rgba(45,212,191,0.14));
            border: 1px solid rgba(94,234,212,0.14);
        }

        .system-content {
            padding: 18px;
            display: grid;
            gap: 18px;
        }

        .system-panels {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
        }

        .system-panel {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 20px;
            padding: 18px;
            position: relative;
            overflow: hidden;
        }

        .system-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
        }

        .system-table th,
        .system-table td {
            padding: 12px 10px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            font-size: 14px;
            font-weight: 500;
        }

        .system-table th {
            color: var(--muted-2);
            font-weight: 700;
        }

        .tag {
            display: inline-flex;
            align-items: center;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
        }

        .tag-green {
            background: rgba(34,197,94,0.12);
            border: 1px solid rgba(34,197,94,0.22);
            color: #86efac;
        }

        .tag-blue {
            background: rgba(20,184,166,0.12);
            border: 1px solid rgba(20,184,166,0.22);
            color: #99f6e4;
        }

        .tag-orange {
            background: rgba(245,158,11,0.12);
            border: 1px solid rgba(245,158,11,0.22);
            color: #fcd34d;
        }

        .cta-box {
            border-radius: 30px;
            padding: 36px;
            background:
                linear-gradient(135deg, rgba(20,184,166,0.14), rgba(45,212,191,0.10)),
                rgba(255,255,255,0.04);
            border: 1px solid rgba(94,234,212,0.12);
            text-align: center;
        }

        .cta-box h2 {
            margin: 0 0 12px;
            font-size: 36px;
            line-height: 1.05;
            letter-spacing: -0.04em;
            font-weight: 800;
        }

        .cta-box p {
            margin: 0 auto 20px;
            max-width: 760px;
            color: var(--muted);
            line-height: 1.75;
            font-size: 15px;
            font-weight: 500;
        }

        .faq {
            display: grid;
            gap: 16px;
        }

        .contact-wrap {
            display: grid;
            grid-template-columns: 1fr;
            max-width: 720px;
            margin: 0 auto;
        }

        .form-box {
            border-radius: 28px;
            padding: 30px;
        }

        .form-box h3 {
            margin-top: 0;
            font-size: 28px;
            text-align: center;
            margin-bottom: 22px;
            position: relative;
            z-index: 2;
            letter-spacing: -0.04em;
            font-weight: 800;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #e5e7eb;
            font-weight: 700;
            font-size: 14px;
            position: relative;
            z-index: 2;
        }

        input,
        textarea,
        select {
            width: 100%;
            padding: 15px 16px;
            margin-bottom: 16px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.10);
            background: rgba(255,255,255,0.06);
            color: #fff;
            font-size: 15px;
            font-family: "Inter", sans-serif;
            font-weight: 500;
            outline: none;
            transition: 0.2s ease;
            position: relative;
            z-index: 2;
        }

        select option {
            background: #0f172a;
            color: #fff;
        }

        input::placeholder,
        textarea::placeholder {
            color: #94a3b8;
        }

        textarea {
            min-height: 120px;
            resize: vertical;
        }

        input:focus,
        select:focus,
        textarea:focus {
            border-color: var(--accent);
            box-shadow:
                0 0 0 4px rgba(20,184,166,0.10),
                0 0 20px rgba(94,234,212,0.08);
        }

        form .btn {
            position: relative;
            z-index: 2;
            width: 100%;
        }

        .alert {
            padding: 14px 16px;
            border-radius: 14px;
            margin-bottom: 18px;
            font-weight: 700;
            position: relative;
            z-index: 2;
            font-size: 14px;
        }

        .success {
            background: rgba(34,197,94,0.16);
            color: #86efac;
            border: 1px solid rgba(34,197,94,0.32);
        }

        .error {
            background: rgba(239,68,68,0.16);
            color: #fca5a5;
            border: 1px solid rgba(239,68,68,0.30);
        }

        .hidden-field {
            position: absolute;
            left: -9999px;
            opacity: 0;
            pointer-events: none;
        }

        .footer {
            padding: 34px 0 42px;
            text-align: center;
            color: var(--muted-2);
            font-size: 14px;
            font-weight: 500;
        }

        .reveal {
            opacity: 0;
            transform: translateY(26px) scale(0.985);
            transition:
                opacity 0.8s ease,
                transform 0.8s ease;
        }

        .reveal.show {
            opacity: 1;
            transform: translateY(0) scale(1);
        }

        .whatsapp-btn {
            position: fixed;
            right: 24px;
            bottom: 24px;
            width: 62px;
            height: 62px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #25D366;
            color: white;
            box-shadow:
                0 10px 25px rgba(0,0,0,0.3),
                0 0 20px rgba(37,211,102,0.4);
            z-index: 999;
            transition: 0.3s ease;
        }

        .whatsapp-btn svg {
            width: 28px;
            height: 28px;
            fill: currentColor;
        }

        .whatsapp-btn:hover {
            transform: scale(1.1);
            box-shadow:
                0 15px 35px rgba(0,0,0,0.4),
                0 0 30px rgba(37,211,102,0.6);
        }

        @media (max-width: 1180px) {
            .hero-grid,
            .dashboard-grid,
            .search-wrap,
            .grid-4,
            .report-grid,
            .report-benefits-grid,
            .report-highlight,
            .system-panels {
                grid-template-columns: 1fr;
            }

            .system-body {
                grid-template-columns: 1fr;
            }

            .system-sidebar {
                border-right: none;
                border-bottom: 1px solid rgba(255,255,255,0.08);
            }

            .hero h1 {
                font-size: 42px;
            }

            .hero-points,
            .mini-stats,
            .hero-metric {
                grid-template-columns: 1fr;
            }

            .bar-row,
            .hero-bar-row {
                grid-template-columns: 1fr;
            }

            .hero-preview {
                min-height: auto;
            }

            .float-card {
                display: none;
            }
        }

        @media (max-width: 760px) {
            .nav-links {
                display: none;
            }

            .hero-box {
                padding: 30px;
            }

            .hero h1 {
                font-size: 32px;
            }

            .section-title h2,
            .cta-box h2 {
                font-size: 28px;
            }

            .animated-score {
                font-size: 42px;
            }
        }
    </style>
</head>
<body>
    <canvas id="network-bg"></canvas>
    <div class="grid-noise"></div>
    <div class="bg-orb bg-orb-1" id="orb1"></div>
    <div class="bg-orb bg-orb-2" id="orb2"></div>
    <div class="bg-orb bg-orb-3" id="orb3"></div>
    <div class="cursor-glow" id="cursorGlow"></div>

    <div class="navbar">
        <div class="container nav-inner">
            <div class="logo glow-text">
                <span class="logo-mark">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <path d="M12 2l2.6 5.8L21 10l-4.7 4.3 1.2 6.2L12 17.7 6.5 20.5l1.2-6.2L3 10l6.4-2.2L12 2z"></path>
                    </svg>
                </span>
                Aqyl<span>Flow</span>
            </div>

            <div class="nav-links">
                <a href="#features">Функции</a>
                <a href="#dashboard">Dashboard</a>
                <a href="#search-ai">AI поиск</a>
                <a href="#system-ui">Интерфейс</a>
                <a href="#reporting">Отчётность</a>
                <a href="#contact" class="btn btn-primary magnetic-btn">Оставить заявку</a>
            </div>
        </div>
    </div>

    <section class="hero">
        <div class="container">
            <div class="hero-box glass gradient-border reveal">
                <div class="hero-grid">
                    <div>
                        <div class="badge">Binotel API • AI dashboard • каз / рус • отчётность для руководителя</div>
                        <h1 class="glow-text">AI-платформа для контроля качества звонков и управленческой отчётности</h1>
                        <p>
                            AqylFlow показывает не просто анализ звонков, а готовую управленческую аналитику:
                            ошибки команды за период, рейтинг операторов, группы просрочки, длительность разговоров,
                            воронку диалога и средние оценки по сотруднику, группе и всей команде.
                        </p>

                        <div class="hero-actions">
                            <a href="#reporting" class="btn btn-primary magnetic-btn">Посмотреть отчётность</a>
                            <a href="#search-ai" class="btn btn-secondary magnetic-btn">Открыть AI поиск</a>
                        </div>

                        <div class="hero-points">
                            <div class="mini-pill">✔ основные ошибки команды за период</div>
                            <div class="mini-pill">✔ рейтинг операторов от лучших до нарушителей</div>
                            <div class="mini-pill">✔ аналитика по группам просрочки</div>
                            <div class="mini-pill">✔ воронка разговора и средние оценки</div>
                        </div>
                    </div>

                    <div class="hero-preview">
                        <div class="float-card float-card-1">
                            <small>Главная ошибка</small>
                            <strong>42%</strong>
                        </div>
                        <div class="float-card float-card-2">
                            <small>Проанализировано</small>
                            <strong>4 250 звонков</strong>
                        </div>
                        <div class="float-card float-card-3">
                            <small>Top score</small>
                            <strong>92 / 100</strong>
                        </div>

                        <div class="hero-dashboard glass gradient-border">
                            <div class="hero-dashboard-top">
                                <div class="hero-dashboard-title">Live AI Preview</div>
                                <div class="hero-dashboard-badge">Demo system</div>
                            </div>

                            <div class="hero-dashboard-grid">
                                <div class="hero-metric">
                                    <div class="hero-metric-box">
                                        <div class="hero-metric-label">Качество</div>
                                        <div class="hero-metric-value">84</div>
                                    </div>
                                    <div class="hero-metric-box">
                                        <div class="hero-metric-label">Жалобы</div>
                                        <div class="hero-metric-value">124</div>
                                    </div>
                                    <div class="hero-metric-box">
                                        <div class="hero-metric-label">PTP</div>
                                        <div class="hero-metric-value">1 087</div>
                                    </div>
                                </div>

                                <div class="typing-wrap">
                                    <span id="typingText"></span><span class="typing-cursor">|</span>
                                </div>

                                <div class="hero-bars">
                                    <div class="hero-bar-row">
                                        <div class="hero-bar-label">Не представился</div>
                                        <div class="hero-bar-track"><div class="hero-bar-fill" style="width:42%"></div></div>
                                        <div class="hero-bar-value">42%</div>
                                    </div>
                                    <div class="hero-bar-row">
                                        <div class="hero-bar-label">Не уточняет причину</div>
                                        <div class="hero-bar-track"><div class="hero-bar-fill" style="width:31%"></div></div>
                                        <div class="hero-bar-value">31%</div>
                                    </div>
                                    <div class="hero-bar-row">
                                        <div class="hero-bar-label">Перебивает клиента</div>
                                        <div class="hero-bar-track"><div class="hero-bar-fill" style="width:18%"></div></div>
                                        <div class="hero-bar-value">18%</div>
                                    </div>
                                </div>

                                <div class="error-row">
                                    <span>Где теряется клиент</span>
                                    <span>Этап предложения решения</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="features">
        <div class="container">
            <div class="section-title center reveal">
                <h2>Функции платформы</h2>
                <p>Glassmorphism интерфейс, AI dashboard, живой поиск звонков и управленческая аналитика.</p>
            </div>

            <div class="grid-4 stagger-parent">
                <div class="feature glass gradient-border reveal tilt-card">
                    <h3>Мультиязычное распознавание</h3>
                    <p>Распознавание речи на русском и казахском языках, включая смешанные разговоры.</p>
                </div>
                <div class="feature glass gradient-border reveal tilt-card">
                    <h3>AI-резюме разговора</h3>
                    <p>Краткая суть звонка, результат разговора и ключевые детали без ручной прослушки.</p>
                </div>
                <div class="feature glass gradient-border reveal tilt-card">
                    <h3>AI-поиск звонков</h3>
                    <p>Поиск разговоров по смыслу: жалобы, обещание оплаты, грубость, конфликт и штрафы.</p>
                </div>
                <div class="feature glass gradient-border reveal tilt-card">
                    <h3>Управленческая отчётность</h3>
                    <p>Отчёты по сотрудникам, группам просрочки, нарушениям и воронке разговора.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="dashboard">
        <div class="container">
            <div class="section-title center reveal">
                <h2>AI Dashboard с графиками</h2>
                <p>Живые метрики, тренды качества, рейтинг операторов и проблемные точки команды.</p>
            </div>

            <div class="dashboard-shell glass gradient-border reveal tilt-card">
                <div class="dashboard-top">
                    <div class="dashboard-title">AI Quality Dashboard</div>
                    <div class="dashboard-badge">Live demo analytics</div>
                </div>

                <div class="dashboard-grid">
                    <div class="dashboard-left">
                        <div class="dashboard-card">
                            <h3>Оценка качества</h3>
                            <div class="animated-score-wrap">
                                <div class="animated-score" data-target="100" data-start="82">82</div>
                                <div class="score-status">Тренд: +8.4%</div>
                            </div>

                            <div class="mini-stats">
                                <div class="mini-stat">
                                    <div class="mini-stat-label">Проанализировано</div>
                                    <div class="mini-stat-value" data-count="4250">0</div>
                                </div>
                                <div class="mini-stat">
                                    <div class="mini-stat-label">Жалобы</div>
                                    <div class="mini-stat-value" data-count="124">0</div>
                                </div>
                                <div class="mini-stat">
                                    <div class="mini-stat-label">Обещания оплаты</div>
                                    <div class="mini-stat-value" data-count="1087">0</div>
                                </div>
                            </div>
                        </div>

                        <div class="dashboard-card">
                            <h3>Ошибки команды</h3>
                            <div class="bars">
                                <div class="bar-row">
                                    <div class="bar-label">Не представился</div>
                                    <div class="bar-track"><div class="bar-fill" data-width="42"></div></div>
                                    <div class="bar-value">42%</div>
                                </div>
                                <div class="bar-row">
                                    <div class="bar-label">Не уточняет причину</div>
                                    <div class="bar-track"><div class="bar-fill" data-width="31"></div></div>
                                    <div class="bar-value">31%</div>
                                </div>
                                <div class="bar-row">
                                    <div class="bar-label">Перебивает клиента</div>
                                    <div class="bar-track"><div class="bar-fill" data-width="18"></div></div>
                                    <div class="bar-value">18%</div>
                                </div>
                                <div class="bar-row">
                                    <div class="bar-label">Не предлагает решение</div>
                                    <div class="bar-track"><div class="bar-fill" data-width="14"></div></div>
                                    <div class="bar-value">14%</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="dashboard-right">
                        <div class="dashboard-card">
                            <h3>Динамика качества</h3>
                            <div class="line-chart">
                                <svg class="chart-svg" viewBox="0 0 600 240" preserveAspectRatio="none">
                                    <polyline fill="none" stroke="rgba(94,234,212,0.18)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" points="40,165 150,150 260,120 370,105 480,85 560,70"></polyline>
                                    <polyline id="quality-line" fill="none" stroke="#5eead4" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" points="40,165 150,150 260,120 370,105 480,85 560,70" stroke-dasharray="1000" stroke-dashoffset="1000"></polyline>
                                    <circle cx="40" cy="165" r="5" fill="#5eead4"></circle>
                                    <circle cx="150" cy="150" r="5" fill="#5eead4"></circle>
                                    <circle cx="260" cy="120" r="5" fill="#5eead4"></circle>
                                    <circle cx="370" cy="105" r="5" fill="#5eead4"></circle>
                                    <circle cx="480" cy="85" r="5" fill="#5eead4"></circle>
                                    <circle cx="560" cy="70" r="5" fill="#5eead4"></circle>
                                </svg>
                            </div>

                            <div class="legend">
                                <div class="legend-item">
                                    <span class="legend-dot" style="background:#5eead4;"></span>
                                    Средняя оценка команды
                                </div>
                            </div>
                        </div>

                        <div class="dashboard-card">
                            <h3>Рейтинг операторов</h3>
                            <div class="metric-row">
                                <span>Иванов</span>
                                <span>92</span>
                            </div>
                            <div class="metric-row">
                                <span>Серикова</span>
                                <span>88</span>
                            </div>
                            <div class="metric-row">
                                <span>Абдуллин</span>
                                <span>84</span>
                            </div>
                            <div class="metric-row">
                                <span>Петрова</span>
                                <span>79</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="search-ai">
        <div class="container">
            <div class="section-title center reveal">
                <h2>Живой поиск звонков</h2>
                <p>Покажи нужные звонки обычным языком, как в ChatGPT.</p>
            </div>

            <div class="search-wrap">
                <div class="chat-search-card glass gradient-border reveal tilt-card">
                    <h3>AI-поиск по смыслу</h3>
                    <p>Введи запрос, и система покажет релевантные звонки, причины и ключевые фразы.</p>

                    <div class="search-input-wrap">
                        <input
                            id="liveSearchInput"
                            class="search-input"
                            type="text"
                            placeholder="Например: покажи звонки, где клиент жалуется на штрафы"
                        >
                        <button class="btn btn-primary magnetic-btn" type="button" id="searchBtn">Найти</button>
                    </div>

                    <div class="search-results" id="searchResults">
                        <div class="search-result">
                            <strong>Звонок #1832</strong>
                            Клиент недоволен начислением штрафа. Оператор не дал полного объяснения и перебивал клиента.
                            <div class="tag-row">
                                <span class="mini-tag">жалоба</span>
                                <span class="mini-tag">штрафы</span>
                                <span class="mini-tag">конфликт</span>
                            </div>
                        </div>

                        <div class="search-result">
                            <strong>Звонок #1933</strong>
                            Клиент жалуется на грубый тон общения. Зафиксировано отклонение от скрипта.
                            <div class="tag-row">
                                <span class="mini-tag">грубость</span>
                                <span class="mini-tag">нарушение</span>
                            </div>
                        </div>

                        <div class="search-result">
                            <strong>Звонок #2024</strong>
                            Клиент сообщил о финансовых трудностях и пообещал оплатить в течение 3 дней.
                            <div class="tag-row">
                                <span class="mini-tag">PTP</span>
                                <span class="mini-tag">обещание оплаты</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="search-side-panel glass gradient-border reveal tilt-card">
                    <h3>AI анализ поиска</h3>
                    <p>Система не ищет только по словам. Она понимает смысл запроса и находит релевантные разговоры.</p>

                    <div class="typing-log">
                        <div class="typing-row"><span class="status-dot"></span><span id="log1">AI анализирует смысл запроса...</span></div>
                        <div class="typing-row"><span class="status-dot"></span><span id="log2">Проверка жалоб, штрафов и конфликтов...</span></div>
                        <div class="typing-row"><span class="status-dot"></span><span id="log3">Формирование релевантной выборки звонков...</span></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="system-ui">
        <div class="container">
            <div class="section-title center reveal">
                <h2>Интерфейс системы</h2>
                <p>Пример рабочего кабинета с glassmorphism панелями и живой аналитикой.</p>
            </div>

            <div class="system-ui glass gradient-border reveal tilt-card">
                <div class="system-topbar">
                    <div class="system-brand">AqylFlow Console</div>
                    <div class="system-actions">
                        <span class="system-dot"></span>
                        <span class="system-dot"></span>
                        <span class="system-dot"></span>
                    </div>
                </div>

                <div class="system-body">
                    <div class="system-sidebar">
                        <div class="dashboard-badge">AI Workspace</div>
                        <div class="system-menu">
                            <div class="system-menu-item active">Dashboard</div>
                            <div class="system-menu-item">Звонки</div>
                            <div class="system-menu-item">Поиск по смыслу</div>
                            <div class="system-menu-item">Операторы</div>
                            <div class="system-menu-item">Отчётность</div>
                            <div class="system-menu-item">Отчёты</div>
                        </div>
                    </div>

                    <div class="system-content">
                        <div class="system-panels">
                            <div class="system-panel">
                                <h3>Последние разговоры</h3>
                                <table class="system-table">
                                    <thead>
                                        <tr>
                                            <th>Звонок</th>
                                            <th>Оператор</th>
                                            <th>Оценка</th>
                                            <th>Статус</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>#2451</td>
                                            <td>Иванов</td>
                                            <td>82</td>
                                            <td><span class="tag tag-green">Обещание оплаты</span></td>
                                        </tr>
                                        <tr>
                                            <td>#2452</td>
                                            <td>Серикова</td>
                                            <td>91</td>
                                            <td><span class="tag tag-blue">Без нарушений</span></td>
                                        </tr>
                                        <tr>
                                            <td>#2453</td>
                                            <td>Абдуллин</td>
                                            <td>74</td>
                                            <td><span class="tag tag-orange">Нарушение скрипта</span></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            <div class="system-panel">
                                <h3>AI-резюме звонка</h3>
                                <p>
                                    Клиент объяснил просрочку временными финансовыми трудностями.
                                    Оператор довёл разговор до обещания оплаты через 3 дня, но не представился
                                    и не полностью уточнил причину просрочки.
                                </p>

                                <div class="metric-row" style="margin-top:14px;">
                                    <span>Нарушений</span>
                                    <span>3</span>
                                </div>
                                <div class="metric-row">
                                    <span>Тон клиента</span>
                                    <span>Нейтральный</span>
                                </div>
                                <div class="metric-row">
                                    <span>Следующий шаг</span>
                                    <span>Контроль оплаты</span>
                                </div>
                            </div>
                        </div>

                        <div class="system-panels">
                            <div class="system-panel">
                                <h3>Топ проблем команды</h3>
                                <div class="error-row">
                                    <span>Не представился</span>
                                    <span>42%</span>
                                </div>
                                <div class="error-row">
                                    <span>Не уточняет причину</span>
                                    <span>31%</span>
                                </div>
                                <div class="error-row">
                                    <span>Перебивает клиента</span>
                                    <span>18%</span>
                                </div>
                            </div>

                            <div class="system-panel">
                                <h3>Быстрый AI-поиск</h3>
                                <div class="search-result">
                                    <strong>Запрос:</strong>
                                    “Покажи звонки, где клиент жалуется на штрафы”
                                </div>
                                <div class="search-result">
                                    <strong>Найдено:</strong>
                                    18 разговоров, 7 повторных обращений, 4 конфликта
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="reporting">
        <div class="container">
            <div class="section-title center reveal">
                <h2>Отчётность для руководителя</h2>
                <p>Не просто анализ звонков, а готовая управленческая аналитика по сотрудникам, группам и процессу.</p>
            </div>

            <div class="report-hero glass gradient-border reveal tilt-card">
                <div class="report-hero-content">
                    <h3>AI-отчётность для руководителя</h3>
                    <p>
                        Система автоматически формирует отчёты по звонкам, операторам и группам просрочки.
                        Руководитель сразу видит, кто нарушает скрипт, какие группы работают слабее,
                        где разговоры слишком длинные или короткие, и на каком этапе оператор теряет клиента.
                    </p>

                    <div class="report-highlight">
                        <div class="report-pill">Основные ошибки команды за период</div>
                        <div class="report-pill">Рейтинг операторов: от лучших до нарушителей</div>
                        <div class="report-pill">Аналитика по группам просрочки</div>
                    </div>
                </div>
            </div>

            <div class="report-grid stagger-parent">
                <div class="report-card glass gradient-border reveal tilt-card">
                    <h3>Команда и сотрудники</h3>
                    <div class="report-list">
                        <div class="report-row"><span>Основные ошибки команды</span><strong>За день / неделю / месяц</strong></div>
                        <div class="report-row"><span>Рейтинг операторов</span><strong>Лучшие → нарушители</strong></div>
                        <div class="report-row"><span>Средняя оценка сотрудника</span><strong>По каждому оператору</strong></div>
                        <div class="report-row"><span>Средняя оценка команды</span><strong>Общий уровень качества</strong></div>
                    </div>
                </div>

                <div class="report-card glass gradient-border reveal tilt-card">
                    <h3>Группы просрочки и длительность</h3>
                    <div class="report-list">
                        <div class="report-row"><span>Группы просрочки</span><strong>-4 → 120 дней</strong></div>
                        <div class="report-row"><span>Средняя длительность</span><strong>По группе и человеку</strong></div>
                        <div class="report-row"><span>Самые длинные разговоры</span><strong>Точки перегруза</strong></div>
                        <div class="report-row"><span>Самые короткие разговоры</span><strong>Риск “слива” клиента</strong></div>
                    </div>
                </div>

                <div class="report-card glass gradient-border reveal tilt-card">
                    <h3>Воронка и контроль процесса</h3>
                    <div class="report-list">
                        <div class="report-row"><span>Воронка разговора</span><strong>Где теряется клиент</strong></div>
                        <div class="report-row"><span>Скрипт и нарушения</span><strong>Где ломается процесс</strong></div>
                        <div class="report-row"><span>Средняя оценка группы</span><strong>Сравнение команд</strong></div>
                        <div class="report-row"><span>Управленческие инсайты</span><strong>Без ручной прослушки</strong></div>
                    </div>
                </div>
            </div>

            <div class="section-title center reveal" style="margin-top:28px;">
                <h2>Что это даёт</h2>
                <p>Понятная ценность для руководителя и ОКК.</p>
            </div>

            <div class="report-benefits-grid stagger-parent">
                <div class="report-benefit glass gradient-border reveal tilt-card">
                    <h3>Быстрый контроль качества</h3>
                    <p>Видно реальную картину по звонкам без долгой ручной прослушки.</p>
                </div>
                <div class="report-benefit glass gradient-border reveal tilt-card">
                    <h3>Выявление слабых операторов</h3>
                    <p>Сразу видно, кто чаще нарушает скрипт и где нужен контроль.</p>
                </div>
                <div class="report-benefit glass gradient-border reveal tilt-card">
                    <h3>Понимание, где ломается скрипт</h3>
                    <p>Система показывает, на каком этапе процесса теряется клиент.</p>
                </div>
                <div class="report-benefit glass gradient-border reveal tilt-card">
                    <h3>Прозрачная система оценки</h3>
                    <p>Единые показатели по сотруднику, группе и всей команде.</p>
                </div>
                <div class="report-benefit glass gradient-border reveal tilt-card">
                    <h3>Управленческая аналитика</h3>
                    <p>Руководитель получает отчёты, по которым можно принимать решения сразу.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="start">
        <div class="container">
            <div class="cta-box glass gradient-border reveal tilt-card">
                <h2>Покажем демо под ваш процесс</h2>
                <p>
                    Покажем, как будет выглядеть отчётность именно для вашей команды:
                    от ошибок операторов и групп просрочки до воронки разговора и рейтинга сотрудников.
                </p>
                <div class="hero-actions" style="justify-content:center;">
                    <a href="#contact" class="btn btn-primary magnetic-btn">Оставить заявку</a>
                    <a href="#dashboard" class="btn btn-secondary magnetic-btn">Посмотреть dashboard</a>
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="faq">
        <div class="container">
            <div class="section-title center reveal">
                <h2>FAQ</h2>
                <p>Ответы на частые вопросы.</p>
            </div>

            <div class="faq stagger-parent">
                <div class="faq-item glass gradient-border reveal tilt-card">
                    <h3>Можно ли видеть отчёты по группам просрочки?</h3>
                    <p>Да. Можно анализировать группы по дням просрочки и сравнивать длительность, нарушения и средние оценки.</p>
                </div>
                <div class="faq-item glass gradient-border reveal tilt-card">
                    <h3>Можно ли выявлять нарушителей и лучших сотрудников?</h3>
                    <p>Да. Платформа показывает рейтинг операторов от лучших до нарушителей по вашим критериям оценки.</p>
                </div>
                <div class="faq-item glass gradient-border reveal tilt-card">
                    <h3>Можно ли видеть, где оператор теряет клиента?</h3>
                    <p>Да. Для этого используется воронка разговора, которая показывает проблемный этап в диалоге.</p>
                </div>
                <div class="faq-item glass gradient-border reveal tilt-card">
                    <h3>Есть ли средняя оценка по сотруднику, группе и команде?</h3>
                    <p>Да. Система считает показатели на всех уровнях и показывает общую картину качества.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="contact">
        <div class="container">
            <div class="section-title center reveal">
                <h2>Оставить заявку</h2>
                <p>
                    Оставьте заявку, и мы свяжемся с вами, покажем демо платформы
                    и обсудим внедрение под ваш процесс.
                </p>
            </div>

            <div class="contact-wrap">
                <div class="form-box glass gradient-border reveal tilt-card">
                    <h3>Форма заявки</h3>

                    {% if message %}
                        {{ message|safe }}
                    {% endif %}

                    <form method="POST">
                        <div class="hidden-field">
                            <input type="text" name="website" placeholder="Ваш сайт" autocomplete="off">
                        </div>

                        <label>Ваше имя</label>
                        <input type="text" name="name" placeholder="Например: Тахир" required>

                        <label>Ваш телефон</label>
                        <input id="phone" type="text" name="phone" placeholder="+7 (___) ___-__-__" required>

                        <label>Выберите услугу</label>
                        <select name="service" required>
                            <option value="">Выберите услугу</option>
                            <option>AI-контроль качества звонков</option>
                            <option>Демо платформы</option>
                            <option>Индивидуальное внедрение</option>
                        </select>

                        <label>Комментарий</label>
                        <textarea name="comment" placeholder="Коротко опишите задачу"></textarea>

                        <button type="submit" class="btn btn-primary magnetic-btn">Отправить заявку</button>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <div class="footer">
        © 2026 AqylFlow. Все права защищены.
    </div>

    <a href="https://wa.me/87078340913" class="whatsapp-btn" target="_blank" aria-label="WhatsApp">
        <svg viewBox="0 0 32 32" aria-hidden="true">
            <path d="M19.11 17.33c-.28-.14-1.66-.82-1.91-.91-.26-.1-.45-.14-.63.14-.19.28-.73.91-.9 1.1-.16.19-.33.21-.61.07-.28-.14-1.2-.44-2.28-1.41-.84-.75-1.4-1.68-1.57-1.96-.16-.28-.02-.43.12-.57.13-.13.28-.33.42-.49.14-.16.19-.28.28-.47.09-.19.05-.35-.02-.49-.07-.14-.63-1.52-.87-2.09-.23-.55-.46-.47-.63-.48h-.54c-.19 0-.49.07-.75.35-.26.28-.98.96-.98 2.35 0 1.38 1.01 2.72 1.15 2.91.14.19 1.98 3.02 4.8 4.24.67.29 1.2.46 1.61.59.68.22 1.29.19 1.78.11.54-.08 1.66-.68 1.9-1.34.23-.66.23-1.22.16-1.34-.07-.12-.26-.19-.54-.33zM16.03 4.8c-6.18 0-11.18 4.99-11.18 11.15 0 1.97.52 3.89 1.5 5.57L4.77 27.2l5.84-1.53a11.17 11.17 0 0 0 5.42 1.39h.01c6.17 0 11.18-4.99 11.18-11.15 0-2.98-1.17-5.79-3.28-7.9A11.12 11.12 0 0 0 16.03 4.8zm0 20.38h-.01a9.22 9.22 0 0 1-4.7-1.29l-.34-.2-3.47.91.93-3.38-.22-.35a9.17 9.17 0 0 1-1.42-4.9c0-5.08 4.15-9.22 9.25-9.22 2.47 0 4.78.96 6.53 2.7a9.16 9.16 0 0 1 2.71 6.52c0 5.08-4.15 9.21-9.26 9.21z"/>
        </svg>
    </a>

    <script>
        const canvas = document.getElementById("network-bg");
        const ctx = canvas.getContext("2d");

        let w = canvas.width = window.innerWidth;
        let h = canvas.height = window.innerHeight;

        const mouse = { x: w / 2, y: h / 2, radius: 150 };
        const particles = [];
        const count = 90;

        function createParticles() {
            particles.length = 0;
            for (let i = 0; i < count; i++) {
                particles.push({
                    x: Math.random() * w,
                    y: Math.random() * h,
                    vx: (Math.random() - 0.5) * 0.55,
                    vy: (Math.random() - 0.5) * 0.55,
                    baseSize: Math.random() * 1.8 + 1.4
                });
            }
        }

        createParticles();

        window.addEventListener("resize", () => {
            w = canvas.width = window.innerWidth;
            h = canvas.height = window.innerHeight;
            createParticles();
        });

        window.addEventListener("mousemove", (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;

            const orb1 = document.getElementById("orb1");
            const orb2 = document.getElementById("orb2");
            const orb3 = document.getElementById("orb3");
            const cursorGlow = document.getElementById("cursorGlow");

            if (orb1 && orb2 && orb3) {
                orb1.style.transform = `translate(${e.clientX * 0.018}px, ${e.clientY * 0.014}px)`;
                orb2.style.transform = `translate(${-e.clientX * 0.014}px, ${-e.clientY * 0.01}px)`;
                orb3.style.transform = `translate(${e.clientX * 0.008}px, ${-e.clientY * 0.008}px)`;
            }

            if (cursorGlow) {
                cursorGlow.style.left = `${e.clientX}px`;
                cursorGlow.style.top = `${e.clientY}px`;
            }
        });

        function draw() {
            ctx.clearRect(0, 0, w, h);

            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];
                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > w) p.vx *= -1;
                if (p.y < 0 || p.y > h) p.vy *= -1;

                const dxm = p.x - mouse.x;
                const dym = p.y - mouse.y;
                const distMouse = Math.sqrt(dxm * dxm + dym * dym);

                let size = p.baseSize;
                let alpha = 0.70;

                if (distMouse < mouse.radius) {
                    size = p.baseSize + 1.9;
                    alpha = 1;
                }

                ctx.beginPath();
                ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(94,234,212,${alpha})`;
                ctx.shadowBlur = distMouse < mouse.radius ? 18 : 8;
                ctx.shadowColor = "rgba(94,234,212,0.7)";
                ctx.fill();

                for (let j = i + 1; j < particles.length; j++) {
                    const p2 = particles[j];
                    const dx = p.x - p2.x;
                    const dy = p.y - p2.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 125) {
                        let opacity = 0.13 - dist / 980;
                        const midX = (p.x + p2.x) / 2;
                        const midY = (p.y + p2.y) / 2;
                        const mdx = midX - mouse.x;
                        const mdy = midY - mouse.y;
                        const mdist = Math.sqrt(mdx * mdx + mdy * mdy);

                        if (mdist < mouse.radius + 30) opacity += 0.10;

                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.strokeStyle = `rgba(94,234,212,${opacity})`;
                        ctx.lineWidth = mdist < mouse.radius + 30 ? 1.1 : 0.8;
                        ctx.shadowBlur = mdist < mouse.radius + 30 ? 10 : 0;
                        ctx.shadowColor = "rgba(94,234,212,0.30)";
                        ctx.stroke();
                    }
                }
            }

            ctx.shadowBlur = 0;
            requestAnimationFrame(draw);
        }

        draw();

        const revealItems = document.querySelectorAll(".reveal");
        revealItems.forEach((el) => {
            const parent = el.closest(".stagger-parent");
            if (parent) {
                const siblings = Array.from(parent.querySelectorAll(".reveal"));
                const pos = siblings.indexOf(el);
                el.style.transitionDelay = `${pos * 90}ms`;
            }
        });

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) entry.target.classList.add("show");
            });
        }, { threshold: 0.12 });

        revealItems.forEach(el => observer.observe(el));

        const phoneInput = document.getElementById("phone");
        if (phoneInput) {
            phoneInput.addEventListener("input", function() {
                let x = phoneInput.value.replace(/\D/g, "");
                if (x.startsWith("8")) x = "7" + x.substring(1);
                if (!x.startsWith("7")) x = "7" + x;
                x = x.substring(0, 11);

                let formatted = "+7";
                if (x.length > 1) formatted += " (" + x.substring(1, 4);
                if (x.length >= 4) formatted += ") " + x.substring(4, 7);
                if (x.length >= 7) formatted += "-" + x.substring(7, 9);
                if (x.length >= 9) formatted += "-" + x.substring(9, 11);

                phoneInput.value = formatted;
            });
        }

        function animateNumber(el, start, end, duration = 1800, locale = true) {
            const startTime = performance.now();

            function update(currentTime) {
                const progress = Math.min((currentTime - startTime) / duration, 1);
                const ease = 1 - Math.pow(1 - progress, 3);
                const value = Math.round(start + (end - start) * ease);
                el.textContent = locale ? value.toLocaleString("ru-RU") : value;
                if (progress < 1) requestAnimationFrame(update);
            }

            requestAnimationFrame(update);
        }

        const scoreObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.animated) {
                    entry.target.dataset.animated = "true";
                    animateNumber(
                        entry.target,
                        parseInt(entry.target.dataset.start || "0", 10),
                        parseInt(entry.target.dataset.target || entry.target.textContent, 10),
                        1800,
                        false
                    );
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll(".animated-score").forEach(el => scoreObserver.observe(el));

        const countObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const el = entry.target;
                if (entry.isIntersecting && !el.dataset.done) {
                    el.dataset.done = "true";
                    animateNumber(el, 0, parseInt(el.dataset.count, 10), 1600, true);
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll("[data-count]").forEach(el => countObserver.observe(el));

        const barObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.filled) {
                    entry.target.dataset.filled = "true";
                    entry.target.style.width = (entry.target.dataset.width || "0") + "%";
                }
            });
        }, { threshold: 0.4 });

        document.querySelectorAll(".bar-fill").forEach(el => barObserver.observe(el));

        const qualityLine = document.getElementById("quality-line");
        const lineObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && qualityLine && !qualityLine.dataset.animated) {
                    qualityLine.dataset.animated = "true";
                    qualityLine.style.transition = "stroke-dashoffset 2s ease";
                    qualityLine.style.strokeDashoffset = "0";
                }
            });
        }, { threshold: 0.4 });

        if (qualityLine) lineObserver.observe(qualityLine);

        const tiltCards = document.querySelectorAll(".tilt-card");
        const isTouch = window.matchMedia("(pointer: coarse)").matches;

        if (!isTouch) {
            tiltCards.forEach(card => {
                card.addEventListener("mousemove", (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;

                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;

                    const rotateX = ((y - centerY) / centerY) * -4;
                    const rotateY = ((x - centerX) / centerX) * 4;

                    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
                    card.style.setProperty("--mx", `${x}px`);
                    card.style.setProperty("--my", `${y}px`);
                });

                card.addEventListener("mouseleave", () => {
                    card.style.transform = "";
                });
            });
        }

        const magneticButtons = document.querySelectorAll(".magnetic-btn");
        if (!isTouch) {
            magneticButtons.forEach(btn => {
                btn.addEventListener("mousemove", (e) => {
                    const rect = btn.getBoundingClientRect();
                    const relX = e.clientX - rect.left - rect.width / 2;
                    const relY = e.clientY - rect.top - rect.height / 2;
                    btn.style.transform = `translate(${relX * 0.16}px, ${relY * 0.16}px)`;
                });

                btn.addEventListener("mouseleave", () => {
                    btn.style.transform = "";
                });
            });
        }

        const typingLines = [
            "AI анализирует звонки и формирует отчётность для руководителя.",
            "AI выявляет нарушения, слабые места команды и проблемные этапы диалога.",
            "AI находит звонки по смыслу и показывает, где оператор теряет клиента."
        ];

        const typingTextEl = document.getElementById("typingText");
        let lineIndex = 0;
        let charIndex = 0;
        let deleting = false;

        function typeLoop() {
            if (!typingTextEl) return;
            const current = typingLines[lineIndex];

            if (!deleting) {
                typingTextEl.textContent = current.slice(0, charIndex + 1);
                charIndex++;
                if (charIndex === current.length) {
                    deleting = true;
                    setTimeout(typeLoop, 1500);
                    return;
                }
            } else {
                typingTextEl.textContent = current.slice(0, charIndex - 1);
                charIndex--;
                if (charIndex === 0) {
                    deleting = false;
                    lineIndex = (lineIndex + 1) % typingLines.length;
                }
            }

            setTimeout(typeLoop, deleting ? 28 : 42);
        }

        typeLoop();

        const searchInput = document.getElementById("liveSearchInput");
        const searchBtn = document.getElementById("searchBtn");
        const searchResults = document.getElementById("searchResults");

        const searchData = [
            {
                id: "#1832",
                text: "Клиент недоволен начислением штрафа. Оператор не дал полного объяснения и перебивал клиента.",
                tags: ["жалоба", "штрафы", "конфликт"]
            },
            {
                id: "#1933",
                text: "Клиент жалуется на грубый тон общения. Зафиксировано отклонение от скрипта.",
                tags: ["грубость", "нарушение"]
            },
            {
                id: "#2024",
                text: "Клиент сообщил о финансовых трудностях и пообещал оплатить в течение 3 дней.",
                tags: ["PTP", "обещание оплаты"]
            },
            {
                id: "#2140",
                text: "Клиент просит объяснить начисленные комиссии и жалуется на непонятные условия.",
                tags: ["жалоба", "комиссия", "штрафы"]
            },
            {
                id: "#2255",
                text: "Оператор довёл разговор до обещания оплаты, но пропустил обязательное приветствие.",
                tags: ["PTP", "приветствие", "нарушение"]
            }
        ];

        function renderResults(query) {
            const q = query.trim().toLowerCase();
            let items = searchData;

            if (q) {
                items = searchData.filter(item =>
                    item.text.toLowerCase().includes(q) ||
                    item.tags.join(" ").toLowerCase().includes(q) ||
                    item.id.toLowerCase().includes(q)
                );
            }

            if (!items.length) {
                searchResults.innerHTML = `
                    <div class="search-result">
                        <strong>Ничего не найдено</strong>
                        Попробуй другой запрос: жалобы, штрафы, PTP, грубость, обещание оплаты.
                    </div>
                `;
                return;
            }

            searchResults.innerHTML = items.map(item => `
                <div class="search-result">
                    <strong>Звонок ${item.id}</strong>
                    ${item.text}
                    <div class="tag-row">
                        ${item.tags.map(tag => `<span class="mini-tag">${tag}</span>`).join("")}
                    </div>
                </div>
            `).join("");
        }

        if (searchInput && searchBtn) {
            searchBtn.addEventListener("click", () => renderResults(searchInput.value));
            searchInput.addEventListener("input", () => renderResults(searchInput.value));
        }

        const logTexts = [
            "AI анализирует смысл запроса...",
            "Проверка жалоб, штрафов и конфликтов...",
            "Формирование релевантной выборки звонков..."
        ];

        function animateLog(id, text, delay) {
            const el = document.getElementById(id);
            if (!el) return;

            setTimeout(() => {
                let i = 0;
                el.textContent = "";
                const interval = setInterval(() => {
                    el.textContent += text.charAt(i);
                    i++;
                    if (i >= text.length) clearInterval(interval);
                }, 24);
            }, delay);
        }

        animateLog("log1", logTexts[0], 400);
        animateLog("log2", logTexts[1], 1200);
        animateLog("log3", logTexts[2], 2100);
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    success = request.args.get("success")
    error = request.args.get("error")

    message = ""

    if success:
        message = """
        <div class="alert success">
            Заявка отправлена. Мы свяжемся с вами.
        </div>
        """

    if error == "empty":
        message = """
        <div class="alert error">
            Заполните имя, телефон и выберите услугу.
        </div>
        """

    if error == "spam":
        message = """
        <div class="alert error">
            Заявка отклонена.
        </div>
        """

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        comment = request.form.get("comment", "").strip()
        website = request.form.get("website", "").strip()

        if website:
            return redirect(url_for("home", error="spam"))

        if not (name and phone and service):
            return redirect(url_for("home", error="empty"))

        try:
            send_telegram(name, phone, service, comment)
        except Exception as e:
            print("TELEGRAM ERROR:", e)

        return redirect(url_for("home", success=1))

    return render_template_string(HTML, message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
