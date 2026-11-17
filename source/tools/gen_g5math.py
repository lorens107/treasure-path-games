"""Builds the parts (strands) for the Grade 5 math standards that have more than one gray-book "I can" line, all 10 LPs,
and writes them into source/gx/g5.js.

5.NBT.A.3 and 5.NF.B.4 have one "I can" line each, so they stay whole standards.
Run:  python3 source/tools/gen_g5math.py
"""
import json, os, re, sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N
import gen_g1pic as P1
import gen_g3math as G3

G5 = os.path.join(HERE, '..', 'gx', 'g5.js')
THEME, rng_for, nm, BAD = N.THEME, N.rng_for, N.nm, N.BAD
svg, row = P1.svg, P1.row
INK = P1.INK
colour = G3.colour


def C(*p):
    return list(p)


CAT = {
    "5.OA.A.1": {"desc": "parentheses, brackets, and braces in numerical expressions", "parts": C(
        ("write", "Write expressions with parentheses, brackets, or braces", "Using parentheses, brackets, or braces in numerical expressions"),
        ("evaluate", "Evaluate expressions with parentheses, brackets, or braces", "Evaluating expressions with parentheses, brackets, or braces"))},
    "5.NBT.A.1": {"desc": "place value patterns of 10 times and 1/10", "parts": C(
        ("ten", "A digit is 10 times the place to its right", "Recognizing that a digit in one place represents 10 times as much as it represents in the place to its right"),
        ("tenth", "A digit is 1/10 of the place to its left", "Recognizing that a digit in one place represents 1/10 of what it represents in the place to its left"))},
    "5.NF.A.1": {"desc": "adding and subtracting fractions and mixed numbers with unlike denominators", "parts": C(
        ("add", "Add fractions with unlike denominators", "Adding fractions with unlike denominators by replacing them with equivalent fractions that have like denominators"),
        ("sub", "Subtract fractions with unlike denominators", "Subtracting fractions with unlike denominators by replacing them with equivalent fractions that have like denominators"),
        ("addmix", "Add mixed numbers with unlike denominators", "Adding mixed numbers with unlike denominators by replacing them with equivalent fractions that have like denominators"),
        ("submix", "Subtract mixed numbers with unlike denominators", "Subtracting mixed numbers with unlike denominators by replacing them with equivalent fractions that have like denominators"))},
    "5.NF.A.2": {"desc": "fraction addition and subtraction word problems and checking if answers are reasonable", "parts": C(
        ("addsame", "Add fractions in word problems", "Solving word problems involving addition of fractions referring to the same whole"),
        ("subsame", "Subtract fractions in word problems", "Solving word problems involving subtraction of fractions referring to the same whole"),
        ("addunlike", "Add fractions with unlike denominators in word problems", "Solving word problems involving addition of fractions with unlike denominators referring to the same whole"),
        ("subunlike", "Subtract fractions with unlike denominators in word problems", "Solving word problems involving subtraction of fractions with unlike denominators referring to the same whole"),
        ("benchmark", "Check answers with benchmark fractions", "Using benchmark fractions to estimate mentally and assess the reasonableness of answers"),
        ("numsense", "Check answers with number sense of fractions", "Using number sense of fractions to estimate mentally and assess the reasonableness of answers"))},
    "5.NF.B.3": {"desc": "fractions as division and word problems that give fraction or mixed number answers", "parts": C(
        ("interpret", "A fraction is a division (a/b = a ÷ b)", "Interpreting a fraction as division of the numerator by the denominator (a/b = a ÷ b)"),
        ("word", "Division word problems with fraction answers", "Solving word problems involving division of whole numbers that lead to answers in the form of fractions or mixed numbers"))},
    "5.MD.C.3": {"desc": "volume as an attribute of solid figures and volume measurement", "parts": C(
        ("attribute", "Volume is an attribute of solid figures", "Recognizing volume as an attribute of solid figures"),
        ("measure", "Volume measurement concepts", "Demonstrating knowledge of the concepts of volume measurement by counting unit cubes"))},
    "5.MD.C.5": {"desc": "volume with multiplication and addition, and volume problems", "parts": C(
        ("relate", "Relate volume to multiplication and addition", "Relating volume to the operations of multiplication and addition"),
        ("solve", "Solve volume problems", "Solving real-world and mathematical problems involving volume"))},
    "5.G.A.1": {"desc": "the coordinate plane, axes, origin, and ordered pairs", "parts": C(
        ("label", "Identify and label the axes and origin", "Identifying and labeling the x-axis, y-axis, and origin on a coordinate grid"),
        ("system", "Use perpendicular number lines to make a coordinate system", "Using a pair of perpendicular number lines, with the origin at 0 on each line, to define a coordinate system"),
        ("locate", "Locate a point with an ordered pair", "Locating a given point in the plane by using an ordered pair of numbers"),
        ("xnum", "The first number is the distance along the x-axis", "Showing that the first number of an ordered pair tells how far to travel from the origin along the x-axis"),
        ("ynum", "The second number is the distance along the y-axis", "Showing that the second number of an ordered pair tells how far to travel from the origin along the y-axis"),
        ("names", "Axis names match coordinate names", "Showing that the names of the two axes and the coordinates correspond (x-axis and x-coordinate, y-axis and y-coordinate)"))},
}

