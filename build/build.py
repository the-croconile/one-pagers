#!/usr/bin/env python3
"""Generate the Croconile one-pager site into ../site."""
import html, os, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent
TM = "&trade;"

ICONS = {
 "chart": '<path d="M4 20V4M4 20h16M9 16v-5M13 16V8M17 16v-3"/>',
 "bot": '<rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M3 13v2M21 13v2"/>',
 "compass": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
 "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
 "swap": '<path d="M7 7h12l-3-3M17 17H5l3 3"/>',
 "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.5 3.5-5.5 6.5-5.5s5.5 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14.5c2 .7 3.2 2.5 3.8 5.5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5h6v2M3 12h18"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
 "sprout": '<path d="M12 21v-9M12 12c0-4-3-6-7-6 0 4 3 6 7 6zM12 14c0-3 2.5-5 6-5 0 3-2.5 5-6 5z"/>',
 "cap": '<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>',
 "book": '<path d="M4 4h6a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4zM20 4h-6a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h6z"/>',
 "building": '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7h.01M15 7h.01M9 11h.01M15 11h.01M9 15h.01M15 15h.01"/>',
 "idcard": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M14 10h4M14 14h4M6 16c.7-1.3 1.7-2 3-2s2.3.7 3 2"/>',
 "handshake": '<path d="m11 17 2 2a1.5 1.5 0 0 0 2-2M14 14l2.5 2.5a1.5 1.5 0 0 0 2-2L15 11l-3 1-2-2 3-3h3l4 4M3 11l4-4 3 1"/><path d="m7 15 2 2"/>',
 "screen": '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="m9 20 3-4 3 4"/>',
 "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
 "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "download": '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
}

def icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[name] + '</svg>')

PAGES = []  # (slug, nav title, card title, card blurb, pdf)

def shell(slug, title, description, body, pdf=None):
    cur = ' aria-current="page"'
    nav = "".join(
        f'<a href="{(s + ".html") if s != "index" else "./"}"{cur if s == slug else ""}>{n}</a>'
        for s, n, *_ in [("index", "All one-pagers")] + PAGES)
    pdf_btn = (f'<a class="pdf-link" href="pdf/{pdf}" download>{icon("download")} Download PDF</a>'
               if pdf else "")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta name="theme-color" content="#0e9a47">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./" aria-label="Croconile one-pagers home"><img src="assets/croconile-logo-sm.png" alt="Croconile" width="168" height="33"></a>
    <span class="mono tagline">Work intelligence, built from the work itself</span>
    {pdf_btn}
  </div>
</header>
<nav class="subnav" aria-label="One-pagers"><div class="wrap">{nav}</div></nav>
<main class="wrap">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <span>&copy; 2026 Croconile. <b>Proprietary and confidential.</b> WorkCard&trade;, DepthCard&trade; and Signal Space&trade; are trademarks of Croconile.</span>
    <span><b>Confidential:</b> Shareable with Permission</span>
  </div>
</footer>
</body>
</html>
"""

def h(black, green):
    return f'{black} <span class="g">{green}</span>'

def section_head(label, title):
    return f'<div class="section-head"><span class="label g">{label}</span><h2>{title}</h2></div>'

def hero(eyebrow, h1, intro, pull):
    eb = f'<span class="label g">{eyebrow}</span>' if eyebrow else ""
    return f"""<section class="hero">
  <div>{eb}<h1>{h1}</h1></div>
  <div class="hero-side"><p>{intro}</p><p class="pull">{pull}</p></div>
</section>"""

def breaks(items, numbered=False):
    out = []
    for it in items:
        lab = f'<span class="label g">{it[2]}</span>' if numbered else ""
        desc = f"<p>{it[1]}</p>" if it[1] else ""
        out.append(f'<div class="break">{lab}<h3>{it[0]}</h3>{desc}</div>')
    return '<div class="cols3">' + "".join(out) + "</div>"

def records(p):
    return f"""<div class="records">
  <div class="r-label"><span class="label">{p['pair']}</span><span class="label">Illustrative</span></div>
  <div class="r-old"><span class="label">{p['old_label']}</span>{p['old']}</div>
  <div class="arrow" aria-hidden="true">&rarr;</div>
  <div class="r-new"><span class="label">{p['new_label']}</span><div class="stat"><b>{p['stat']}</b><span>{p['stat_desc']}</span></div></div>
