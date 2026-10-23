# baibai 收款与门控（爱发电 afdian 赞赏码）

## 定位
22 工具 + MCP Server 永久免费开源，通过爱发电赞赏码 + 企业定制变现。

## 定价档位（与 billing.py 对齐）
| 档位 | 价格 | 限制 |
|---|---|---|
| Free | ¥0（永久免费） | 30 次/天，全部 22 工具 |
| 企业 | 定制报价 | 定制开发/SLA/批量处理 |

## 收款流程（先体验后付费）
1. 免费 30 次/天，超限 402 + 赞赏/企业定制链接（爱发电 https://afdian.com/@Zeon7744）
2. 赞赏码不支持退款；企业定制走线下合同
3. 无 key 走 `noop` 安全降级

## 环境变量
`JZ_AFDIAN_USER` / `JZ_AFDIAN_TOKEN` / `BILLING_GATEWAY`（noop|afdian）
