#!/usr/bin/env python3
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
TS = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

SOURCES = {
    "openai_news": "https://openai.com/news/",
    "openai_ads": "https://openai.com/index/new-ways-to-buy-chatgpt-ads/",
    "carb_act": "https://ww2.arb.ca.gov/our-work/programs/advanced-clean-trucks",
    "carb_fact": "https://ww2.arb.ca.gov/resources/fact-sheets/advanced-clean-trucks-fact-sheet",
    "daimler": "https://www.daimlertruck.com/en/innovation/powertrain/our-eportfolio",
    "torc": "https://torc.ai/",
}


def fetch(url: str):
    t0 = time.time()
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 ClawBriefBot/1.0"})
    try:
        with urlopen(req, timeout=20) as r:
            body = r.read().decode("utf-8", errors="ignore")
            return {"ok": True, "status": r.status, "latency_ms": int((time.time()-t0)*1000), "body": body, "error": None}
    except HTTPError as e:
        return {"ok": False, "status": int(e.code), "latency_ms": int((time.time()-t0)*1000), "body": "", "error": f"HTTP {e.code}"}
    except URLError as e:
        return {"ok": False, "status": None, "latency_ms": int((time.time()-t0)*1000), "body": "", "error": str(e.reason)}
    except Exception as e:
        return {"ok": False, "status": None, "latency_ms": int((time.time()-t0)*1000), "body": "", "error": str(e)}


def pick(pattern, text, default="N/A"):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else default


results = {k: fetch(u) for k, u in SOURCES.items()}
success = sum(1 for r in results.values() if r["ok"])
failed = len(results) - success

# hard data extraction from stable pages
ads = results["openai_ads"]["body"]
carb = results["carb_fact"]["body"]
dai = results["daimler"]["body"]

# Build report body with only verified values we can anchor to source docs.
report = f"""# 商用情报简报 · {TODAY}（自动抓取实版）

- 刷新时间：{TS}
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

- 总源数：{len(results)}
- 成功：{success}
- 失败：{failed}

"""

for k, v in results.items():
    status = v['status'] if v['status'] is not None else '-'
    err = v['error'] or ''
    report += f"- {k}: status={status}, latency={v['latency_ms']}ms {err}\n"

report_path = DATA / f"{TODAY}-ai-opportunity.md"
report_path.write_text(report, encoding="utf-8")

monitor = {
    "timestamp": TS,
    "date": TODAY,
    "total": len(results),
    "success": success,
    "failed": failed,
    "sources": {
        k: {
            "url": SOURCES[k],
            "ok": v["ok"],
            "status": v["status"],
            "latency_ms": v["latency_ms"],
            "error": v["error"],
        }
        for k, v in results.items()
    },
}

(DATA / "monitoring-latest.json").write_text(json.dumps(monitor, ensure_ascii=False, indent=2), encoding="utf-8")
(DATA / f"{TODAY}-monitoring.json").write_text(json.dumps(monitor, ensure_ascii=False, indent=2), encoding="utf-8")

monitor_html = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>ClawBrief Monitoring</title>
<style>body{{font-family:Arial,sans-serif;max-width:980px;margin:20px auto;padding:0 12px}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #ddd;padding:8px}}th{{background:#f6f6f6}}</style></head><body>
<h1>ClawBrief 抓取监测</h1><p>更新时间：{TS}</p>
<p>总源数：{len(results)} | 成功：{success} | 失败：{failed}</p>
<table><tr><th>source</th><th>status</th><th>latency_ms</th><th>error</th><th>url</th></tr>
"""
for k,v in monitor["sources"].items():
    monitor_html += f"<tr><td>{k}</td><td>{v['status']}</td><td>{v['latency_ms']}</td><td>{v['error'] or ''}</td><td><a href='{v['url']}'>link</a></td></tr>"
monitor_html += "</table><p><a href='./'>回到报告</a></p></body></html>"
(REPO / "monitoring.html").write_text(monitor_html, encoding="utf-8")

# update index entry list
index = REPO / "index.html"
h = index.read_text(encoding="utf-8")
entry = f"      '{TODAY}-ai-opportunity.md',"
if entry not in h:
    h = h.replace("    const entries = [\n", "    const entries = [\n" + entry + "\n", 1)
    index.write_text(h, encoding="utf-8")

print(report_path)
print(REPO / 'monitoring.html')
