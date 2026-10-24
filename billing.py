"""
baibai 收款层 — 面包多 Pay（赞赏码/H5 收款，永久免费开源，企业定制报价）

定位：22 工具 + MCP Server 永久免费，通过面包多 Pay赞赏/企业定制变现。
免费版：30 次/天（拉满体验），深度/批量工具需企业定制。
"""
import os
import hashlib
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
            "upgrade_url": "https://mbd.pub/@Zeon7744",
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

# ─────────────────────────── 面包多 Pay 网关（mbd.pub）───────────────────────────
# 官方文档 https://doc.mbd.pub/ ；费率 2% + 0.1 元/笔（<0.5 元免收），以开通页为准。
# 个人可实名收款；支付宝即时到账（5 分钟内），微信次日自动提现至银行卡。
# 环境变量（不入库）：MBD_APP_ID / MBD_API_KEY / MBD_GATEWAY_URL / MBD_WEBHOOK_URL / MBD_PAY_CHANNEL


def mbd_sign_mbd(data: dict, api_key: str) -> str:
    """面包多 Pay 官方签名：非空参数按 key ASCII 字典序拼 k=v&k=v，再 &key=app_key，取 MD5。"""
    ordered = {k: v for k, v in sorted(data.items()) if v not in ("", None)}
    s = "&".join(f"{k}={v}" for k, v in ordered.items())
    return hashlib.md5((s + "&key=" + api_key).encode("utf-8")).hexdigest()


class MbdGateway:
    """
    面包多 Pay 网关：赞赏码 / 支付宝 H5 / 微信 H5 三种收款模式，均走 newapi.mbd.pub。
    未配 MBD_API_KEY/MBD_APP_ID 时降级（对齐 noop 未配密钥行为，不发起真实请求）。
    """
    name = "mbd"
    DEFAULT_BASE = "https://newapi.mbd.pub/release"

    def __init__(self):
        self.app_id = os.getenv("MBD_APP_ID", "")
        self.api_key = os.getenv("MBD_API_KEY", "")
        self.base = os.getenv("MBD_GATEWAY_URL", self.DEFAULT_BASE)
        self.webhook_url = os.getenv("MBD_WEBHOOK_URL", "")

    def _missing(self):
        return [k for k, v in (("MBD_API_KEY", self.api_key), ("MBD_APP_ID", self.app_id)) if not v]

    def _post(self, path, payload):
        import urllib.request as _ur
        body = dict(payload)
        body["app_id"] = self.app_id
        body["sign"] = mbd_sign_mbd(body, self.api_key)
        req = _ur.Request(f"{self.base}{path}",
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST")
        with _ur.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def create_order(self, tenant_id, amount_cents, product, plan, order_meta=None):
        missing = self._missing()
        if missing:
            return {"order_id": "pending", "status": "created_pending_key",
                    "needs_secret": missing, "amount_cents": amount_cents,
                    "plan": plan, "product": product, "gateway": "mbd",
                    "note": "面包多 Pay 未开通：注册 mbd.pub → 闪电结算 → 控制台取 app_id/app_key → 填 MBD_APP_ID + MBD_API_KEY 即可真下单"}
        out_trade_no = "mbd_" + str(uuid.uuid4())[:16]
        payload = {"description": f"{product}({plan})"[:42],
                   "amount_total": int(amount_cents), "out_trade_no": out_trade_no}
        channel = os.getenv("MBD_PAY_CHANNEL", "alipay")
        path = "/wx/prepay" if channel == "wx_h5" else "/alipay/pay"
        if channel == "wx_h5":
            payload["channel"] = "h5"
        try:
            result = self._post(path, payload)
            if "error" in result:
                return {"order_id": out_trade_no, "status": "gateway_rejected", "error": result["error"], "gateway": "mbd"}
            key = "h5_url" if channel == "wx_h5" else "pay_body"
            return {"order_id": out_trade_no, "status": "created",
                    key: result.get("h5_url" if channel == "wx_h5" else "body", ""), "gateway": "mbd"}
        except Exception as e:
            return {"order_id": out_trade_no, "status": "gateway_error", "error": str(e), "gateway": "mbd"}

    def query_callback(self, order_id):
        missing = self._missing()
        if missing:
            return {"order_id": order_id, "status": "pending_key", "paid": False,
                    "needs_secret": missing, "gateway": "mbd"}
        payload = {"out_trade_no": order_id, "app_id": self.app_id}
        payload["sign"] = mbd_sign_mbd(payload, self.api_key)
        try:
            result = self._post("/search_order", payload)
            if "error" in result:
                return {"order_id": order_id, "status": "query_error", "paid": False, "error": result["error"], "gateway": "mbd"}
            state = str(result.get("state", ""))
            return {"order_id": order_id, "status": state, "paid": state in ("1", "2"),
                    "amount_cents": int(result.get("amount", 0)), "gateway": "mbd"}
        except Exception as e:
            return {"order_id": order_id, "status": "query_failed", "paid": False, "error": str(e), "gateway": "mbd"}

    def verify_callback(self, payload):
        """Webhook（charge_succeeded / complaint）：控制台直连 URL + 本地 out_trade_no 去重。"""
        if not isinstance(payload, dict):
            return False
        data = payload.get("data") or {}
        return payload.get("type") in ("charge_succeeded", "complaint") and bool(data.get("out_trade_no"))

    def refund(self, order_id, amount_cents, reason=""):
        missing = self._missing()
        if missing:
            return {"order_id": order_id, "ok": False, "note": "面包多 Pay 凭据未配",
                    "needs_secret": missing, "gateway": "mbd"}
        payload = {"out_trade_no": order_id, "refund_amount": int(amount_cents or 0), "app_id": self.app_id}
        payload["sign"] = mbd_sign_mbd(payload, self.api_key)
        try:
            result = self._post("/refund", payload)
            ok = "error" not in result
            return {"order_id": order_id, "ok": ok, "refunded_cents": amount_cents if ok else 0, "gateway": "mbd"}
        except Exception as e:
            return {"order_id": order_id, "ok": False, "error": str(e), "gateway": "mbd"}


_REGISTRY = {"noop": NoopGateway, "mbd": MbdGateway}
def get_gateway(name=None):
    return _REGISTRY.get(name or os.environ.get("BILLING_GATEWAY", "mbd"), NoopGateway)()