</div>"""

def steps(items, stack=False):
    out = []
    for i, it in enumerate(items, 1):
        tags = ""
        if len(it) > 2 and it[2]:
            tags = '<div class="tags">' + "".join(f'<span class="tag">{t}</span>' for t in it[2]) + "</div>"
        out.append(f'<div class="step"><h3><span class="n">0{i}</span>{it[0]}</h3><p>{it[1]}</p>{tags}</div>')
    return f'<div class="steps{" stack" if stack else ""}">' + "".join(out) + "</div>"

STATUS = {"Acknowledged": "ok", "Published": "ok", "Awaiting": "wait", "Writing": "wait"}

def person(name, role, status):
    k = STATUS.get(status, "none")
    cls = {"ok": "", "wait": "status-wait", "none": "status-none"}[k]
    return (f'<span class="person st st-{k}"><b>{name}</b> <span class="role">{role}</span>'
            f' <span class="sep">&middot;</span> <span class="{cls}">{status}</span></span>')

def workcard(c):
    def col(lbl, sub, text, box=False):
        s = f'<span class="sub">{sub}</span>' if sub else ""
        t = f'<p class="outcome-box">{text}</p>' if box else f"<p>{text}</p>"
        return f'<div><span class="label">{lbl}</span>{s}{t}</div>'
    subs = c.get("subs", [None, None, None])
    people = "".join(person(*x) for x in c["people"])
    return f"""<article class="workcard" aria-label="Example {c['kind']}">
  <div class="wc-top"><span class="wc-kind"><span class="dot"></span><span class="mono">{c['kind']}</span><span class="label">Example</span></span><span class="wc-meta">{c['meta']}</span></div>
  <h3 class="wc-title">{c['title']}</h3>
  <div class="sao">{col('Situation', subs[0], c['situation'])}{col('Action', subs[1], c['action'])}{col('Outcome', subs[2], c['outcome'], True)}</div>
  <div class="wc-row"><span class="label">{c.get('people_label', 'People who were in the room')}</span><div class="people">{people}</div></div>
  <div class="wc-row why"><span class="label">{c['why_label']}</span><p>{c['why']}</p></div>
</article>"""

def features(items):
    return "".join(f'<div class="feature"><div class="icon">{icon(i)}</div><div><h3>{t}</h3><p>{d}</p></div></div>'
                   for i, t, d in items)

def start_here(title, bullets):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return f"""<aside class="start"><span class="label g">Start here</span><h3>{title}</h3><ul>{lis}</ul>
<div class="foot"><span class="label">Free to start</span><a href="https://croconile.com">CROCONILE.COM</a></div></aside>"""

def profile(text):
    return f"""<div class="profile"><span class="mono">Your Croconile Profile</span><p>{text}</p>
