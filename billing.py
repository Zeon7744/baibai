"""
baibai 收款层 — 爱发电 afdian 赞赏码（永久免费开源，企业定制报价）

定位：22 工具 + MCP Server 永久免费，通过爱发电赞赏/企业定制变现。
免费版：30 次/天（拉满体验），深度/批量工具需企业定制。
"""
import os
import time
import uuid
import json
import urllib.request

PAYWALL_RULES = {
    "free":     {"daily_limit": 30, "label": "免费版（30 次/天）"},
    "enterprise": {"daily_limit": -1, "label": "企业定制（联系报价）"},
}

_STATE = {"date": "", "count": 0}

def _today():
    return time.strftime("%Y-%m-%d")

def check_access(plan: str = "free", action: str = "tool_call") -> dict:
    """门控：免费版 30 次/天（拉满体验），企业不限次。"""
    rules = PAYWALL_RULES.get(plan, PAYWALL_RULES["free"])
    limit = rules["daily_limit"]

    if limit == -1:
        return {"allowed": True, "remaining": -1, "reason": ""}

    if _STATE["date"] != _today():
        _STATE["date"] = _today()
        _STATE["count"] = 0

    if _STATE["count"] >= limit:
        return {
            "allowed": False,
            "remaining": 0,
            "reason": f"免费版每日 {limit} 次已用完，深度/批量需求请联系企业定制",
            "upgrade_url": "https://afdian.com/@Zeon7744",
            "http_status": 402,
        }

    _STATE["count"] += 1
    return {"allowed": True, "remaining": limit - _STATE["count"], "reason": ""}

def get_pricing() -> list[dict]:
    return [
        {"plan": "free", "price": 0, "price_label": "¥0（永久免费）",
         "features": ["全部 22 个工具", "MCP Server", "30 次/天"]},
        {"plan": "enterprise", "price": 0, "price_label": "定制报价",
         "features": ["定制开发", "技术对接", "SLA", "批量处理"]},
    ]

class NoopGateway:
    name = "noop"
    def create_order(self, tenant_id, amount_cents, product, plan, order_meta=None):
        return {"order_id": "noop_" + str(uuid.uuid4())[:12], "status": "created", "gateway": "noop"}
    def query_callback(self, order_id):
        return {"order_id": order_id, "status": "unpaid", "paid": False}
    def refund(self, order_id, amount_cents, reason=""):
        return {"order_id": order_id, "ok": True}

class AfdianGateway:
    """爱发电赞赏码网关"""
    name = "afdian"
    DEFAULT_BASE = "https://afdian.com/api"
    def __init__(self):
        self.user_id = os.environ.get("JZ_AFDIAN_USER", "")
        self.token = os.environ.get("JZ_AFDIAN_TOKEN", "")
        self.base = os.environ.get("JZ_AFDIAN_BASE", self.DEFAULT_BASE)

    def _post(self, path, payload):
        body = dict(payload)
        if self.token:
            body["token"] = self.token
        req = urllib.request.Request(f"{self.base}{path}",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def create_order(self, tenant_id, amount_cents, product, plan, order_meta=None):
        if not self.user_id or not self.token:
            return {"order_id": "pending", "status": "created_pending_key",
                    "needs_secret": ["JZ_AFDIAN_USER", "JZ_AFDIAN_TOKEN"]}
        price = round(amount_cents / 100.0, 2)
        out_trade_no = "baibai_" + str(uuid.uuid4())[:16]
        payload = {"user_id": self.user_id, "price": str(price),
                   "name": f"baibai({plan})"[:42], "out_trade_no": out_trade_no}
        try:
            result = self._post("/payment/create", payload)
            if result.get("code") != 0:
                return {"order_id": out_trade_no, "status": "gateway_rejected"}
            return {"order_id": out_trade_no, "status": "created",
                    "pay_url": result.get("data", {}).get("url", ""), "gateway": "afdian"}
        except Exception as e:
            return {"order_id": out_trade_no, "status": "gateway_error", "error": str(e)}

    def query_callback(self, order_id):
        if not self.user_id or not self.token:
            return {"order_id": order_id, "status": "pending_key", "paid": False}
        payload = {"user_id": self.user_id, "out_trade_no": order_id}
        try:
            result = self._post("/payment/query", payload)
            return {"order_id": order_id, "paid": result.get("data", {}).get("status") in ("paid", "success")}
        except Exception as e:
            return {"order_id": order_id, "paid": False, "error": str(e)}

    def refund(self, order_id, amount_cents, reason=""):
        return {"order_id": order_id, "ok": False, "note": "赞赏码不支持退款"}

_REGISTRY = {"noop": NoopGateway, "afdian": AfdianGateway}
def get_gateway(name=None):
    return _REGISTRY.get(name or os.environ.get("BILLING_GATEWAY", "noop"), NoopGateway)()
