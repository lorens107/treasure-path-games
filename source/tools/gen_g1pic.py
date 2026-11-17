"""Builds the parts (strands) for the Grade 1 picture standards, all 10 LPs, and writes them into source/gx/g1.js.

Standards: 1.MD.A.2 (length), 1.MD.B.3 (time), 1.MD.C.4 (data), 1.G.A.3 (equal shares)
Run:  python3 source/tools/gen_g1pic.py
Figures are plain SVG strings stored with each part, so they always show (not tied to picture supports).
"""
import json, os, re, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N

G1 = N.G1
THEME, rng_for, nm, BAD = N.THEME, N.rng_for, N.nm, N.BAD
LET = "ABC"
INK = "#4a3b32"

CAT = {
    "1.MD.A.2": {
        "desc": "measuring length by laying shorter objects (length units) end to end",
        "parts": [
            ("express", "Say a length using a smaller object", "Express the length of an object using a smaller object as the unit"),
            ("linedup", "Line units up end to end", "Understand that units must line up end to end with no gaps or overlaps"),
            ("countunits", "Count the units that make the length", "Count the total number of units used to express the length"),
        ]},
    "1.MD.B.3": {
        "desc": "telling and writing time in hours and half-hours, on analog and digital clocks",
        "parts": [
            ("th_an", "Tell time in hours (analog clock)", "Tell time in hours using an analog clock"),
            ("th_dg", "Tell time in hours (digital clock)", "Tell time in hours using a digital clock"),
            ("tf_an", "Tell time in half-hours (analog clock)", "Tell time in half-hours using an analog clock"),
            ("tf_dg", "Tell time in half-hours (digital clock)", "Tell time in half-hours using a digital clock"),
            ("wh_an", "Write time in hours (analog clock)", "Write time in hours using an analog clock"),
            ("wh_dg", "Write time in hours (digital clock)", "Write time in hours using a digital clock"),
            ("wf_an", "Write time in half-hours (analog clock)", "Write time in half-hours using an analog clock"),
            ("wf_dg", "Write time in half-hours (digital clock)", "Write time in half-hours using a digital clock"),
        ]},
    "1.MD.C.4": {
        "desc": "organizing, representing, and interpreting data with up to three categories",
        "parts": [
            ("organize", "Organize information into groups", "Organize information into groups (up to 3)"),
            ("represent", "Represent data in a chart or graph", "Represent data in a chart or graph"),
            ("interpret", "Interpret the data in a graph", "Interpret the data in a chart or graph"),
            ("ask", "Ask questions about the data", "Ask questions about the data, such as how many in all, how many in each group, which group has more or less"),
            ("answer", "Answer questions about the data", "Answer questions about the data, such as how many in all, how many in each group, which group has more or less"),
        ]},
    "1.G.A.3": {
        "desc": "partitioning circles and rectangles into two and four equal shares",
        "parts": [
            ("partcircle", "Partition circles into 2 and 4 equal shares", "Partition circles into two and four equal shares (student draws the lines)"),
            ("partrect", "Partition rectangles into 2 and 4 equal shares", "Partition rectangles into two and four equal shares (student draws the lines)"),
            ("words", "Describe shares with halves, fourths, quarters", "Describe the shares using the words halves, fourths, and quarters"),
            ("phrases", "Use the phrases half of, fourth of, quarter of", "Use the phrases half of, fourth of, and quarter of when describing the shares"),
            ("whole", "Describe the whole as two of or four of the shares", "Describe the whole as two of, or four of the shares"),
            ("smaller", "More equal shares make smaller shares", "Show the knowledge that decomposing a shape into more equal shares creates smaller shares"),
        ]},
}

UNITS = ["cubes", "paper clips", "craft sticks", "tiles", "buttons", "blocks"]
THINGS = ["ribbon", "stick", "pencil", "crayon", "rope", "scarf", "leaf", "strip of paper"]


