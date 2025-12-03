from typing import Any, Dict, List

from .privacy import mask_text


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


def call_llm(prompt: str, llm_cfg: Dict[str, Any]) -> str:
    """
    For now, return a template answer so the system runs even without an API key.
    Later we can plug in OpenAI or Gemini here.
    """
    provider = llm_cfg.get("provider", "template")

    if provider == "openai":
        # Example wiring (commented to keep project self-contained):
        # from openai import OpenAI
        # import os
        # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        # resp = client.chat.completions.create(
        #     model=llm_cfg.get("model", "gpt-4o-mini"),
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=llm_cfg.get("max_tokens", 400),
        # )
        # return resp.choices[0].message.content
        pass

    # Fallback – deterministic template that still uses the idea of personalization
    return (
        "Thanks for reaching out! Based on your profile and recent visits, the nearest open "
        "store is ready to serve you, and we have at least one active coupon on your account. "
        "Please head to the suggested store and show this message at the counter to redeem your offer."
    )
