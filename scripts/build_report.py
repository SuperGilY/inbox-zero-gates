#!/usr/bin/env python3
"""Build a self-contained HTML triage report from a JSON file.

Usage:  python3 build_report.py groups.json report.html

JSON shape (see examples/example-groups.json):
{
  "title": "...", "account": "...", "lang": "en" | "he",
  "inbox_now": 1234, "inbox_start": 5000,
  "groups": [ {"action": "trash|label|keep|decide", "title": "...",
               "count": "~120", "description": "...", "query": "..."} ],
  "keep": ["..."], "unknown": ["..."]
}
The output has no external dependencies and works on a phone.
"""
import html
import json
import sys

L = {
    "en": {
        "dir": "ltr", "now": "In inbox now", "start": "At the start", "done": "Done",
        "groups": "groups", "copy": "Copy query", "copied": "Copied", "select": "Selected - press Ctrl+C",
        "mark": "Done", "threads": "threads", "keep": "Stays in the inbox",
        "unknown": "What is not known", "trash": "Trash", "label": "Label, then archive",
        "keepb": "Keep", "decide": "Your call",
        "how": "Paste the query in Gmail, select all, then choose Select all conversations that match this search.",
    },
    "he": {
        "dir": "rtl", "now": "בתיבה עכשיו", "start": "בתחילת העבודה", "done": "הושלמו",
        "groups": "קבוצות", "copy": "העתקת שאילתה", "copied": "הועתק", "select": "סומן - Ctrl+C",
        "mark": "עשיתי", "threads": "שיחות", "keep": "נשאר בתיבה",
        "unknown": "מה לא ידוע", "trash": "לאשפה", "label": "לתיוג ואז לארכיון",
        "keepb": "נשאר", "decide": "החלטה שלך",
        "how": "מדביקים את השאילתה ב-Gmail, בוחרים הכל ולוחצים על ״בחר את כל השיחות התואמות לחיפוש זה״.",
    },
}

CSS = """
:root{--bg:#f7f4ef;--fg:#2a2622;--mut:#7b746b;--card:#fff;--bd:#ece6dc;--trash:#e4604e;--trashb:#fdeeea;
--label:#3e7bb0;--labelb:#e8f1f8;--decide:#d4961c;--decideb:#fcf3df;--keep:#3f9c73;--keepb:#e6f5ee;--sh:0 2px 10px rgba(60,40,20,.07)}
@media(prefers-color-scheme:dark){:root{--bg:#171513;--fg:#f0ebe3;--mut:#a39b8f;--card:#221f1c;--bd:#35302b;
--trash:#ff8a78;--trashb:#3a2420;--label:#7db6e6;--labelb:#1f2d3a;--decide:#f0b84a;--decideb:#3a301a;--keep:#6dd0a2;--keepb:#1c3128;--sh:none}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:Heebo,system-ui,sans-serif;line-height:1.6;padding:20px 16px 60px}
.wrap{max-width:720px;margin:auto}
.hero{background:linear-gradient(135deg,#3f9c73,#3e7bb0);color:#fff;border-radius:22px;padding:24px;box-shadow:var(--sh)}
.hero h1{margin:0 0 4px;font-size:1.5rem;font-weight:800}.hero p{margin:0;opacity:.92}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:18px}
.stat{background:rgba(255,255,255,.18);border-radius:14px;padding:10px;text-align:center}
.stat b{display:block;font-size:1.4rem;font-weight:800}.stat span{font-size:.78rem;opacity:.9}
.bar{height:10px;background:rgba(255,255,255,.25);border-radius:9px;margin-top:16px;overflow:hidden}
.bar i{display:block;height:100%;width:0;background:#fff;border-radius:9px;transition:width .4s}
.how{color:var(--mut);font-size:.9rem;margin:14px 2px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:18px;padding:16px 18px;margin:12px 0;box-shadow:var(--sh);
border-inline-start:6px solid var(--trash);transition:.25s}
.card.label{border-inline-start-color:var(--label)}.card.decide{border-inline-start-color:var(--decide)}.card.keep{border-inline-start-color:var(--keep)}
.card.finished{opacity:.5}.card.finished h3{text-decoration:line-through}
.top{display:flex;justify-content:space-between;align-items:center}
.badge{font-size:.8rem;font-weight:700;padding:3px 12px;border-radius:99px;background:var(--trashb);color:var(--trash)}
.badge.label{background:var(--labelb);color:var(--label)}.badge.decide{background:var(--decideb);color:var(--decide)}.badge.keep{background:var(--keepb);color:var(--keep)}
.num{color:var(--mut);font-size:.9rem}.num b{color:var(--fg);font-size:1.15rem}
h3{margin:8px 0 2px;font-size:1.08rem;font-weight:700}.card p{margin:2px 0 8px;color:var(--mut);font-size:.93rem}
pre{cursor:pointer;background:var(--bg);border:1px solid var(--bd);border-radius:10px;padding:10px;white-space:pre-wrap;word-break:break-all;font-size:.76rem;text-align:left;margin:8px 0}
.actions{display:flex;justify-content:space-between;align-items:center;margin-top:10px;gap:10px}
button.copy{border:0;border-radius:12px;padding:10px 18px;font:700 .95rem Heebo,system-ui,sans-serif;cursor:pointer;background:var(--trash);color:#fff}
.label button.copy{background:var(--label)}.decide button.copy{background:var(--decide)}button.copy.ok{background:var(--keep)!important}
.done{display:flex;align-items:center;gap:8px;cursor:pointer;font-weight:500}.done input{display:none}
.box{width:26px;height:26px;border-radius:9px;border:2px solid var(--bd);display:grid;place-items:center;transition:.2s}
.done input:checked+.box{background:var(--keep);border-color:var(--keep)}.done input:checked+.box::after{content:"\\2713";color:#fff;font-weight:800}
h2{font-size:1.15rem;font-weight:800;margin:30px 0 8px}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{background:var(--keepb);color:var(--keep);border-radius:99px;padding:5px 14px;font-size:.88rem;font-weight:500}
.est{background:var(--card);border:1px dashed var(--bd);border-radius:16px;padding:14px 18px;color:var(--mut);font-size:.9rem}
.est ul{margin:0;padding-inline-start:20px}
"""

