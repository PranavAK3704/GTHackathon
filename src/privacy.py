import re


_PHONE_REGEX = re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")
_EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def _mask_phone_match(match: re.Match) -> str:
    number = match.group()
    return "***-***-" + number[-4:]


def _mask_email_match(match: re.Match) -> str:
    email = match.group()
    local, _, domain = email.partition("@")
    if len(local) <= 2:
        masked_local = "*" * len(local)
    else:
        masked_local = local[0] + "***" + local[-1]
    return f"{masked_local}@{domain}"


def mask_text(text: str) -> str:
    """
    Mask phone numbers and emails inside a string.
    Used before sending anything to a public LLM.
    """
    text = _PHONE_REGEX.sub(_mask_phone_match, text)
    text = _EMAIL_REGEX.sub(_mask_email_match, text)
    return text