TELL = "Look at the figures. Your teacher asks about one at a time. Say your answer out loud."


def cm(n):
    return "{:,}".format(n)


def mixed(f):
    w, r = divmod(f.numerator, f.denominator)
    if r == 0:
        return "%d" % w
    return ("%d %d/%d" % (w, r, f.denominator)) if w else "%d/%d" % (r, f.denominator)


def lcm(a, b):
    return a * b // gcd(a, b)


DENS = [2, 3, 4, 5, 6, 8, 10, 12]


def frac_pair(r, need_unlike=True, sub=False):
    while True:
        d1, d2 = r.sample(DENS, 2)
        n1, n2 = r.randint(1, d1 - 1), r.randint(1, d2 - 1)
        if d1 == d2 or gcd(n1, d1) != 1 and False:
            continue
        a, b = F(n1, d1), F(n2, d2)
        if a == b or a.denominator == b.denominator:
            continue
        if sub and a < b:
            a, b = b, a
        if not sub and a + b >= 2:
            continue
        if sub and a - b == 0:
            continue
        return a, b


def fstr(f):
    return "%d/%d" % (f.numerator, f.denominator)


def fkey(a, b, op):
    L = lcm(a.denominator, b.denominator)
    A, B = a.numerator * (L // a.denominator), b.numerator * (L // b.denominator)
    res = a + b if op == "+" else a - b
    top = A + B if op == "+" else A - B
    sy = "+" if op == "+" else "\u2212"
    s = "%s %s %s = %d/%d %s %d/%d = %d/%d" % (fstr(a), sy, fstr(b), A, L, sy, B, L, top, L)
    if res.denominator != L or res.numerator >= res.denominator:
        s += " = %s" % mixed(res)
    return s + "."


# ------------------------------------------------------------------ OA.A.1
def b_write(lp, r):
    a, b, c = r.randint(3, 9), r.randint(2, 8), r.randint(2, 5)
    q = r.randint(2, 6); s = r.randint(2, 9); t = r.randint(2, 6); d = r.randint(2, 9)
    x = r.randint(10, 20); y = r.randint(2, 7); z = r.randint(2, 4)
    qs = ["Write an expression for: add %d and %d, then multiply by %d. Use parentheses. Do not solve it." % (a, b, c),
          "Write an expression for: subtract %d from %d, then divide by %d. Use parentheses. Do not solve it." % (y, x * z if False else (y + z * q), z),
          "Write an expression for: multiply %d by the sum of %d and %d, then subtract %d. Use brackets and parentheses. Do not solve it." % (t, s, q, d)]
    key = ["%d × (%d + %d)." % (c, a, b), "(%d − %d) ÷ %d." % (y + z * q, y, z), "[%d × (%d + %d)] − %d." % (t, s, q, d)]
    return dict(qs=qs, key=key, dir="Listen to each question. Write the expression on your paper. Do not solve it.", dur=140)


def b_evaluate(lp, r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 5)
    s, q, t, d = r.randint(2, 6), r.randint(2, 6), r.randint(2, 5), r.randint(2, 9)
    m, k, p = r.randint(2, 5), r.randint(2, 6), r.randint(2, 4)
    e1 = c * (a + b)
    e2 = t * (s + q) - d
    inner = (m + k)
    e3 = (inner * p + 1 * 0)
    ex3 = "{ [ %d + %d ] × %d } − %d" % (m, k, p, p) if False else None
    v3 = (m + k) * p - p
    qs = ["Evaluate: %d × (%d + %d)" % (c, a, b),
          "Evaluate: [%d × (%d + %d)] − %d" % (t, s, q, d),
          "Evaluate: {[%d + %d] × %d} − %d" % (m, k, p, p)]
    key = ["%d. First %d + %d = %d, then %d × %d = %d." % (e1, a, b, a + b, c, a + b, e1),
           "%d. First (%d + %d) = %d, then %d × %d = %d, then %d − %d = %d." % (e2, s, q, s + q, t, s + q, t * (s + q), t * (s + q), d, e2),
           "%d. First [%d + %d] = %d, then %d × %d = %d, then %d − %d = %d." % (v3, m, k, m + k, m + k, p, (m + k) * p, (m + k) * p, p, v3)]
    return dict(qs=qs, key=key, dir="Listen to each question. Work from the inside out. Write each step on your paper.", dur=160)


# ------------------------------------------------------------------ NBT.A.1
def b_ten(lp, r):
    d1, d2, d3 = r.sample(range(2, 9), 3)
    qs = ["In the number %s, how many times as much is the %d in the thousands place as the %d in the hundreds place? Tell how you know." % (cm(d1 * 1000 + d1 * 100 + r.choice([0, 20, 30, 40])), d1, d1),
          "In the number %s, how many times as much is the %d in the tens place as the %d in the ones place?" % (cm(d2 * 100 + d2 * 10 + d2), d2, d2),
          "In the number %d.%d%d, how many times as much is the %d in the ones place as the %d in the tenths place?" % (d3, d3, r.choice([1, 5, 6]), d3, d3)]
    key = ["10 times as much. %s is 10 × %s." % (cm(d1 * 1000), cm(d1 * 100)),
           "10 times as much. %d is 10 × %d." % (d2 * 10, d2),
           "10 times as much. %d is 10 × %.1f." % (d3, d3 / 10.0)]
    return dict(qs=qs, key=key, dir="Listen to each question. Say your answer and tell how you know.", dur=140)


def b_tenth(lp, r):
    d1, d2, d3 = r.sample(range(2, 9), 3)
    qs = ["In the number %s, the %d in the tens place is what fraction of the %d in the hundreds place?" % (cm(d1 * 100 + d1 * 10 + r.choice([0, 5, 9])), d1, d1),
          "In the number %s, the %d in the hundreds place is what fraction of the %d in the thousands place?" % (cm(d2 * 1000 + d2 * 100 + r.choice([0, 40, 70])), d2, d2),
          "In the number %d.%d%d, the %d in the hundredths place is what fraction of the %d in the tenths place?" % (r.choice([1, 4, 6]), d3, d3, d3, d3)]
    key = ["1/10. %d is 1/10 of %d." % (d1 * 10, d1 * 100),
           "1/10. %s is 1/10 of %s." % (cm(d2 * 100), cm(d2 * 1000)),
           "1/10. %.2f is 1/10 of %.1f." % (d3 / 100.0, d3 / 10.0)]
    return dict(qs=qs, key=key, dir="Listen to each question. Say your answer and tell how you know.", dur=140)


# ------------------------------------------------------------------ NF.A.1
def b_add(lp, r):
    ps = [frac_pair(r) for _ in range(3)]
    qs = ["Add %s + %s. Use equivalent fractions with like denominators." % (fstr(a), fstr(b)) for a, b in ps]
    return dict(qs=qs, key=[fkey(a, b, "+") for a, b in ps], dir="Listen to each question. Write each step on your paper.", dur=170)


def b_sub(lp, r):
    ps = [frac_pair(r, sub=True) for _ in range(3)]
    qs = ["Subtract %s − %s. Use equivalent fractions with like denominators." % (fstr(a), fstr(b)) for a, b in ps]
    return dict(qs=qs, key=[fkey(a, b, "-") for a, b in ps], dir="Listen to each question. Write each step on your paper.", dur=170)


def mixed_pair(r, sub):
    while True:
        a, b = frac_pair(r, sub=False)
        w1, w2 = r.randint(1, 5), r.randint(1, 4)
        x, y = w1 + a, w2 + b
        if sub:
            if x < y:
                x, y = y, x
            if x - y <= 0:
                continue
        return x, y


def mkey(x, y, op):
    L = lcm(x.denominator, y.denominator)
    xs, ys = x.numerator * (L // x.denominator), y.numerator * (L // y.denominator)
    wx, rx = divmod(xs, L); wy, ry = divmod(ys, L)
    res = x + y if op == "+" else x - y
    sy = "+" if op == "+" else "\u2212"
    return "%s %s %s = %d %d/%d %s %d %d/%d = %s." % (mixed(x), sy, mixed(y), wx, rx, L, sy, wy, ry, L, mixed(res))


def b_addmix(lp, r):
    ps = [mixed_pair(r, False) for _ in range(3)]
    qs = ["Add %s + %s. Replace the fractions with equivalent fractions that have like denominators." % (mixed(x), mixed(y)) for x, y in ps]
    return dict(qs=qs, key=[mkey(x, y, "+") for x, y in ps], dir="Listen to each question. Write each step on your paper.", dur=190)


def b_submix(lp, r):
    ps = [mixed_pair(r, True) for _ in range(3)]
    qs = ["Subtract %s − %s. Replace the fractions with equivalent fractions that have like denominators." % (mixed(x), mixed(y)) for x, y in ps]
    return dict(qs=qs, key=[mkey(x, y, "-") for x, y in ps], dir="Listen to each question. Write each step on your paper.", dur=190)


# ------------------------------------------------------------------ NF.A.2
ITEMS = ["cups of flour", "pounds of apples", "yards of ribbon", "gallons of paint", "miles of trail", "pounds of sand"]


def wp(lp, r, op, like):
    out, key = [], []
    items = r.sample(ITEMS, 3)
    names = [nm(lp, i) for i in range(3)]
    for n, it in zip(names, items):
        if like:
            d = r.choice([5, 6, 8, 10, 12])
            if op == "+":
                n1 = r.randint(1, d - 2); n2 = r.randint(1, d - n1 - 1) if d - n1 > 1 else 1
                a, b = F(n1, d), F(n2, d)
            else:
                n1 = r.randint(3, d - 1); n2 = r.randint(1, n1 - 1)
                a, b = F(n1, d), F(n2, d)
            a = F(a.numerator, a.denominator)
            sa, sb = "%d/%d" % (n1, d), "%d/%d" % (n2, d)
        else:
            a, b = frac_pair(r, sub=(op == "-"))
            sa, sb = fstr(a), fstr(b)
        if op == "+":
            res = a + b
            q = "%s used %s of %s on Monday and %s on Tuesday. How many %s in all? Write an equation." % (n, sa, it, sb, it.split(" of ")[1] if False else "was used")
            q = "%s has %s %s and then gets %s more. How much does %s have now? Write an equation." % (n, sa, it, sb, n)
            ans = "%s + %s = %s" % (sa, sb, mixed(res))
        else:
            res = a - b
            q = "%s has %s %s and uses %s. How much is left? Write an equation." % (n, sa, it, sb)
            ans = "%s − %s = %s" % (sa, sb, mixed(res))
        if not like:
            L = lcm(a.denominator, b.denominator)
            ans = "%s (common denominator %d)." % (ans, L)
        else:
            ans += "."
        out.append(q); key.append(ans)
    return out, key


def b_addsame(lp, r):
    q, k = wp(lp, r, "+", True)
    return dict(qs=q, key=k, dir="Listen to each problem. Draw a model or write an equation, then solve.", dur=170)


def b_subsame(lp, r):
    q, k = wp(lp, r, "-", True)
    return dict(qs=q, key=k, dir="Listen to each problem. Draw a model or write an equation, then solve.", dur=170)


def b_addunlike(lp, r):
    q, k = wp(lp, r, "+", False)
    return dict(qs=q, key=k, dir="Listen to each problem. Draw a model or write an equation, then solve.", dur=190)


def b_subunlike(lp, r):
    q, k = wp(lp, r, "-", False)
    return dict(qs=q, key=k, dir="Listen to each problem. Draw a model or write an equation, then solve.", dur=190)


BM = [F(1, 8), F(1, 10), F(2, 9), F(3, 8), F(4, 9), F(5, 12), F(3, 5), F(5, 8), F(7, 12), F(7, 8), F(9, 10), F(11, 12), F(5, 6), F(1, 2)]


def bench(f):
    return F(0) if f < F(1, 4) else F(1, 2) if f < F(3, 4) else F(1)


def b_benchmark(lp, r):
    a, b = r.sample([x for x in BM if x != F(1, 2)], 2)
    ea, eb = bench(a), bench(b)
    wrong_pairs = [((2, 5), (1, 2), (3, 7)), ((3, 4), (2, 3), (5, 7)), ((1, 2), (3, 8), (4, 10)), ((5, 6), (1, 2), (6, 8)), ((2, 3), (3, 4), (5, 7)), ((3, 5), (1, 2), (4, 7))]
    (n1, d1), (n2, d2), (nn, dd) = r.choice(wrong_pairs)
    sub_pairs = [((5, 6), (1, 2), (4, 4)), ((5, 8), (1, 4), (4, 4)), ((7, 8), (1, 2), (6, 6))]
    (m1, e1), (m2, e2), (mm, ee) = r.choice(sub_pairs)
    qs = ["Use the benchmarks 0, 1/2, and 1 to estimate %s + %s. Tell your estimate." % (fstr(a), fstr(b)),
          "A student says %d/%d + %d/%d = %d/%d. Use a benchmark fraction to tell whether that answer is reasonable." % (n1, d1, n2, d2, nn, dd),
          "A student says %d/%d − %d/%d = %d/%d. Use a benchmark fraction to tell whether that answer is reasonable." % (m1, e1, m2, e2, mm, ee)]
    est = ea + eb
    key = ["About %s. %s is close to %s and %s is close to %s." % (mixed(est) if est != 0 else "0", fstr(a), mixed(ea) if ea else "0", fstr(b), mixed(eb) if eb else "0"),
           "Not reasonable. %d/%d is less than %s, one of the fractions being added, and a sum can't be smaller than one of its addends. The correct sum is %s." % (nn, dd, fstr(max(F(n1, d1), F(n2, d2))), mixed(F(n1, d1) + F(n2, d2))),
           "Not reasonable. %d/%d is more than %d/%d, but subtracting makes a number smaller. The correct difference is %s." % (mm, ee, m1, e1, mixed(F(m1, e1) - F(m2, e2)))]
    return dict(qs=qs, key=key, dir="Listen to each question. Think about 0, 1/2, and 1. Say your answer out loud.", dur=170)


def rnd(f):
    w, rem = divmod(f.numerator, f.denominator)
    return w + (1 if F(rem, f.denominator) > F(1, 2) else 0)


MIXF = [F(1, 6), F(1, 8), F(1, 10), F(1, 4), F(1, 3), F(2, 5), F(5, 8), F(2, 3), F(3, 4), F(7, 8), F(5, 6), F(9, 10)]


def b_numsense(lp, r):
    def mx():
        return r.randint(1, 5) + r.choice(MIXF)
    a, b = mx(), mx()
    c, d = mx(), mx()
    while a + b > 9 or c < d + 1:
        c, d = mx(), mx()
        a, b = mx(), mx()
    e, f = mx(), mx()
    while e < f + 1:
        e, f = mx(), mx()
    qs = ["Round each mixed number to the nearest whole number to estimate %s + %s. Tell your estimate." % (mixed(a), mixed(b)),
          "A student says %s + %s = %s. Use number sense of fractions to tell whether that answer is reasonable." % (mixed(c), mixed(d), mixed(c + d + 3)),
          "A student says %s − %s = %s. Use number sense of fractions to tell whether that answer is reasonable." % (mixed(e), mixed(f), mixed(e - f))]
    key = ["About %d. %s is close to %d and %s is close to %d." % (rnd(a) + rnd(b), mixed(a), rnd(a), mixed(b), rnd(b)),
           "Not reasonable. %s is close to %d and %s is close to %d, so the sum is about %d, not %s. The correct sum is %s." % (mixed(c), rnd(c), mixed(d), rnd(d), rnd(c) + rnd(d), mixed(c + d + 3), mixed(c + d)),
           "Reasonable. %s is close to %d and %s is close to %d, so the difference is about %d, and %s is close to that." % (mixed(e), rnd(e), mixed(f), rnd(f), rnd(e) - rnd(f), mixed(e - f))]
    return dict(qs=qs, key=key, dir="Listen to each question. Round to the nearest whole number to estimate. Say your answer out loud.", dur=180)


# ------------------------------------------------------------------ NF.B.3
def b_interpret(lp, r):
    a, b = r.choice([(3, 4), (2, 5), (5, 8), (3, 8), (4, 9), (2, 7)])
    c, d = r.choice([(7, 8), (5, 6), (3, 10), (9, 4)])
    e, f = r.choice([(3, 4), (2, 3), (5, 6), (4, 5)])
    qs = ["Write the fraction %d/%d as a division problem." % (a, b),
          "Write %d ÷ %d as a fraction." % (c, d),
          "%d wholes are shared equally among %d people. What fraction of a whole does each person get? Tell how you know." % (e, f)]
    key = ["%d ÷ %d." % (a, b), "%d/%d." % (c, d), "%d/%d of a whole, because %d ÷ %d = %d/%d. Check: %d/%d × %d = %d." % (e, f, e, f, e, f, e, f, f, e)]
    return dict(qs=qs, key=key, dir="Listen to each question. Say or write your answer.", dur=140)


def b_wordnf(lp, r):
    pool = [(50, 9, "pounds of rice", "people", "pounds"), (25, 4, "feet of rope", "pieces", "feet"), (30, 7, "cups of juice", "friends", "cups"), (19, 5, "pizzas", "kids", "pizzas"),
            (11, 3, "pounds of trail mix", "bags", "pounds"), (23, 6, "yards of ribbon", "crafts", "yards"), (41, 8, "liters of water", "bottles", "liters"), (14, 4, "sandwiches", "kids", "sandwiches")]
    ps = r.sample(pool, 3)
    qs, key = [], []
    for a, b, what, who, un in ps:
        qs.append("%d %s are shared equally among %d %s. How much does each one get? Write an equation and say which two whole numbers your answer is between." % (a, what, b, who))
        w = a // b
        key.append("%d ÷ %d = %d/%d = %s %s each. It is between %d and %d." % (a, b, a, b, mixed(F(a, b)), un, w, w + 1))
    return dict(qs=qs, key=key, dir="Listen to each problem. Draw a model or write an equation, then solve.", dur=190)


# ------------------------------------------------------------------ MD.C.3
def b_pool(pool, dur=100):
    def f(lp, r):
        it = pool[:]
        r.shuffle(it)
        it = it[:3]
        return dict(qs=[q for q, k in it], key=[k for q, k in it], dir="Listen to each question. Say your answer out loud.", dur=dur)
    return f


ATTR = [("A box can hold sand. What do we call the amount of space inside the box?", "Volume."),
        ("Which tells how much space a solid figure takes up: perimeter, area, or volume?", "Volume."),
        ("Which unit measures volume: centimeters, square centimeters, or cubic centimeters?", "Cubic centimeters."),
        ("Is volume an attribute of a flat shape like a triangle drawn on paper, or of a solid figure like a box? Explain.", "A solid figure. A flat shape has no depth, so it holds no space."),
        ("A cube has edges that are 1 unit long. What do we call its volume?", "1 cubic unit."),
        ("Can we measure volume by counting squares or by counting cubes? Why?", "Count cubes. A cube takes up space in three directions, a square covers a flat surface.")]


def iso(l, w, h, s=24, col="#e8b4f0", lines=True):
    d = int(s * 0.55)
    X0, Y0 = 8, 8 + w * d
    W = int(X0 + l * s + w * d + 10)
    H = int(Y0 + h * s + 10)
    top = [(X0, Y0), (X0 + l * s, Y0), (X0 + l * s + w * d, Y0 - w * d), (X0 + w * d, Y0 - w * d)]
    right = [(X0 + l * s, Y0), (X0 + l * s + w * d, Y0 - w * d), (X0 + l * s + w * d, Y0 - w * d + h * s), (X0 + l * s, Y0 + h * s)]
    front = [(X0, Y0), (X0 + l * s, Y0), (X0 + l * s, Y0 + h * s), (X0, Y0 + h * s)]
    p = lambda pts, f: '<polygon points="%s" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (" ".join("%d,%d" % q for q in pts), f, INK)
    body = p(front, col) + p(top, "#ffffff") + p(right, "#d9d0c4")
    g = ""
    for i in range(1, l):
        g += '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (X0 + i * s, Y0, X0 + i * s, Y0 + h * s)
        g += '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (X0 + i * s, Y0, X0 + i * s + w * d, Y0 - w * d)
    for j in range(1, h):
        g += '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (X0, Y0 + j * s, X0 + l * s, Y0 + j * s)
        g += '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (X0 + l * s, Y0 + j * s, X0 + l * s + w * d, Y0 + j * s - w * d)
    for k in range(1, w):
        g += '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (X0 + k * d, Y0 - k * d, X0 + l * s + k * d, Y0 - k * d)
        g += '<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (X0 + l * s + k * d, Y0 - k * d, X0 + l * s + k * d, Y0 - k * d + h * s)
    body += '<g stroke="%s" stroke-width="1.2" opacity="0.6">%s</g>' % (INK, g)
    return svg(W, H, body, "A box built from unit cubes, %d long, %d wide, %d tall" % (l, w, h))


def b_measure(lp, r):
    dims = []
    while len(dims) < 3:
        l, w, h = r.randint(2, 5), r.randint(2, 4), r.randint(2, 4)
        if (l, w, h) not in dims:
            dims.append((l, w, h))
    col = colour(lp)
    figs = [(L, iso(l, w, h, col=col)) for L, (l, w, h) in zip("ABC", dims)]
    qs, key = [], []
    for L, (l, w, h) in zip("ABC", dims):
        qs.append("Box %s is packed with unit cubes, 1 cubic unit each. How many cubes are in the bottom layer? How many layers are there? What is the volume?" % L)
        key.append("Bottom layer: %d × %d = %d cubes. %d layers. Volume: %d × %d = %d cubic units." % (l, w, l * w, h, l * w, h, l * w * h))
    return dict(qs=qs, key=key, dir="Look at the three boxes. Your teacher asks about one box at a time. Count the layers and cubes.", dur=200, html=row(figs))


# ------------------------------------------------------------------ MD.C.5
def b_relate(lp, r):
    l, w, h = r.randint(3, 7), r.randint(2, 5), r.randint(2, 5)
    B, hh = r.choice([12, 15, 20, 24, 18]), r.randint(3, 8)
    a1, a2, wd, ht = r.randint(4, 8), r.randint(2, 5), r.randint(2, 4), r.randint(2, 5)
    qs = ["A box is %d units long, %d units wide, and %d units tall. Write two multiplication equations that show its volume, one with l × w × h and one that starts with the area of the base." % (l, w, h),
          "The base of a box has an area of %d square units. The box is %d units tall. Use V = B × h to find its volume." % (B, hh),
          "Two boxes are stuck together. Box 1 is %d long, %d wide, %d tall. Box 2 is %d long, %d wide, %d tall. What is the volume of the whole solid? Add the two volumes." % (a1, wd, ht, a2, wd, ht)]
    key = ["V = %d × %d × %d = %d cubic units. Also V = (%d × %d) × %d = %d × %d = %d cubic units." % (l, w, h, l * w * h, l, w, h, l * w, h, l * w * h),
           "V = %d × %d = %d cubic units." % (B, hh, B * hh),
           "Box 1: %d × %d × %d = %d. Box 2: %d × %d × %d = %d. Total: %d + %d = %d cubic units." % (a1, wd, ht, a1 * wd * ht, a2, wd, ht, a2 * wd * ht, a1 * wd * ht, a2 * wd * ht, (a1 + a2) * wd * ht)]
    return dict(qs=qs, key=key, dir="Listen to each question. Write the equations on your paper. Say what each number stands for.", dur=190)


def b_solve(lp, r):
    n0, n1 = nm(lp, 0), nm(lp, 1)
    l, w, h = r.randint(20, 40), r.randint(10, 20), r.randint(10, 20)
    l2, w2, h2 = r.randint(6, 12), r.randint(3, 6), r.randint(2, 5)
    h3 = r.randint(3, 8); l3, w3 = r.randint(4, 9), r.randint(3, 6)
    qs = ["%s has a fish tank shaped like a box. It is %d cm long, %d cm wide, and %d cm tall. How many cubic centimeters of water fill the tank to the top?" % (n0, l, w, h),
          "%s builds a sandbox that is %d feet long, %d feet wide, and %d feet deep. How many cubic feet of sand will fill it?" % (n1, l2, w2, h2),
          "A box has a volume of %d cubic inches. Its length is %d inches and its width is %d inches. What is its height? Write an equation with an unknown." % (l3 * w3 * h3, l3, w3)]
    key = ["%s cubic centimeters (%d × %d × %d = %s)." % (cm(l * w * h), l, w, h, cm(l * w * h)),
           "%d cubic feet (%d × %d × %d = %d)." % (l2 * w2 * h2, l2, w2, h2, l2 * w2 * h2),
           "%d inches. %d × %d × ? = %d, so %d × ? = %d and ? = %d." % (h3, l3, w3, l3 * w3 * h3, l3 * w3, l3 * w3 * h3, h3)]
    return dict(qs=qs, key=key, dir="Listen to each problem. Solve it on your paper. Write the equation you used.", dur=190)


# ------------------------------------------------------------------ G.A.1
def grid(n=8, pts=None, nums=True, marks=None, c=26):
    pts = pts or {}
    M = 30
    W = M + n * c + 24
    H = M + n * c + 18
    ox, oy = M, 10 + n * c
    body = ""
    for i in range(n + 1):
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#c9c1b3" stroke-width="1"/>' % (ox + i * c, oy, ox + i * c, oy - n * c)
        body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#c9c1b3" stroke-width="1"/>' % (ox, oy - i * c, ox + n * c, oy - i * c)
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (ox, oy, ox + n * c + 12, oy, INK)
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (ox, oy, ox, oy - n * c - 10, INK)
    body += '<polygon points="%d,%d %d,%d %d,%d" fill="%s"/>' % (ox + n * c + 14, oy, ox + n * c + 5, oy - 5, ox + n * c + 5, oy + 5, INK)
    body += '<polygon points="%d,%d %d,%d %d,%d" fill="%s"/>' % (ox, oy - n * c - 12, ox - 5, oy - n * c - 3, ox + 5, oy - n * c - 3, INK)
    if nums:
        for i in range(n + 1):
            body += '<text x="%d" y="%d" font-size="12" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%d</text>' % (ox + i * c, oy + 15, INK, i)
            if i:
                body += '<text x="%d" y="%d" font-size="12" font-weight="700" text-anchor="end" fill="%s" font-family="sans-serif">%d</text>' % (ox - 6, oy - i * c + 4, INK, i)
    for L, (x, y) in pts.items():
        body += '<circle cx="%d" cy="%d" r="6" fill="#c0392b" stroke="%s" stroke-width="2"/>' % (ox + x * c, oy - y * c, INK)
        body += '<text x="%d" y="%d" font-size="15" font-weight="800" fill="%s" font-family="sans-serif">%s</text>' % (ox + x * c + 8, oy - y * c - 8, INK, L)
    for L, (px, py) in (marks or {}).items():
        body += '<text x="%d" y="%d" font-size="17" font-weight="800" text-anchor="middle" fill="#c0392b" font-family="sans-serif">%s</text>' % (px, py, L)
    return svg(W, H, body, "A coordinate grid")


def b_label(lp, r):
    n, c = 8, 26
    ox, oy = 30, 10 + n * c
    letters = list("ABC")
    r.shuffle(letters)
    parts = {"x-axis": letters[0], "y-axis": letters[1], "origin": letters[2]}
    marks = {parts["x-axis"]: (ox + 5 * c, oy + 34), parts["y-axis"]: (ox - 22, oy - 6 * c), parts["origin"]: (ox - 14, oy + 18)}
    fig = grid(n, nums=False, marks=marks, c=c)
    order = sorted(parts.items(), key=lambda kv: kv[1])
    qs, key = [], []
    for nme, L in order:
        qs.append("What is the name of the line or point marked %s on the grid?" % L)
        key.append({"x-axis": "The x-axis, the horizontal number line.", "y-axis": "The y-axis, the vertical number line.", "origin": "The origin, where the two axes meet. It is 0 on both number lines."}[nme])
    return dict(qs=qs, key=key, dir="Look at the grid. Your teacher asks about each red letter. Say its name.", dur=150, html=row([("", fig)]))


def b_system(lp, r):
    n = r.randint(5, 9)
    qs = ["How do the two number lines of a coordinate grid meet? What are the two lines called?",
          "Where do the two number lines cross? What number is at that point on each line?",
          "Draw a coordinate grid on your paper that goes from 0 to %d on each axis. Show where the origin goes." % n]
    key = ["They cross at a right angle (they are perpendicular). They are called the axes: the x-axis is horizontal and the y-axis is vertical.",
           "They cross at the origin. The 0 of each number line is at the origin, so the origin is the ordered pair (0, 0).",
           "One horizontal line (x-axis) and one vertical line (y-axis), both numbered 0 to %d. They cross at the 0 on each line, and that point is the origin." % n]
    return dict(qs=qs, key=key, dir="Listen to each question. Say or draw your answer.", dur=160)


def b_locate(lp, r):
    pts = {}
    while len(pts) < 2:
        x, y = r.randint(1, 8), r.randint(1, 8)
        if (x, y) not in pts.values() and x != y:
            pts["AB"[len(pts)]] = (x, y)
    fig = grid(8, pts)
    px, py = r.randint(1, 7), r.randint(1, 7)
    while px == py:
        py = r.randint(1, 7)
    qs = ["Write the ordered pair for point %s." % "A", "Write the ordered pair for point %s." % "B",
          "Draw a coordinate grid on your paper. Plot and label the point (%d, %d)." % (px, py)]
    key = ["(%d, %d)." % pts["A"], "(%d, %d)." % pts["B"], "Start at the origin, go %d right along the x-axis, then %d up. Mark the point (%d, %d)." % (px, py, px, py)]
    return dict(qs=qs, key=key, dir="Look at the grid. Your teacher asks about the points. Say or write the answers.", dur=170, html=row([("", fig)]))


def b_xnum(lp, r):
    a, b = r.sample(range(2, 9), 2)
    c, d = r.sample(range(2, 9), 2)
    e = r.randint(2, 7)
    qs = ["To plot the point (%d, %d), which axis do you travel along first? How far do you go, and which direction?" % (a, b),
          "In the ordered pair (%d, %d), what does the %d tell you?" % (c, d, c),
          "Point P is at (%d, %d). Point Q is at (%d, %d). Which point is farther from the origin along the x-axis, and how many units farther?" % (e, 1, e + 3, 1)]
    key = ["The x-axis first. Go %d units to the right from the origin. Then go %d up." % (a, b),
           "It tells how far to travel from the origin along the x-axis (%d units to the right)." % c,
           "Point Q. Its first number is 3 more than P's, so it is 3 units farther along the x-axis."]
    return dict(qs=qs, key=key, dir="Listen to each question. Say your answer out loud.", dur=140)


def b_ynum(lp, r):
    a, b = r.sample(range(2, 9), 2)
    c, d = r.sample(range(2, 9), 2)
    e = r.randint(2, 7)
    qs = ["To plot the point (%d, %d), after you go along the x-axis, how far do you travel next, and in which direction?" % (a, b),
          "In the ordered pair (%d, %d), what does the %d tell you?" % (c, d, d),
          "Point P is at (1, %d). Point Q is at (1, %d). Which point is higher on the grid, and how many units higher?" % (e, e + 3)]
    key = ["Go %d units up, parallel to the y-axis." % b,
           "It tells how far to travel from the origin along the y-axis (%d units up)." % d,
           "Point Q. Its second number is 3 more than P's, so it is 3 units higher along the y-axis."]
    return dict(qs=qs, key=key, dir="Listen to each question. Say your answer out loud.", dur=140)


def b_names(lp, r):
    a, b = r.sample(range(2, 9), 2)
    c, d = r.sample(range(2, 9), 2)
    e, f = r.sample(range(2, 9), 2)
    qs = ["In the ordered pair (%d, %d), which number is the x-coordinate and which is the y-coordinate?" % (a, b),
          "The x-coordinate of a point tells the distance along which axis? What about the y-coordinate? Use the point (%d, %d)." % (c, d),
          "A point has the y-coordinate %d and the x-coordinate %d. Write its ordered pair." % (e, f)]
    key = ["The x-coordinate is %d and the y-coordinate is %d." % (a, b),
           "The x-coordinate (%d) goes with the x-axis. The y-coordinate (%d) goes with the y-axis." % (c, d),
           "(%d, %d). The x-coordinate always comes first." % (f, e)]
    return dict(qs=qs, key=key, dir="Listen to each question. Say your answer out loud.", dur=140)


BUILD = {
    ("5.OA.A.1", "write"): b_write, ("5.OA.A.1", "evaluate"): b_evaluate,
    ("5.NBT.A.1", "ten"): b_ten, ("5.NBT.A.1", "tenth"): b_tenth,
    ("5.NF.A.1", "add"): b_add, ("5.NF.A.1", "sub"): b_sub, ("5.NF.A.1", "addmix"): b_addmix, ("5.NF.A.1", "submix"): b_submix,
    ("5.NF.A.2", "addsame"): b_addsame, ("5.NF.A.2", "subsame"): b_subsame, ("5.NF.A.2", "addunlike"): b_addunlike, ("5.NF.A.2", "subunlike"): b_subunlike,
    ("5.NF.A.2", "benchmark"): b_benchmark, ("5.NF.A.2", "numsense"): b_numsense,
    ("5.NF.B.3", "interpret"): b_interpret, ("5.NF.B.3", "word"): b_wordnf,
    ("5.MD.C.3", "attribute"): b_pool(ATTR), ("5.MD.C.3", "measure"): b_measure,
    ("5.MD.C.5", "relate"): b_relate, ("5.MD.C.5", "solve"): b_solve,
    ("5.G.A.1", "label"): b_label, ("5.G.A.1", "system"): b_system, ("5.G.A.1", "locate"): b_locate,
    ("5.G.A.1", "xnum"): b_xnum, ("5.G.A.1", "ynum"): b_ynum, ("5.G.A.1", "names"): b_names,
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
    L = ["/* G5MATH-STRANDS-BEGIN (generated by source/tools/gen_g5math.py, edit the generator, not this block) */",
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append("var G5PIC=%s;" % json.dumps(data, ensure_ascii=False))
    L.append(P1.APPLY.replace("G1PIC", "G5PIC"))
    L.append("/* G5MATH-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G5, encoding="utf8").read()
    if "G5MATH-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G5MATH-STRANDS-BEGIN.*?G5MATH-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        s = src.rstrip()
        assert s.endswith("})();"), s[-40:]
        src = s[:-5] + block + "\n})();\n"
    open(G5, "w", encoding="utf8").write(src)
    print("parts:", sum(len(p) for std in data.values() for p in std.values()), "block bytes:", len(block))


if __name__ == "__main__":
    main()
