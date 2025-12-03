from datetime import datetime
from typing import Any, Dict, List

from .config import load_config
from .data_loader import load_all_data, get_customer, get_recent_orders, get_active_coupons
from .geo import find_nearest_open_store
from .llm_orchestrator import build_prompt, call_llm
from .rag import RAGIndex


class PulseCXAgent:
    """
    Core orchestrator that ties together data, geo, privacy, RAG, and LLM.
    """

    def __init__(self, config_path: str = "config.yaml") -> None:
        self.config = load_config(config_path)
        self.customers, self.orders, self.stores, self.coupons = load_all_data(self.config)

        rag_cfg = self.config.get("rag", {})
        self.rag_index = None
        if rag_cfg.get("enabled", False):
            self.rag_index = RAGIndex(rag_cfg["docs_path"])
            self.rag_index.build()

    def _get_rag_snippets(self, message: str) -> List[str]:
        if self.rag_index is None:
            return []
        rag_cfg = self.config.get("rag", {})
        top_k = rag_cfg.get("top_k", 3)
        return self.rag_index.retrieve(message, top_k=top_k)

    def handle_message(
        self,
        user_id: str,
        message: str,
        lat: float,
        lon: float,
    ) -> Dict[str, Any]:
        """
        Main entrypoint: given user_id + message + location, return bot response payload.
        """
        customer = get_customer(self.customers, user_id)
        recent_orders = get_recent_orders(self.orders, user_id)
        active_coupons = get_active_coupons(self.coupons, user_id)

        now = datetime.now()
        store = find_nearest_open_store(self.stores, lat, lon, now.hour)

        context = {
            "customer": customer,
            "recent_orders": recent_orders,
            "store": store,
            "coupons": active_coupons,
        }

        rag_snippets = self._get_rag_snippets(message)
        prompt = build_prompt(context, message, rag_snippets)
        reply = call_llm(prompt, self.config["llm"])

        return {
            "reply": reply,
            "store": store,
            "coupon": active_coupons[0] if active_coupons else None,
        }
