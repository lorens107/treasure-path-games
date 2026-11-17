"""Builds the parts (strands) for the Grade 6 math standards, all 10 LPs, and writes them into source/gx/g6.js.

The Grade 6 gradebook file in the project has no "I can" lines, so each standard is split by the sub-skills
written inside the CCSS wording (Loren chose this). Every standard gets 2 or more parts.
Run:  python3 source/tools/gen_g6math.py
"""
import json, os, re, sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N
import gen_g1pic as P1
import gen_g5math as G5

G6 = os.path.join(HERE, '..', 'gx', 'g6.js')
THEME, rng_for, nm, BAD = N.THEME, N.rng_for, N.nm, N.BAD
svg, row = P1.svg, P1.row
INK = P1.INK
mixed, fstr, lcm = G5.mixed, G5.fstr, G5.lcm
MINUS = "−"


def C(*p):
    return list(p)


def sg(n):
    """signed integer with a real minus sign"""
    return (MINUS + str(-n)) if n < 0 else str(n)


CAT = {
    "6.RP.A.3": {"desc": "ratio and rate problems with tables, double number lines, unit rates, percents, and unit conversions", "parts": C(
        ("tables", "Ratio tables, double number lines, and graphs", "Solving ratio problems with tables of equivalent ratios, tape diagrams, double number line diagrams, and graphs on the coordinate plane"),
        ("unitrate", "Unit rate problems", "Solving unit rate problems, including unit pricing and constant speed"),
        ("percent", "Percent problems", "Solving percent problems by treating a percent as a rate per 100 and finding the part, the percent, or the whole"),
        ("convert", "Convert measurement units", "Using ratio reasoning to convert measurement units and manipulating and transforming units when multiplying or dividing quantities"))},
    "6.NS.A.1": {"desc": "dividing fractions by fractions and solving word problems that divide fractions", "parts": C(
        ("compute", "Divide fractions by fractions", "Computing quotients of fractions divided by fractions"),
        ("word", "Fraction division word problems", "Solving word problems involving division of fractions by fractions using visual fraction models and equations"))},
    "6.NS.C.5": {"desc": "positive and negative numbers for opposite directions or values", "parts": C(
        ("contexts", "Use positive and negative numbers for real situations", "Using positive and negative numbers to represent quantities in real-world contexts with opposite directions or values"),
        ("zero", "Explain what 0 means in a situation", "Explaining the meaning of 0 in each real-world situation"))},
    "6.NS.C.6": {"desc": "opposites, rational numbers on the number line, and points in the coordinate plane", "parts": C(
        ("opposites", "Opposites of numbers", "Recognizing opposite signs of numbers as locations on opposite sides of 0 on the number line and that the opposite of the opposite of a number is the number itself"),
        ("numberline", "Rational numbers on the number line", "Locating and reading integers and other rational numbers on a number line diagram"),
        ("plane", "Points in all four quadrants", "Locating and naming points in all four quadrants of the coordinate plane using ordered pairs with negative coordinates"))},
    "6.EE.A.1": {"desc": "numerical expressions with whole-number exponents", "parts": C(
        ("write", "Write expressions with exponents", "Writing numerical expressions involving whole-number exponents"),
        ("evaluate", "Evaluate expressions with exponents", "Evaluating numerical expressions involving whole-number exponents"))},
    "6.EE.A.2c": {"desc": "evaluating expressions and formulas at specific values of their variables", "parts": C(
        ("substitute", "Evaluate expressions at given values", "Evaluating expressions at specific values of their variables using the order of operations"),
        ("formula", "Use formulas from real-world problems", "Evaluating formulas that arise in real-world problems at specific values of their variables"))},
    "6.EE.C.9": {"desc": "equations and tables for two quantities that change together", "parts": C(
        ("equation", "Write an equation for two quantities", "Using variables and writing an equation to express a dependent variable in terms of an independent variable"),
        ("tables", "Connect equations to tables", "Analyzing the relationship between the dependent and independent variables using tables and relating them to an equation"))},
    "6.G.A.1": {"desc": "area of triangles, special quadrilaterals, and polygons by composing and decomposing", "parts": C(
        ("triangles", "Area of triangles", "Finding the area of right triangles and other triangles by composing into rectangles or decomposing into triangles"),
        ("quads", "Area of special quadrilaterals", "Finding the area of special quadrilaterals by composing into rectangles or decomposing into triangles and other shapes"),
        ("polygons", "Area of polygons", "Finding the area of polygons by composing into rectangles or decomposing into triangles and other shapes and applying these techniques to real-world problems"))},
    "6.G.A.2": {"desc": "volume of right rectangular prisms with fractional edge lengths", "parts": C(
        ("pack", "Pack a prism with unit fraction cubes", "Finding the volume of a right rectangular prism with fractional edge lengths by packing it with unit cubes of the appropriate unit fraction edge lengths"),
        ("formula", "Volume with the formulas V = l × w × h and V = B × h", "Showing that the volume of a prism with fractional edge lengths is the same as multiplying the edge lengths and applying V = l × w × h and V = B × h"))},
    "6.SP.B.5": {"desc": "summarizing numerical data sets in relation to their context", "parts": C(
        ("observations", "Report the number of observations", "Reporting the number of observations in a numerical data set"),
        ("attribute", "Describe the attribute, how it was measured, and its units", "Describing the nature of the attribute under investigation, including how it was measured and its units of measurement"),
        ("centervar", "Find center and variability", "Giving quantitative measures of center (median and mean) and variability (range, interquartile range, and mean absolute deviation) for a data set"),
        ("choose", "Choose the measure that fits the data", "Relating the choice of measures of center and variability to the shape of the data distribution and the context"))},
}

TEL = "Look at the figures. Your teacher asks about one at a time. Say or write your answer."


def cm(n):
    return "{:,}".format(n)


def pick(pool, k, r):
    p = pool[:]
    r.shuffle(p)
    return p[:k]


