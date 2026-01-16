from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from .config import settings

# IMPORTANT:
# - bcrypt only supports up to 72 bytes
# - we truncate safely to avoid runtime crashes

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

MAX_BCRYPT_LEN = 72


def _normalize_password(pw: str) -> str:
    if not pw:
        return pw
    # bcrypt limit protection
    if len(pw.encode("utf-8")) > MAX_BCRYPT_LEN:
        return pw.encode("utf-8")[:MAX_BCRYPT_LEN].decode("utf-8", errors="ignore")
    return pw


def hash_password(pw: str) -> str:
    pw = _normalize_password(pw)
    return pwd_context.hash(pw)


def verify_password(pw: str, hashed: str) -> bool:
    pw = _normalize_password(pw)
    return pwd_context.verify(pw, hashed)


def create_access_token(sub: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_MINUTES
    )
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG],
        )
        return payload.get("sub")
    except JWTError:
        return None
