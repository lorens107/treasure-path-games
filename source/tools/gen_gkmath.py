"""Builds the parts (strands) for the Kindergarten and TK math standards, all 10 LPs.
Writes source/gx/gk.js (Kindergarten) and source/gx/gtk.js (TK).

Kindergarten: one part per "I can" line in the gray book (Visions TK-8 CORE pacing document). Standards with only
one "I can" line stay whole: K.CC.B.4, K.CC.C.6, K.OA.A.3, K.G.A.3.
TK: the TK pacing page has no "I can" lines, so the splits follow the sub-skills written in each TK standard
(Loren chose that approach for Grades 6 to 8). Whole: TK.MATH.1.2, 1.5, 1.6, 3.2, 4.5.
Run:  python3 source/tools/gen_gkmath.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N
import gen_g1pic as P1

GK = os.path.join(HERE, '..', 'gx', 'gk.js')
GTK = os.path.join(HERE, '..', 'gx', 'gtk.js')
THEME, rng_for, nm, BAD = N.THEME, N.rng_for, N.nm, N.BAD
svg, row, INK = P1.svg, P1.row, P1.INK


def C(*p):
    return list(p)


CAT_K = {
    "K.CC.A.1": {"desc": "counting to 100", "parts": C(
        ("ones", "Count to 100 by ones", "Counting to 100 by ones"),
        ("tens", "Count to 100 by tens", "Counting to 100 by tens"))},
    "K.OA.A.2": {"desc": "addition and subtraction within 10", "parts": C(
        ("addword", "Solve addition word problems", "Solving addition word problems with objects or drawings"),
        ("subword", "Solve subtraction word problems", "Solving subtraction word problems with objects or drawings"),
        ("add10", "Add within 10", "Adding within 10 with objects or drawings"),
        ("sub10", "Subtract within 10", "Subtracting within 10 with objects or drawings"))},
    "K.NBT.A.1": {"desc": "numbers from 11 to 19 as ten ones and some more ones", "parts": C(
        ("compose", "Compose numbers 11 to 19", "Composing numbers from 11 to 19 into ten ones and some further ones with objects or drawings"),
        ("reccompose", "Record a composition", "Recording each composition with a drawing or equation"),
        ("decompose", "Decompose numbers 11 to 19", "Decomposing numbers from 11 to 19 into ten ones and some further ones with objects or drawings"),
        ("recdecompose", "Record a decomposition", "Recording each decomposition with a drawing or equation"),
        ("know", "Know 11 to 19 are ten ones and more ones", "Showing that the numbers from 11 to 19 are composed of ten ones and one to nine ones"))},
    "K.MD.A.2": {"desc": "comparing two objects by a measurable attribute", "parts": C(
        ("compare", "Compare two objects", "Directly comparing two objects with a measurable attribute in common to see which has more of or less of the attribute"),
        ("describe", "Describe the difference", "Describing the difference when comparing two objects with a measurable attribute in common"))},
    "K.MD.B.3": {"desc": "classifying objects and counting the groups", "parts": C(
        ("classify", "Classify objects into groups", "Classifying objects into given categories"),
        ("count", "Count the objects in each group", "Counting the number of objects in each category"),
        ("sortcount", "Sort the groups by count", "Sorting the categories by count"))},
    "K.G.A.1": {"desc": "describing objects with shape names and positions", "parts": C(
        ("names", "Name shapes in the environment", "Describing objects in the environment using names of shapes"),
        ("positions", "Describe where objects are", "Describing the relative positions of objects using terms such as above, below, beside, in front of, behind, and next to"))},
}

CAT_TK = {
    "TK.MATH.2.5": {"desc": "sorting and classifying objects", "parts": C(
        ("one", "Sort by one attribute", "Sorting and classifying objects by one attribute into two or more groups"),
        ("two", "Sort by two attributes", "Sorting and classifying objects by two attributes, first by one and then by the other"))},
    "TK.MATH.2.6": {"desc": "repeating patterns", "parts": C(
        ("duplicate", "Copy a repeating pattern", "Duplicating a repeating pattern"),
        ("extend", "Extend a repeating pattern", "Extending a repeating pattern"),
        ("unit", "Name the repeating part", "Describing the repeating part of a pattern (the pattern unit)"))},
    "TK.MATH.3.4": {"desc": "showing data with objects, tally marks, and pictographs", "parts": C(
        ("objects", "Show data with objects", "Using objects to represent data in two or more groups"),
        ("tally", "Show data with tally marks", "Using tally marks to represent data in two or more groups, with each mark standing for one"),
        ("picto", "Show data with a pictograph", "Using pictographs to represent data in two or more groups, with each picture standing for one"))},
    "TK.MATH.4.1": {"desc": "identifying, describing, and building shapes", "parts": C(
        ("identify", "Identify shapes", "Identifying different shapes, including variations of circle, square, triangle, and rectangle"),
        ("describe", "Describe shapes", "Describing shapes with informal language such as sides, corners, and round"),
        ("construct", "Build shapes", "Constructing different shapes"))},
}

D1 = "Your teacher reads each question. Use counters, blocks, or a drawing if you want. Tell your answer out loud."
SHP = ["circle", "square", "triangle"]
COLS = {"red": "#e0534f", "blue": "#3f7fd0", "green": "#4aa05a", "yellow": "#e8b92c"}


def pick(pool, k, r):
    p = pool[:]
    r.shuffle(p)
    return p[:k]


# ---------------------------------------------------------------- pictures
def glyph(kind, x, y, col, s=1.0):
    r_ = 12 * s
    if kind == "circle":
        return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, r_, col, INK)
    if kind == "square":
        return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (x - r_, y - r_, 2 * r_, 2 * r_, col, INK)
    return '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (x, y - r_ - 1, x - r_ - 2, y + r_ - 1, x + r_ + 2, y + r_ - 1, col, INK)


def dots_fig(counts, col, label):
    """rows of dots, one group per count, side by side"""
    items = []
    for L, c in zip("ABCDEF", counts):
        body = ""
        for i in range(c):
            body += '<circle cx="%d" cy="%d" r="10" fill="%s" stroke="%s" stroke-width="1.6"/>' % (16 + (i % 5) * 26, 16 + (i // 5) * 26, col, INK)
        w = 16 * 2 + 4 * 26 - 12
        rows = max(1, (c + 4) // 5)
        items.append((L, svg(w + 6, 14 + rows * 26, body, label)))
    return row(items)


def tenframe(n, col, extra=0):
    """a ten frame with n dots in it, plus 'extra' loose dots below"""
    body = ""
    for i in range(10):
        x, y = 8 + (i % 5) * 30, 8 + (i // 5) * 30
        body += '<rect x="%d" y="%d" width="30" height="30" fill="#fffaf0" stroke="%s" stroke-width="2"/>' % (x, y, INK)
        if i < n:
            body += '<circle cx="%d" cy="%d" r="11" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x + 15, y + 15, col, INK)
    for j in range(extra):
        body += '<circle cx="%d" cy="%d" r="11" fill="%s" stroke="%s" stroke-width="1.6"/>' % (23 + (j % 5) * 30, 88 + (j // 5) * 28, col, INK)
    h = 76 + (28 * ((extra + 4) // 5) + 14 if extra else 4)
    return svg(166, h, body, "A ten frame")


def bars_fig(items, vertical):
    """items: list of (label, size, color). Two objects to compare."""
    body = ""
    if vertical:
        w, h = 40 + len(items) * 80, 140
        for i, (lab, s, col) in enumerate(items):
            x = 30 + i * 80
            body += '<rect x="%d" y="%d" width="30" height="%d" rx="4" fill="%s" stroke="%s" stroke-width="2"/>' % (x, 120 - s, s, col, INK)
            body += '<text x="%d" y="136" font-size="14" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (x + 15, INK, lab)
    else:
        w, h = 200, 24 + len(items) * 48
        for i, (lab, s, col) in enumerate(items):
            y = 10 + i * 48
            body += '<rect x="30" y="%d" width="%d" height="22" rx="4" fill="%s" stroke="%s" stroke-width="2"/>' % (y, s, col, INK)
            body += '<text x="14" y="%d" font-size="14" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (y + 17, INK, lab)
    return svg(w, h, body, "Two objects to compare")


def mixed_fig(items, cols=5):
    body = ""
    for i, (k, c, _) in enumerate(items):
        body += glyph(k, 26 + (i % cols) * 40, 24 + (i // cols) * 40, c, 0.8)
    rows = (len(items) + cols - 1) // cols
    return svg(14 + cols * 40, 10 + rows * 40, body, "A mix of colored shapes")


def grouped_fig(groups):
    """groups: list of (name, kind, color, count)"""
    body = ""
    x = 0
    for name, kind, col, n in groups:
        w = 66
        body += '<rect x="%d" y="6" width="%d" height="190" rx="8" fill="#fffaf0" stroke="%s" stroke-width="2"/>' % (x + 4, w, INK)
        for i in range(n):
            body += glyph(kind, x + 4 + w / 2, 24 + i * 24, col, 0.65)
        body += '<text x="%d" y="212" font-size="13" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (x + 4 + w / 2, INK, name)
        x += w + 10
    return svg(x + 4, 222, body, "Groups of shapes")


# ================================================================== K.CC.A.1
def b_ones(lp, r):
    e1, e2 = 29 + lp, 59 + lp
    qs = ["Count out loud by ones. Start at 1 and stop at %d." % e1,
          "Count out loud by ones. Start at %d and stop at %d." % (e1 + 1, e2),
          "Count out loud by ones. Start at %d and stop at 100." % (e2 + 1)]
    key = ["1 to %d, in order, no number skipped or said twice. A change of decade, such as %d, %d, is where mistakes happen." % (e1, e1 - 1 if e1 % 10 == 0 else (e1 // 10) * 10 - 1, (e1 // 10) * 10) if False else "Says 1 through %d in order, with no number skipped or said twice." % e1,
           "Says %d through %d in order. Listen at the change of decade (for example 39 to 40, 49 to 50, 59 to 60)." % (e1 + 1, e2),
           "Says %d through 100 in order, ending at 100." % (e2 + 1)]
    return dict(qs=qs, key=key, dir="Your teacher asks you to count out loud. Count slowly and carefully.", dur=120)


def b_tens(lp, r):
    s = r.choice([20, 30, 40, 50])
    gap = r.choice([(40, 50), (60, 70), (30, 40), (70, 80)])
    qs = ["Count to 100 by tens. Start at 10.",
          "Count by tens. Start at %d and stop at 100." % s,
          "Count by tens: %d, %d, %d. What number comes next? What comes after that?" % (gap[0] - 20 if gap[0] > 20 else 10, gap[0] - 10, gap[0])]
    a = gap[0]
    key = ["10, 20, 30, 40, 50, 60, 70, 80, 90, 100.",
           ", ".join(str(x) for x in range(s, 101, 10)) + ".",
           "%d, then %d. Counting by tens adds 10 each time." % (a + 10, a + 20)]
    return dict(qs=qs, key=key, dir="Your teacher asks you to count by tens out loud.", dur=110)


# ================================================================== K.OA.A.2
STORY = {
    1: ["coins", "gems", "shells"], 2: ["apples", "pears", "plums"], 3: ["pumpkins", "gourds", "acorns"], 4: ["snowballs", "mittens", "hats"],
    5: ["fish", "flags", "boats"], 6: ["lanterns", "balloons", "kites"], 7: ["hearts", "cards", "stickers"], 8: ["seeds", "flowers", "bees"],
    9: ["logs", "rocks", "shells"], 10: ["ribbons", "cupcakes", "cookies"]}


def sums(r, k):
    out = []
    pool = [(a, b) for a in range(1, 8) for b in range(1, 8) if a + b <= 10 and a != b]
    r.shuffle(pool)
    seen = set()
    for a, b in pool:
        if (a + b) in seen:
            continue
        seen.add(a + b)
        out.append((a, b))
        if len(out) == k:
            break
    return out


def b_addword(lp, r):
    th = STORY[lp]
    ps = sums(r, 3)
    names = [nm(lp, 0), nm(lp, 1), nm(lp, 2)]
    tpl = ["%s has %d %s. %s gets %d more. How many %s does %s have now?",
           "%s puts %d %s in a basket. Then %s puts in %d more. How many %s are in the basket now?",
           "%s sees %d %s. Then %d more come. How many %s does %s see in all?"]
    qs = [tpl[0] % (names[0], ps[0][0], th[0], names[0], ps[0][1], th[0], names[0]),
          tpl[1] % (names[1], ps[1][0], th[1], names[1], ps[1][1], th[1]),
          tpl[2] % (names[2], ps[2][0], th[2], ps[2][1], th[2], names[2])]
    key = ["%d %s. %d + %d = %d." % (a + b, th[i], a, b, a + b) for i, (a, b) in enumerate(ps)]
    return dict(qs=qs, key=key, dir="Your teacher reads each story. Use counters or draw a picture to solve it. Tell the answer.", dur=150)


def b_subword(lp, r):
    th = STORY[lp]
    pool = [(a, b) for a in range(3, 10) for b in range(1, a) if a != 2 * b]
    r.shuffle(pool)
    ps, seen = [], set()
    for a, b in pool:
        if a - b not in seen:
            seen.add(a - b)
            ps.append((a, b))
        if len(ps) == 3:
            break
    names = [nm(lp, 0), nm(lp, 1), nm(lp, 2)]
    qs = ["%s has %d %s. %s gives away %d. How many %s does %s have left?" % (names[0], ps[0][0], th[0], names[0], ps[0][1], th[0], names[0]),
          "There are %d %s on a table. %d fall off. How many %s are on the table now?" % (ps[1][0], th[1], ps[1][1], th[1]),
          "%s has %d %s. %s loses %d. How many %s are left?" % (names[2], ps[2][0], th[2], names[2], ps[2][1], th[2])]
    key = ["%d %s. %d − %d = %d." % (a - b, th[i], a, b, a - b) for i, (a, b) in enumerate(ps)]
    key = [k.replace("−", "−") for k in key]
    return dict(qs=qs, key=key, dir="Your teacher reads each story. Use counters or draw a picture to solve it. Tell the answer.", dur=150)


def b_add10(lp, r):
    ps = sums(r, 3)
    col = THEME[lp][1]
    qs = ["What is %d + %d? Use counters or draw dots to check." % ps[0], "What is %d + %d? Use counters or draw dots to check." % ps[1], "What is %d + %d? Use counters or draw dots to check." % ps[2]]
    key = ["%d. %d and %d make %d." % (a + b, a, b, a + b) for a, b in ps]
    return dict(qs=qs, key=key, dir="Your teacher reads each addition. Use counters or draw a picture to find the total.", dur=110)


def b_sub10(lp, r):
    pool = [(a, b) for a in range(3, 11) for b in range(1, a)]
    r.shuffle(pool)
    ps, seen = [], set()
    for a, b in pool:
        if a - b not in seen:
            seen.add(a - b)
            ps.append((a, b))
        if len(ps) == 3:
            break
    qs = ["What is %d − %d? Use counters or draw dots and cross some out." % p for p in ps]
    key = ["%d. Start with %d and take away %d." % (a - b, a, b) for a, b in ps]
    return dict(qs=qs, key=key, dir="Your teacher reads each subtraction. Use counters or draw a picture to find what is left.", dur=110)


# ================================================================== K.NBT.A.1
def teens(r, k):
    return r.sample(range(11, 20), k)


def b_compose(lp, r):
    col = THEME[lp][1]
    ns = teens(r, 3)
    figs = [(L, tenframe(10, col, n - 10)) for L, n in zip("ABC", ns)]
    qs = ["Picture %s shows a full ten frame and some more dots. How many dots in all? Use the ten and the extra dots to tell." % L for L in "ABC"]
    key = ["%d. Ten dots in the frame and %d more make %d." % (n, n - 10, n) for n in ns]
    return dict(qs=qs, key=key, dir="Look at the three pictures. Each has a full ten frame and some extra dots. Tell how many in all.", dur=140, html=row(figs))


def b_reccompose(lp, r):
    ns = teens(r, 3)
    qs = ["Ten ones and %d ones are put together. Write an equation. What number do they make?" % (n - 10) for n in ns]
    key = ["10 + %d = %d." % (n - 10, n) for n in ns]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write the equation on your paper. Then say the number.", dur=150)


def b_decompose(lp, r):
    col = THEME[lp][1]
    ns = teens(r, 3)
    qs = ["Use counters to show the number %d. Make a group of ten. How many are left over?" % n for n in ns]
    key = ["%d is 10 and %d. One group of ten, with %d left over." % (n, n - 10, n - 10) for n in ns]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Use counters or draw dots, circle a group of ten, and tell how many are left.", dur=160)


def b_recdecompose(lp, r):
    ns = teens(r, 3)
    qs = ["Write an equation that shows %d as ten and some ones." % n for n in ns]
    key = ["%d = 10 + %d (or 10 + %d = %d)." % (n, n - 10, n - 10, n) if False else "%d = 10 + %d." % (n, n - 10) for n in ns]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write the equation on your paper.", dur=150)


def b_know(lp, r):
    ns = teens(r, 3)
    o1 = ns[0] - 10
    n2 = ns[1]
    wrong = 10 + (n2 - 10) + r.choice([1, 2])
    if wrong > 19:
        wrong = n2 - 1 if n2 > 11 else n2 + 1
    k = ns[2] - 10
    qs = ["The number %d is ten ones and some more ones. How many more ones?" % ns[0],
          "True or not true: %d is ten ones and %d ones." % (n2, n2 - 10),
          "What number is ten ones and %d more ones?" % k]
    key = ["%d more ones. %d is 10 and %d." % (o1, ns[0], o1),
           "True. %d = 10 + %d." % (n2, n2 - 10),
           "%d. 10 and %d more is %d." % (ns[2], k, ns[2])]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Think about ten ones and some more ones. Tell your answer.", dur=130)


# ================================================================== K.MD.A.2
def b_compare(lp, r):
    cols = ["#e0534f", "#3f7fd0", "#4aa05a", "#e8b92c"]
    specs = [("horizontal", "longer", "shorter"), ("vertical", "taller", "shorter"), ("horizontal", "shorter", "longer")]
    figs, qs, key = [], [], []
    for L, (orient, ask, other) in zip("ABC", specs):
        a, b = r.sample([60, 90, 120, 150, 80, 110], 2)
        c1, c2 = r.sample(cols, 2)
        items = [("1", a, c1), ("2", b, c2)]
        figs.append((L, bars_fig(items, orient == "vertical")))
        big = "1" if a > b else "2"
        sm = "2" if a > b else "1"
        qs.append("In picture %s, which one is %s, number 1 or number 2?" % (L, ask))
        key.append("Number %s." % (big if ask in ("longer", "taller") else sm))
    return dict(qs=qs, key=key, dir="Look at the three pictures. Each has two objects. Your teacher asks which one has more or less of something. Tell the number.", dur=110, html=row(figs))


def b_describe(lp, r):
    cols = ["#e0534f", "#3f7fd0", "#4aa05a", "#e8b92c"]
    figs, qs, key = [], [], []
    modes = [("horizontal", "long", "longer", "shorter"), ("vertical", "tall", "taller", "shorter"), ("horizontal", "long", "longer", "shorter")]
    for L, (orient, adj, cmp1, cmp2) in zip("ABC", modes):
        a, b = r.sample([60, 90, 120, 150, 80, 110], 2)
        c1, c2 = r.sample(cols, 2)
        figs.append((L, bars_fig([("1", a, c1), ("2", b, c2)], orient == "vertical")))
        big = "1" if a > b else "2"
        sm = "2" if a > b else "1"
        qs.append("Look at picture %s. Tell how number 1 and number 2 are different. Use the words %s and %s." % (L, cmp1, cmp2))
        key.append("Number %s is %s than number %s. Number %s is %s than number %s." % (big, cmp1, sm, sm, cmp2, big))
    return dict(qs=qs, key=key, dir="Look at the three pictures. Tell how the two objects in each picture are different. Use comparing words.", dur=140, html=row(figs))


# ================================================================== K.MD.B.3
def group_data(r, k, lo=1, hi=6):
    names = ["red", "blue", "green", "yellow"][:k]
    kind = r.choice(SHP)
    cnt = P1.distinct_counts(r, k, lo, hi, 15)
    return [(nm_, kind, COLS[nm_], c) for nm_, c in zip(names, cnt)]


def b_classify(lp, r):
    kinds = SHP[:]
    r.shuffle(kinds)
    cols = ["red", "blue", "green"]
    r.shuffle(cols)
    items = []
    for k in kinds:
        for c in cols:
            items.append((k, COLS[c], c))
    items = pick(items, 9, r) if False else items
    r.shuffle(items)
    fig = mixed_fig(items, 5)
    cs = r.choice(range(len(items)))
    kind, _, cname = items[cs]
    qs = ["Look at the shapes. Sort them into groups by color. What groups do you make?",
          "Now sort the same shapes by kind of shape. What groups do you make?",
          "There is a %s %s. Which group is it in when you sort by color? Which group is it in when you sort by shape?" % (cname, kind)]
    key = ["3 groups: %s." % ", ".join(sorted(cols)),
           "3 groups: %s." % ", ".join(sorted(k + "s" for k in kinds)),
           "The %s group when sorted by color. The %s group when sorted by shape." % (cname, kind)]
    return dict(qs=qs, key=key, dir="Look at the picture of mixed shapes. Your teacher asks how you would sort them into groups.", dur=130, html=row([("", fig)]))


def b_countgroups(lp, r):
    g = group_data(r, 3, 2, 7)
    fig = grouped_fig(g)
    qs = ["How many shapes are in the %s group?" % n for n, _, _, _ in g]
    key = ["%d." % c for _, _, _, c in g]
    return dict(qs=qs, key=key, dir="Look at the three groups of shapes. Count the shapes in each group. Tell how many.", dur=120, html=row([("", fig)]))


def b_sortcount(lp, r):
    g = group_data(r, 3, 2, 7)
    fig = grouped_fig(g)
    srt = sorted(g, key=lambda x: x[3])
    qs = ["Which group has the most shapes?",
          "Which group has the fewest shapes?",
          "Say the groups in order from the fewest shapes to the most shapes."]
    key = ["The %s group (%d)." % (srt[-1][0], srt[-1][3]),
           "The %s group (%d)." % (srt[0][0], srt[0][3]),
           "%s (%s)." % (", then ".join(x[0] for x in srt), ", ".join(str(x[3]) for x in srt))]
    return dict(qs=qs, key=key, dir="Look at the three groups of shapes. Count each group. Tell which has the most and the fewest.", dur=130, html=row([("", fig)]))


# ================================================================== K.G.A.1
def house_fig(wall, roof, door, sun, door_kind="rectangle"):
    body = '<circle cx="230" cy="36" r="22" fill="%s" stroke="%s" stroke-width="2.5"/>' % (sun, INK)
    body += '<rect x="60" y="80" width="110" height="90" fill="%s" stroke="%s" stroke-width="2.5"/>' % (wall, INK)
    body += '<polygon points="50,82 115,28 180,82" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (roof, INK)
    body += '<rect x="102" y="120" width="26" height="50" fill="%s" stroke="%s" stroke-width="2.5"/>' % (door, INK)
    return svg(270, 184, body, "A house with a sun")


def b_names(lp, r):
    cols = ["#f2c14e", "#f08a5d", "#7fc8a9", "#8ecae6", "#c77dff", "#f4a6c0"]
    r.shuffle(cols)
    fig = house_fig(cols[0], cols[1], cols[2], cols[3])
    asks = [("the roof", "triangle"), ("the sun", "circle"), ("the door", "rectangle"), ("the wall of the house", "square")]
    it = pick(asks, 3, r)
    qs = ["Look at the house. What shape is %s?" % w for w, _ in it]
    key = ["A %s." % s for _, s in it]
    return dict(qs=qs, key=key, dir="Look at the picture of a house and the sun. Your teacher asks about the shapes you see. Tell the shape names.", dur=110, html=row([("", fig)]))


def position_fig(top, bl, bm, br):
    body = ""
    pos = [(top, 135, 34), (bl, 50, 120), (bm, 135, 120), (br, 220, 120)]
    for (k, col), x, y in pos:
        body += glyph(k, x, y, col, 1.3)
    return svg(270, 160, body, "Four shapes")


def b_positions(lp, r):
    ks = SHP[:] + ["circle"]
    shapes = [("circle", COLS["red"]), ("square", COLS["blue"]), ("triangle", COLS["green"]), ("circle", COLS["yellow"])]
    r.shuffle(shapes)
    names = {COLS["red"]: "red", COLS["blue"]: "blue", COLS["green"]: "green", COLS["yellow"]: "yellow"}
    lab = lambda s: "%s %s" % (names[s[1]], s[0])
    top, bl, bm, br = shapes
    fig = position_fig(top, bl, bm, br)
    qs = ["Which shape is above the %s?" % lab(bm),
          "Which shape is next to the %s on its left?" % lab(bm) if False else "Which shape is below the %s?" % lab(top),
          "Which shape is between the %s and the %s?" % (lab(bl), lab(br))]
    key = ["The %s." % lab(top), "The %s." % lab(bm), "The %s." % lab(bm)]
    return dict(qs=qs, key=key, dir="Look at the four shapes. Your teacher asks where the shapes are. Use position words like above, below, next to, and between.", dur=130, html=row([("", fig)]))


# ================================================================== TK
def attr_items(r, two=False):
    colset = ["red", "blue"]
    kinds = ["circle", "square"]
    items = []
    for c in colset:
        for k in kinds:
            for s in (["big", "small"] if two else ["big"]):
                items.append((k, COLS[c], c, s))
    return items


def mixed_size_fig(items, cols=4):
    body = ""
    for i, (k, c, cn, sz) in enumerate(items):
        scale = 0.95 if sz == "big" else 0.55
        body += glyph(k, 30 + (i % cols) * 48, 28 + (i // cols) * 50, c, scale)
    rows = (len(items) + cols - 1) // cols
    return svg(20 + cols * 48, 14 + rows * 50, body, "A mix of shapes")


def b_sort1(lp, r):
    # two colors, two kinds, random counts
    n_red = r.randint(2, 5)
    n_blue = r.randint(2, 5)
    while n_blue == n_red:
        n_blue = r.randint(2, 5)
    items = []
    kinds = ["circle", "square"]
    for c, n in (("red", n_red), ("blue", n_blue)):
        for _ in range(n):
            items.append((r.choice(kinds), COLS[c], c, "big"))
    r.shuffle(items)
    fig = mixed_size_fig(items, 5)
    nc = sum(1 for x in items if x[0] == "circle")
    ns = len(items) - nc
    qs = ["Sort these into groups by color. What groups do you make?",
          "How many are in the red group? How many are in the blue group?",
          "Now sort them by shape. How many circles? How many squares?"]
    key = ["2 groups: red and blue.",
           "%d red, %d blue." % (n_red, n_blue),
           "%d circles, %d squares." % (nc, ns)]
    return dict(qs=qs, key=key, dir="Look at the picture of mixed shapes. Your teacher asks you to sort them into groups. Use counters or point and tell.", dur=130, html=row([("", fig)]))


def b_sort2(lp, r):
    items = attr_items(r, True)
    r.shuffle(items)
    fig = mixed_size_fig(items, 4)
    c, k, s = r.choice(["red", "blue"]), r.choice(["circle", "square"]), r.choice(["big", "small"])
    qs = ["Sort these by color first. How many red? How many blue?",
          "Now sort the red ones by size. How many big red? How many small red?",
          "How many %s %s %ss are there?" % (s, c, k)]
    key = ["4 red and 4 blue.",
           "2 big red and 2 small red.",
           "1. There is one %s %s %s." % (s, c, k)]
    return dict(qs=qs, key=key, dir="Look at the picture of mixed shapes. Sort first by one thing, then by another. Tell what you find.", dur=150, html=row([("", fig)]))


def pat_fig(seq, cols_map):
    body = ""
    for i, s in enumerate(seq):
        body += '<circle cx="%d" cy="24" r="16" fill="%s" stroke="%s" stroke-width="2"/>' % (26 + i * 40, cols_map[s], INK) if s != "?" else '<rect x="%d" y="8" width="32" height="32" rx="6" fill="#fffaf0" stroke="%s" stroke-width="2" stroke-dasharray="4 3"/>' % (10 + i * 40, INK)
    return svg(20 + len(seq) * 40, 50, body, "A pattern of colored circles")


PATS = [("AB", ["A", "B"]), ("AAB", ["A", "A", "B"]), ("ABB", ["A", "B", "B"]), ("ABC", ["A", "B", "C"]), ("AABB", ["A", "A", "B", "B"])]


def pat_data(r, k):
    cs = ["red", "blue", "green", "yellow"]
    r.shuffle(cs)
    out = []
    pats = PATS[:]
    r.shuffle(pats)
    for name, unit in pats[:k]:
        letters = sorted(set(unit))
        cmap = {l: COLS[cs[i]] for i, l in enumerate(letters)}
        cname = {l: cs[i] for i, l in enumerate(letters)}
        out.append((name, unit, cmap, cname))
    return out


def b_pdup(lp, r):
    pd = pat_data(r, 3)
    figs, qs, key = [], [], []
    for L, (name, unit, cmap, cname) in zip("ABC", pd):
        seq = (unit * 3)[:max(6, len(unit) * 2)]
        figs.append((L, pat_fig(seq, cmap)))
        n = r.randint(2, len(seq))
        qs.append("Copy pattern %s with your blocks. What color is your block number %d?" % (L, n))
        key.append("%s. The pattern is %s." % (cname[seq[n - 1]], ", ".join(cname[x] for x in seq)))
    return dict(qs=qs, key=key, dir="Look at the three patterns. Copy each one with your blocks. Then answer your teacher's question.", dur=150, html=row(figs))


def b_pext(lp, r):
    pd = pat_data(r, 3)
    figs, qs, key = [], [], []
    for L, (name, unit, cmap, cname) in zip("ABC", pd):
        reps = (unit * 4)
        shown = reps[:len(unit) * 2 + (1 if len(unit) > 2 else 0)]
        nxt = reps[len(shown)]
        seq = shown + ["?"]
        cm = dict(cmap)
        figs.append((L, pat_fig(seq, cm)))
        qs.append("Look at pattern %s. What color comes next? Then say the one after that." % L)
        key.append("%s, then %s." % (cname[nxt], cname[reps[len(shown) + 1]]))
    return dict(qs=qs, key=key, dir="Look at the three patterns. Tell what comes next in each one.", dur=140, html=row(figs))


def b_punit(lp, r):
    pd = pat_data(r, 3)
    figs, qs, key = [], [], []
    for L, (name, unit, cmap, cname) in zip("ABC", pd):
        seq = (unit * 3)[:len(unit) * 3]
        figs.append((L, pat_fig(seq, cmap)))
        qs.append("Look at pattern %s. What part keeps repeating? Say the colors of the part that repeats." % L)
        key.append("%s. This part repeats." % ", ".join(cname[x] for x in unit))
    return dict(qs=qs, key=key, dir="Look at the three patterns. Tell the part that repeats over and over.", dur=140, html=row(figs))


def b_dobj(lp, r):
    g = group_data(r, 2, 2, 7)
    fig = grouped_fig([g[0], g[1]])
    n0, n1 = g[0][3], g[1][3]
    q1 = "The picture shows two groups of shapes. Put one counter for each shape in the %s group. How many counters is that?" % g[0][0]
    q2 = "Do the same for the %s group. How many counters?" % g[1][0]
    q3 = "Which group has more? How many more?"
    big = g[0] if n0 > n1 else g[1]
    key = ["%d counters. One counter stands for one shape." % n0, "%d counters." % n1, "The %s group has more, by %d." % (big[0], abs(n0 - n1))]
    return dict(qs=[q1, q2, q3], key=key, dir="Look at the two groups of shapes. Use counters to show how many are in each group. Tell your answers.", dur=150, html=row([("", fig)]))


def tally_svg(n):
    body = ""
    x = 10
    for g in range(n // 5 + (1 if n % 5 else 0)):
        k = min(5, n - g * 5)
        for i in range(min(k, 4)):
            body += '<line x1="%d" y1="6" x2="%d" y2="36" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % (x + i * 9, x + i * 9, INK)
        if k == 5:
            body += '<line x1="%d" y1="30" x2="%d" y2="12" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % (x - 4, x + 4 * 9 - 1, INK) if False else '<line x1="%d" y1="30" x2="%d" y2="10" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % (x - 5, x + 3 * 9 + 5, INK)
        x += 4 * 9 + 16 if k == 5 else k * 9 + 14
    return body, x


def tally_fig(names, counts):
    body = ""
    w = 40
    for i, (nme, c) in enumerate(zip(names, counts)):
        y = 6 + i * 52
        body += '<text x="6" y="%d" font-size="15" font-weight="700" fill="%s" font-family="sans-serif">%s</text>' % (y + 28, INK, nme)
        t, _ = tally_svg(c)
        body += '<g transform="translate(90,%d)">%s</g>' % (y, t)
    return svg(250, 12 + len(names) * 52, body, "Tally marks for each group")


def b_ttally(lp, r):
    names = pick(["apples", "pears", "plums", "cats", "dogs", "fish", "red cars", "blue cars"], 2, r)
    ca = r.randint(2, 7)
    cb = r.randint(2, 7)
    while cb == ca:
        cb = r.randint(2, 7)
    fig = tally_fig(names, [ca, cb])
    qs = ["Count the tally marks next to %s. How many are there? What does each mark stand for?" % names[0],
          "How many tally marks are there for %s?" % names[1],
          "Which has more, %s or %s? How many more?" % (names[0], names[1])]
    big = names[0] if ca > cb else names[1]
    key = ["%d. Each tally mark stands for one." % ca, "%d." % cb, "%s have more, by %d." % (big.capitalize(), abs(ca - cb)) if big.endswith("s") else "%s has more, by %d." % (big.capitalize(), abs(ca - cb))]
    return dict(qs=qs, key=key, dir="Look at the tally marks. Count them. Each mark stands for one thing.", dur=150, html=row([("", fig)]))


def picto_fig(names, counts, col):
    body = ""
    for i, (nme, c) in enumerate(zip(names, counts)):
        y = 6 + i * 40
        body += '<text x="6" y="%d" font-size="14" font-weight="700" fill="%s" font-family="sans-serif">%s</text>' % (y + 20, INK, nme)
        for j in range(c):
            body += '<circle cx="%d" cy="%d" r="12" fill="%s" stroke="%s" stroke-width="2"/>' % (110 + j * 30, y + 16, col, INK)
    return svg(110 + 7 * 30 + 10, 10 + len(names) * 40, body, "A picture graph")


def b_tpicto(lp, r):
    names = pick(["cats", "dogs", "fish", "birds", "frogs"], 2, r)
    ca = r.randint(2, 6)
    cb = r.randint(2, 6)
    while cb == ca:
        cb = r.randint(2, 6)
    fig = picto_fig(names, [ca, cb], THEME[lp][1])
    qs = ["How many pictures are in the row for %s? What does each picture stand for?" % names[0],
          "How many pictures are in the row for %s?" % names[1],
          "Which row has more pictures? How many more?"]
    big = names[0] if ca > cb else names[1]
    key = ["%d. Each picture stands for one." % ca, "%d." % cb, "The %s row, by %d." % (big, abs(ca - cb))]
    return dict(qs=qs, key=key, dir="Look at the picture graph. Each picture stands for one. Count the pictures in each row.", dur=150, html=row([("", fig)]))


SHP_NAMES = ["circle", "square", "triangle", "rectangle"]


def shape_var(kind, x, y, col, v):
    if kind == "circle":
        rr = 22 if v == 0 else 15
        return '<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x, y, rr, col, INK)
    if kind == "square":
        s = 40 if v == 0 else 28
        return '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - s // 2, y - s // 2, s, s, col, INK)
    if kind == "rectangle":
        w, h = (56, 30) if v == 0 else (28, 52)
        return '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - w // 2, y - h // 2, w, h, col, INK)
    pts = [(x, y - 24), (x - 26, y + 20), (x + 26, y + 20)] if v == 0 else [(x - 28, y - 18), (x + 24, y), (x - 28, y + 18)]
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (" ".join("%d,%d" % p for p in pts), col, INK)


def b_tidentify(lp, r):
    kinds = pick(SHP_NAMES, 3, r)
    cols = pick(list(COLS.values()), 3, r)
    body = ""
    for i, (k, c) in enumerate(zip(kinds, cols)):
        body += shape_var(k, 40 + i * 90, 40, c, r.randint(0, 1))
    fig = svg(20 + 3 * 90, 84, body, "Three shapes")
    letters = list("ABC")
    qs = ["Which shape is the %s: A, B, or C?" % kinds[i] for i in range(3)]
    key = ["Shape %s." % letters[i] for i in range(3)]
    r2 = list(range(3))
    r.shuffle(r2)
    qs = [qs[i] for i in r2]
    key = [key[i] for i in r2]
    fig = row([("A", svg(90, 84, shape_var(kinds[0], 45, 42, cols[0], 0), "Shape A")), ("B", svg(90, 84, shape_var(kinds[1], 45, 42, cols[1], 1), "Shape B")), ("C", svg(90, 84, shape_var(kinds[2], 45, 42, cols[2], 0), "Shape C"))])
    return dict(qs=qs, key=key, dir="Look at the three shapes. Your teacher asks you to find a shape. Tell the letter.", dur=110, html=fig)


def b_tdescribe(lp, r):
    qs = ["How many sides does a triangle have? How many corners?",
          "A square has sides and corners. How many of each?",
          "Which shape is round: a circle or a square? How do you know?"]
    key = ["3 sides and 3 corners.", "4 sides and 4 corners. All the sides are the same length.", "A circle. It is round and has no corners and no straight sides."]
    alt = [("How many sides does a rectangle have? How many corners?", "4 sides and 4 corners. Two long sides and two short sides."),
           ("Tell me about a circle. Does it have corners or sides?", "No corners and no straight sides. It is round."),
           ("How are a square and a triangle different? Talk about sides and corners.", "A square has 4 sides and 4 corners. A triangle has 3 sides and 3 corners.")]
    k = r.randint(0, 2)
    qs[k], key[k] = alt[k]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Tell about the shapes with words like sides, corners, and round.", dur=140)


def b_tconstruct(lp, r):
    pool = [("Use craft sticks or straws to build a triangle. How many sticks did you use?", "3 sticks."),
            ("Use craft sticks or straws to build a square. How many sticks did you use?", "4 sticks, all the same length."),
            ("Use clay or a pipe cleaner to make a circle. Does your shape have corners?", "No. A circle is round with no corners."),
            ("Use craft sticks to build a rectangle. How many sticks did you use? Are all the sticks the same length?", "4 sticks. Two long sticks and two short sticks."),
            ("Draw a triangle on your paper. How many sides and how many corners did you draw?", "3 sides and 3 corners."),
            ("Draw a square on your paper. How many corners did you draw?", "4 corners.")]
    it = pick(pool, 3, r)
    return dict(qs=[q for q, _ in it], key=[k for _, k in it], dir="Your teacher reads each task. Use your materials to build the shape. Then answer the question.", dur=170)


BUILD = {
    ("K.CC.A.1", "ones"): b_ones, ("K.CC.A.1", "tens"): b_tens,
    ("K.OA.A.2", "addword"): b_addword, ("K.OA.A.2", "subword"): b_subword, ("K.OA.A.2", "add10"): b_add10, ("K.OA.A.2", "sub10"): b_sub10,
    ("K.NBT.A.1", "compose"): b_compose, ("K.NBT.A.1", "reccompose"): b_reccompose, ("K.NBT.A.1", "decompose"): b_decompose,
    ("K.NBT.A.1", "recdecompose"): b_recdecompose, ("K.NBT.A.1", "know"): b_know,
    ("K.MD.A.2", "compare"): b_compare, ("K.MD.A.2", "describe"): b_describe,
    ("K.MD.B.3", "classify"): b_classify, ("K.MD.B.3", "count"): b_countgroups, ("K.MD.B.3", "sortcount"): b_sortcount,
    ("K.G.A.1", "names"): b_names, ("K.G.A.1", "positions"): b_positions,
    ("TK.MATH.2.5", "one"): b_sort1, ("TK.MATH.2.5", "two"): b_sort2,
    ("TK.MATH.2.6", "duplicate"): b_pdup, ("TK.MATH.2.6", "extend"): b_pext, ("TK.MATH.2.6", "unit"): b_punit,
    ("TK.MATH.3.4", "objects"): b_dobj, ("TK.MATH.3.4", "tally"): b_ttally, ("TK.MATH.3.4", "picto"): b_tpicto,
    ("TK.MATH.4.1", "identify"): b_tidentify, ("TK.MATH.4.1", "describe"): b_tdescribe, ("TK.MATH.4.1", "construct"): b_tconstruct,
}


def build(cat):
    out = {}
    for std, c in cat.items():
        for lp in range(1, 11):
            parts = []
            for pid, label, desc in c["parts"]:
                d = BUILD[(std, pid)](lp, rng_for(lp, std + pid))
                assert len(d["qs"]) == 3 and len(d["key"]) == 3, (std, pid, lp, len(d["qs"]), len(d["key"]))
                for t in d["qs"] + d["key"] + [d["dir"]]:
                    assert not BAD.search(t), (std, pid, lp, t)
                part = {"id": pid, "title": label, "desc": desc, "qs": d["qs"], "key": d["key"], "dir": d["dir"], "dur": d["dur"]}
                if d.get("html"):
                    assert "—" not in d["html"]
                    part["html"] = d["html"]
                parts.append(part)
            out.setdefault(std, {})[str(lp)] = parts
    return out


def js(cat, data, grade, var, tag):
    L = ["/* %s-STRANDS-BEGIN (generated by source/tools/gen_gkmath.py, edit the generator, not this block) */" % tag,
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, c in cat.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": c["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in c["parts"]]}, ensure_ascii=False)))
    L.append("var %s=%s;" % (var, json.dumps(data, ensure_ascii=False)))
    L.append(P1.APPLY.replace("G1PIC", var))
    L.append("/* %s-STRANDS-END */" % tag)
    return "\n".join(L)


def write(path, grade, cat, var, tag):
    data = build(cat)
    block = js(cat, data, grade, var, tag)
    assert "—" not in block and "–" not in block
    head = '(function(){var A=function(x){GXadd("%s",x)},P=GXp;\n' % grade
    src = head + block + "\n})();\n"
    open(path, "w", encoding="utf8").write(src)
    print(grade, "parts:", sum(len(p) for std in data.values() for p in std.values()), "bytes:", len(src))


def main():
    write(GK, "K", CAT_K, "GKPIC", "GKMATH")
    write(GTK, "TK", CAT_TK, "GTKPIC", "GTKMATH")


if __name__ == "__main__":
    main()