# ================================================================== RP.A.3
def b_rp_tables(lp, r):
    a, b = r.choice([(2, 3), (3, 5), (4, 7), (2, 5), (3, 4)])
    x, y, mile = r.choice([(2, 3, 10), (3, 4, 9), (4, 5, 12)])
    c, d = r.choice([(1, 2), (2, 3), (3, 5), (1, 4)])
    n0 = nm(lp, 0)
    qs = ["A recipe uses %d cups of flour for every %d cups of sugar. Make a table of 4 equivalent ratios. How much sugar goes with %d cups of flour?" % (a, b, 5 * a),
          "%s walks %d miles every %d minutes at a steady pace. Draw a double number line. How many miles does %s walk in %d minutes?" % (n0, x, y * 5, n0, y * 20),
          "Use the ratio %d : %d. Write 3 ordered pairs (first number, second number) from a table of equivalent ratios, and plot them on a coordinate plane. What do you notice?" % (c, d)]
    key = ["For example, flour: %d, %d, %d, %d and sugar: %d, %d, %d, %d. With %d cups of flour: %d cups of sugar." % (a, 2 * a, 3 * a, 5 * a, b, 2 * b, 3 * b, 5 * b, 5 * a, 5 * b),
           "%d miles every %d minutes. %d minutes is 4 times %d, so %d × 4 = %d miles." % (x, y * 5, y * 20, y * 5, x, x * 4),
           "(%d, %d), (%d, %d), (%d, %d). The points fall on a straight line that goes through (0, 0)." % (c, d, 2 * c, 2 * d, 3 * c, 3 * d)]
    return dict(qs=qs, key=key, dir="Listen to each problem. Draw the table, number line, or graph on your paper. Then answer.", dur=200)


def b_rp_unitrate(lp, r):
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    u1, n = r.choice([3, 4, 6, 8]), r.choice([4, 6, 8])
    sp, h = r.choice([45, 55, 60, 65, 40]), r.choice([3, 4, 5])
    pg, mn = r.choice([4, 5, 6, 3]), r.choice([6, 8, 9, 12])
    qs = ["%s buys %d notebooks for $%d. What is the unit price per notebook? At that price, how much do %d notebooks cost?" % (n0, n, u1 * n, n + 3),
          "%s drives %d miles in %d hours at a constant speed. What is the speed in miles per hour? How far does %s go in %d hours?" % (n1, sp * h, h, n1, h + 2),
          "%s reads %d pages in %d minutes. How many pages per minute? How many pages in %d minutes?" % (n2, pg * mn, mn, mn + 5)]
    key = ["$%d per notebook ($%d ÷ %d = $%d). %d notebooks cost $%d." % (u1, u1 * n, n, u1, n + 3, u1 * (n + 3)),
           "%d miles per hour (%d ÷ %d = %d). In %d hours: %d × %d = %d miles." % (sp, sp * h, h, sp, h + 2, sp, h + 2, sp * (h + 2)),
           "%d pages per minute (%d ÷ %d = %d). In %d minutes: %d × %d = %d pages." % (pg, pg * mn, mn, pg, mn + 5, pg, mn + 5, pg * (mn + 5))]
    return dict(qs=qs, key=key, dir="Listen to each problem. Find the unit rate first, then use it. Show your work.", dur=190)


