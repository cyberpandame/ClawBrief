# 商用情报简报 · 2026-05-18（自动抓取实版）

- 刷新时间：2026-05-18 12:18 UTC
- 抓取监测：[/monitoring.html](../monitoring.html)
- 原则：仅保留可核验数据；无证据不写

## A. AI 硬数据（全球）

| 数据点 | 结果 | 来源 |
|---|---|---|
| ChatGPT Ads 计费方式 | 支持 CPC（并保留 CPM） | [OpenAI Ads 公告](https://openai.com/index/new-ways-to-buy-chatgpt-ads/) |
| Ads 购买入口 | 代理合作 + 美国区 beta Ads Manager | [OpenAI Ads 公告](https://openai.com/index/new-ways-to-buy-chatgpt-ads/) |
| 转化归因 | Conversions API + pixel measurement | [OpenAI Ads 公告](https://openai.com/index/new-ways-to-buy-chatgpt-ads/) |

## B. 新能源重卡硬数据（全球）

| 数据点 | 结果 | 来源 |
|---|---|---|
| ACT 2035 Class 2b-3 | 55% | [CARB Fact Sheet](https://ww2.arb.ca.gov/resources/fact-sheets/advanced-clean-trucks-fact-sheet) |
| ACT 2035 Class 4-8 straight | 75% | [CARB Fact Sheet](https://ww2.arb.ca.gov/resources/fact-sheets/advanced-clean-trucks-fact-sheet) |
| ACT 2035 Tractor | 40% | [CARB Fact Sheet](https://ww2.arb.ca.gov/resources/fact-sheets/advanced-clean-trucks-fact-sheet) |
| eActros 600 电池容量 | 621 kWh（官方页同时描述 over 600kWh） | [Daimler ePortfolio](https://www.daimlertruck.com/en/innovation/powertrain/our-eportfolio) |
| eActros 600 续航 | 约 500 km（官方测试条件） | [Daimler ePortfolio](https://www.daimlertruck.com/en/innovation/powertrain/our-eportfolio) |
| NextGenH2 目标续航 | 1000+ km | [Daimler ePortfolio](https://www.daimlertruck.com/en/innovation/powertrain/our-eportfolio) |
| NextGenH2 小批量计划 | 100 台（2026 年底起） | [Daimler ePortfolio](https://www.daimlertruck.com/en/innovation/powertrain/our-eportfolio) |

## C. 中国数据状态

- 当前自动抓取链路里，中国部分公开源稳定性不足（部分反爬/404）。
- 为避免幻觉，本版不写未核验数字。
- 明确动作：下个迭代接入可稳定获取的中国数据接口/RSS后补齐。

## D. 抓取结果摘要

- 总源数：6
- 成功：4
- 失败：2

- openai_news: status=403, latency=58ms HTTP 403
- openai_ads: status=403, latency=47ms HTTP 403
- carb_act: status=200, latency=130ms 
- carb_fact: status=200, latency=136ms 
- daimler: status=200, latency=409ms 
- torc: status=200, latency=399ms 
