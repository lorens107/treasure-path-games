"""Builds the parts (strands) for the Grade 3 math standards that have more than one gray-book "I can" line, all 10 LPs,
and writes them into source/gx/g3.js.

3.OA.A.1, 3.OA.A.2, 3.NBT.A.1 and 3.MD.C.7 have one "I can" line each, so they stay whole standards.
Run:  python3 source/tools/gen_g3math.py
"""
import json, os, re, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N
import gen_g1pic as P1

G3 = os.path.join(HERE, '..', 'gx', 'g3.js')
THEME, rng_for, nm, BAD = N.THEME, N.rng_for, N.nm, N.BAD
svg, row = P1.svg, P1.row
INK = P1.INK


def C(*p):
    return list(p)


# desc must read after "Secure with ..." in a gradebook line, so no "I can"
CAT = {
    "3.OA.D.8": {"desc": "two-step word problems with the four operations, equations with a letter for the unknown, and checking if answers are reasonable", "parts": C(
        ("solve2", "Solve two-step word problems", "Solving two-step word problems using the four operations"),
        ("equation", "Write an equation with a letter", "Representing two-step word problems with equations that use a letter for the unknown quantity"),
        ("mental", "Check an answer with mental math", "Assessing the reasonableness of answers using mental computation"),
        ("estimate", "Check an answer with an estimate", "Assessing the reasonableness of answers using estimation strategies"),
        ("rounding", "Check an answer by rounding", "Assessing the reasonableness of answers using rounding"))},
    "3.NF.A.1": {"desc": "understanding unit fractions 1/b and fractions a/b as parts of a whole", "parts": C(
        ("unit", "Unit fractions (1/b)", "Showing that a fraction 1/b is formed by 1 part when a whole is partitioned into b equal parts"),
        ("amountb", "Fractions (a/b) built from unit fractions", "Showing that a fraction a/b is formed by a parts of size 1/b"))},
    "3.NF.A.2": {"desc": "fractions as numbers on a number line", "parts": C(
        ("isnumber", "A fraction is a number on the number line", "Showing that a fraction is a number on the number line"),
        ("drawline", "Show fractions on a number line diagram", "Representing fractions on a number line diagram"))},
    "3.NF.A.3": {"desc": "equivalent fractions in special cases, and comparing fractions by reasoning about size", "parts": C(
        ("equiv", "Explain equivalent fractions", "Explaining equivalence of fractions in special cases"),
        ("compare", "Compare fractions by reasoning", "Comparing fractions by reasoning about their size"))},
    "3.MD.B.4": {"desc": "measuring to halves and fourths of an inch and showing the data on a line plot", "parts": C(
        ("measure", "Measure to the half and fourth inch", "Measuring lengths using rulers marked with halves and fourths of an inch"),
        ("gendata", "Generate measurement data", "Generating measurement data by measuring lengths using rulers marked with halves and fourths of an inch"),
        ("lineplot", "Show the data on a line plot", "Showing measurement data by making a line plot"),
        ("lpscale", "Mark the line plot scale", "Making a line plot with the horizontal scale marked off in whole numbers, halves, or quarters"))},
    "3.G.A.2": {"desc": "partitioning shapes into equal areas and naming each part as a unit fraction", "parts": C(
        ("partition", "Partition shapes into equal areas", "Partitioning shapes into parts with equal areas"),
        ("unitarea", "Name each part as a unit fraction", "Expressing the area of each part as a unit fraction of the whole"))},
}

DIR_SOLVE = "Listen to each problem. Solve it on your paper. Tell your teacher how you solved it."
DIR_EQ = "Listen to each problem. Write an equation on your paper with a letter for the number you do not know. Then solve it."
LET = "ABCDE"


def pl(n, one, many):
    return "%d %s" % (n, one if n == 1 else many)


# ------------------------------------------------------------------ OA.D.8
def nouns(lp, r):
    n = list(THEME[lp][0])
    r.shuffle(n)
    return n