def b_rp_percent(lp, r):
    p1, w1 = r.choice([(30, 80), (25, 64), (60, 50), (15, 40), (40, 35)])
    pa, wb = r.choice([(18, 24), (9, 12), (21, 28), (15, 20), (12, 16)])
    p3, part3 = r.choice([(30, 15), (20, 14), (40, 18), (25, 12), (60, 27)])
    n0 = nm(lp, 0)
    qs = ["What is %d%% of %d? Tell how you know that %d%% means %d out of every 100." % (p1, w1, p1, p1),
          "%s answered %d of %d questions correctly. What percent is that?" % (n0, pa, wb),
          "%d is %d%% of a number. What is the whole number?" % (part3, p3)]
    k1 = F(p1 * w1, 100)
    key = ["%s. %d%% is %d/100, so %d/100 × %d = %s." % (mixed(k1) if k1.denominator != 1 else str(k1.numerator), p1, p1, p1, w1, mixed(k1) if k1.denominator != 1 else str(k1.numerator)),
           "%d%%. %d out of %d = %s = %d/100." % (pa * 100 // wb, pa, wb, fstr(F(pa, wb)), pa * 100 // wb),
           "%d. %d%% of the whole is %d, so 1%% is %s and 100%% is %d." % (part3 * 100 // p3, p3, part3, mixed(F(part3, p3)), part3 * 100 // p3)]
    return dict(qs=qs, key=key, dir="Listen to each problem. Think of a percent as a rate per 100. Show your work.", dur=190)


CONV = [("feet", "inches", 12), ("yards", "feet", 3), ("hours", "minutes", 60), ("meters", "centimeters", 100), ("kilograms", "grams", 1000), ("pounds", "ounces", 16), ("gallons", "quarts", 4), ("minutes", "seconds", 60)]
SING = {"feet": "foot", "yards": "yard", "hours": "hour", "meters": "meter", "kilograms": "kilogram", "pounds": "pound", "gallons": "gallon", "minutes": "minute"}


def b_rp_convert(lp, r):
    a, b, c = pick(CONV, 3, r)
    x1, x2, x3 = r.randint(2, 9), r.randint(2, 9), r.randint(2, 6)
    qs = ["Convert %d %s to %s. Use a ratio to show your thinking." % (x1, a[0], a[1]),
          "Convert %d %s to %s. Use a ratio to show your thinking." % (b[2] * x2, b[1], b[0]),
          "A speed is %d feet per second. How many feet per minute is that? Use ratio reasoning." % (x3 * 5)]
    key = ["%d %s. 1 %s = %d %s, so %d × %d = %d." % (x1 * a[2], a[1], SING[a[0]], a[2], a[1], x1, a[2], x1 * a[2]),
           "%d %s. %d %s = 1 %s, so %d ÷ %d = %d." % (x2, b[0], b[2], b[1], SING[b[0]], b[2] * x2, b[2], x2),
           "%d feet per minute. 1 minute = 60 seconds, so %d × 60 = %d." % (x3 * 5 * 60, x3 * 5, x3 * 5 * 60)]
    return dict(qs=qs, key=key, dir="Listen to each problem. Use the unit ratio to convert. Show your work.", dur=170)


# ================================================================== NS.A.1
def b_ns_compute(lp, r):
    out = []
    while len(out) < 3:
        d1, d2 = r.choice([2, 3, 4, 5, 6, 8]), r.choice([2, 3, 4, 5, 6, 8])
        n1, n2 = r.randint(1, d1 - 1), r.randint(1, d2 - 1)
        a, b = F(n1, d1), F(n2, d2)
        if a.denominator == 1 or b.denominator == 1 or (a, b) in [(x, y) for x, y, _ in out] or n1 == n2 and d1 == d2:
            continue
        out.append((a, b, a / b))
    qs = ["Divide %s ÷ %s. Show your work." % (fstr(a), fstr(b)) for a, b, _ in out]
    key = ["%s ÷ %s = %s × %d/%d = %s." % (fstr(a), fstr(b), fstr(a), b.denominator, b.numerator, mixed(q)) for a, b, q in out]
    return dict(qs=qs, key=key, dir="Listen to each question. Show each step on your paper.", dur=170)


def b_ns_word(lp, r):
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    s1, k1 = r.choice([F(3, 4), F(2, 3), F(1, 2)]), r.choice([4, 6, 8])
    tot1 = s1 * k1
    a2, p2 = r.choice([(F(5, 6), F(1, 12)), (F(3, 4), F(1, 8)), (F(2, 3), F(1, 6))])
    wd3, ln3 = r.choice([(F(3, 4), F(5, 2)), (F(2, 3), F(3, 2)), (F(1, 2), F(7, 4))])
    qs = ["%s has %s cups of juice. Each glass holds %s cup. How many glasses can %s fill? Write an equation." % (n0, mixed(tot1), fstr(s1), n0),
          "%s has a ribbon that is %s yard long. %s cuts pieces that are %s yard long. How many pieces does %s get? Write an equation." % (n1, fstr(a2), n1, fstr(p2), n1),
          "A rectangle has an area of %s square feet and a width of %s foot. What is its length? Write an equation." % (mixed(wd3 * ln3), fstr(wd3))]
    key = ["%d glasses. %s ÷ %s = %d." % (k1, mixed(tot1), fstr(s1), k1),
           "%s pieces. %s ÷ %s = %s." % (mixed(a2 / p2), fstr(a2), fstr(p2), mixed(a2 / p2)),
           "%s feet. %s × ? = %s, so ? = %s ÷ %s = %s." % (mixed(ln3), fstr(wd3), mixed(wd3 * ln3), mixed(wd3 * ln3), fstr(wd3), mixed(ln3))]
    return dict(qs=qs, key=key, dir="Listen to each problem. Draw a model or write an equation, then solve.", dur=200)


# ================================================================== NS.C.5
def b_ns_contexts(lp, r):
    pool = [("a temperature of %d degrees above zero", "a temperature of %d degrees below zero", "+", "−"),
            ("an elevation of %d feet above sea level", "an elevation of %d feet below sea level", "+", "−"),
            ("a deposit of $%d into an account", "a withdrawal of $%d from an account", "+", "−"),
            ("a gain of %d yards in football", "a loss of %d yards in football", "+", "−"),
            ("%d points earned in a game", "%d points lost in a game", "+", "−")]
    its = pick(pool, 3, r)
    qs, key = [], []
    for up, dn, _, _ in its:
        a, b = r.randint(2, 40), r.randint(2, 40)
        qs.append("Write a positive or negative number for each situation: %s, and %s." % (up % a, dn % b))
        key.append("+%d (or %d) for the first. %s%d for the second." % (a, a, MINUS, b))
    return dict(qs=qs, key=key, dir="Listen to each question. Write a number with a sign for each situation.", dur=140)


ZERO = [("the temperature in degrees Celsius", "the freezing point of water, 0 degrees"), ("the elevation in feet", "sea level, neither above nor below it"),
        ("a bank account balance", "no money in the account, neither saved nor owed"), ("the change in a student's weight in pounds", "no change in weight"),
        ("a team's score difference", "the teams are tied"), ("the number of floors above or below ground level", "ground level")]


def b_ns_zero(lp, r):
    its = pick(ZERO, 3, r)
    qs = ["Positive and negative numbers describe %s. What does 0 mean in this situation? What does a number greater than 0 mean? What does a number less than 0 mean?" % t for t, _ in its]
    key = ["0 means %s. Greater than 0 is on one side of 0, and less than 0 is on the opposite side." % z for _, z in its]
    return dict(qs=qs, key=key, dir="Listen to each question. Tell what 0 means, then what the positive and negative numbers mean.", dur=170)


# ================================================================== NS.C.6
def b_ns_opposites(lp, r):
    a, b, c = r.sample(range(2, 12), 3)
    qs = ["What is the opposite of %s? What is the opposite of %d? Where are they on the number line compared to 0?" % (sg(-a), a),
          "What is the opposite of the opposite of %s? Use the number line to explain. Write it with symbols." % sg(b),
          "Which number is its own opposite? Then tell what −(−%d) equals." % c]
    key = ["The opposite of %s is %d, and the opposite of %d is %s. They are the same distance from 0 on opposite sides." % (sg(-a), a, a, sg(-a)),
           "%s. The opposite of %s is %s, and flipping across 0 again gets back to %s. −(−%s) = %s." % (sg(b), sg(b), sg(-b), sg(b), sg(b), sg(b)),
           "0 is its own opposite. −(−%d) = %d." % (c, c)]
    return dict(qs=qs, key=key, dir="Listen to each question. Think about the number line. Say your answer out loud.", dur=160)


def numline_fig(pts, lo=-6, hi=6):
    w = 36 * (hi - lo) + 40
    ox = 20
    body = '<line x1="%d" y1="60" x2="%d" y2="60" stroke="%s" stroke-width="3"/>' % (ox - 8, ox + 36 * (hi - lo) + 8, INK)
    for i in range(lo, hi + 1):
        x = ox + (i - lo) * 36
        body += '<line x1="%d" y1="52" x2="%d" y2="68" stroke="%s" stroke-width="2.5"/>' % (x, x, INK)
        body += '<text x="%d" y="88" font-size="14" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (x, INK, sg(i))
    for L, v in pts.items():
        x = ox + (v - lo) * 36
        body += '<circle cx="%.1f" cy="60" r="7" fill="#c0392b" stroke="%s" stroke-width="2"/>' % (x, INK)
        body += '<text x="%.1f" y="40" font-size="17" font-weight="800" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (x, INK, L)
    return svg(w, 100, body, "A number line from %d to %d" % (lo, hi))


def b_ns_numberline(lp, r):
    a = r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    b = r.choice([x for x in (-5.5, -4.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5)])
    cpt = r.choice([x for x in (-6, -3, 0, 3, 6) if x != a])
    fig = numline_fig({"A": a, "B": b})

    def fmt(v):
        if float(v).is_integer():
            return sg(int(v))
        return (MINUS if v < 0 else "") + "%d 1/2" % int(abs(v)) if abs(v) >= 1 else (MINUS if v < 0 else "") + "1/2"
    d = r.choice([-4, -3, -2, 2, 3, 4])
    qs = ["Look at the number line. What number is at point A?", "What number is at point B? Tell which two integers it is between.", "On your paper, draw a number line from %s to 6. Plot and label the number %s." % (MINUS + "6", sg(d))]
    key = [fmt(a) + ".", "%s. It is between %s and %s." % (fmt(b), sg(int(b // 1)), sg(int(b // 1) + 1)), "Draw a line with 0 in the middle. %s goes %d spaces %s of 0." % (sg(d), abs(d), "left" if d < 0 else "right")]
    return dict(qs=qs, key=key, dir="Look at the number line. Your teacher asks the questions. Say or draw your answers.", dur=160, html=row([("", fig)]))


def grid4(pts, n=6, c=24):
    M = 26
    W = 2 * n * c + 2 * M
    H = 2 * n * c + 2 * M
    ox = oy = n * c + M
    body = ""
    for i in range(-n, n + 1):
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#d6cfc2" stroke-width="1"/>' % (ox + i * c, M, ox + i * c, H - M)
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#d6cfc2" stroke-width="1"/>' % (M, oy + i * c, W - M, oy + i * c)
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (M - 8, oy, W - M + 8, oy, INK)
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (ox, M - 8, ox, H - M + 8, INK)
    for i in range(-n, n + 1):
        if i:
            body += '<text x="%d" y="%d" font-size="11" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (ox + i * c, oy + 14, INK, sg(i))
            body += '<text x="%d" y="%d" font-size="11" font-weight="700" text-anchor="end" fill="%s" font-family="sans-serif">%s</text>' % (ox - 4, oy - i * c + 4, INK, sg(i))
    for L, (x, y) in pts.items():
        body += '<circle cx="%d" cy="%d" r="6" fill="#c0392b" stroke="%s" stroke-width="2"/>' % (ox + x * c, oy - y * c, INK)
        body += '<text x="%d" y="%d" font-size="15" font-weight="800" fill="%s" stroke="#ffffff" stroke-width="3" paint-order="stroke" font-family="sans-serif">%s</text>' % (ox + x * c + 8, oy - y * c - 8, INK, L)
    return svg(W, H, body, "A coordinate plane with all four quadrants")


QN = {(1, 1): "I", (-1, 1): "II", (-1, -1): "III", (1, -1): "IV"}


def quad(x, y):
    return QN[(1 if x > 0 else -1, 1 if y > 0 else -1)]


def b_ns_plane(lp, r):
    pts = {}
    qs_used = []
    while len(pts) < 2:
        x, y = r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]), r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        if quad(x, y) not in qs_used:
            qs_used.append(quad(x, y))
            pts["AB"[len(pts)]] = (x, y)
    fig = grid4(pts)
    px, py = r.choice([-7, -6, -4, -3, 5, 6, 8]), r.choice([-9, -5, -2, 3, 7])
    qs = ["Write the ordered pair for point A. Which quadrant is it in?", "Write the ordered pair for point B. Which quadrant is it in?",
          "Point P is at (%s, %s). Without graphing, which quadrant is it in? What are the coordinates of the point when P is reflected across the x-axis?" % (sg(px), sg(py))]
    key = ["(%s, %s). Quadrant %s." % (sg(pts["A"][0]), sg(pts["A"][1]), quad(*pts["A"])), "(%s, %s). Quadrant %s." % (sg(pts["B"][0]), sg(pts["B"][1]), quad(*pts["B"])),
           "Quadrant %s, because the x-coordinate is %s and the y-coordinate is %s. Reflected across the x-axis: (%s, %s)." % (quad(px, py), "positive" if px > 0 else "negative", "positive" if py > 0 else "negative", sg(px), sg(-py))]
    return dict(qs=qs, key=key, dir="Look at the grid. Your teacher asks about the points. Say or write your answers.", dur=190, html=row([("", fig)]))


# ================================================================== EE.A.1
def b_ee_write(lp, r):
    a, k = r.randint(2, 9), r.randint(3, 5)
    b, m = r.choice([2, 5, 10]), r.randint(3, 6)
    c, j = r.randint(2, 6), r.randint(2, 6)
    sup = {2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶"}
    qs = ["Write %s using an exponent." % " × ".join([str(a)] * k),
          "Write %s using an exponent." % " × ".join([str(b)] * m),
          "Write %d%s as repeated multiplication. Then tell what the base and the exponent are." % (c, sup[j])]
    key = ["%d%s." % (a, sup[k]), "%d%s." % (b, sup[m]), "%s. The base is %d and the exponent is %d." % (" × ".join([str(c)] * j), c, j)]
    return dict(qs=qs, key=key, dir="Listen to each question. Write your answer on your paper.", dur=130)


def b_ee_eval(lp, r):
    sup = {2: "²", 3: "³", 4: "⁴"}
    a, e1 = r.randint(2, 6), r.choice([2, 3])
    b, c = r.randint(2, 4), r.randint(2, 6)
    d, e = r.choice([2, 3, 4]), r.choice([6, 8, 9, 12])
    f = r.randint(2, 5)
    qs = ["Evaluate %d%s." % (a, sup[e1]),
          "Evaluate %d³ + %d²." % (b, c),
          "Evaluate %d² ÷ %d + %d³." % (4 if d == 2 else 6, 2 if d == 2 else 3, f)]
    q3a = 4 if d == 2 else 6
    q3b = 2 if d == 2 else 3
    key = ["%d. %s" % (a ** e1, " × ".join([str(a)] * e1) + " = %d" % a ** e1 + "."),
           "%d. %d³ = %d and %d² = %d, so %d + %d = %d." % (b ** 3 + c ** 2, b, b ** 3, c, c ** 2, b ** 3, c ** 2, b ** 3 + c ** 2),
           "%d. %d² = %d, %d ÷ %d = %d, %d³ = %d, so %d + %d = %d." % (q3a ** 2 // q3b + f ** 3, q3a, q3a ** 2, q3a ** 2, q3b, q3a ** 2 // q3b, f, f ** 3, q3a ** 2 // q3b, f ** 3, q3a ** 2 // q3b + f ** 3)]
    return dict(qs=qs, key=key, dir="Listen to each question. Write each step on your paper.", dur=150)


# ================================================================== EE.A.2.c
def b_ee_sub(lp, r):
    a, b, x = r.randint(2, 6), r.randint(2, 9), r.randint(2, 7)
    c, y = r.randint(2, 4), r.randint(2, 5)
    p, z, q = r.randint(2, 4), r.choice([4, 8, 12, 16]), r.randint(2, 5)
    qs = ["Evaluate %dx + %d when x = %d." % (a, b, x),
          "Evaluate %dy² − %d when y = %d." % (c, y, y + 1),
          "Evaluate z ÷ %d + %dw² when z = %d and w = %d." % (4, p, z, q)]
    key = ["%d. %d × %d + %d = %d + %d = %d." % (a * x + b, a, x, b, a * x, b, a * x + b),
           "%d. %d × %d² − %d = %d × %d − %d = %d." % (c * (y + 1) ** 2 - y, c, y + 1, y, c, (y + 1) ** 2, y, c * (y + 1) ** 2 - y),
           "%d. %d ÷ 4 = %d and %d × %d² = %d, so %d + %d = %d." % (z // 4 + p * q * q, z, z // 4, p, q, p * q * q, z // 4, p * q * q, z // 4 + p * q * q)]
    return dict(qs=qs, key=key, dir="Listen to each question. Put the number in for the letter, then use the order of operations.", dur=160)


def b_ee_formula(lp, r):
    s = r.randint(2, 6)
    bb, hh = r.choice([(10, 6), (8, 5), (12, 7), (6, 9)])
    rr, t = r.choice([(45, 3), (55, 4), (60, 2), (50, 5)])
    l, w = r.randint(6, 15), r.randint(3, 9)
    pool = [("The volume of a cube is V = s³. A cube has edges of %d cm. What is its volume?" % s, "%d cubic cm. %d³ = %d." % (s ** 3, s, s ** 3)),
            ("The area of a triangle is A = ½bh. A triangle has a base of %d ft and a height of %d ft. What is its area?" % (bb, hh), "%s square ft. ½ × %d × %d = %s." % (mixed(F(bb * hh, 2)), bb, hh, mixed(F(bb * hh, 2)))),
            ("The distance formula is d = rt. A car goes %d miles per hour for %d hours. How far does it go?" % (rr, t), "%d miles. %d × %d = %d." % (rr * t, rr, t, rr * t)),
            ("The perimeter of a rectangle is P = 2l + 2w. A rectangle is %d in long and %d in wide. What is its perimeter?" % (l, w), "%d inches. 2 × %d + 2 × %d = %d." % (2 * l + 2 * w, l, w, 2 * l + 2 * w)),
            ("The surface area of a cube is S = 6s². A cube has edges of %d inches. What is its surface area?" % s, "%d square inches. 6 × %d² = 6 × %d = %d." % (6 * s * s, s, s * s, 6 * s * s))]
    it = pick(pool, 3, r)
    return dict(qs=[q for q, _ in it], key=[k for _, k in it], dir="Listen to each problem. Put the numbers in the formula and solve. Show your work.", dur=170)


# ================================================================== EE.C.9
def b_ee_equation(lp, r):
    a, b = r.randint(2, 5), r.randint(3, 9)
    c = r.randint(4, 9)
    d, e = r.randint(2, 4), r.randint(3, 8)
    qs = ["A plant is %d inches tall and grows %d inches each week. Let w be the number of weeks and h be the height. Which variable is independent and which is dependent? Write an equation for h in terms of w." % (b, a),
          "A movie ticket costs $%d. Let n be the number of tickets and c be the total cost. Which variable is independent? Write an equation for c in terms of n." % c,
          "A taxi charges $%d to start and $%d per mile. Let m be miles and c be the total cost. Write an equation for c in terms of m." % (e, d)]
    key = ["Independent: w (weeks). Dependent: h (height). h = %dw + %d." % (a, b), "Independent: n. Dependent: c. c = %dn." % c, "c = %dm + %d." % (d, e)]
    return dict(qs=qs, key=key, dir="Listen to each problem. Write the equation on your paper.", dur=160)


def b_ee_tables(lp, r):
    a, b = r.randint(2, 6), r.choice([0, 1, 2, 3, 4, 5])
    xs = [1, 2, 3, 4]
    ys = [a * x + b for x in xs]
    a2 = r.randint(3, 9)
    ys2 = [a2 * x for x in (1, 2, 3)]
    a3, b3 = r.randint(2, 5), r.randint(1, 6)
    xs3 = [2, 4, 6, 8]
    qs = ["x: %s. y: %s. Write an equation that shows how y depends on x. What is y when x = 10?" % (", ".join(map(str, xs)), ", ".join(map(str, ys))),
          "A graph has the points (1, %d), (2, %d), (3, %d). Write an equation for y in terms of x. By how much does y change when x goes up by 1?" % tuple(ys2),
          "t: %s. d: %s. Write an equation for d in terms of t. What is d when t = 20?" % (", ".join(map(str, xs3)), ", ".join(str(a3 * t + b3) for t in xs3))]
    eq1 = "y = %dx" % a + (" + %d" % b if b else "")
    key = ["%s. When x = 10, y = %d." % (eq1, a * 10 + b), "y = %dx. y goes up by %d each time x goes up by 1." % (a2, a2), "d = %dt + %d. When t = 20, d = %d." % (a3, b3, a3 * 20 + b3)]
    return dict(qs=qs, key=key, dir="Listen to each problem. Look at the pattern in the table or graph. Write the equation.", dur=170)


# ================================================================== G.A.1
def T(x, y, s, a="middle", sz=13, fw=700):
    return '<text x="%.1f" y="%.1f" font-size="%d" font-weight="%d" text-anchor="%s" fill="%s" font-family="sans-serif">%s</text>' % (x, y, sz, fw, a, INK, s)


def poly(pts, fill):
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (" ".join("%.1f,%.1f" % p for p in pts), fill, INK)


def dash(x1, y1, x2, y2):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#c0392b" stroke-width="2.5" stroke-dasharray="6,4"/>' % (x1, y1, x2, y2)


def tri_fig(kind, b, h, col):
    sc = 120.0 / max(b, h)
    bs, hs = b * sc, h * sc
    X0, Y0 = 20, 20 + hs
    if kind == "right":
        pts = [(X0, Y0), (X0 + bs, Y0), (X0, Y0 - hs)]
        body = poly(pts, col) + T(X0 + bs / 2, Y0 + 18, "%d" % b) + T(X0 - 6, Y0 - hs / 2, "%d" % h, "end")
        body += '<rect x="%d" y="%d" width="10" height="10" fill="none" stroke="%s" stroke-width="2"/>' % (X0, Y0 - 10, INK)
        W = bs + 60
    else:
        ap = X0 + bs * 0.35
        pts = [(X0, Y0), (X0 + bs, Y0), (ap, Y0 - hs)]
        body = poly(pts, col) + dash(ap, Y0 - hs, ap, Y0) + T(X0 + bs / 2, Y0 + 18, "%d" % b) + T(ap + 6, Y0 - hs / 2, "%d" % h, "start")
        W = bs + 60
    return svg(int(W), int(hs + 44), body, "A triangle with base %d and height %d" % (b, h))


def b_g_triangles(lp, r):
    from gen_g3math import colour
    col = colour(lp)
    b1, h1 = r.choice([(6, 8), (8, 6), (10, 4), (12, 5), (6, 5)])
    b2, h2 = r.choice([(10, 6), (8, 7), (12, 4), (9, 8), (14, 5)])
    b3, h3 = r.choice([(6, 4), (8, 3), (10, 5)])
    figs = [("A", tri_fig("right", b1, h1, col)), ("B", tri_fig("acute", b2, h2, col))]
    qs = ["Triangle A is a right triangle. Find its area in square units. Tell how a rectangle helps you.",
          "Triangle B is not a right triangle. The dashed line is its height. Find its area in square units.",
          "A rectangle is %d units by %d units. It is cut along a diagonal into two right triangles. What is the area of one triangle? Explain." % (b3, h3)]
    key = ["%s square units. Two copies make a %d by %d rectangle (area %d), so one triangle is half: %d ÷ 2 = %s." % (mixed(F(b1 * h1, 2)), b1, h1, b1 * h1, b1 * h1, mixed(F(b1 * h1, 2))),
           "%s square units. A = ½ × %d × %d = %s." % (mixed(F(b2 * h2, 2)), b2, h2, mixed(F(b2 * h2, 2))),
           "%d square units. The rectangle has area %d × %d = %d, and the two triangles are the same size, so each is half: %d." % (b3 * h3 // 2, b3, h3, b3 * h3, b3 * h3 // 2)]
    return dict(qs=qs, key=key, dir=TEL, dur=190, html=row(figs))


def para_fig(b, h, side, col):
    sc = 120.0 / max(b, h)
    bs, hs = b * sc, h * sc
    off = bs * 0.28
    X0, Y0 = 20, 20 + hs
    pts = [(X0, Y0), (X0 + bs, Y0), (X0 + bs + off, Y0 - hs), (X0 + off, Y0 - hs)]
    body = poly(pts, col) + dash(X0 + off, Y0 - hs, X0 + off, Y0) + T(X0 + bs / 2, Y0 + 18, "%d" % b) + T(X0 + off + 6, Y0 - hs / 2 + 4, "%d" % h, "start")
    body += T(X0 + bs + off / 2 + 16, Y0 - hs / 2, "%d" % side, "start")
    return svg(int(bs + off + 70), int(hs + 44), body, "A parallelogram")


def trap_fig(b1, b2, h, col):
    sc = 150.0 / max(b2, h)
    t, bo, hs = b1 * sc, b2 * sc, h * sc
    X0, Y0 = 20, 20 + hs
    off = (bo - t) / 2
    pts = [(X0, Y0), (X0 + bo, Y0), (X0 + off + t, Y0 - hs), (X0 + off, Y0 - hs)]
    body = poly(pts, col) + dash(X0 + off, Y0 - hs, X0 + off, Y0) + T(X0 + off + t / 2, Y0 - hs - 6, "%d" % b1) + T(X0 + bo / 2, Y0 + 18, "%d" % b2) + T(X0 + off + 6, Y0 - hs / 2 + 4, "%d" % h, "start")
    return svg(int(bo + 50), int(hs + 50), body, "A trapezoid")


def b_g_quads(lp, r):
    from gen_g3math import colour
    col = colour(lp)
    b1, h1 = r.choice([(8, 5), (10, 6), (7, 4), (12, 5)])
    side = h1 + r.randint(2, 4)
    t2, b2, h2 = r.choice([(4, 10, 6), (5, 9, 4), (3, 11, 6), (6, 12, 4)])
    b3, h3 = r.choice([(12, 7), (9, 8), (15, 6)])
    figs = [("A", para_fig(b1, h1, side, col)), ("B", trap_fig(t2, b2, h2, col))]
    qs = ["Parallelogram A has a base of %d and a height of %d (the dashed line). Find its area. The slanted side is %d. Do you use it? Why?" % (b1, h1, side),
          "Trapezoid B has parallel sides of %d and %d, and a height of %d. Cut it into a rectangle and two triangles, or use another way, to find its area." % (t2, b2, h2),
          "A garden is shaped like a parallelogram. Its base is %d meters and its height is %d meters. How many square meters is the garden?" % (b3, h3)]
    key = ["%d square units. A = b × h = %d × %d. The slanted side is not used because it is not the height." % (b1 * h1, b1, h1),
           "%s square units. Rectangle %d × %d = %d, plus two triangles with total base %d: ½ × %d × %d = %s. Total %s." % (mixed(F((t2 + b2) * h2, 2)), t2, h2, t2 * h2, b2 - t2, b2 - t2, h2, mixed(F((b2 - t2) * h2, 2)), mixed(F((t2 + b2) * h2, 2))),
           "%d square meters (%d × %d)." % (b3 * h3, b3, h3)]
    return dict(qs=qs, key=key, dir=TEL, dur=210, html=row(figs))


def lshape_fig(W, H, nw, nh, col):
    sc = 130.0 / max(W, H)
    X0, Y0 = 24, 14
    w, h, a, b = W * sc, H * sc, nw * sc, nh * sc
    pts = [(X0, Y0), (X0 + w - a, Y0), (X0 + w - a, Y0 + b), (X0 + w, Y0 + b), (X0 + w, Y0 + h), (X0, Y0 + h)]
    body = poly(pts, col) + T(X0 + w / 2, Y0 + h + 18, "%d" % W) + T(X0 - 6, Y0 + h / 2, "%d" % H, "end") + T(X0 + (w - a) / 2, Y0 - 3, "%d" % (W - nw)) + T(X0 + w - a + 8, Y0 + b / 2 + 4, "%d" % nh, "start")
    return svg(int(w + 60), int(h + 40), body, "An L-shaped polygon")


def house_fig(bw, bh, th, col):
    sc = 130.0 / max(bw, bh + th)
    X0, Y0 = 20, 18 + th * sc
    w, h, t = bw * sc, bh * sc, th * sc
    pts = [(X0, Y0 + h), (X0 + w, Y0 + h), (X0 + w, Y0), (X0 + w / 2, Y0 - t), (X0, Y0)]
    body = poly(pts, col) + '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2"/>' % (X0, Y0, X0 + w, Y0, INK)
    body += dash(X0 + w / 2, Y0 - t, X0 + w / 2, Y0) + T(X0 + w / 2, Y0 + h + 18, "%d" % bw) + T(X0 - 6, Y0 + h / 2, "%d" % bh, "end") + T(X0 + w / 2 + 6, Y0 - t / 2, "%d" % th, "start")
    return svg(int(w + 60), int(h + t + 44), body, "A polygon made of a rectangle and a triangle")


def b_g_polygons(lp, r):
    from gen_g3math import colour
    col = colour(lp)
    W, H, nw, nh = r.choice([(10, 8, 4, 3), (12, 9, 5, 4), (9, 7, 3, 3), (11, 8, 4, 2)])
    bw, bh, th = r.choice([(8, 6, 4), (10, 5, 6), (6, 5, 4), (12, 4, 5)])
    ww, wh, dw, dh = r.choice([(12, 9, 3, 7), (10, 8, 3, 6), (14, 9, 4, 7)])
    figs = [("A", lshape_fig(W, H, nw, nh, col)), ("B", house_fig(bw, bh, th, col))]
    qs = ["Polygon A is an L shape. Find its area. Tell how you split it or how you filled it in.",
          "Polygon B is a rectangle with a triangle on top. The dashed line is the triangle's height. Find the total area.",
          "A wall is %d feet wide and %d feet tall. It has a door that is %d feet wide and %d feet tall. How many square feet of wall need paint?" % (ww, wh, dw, dh)]
    key = ["%d square units. Big rectangle %d × %d = %d, minus the missing corner %d × %d = %d. (Or two rectangles added.)" % (W * H - nw * nh, W, H, W * H, nw, nh, nw * nh),
           "%s square units. Rectangle %d × %d = %d, triangle ½ × %d × %d = %s. Total %s." % (mixed(F(bw * bh) + F(bw * th, 2)), bw, bh, bw * bh, bw, th, mixed(F(bw * th, 2)), mixed(F(bw * bh) + F(bw * th, 2))),
           "%d square feet. Wall %d × %d = %d, door %d × %d = %d, and %d − %d = %d." % (ww * wh - dw * dh, ww, wh, ww * wh, dw, dh, dw * dh, ww * wh, dw * dh, ww * wh - dw * dh)]
    return dict(qs=qs, key=key, dir=TEL, dur=220, html=row(figs))


# ================================================================== G.A.2
def b_g_pack(lp, r):
    its = []
    while len(its) < 3:
        n = r.choice([2, 3, 4])
        a, b, c = r.randint(2, 4) * (1 if n != 2 else 1), r.randint(2, 4), r.randint(2, 4)
        its.append((n, a, b, c))
    qs, key = [], []
    for n, a, b, c in its:
        l, w, h = F(a, n), F(b, n), F(c, n)
        qs.append("A box is %s unit long, %s unit wide, and %s unit tall. It is packed with cubes whose edges are 1/%d unit. How many cubes fit? What is the volume of the box in cubic units?" % (fstr(l) if l.denominator != 1 else str(l.numerator), fstr(w) if w.denominator != 1 else str(w.numerator), fstr(h) if h.denominator != 1 else str(h.numerator), n))
        vol = F(a * b * c, n ** 3)
        key.append("%d cubes (%d × %d × %d). Each cube is 1/%d cubic unit because %d cubes fill 1 cubic unit. Volume: %d × 1/%d = %s cubic unit%s." % (a * b * c, a, b, c, n ** 3, n ** 3, a * b * c, n ** 3, fstr(vol) if vol.denominator != 1 else str(vol.numerator), "" if vol <= 1 else "s"))
    return dict(qs=qs, key=key, dir="Listen to each problem. Think about how many small cubes fill 1 cubic unit. Show your work.", dur=210)


def b_g_vformula(lp, r):
    l1, w1, h1 = r.choice([(F(3, 2), F(1, 2), F(4)), (F(5, 2), F(3, 2), F(2)), (F(3, 4), F(2), F(1, 2)), (F(7, 2), F(1, 2), F(2))])
    B2, h2 = r.choice([(F(3, 4), F(2)), (F(5, 2), F(3, 2)), (F(9, 4), F(4, 3)), (F(3, 2), F(5, 3))])
    l3, w3, h3 = r.choice([(F(5, 2), F(3, 2), F(2)), (F(3, 2), F(3, 2), F(1, 2)), (F(5, 2), F(1, 2), F(4))])
    n0 = nm(lp, 0)
    qs = ["A box is %s foot long, %s foot wide, and %s feet tall. Use V = l × w × h to find the volume." % (mixed(l1), mixed(w1), mixed(h1)),
          "The base of a prism has an area of %s square meters. The prism is %s meters tall. Use V = B × h to find the volume." % (mixed(B2), mixed(h2)),
          "%s fills a fish tank that is %s feet long, %s feet wide, and %s feet tall. How many cubic feet of water does the tank hold?" % (n0, mixed(l3), mixed(w3), mixed(h3))]
    key = ["%s cubic feet. %s × %s × %s = %s." % (mixed(l1 * w1 * h1), fstr(l1) if l1.denominator != 1 else str(l1.numerator), fstr(w1) if w1.denominator != 1 else str(w1.numerator), str(h1.numerator) if h1.denominator == 1 else fstr(h1), mixed(l1 * w1 * h1)),
           "%s cubic meters. %s × %s = %s." % (mixed(B2 * h2), fstr(B2), fstr(h2) if h2.denominator != 1 else str(h2.numerator), mixed(B2 * h2)),
           "%s cubic feet. %s × %s × %s = %s." % (mixed(l3 * w3 * h3), fstr(l3), fstr(w3), fstr(h3) if h3.denominator != 1 else str(h3.numerator), mixed(l3 * w3 * h3))]
    return dict(qs=qs, key=key, dir="Listen to each problem. Write the formula and put the fractions in. Show your work.", dur=200)


# ================================================================== SP.B.5
def b_sp_obs(lp, r):
    sets = []
    for _ in range(3):
        n = r.randint(8, 14)
        sets.append([r.randint(2, 20) for _ in range(n)])
    ctx = ["the number of books 14 students read in a month", "the number of minutes students practiced piano", "the number of pages in a student's reading log each day"]
    qs = ["These are %s: %s. How many observations are in the data set?" % (c, ", ".join(map(str, s))) for c, s in zip(ctx, sets)]
    key = ["%d observations. I counted every value in the list." % len(s) for s in sets]
    qs[0] = "These are the number of books students read in a month: %s. How many observations are in the data set?" % ", ".join(map(str, sets[0]))
    return dict(qs=qs, key=key, dir="Listen to each question. Count carefully. Say the number of observations.", dur=130)


ATTRS = [("Students walked from home to school and a timer recorded how long it took, in minutes.", "The attribute is how long the walk takes. It was measured with a timer. The unit is minutes."),
         ("A class measured the height of bean plants with a ruler, in centimeters.", "The attribute is plant height. It was measured with a ruler. The unit is centimeters."),
         ("A store weighed bags of apples on a scale, in pounds.", "The attribute is the weight of a bag of apples. It was measured with a scale. The unit is pounds."),
         ("A coach recorded how many free throws each player made out of 10 tries.", "The attribute is free throws made. It was counted. The unit is a number of free throws out of 10."),
         ("A nurse used a thermometer to check body temperature in degrees Fahrenheit.", "The attribute is body temperature. It was measured with a thermometer. The unit is degrees Fahrenheit."),
         ("Students counted how many pets they have at home.", "The attribute is the number of pets. It was counted by asking each student. The unit is pets.")]


def b_sp_attr(lp, r):
    its = pick(ATTRS, 3, r)
    qs = ["%s Describe the attribute being studied, how it was measured, and its unit." % t for t, _ in its]
    return dict(qs=qs, key=[k for _, k in its], dir="Listen to each description. Tell the attribute, how it was measured, and the unit.", dur=170)


def quart(s):
    n = len(s)
    lo, hi = s[:n // 2], s[(n + 1) // 2:]

    def med(x):
        m = len(x)
        return F(x[m // 2]) if m % 2 else F(x[m // 2 - 1] + x[m // 2], 2)
    return med(lo), med(hi)


def b_sp_centervar(lp, r):
    # Q1: n=7 mean and median
    while True:
        s1 = sorted(r.randint(3, 15) for _ in range(7))
        if sum(s1) % 7 == 0:
            break
    # Q2: n=8 range and IQR
    s2 = sorted(r.randint(2, 30) for _ in range(8))
    q1, q3 = quart(s2)
    # Q3: n=5 MAD with integer mean
    while True:
        s3 = [r.randint(2, 14) for _ in range(5)]
        if sum(s3) % 5 == 0:
            break
    m3 = sum(s3) // 5
    dev = [abs(x - m3) for x in s3]
    mad = F(sum(dev), 5)
    s3o = list(s3)
    qs = ["Find the mean and the median of this data set: %s." % ", ".join(map(str, r.sample(s1, 7))),
          "Find the range and the interquartile range (IQR) of this data set: %s." % ", ".join(map(str, r.sample(s2, 8))),
          "Find the mean absolute deviation (MAD) of this data set: %s." % ", ".join(map(str, s3o))]
    key = ["Mean = %d. Median = %d. (Sorted: %s. Sum %d ÷ 7 = %d. The middle value is the median.)" % (sum(s1) // 7, s1[3], ", ".join(map(str, s1)), sum(s1), sum(s1) // 7),
           "Range = %d (%d − %d). IQR = %s (Q3 %s − Q1 %s). Sorted: %s." % (s2[-1] - s2[0], s2[-1], s2[0], mixed(q3 - q1), mixed(q3), mixed(q1), ", ".join(map(str, s2))),
           "Mean = %d. Distances from the mean: %s. Add them: %d, then divide by 5: MAD = %s." % (m3, ", ".join(map(str, dev)), sum(dev), mixed(mad))]
    return dict(qs=qs, key=key, dir="Listen to each question. Show your steps on your paper.", dur=230)


def b_sp_choose(lp, r):
    base = sorted(r.randint(4, 9) for _ in range(7))
    out = r.randint(35, 60)
    s1 = base + [out]
    mean1 = F(sum(s1), len(s1))
    med1 = F(s1[3] + s1[4], 2)
    c = r.randint(8, 14)
    s2 = [c - 3, c - 2, c - 1, c, c, c + 1, c + 2, c + 3]
    qs = ["Students recorded how many minutes they read: %s. Find the mean and the median. Which one better shows a typical amount, and why?" % ", ".join(map(str, r.sample(s1, 8))),
          "Here is a data set that is balanced on both sides: %s. Find the mean and the median. Do they differ much? Which would you use?" % ", ".join(map(str, r.sample(s2, 8))),
          "Which measure of variability goes with the median? Which goes with the mean? When would you pick the median and IQR instead of the mean and MAD?"]
    key = ["Mean = %s. Median = %s. The median is better because the value %d is an outlier that pulls the mean up." % (mixed(mean1), mixed(med1), out),
           "Mean = %d and median = %d. They are the same because the data is balanced. Either works." % (c, c),
           "The IQR goes with the median, and the MAD goes with the mean. Use the median and IQR when the data is skewed or has outliers."]
    return dict(qs=qs, key=key, dir="Listen to each question. Say your answer and why.", dur=200)


BUILD = {
    ("6.RP.A.3", "tables"): b_rp_tables, ("6.RP.A.3", "unitrate"): b_rp_unitrate, ("6.RP.A.3", "percent"): b_rp_percent, ("6.RP.A.3", "convert"): b_rp_convert,
    ("6.NS.A.1", "compute"): b_ns_compute, ("6.NS.A.1", "word"): b_ns_word,
    ("6.NS.C.5", "contexts"): b_ns_contexts, ("6.NS.C.5", "zero"): b_ns_zero,
    ("6.NS.C.6", "opposites"): b_ns_opposites, ("6.NS.C.6", "numberline"): b_ns_numberline, ("6.NS.C.6", "plane"): b_ns_plane,
    ("6.EE.A.1", "write"): b_ee_write, ("6.EE.A.1", "evaluate"): b_ee_eval,
    ("6.EE.A.2c", "substitute"): b_ee_sub, ("6.EE.A.2c", "formula"): b_ee_formula,
    ("6.EE.C.9", "equation"): b_ee_equation, ("6.EE.C.9", "tables"): b_ee_tables,
    ("6.G.A.1", "triangles"): b_g_triangles, ("6.G.A.1", "quads"): b_g_quads, ("6.G.A.1", "polygons"): b_g_polygons,
    ("6.G.A.2", "pack"): b_g_pack, ("6.G.A.2", "formula"): b_g_vformula,
    ("6.SP.B.5", "observations"): b_sp_obs, ("6.SP.B.5", "attribute"): b_sp_attr, ("6.SP.B.5", "centervar"): b_sp_centervar, ("6.SP.B.5", "choose"): b_sp_choose,
}


def build():
    out = {}
    for std, cat in CAT.items():
        for lp in range(1, 11):
            parts = []
            for pid, label, desc in cat["parts"]:
                d = BUILD[(std, pid)](lp, rng_for(lp, std + pid))
                assert len(d["qs"]) == 3 and len(d["key"]) == 3, (std, pid, lp, len(d["qs"]), len(d["key"]))
                for t in d["qs"] + d["key"] + [d["dir"]]:
                    assert not BAD.search(t), (std, pid, lp, t)
                part = {"id": pid, "title": label, "desc": desc, "qs": d["qs"], "key": d["key"], "dir": d["dir"], "dur": d["dur"]}
                if d.get("html"):
                    part["html"] = d["html"]
                parts.append(part)
            out.setdefault(std, {})[str(lp)] = parts
    return out


def js(data):
    L = ["/* G6MATH-STRANDS-BEGIN (generated by source/tools/gen_g6math.py, edit the generator, not this block) */",
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append("var G6PIC=%s;" % json.dumps(data, ensure_ascii=False))
    L.append(P1.APPLY.replace("G1PIC", "G6PIC"))
    L.append("/* G6MATH-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G6, encoding="utf8").read()
    if "G6MATH-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G6MATH-STRANDS-BEGIN.*?G6MATH-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        s = src.rstrip()
        assert s.endswith("})();"), s[-40:]
        src = s[:-5] + block + "\n})();\n"
    open(G6, "w", encoding="utf8").write(src)
    print("parts:", sum(len(p) for std in data.values() for p in std.values()), "block bytes:", len(block))


if __name__ == "__main__":
    main()