<a href="https://croconile.com">See my work on Croconile <span>&rarr;</span></a></div>"""

def fromto(items):
    return '<div class="fromto">' + "".join(f"<div><span>{a}</span><b>{b}</b></div>" for a, b in items) + "</div>"

DEFAULT_PROFILE = "One link to the work you choose to share. Put it in your signature, your bio or your resume."
WHY_STD = "You write your account. <b>You can&rsquo;t write theirs.</b> Each account sits on its author&rsquo;s own record, never merged into yours."
FEAT_STD = [
 ("chart", "See what your work says you&rsquo;re good at", "The Work Intelligence Matrix maps the problems you&rsquo;ve solved, where you solved them, and how."),
 ("bot", "Built for Human + AI work", "Derived from real work&mdash;including where your judgment led and where AI accelerated the work."),
 ("compass", "See where your work is taking you next", "As your record deepens, patterns emerge&mdash;making your next best capabilities and roles visible."),
]

def persona_page(p):
    body = [hero(p["eyebrow"], p["h1"], p["intro"], p["pull"])]
    body.append(f'<section class="section">{section_head("Where it breaks", p["breaks_title"])}{breaks(p["breaks"])}{records(p["records"])}</section>')
    body.append(f'<section class="section">{section_head("How it works", p["how_title"])}{steps(p["steps"])}{workcard(p["card"])}</section>')
    body.append(f'<section class="section">{section_head("What it does for you", p["does_title"])}'
                f'<div class="does"><div>{features(p["features"])}</div>{start_here(*p["start"])}</div>'
                f'{profile(p.get("profile", DEFAULT_PROFILE))}{fromto(p["fromto"])}</section>')
    return "\n".join(body)

# ---------------------------------------------------------------- personas
PERSONAS = [
dict(slug="employed", nav="Employed", pdf="employed.pdf",
 card_title="Careers move. Your record moves with you.",
 blurb="For people in a role, exploring what&rsquo;s next. Journal your work while it&rsquo;s real.",
 eyebrow="For people in a role, exploring what&rsquo;s next",
 h1=h("Careers move.", "Your record moves with you."),
 intro="Journal your work while it&rsquo;s real. The record belongs to you, not your employer, and it compounds whether you&rsquo;re looking or not.",
 pull=h("The best records are built in the good times,", "not the desperate ones."),
 breaks_title=h("By review season,", "the context is gone."),
 breaks=[("Work evaporates between reviews.", "What made it matter rarely survives the review cycle."),
         ("Your history lives in your employer&rsquo;s systems.", "Leave, and the difference you made stays behind."),
         ("Nobody points to your next move.", "Reviews look back. Nothing tells you what to build next.")],
 records=dict(pair="Same work &middot; Two records", old_label="In the self-review",
   old="<q>Supported month-end close improvements across entities.</q>",
   new_label="WorkCard&trade; &middot; Example", stat="9 &rarr; 5", stat_desc="working days to close, across 14 entities"),
 how_title=h("Capture the work.", "Let the record compound."),
 steps=[("Capture", "Journal the work while it&rsquo;s fresh: the problem, your calls, what changed."),
        ("Acknowledge", "Colleagues who were there add their own account. No sign-off needed."),
        ("Compound", "Each card you add deepens the record, and it compounds for years."),
        ("Discover", "Get found for the work itself when you switch it on, without signaling that you&rsquo;re looking.")],
 card=dict(kind="WorkCard&trade;", meta="Ardent Foods &middot; Senior Financial Analyst &middot; 2026",
   title="Intercompany Close Exceptions Queue",
   situation="Month-end close took nine working days, most of it spent chasing 1,200 unmatched intercompany entries by hand.",
   action="Built a matching-rules layer and an exceptions queue owned by each entity. Directed an AI model to draft match suggestions, and set the rule that nothing posts automatically.",
   outcome="Close shortened from <b>nine working days to five</b> across 14 entities.",
   people=[("Grace Okafor", "Controller", "Acknowledged"), ("Tom&aacute;s Lind", "Entity accountant", "Awaiting")],
   why_label="Why it holds", why=WHY_STD),
 does_title=h("A capability map,", "revealed by real work."),
 features=FEAT_STD,
 start=("Start with something you did this quarter.",
        ["One WorkCard, five to eight minutes.", "Walk into your next review with evidence.",
         "Discoverable to recruiters only when you switch it on.", "Drafts stay private. You choose who sees each card."]),
 fromto=[("From fading memory", "to a living record"), ("From employer systems", "to your own record"), ("From AI-polished noise", "to authentic signals")]),

dict(slug="experienced-job-seekers", nav="Experienced job seekers", pdf="experienced-job-seekers.pdf",
 card_title="Your years deserve more than three bullets.",
 blurb="For experienced job seekers. Show the situation, the calls that were yours and what changed.",
 eyebrow="For experienced job seekers",
 h1=h("Your years deserve", "more than three bullets."),
 intro="Show the situation you walked into, the calls that were yours and what measurably changed. The people who were there add their own account of the same work.",
 pull=h("A resume says what you can do.", "A WorkCard shows what you did."),
 breaks_title=h("A decade of judgment,", "read as three lines of verbs."),
 breaks=[("Every search starts from zero.", "Nothing from your last search carries into the next one."),
         ("Every resume looks polished now.", "AI made the narrative cheap. Polish no longer earns trust."),
         ("Years flatten into bullets.", "The calls that were yours vanish into &ldquo;managed&rdquo; and &ldquo;led.&rdquo;")],
 records=dict(pair="Same work &middot; Two records", old_label="On the resume",
   old="<q>Managed carrier relationships and reduced freight costs.</q>",
   new_label="WorkCard&trade; &middot; Example", stat="&minus;11%", stat_desc="freight cost per shipment, year over year, with on-time delivery held at 96%"),
 how_title=h("One piece of work,", "several accounts."),
 steps=[("Capture", "Turn a decade of work into cards, one project at a time."),
        ("Acknowledge", "Colleagues who were there add their own account. No sign-off needed."),
        ("Compound", "Card by card, your years connect into a pattern others can read."),
        ("Discover", "Get read on evidence, not assertion, when you choose to be found.")],
 card=dict(kind="WorkCard&trade;", meta="Meridian Home Goods &middot; Senior Logistics Manager &middot; 2025",
   title="Lane-Level Freight Visibility",
   situation="Freight spend was reported as one monthly number. Nobody could see which of the 14 lanes were driving six straight quarters of increases.",
   action="Built a lane-level cost and on-time model from carrier invoices, ran a competitive rebid, and kept two incumbents where service data justified it.",
   outcome="Cost per shipment fell <b>11% year over year</b>, with on-time held at <b>96%</b>.",
   people=[("Priya Nand", "Transportation analyst", "Acknowledged"), ("Marcus Hale", "VP, Supply Chain", "Acknowledged")],
   why_label="Why it holds", why=WHY_STD),
 does_title=h("Your years,", "read as a pattern."),
 features=[("chart", "Compete on evidence, not polish", "Your decisions and outcomes, with accounts from the people who were there."),
           ("search", "Found by what you&rsquo;ve solved", "Matched on the problems behind your work, not keywords in a title."),
           ("clock", "Shorter time to trust", "Interviews move from &ldquo;can you do this?&rdquo; to &ldquo;walk me through this card.&rdquo;")],
 start=("Start with the work you&rsquo;d walk an interviewer through.",
        ["One WorkCard, five to eight minutes.", "Tag up to two people who were there.",
         "Open to recruiters only when you say so.", "Drafts stay private. You choose who sees each card."]),
 fromto=[("From three bullets", "to the whole story"), ("From assertion", "to acknowledgment"), ("From starting over", "to building on it")]),

dict(slug="first-time-job-seekers", nav="First-time job seekers", pdf="first-time-job-seekers.pdf",
 card_title="No experience doesn&rsquo;t mean no evidence.",
 blurb="For first-time job seekers. Your capstone, internship and hackathon work already happened.",
 eyebrow="For first-time job seekers",
 h1=h("No experience doesn&rsquo;t", "mean no evidence."),
 intro="Your capstone, internship and hackathon work already happened. Capture it as a WorkCard, and the people who were there add their own accounts.",
 pull=h("A transcript says you passed.", "A WorkCard shows what you built, and who was there."),
 breaks_title=h("Your first job shouldn&rsquo;t be", "your first evidence."),
 breaks=[("Grades don&rsquo;t show the work.", "A transcript never says what you built, or who you built it with."),
         ("Group work hides your part.", "One grade, split five ways. Nobody can tell which calls were yours."),
         ("Entry-level roles ask for experience.", "The projects you&rsquo;ve already done rarely count as any.")],
 records=dict(pair="Same project &middot; Two records", old_label="On the transcript",
   old="<em>IE 491 &middot; Capstone &middot; A&minus;</em>",
   new_label="WorkCard&trade; &middot; Example", stat="40 &rarr; 11", stat_desc="last-minute shift swaps a week, across 120 student staff"),
 how_title=h("Capture the project.", "The people who were there add theirs."),
 steps=[("Capture", "Capture your capstone while it&rsquo;s fresh: your part and the result."),
        ("Acknowledge", "Teammates add their own account of the project. No sign-off needed."),
        ("Compound", "Every project, internship and hackathon adds depth to one record."),
        ("Discover", "Get found for what you built, not your GPA, when you choose.")],
 card=dict(kind="WorkCard&trade;", meta="Harlow State University &middot; Capstone, Industrial Engineering &middot; 2026",
   title="Shift Scheduler for Campus Dining",
   situation="Weekly schedules for 120 student staff were built by hand, and roughly 40 shifts a week were swapped at the last minute.",
   action="Built an availability intake and a constraint-based scheduler, then ran a two-week pilot with the dining managers.",
   outcome="Last-minute swaps fell from <b>about 40 a week to 11</b> across 120 student staff.",
   people=[("Dev Raman", "Teammate", "Acknowledged"), ("Lena Ortiz", "Dining operations lead", "Awaiting"),
           ("Prof. R. Mendes", "Guide, tagged", "Not an author")],
   why_label="Why it holds", why=WHY_STD),
 does_title=h("One record,", "from the first project on."),
 features=[("clock", "Capture it while it&rsquo;s fresh", "Written now, not pieced together during interview prep."),
           ("users", "The people who were there add theirs", "Tag up to two teammates or a supervisor, or up to five on a guided project."),
           ("chart", "Read on outcomes, not a GPA", "When you&rsquo;re found, it&rsquo;s for what you did.")],
 start=("Start with the one project you&rsquo;re proudest of.",
        ["One WorkCard, five to eight minutes.", "Then tag up to two people who were there.",
         "Open to recruiters only when you say so.", "Drafts stay private. You choose who sees each card."]),
 fromto=[("From transcripts", "to records"), ("From a group grade", "to your own account"), ("From &ldquo;no experience&rdquo;", "to first evidence")]),

dict(slug="leaders-and-managers", nav="Leaders and managers", pdf="leaders-and-managers.pdf",
 card_title="You made the calls. The org chart took the credit.",
 blurb="For leaders and managers. Record the calls you made under constraint, in your words and your team&rsquo;s.",
 eyebrow="For leaders and managers",
 h1=h("You made the calls.", "The org chart took the credit."),
 intro="Leaders do real work too. Record the calls you made under constraint, in your words and your team&rsquo;s. It outlasts every reorg.",
 pull=h("Headcount is a line on a chart.", "Judgment is a record."),
 breaks_title=h("The work shipped.", "The calls behind it vanished."),
 breaks=[("Reorgs erase the record.", "New boxes, new lines, and the history of decisions goes with them."),
         ("Your wins get credited to &ldquo;the team.&rdquo;", "The outcome is on the slide. The decisions that shaped it are not."),
         ("Your judgment on AI leaves no trace.", "What you checked before anything shipped isn&rsquo;t in any report.")],
 records=dict(pair="Same work &middot; Two records", old_label="In the quarterly deck",
   old="<q>Customer Ops consolidated the regional desks. Great team effort.</q>",
   new_label="WorkCard&trade; &middot; Example", stat="3.2 &rarr; 1.4", stat_desc="handoffs per case, with first-contact resolution up from 58% to 71%"),
 how_title=h("Your calls,", "in your team&rsquo;s words too."),
 steps=[("Capture", "Record the calls you made under constraint, and why you made them."),
        ("Acknowledge", "Your team and peers add their own accounts. No sign-off needed."),
        ("Compound", "The record survives every reorg, every move and every new title."),
        ("Discover", "Your judgment, visible beyond the org chart whenever you choose.")],
 card=dict(kind="WorkCard&trade;", meta="Kestrel Mutual &middot; Director, Customer Operations &middot; 2025",
   title="One Queue for Three Regional Desks",
   situation="Three regional desks ran separate queues and tools. The same case was often routed up to four times before anyone owned it.",
   action="Merged the desks into one queue with shared triage rules. Decided which calls to push down to team leads. Let AI draft the routing, and kept people on every escalation.",
   outcome="Handoffs per case fell from <b>3.2 to 1.4</b>. First-contact resolution rose from 58% to 71%.",
   people=[("Aisha Bello", "Team lead, Southeast desk", "Acknowledged"), ("Ron Whitaker", "VP, Service Operations", "Awaiting")],
   why_label="Tagged by someone on your team?",
   why="Your account of her WorkCard takes about ten minutes. <b>It isn&rsquo;t a favor.</b> It stays on her record, and it starts yours."),
 does_title=h("A record that", "survives the reorg."),
 features=[("flag", "Keep the record of your calls", "The decisions you made, not the headcount you held."),
           ("swap", "Write accounts for your team", "Specific and attributed. It stays on their record and on yours."),
           ("bot", "Record your judgment on AI", "What you directed, where you stopped it and what you checked.")],
 start=("Start with the call you&rsquo;d defend in any room.",
        ["One WorkCard, five to eight minutes.", "Then write an account for someone on your team.",
         "Open to recruiters only when you say so.", "Drafts stay private. You choose who sees each card."]),
 fromto=[("From the org chart", "to the record"), ("From &ldquo;the team&rdquo;", "to attributed calls"), ("From review cycles", "to a lasting record")]),

dict(slug="professors-and-trainers", nav="Professors and trainers", pdf="professors-and-trainers.pdf",
 card_title="Your impact lives in other people&rsquo;s work.",
 blurb="For professors and trainers. Set up a project once and invite up to five students or trainees.",
 eyebrow="For professors and trainers",
 h1=h("Your impact lives in", "other people&rsquo;s work."),
 intro="Set up a project once and invite up to five students or trainees. The WorkCards they write become the record of what your guidance produced.",
 pull=h("A CV lists what you advised.", "Their work shows what it produced."),
 breaks_title=h("Mentorship ends with the term.", "So does the record of it."),
 breaks=[("Student work ends at the grade.", "The problem, the outcome and the partner fade into a letter grade."),
         ("Reference letters are rebuilt from memory.", "Every recommendation season starts from a blank page."),
         ("Your guidance leaves no trace of its own.", "A CV counts the projects you advised, not what they changed.")],
 records=dict(pair="Same career &middot; Two records", old_label="On the CV",
   old="<q>Capstone advisor.</q>",
   new_label="Guided Work &middot; Example", stat="28", stat_desc="WorkCards by 21 students on eight projects. None written by you."),
 how_title=h("Set it up once.", "Every student writes their own."),
 steps=[("Set up", "Name the project and write its Situation once, for every card."),
        ("Invite", "Invite up to five students or trainees to each project you guide."),
        ("Compound", "Each writes independently. Together, they compound into one DepthCard."),
        ("Carry", "Your Guided Work record grows with every WorkCard, term after term.")],
 card=dict(kind="Guided project", meta="Ridgeway College &middot; Senior Capstone &middot; Spring 2026",
   title="Enrollment Forecast for Course Scheduling",
   subs=["Written once by you, inherited by every card", "Written by each student, never prefilled", "As the students report it"],
   situation="Section counts were copied from the year before, and about 30 sections a term opened badly over- or under-filled.",
   action="Five accounts of one project: the data cleanup, the model, the registrar&rsquo;s sign-off, the pilot and the handover.",
   outcome="Badly filled sections fell from <b>about 30 a term to 9</b> in the first fall.",
   people_label="Invited to this project &middot; 5 of 5",
   people=[("Amara Osei", "Forecasting model", "Published"), ("Jonah Pierce", "Data cleanup", "Published"),
           ("Sof&iacute;a Mar&iacute;n", "Registrar liaison", "Published"), ("Leo Brandt", "Pilot lead", "Writing"),
           ("Kiran Das", "Handover", "Invited")],
   why_label="Guided, not authored",
   why="You write the Situation. <b>You never write their accounts.</b> A contribution of yours counts only when the students&rsquo; own cards describe it."),
 does_title=h("Your guidance", "carries forward."),
 features=[("doc", "Letters written from evidence", "Dated, specific accounts for every project you&rsquo;ve guided."),
           ("user", "Mentorship on your own record", "Guided Work on your Profile: the projects, the people and what changed."),
           ("clock", "Minutes per project", "Set it up once. Students do the writing. Nothing to post or maintain.")],
 start=("Start with the project you&rsquo;re guiding this term.",
        ["Set up the project and write its Situation.", "Invite up to five students or trainees.",
         "Each student chooses who sees their own card."]),
 profile="Your Guided Work and the cards you choose to share, behind one link. Put it in your signature, your bio or your CV.",
 fromto=[("From a line on a CV", "to a guided record"), ("From memory", "to evidence"), ("From one term", "to a career")]),

dict(slug="students-and-trainees", nav="Students and trainees", pdf="students-and-trainees.pdf",
 card_title="The people who were there, already named.",
 blurb="For students and trainees. Your guide sets up the project; you write your part.",
 eyebrow="For students and trainees",
 h1=h("The people who were there,", "already named."),
 intro="Your professor or trainer sets up the project and names your collaborators, up to five. You write your part. They write theirs.",
 pull=h("A group grade hides your part.", "Five accounts show it."),
 breaks_title=h("Team projects end as", "one grade for five people."),
 breaks=[("Teammates scatter when the term ends.", "By the time you need their account, they&rsquo;ve moved on."),
         ("One grade, split five ways.", "Nobody reading it can tell which calls were yours."),
         ("Every cohort shows the same project.", "Portfolios look alike. Nothing shows who did what.")],
 records=dict(pair="Same project &middot; Two records", old_label="On the certificate",
   old="<em>Analytics Cohort &middot; Pass</em>",
   new_label="WorkCard&trade; &middot; Example", stat="33% &rarr; 8%", stat_desc="of help-desk tickets misrouted, over a four-week pilot"),
 how_title=h("Your guide sets it up.", "You write your part."),
 steps=[("Join", "Accept your guide&rsquo;s invite. Your teammates are already tagged on it."),
        ("Capture", "The Situation is set. Write your own Action and Outcome."),
        ("Compound", "Each writes their part. Together, they compound into one DepthCard."),
        ("Carry", "Your record goes with you past graduation, into every job after.")],
 card=dict(kind="WorkCard&trade;", meta="Harbor Tech Institute &middot; Data Analytics Cohort &middot; 2026",
   title="Help-Desk Ticket Routing for a City Library System",
   subs=["Set by your guide, shared by the team", "Yours alone", "As you report it"],
   situation="The library&rsquo;s help desk received about 1,400 tickets a month by email, and one in three went to the wrong team first.",
   action="Built the labeling set from six months of closed tickets. Let a model suggest the route, and wrote the rule for when a ticket goes to a person instead.",
   outcome="Misrouted tickets fell from <b>1 in 3 to 1 in 12</b> over a four-week pilot.",
   people=[("Ava Chen", "Data cleanup", "Acknowledged"), ("Marcus Bell", "Pilot lead", "Acknowledged"),
           ("Rosa Delgado", "Library liaison", "Awaiting"), ("Theo Nguyen", "Testing", "Awaiting"),
           ("D. Varga", "Trainer, guide", "Not an author")],
   why_label="Why it holds",
   why="Your guide sets the shared Situation. <b>Your Action and Outcome are yours alone</b>, and each teammate&rsquo;s account sits on their own record."),
 does_title=h("Your work", "carries forward."),
 features=[("users", "Collaborators, already identified", "Up to five, named by your guide. No chasing anyone after the term."),
           ("user", "Your part, not the group&rsquo;s", "Each teammate writes their own card, so your calls stay yours."),
           ("arrow", "A record before your first job", "It carries into every job after. It doesn&rsquo;t reset at graduation.")],
 start=("Accept the invite and write your part.",
        ["One WorkCard, five to eight minutes.", "No guide? Start solo and tag up to two.",
         "Open to recruiters only when you say so.", "Drafts stay private. You choose who sees each card."]),
 fromto=[("From a group grade", "to five accounts"), ("From chasing teammates", "to named collaborators"), ("From a certificate", "to a record")]),
]

# ---------------------------------------------------------------- overview pages
WHY_ALL = [("The project ends. <span class=\"g\">What you did starts to fade.</span>", "Teams move on. Context goes with them.", "01 &middot; Memory problem"),
           ("AI can polish the story. <span class=\"g\">It can&rsquo;t show the work.</span>", "When every resume reads well, none of them stands out.", "02 &middot; Signal problem"),
           ("Human + AI work <span class=\"g\">blurs who did what.</span>", "Titles can&rsquo;t show the judgment behind the outcome.", "03 &middot; Capability problem")]
FROMTO_ALL = [("From fading memory", "to a living record"), ("From employer systems", "to your own record"), ("From AI-polished noise", "to authentic signals")]

def mini_people():
    return """<div class="people-list">
