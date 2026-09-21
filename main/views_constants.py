import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
PHONE_RE = re.compile(r"^\+?[0-9\s\-()]{7,20}$")
IRAN_MOBILE_RE = re.compile(r"^09\d{9}$")
PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def normalize_phone(value: str) -> str:
    return value.translate(PERSIAN_DIGITS).strip()


def normalize_iranian_mobile(value: str) -> str:
    phone = normalize_phone(value)
    compact = re.sub(r"[\s\-()]", "", phone)
    if compact.startswith("+98"):
        compact = "0" + compact[3:]
    elif compact.startswith("0098"):
        compact = "0" + compact[4:]
    return compact


## بهت افتخار میکنم بهت پارسا