def two_step(r, kind, x, n0, n1):
    """returns text, equation (with letter n), answer, steps"""
    if kind == "multadd":
        a = r.randint(3, 9); k = r.randint(3, 8); b = r.randint(4, 19)
        ans = a * k + b
        return ("%s puts %d %s in each of %d bags. Then %s adds %d more %s. How many %s does %s have in all?" % (n0, a, x, k, n0, b, x, x, n0),
                "%d × %d + %d = n" % (k, a, b), ans, "%d × %d = %d, then %d + %d = %d" % (k, a, k * a, k * a, b, ans))
    if kind == "multsub":
        a = r.randint(4, 9); k = r.randint(3, 8); b = r.randint(3, 15)
        ans = a * k - b
        return ("%s has %d boxes with %d %s in each box. %s gives %d %s to %s. How many %s does %s have left?" % (n0, k, a, x, n0, b, x, n1, x, n0),
                "%d × %d - %d = n" % (k, a, b), ans, "%d × %d = %d, then %d - %d = %d" % (k, a, k * a, k * a, b, ans))
    if kind == "divadd":
        k = r.randint(3, 8); q = r.randint(3, 9); b = r.randint(2, 9)
        T = k * q
        ans = q + b
        return ("%d %s are shared equally among %d children. Then each child finds %d more %s. How many %s does each child have now?" % (T, x, k, b, x, x),
                "%d ÷ %d + %d = n" % (T, k, b), ans, "%d ÷ %d = %d, then %d + %d = %d" % (T, k, q, q, b, ans))
    if kind == "adddiv":
        k = r.randint(3, 8); q = r.randint(4, 12); T = k * q
        a = r.randint(max(5, T // 3), T - 5); b = T - a
        return ("%s has %d %s and %s has %d %s. They put all of them into %d equal groups. How many %s are in each group?" % (n0, a, x, n1, b, x, k, x),
                "(%d + %d) ÷ %d = n" % (a, b, k), q, "%d + %d = %d, then %d ÷ %d = %d" % (a, b, T, T, k, q))
    if kind == "submult":
        a = r.randint(15, 30); b = r.randint(4, 12); m = r.randint(3, 6)
        ans = (a - b) * m
        return ("%s had %d %s and lost %d of them. %s has %d times as many %s as %s has now. How many %s does %s have?" % (n0, a, x, b, n1, m, x, n0, x, n1),
                "(%d - %d) × %d = n" % (a, b, m), ans, "%d - %d = %d, then %d × %d = %d" % (a, b, a - b, a - b, m, ans))
    if kind == "multdiv":
        m = r.randint(3, 6); q = r.randint(3, 8); T = m * q
        facs = [(k, T // k) for k in range(2, 10) if T % k == 0 and 3 <= T // k <= 10]
        k, a = r.choice(facs)
        return ("%d trays hold %d %s each. All the %s are put into %d equal groups. How many %s are in each group?" % (k, a, x, x, m, x),
                "%d × %d ÷ %d = n" % (k, a, m), q, "%d × %d = %d, then %d ÷ %d = %d" % (k, a, T, T, m, q))
    raise ValueError(kind)


KINDS = ["multadd", "multsub", "divadd", "adddiv", "submult", "multdiv"]


def pick_kinds(r, lp, shift):
    ks = KINDS[:]
    off = (lp + shift) % 6
    ks = ks[off:] + ks[:off]
    return ks[:3] if lp % 2 else [ks[0], ks[2], ks[4]]


def b_solve2(lp, r):
    xs = nouns(lp, r)
    qs, key = [], []
    for i, k in enumerate(pick_kinds(r, lp, 0)):
        t, eq, ans, steps = two_step(r, k, xs[i % 3], nm(lp, i), nm(lp, i + 1))
        qs.append(t); key.append("%d. Steps: %s." % (ans, steps))
    return dict(qs=qs, key=key, dir=DIR_SOLVE, dur=190)


def b_equation(lp, r):
    xs = nouns(lp, r)
    qs, key = [], []
    for i, k in enumerate(pick_kinds(r, lp, 2)):
        t, eq, ans, steps = two_step(r, k, xs[i % 3], nm(lp, i + 1), nm(lp, i + 2))
        qs.append(t + " Write an equation with a letter for the unknown.")
        key.append("%s, so n = %d. Any letter works. Steps: %s." % (eq, ans, steps))
    return dict(qs=qs, key=key, dir=DIR_EQ, dur=200)


def wrong_for(kind, r, text_ans, steps_first):
    return None


def b_mental(lp, r):
    xs = nouns(lp, r)
    qs, key = [], []
    ks = pick_kinds(r, lp, 1)
    verdict = [True, False, False] if lp % 2 else [False, True, False]
    for i, k in enumerate(ks):
        t, eq, ans, steps = two_step(r, k, xs[i % 3], nm(lp, i), nm(lp, i + 1))
        if verdict[i]:
            said = ans
        else:
            said = ans + r.choice([-10, 10, 20, -20, 5, -5]) if r.random() < 0.5 else ans * 2 + 1
            if said <= 0 or said == ans:
                said = ans + 10
        qs.append("%s %s says the answer is %d. Use mental math to check each step. Is that answer reasonable?" % (t, nm(lp, i + 2), said))
        if verdict[i]:
            key.append("Yes. %d is right. Mental math steps: %s." % (ans, steps))
        else:
            key.append("No. The answer should be %d, not %d. Mental math steps: %s." % (ans, said, steps))
    return dict(qs=qs, key=key, dir="Listen to each problem. Use mental math to check the answer. Tell your teacher if it is reasonable and why.", dur=190)


def r10(v):
    return int(round(v / 10.0)) * 10


def verdict_line(said, exact, est, how, place_txt=""):
    """Key text. said==exact means a reasonable answer; otherwise said is far from the estimate."""
    if said == exact:
        return "Yes. %s. The exact answer is %d, so %d is reasonable." % (how, exact, said)
    return "No. %s. %d is not close to %d, so it is not reasonable. The exact answer is %d." % (how, said, est, exact)


def wrong_of(r, exact):
    d = max(40, int(exact * 0.35))
    d = d - d % 10 if d > 20 else d
    return exact + r.choice([d, -d]) if exact - d > 10 else exact + d


def est_set(r, x, nme, which):
    if which == "mult":
        k = r.randint(5, 9); a = r.choice([38, 39, 41, 42, 48, 49, 51, 52, 58, 59, 61]); b = r.randint(11, 19)
        exact = k * a - b
        txt = "%s has %d boxes with %d %s in each box. %s gives away %d. How many %s are left?" % (nme, k, a, x, nme, b, x)
        est = k * r10(a) - r10(b)
        how = "Friendly numbers: %d × %d is about %d, and %d is about %d. So about %d - %d = %d" % (k, r10(a), k * r10(a), b, r10(b), k * r10(a), r10(b), est)
        return txt, exact, est, how
    if which == "chain":
        a = r.randint(231, 489); b = r.randint(112, 198); c = r.randint(61, 118)
        exact = a + b - c
        txt = "%s has %d %s. %s buys %d more and then gives away %d. How many %s does %s have now?" % (nme, a, x, nme, b, c, x, nme)
        est = r10(a) + r10(b) - r10(c)
        how = "Friendly numbers: about %d + %d - %d = %d" % (r10(a), r10(b), r10(c), est)
        return txt, exact, est, how
    k = r.choice([2, 4, 5]); q = r.randint(21, 49); T = k * q
    while T % 10 == 0:
        q = r.randint(21, 49); T = k * q
    exact = q
    txt = "%d %s are shared equally among %d classes. How many %s does each class get?" % (T, x, k, x)
    est = int(round(r10(T) / float(k)))
    how = "Friendly numbers: %d is about %d, and %d ÷ %d is about %d" % (T, r10(T), r10(T), k, est)
    return txt, exact, est, how


def b_estimate(lp, r):
    xs = nouns(lp, r)
    order = ["mult", "chain", "div"]
    r.shuffle(order)
    verdict = [True, False, True] if lp % 2 else [False, True, False]
    qs, key = [], []
    for i, w in enumerate(order):
        t, exact, est, how = est_set(r, xs[i % 3], nm(lp, i), w)
        said = exact if verdict[i] else wrong_of(r, exact)
        qs.append("%s %s says %d. Use an estimation strategy, like friendly numbers. Is that reasonable?" % (t, nm(lp, i + 2), said))
        key.append(verdict_line(said, exact, est, how))
    return dict(qs=qs, key=key, dir="Listen to each problem. Estimate to check the answer. Tell your teacher if it is reasonable and how you know.", dur=200)


def b_rounding(lp, r):
    xs = nouns(lp, r)
    plan = [("add", 100), ("add", 10), ("sub", 100)]
    verdict = [True, False, False] if lp % 2 == 0 else [False, True, False]
    qs, key = [], []
    for i, (op, place) in enumerate(plan):
        nme = nm(lp, i)
        x = xs[i % 3]
        rd = lambda v: int(round(v / float(place))) * place
        if op == "add" and place == 100:
            a = r.randint(231, 689); b = r.randint(142, 398)
        elif op == "add":
            a = r.randint(43, 89); b = r.randint(27, 58)
        else:
            a = r.randint(521, 889); b = r.randint(112, 347)
        if op == "add":
            exact = a + b; est = rd(a) + rd(b)
            txt = "%s has %d %s and gets %d more. How many %s does %s have in all?" % (nme, a, x, b, x, nme)
            how = "Round to the nearest %d: %d + %d = %d" % (place, rd(a), rd(b), est)
        else:
            exact = a - b; est = rd(a) - rd(b)
            txt = "%s has %d %s. %s uses %d of them. How many %s does %s have left?" % (nme, a, x, nme, b, x, nme)
            how = "Round to the nearest %d: %d - %d = %d" % (place, rd(a), rd(b), est)
        if verdict[i]:
            said = exact
        else:
            d = 100 if place == 100 else 30
            said = exact + r.choice([d, 2 * d]) if exact - d < 20 else exact + r.choice([d, -d, 2 * d])
        qs.append("%s %s says %d. Round the numbers to the nearest %d to estimate. Is that reasonable?" % (txt, nm(lp, i + 2), said, place))
        key.append(verdict_line(said, exact, est, how))
    return dict(qs=qs, key=key, dir="Listen to each problem. Round the numbers, estimate, and tell your teacher if the answer is reasonable.", dur=180)


# ------------------------------------------------------------------ fractions
def colour(lp):
    return THEME[lp][1]


def bar_frac(b, shaded, col, w=240, h=44, label=None):
    cw = w / float(b)
    body = ""
    for i in range(b):
        body += '<rect x="%.1f" y="6" width="%.1f" height="%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (8 + i * cw, cw, h, col if i in shaded else "#fffaf0", INK)
    return svg(w + 16, h + 12, body, "A bar divided into %d equal parts with %d shaded" % (b, len(shaded)))


def bar_uneq(pos, col, w=240, h=44, shaded=(0,)):
    xs = [0] + [p * w for p in pos] + [w]
    body = ""
    for i in range(len(xs) - 1):
        body += '<rect x="%.1f" y="6" width="%.1f" height="%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (8 + xs[i], xs[i + 1] - xs[i], h, col if i in shaded else "#fffaf0", INK)
    return svg(w + 16, h + 12, body, "A bar divided into unequal parts")


def pie_frac(b, shaded, col, R=50):
    cx = cy = R + 6
    body = ""
    for i in range(b):
        a1 = -math.pi / 2 + 2 * math.pi * i / b
        a2 = -math.pi / 2 + 2 * math.pi * (i + 1) / b
        x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        x2, y2 = cx + R * math.cos(a2), cy + R * math.sin(a2)
        large = 1 if (a2 - a1) > math.pi else 0
        if b == 1:
            body += '<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (cx, cy, R, col if i in shaded else "#fffaf0", INK)
        else:
            body += '<path d="M%d %d L%.1f %.1f A%d %d 0 %d 1 %.1f %.1f Z" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (cx, cy, x1, y1, R, R, large, x2, y2, col if i in shaded else "#fffaf0", INK)
    return svg(2 * R + 12, 2 * R + 12, body, "A circle divided into %d equal parts with %d shaded" % (b, len(shaded)))


def numline(b, pts, top=1, w=360):
    """number line from 0 to top, ticks every 1/b, labels at whole numbers, points as {letter: numerator over b}"""
    x0 = 20; L = w - 40
    n = b * top
    body = '<line x1="%d" y1="56" x2="%d" y2="56" stroke="%s" stroke-width="3"/>' % (x0, x0 + L, INK)
    for i in range(n + 1):
        x = x0 + L * i / float(n)
        big = (i % b == 0)
        body += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.5"/>' % (x, 46 if big else 49, x, 66 if big else 63, INK)
        if big:
            body += '<text x="%.1f" y="86" font-size="15" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%d</text>' % (x, INK, i // b)
    for L_, num in pts.items():
        x = x0 + L * num / float(n)
        body += '<circle cx="%.1f" cy="56" r="7" fill="#c0392b" stroke="%s" stroke-width="2"/>' % (x, INK)
        body += '<text x="%.1f" y="36" font-size="16" font-weight="800" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (x, INK, L_)
    return svg(w, 96, body, "A number line from 0 to %d" % top)


def b_unit(lp, r):
    col = colour(lp)
    bs = r.sample([3, 4, 5, 6, 8], 3)
    b1, b2, b3 = bs
    pos = [0.14, 0.44, 0.78] if b2 == 4 else [0.2, 0.6]
    fig1 = bar_frac(b1, {0}, col)
    cuts = r.choice([[0.2, 0.55, 0.8], [0.15, 0.4, 0.75], [0.3, 0.45, 0.85]])
    fig2 = bar_uneq(cuts, col)
    fig3 = pie_frac(b3, {0}, col)
    figs = [("A", fig1), ("B", fig2), ("C", fig3)]
    qs = ["Shape A is a whole cut into equal parts. What fraction of the whole is the shaded part? Tell what the top number and the bottom number mean.",
          "Shape B is a whole cut into 4 parts. Is the shaded part 1/4 of the whole? Why or why not?",
          "Shape C is a whole cut into equal parts. What fraction is one shaded part? How many of these parts make the whole?"]
    key = ["1/%d. The bottom number says the whole is cut into %d equal parts. The top number says 1 of those parts is shaded." % (b1, b1),
           "No. The 4 parts are not equal in size, so one part is not 1/4. A unit fraction needs equal parts.",
           "1/%d. It takes %d of these parts to make the whole." % (b3, b3)]
    return dict(qs=qs, key=key, dir="Look at the three shapes. Your teacher asks about one at a time. Tell about the fraction out loud.", dur=140, html=row(figs))


def b_amountb(lp, r):
    col = colour(lp)
    b1 = r.choice([4, 5, 6, 8]); a1 = r.randint(2, b1 - 1)
    b2 = r.choice([3, 4, 6]); a2 = r.randint(2, b2)
    b3 = r.choice([4, 6, 8]); a3 = r.randint(2, b3 - 1)
    figs = [("A", bar_frac(b1, set(range(a1)), col)), ("B", pie_frac(b2, set(range(a2)), col))]
    qs = ["Shape A is a whole cut into equal parts. What fraction is shaded? How many parts of size 1/%d are shaded?" % b1,
          "Shape B is a whole cut into equal parts. What fraction is shaded? Tell how many parts of size 1/%d make that fraction." % b2,
          "Draw a bar and show %d/%d. Tell how many parts you shaded and how big each part is." % (a3, b3)]
    key = ["%d/%d. It is %d parts, and each part is 1/%d." % (a1, b1, a1, b1),
           "%d/%d. It is %d parts of size 1/%d%s." % (a2, b2, a2, b2, (", which is the whole" if a2 == b2 else "")),
           "The bar is cut into %d equal parts and %d are shaded. Each part is 1/%d." % (b3, a3, b3)]
    return dict(qs=qs, key=key, dir="Look at the two shapes. Your teacher asks about each one, then asks you to draw. Say your answer out loud.", dur=150, html=row(figs))


def b_isnumber(lp, r):
    b1 = r.choice([4, 6, 8]); a1 = r.randint(1, b1 - 1)
    b2 = r.choice([3, 5, 6]); a2 = r.randint(2, b2 - 1)
    b3 = r.choice([4, 8]); a3 = r.randint(1, b3 - 1)
    top2 = 2 if r.random() < 0.5 else 1
    n2 = r.randint(b2 + 1, 2 * b2 - 1) if top2 == 2 else a2
    figs = [("A", numline(b1, {"A": a1})), ("B", numline(b2, {"B": n2}, top=top2)), ("C", numline(b3, {"C": a3}))]
    n2_ = n2
    key2 = "%d/%d. Count %d parts of size 1/%d from 0.%s" % (n2_, b2, n2_, b2, (" It is past 1, so it is more than 1 whole." if n2_ > b2 else ""))
    qs = ["Point A is on a number line from 0 to 1. What number is at point A? Tell how you counted.",
          "Point B is on a number line. What number is at point B? Tell how you know.",
          "Point C is on a number line from 0 to 1. What fraction names the spot? Tell how many parts the line from 0 to 1 is cut into."]
    key = ["%d/%d. The line from 0 to 1 is cut into %d equal parts and A is %d jumps from 0." % (a1, b1, b1, a1),
           key2,
           "%d/%d. The line is cut into %d equal parts, and C is at the end of part %d." % (a3, b3, b3, a3)]
    return dict(qs=qs, key=key, dir="Look at the three number lines. Your teacher asks about one at a time. Name the number at the point.", dur=140, html=row(figs))


def b_drawline(lp, r):
    b1 = r.choice([2, 3, 4]); b2 = r.choice([4, 6, 8]); a2 = r.randint(2, b2 - 1); b3 = r.choice([3, 4, 6]); a3 = r.randint(2, b3)
    qs = ["Draw a number line from 0 to 1 on your paper. Cut it into %d equal parts. Label the point 1/%d. Tell how you found it." % (b1, b1),
          "Draw a number line from 0 to 1 on your paper. Show %d/%d. Tell how many lengths of 1/%d you marked off from 0." % (a2, b2, b2),
          "Draw a number line from 0 to 1 on your paper. Cut it into %d equal parts and label every part. Show where %d/%d is." % (b3, a3, b3)]
    key = ["The line from 0 to 1 is the whole, cut into %d equal parts. The first mark after 0 is 1/%d." % (b1, b1),
           "The line is cut into %d equal parts. Mark off %d lengths of 1/%d from 0. The point is %d/%d." % (b2, a2, b2, a2, b2),
           "Every mark is a multiple of 1/%d: %s. %d/%d is the %s mark%s." % (b3, ", ".join("%d/%d" % (i, b3) for i in range(1, b3 + 1)), a3, b3, a3, " and it lands on 1" if a3 == b3 else "")]
    return dict(qs=qs, key=key, dir="Listen to each question. Draw the number line on your paper. Then tell your teacher about it.", dur=190)


EQ_PAIRS = [(1, 2, 2, 4), (1, 2, 3, 6), (1, 3, 2, 6), (2, 3, 4, 6), (1, 4, 2, 8), (3, 4, 6, 8), (1, 2, 4, 8)]


def b_equiv(lp, r):
    col = colour(lp)
    pr = r.sample(EQ_PAIRS, 1)[0]
    a, b, c, d = pr
    fig = row([("A", bar_frac(b, set(range(a)), col, w=240)), ("B", bar_frac(d, set(range(c)), col, w=240))])
    w1 = r.choice([2, 3, 4, 6, 8])
    w2 = r.randint(2, 4); d2 = r.choice([2, 3, 4])
    qs = ["Look at bar A and bar B. They are the same size. Are the two shaded parts the same amount? Say what two fractions are equal and tell how you know.",
          "Write %d/%d as a whole number. Tell how you know." % (w1, w1),
          "Write the whole number %d as a fraction with %d on the bottom. How do you know it is the same size?" % (w2, d2)]
    key = ["Yes. %d/%d = %d/%d. The same amount of the whole is shaded, even though the number of parts is different." % (a, b, c, d),
           "%d/%d = 1. All %d of the %d equal parts make one whole." % (w1, w1, w1, w1),
           "%d = %d/%d. %d wholes each cut into %d parts gives %d parts of size 1/%d." % (w2, w2 * d2, d2, w2, d2, w2 * d2, d2)]
    return dict(qs=qs, key=key, dir="Look at the two bars. Your teacher asks about them, then asks two more questions. Say your answers out loud.", dur=160, html=fig)


def b_compare(lp, r):
    n1, d1 = r.choice([(3, 8), (5, 6), (2, 5), (3, 4)]); n2 = r.randint(1, d1 - 1)
    while n2 == n1:
        n2 = r.randint(1, d1 - 1)
    da, db = r.sample([3, 4, 5, 6, 8], 2); nn = r.randint(1, min(da, db) - 1)
    nb = r.randint(2, 7); ds = r.choice([4, 6, 8]); nc = r.randint(1, ds - 1)
    sym = lambda x, y: ">" if x > y else "<" if x < y else "="
    big, small = (da, db) if da < db else (db, da)
    qs = ["Compare %d/%d and %d/%d with >, =, or <. Tell how you know." % (n1, d1, n2, d1),
          "Compare %d/%d and %d/%d with >, =, or <. Tell how you know." % (nn, da, nn, db),
          "Compare %d/%d and %d/%d with >, =, or <. Tell how you know. A drawing can help." % (nc, ds, nc + 1 if nc + 1 <= ds else nc, ds)]
    key = ["%d/%d %s %d/%d. Same denominator, so the one with more parts of the same size is greater." % (n1, d1, sym(n1, n2), n2, d1),
           "%d/%d %s %d/%d. Same numerator, so look at the size of the parts. The smaller the denominator, the bigger each part, so %d/%d is greater." % (nn, da, sym(db, da), nn, db, nn, big),
           "%d/%d %s %d/%d. Same denominator, so compare the number of parts." % (nc, ds, sym(nc, nc + 1 if nc + 1 <= ds else nc), nc + 1 if nc + 1 <= ds else nc, ds)]
    return dict(qs=qs, key=key, dir="Listen to each question. Say the comparison and tell how you know.", dur=140)


# ------------------------------------------------------------------ MD.B.4 rulers and line plots
def qfrac(q):
    w, f = divmod(q, 4)
    fr = {0: "", 1: "1/4", 2: "1/2", 3: "3/4"}[f]
    if w and fr:
        return "%d %s" % (w, fr)
    return fr if fr else "%d" % w


def ruler_q(maxin, objs, title=""):
    u = 56
    x0 = 20
    W = maxin * u + 40
    ystrips = 6 + len(objs) * 22
    body = ""
    for i, (lab, qlen) in enumerate(objs):
        y = 6 + i * 22
        body += '<rect x="%d" y="%d" width="%.1f" height="16" rx="5" fill="#f3e3b3" stroke="%s" stroke-width="2"/>' % (x0, y, qlen * u / 4.0, INK)
        if lab:
            body += '<text x="%d" y="%d" font-size="11" font-weight="700" fill="%s" font-family="sans-serif">%s</text>' % (x0 + 6, y + 12, INK, lab)
    ry = ystrips + 10
    body += '<rect x="%d" y="%d" width="%d" height="44" fill="#fffaf0" stroke="%s" stroke-width="2"/>' % (x0, ry, maxin * u, INK)
    for i in range(maxin * 4 + 1):
        x = x0 + i * u / 4.0
        L = 24 if i % 4 == 0 else 17 if i % 2 == 0 else 10
        body += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="%s"/>' % (x, ry, x, ry + L, INK, 2 if i % 4 == 0 else 1.4)
        if i % 4 == 0:
            body += '<text x="%.1f" y="%d" font-size="13" text-anchor="middle" fill="%s" font-family="sans-serif">%d</text>' % (x, ry + 38, INK, i // 4)
    body += '<text x="%d" y="%d" font-size="12" text-anchor="middle" fill="%s" font-family="sans-serif">inches</text>' % (x0 + maxin * u // 2, ry + 58, INK)
    return svg(W, ry + 66, body, "Objects above a ruler marked in inches, halves, and fourths")


def b_measure(lp, r):
    things = r.sample(["pencil", "ribbon", "crayon", "stick", "paper strip", "leaf", "key"], 3)
    qs_len = [r.choice([6, 10, 14, 18]) + 0, r.choice([5, 7, 9, 11, 13, 15, 17]), r.choice([4, 8, 12, 16])]
    # one with a half, one with a fourth, one whole or half
    qs_len = [r.choice([9, 11, 13, 15, 17]), r.choice([10, 14, 18, 22]), r.choice([8, 12, 16, 6])]
    r.shuffle(qs_len)
    figs = [(L + ": " + t, ruler_q(6, [("", q)])) for L, t, q in zip("ABC", things, qs_len)]
    qs = ["How long is the %s in picture %s? Measure to the nearest half or fourth of an inch." % (t, L) for L, t in zip("ABC", things)]
    key = ["%s inches. The right end lines up with the %s mark." % (qfrac(q), qfrac(q)) for q in qs_len]
    return dict(qs=qs, key=key, dir="Look at the three pictures. Your teacher asks about one at a time. Say how long each object is.", dur=130, html=row(figs))


def b_gendata(lp, r):
    sets = []
    for _ in range(3):
        sets.append(sorted(r.sample(range(4, 25), 4)) if False else [r.choice([4, 6, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20]) for _ in range(4)])
    figs = [(L, ruler_q(6, [("%d" % (i + 1), q) for i, q in enumerate(s)])) for L, s in zip("ABC", sets)]
    qs = ["Measure the 4 strips in picture %s. Write each length on your paper as a list. Which length is the longest?" % L for L in "ABC"]
    key = []
    for s in sets:
        lst = ", ".join("%s" % qfrac(q) for q in s)
        key.append("Strips 1 to 4: %s inches. Longest: %s inches." % (lst, qfrac(max(s))))
    return dict(qs=qs, key=key, dir="Look at the three pictures. Measure each strip and write the lengths on your paper. Then tell your teacher.", dur=200, html=row(figs))


def data_set(r, step, n=8, lo=1, hi=5):
    vals = [lo + step * k for k in range(int((hi - lo) / step) + 1)]
    return sorted(r.choice(vals) for _ in range(n))


def fmt_data(vals):
    return ", ".join(qfrac(int(round(v * 4))) for v in vals)


def plot_key(vals):
    from collections import Counter
    c = Counter(vals)
    return "; ".join("%s: %d X%s" % (qfrac(int(round(k * 4))), c[k], "" if c[k] == 1 else "s") for k in sorted(c))


def b_lineplot(lp, r):
    qs, key = [], []
    for step, lo, hi in [(1.0, 1, 5), (0.5, 1, 4), (0.25, 1, 3)]:
        v = data_set(r, step, 8, lo, hi)
        qs.append("These lengths in inches were measured: %s. Make a line plot of the data on your paper." % fmt_data(v))
        key.append("Count of X marks above each length (total 8): %s." % plot_key(v))
    return dict(qs=qs, key=key, dir="Listen to each set of lengths. Draw a line plot on your paper. Put one X above the number line for each length.", dur=240)


def b_lpscale(lp, r):
    qs, key = [], []
    specs = [(1.0, 1, 6), (0.5, 2, 5), (0.25, 3, 4)]
    if lp % 2:
        specs = specs[::-1]
    for step, lo, hi in specs:
        v = data_set(r, step, 8, lo, hi)
        unit = {1.0: "whole numbers", 0.5: "halves", 0.25: "quarters"}[step]
        lo_, hi_ = min(v), max(v)
        qs.append("These lengths in inches were measured: %s. Before you plot, tell me the smallest and largest length. What should the horizontal scale of the line plot look like?" % fmt_data(v))
        key.append("Smallest %s, largest %s. The scale should start at or below %s and go to or past %s, marked off in %s (%s inch between marks)." % (qfrac(int(round(lo_ * 4))), qfrac(int(round(hi_ * 4))), qfrac(int(round(lo_ * 4))), qfrac(int(round(hi_ * 4))), unit, {1.0: "1", 0.5: "1/2", 0.25: "1/4"}[step]))
    return dict(qs=qs, key=key, dir="Listen to each set of lengths. Tell your teacher what the number line for the line plot needs. Draw it if you like.", dur=170)


# ------------------------------------------------------------------ G.A.2
def rect_cuts(cuts_x=(), cuts_y=(), col=None, shade=None, w=240, h=120, diag=False):
    body = '<rect x="8" y="8" width="%d" height="%d" fill="#fffaf0" stroke="%s" stroke-width="3"/>' % (w, h, INK)
    if shade is not None:
        x0, x1 = shade
        body += '<rect x="%.1f" y="8" width="%.1f" height="%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (8 + x0 * w, (x1 - x0) * w, h, col, INK)
    for c in cuts_x:
        body += '<line x1="%.1f" y1="8" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.5"/>' % (8 + c * w, 8 + c * w, 8 + h, INK)
    for c in cuts_y:
        body += '<line x1="8" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="2.5"/>' % (8 + c * h, 8 + w, 8 + c * h, INK)
    if diag:
        body += '<line x1="8" y1="8" x2="%d" y2="%d" stroke="%s" stroke-width="2.5"/><line x1="%d" y1="8" x2="8" y2="%d" stroke="%s" stroke-width="2.5"/>' % (8 + w, 8 + h, INK, 8 + w, 8 + h, INK)
    return svg(w + 16, h + 16, body, "A rectangle cut into parts")


def b_partition(lp, r):
    col = colour(lp)
    cuts = r.choice([[0.2, 0.45, 0.8], [0.15, 0.5, 0.7], [0.3, 0.55, 0.9]])
    figA = rect_cuts(cuts_x=cuts)
    figB = rect_cuts(w=160, h=160, diag=True)
    figC = rect_cuts(w=240, h=120)
    n = r.choice([3, 4, 6, 8])
    qs = ["Shape A is cut into 4 parts. Do the parts have equal areas? How do you know?",
          "Shape B is a square cut into 4 parts. Do the parts have equal areas? Tell how you know.",
          "Shape C is a whole. Draw lines on your paper to partition a copy of it into %d parts with equal areas. Tell how you know they are equal." % n]
    key = ["No. The parts are different widths and the same height, so the areas are not equal.",
           "Yes. The two diagonals cut the square into 4 triangles of the same size, so the areas are equal.",
           "Cut it into %d parts that are the same size, for example %s. Each part covers the same amount of the whole." % (n, {3: "3 equal strips", 4: "4 equal strips or 2 by 2 squares", 6: "3 by 2 equal rectangles", 8: "4 by 2 equal rectangles"}[n])]
    return dict(qs=qs, key=key, dir="Look at the three shapes. Your teacher asks about one at a time. Tell about the parts and draw when asked.", dur=170, html=row([("A", figA), ("B", figB), ("C", figC)]))


def b_unitarea(lp, r):
    col = colour(lp)
    n1, n2 = r.sample([2, 3, 4, 6, 8], 2)
    n3 = r.choice([3, 4, 5, 6])
    figs = []
    figA = rect_cuts(cuts_x=[i / float(n1) for i in range(1, n1)], shade=(0, 1.0 / n1), col=col)
    figB = rect_cuts(cuts_x=[i / float(n2) for i in range(1, n2)], shade=(0, 1.0 / n2), col=col)
    if n3 in (4, 6, 8):
        pass
    figC = pie_frac(n3, {0}, col)
    qs = ["Shape A is cut into equal parts. The shaded part is one part. What fraction of the whole is its area?",
          "Shape B is cut into equal parts. What fraction of the whole is the area of one part? Tell how you know.",
          "Shape C is cut into equal parts. What unit fraction names the area of each part?"]
    key = ["1/%d of the whole." % n1, "1/%d of the whole. The whole is cut into %d equal parts, so each part has area 1/%d." % (n2, n2, n2), "1/%d. Each of the %d equal parts is 1/%d of the whole." % (n3, n3, n3)]
    return dict(qs=qs, key=key, dir="Look at the three shapes. Your teacher asks about one at a time. Name the fraction of the whole.", dur=140, html=row([("A", figA), ("B", figB), ("C", figC)]))


BUILD = {
    ("3.OA.D.8", "solve2"): b_solve2, ("3.OA.D.8", "equation"): b_equation, ("3.OA.D.8", "mental"): b_mental,
    ("3.OA.D.8", "estimate"): b_estimate, ("3.OA.D.8", "rounding"): b_rounding,
    ("3.NF.A.1", "unit"): b_unit, ("3.NF.A.1", "amountb"): b_amountb,
    ("3.NF.A.2", "isnumber"): b_isnumber, ("3.NF.A.2", "drawline"): b_drawline,
    ("3.NF.A.3", "equiv"): b_equiv, ("3.NF.A.3", "compare"): b_compare,
    ("3.MD.B.4", "measure"): b_measure, ("3.MD.B.4", "gendata"): b_gendata, ("3.MD.B.4", "lineplot"): b_lineplot, ("3.MD.B.4", "lpscale"): b_lpscale,
    ("3.G.A.2", "partition"): b_partition, ("3.G.A.2", "unitarea"): b_unitarea,
}


def fixgram(t):
    t = re.sub(r"\b1 tens\b", "1 ten", t)
    t = t.replace("a a ", "a ")
    return t


def build():
    out = {}
    for std, cat in CAT.items():
        for lp in range(1, 11):
            parts = []
            for pid, label, desc in cat["parts"]:
                d = BUILD[(std, pid)](lp, rng_for(lp, std + pid))
                assert len(d["qs"]) == 3 and len(d["key"]) == 3, (std, pid, lp, len(d["qs"]), len(d["key"]))
                d["qs"] = [fixgram(t) for t in d["qs"]]
                d["key"] = [fixgram(t) for t in d["key"]]
                for t in d["qs"] + d["key"] + [d["dir"]]:
                    assert not BAD.search(t), (std, pid, lp, t)
                part = {"id": pid, "title": label, "desc": desc, "qs": d["qs"], "key": d["key"], "dir": d["dir"], "dur": d["dur"]}
                if d.get("html"):
                    assert "—" not in d["html"]
                    part["html"] = d["html"]
                parts.append(part)
            out.setdefault(std, {})[str(lp)] = parts
    return out


def js(data):
    L = ["/* G3MATH-STRANDS-BEGIN (generated by source/tools/gen_g3math.py, edit the generator, not this block) */",
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append("var G3PIC=%s;" % json.dumps(data, ensure_ascii=False))
    L.append(P1.APPLY.replace("G1PIC", "G3PIC"))
    L.append("/* G3MATH-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G3, encoding="utf8").read()
    if "G3MATH-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G3MATH-STRANDS-BEGIN.*?G3MATH-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        s = src.rstrip()
        assert s.endswith("})();"), s[-40:]
        src = s[:-5] + block + "\n})();\n"
    open(G3, "w", encoding="utf8").write(src)
    print("parts:", sum(len(p) for std in data.values() for p in std.values()), "block bytes:", len(block))


if __name__ == "__main__":
    main()
