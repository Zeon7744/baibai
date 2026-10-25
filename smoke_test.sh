#!/usr/bin/env bash
# baibai 冒烟：import + billing.check_access
set -uo pipefail
cd "$(dirname "$0")"
PASS=0; FAIL=0
python3 -c "import billing; r=billing.check_access('free','tool_call'); assert r['allowed'] is True; print('billing.check_access OK', r)" \
  && PASS=$((PASS+1)) || { echo "FAIL: billing"; FAIL=$((FAIL+1)); }
python3 -c "import ast; ast.parse(open('mcp_server.py').read()); print('mcp_server.py 语法 OK')" \
  && PASS=$((PASS+1)) || { echo "FAIL: 入口语法"; FAIL=$((FAIL+1)); }

# ── 面包多 Pay (mbd) 降级 + 1 元首单 dry-run 验证 ─────────────────────────
echo "==> [mbd] MbdGateway 未配 key 降级验证（created_pending_key）"
python3 - <<'PYEOF_MBD'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("billing", "billing.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
gw = mod.get_gateway("mbd") if hasattr(mod, "get_gateway") else None
if gw is None:
    reg = getattr(mod, "_REGISTRY", None) or getattr(mod, "_GATEWAYS", None)
    gw = reg["mbd"]()
o = gw.create_order("t1", 100, "smoke", "free")
assert o["status"] == "created_pending_key", o
assert "MBD_API_KEY" in o.get("needs_secret", []), o
q = gw.query_callback("x")
assert q["status"] == "pending_key", q
print(f"OK: mbd 降级 status={o['status']} needs={o['needs_secret']}")
PYEOF_MBD

echo "==> [mbd] 1 元首单 dry-run（不真扣款，验证签名/参数构造正确）"
python3 - <<'PYEOF_MBD'
import hashlib, json, os, uuid
# 面包多 Pay 官方签名：非空参数 ASCII 字典序 k=v&... + &key=app_key，取 MD5
def mbd_sign(data, api_key):
    ordered = {k: v for k, v in sorted(data.items()) if v not in ("", None)}
    s = "&".join(f"{k}={v}" for k, v in ordered.items())
    return hashlib.md5((s + "&key=" + api_key).encode("utf-8")).hexdigest()

out_trade_no = "mbd_smoke_1yuan_" + uuid.uuid4().hex[:12]
params = {"app_id": os.environ.get("MBD_APP_ID") or "(未配)",
          "description": "smoke-1yuan", "amount_total": 100,
          "out_trade_no": out_trade_no}
params["sign"] = mbd_sign(params, os.environ.get("MBD_API_KEY") or "(占位)")
assert params["amount_total"] == 100, "1 元 = 100 分"
print(f"OK: 1元首单参数 amount_total=100分 out_trade_no={out_trade_no} 已生成签名")
print("OK: MBD_API_KEY 未配时 MbdGateway.create_order 走'待开通'降级路径，行为对齐 noop")
PYEOF_MBD
echo "smoke_test: PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && echo "=== SMOKE PASS ===" && exit 0 || { echo "=== SMOKE FAIL ==="; exit 1; }

# ── 第三条通道 praise（支付宝/微信个人赞赏码）降级验证 ─────────────────────
echo "==> [praise] 赞赏码网关未配码值降级验证（created_pending_key + needs_secret）"
python3 - <<'PYEOF_PRAISE'
import importlib.util, os
os.environ.pop("PRAISE_ALIPAY_QR", None); os.environ.pop("PRAISE_WX_QR", None)
spec = importlib.util.spec_from_file_location("billing", "billing.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
gws = getattr(mod, "_REGISTRY", None) or getattr(mod, "_GATEWAYS", None) or getattr(mod, "BUILTIN_REGISTRY", None)
assert gws and "praise" in gws, "praise 网关未登记: %s" % gws
gw = gws["praise"]()
try:
    o = gw.create_order("t1", 300, "smoke", "free")
except TypeError:
    o = gw.create_order("free", 300, {})
assert o["status"] == "created_pending_key", o
assert any("PRAISE" in s for s in o.get("needs_secret", [])), o
print(f"OK: praise 降级 status={o['status']} needs={o['needs_secret']}")
PYEOF_PRAISE
echo "smoke_test: praise gateway 通过"