JS = """
function selq(p){var r=document.createRange();r.selectNodeContents(p);var g=getSelection();g.removeAllRanges();g.addRange(r)}
function cp(id,b){var p=document.querySelector('#'+id+' pre'),t=p.textContent,ok=false;
try{var ta=document.createElement('textarea');ta.value=t;ta.setAttribute('readonly','');ta.style.cssText='position:fixed;top:0;left:0;opacity:0';
document.body.appendChild(ta);ta.select();ta.setSelectionRange(0,99999);ok=document.execCommand('copy');document.body.removeChild(ta)}catch(e){}
function fin(v){if(v){b.classList.add('ok');b.textContent=T.copied}else{selq(p);b.textContent=T.select}
setTimeout(function(){b.classList.remove('ok');b.textContent=T.copy},2500)}
if(ok){fin(true)}else{try{navigator.clipboard.writeText(t).then(function(){fin(true)},function(){fin(false)})}catch(e){fin(false)}}}
function upd(){var a=document.querySelectorAll('input[data-k]'),n=0;
a.forEach(function(c){c.closest('.card').classList.toggle('finished',c.checked);if(c.checked)n++});
document.getElementById('p').textContent=n+'/'+a.length;document.getElementById('bar').style.width=(a.length?100*n/a.length:0)+'%'}
document.querySelectorAll('input[data-k]').forEach(function(c){
try{c.checked=localStorage.getItem(KEY+c.dataset.k)==='1'}catch(e){}
c.addEventListener('change',function(){try{localStorage.setItem(KEY+c.dataset.k,c.checked?'1':'0')}catch(e){}upd()})});upd();
"""


def esc(s):
    return html.escape(str(s), quote=True)


def card(i, g, t):
    action = g.get("action", "trash")
    if action not in ("trash", "label", "keep", "decide"):
        action = "trash"
    cid = "c%d" % i
    query = g.get("query", "")
    q_html = '<pre dir="ltr" onclick="selq(this)">%s</pre>' % esc(query) if query else ""
    btn = '<button class="copy" onclick="cp(\'%s\',this)">%s</button>' % (cid, esc(t["copy"])) if query else "<span></span>"
    check = ('<label class="done"><input type="checkbox" data-k="%d"><span class="box"></span>%s</label>' % (i, esc(t["mark"]))) if query else ""
    count = ('<span class="num"><b><bdi>%s</bdi></b> %s</span>' % (esc(g["count"]), esc(t["threads"]))) if g.get("count") else ""
    return (
        '<article class="card %s" id="%s"><div class="top"><span class="badge %s">%s</span>%s</div>'
        "<h3>%s</h3><p>%s</p>%s<div class=\"actions\">%s%s</div></article>"
        % (action, cid, action, esc(t.get(action if action != "keep" else "keepb", action)), count,
           esc(g.get("title", "")), esc(g.get("description", "")), q_html, btn, check)
    )


def build(cfg):
    lang = cfg.get("lang", "en")
    t = L.get(lang, L["en"])
    groups = cfg.get("groups", [])
    cards = "".join(card(i, g, t) for i, g in enumerate(groups))
    keep = "".join('<span class="chip">%s</span>' % esc(k) for k in cfg.get("keep", []))
    unknown = "".join("<li>%s</li>" % esc(u) for u in cfg.get("unknown", []))
    now = cfg.get("inbox_now", "-")
    start = cfg.get("inbox_start", "-")
    fmt = lambda v: "{:,}".format(v) if isinstance(v, int) else esc(v)
    key = "iz_" + esc(cfg.get("account", "x")) + "_"
    return (
        '<!doctype html><html lang="%s" dir="%s"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800&display=swap" rel="stylesheet">'
        "<style>%s</style></head><body><div class=\"wrap\">"
        '<div class="hero"><h1>%s</h1><p>%s</p><div class="stats">'
        '<div class="stat"><b>%s</b><span>%s</span></div><div class="stat"><b>%s</b><span>%s</span></div>'
        '<div class="stat"><b id="p">0/%d</b><span>%s</span></div></div><div class="bar"><i id="bar"></i></div></div>'
        '<p class="how">%s</p>%s'
        "%s%s</div><script>var T=%s,KEY=%s;%s</script></body></html>"
        % (esc(lang), t["dir"], esc(cfg.get("title", "Inbox zero")), CSS, esc(cfg.get("title", "Inbox zero")),
           esc(cfg.get("account", "")), fmt(now), esc(t["now"]), fmt(start), esc(t["start"]), len(groups),
           esc(t["done"]), esc(t["how"]), cards,
           ('<h2>%s</h2><div class="chips">%s</div>' % (esc(t["keep"]), keep)) if keep else "",
           ('<h2>%s</h2><div class="est"><ul>%s</ul></div>' % (esc(t["unknown"]), unknown)) if unknown else "",
           json.dumps({"copy": t["copy"], "copied": t["copied"], "select": t["select"]}, ensure_ascii=False),
           json.dumps(key), JS)
    )


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: build_report.py groups.json report.html")
    with open(sys.argv[1], encoding="utf-8") as f:
        cfg = json.load(f)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(build(cfg))
    print("wrote", sys.argv[2], "(%d groups)" % len(cfg.get("groups", [])))


if __name__ == "__main__":
    main()
