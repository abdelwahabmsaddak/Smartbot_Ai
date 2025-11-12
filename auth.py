import os, hmac, hashlib
from typing import Optional
from dotenv import load_dotenv
from passlib.hash import bcrypt
from itsdangerous import URLSafeSerializer
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from app.db import get_user_by_email, create_user, get_user_by_google_sub, get_user_by_telegram_id

load_dotenv()
SECRET = os.getenv("SECRET_KEY", "CHANGE_ME")
SER = URLSafeSerializer(SECRET, salt="session")
SITE_NAME = os.getenv("SITE_NAME", "SmartBot AI")

# -------------------------
# Password helpers
def hash_password(pw: str) -> str:
    return bcrypt.hash(pw)

def verify_password(pw: str, pw_hash: str) -> bool:
    return bcrypt.verify(pw, pw_hash)

# -------------------------
# Sessions (cookie)
SESSION_COOKIE = "sb_session"

def set_session(resp: Response, user_id: int):
    token = SER.dumps({"uid": user_id})
    resp.set_cookie(SESSION_COOKIE, token, httponly=True, samesite="lax")

def clear_session(resp: Response):
    resp.delete_cookie(SESSION_COOKIE)

def get_session_uid(request: Request) -> Optional[int]:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    try:
        data = SER.loads(token)
        return int(data.get("uid"))
    except Exception:
        return None

# -------------------------
# Google OAuth
def get_oauth():
    oauth = OAuth()
    oauth.register(
        name='google',
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={'scope': 'openid email profile'},
    )
    return oauth

async def google_login(request: Request):
    oauth = get_oauth()
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URL")
    return await oauth.google.authorize_redirect(request, redirect_uri)

async def google_callback(request: Request):
    oauth = get_oauth()
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get('userinfo')
    if not userinfo:
        return RedirectResponse(url="/login?error=google")
    sub = userinfo["sub"]
    email = userinfo.get("email", f"user-{sub}@google.local")
    name = userinfo.get("name", "Google User")

    user = get_user_by_google_sub(sub)
    if not user:
        # create or attach to existing email
        existing = get_user_by_email(email)
        if existing:
            # attach google_sub
            from app.db import sqlite3, DB_PATH
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("UPDATE users SET google_sub=?, provider=? WHERE id=?",
                        (sub, "google", existing["id"]))
            con.commit(); con.close()
            uid = existing["id"]
        else:
            uid = create_user(email=email, name=name, provider="google", google_sub=sub)
    else:
        uid = user["id"]

    resp = RedirectResponse(url="/dashboard")
    set_session(resp, uid)
    return resp

# -------------------------
# Telegram Login (Widget)
# توثيق: https://core.telegram.org/widgets/login
def check_telegram_auth(data: dict) -> bool:
    """تحقق التوقيع من Telegram."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        return False
    auth_data = {k: v for k, v in data.items() if k != "hash"}
    check_string = "\n".join(f"{k}={auth_data[k]}" for k in sorted(auth_data))
    secret_key = hashlib.sha256(token.encode()).digest()
    hsh = hmac.new(secret_key, msg=check_string.encode(), digestmod=hashlib.sha256).hexdigest()
    return hsh == data.get("hash")

def telegram_login_response(tg_id: str, name: str, email: str = None):
    user = get_user_by_telegram_id(tg_id)
    if not user:
        email = email or f"user-{tg_id}@telegram.local"
        uid = create_user(email=email, name=name, provider="telegram", telegram_id=tg_id)
    else:
        uid = user["id"]
    resp = RedirectResponse(url="/dashboard")
    set_session(resp, uid)
    return resp
