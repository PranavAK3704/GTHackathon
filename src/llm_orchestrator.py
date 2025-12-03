from typing import Any, Dict, List
import os

from .privacy import mask_text

TEMPLATE_FALLBACK = (
    "Thanks for reaching out! Based on your profile and recent visits, the nearest "
    "open store is ready to serve you, and we have at least one active coupon on "
    "your account. Please head to the suggested store and show this message at the "
    "counter to redeem your offer."
)


def build_prompt(context: Dict[str, Any], user_message: str, rag_snippets: List[str]) -> str:
    """
    Build the prompt that will be sent to the LLM (or used for template response).
    """
    safe_message = mask_text(user_message)

    prompt = (
        "You are PulseCX, a hyper-personalized retail assistant. "
        "You MUST answer using only the provided structured context. "
        "If you don't know something from the context, say you are not sure.\n\n"
        f"Customer context: {context.get('customer')}\n"
        f"Recent orders: {context.get('recent_orders')}\n"
        f"Nearest store: {context.get('store')}\n"
        f"Available coupons: {context.get('coupons')}\n"
    )

    if rag_snippets:
        prompt += f"\nRelevant policy snippets: {rag_snippets}\n"

    prompt += f"\nUser message: {safe_message}\n"
    prompt += "Respond in under 80 words, friendly and specific.\n"

    return prompt


def _call_groq(prompt: str, llm_cfg: Dict[str, Any]) -> str:
    """
    Call Groq chat completions API. Requires:
      - pip install groq
      - environment variable GROQ_API_KEY
    """
    try:
        from groq import Groq  # type: ignore
    except Exception:
        # Library not installed – fall back
        return TEMPLATE_FALLBACK

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        # No key in env – fall back
        return TEMPLATE_FALLBACK

    client = Groq(api_key=api_key)

    model = llm_cfg.get("model", "llama-3.3-70b-versatile")

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are PulseCX, a helpful, precise retail assistant. "
                        "Always ground your answers in the given context."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=llm_cfg.get("max_tokens", 400),
        )
        return completion.choices[0].message.content  # type: ignore[index]
    except Exception:
        # Any Groq API error – silently fall back for demo stability
        return TEMPLATE_FALLBACK


def call_llm(prompt: str, llm_cfg: Dict[str, Any]) -> str:
    """
    Dispatch to the correct LLM provider. Currently supports:
      - provider: "groq"
      - provider: "template" (fallback)
    """
    provider = llm_cfg.get("provider", "template").lower()

    if provider == "groq":
        return _call_groq(prompt, llm_cfg)

    # Default: deterministic template answer so the project runs offline
    return TEMPLATE_FALLBACK