<div class="pl"><span class="st st-ok"><b>Grace Okafor</b><small>Controller</small></span><span>Acknowledged</span></div>
<div class="pl"><span class="st st-wait"><b>Tom&aacute;s Lind</b><small>ERP Engineer</small></span><span class="status-wait">Awaiting</span></div>
</div>"""

def diagram():
    lanes = [("briefcase", "Employed", "Building a record in role", "employed"),
             ("search", "Experienced Job Seeker", "Years of work, told in full", "experienced-job-seekers"),
             ("sprout", "First-Time Job Seeker", "Projects as first evidence", "first-time-job-seekers"),
             ("flag", "Leader / Manager", "Calls made under constraint", "leaders-and-managers"),
             ("cap", "Guide", "Professor or trainer", "professors-and-trainers"),
             ("book", "Learner", "Student or trainee", "students-and-trainees")]
    ctx = [("building", "Employment", "Salaried or hourly role"), ("idcard", "Internship", "Supervised placement"),
           ("handshake", "Client", "Freelance or contract"), ("book", "Academic", "Course or research"),
           ("screen", "Training", "Cohort or bootcamp"), ("users", "Community", "Volunteer or society"),
           ("bulb", "Personal", "Self-initiated project"), ("bolt", "Hackathon", "Competition or challenge")]
    lane_html = "".join(f'<a class="lane" href="{s}.html" style="text-decoration:none">{icon(i)}<div><b>{t}</b><span>{d}</span></div></a>' for i, t, d, s in lanes)
    ctx_html = "".join(f'<div class="lane{" active" if n == 0 else ""}">{icon(i)}<div><b>{t}</b><span>{d}</span></div></div>' for n, (i, t, d) in enumerate(ctx))
    avatar = '<svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="40" r="22" fill="#0e9a47"/><path d="M18 108c4-28 22-42 42-42s38 14 42 42z" fill="#0e9a47"/></svg>'
    return f"""<div class="diagram">
