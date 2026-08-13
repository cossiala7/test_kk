"""
Backend FastAPI minimal pour recevoir les infos d'appareil
et envoyer un e-mail de notification.

Installation :
    pip install fastapi uvicorn python-dotenv --break-system-packages

Lancement local :
    uvicorn main:app --reload

Variables d'environnement à définir (voir .env.example) :
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
    NOTIFY_EMAIL_TO   -> ton adresse e-mail (celle qui reçoit les notifs)
"""

import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Autoriser les requêtes depuis ta page HTML (ajuste l'origine en prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dakar-shop.onrender.com"],  # remplace par ton domaine en prod, ex: ["https://tonsite.com"]
    allow_methods=["POST"],
    allow_headers=["*"],
)


class DeviceInfo(BaseModel):
    brand: str
    os: str
    browser: str
    time: str


SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
NOTIFY_EMAIL_TO = os.getenv("NOTIFY_EMAIL_TO", "")


def send_email(info: DeviceInfo):
    body = f"""📱 Nouveau clic détecté

Appareil : {info.brand}
Système  : {info.os}
Navigateur : {info.browser}
Heure    : {info.time}
"""
    msg = MIMEText(body)
    msg["Subject"] = "Nouvelle détection d'appareil"
    msg["From"] = SMTP_USER
    msg["To"] = NOTIFY_EMAIL_TO

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)


@app.post("/notify")
def notify(info: DeviceInfo):
    try:
        send_email(info)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.get("/")
def health():
    return {"status": "running", "time": datetime.now().isoformat()}