def svg(w, h, body, label):
    return '<svg viewBox="0 0 %d %d" width="%d" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (w, h, w, label, body)


def row(items):
    """items: list of (label, svgstring)"""
    cells = "".join('<div style="text-align:center"><div class="small" style="font-weight:700;margin-bottom:2px">%s</div>%s</div>' % (l, s) for l, s in items)
    return '<div style="display:flex;gap:22px;justify-content:center;flex-wrap:wrap;margin:10px 0">%s</div>' % cells


# ------------------------------------------------------------------ length
def length_fig(n, unit_w, col, mode="ok", gap_at=None, ov_at=None):
    w = n * unit_w + 20 if mode == "ok" else n * unit_w + 60
    h = 74
    x0 = 10
    body = '<rect x="%d" y="8" width="%d" height="20" rx="5" fill="#f3e3b3" stroke="%s" stroke-width="2"/>' % (x0, n * unit_w, INK)
    x = x0
    for i in range(n):
        if mode == "gap" and i == gap_at:
            x += 14
        if mode == "over" and i == ov_at:
            x -= 10
        body += '<rect x="%d" y="40" width="%d" height="20" rx="4" fill="%s" stroke="%s" stroke-width="2"/>' % (x, unit_w, col, INK)
        x += unit_w
    return svg(w, h, body, "An object with small units lined up under it")


def b_express(lp, r):
    col = THEME[lp][1]
    unit = UNITS[(lp + 0) % len(UNITS)]
    ns = r.sample(range(3, 10), 3)
    things = r.sample(THINGS, 3)
    figs = [(L + ": " + t, length_fig(n, 26, col)) for L, t, n in zip(LET, things, ns)]
    qs = ["The %s in picture %s is measured with %s. How long is it? Say it like this: it is __ %s long." % (t, L, unit, unit) for L, t in zip(LET, things)]
    key = ["%d %s long. The units go end to end under the %s with no gaps or overlaps." % (n, unit, t) for n, t in zip(ns, things)]
    return dict(qs=qs, key=key, dir="Look at the three pictures. Your teacher asks about one at a time. Say how long each thing is.", dur=100, html=row(figs))


def b_linedup(lp, r):
    col = THEME[lp][1]
    unit = UNITS[(lp + 2) % len(UNITS)]
    modes = ["ok", "gap", "over"]
    r.shuffle(modes)
    figs, qs, key = [], [], []
    for L, m in zip(LET, modes):
        n = r.randint(5, 8)
        thing = r.choice(THINGS)
        if m == "ok":
            f = length_fig(n, 26, col)
            key.append("Yes. The %s go end to end with no gaps and no overlaps, so the count is %d." % (unit, n))
        elif m == "gap":
            f = length_fig(n, 26, col, "gap", gap_at=r.randint(2, n - 2))
            key.append("No. There is a gap between two of the %s. They need to touch with no space between." % unit)
        else:
            f = length_fig(n, 26, col, "over", ov_at=r.randint(2, n - 2))
            key.append("No. Two of the %s overlap. They need to go end to end with no overlap." % unit)
        figs.append((L, f))
        qs.append("Look at picture %s. Is this a good way to measure with %s? Tell why or why not." % (L, unit))
    return dict(qs=qs, key=key, dir="Look at the three pictures. Your teacher asks about one at a time. Say if the units are lined up the right way.", dur=110, html=row(figs))


def b_countunits(lp, r):
    col = THEME[lp][1]
    unit = UNITS[(lp + 4) % len(UNITS)]
    ns = r.sample(range(9, 15), 3)
    figs = [(L, length_fig(n, 22, col)) for L, n in zip(LET, ns)]
    qs = ["Count the %s under object %s. How many are there? What number tells how long the object is?" % (unit, L) for L in LET]
    key = ["%d. The object is %d %s long. The total number of %s is its length." % (n, n, unit, unit) for n in ns]
    return dict(qs=qs, key=key, dir="Look at the three pictures. Count the units under each object. Say the total.", dur=110, html=row(figs))