<div><span class="label col-head">Who &middot; Six lanes</span><div class="lanes">{lane_html}</div></div>
<div class="user-hub"><span class="label col-head">The Croconile user</span><div class="avatar">{avatar}</div><h3>Croconile User</h3><p>One person &middot; one portable record</p><span class="mono writes">Writes &rarr;</span></div>
<div><span class="label col-head">What they capture</span><div class="mini-card">
 <div class="wc-top"><span class="wc-kind"><span class="dot"></span><span class="mono">WorkCard&trade;</span></span><span class="label">Example</span></div>
 <div class="meta">Senior Financial Analyst &middot; 2026</div><h4>Intercompany Close Queue</h4>
 <span class="label">Situation</span><p>Month-end close took nine days, chasing 1,200 entries by hand.</p>
 <span class="label">Action</span><p>Built matching rules and an exceptions queue per entity.</p>
 <span class="label">Outcome</span><p class="outcome-box">Close cut from <b>nine days to five</b></p>
 {mini_people()}
 <div style="margin-top:10px"><span class="label" style="display:inline">Context</span><span class="ctx-tag mono">Employment</span></div>
</div></div>
<div><span class="label col-head">Where &middot; Eight contexts</span><div class="lanes">{ctx_html}</div></div>
</div>"""

def matrix():
    rows = [("Manual Overload", ["l3", "l1", "l1", "l3", ""], ["3", "1", "1", "3", ""]),
            ("Limited Visibility", ["l1", "l1", "l2", "", ""], ["1", "1", "2", "", ""]),
            ("Slow Turnaround", ["stated", "", "", "", "stated"], ["1", "", "", "", "1"])]
    body = "".join("<tr><th class=\"row\" scope=\"row\">" + r + "</th>" +
                   "".join(f'<td class="{c}">{v}</td>' for c, v in zip(cls, vals)) + "</tr>" for r, cls, vals in rows)
    return f"""<div class="matrix">
