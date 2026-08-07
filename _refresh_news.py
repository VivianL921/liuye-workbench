#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刷新 brand-news.json：
  - 合并 _pending_news.json 中的新动态（按 brand+title 去重，绝不删除已有条目 → 历史全保留）
  - 自动分配新 id（在现有最大 id 之后）
  - 写入 updatedAt = 今天（即使没有任何新动态，也用 --bump-only 刷新时间戳，保证“每天更新”）
用法：
  python _refresh_news.py            # 合并 _pending_news.json 并刷新时间戳
  python _refresh_news.py --bump-only # 无新动态时仅刷新 updatedAt
"""
import json, os, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
NEWS = os.path.join(BASE, "data", "brand-news.json")
PENDING = os.path.join(BASE, "_pending_news.json")
TODAY = datetime.date.today().strftime("%Y-%m-%d")

bump_only = "--bump-only" in sys.argv

with open(NEWS, encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", [])
existing = {(it.get("brand", ""), (it.get("title") or "").strip().lower()) for it in items}

maxn = 0
for it in items:
    iid = it.get("id", "")
    if iid.startswith("n") and iid[1:].isdigit():
        maxn = max(maxn, int(iid[1:]))

added = 0
if not bump_only and os.path.exists(PENDING):
    with open(PENDING, encoding="utf-8") as f:
        pend = json.load(f)
    for p in pend:
        key = (p.get("brand", ""), (p.get("title") or "").strip().lower())
        if key in existing:
            continue  # 去重：保留历史，不重复添加
        maxn += 1
        it = {
            "id": "n%d" % maxn,
            "brand": p["brand"],
            "category": p.get("category", "news"),
            "catLabel": p.get("catLabel", "动态"),
            "title": p["title"],
            "summary": p.get("summary", ""),
            "url": p.get("url", "#"),
            "source": p.get("source", ""),
            "date": p.get("date", TODAY),
        }
        items.append(it)
        existing.add(key)
        added += 1

data["items"] = items
data["updatedAt"] = TODAY
data["note"] = "每日 09:00（周一~周六）自动刷新；合并保留全部历史动态，未读新闻不会因更新而消失。"

with open(NEWS, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 同时刷新品牌新品监控的时间戳（保留各品牌 releaseDate，不改动）
STATUS = os.path.join(BASE, "data", "brand-status.json")
if os.path.exists(STATUS):
    with open(STATUS, encoding="utf-8") as f:
        sd = json.load(f)
    sd["updatedAt"] = TODAY
    with open(STATUS, "w", encoding="utf-8") as f:
        json.dump(sd, f, ensure_ascii=False, indent=2)

print("updatedAt=%s | 总条数=%d | 本次新增=%d" % (TODAY, len(items), added))