# ------------------------------------------------------------------ time
HOURS12 = list(range(1, 13))


def clock_svg(h, half):
    cx = cy = 60
    body = '<circle cx="60" cy="60" r="54" fill="#fffaf0" stroke="%s" stroke-width="3"/>' % INK
    import math
    for k in range(1, 13):
        a = math.radians(k * 30)
        body += '<text x="%.1f" y="%.1f" font-size="12" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%d</text>' % (cx + 41 * math.sin(a), cy - 41 * math.cos(a) + 4, INK, k)
    ha = math.radians(((h % 12) + (0.5 if half else 0)) * 30)
    ma = math.radians(180 if half else 0)
    body += '<line x1="60" y1="60" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (cx + 24 * math.sin(ha), cy - 24 * math.cos(ha), INK)
    body += '<line x1="60" y1="60" x2="%.1f" y2="%.1f" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/>' % (cx + 37 * math.sin(ma), cy - 37 * math.cos(ma))
    body += '<circle cx="60" cy="60" r="4" fill="%s"/>' % INK
    return svg(120, 120, body, "An analog clock")


def digital_svg(h, half):
    t = "%d:%s" % (h, "30" if half else "00")
    body = '<rect x="4" y="4" width="112" height="52" rx="10" fill="#2b2b2b" stroke="%s" stroke-width="3"/>' % INK
    body += '<text x="60" y="42" font-size="30" font-weight="700" text-anchor="middle" fill="#9ef0a0" font-family="monospace">%s</text>' % t
    return svg(120, 60, body, "A digital clock")


def tstr(h, half):
    return "half past %d" % h if half else "%d o'clock" % h


def nstr(h, half):
    return "%d:%s" % (h, "30" if half else "00")


def b_time(kind, half, mode):
    """kind 'an' or 'dg', half bool, mode 'tell' or 'write'"""
    def f(lp, r):
        hs = r.sample(HOURS12, 3)
        words_h = N.ONES
        if mode == "write" and kind == "dg":
            # teacher says a time, student writes it the way a digital clock shows it
            qs = ["Write the time %s the way a digital clock shows it." % ("\"" + tstr(h, half).replace(str(h), words_h[h]) + "\"") for h in hs]
            key = ["%s. Look for the hour, a colon, then %s." % (nstr(h, half), "30" if half else "two zeros") for h in hs]
            return dict(qs=qs, key=key, dir="Listen to each time. Write it on your paper the way a digital clock shows it, with a colon.", dur=80, html=None)
        mk = clock_svg if kind == "an" else digital_svg
        figs = [(L, mk(h, half)) for L, h in zip(LET, hs)]
        if mode == "tell":
            qs = ["What time does clock %s show? Say the time out loud." % L for L in LET]
            if kind == "an":
                look = (lambda h: "The short hand is halfway between %d and %d and the long hand points to 6." % (h, h % 12 + 1)) if half else (lambda h: "The short hand points to %d and the long hand points to 12." % h)
            else:
                look = lambda h: "The display reads %s." % nstr(h, half)
            key = ["%s (%s). %s" % (tstr(h, half), nstr(h, half), look(h)) for h in hs]
            d = "Look at the three clocks. Your teacher asks about one at a time. Say the time out loud."
        else:
            qs = ["Write the time clock %s shows on your paper." % L for L in LET]
            key = ["%s. Look for the hour, a colon, then %s. Saying it as %s is also fine." % (nstr(h, half), "30" if half else "two zeros", tstr(h, half)) for h in hs]
            d = "Look at the three clocks. Write the time each one shows on your paper, with a colon."
        return dict(qs=qs, key=key, dir=d, dur=80, html=row(figs))
    return f