<div class="m-top"><span class="label">Work Intelligence Matrix</span><span class="label">Illustrative</span></div>
<table>
<thead>
<tr class="grp"><th></th><th colspan="2" scope="colgroup">WHERE</th><th colspan="3" scope="colgroup">HOW</th></tr>
<tr><th class="row"><span class="label">Problem &darr;</span></th><th scope="col">Close</th><th scope="col">Treasury</th><th scope="col">Build</th><th scope="col">Automate</th><th scope="col">Govern</th></tr>
</thead>
<tbody>{body}</tbody>
</table>
<div class="m-note"><span class="label">Not there yet</span><span>Govern &middot; no acknowledged work yet</span></div>
<div class="legend"><span><i class="l1" style="background:#c3e7bc"></i>1</span><span><i style="background:#86d07c"></i>2</span><span><i style="background:#47b83e"></i>3</span><span><i style="background:#128a1f"></i>4+</span><span><i style="border:1.5px dashed #9a9a9a"></i>Stated</span><span><i></i>None</span></div>
</div>"""

def all_page():
    b = [hero("A work intelligence platform for the AI era",
              h("Your best work shouldn&rsquo;t disappear", "when the project ends."),
              "Capture your work as WorkCards. The people who were there add their own perspectives, creating a record no one person could write alone. Over time, every record compounds, revealing patterns in problems solved, capabilities demonstrated, and outcomes achieved across people, roles, companies, and domains.",
              h("AI-polished narratives are everywhere.", "Credible work signals are scarce."))]
    b.append(f'<section class="section">{section_head("Why", h("Three problems. One cause:", "real work becomes invisible."))}{breaks(WHY_ALL, numbered=True)}</section>')
    b.append(f'<section class="section">{section_head("The record", h("Any kind of real work.", "One record."))}{diagram()}</section>')
    b.append(f'<section class="section">{section_head("How it works", h("Capture the work.", "Let the record compound."))}' + steps([
        ("Capture", "Journal the work while it&rsquo;s fresh: the problem, your calls, what changed."),
        ("Acknowledge", "The people who were there add their own account. No sign-off needed."),
        ("Compound", "WorkCards join into a DepthCard&trade;. Each of you saw a different part."),
        ("Discover", "Get found for the work itself, only when you switch it on.")]) + "</section>")
    b.append(f'<section class="section">{section_head("What it does for you", h("A capability map,", "revealed by real work."))}'
             f'<div class="does does-matrix"><div>{features(FEAT_STD)}</div>{matrix()}</div>'
             f'{profile(DEFAULT_PROFILE)}{fromto(FROMTO_ALL)}</section>')
    return "\n".join(b)

def all_v2_page():
    why = [(t, None, l) for t, _, l in WHY_ALL]
    strip = f"""<div class="wc-strip">
