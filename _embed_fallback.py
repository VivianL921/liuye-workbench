#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把当前 data/brand-news.json 与 data/brand-status.json 的内容，
重新注入 index.html 的内联兜底常量 NEWS_FALLBACK / BRAND_STATUS_FALLBACK。
用途：用户常双击本地 HTML（file://）打开，浏览器拦截 fetch，
此时页面会退回使用内联兜底；必须让兜底数据保持与线上一致，
否则离线打开会显示旧日期（这正是用户看到 8/4/8/5 的根因）。
"""
import json, re, os

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "index.html")
NEWS = os.path.join(BASE, "data", "brand-news.json")
STATUS = os.path.join(BASE, "data", "brand-status.json")

news = json.load(open(NEWS, encoding="utf-8"))
status = json.load(open(STATUS, encoding="utf-8"))

news_js = json.dumps(news, ensure_ascii=False)
status_js = json.dumps(status, ensure_ascii=False)

h = open(HTML, encoding="utf-8").read()

def repl_const(h, name, val):
    pat = re.compile(r'^const ' + re.escape(name) + r' = .*$', re.M)
    new_h, n = pat.subn('const ' + name + ' = ' + val + ';', h, count=1)
    return new_h, n

h, n1 = repl_const(h, "NEWS_FALLBACK", news_js)
h, n2 = repl_const(h, "BRAND_STATUS_FALLBACK", status_js)

if n1 != 1 or n2 != 1:
    raise SystemExit("替换失败：NEWS_FALLBACK 命中 %d 处，BRAND_STATUS_FALLBACK 命中 %d 处（期望各 1）" % (n1, n2))

open(HTML, "w", encoding="utf-8").write(h)
print("已注入兜底：NEWS_FALLBACK updatedAt=%s 条数=%d | BRAND_STATUS_FALLBACK updatedAt=%s 品牌=%d"
      % (news.get("updatedAt"), len(news.get("items", [])), status.get("updatedAt"), len(status.get("brands", {}))))