# ------------------------------------------------------------------ data
KINDS = [("circles", "circle", "#d9534f", "red"), ("squares", "square", "#4a90d9", "blue"), ("triangles", "triangle", "#3fa34d", "green")]
DSETS = [("Favorite pets", ["cats", "dogs", "fish"]), ("Favorite fruit", ["apples", "bananas", "grapes"]),
         ("Favorite snack", ["crackers", "cheese", "carrots"]), ("Weather this week", ["sunny", "rainy", "cloudy"]),
         ("Favorite color", ["red", "blue", "green"]), ("Favorite playground toy", ["swings", "slide", "sandbox"]),
         ("Favorite book", ["animals", "space", "trucks"]), ("Favorite season", ["summer", "winter", "spring"])]


def distinct_counts(r, k, lo=1, hi=8, total_max=16):
    while True:
        c = [r.randint(lo, hi) for _ in range(k)]
        if len(set(c)) == k and sum(c) <= total_max and sum(c) >= k + 3:
            return c


def shape_glyph(kind, x, y, col):
    if kind == "circle":
        return '<circle cx="%d" cy="%d" r="9" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, col, INK)
    if kind == "square":
        return '<rect x="%d" y="%d" width="18" height="18" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x - 9, y - 9, col, INK)
    return '<polygon points="%d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y - 10, x - 10, y + 8, x + 10, y + 8, col, INK)