<div><span class="wc-kind"><span class="dot"></span><span class="mono">WorkCard&trade;</span><span class="label">Example</span></span><div class="meta" style="margin-top:8px">Senior Financial Analyst &middot; 2026</div><h4>Intercompany Close Queue</h4></div>
<div><span class="label">Situation</span><p>Month-end close took nine days, chasing 1,200 entries by hand.</p></div>
<div><span class="label">Action</span><p>Built matching rules and an exceptions queue per entity.</p></div>
<div><span class="label">Outcome</span><p class="outcome-box">Close cut from <b>nine days to five</b></p></div>
<div><span class="label">The people who were there</span>
<div class="pl"><span class="st st-ok"><b>Grace Okafor</b><small>Controller</small></span><span>Acknowledged</span></div>
<div class="pl"><span class="st st-wait"><b>Tom&aacute;s Lind</b><small>ERP Engineer</small></span><span class="status-wait">Awaiting</span></div></div>
</div>"""
    b = [hero(None, h("Your best work shouldn&rsquo;t disappear", "when the project ends."),
              "Capture your work as WorkCards. The people who were there add their own perspectives, creating a record no one person could write alone.",
              h("AI-polished narratives are everywhere.", "Credible work signals are scarce."))]
    b.append(f'<section class="section">{section_head("Why", h("Three problems. One cause:", "real work becomes invisible."))}{breaks(why, numbered=True)}</section>')
    b.append(f'<section class="section">{section_head("The record", h("Any kind of real work.", "One record."))}{strip}</section>')
    b.append(f'<section class="section">{section_head("How it works", h("Capture the work.", "Let the record compound."))}' + steps([
        ("Capture", "Journal the work while it&rsquo;s fresh: the problem, your calls, what changed.", ["WorkCard&trade;"]),
        ("Acknowledge", "The people who were there add their own account. No sign-off needed.", ["Collaborators&rsquo; own WorkCards"]),
        ("Compound", "WorkCards join into a DepthCard. Each of you saw a different part.", ["DepthCard&trade;"]),
        ("Discover", "Get found for the work itself. You choose who sees each card.", ["Signal Space&trade;", "Croconile Profile"])], stack=True) + "</section>")
    b.append(f'<section class="section">{section_head("What it does for you", h("A capability map,", "revealed by real work."))}'
             f'<div class="features-row">{features(FEAT_STD)}</div>{profile(DEFAULT_PROFILE)}{fromto(FROMTO_ALL)}</section>')
    return "\n".join(b)

def hub_page():
    cards = []
    for slug, nav, title, blurb, pdf in PAGES:
        feat = " featured" if slug == "croconile-for-all" else ""
        cards.append(f'<a class="hub-card{feat}" href="{slug}.html"><span class="label g">{nav}</span><h3>{title}</h3><p>{blurb}</p><span class="go">Read the one-pager &rarr;</span></a>')
    pdfs = "".join(f'<a class="pdf-link" href="pdf/{pdf}" download>{icon("download")} {nav}</a>' for _, nav, _, _, pdf in PAGES)
    return f"""{hero("Croconile one-pagers", h("Work intelligence,", "built from the work itself."),
      "One record of real work, told by the people who were there. Pick the one-pager that fits your audience, read it on the web, or download the original PDF.",
      h("AI-polished narratives are everywhere.", "Credible work signals are scarce."))}
