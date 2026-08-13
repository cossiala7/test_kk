# Détecteur de téléphone (avec notice de consentement)

## Fichiers
- `index.html` — page à envoyer aux gens. Affiche la marque/modèle détecté ET informe la personne que l'info est envoyée par e-mail.
- `main.py` — backend FastAPI qui reçoit les infos et envoie l'e-mail.
- `.env.example` — variables SMTP à configurer.

## Étapes

### 1. Backend
```bash
pip install fastapi uvicorn python-dotenv --break-system-packages
cp .env.example .env
# édite .env avec tes identifiants SMTP (pour Gmail, utilise un "mot de passe d'application")
uvicorn main:app --reload
```
Teste sur http://localhost:8000

Pour l'héberger gratuitement : Render.com, Railway.app, ou Fly.io fonctionnent bien avec FastAPI.

### 2. Frontend
Dans `index.html`, remplace :
```js
"https://TON-BACKEND.exemple.com/notify"
```
par l'URL réelle de ton backend une fois déployé.

Héberge `index.html` sur Vercel, Netlify ou GitHub Pages (gratuit, glisser-déposer).

### 3. Important — CORS
Dans `main.py`, remplace `allow_origins=["*"]` par l'URL exacte de ton site une fois en prod, pour éviter que n'importe qui utilise ton backend.

### 4. Gmail
Si tu utilises Gmail comme SMTP, active la validation en 2 étapes puis génère un
"mot de passe d'application" ici : https://myaccount.google.com/apppasswords
Le mot de passe normal de ton compte ne fonctionnera pas.

## Ce que la page fait (et ne fait pas)
- ✅ Affiche à la personne la marque/OS/navigateur détecté
- ✅ Affiche clairement qu'un e-mail va être envoyé, avant l'envoi
- ✅ N'envoie que des infos techniques non identifiantes (pas de nom, localisation, contacts...)
- ❌ Ne collecte rien à l'insu de la personne