def scatter_fig(counts, kinds, r):
    items = []
    for (pl, sg, col, cn), c in zip(kinds, counts):
        items += [(sg, col)] * c
    r.shuffle(items)
    cols = 6
    body = ""
    for i, (sg, col) in enumerate(items):
        x = 20 + (i % cols) * 34 + r.randint(-3, 3)
        y = 20 + (i // cols) * 34 + r.randint(-3, 3)
        body += shape_glyph(sg, x, y, col)
    rows = (len(items) + cols - 1) // cols
    return svg(20 + cols * 34, 14 + rows * 34, body, "A mix of colored shapes")


def bar_fig(title, cats, counts, col):
    w = 40 + len(cats) * 86
    mx = max(counts)
    h = 34 + mx * 22 + 30
    body = '<text x="%d" y="18" font-size="14" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (w // 2, INK, title)
    base = h - 26
    for i, (c, n) in enumerate(zip(cats, counts)):
        x = 30 + i * 86
        for k in range(n):
            body += '<rect x="%d" y="%d" width="60" height="20" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, base - (k + 1) * 22, col, INK)
        body += '<text x="%d" y="%d" font-size="13" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (x + 30, base + 18, INK, c)
    return svg(w, h, body, "A bar graph: " + title)


def b_organize(lp, r):
    figs, qs, key = [], [], []
    for i, L in enumerate(LET):
        k = 2 if i == 1 else 3
        kinds = r.sample(KINDS, k)
        counts = distinct_counts(r, k, 2, 7, 15)
        figs.append((L, scatter_fig(counts, kinds, r)))
        qs.append("Sort the shapes in picture %s into groups on your paper. How many groups are there, and how many are in each group?" % L)
        key.append("%d groups: %s. Look for groups sorted by one kind." % (k, ", ".join("%d %s %s" % (c, kd[3], kd[0]) for c, kd in zip(counts, kinds))))
    return dict(qs=qs, key=key, dir="Look at the three pictures. Sort the shapes into groups on your paper. Then tell your teacher about your groups.", dur=180, html=row(figs))


def b_represent(lp, r):
    sets = r.sample(DSETS, 3)
    qs, key = [], []
    for i, (title, cats) in enumerate(sets):
        k = 2 if i == 0 else 3
        cs = cats[:k] if k == 3 else r.sample(cats, 2)
        counts = distinct_counts(r, k, 1, 6, 12)
        lst = [c for c, n in zip(cs, counts) for _ in range(n)]
        r.shuffle(lst)
        qs.append("%s. Here are the answers: %s. Make a tally chart or a picture graph on your paper to show the data." % (title, ", ".join(lst)))
        key.append("%s. Look for %d labeled groups and the right number in each group." % (", ".join("%s %d" % (c, n) for c, n in zip(cs, counts)), k))
    return dict(qs=qs, key=key, dir="Listen to each set of answers. Show the answers in a tally chart or picture graph on your paper.", dur=210, html=None)


def graph_set(lp, r, n=3):
    sets = r.sample(DSETS, n)
    out = []
    for i, (title, cats) in enumerate(sets):
        k = 3 if i != 1 else 2
        cs = cats[:k] if k == 3 else r.sample(cats, 2)
        counts = distinct_counts(r, k, 1, 8, 18)
        out.append((title, cs, counts))
    return out


def b_interpret(lp, r):
    gs = graph_set(lp, r)
    col = THEME[lp][1]
    figs = [(L, bar_fig(t, c, n, col)) for L, (t, c, n) in zip(LET, gs)]
    (t1, c1, n1), (t2, c2, n2), (t3, c3, n3) = gs
    mx = c1[n1.index(max(n1))]; mn = c1[n1.index(min(n1))]
    qs = ["Look at graph A. Which group has the most? Which group has the fewest? How do you know?",
          "Look at graph B. How many are in each group? Say each one.",
          "Look at graph C. What is this graph about? Tell what each column shows."]
    key = ["Most: %s (%d). Fewest: %s (%d). The tallest column has the most." % (mx, max(n1), mn, min(n1)),
           ", ".join("%s %d" % (c, n) for c, n in zip(c2, n2)) + ".",
           "It shows %s. " % t3.lower() + "; ".join("the %s column is %d" % (c, n) for c, n in zip(c3, n3)) + "."]
    return dict(qs=qs, key=key, dir="Look at the three graphs. Your teacher asks about one at a time. Tell what you see.", dur=150, html=row(figs))


def b_ask(lp, r):
    gs = graph_set(lp, r)
    col = THEME[lp][1]
    figs = [(L, bar_fig(t, c, n, col)) for L, (t, c, n) in zip(LET, gs)]
    (t1, c1, n1), (t2, c2, n2), (t3, c3, n3) = gs
    qs = ["Look at graph A. Ask a question about how many there are in all.",
          "Look at graph B. Ask a question that compares two groups, such as which group has more or fewer.",
          "Look at graph C. Ask a question about how many are in one group."]
    key = ["For example: How many are there in all? The answer is %d (%s)." % (sum(n1), " + ".join(str(x) for x in n1)),
           "For example: Which has more, %s or %s? The answer is %s (%d and %d)." % (c2[0], c2[1], c2[0] if n2[0] > n2[1] else c2[1], n2[0], n2[1]),
           "For example: How many %s are there? The answer is %d. Any question about one group that the graph can answer counts." % (c3[0], n3[0])]
    return dict(qs=qs, key=key, dir="Look at the three graphs. Your teacher asks you to make up a question about each one. Say your question out loud.", dur=120, html=row(figs))


def b_answer(lp, r):
    gs = graph_set(lp, r)
    col = THEME[lp][1]
    figs = [(L, bar_fig(t, c, n, col)) for L, (t, c, n) in zip(LET, gs)]
    (t1, c1, n1), (t2, c2, n2), (t3, c3, n3) = gs
    hi, lo = (0, 1) if n3[0] > n3[1] else (1, 0)
    qs = ["Look at graph A. How many are there in all?",
          "Look at graph B. How many are in each group? Which group has fewer?",
          "Look at graph C. How many more %s than %s?" % (c3[hi], c3[lo])]
    fewer = c2[n2.index(min(n2))]
    key = ["%d in all (%s)." % (sum(n1), " + ".join(str(x) for x in n1)),
           "%s. %s has fewer." % (", ".join("%s %d" % (c, n) for c, n in zip(c2, n2)), fewer),
           "%d more (%d - %d = %d)." % (n3[hi] - n3[lo], n3[hi], n3[lo], n3[hi] - n3[lo])]
    return dict(qs=qs, key=key, dir="Look at the three graphs. Your teacher asks about one at a time. Answer out loud.", dur=130, html=row(figs))


# ------------------------------------------------------------------ shares
def shape_svg(shape, parts, shade=None, w=100, h=80, wide=True):
    """shape circle/rect; parts 1, 2, 4; shade = index of shaded share or None"""
    body = ""
    if shape == "circle":
        cx, cy, rr = 50, 42, 34
        shares = []
        if parts == 1:
            shares = ["M %d %d m -%d 0 a %d %d 0 1 0 %d 0 a %d %d 0 1 0 -%d 0" % (cx, cy, rr, rr, rr, 2 * rr, rr, rr, 2 * rr)]
        elif parts == 2:
            shares = ["M %d %d L %d %d A %d %d 0 0 1 %d %d Z" % (cx, cy, cx, cy - rr, rr, rr, cx, cy + rr),
                      "M %d %d L %d %d A %d %d 0 0 1 %d %d Z" % (cx, cy, cx, cy + rr, rr, rr, cx, cy - rr)]
        else:
            shares = ["M %d %d L %d %d A %d %d 0 0 1 %d %d Z" % (cx, cy, cx, cy - rr, rr, rr, cx + rr, cy),
                      "M %d %d L %d %d A %d %d 0 0 1 %d %d Z" % (cx, cy, cx + rr, cy, rr, rr, cx, cy + rr),
                      "M %d %d L %d %d A %d %d 0 0 1 %d %d Z" % (cx, cy, cx, cy + rr, rr, rr, cx - rr, cy),
                      "M %d %d L %d %d A %d %d 0 0 1 %d %d Z" % (cx, cy, cx - rr, cy, rr, rr, cx, cy - rr)]
        for i, d in enumerate(shares):
            fill = "#ffd36e" if shade == i else "#fffaf0"
            body += '<path d="%s" fill="%s" stroke="%s" stroke-width="2.5"/>' % (d, fill, INK)
    else:
        x0, y0, W, H = 10, 12, (80 if wide else 60), (50 if wide else 60)
        rects = []
        if parts == 1:
            rects = [(x0, y0, W, H)]
        elif parts == 2:
            rects = [(x0, y0, W // 2, H), (x0 + W // 2, y0, W // 2, H)]
        else:
            rects = [(x0, y0, W // 2, H // 2), (x0 + W // 2, y0, W // 2, H // 2), (x0, y0 + H // 2, W // 2, H // 2), (x0 + W // 2, y0 + H // 2, W // 2, H // 2)]
        for i, (x, y, ww, hh) in enumerate(rects):
            fill = "#ffd36e" if shade == i else "#fffaf0"
            body += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x, y, ww, hh, fill, INK)
    return svg(w, h, body, "A %s cut into %d equal shares" % (shape, parts))


def b_partcircle(lp, r):
    qs = ["Draw a circle on your paper. Draw one line to cut it into 2 equal shares. How do you know the shares are equal?",
          "Draw another circle. Draw lines to cut it into 4 equal shares. Say how many shares you made.",
          "Draw one more circle and cut it into 2 equal shares. Tell your teacher what the shares are called."]
    key = ["One straight line through the middle of the circle. The 2 shares are the same size. Student can say they match or are the same size.",
           "Two lines crossing in the middle. 4 shares of the same size.",
           "2 equal shares in a circle. They are called halves."]
    return dict(qs=qs, key=key, dir="Listen to each question. Draw on your paper with a pencil. Then tell your teacher about your drawing.", dur=150, html=None)


def b_partrect(lp, r):
    qs = ["Draw a rectangle on your paper. Draw one line to cut it into 2 equal shares. How do you know the shares are equal?",
          "Draw another rectangle. Draw lines to cut it into 4 equal shares. Say how many shares you made.",
          "Draw one more rectangle. Cut it into 4 equal shares a different way than before."]
    key = ["One line straight across or down the middle, or from corner to corner. The 2 shares are the same size.",
           "Two lines crossing in the middle, or three parallel lines. 4 shares of the same size.",
           "A different way to make 4 equal shares, such as 4 strips instead of a cross (or the other way around). The shares are the same size."]
    return dict(qs=qs, key=key, dir="Listen to each question. Draw on your paper with a pencil. Then tell your teacher about your drawing.", dur=150, html=None)


def shape_pair(lp):
    return ("circle", "rectangle") if lp % 2 else ("rectangle", "circle")


def b_words(lp, r):
    s1, s2 = shape_pair(lp)
    figs = [("A", shape_svg(s1, 2)), ("B", shape_svg(s2, 4)), ("C", shape_svg(s1, 4))]
    qs = ["What are the shares in shape A called?",
          "What are the shares in shape B called?",
          "Shape C has 4 equal shares. Tell me two words that name these shares."]
    key = ["Halves.", "Fourths (or quarters).", "Fourths and quarters."]
    return dict(qs=qs, key=key, dir="Look at the three shapes. Your teacher asks about one at a time. Use the words halves, fourths, and quarters.", dur=100, html=row(figs))


def b_phrases(lp, r):
    s1, s2 = shape_pair(lp)
    figs = [("A", shape_svg(s1, 2, shade=0)), ("B", shape_svg(s2, 4, shade=1)), ("C", shape_svg(s1, 4, shade=2))]
    qs = ["One share of shape A is shaded. What part of the %s is shaded? Use the words half of, fourth of, or quarter of." % s1,
          "One share of shape B is shaded. What part of the %s is shaded? Use the words half of, fourth of, or quarter of." % s2,
          "One share of shape C is shaded. What part of the %s is shaded? Say it a different way than you did for B." % s1]
    key = ["Half of the %s." % s1, "A fourth of the %s, or a quarter of the %s." % (s2, s2),
           "A quarter of the %s if the student said fourth for B, or a fourth of the %s if they said quarter." % (s1, s1)]
    return dict(qs=qs, key=key, dir="Look at the three shapes. Your teacher asks about one at a time. Say what part is shaded, using half of, fourth of, or quarter of.", dur=110, html=row(figs))


def b_whole(lp, r):
    s1, s2 = shape_pair(lp)
    figs = [("A", shape_svg(s1, 2)), ("B", shape_svg(s2, 4)), ("C", shape_svg(s1, 4))]
    qs = ["Shape A is cut into halves. Say it like this: the whole %s is __ of the shares." % s1,
          "Shape B is cut into fourths. Say it like this: the whole %s is __ of the shares." % s2,
          "Shape C is cut into fourths. How many fourths make the whole %s?" % s1]
    key = ["Two of the shares (two halves).", "Four of the shares (four fourths).", "Four fourths make the whole."]
    return dict(qs=qs, key=key, dir="Look at the three shapes. Your teacher asks about one at a time. Tell how many shares make the whole.", dur=100, html=row(figs))


def b_smaller(lp, r):
    s1, s2 = shape_pair(lp)
    figs = [("A (left)", shape_svg(s1, 2)), ("A (right)", shape_svg(s1, 4)), ("B (left)", shape_svg(s2, 2)), ("B (right)", shape_svg(s2, 4)), ("C", shape_svg(s1, 2))]
    qs = ["Look at the two shapes in A. One is cut into halves and one is cut into fourths. Which one has smaller shares? How do you know?",
          "Look at the two shapes in B. Which one has smaller shares? How do you know?",
          "Shape C is cut into halves. If you cut each half into 2 equal shares, how many shares will there be? Will each share be bigger or smaller than a half?"]
    key = ["The one cut into fourths (on the right). More equal shares make each share smaller.",
           "The one cut into fourths (on the right). More equal shares make each share smaller.",
           "4 shares. Each share will be smaller than a half (they will be fourths)."]
    return dict(qs=qs, key=key, dir="Look at the shapes. Your teacher asks about one at a time. Tell which shares are smaller and how you know.", dur=130, html=row(figs))


BUILD = {
    ("1.MD.A.2", "express"): b_express, ("1.MD.A.2", "linedup"): b_linedup, ("1.MD.A.2", "countunits"): b_countunits,
    ("1.MD.B.3", "th_an"): b_time("an", False, "tell"), ("1.MD.B.3", "th_dg"): b_time("dg", False, "tell"),
    ("1.MD.B.3", "tf_an"): b_time("an", True, "tell"), ("1.MD.B.3", "tf_dg"): b_time("dg", True, "tell"),
    ("1.MD.B.3", "wh_an"): b_time("an", False, "write"), ("1.MD.B.3", "wh_dg"): b_time("dg", False, "write"),
    ("1.MD.B.3", "wf_an"): b_time("an", True, "write"), ("1.MD.B.3", "wf_dg"): b_time("dg", True, "write"),
    ("1.MD.C.4", "organize"): b_organize, ("1.MD.C.4", "represent"): b_represent,
    ("1.MD.C.4", "interpret"): b_interpret, ("1.MD.C.4", "ask"): b_ask, ("1.MD.C.4", "answer"): b_answer,
    ("1.G.A.3", "partcircle"): b_partcircle, ("1.G.A.3", "partrect"): b_partrect,
    ("1.G.A.3", "words"): b_words, ("1.G.A.3", "phrases"): b_phrases, ("1.G.A.3", "whole"): b_whole, ("1.G.A.3", "smaller"): b_smaller,
}


def build():
    out = {}
    for std, cat in CAT.items():
        for lp in range(1, 11):
            parts = []
            for pid, label, desc in cat["parts"]:
                d = BUILD[(std, pid)](lp, rng_for(lp, std + pid))
                assert len(d["qs"]) == 3 and len(d["key"]) == 3, (std, pid, lp)
                for t in d["qs"] + d["key"] + [d["dir"]]:
                    assert not BAD.search(t), (std, pid, lp, t)
                part = {"id": pid, "title": label, "desc": desc, "qs": d["qs"], "key": d["key"], "dir": d["dir"], "dur": d["dur"]}
                if d.get("html"):
                    assert "—" not in d["html"]
                    part["html"] = d["html"]
                parts.append(part)
            out.setdefault(std, {})[str(lp)] = parts
    return out


APPLY = r"""Object.keys(G1PIC).forEach(function(std){A({std:std,op:"strands",make:function(lp){return G1PIC[std][String(lp)].map(function(s){var o={std:std,strand:s.id,title:s.title,n:3,dur:s.dur,dir:s.dir,desc:s.desc,mats:["a pencil and paper"],rows:s.qs.map(function(q,j){return[q,s.key[j]]})};if(s.html){(function(h){o.html=function(){return h}})(s.html)}return P(o)})}})});"""


def js(data):
    L = ["/* G1PIC-STRANDS-BEGIN (generated by source/tools/gen_g1pic.py, edit the generator, not this block) */",
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append("var G1PIC=%s;" % json.dumps(data, ensure_ascii=False))
    L.append(APPLY)
    L.append("/* G1PIC-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G1, encoding="utf8").read()
    if "G1PIC-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G1PIC-STRANDS-BEGIN.*?G1PIC-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        marker = "/* G1NUM-STRANDS-END */"
        assert marker in src
        src = src.replace(marker, marker + "\n" + block)
    open(G1, "w", encoding="utf8").write(src)
    print("parts:", sum(len(p) for std in data.values() for p in std.values()), "block bytes:", len(block))


if __name__ == "__main__":
    main()