<section class="section">{section_head("One-pagers", h("One platform.", "A page for every audience."))}<div class="hub-grid">{''.join(cards)}</div></section>
<section class="section">{section_head("Downloads", h("Original", "print-ready PDFs."))}<div style="display:flex;flex-wrap:wrap;gap:10px">{pdfs}</div></section>"""

def main():
    PAGES.append(("croconile-for-all", "Croconile for All", "Your best work shouldn&rsquo;t disappear when the project ends.",
                  "The full overview: why real work becomes invisible, the six lanes and eight contexts, and the Work Intelligence Matrix.", "croconile-for-all.pdf"))
    PAGES.append(("croconile-for-all-v2", "Croconile for All (v2)", "Your best work shouldn&rsquo;t disappear when the project ends.",
                  "The condensed overview: three problems, one WorkCard, four steps and the capability map.", "croconile-for-all-v2.pdf"))
    for p in PERSONAS:
        PAGES.append((p["slug"], p["nav"], p["card_title"], p["blurb"], p["pdf"]))
    plain = lambda s: html.unescape(s).replace("\u2019", "'")
    files = {
        "index": ("Croconile One-Pagers", "Croconile one-pagers: work intelligence, built from the work itself.", hub_page(), None),
        "croconile-for-all": ("Croconile for All | Croconile", "Your best work shouldn't disappear when the project ends.", all_page(), "croconile-for-all.pdf"),
        "croconile-for-all-v2": ("Croconile for All (v2) | Croconile", "Your best work shouldn't disappear when the project ends.", all_v2_page(), "croconile-for-all-v2.pdf"),
    }
    for p in PERSONAS:
        files[p["slug"]] = (f"{plain(p['nav'])} | Croconile", plain(p["card_title"]), persona_page(p), p["pdf"])
    for slug, (title, desc, body, pdf) in files.items():
        (OUT / f"{slug}.html").write_text(shell(slug, title, desc, body, pdf), encoding="utf-8")
        print("wrote", slug)

if __name__ == "__main__":
    main()
