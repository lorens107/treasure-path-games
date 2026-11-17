"""Builds the parts (strands) for the Grade 8 math standards, all 10 LPs, and writes them into source/gx/g8.js.

No Grade 8 gradebook "I can" lines exist in the project, so each standard is split by the sub-skills written inside
the CCSS wording (Loren chose this approach for Grade 6 onward).
Run:  python3 source/tools/gen_g8math.py
"""
import json, os, re, sys, math
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N
import gen_g1pic as P1
import gen_g5math as G5

G8 = os.path.join(HERE, '..', 'gx', 'g8.js')
THEME, rng_for, nm, BAD = N.THEME, N.rng_for, N.nm, N.BAD
svg, row = P1.svg, P1.row
INK = P1.INK
mixed, fstr = G5.mixed, G5.fstr
MINUS = "−"
SUP = {0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹"}


def C(*p):
    return list(p)


def sg(n):
    if isinstance(n, F):
        s = mixed(abs(n))
        return (MINUS + s) if n < 0 else s
    return (MINUS + str(-n)) if n < 0 else str(n)


def pw(base, e):
    """base with a superscript exponent (supports negatives)"""
    s = "".join(SUP[int(c)] for c in str(abs(e)))
    return "%s%s%s" % (base, MINUS.replace("−", "⁻") if e < 0 else "", s)


def pick(pool, k, r):
    p = pool[:]
    r.shuffle(p)
    return p[:k]


CAT = {
    "8.NS.A.1": {"desc": "rational and irrational numbers", "parts": C(
        ("rational", "Rational numbers and repeating decimals", "Showing that every rational number has a decimal expansion that ends or repeats and converting a repeating decimal to a fraction"),
        ("irrational", "Tell rational from irrational numbers", "Knowing that numbers that are not rational are irrational"),
        ("approx", "Approximate irrational numbers", "Using rational approximations of irrational numbers to compare their size and locate them on a number line"))},
    "8.EE.A.1": {"desc": "properties of integer exponents", "parts": C(
        ("product", "Multiply and divide powers with the same base", "Using the product and quotient properties of integer exponents to write equivalent numerical expressions"),
        ("power", "Raise a power to a power", "Using the power of a power and power of a product properties of integer exponents to write equivalent numerical expressions"),
        ("zeroneg", "Zero and negative exponents", "Using zero and negative integer exponents to write equivalent numerical expressions"))},
    "8.EE.A.2": {"desc": "square roots and cube roots", "parts": C(
        ("solve", "Solve x² = p and x³ = p", "Solving equations of the form x² = p and x³ = p where p is a positive rational number"),
        ("evaluate", "Evaluate square roots and cube roots", "Evaluating square roots of small perfect squares and cube roots of small perfect cubes"),
        ("irrational", "Square roots that are irrational", "Knowing that the square root of a non-perfect square is irrational and estimating it"))},
    "8.EE.B.5": {"desc": "proportional relationships, unit rate as slope, and comparing relationships", "parts": C(
        ("graph", "Graph a proportional relationship", "Graphing proportional relationships"),
        ("slope", "Unit rate as the slope of a graph", "Interpreting the unit rate as the slope of the graph of a proportional relationship"),
        ("compare", "Compare two proportional relationships", "Comparing two different proportional relationships represented in different ways"))},
    "8.EE.C.8": {"desc": "systems of two linear equations", "parts": C(
        ("graph", "Solutions of a system as the point where lines meet", "Understanding that solutions to a system of two linear equations in two variables correspond to points of intersection of their graphs"),
        ("algebra", "Solve a system by substitution or elimination", "Solving systems of two linear equations in two variables algebraically"),
        ("world", "Solve real-world problems with systems", "Solving real-world and mathematical problems leading to two linear equations in two variables"))},
    "8.F.A.1": {"desc": "functions as rules with exactly one output for each input", "parts": C(
        ("decide", "Decide if a relation is a function", "Understanding that a function assigns exactly one output to each input and deciding whether a relation is a function"),
        ("rule", "Use a function rule and its ordered pairs", "Using a function rule to find outputs and writing the graph of a function as a set of ordered pairs"))},
    "8.F.A.3": {"desc": "linear functions y = mx + b and nonlinear functions", "parts": C(
        ("identify", "Tell linear functions from nonlinear ones", "Interpreting the equation y = mx + b as defining a linear function and identifying functions that are not linear"),
        ("examples", "Give examples of nonlinear functions", "Giving examples of functions that are not linear"))},
    "8.G.A.3": {"desc": "dilations, translations, rotations, and reflections using coordinates", "parts": C(
        ("translate", "Translate figures using coordinates", "Describing the effect of translations on two-dimensional figures using coordinates"),
        ("reflect", "Reflect figures using coordinates", "Describing the effect of reflections on two-dimensional figures using coordinates"),
        ("rotate", "Rotate figures using coordinates", "Describing the effect of rotations on two-dimensional figures using coordinates"),
        ("dilate", "Dilate figures using coordinates", "Describing the effect of dilations on two-dimensional figures using coordinates"))},
    "8.G.B.7": {"desc": "the Pythagorean theorem to find unknown side lengths", "parts": C(
        ("math", "Find unknown sides in right triangles", "Applying the Pythagorean theorem to find unknown side lengths in right triangles in mathematical problems"),
        ("real", "Real-world problems with right triangles", "Applying the Pythagorean theorem to find unknown side lengths in right triangles in real-world problems"),
        ("threed", "Right triangles in three dimensions", "Applying the Pythagorean theorem to find unknown side lengths in right triangles in three-dimensional problems"))},
    "8.SP.A.1": {"desc": "scatter plots and patterns of association", "parts": C(
        ("construct", "Make a scatter plot from data", "Constructing scatter plots for bivariate measurement data"),
        ("describe", "Describe the pattern of a scatter plot", "Describing patterns in scatter plots such as positive or negative association and linear or nonlinear association"),
        ("outlier", "Clusters and outliers", "Describing clusters and outliers in scatter plots"))},
}

D1 = "Listen to each question. Show your work on your paper."


# ================================================================== NS.A.1
def expand(n, d):
    """decimal expansion of n/d (0 < n < d): returns (prefix, repeat)"""
    seen, digs, rem = {}, [], n % d
    while rem and rem not in seen:
        seen[rem] = len(digs)
        rem *= 10
        digs.append(rem // d)
        rem %= d
    if rem == 0:
        return "".join(map(str, digs)), ""
    i = seen[rem]
    return "".join(map(str, digs[:i])), "".join(map(str, digs[i:]))


def show(n, d):
    pre, rep = expand(n, d)
    if not rep:
        return "0." + pre
    return "0." + pre + rep * 3 + "..."


def b_rational(lp, r):
    ds = r.sample([3, 6, 9, 11, 12], 1)
    d1 = ds[0]
    n1 = r.choice([x for x in range(1, d1) if gcd(x, d1) == 1])
    dg = r.randint(1, 9)
    ab = r.choice([12, 45, 27, 36, 63, 81])
    frac_ab = F(ab, 99)
    qs = ["Use long division to write %d/%d as a decimal. Does it end or repeat?" % (n1, d1),
          "Write 0.%s... (the %d repeats forever) as a fraction. Use x = 0.%s..., then 10x." % (str(dg) * 3, dg, str(dg) * 3),
          "Write 0.%s%s%s... (the block %s repeats forever) as a fraction in simplest form. Use 100x." % (str(ab).zfill(2), str(ab).zfill(2), str(ab).zfill(2), str(ab).zfill(2))]
    pre, rep = expand(n1, d1)
    key = ["%s The digits '%s' repeat, so it repeats." % (show(n1, d1), rep) if rep else "%s. It ends." % show(n1, d1),
           "%s. 10x = %s.%s..., so 10x − x = %d, and 9x = %d, so x = %s." % (fstr(F(dg, 9)), dg, str(dg) * 3, dg, dg, fstr(F(dg, 9))),
           "%s. 100x − x = %d, so 99x = %d and x = %d/99 = %s." % (fstr(frac_ab), ab, ab, ab, fstr(frac_ab))]
    return dict(qs=qs, key=key, dir=D1, dur=200)


def b_irrational(lp, r):
    n1 = r.choice([2, 3, 5, 6, 7, 10, 11])
    n2 = r.choice([16, 25, 36, 49, 64, 81])
    ab = r.choice(["12", "27", "45", "36"])
    qs = ["Is √%d rational or irrational? Tell how you know." % n1,
          "Is √%d rational or irrational? Tell how you know." % n2,
          "Is 0.%s%s%s... (the block %s repeats forever) rational or irrational? Why?" % (ab, ab, ab, ab)]
    key = ["Irrational. %d is not a perfect square, so its square root is a decimal that never ends and never repeats." % n1,
           "Rational. %d is a perfect square, so √%d = %d, a whole number." % (n2, n2, int(math.sqrt(n2))),
           "Rational. A decimal that repeats can be written as a fraction (%s/99)." % ab]
    return dict(qs=qs, key=key, dir=D1, dur=160)


def b_approx(lp, r):
    a, b, c = r.sample([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15], 3)
    tenth = lambda n: ("%.1f" % math.sqrt(n))
    k = r.choice([2, 3, 4, 5, 6])
    x = r.choice([n for n in (11, 12, 13, 14, 15, 17, 18, 19, 20) if abs(math.sqrt(n) - k) > 0.05])
    qs = ["Between which two whole numbers is √%d? Which is it closer to?" % a,
          "Estimate √%d to the nearest tenth. Check by squaring your answer." % b,
          "Which is greater, √%d or %d? Use a rational approximation to decide." % (x, k)]
    lo = int(math.floor(math.sqrt(a)))
    near = lo if math.sqrt(a) - lo < 0.5 else lo + 1
    key = ["Between %d and %d, because %d² = %d and %d² = %d. It is closer to %d (√%d ≈ %s)." % (lo, lo + 1, lo, lo * lo, lo + 1, (lo + 1) ** 2, near, a, tenth(a)),
           "About %s. %s² = %.2f, which is close to %d." % (tenth(b), tenth(b), float(tenth(b)) ** 2, b),
           "%s is greater. √%d ≈ %s, and %s %s %d." % ("√%d" % x if math.sqrt(x) > k else str(k), x, tenth(x), tenth(x), ">" if math.sqrt(x) > k else "<", k)]
    return dict(qs=qs, key=key, dir=D1, dur=190)


# ================================================================== EE.A.1
def b_product(lp, r):
    b1, m1, n1 = r.choice([2, 3, 5, 7]), r.randint(2, 6), r.randint(2, 6)
    b2, m2, n2 = r.choice([2, 3, 5, 10]), r.randint(6, 9), r.randint(2, 5)
    b3, m3, n3 = r.choice([3, 4, 5]), r.randint(2, 4), r.randint(2, 4)
    qs = ["Write %s × %s as one power. Then check by writing both out as repeated multiplication if you need to." % (pw(b1, m1), pw(b1, n1)),
          "Write %s ÷ %s as one power." % (pw(b2, m2), pw(b2, n2)),
          "Write %s × %s ÷ %s as one power, and find its value." % (pw(b3, m3 + 2), pw(b3, n3 + 1), pw(b3, 3))]
    e3 = m3 + 2 + n3 + 1 - 3
    key = ["%s. Add the exponents: %d + %d = %d." % (pw(b1, m1 + n1), m1, n1, m1 + n1),
           "%s. Subtract the exponents: %d − %d = %d." % (pw(b2, m2 - n2), m2, n2, m2 - n2),
           "%s = %d. (%d + %d) − 3 = %d." % (pw(b3, e3), b3 ** e3, m3 + 2, n3 + 1, e3)]
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_power(lp, r):
    b1, m1, n1 = r.choice([2, 3, 4, 5]), r.randint(2, 4), r.randint(2, 4)
    b2, m2 = r.choice([2, 3, 5]), r.randint(2, 4)
    c, d, e = r.choice([2, 3, 5]), r.choice([2, 5, 10]), r.randint(2, 4)
    qs = ["Write (%s)%s as one power." % (pw(b1, m1), SUP[n1]),
          "Write (%s)%s as one power and find its value." % (pw(b2, 2), SUP[m2]),
          "Write (%d × %d)%s as a product of two powers. Then find the value." % (c, d, SUP[e])]
    key = ["%s. Multiply the exponents: %d × %d = %d." % (pw(b1, m1 * n1), m1, n1, m1 * n1),
           "%s = %d. Multiply the exponents: 2 × %d = %d." % (pw(b2, 2 * m2), b2 ** (2 * m2), m2, 2 * m2),
           "%s × %s = %d × %d = %d." % (pw(c, e), pw(d, e), c ** e, d ** e, (c * d) ** e)]
    return dict(qs=qs, key=key, dir=D1, dur=180)


def b_zeroneg(lp, r):
    b0 = r.choice([7, 12, 25, 100])
    b1, e1 = r.choice([2, 3, 5]), r.randint(2, 3)
    b2, e2 = 10, r.randint(2, 4)
    b3, m3, n3 = r.choice([2, 3, 5]), r.randint(1, 2), r.randint(3, 5)
    qs = ["What is %s? Explain why." % pw(b0, 0),
          "Write %s as a fraction. Then do the same for %s." % (pw(b1, -e1), pw(b2, -e2)),
          "Write %s × %s as one power and find its value as a fraction or whole number." % (pw(b3, -m3), pw(b3, n3))]
    key = ["1. Any nonzero number to the zero power is 1. For example, %s ÷ %s = %s and any number divided by itself is 1." % (pw(b0, 3), pw(b0, 3), pw(b0, 0)),
           "%s = 1/%d. %s = 1/%s." % (pw(b1, -e1), b1 ** e1, pw(b2, -e2), "{:,}".format(10 ** e2)),
           "%s = %d. Add the exponents: %s + %d = %d." % (pw(b3, n3 - m3), b3 ** (n3 - m3), MINUS + str(m3), n3, n3 - m3)]
    return dict(qs=qs, key=key, dir=D1, dur=180)


# ================================================================== EE.A.2
def b_sqsolve(lp, r):
    p = r.choice([16, 25, 36, 49, 64, 81, 100, 121])
    q = r.choice([8, 27, 64, 125])
    fr = r.choice([(1, 4), (4, 9), (9, 25), (16, 49)])
    qs = ["Solve x² = %d. Give both solutions." % p,
          "Solve x³ = %d." % q,
          "A square has an area of %d square inches. What is the length of one side? Why is there only one answer?" % r.choice([49, 64, 81])]
    # recompute third to stay consistent
    area = int(qs[2].split("area of ")[1].split(" ")[0])
    key = ["x = %d or x = %s. Both %d² and (%s)² equal %d." % (math.isqrt(p), MINUS + str(math.isqrt(p)), math.isqrt(p), MINUS + str(math.isqrt(p)), p),
           "x = %d, because %d³ = %d." % (round(q ** (1 / 3.0)), round(q ** (1 / 3.0)), q),
           "%d inches. s² = %d, so s = %d. A length cannot be negative." % (math.isqrt(area), area, math.isqrt(area))]
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_sqeval(lp, r):
    a = r.choice([9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
    b = r.choice([8, 27, 64, 125, 216])
    f = r.choice([(F(1, 4), 2), (F(4, 9), 3), (F(9, 16), 4), (F(1, 9), 3), (F(25, 36), 6)])
    g = r.choice([(F(1, 8), 2), (F(8, 27), 3), (F(27, 64), 4)])
    qs = ["Evaluate √%d." % a, "Evaluate ∛%d." % b,
          "Evaluate √(%s) and ∛(%s)." % (fstr(f[0]), fstr(g[0]))]
    key = ["%d, because %d × %d = %d." % (math.isqrt(a), math.isqrt(a), math.isqrt(a), a),
           "%d, because %d × %d × %d = %d." % (round(b ** (1 / 3.0)), round(b ** (1 / 3.0)), round(b ** (1 / 3.0)), round(b ** (1 / 3.0)), b),
           "√(%s) = %s and ∛(%s) = %s." % (fstr(f[0]), fstr(F(1) * F(math.isqrt(f[0].numerator), math.isqrt(f[0].denominator))), fstr(g[0]), fstr(F(round(g[0].numerator ** (1 / 3.0)), round(g[0].denominator ** (1 / 3.0)))))]
    return dict(qs=qs, key=key, dir=D1, dur=160)


def b_sqirr(lp, r):
    a, b, c = r.sample([2, 3, 5, 6, 7, 10, 11, 12, 13, 15], 3)
    cube = r.choice([2, 3, 4, 5, 6, 7, 9, 10])
    ten = lambda n: "%.1f" % math.sqrt(n)
    qs = ["Is √%d a decimal that ends or repeats? Tell how you know." % a,
          "Between which two whole numbers is √%d? Estimate it to the nearest tenth." % b,
          "Between which two whole numbers is ∛%d? How do you know?" % cube]
    lo = int(math.floor(math.sqrt(b)))
    cl = int(math.floor(cube ** (1 / 3.0)))
    key = ["No. %d is not a perfect square, so √%d is irrational. Its decimal never ends and never repeats." % (a, a),
           "Between %d and %d. √%d is about %s." % (lo, lo + 1, b, ten(b)),
           "Between %d and %d, because %d³ = %d and %d³ = %d." % (cl, cl + 1, cl, cl ** 3, cl + 1, (cl + 1) ** 3)]
    return dict(qs=qs, key=key, dir=D1, dur=170)


# ================================================================== EE.B.5
def b_pgraph(lp, r):
    k1 = r.choice([2, 3, 4, 5, F(3, 2)])
    k2, x2 = r.choice([(3, 4), (5, 3), (2, 6), (4, 5)])
    n0 = nm(lp, 0)
    k3 = r.choice([6, 8, 9, 12])
    qs = ["Make a table of 3 points for y = %sx and graph it. What does the graph look like?" % (fstr(F(k1)) if isinstance(k1, F) else k1),
          "A straight line goes through the origin and the point (%d, %d). Write its equation y = kx." % (x2, k2 * x2),
          "%s earns $%d per hour. Graph earnings (y) against hours (x). Where does the line start, and how steep is it?" % (n0, k3)]
    kk = F(k1)
    key = ["For example (0, 0), (2, %s), (4, %s). The graph is a straight line through the origin." % (mixed(kk * 2), mixed(kk * 4)),
           "y = %dx, because %d ÷ %d = %d." % (k2, k2 * x2, x2, k2),
           "The line starts at the origin (0, 0). It goes up %d for every 1 hour across, so the steepness (slope) is %d." % (k3, k3)]
    return dict(qs=qs, key=key, dir=D1, dur=180)


def b_pslope(lp, r):
    a, b = r.choice([(2, 5), (3, 9), (4, 6), (5, 15), (2, 3)])
    mi, hr = r.choice([(150, 3), (180, 4), (240, 4), (90, 2)])
    k = r.choice([2, 3, 4, 6])
    qs = ["A line through the origin also passes through (%d, %d). What is the slope? What is the unit rate?" % (a, b),
          "A car's graph of distance against time goes through (0, 0) and (%d, %d). What is the slope, and what does it mean in this situation (miles and hours)?" % (hr, mi),
          "The equation of a proportional relationship is y = %dx. What is the slope of its graph? What is the value of y when x = 1?" % k]
    key = ["%s. The slope is %d ÷ %d = %s, and the unit rate is the same: %s." % (mixed(F(b, a)), b, a, mixed(F(b, a)), mixed(F(b, a))),
           "%d. The slope is %d ÷ %d = %d, so the car goes %d miles per hour." % (mi // hr, mi, hr, mi // hr, mi // hr),
           "The slope is %d. When x = 1, y = %d, which is the unit rate." % (k, k)]
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_pcompare(lp, r):
    n0, n1 = nm(lp, 0), nm(lp, 1)
    s1, s2 = r.choice([(50, 45), (60, 55), (40, 35)])
    t, d = r.choice([(2, 120), (3, 150), (2, 90)])
    ka, kb = r.choice([(4, 3), (5, 4), (6, 5)])
    xx, yy = r.choice([(2, 7), (3, 9), (4, 14)])
    ca = F(yy, xx)
    qs = ["%s drives at a steady speed with the equation d = %dt. %s drives so that the graph passes through (0, 0) and (%d, %d). Who is faster? By how many miles per hour?" % (n0, s1, n1, t, d),
          "Plan A is y = %dx. Plan B has this table: x: 1, 2, 3 and y: %d, %d, %d. Which plan has the greater unit rate?" % (ka, kb, 2 * kb, 3 * kb),
          "Line A is y = %dx. Line B goes through (0, 0) and (%d, %d). Which line is steeper? How do you know?" % (r.choice([2, 3]), xx, yy)]
    sA = int(qs[2].split("y = ")[1].split("x")[0])
    key = ["%s: %d mph. %s: %d ÷ %d = %d mph. %s." % (n0, s1, n1, d, t, d // t, "%s is faster by %d mph" % (n0, s1 - d // t) if s1 > d // t else "%s is faster by %d mph" % (n1, d // t - s1) if d // t > s1 else "They are equal"),
           "Plan A: %d. Plan B: %d. Plan A has the greater unit rate by %d." % (ka, kb, ka - kb),
           "Line A has slope %d. Line B has slope %d ÷ %d = %s. %s is steeper." % (sA, yy, xx, mixed(ca), "Line A" if sA > ca else "Line B")]
    return dict(qs=qs, key=key, dir=D1, dur=200)


# ================================================================== EE.C.8
def sys_through(r, a, b):
    m1 = r.choice([1, 2, 3, -1, -2])
    m2 = r.choice([x for x in (1, 2, -1, -2, -3, 3) if x != m1])
    return m1, b - m1 * a, m2, b - m2 * a


def lin(m, c):
    s = "y = "
    s += ("%d" % m if m not in (1, -1) else ("" if m == 1 else MINUS)).replace("-", MINUS) + "x"
    if c > 0:
        s += " + %d" % c
    elif c < 0:
        s += " %s %d" % (MINUS, -c)
    return s


def b_sgraph(lp, r):
    a, b = r.randint(1, 5), r.randint(2, 8)
    m1, c1, m2, c2 = sys_through(r, a, b)
    a2, b2 = r.randint(1, 4), r.randint(1, 7)
    m3 = r.choice([2, 3])
    c3, c4 = r.randint(1, 4), r.randint(5, 9)
    qs = ["Two lines on a graph cross at the point (%d, %d). What is the solution to the system, and why?" % (a, b),
          "Is (%d, %d) a solution of this system? %s and %s. Check both equations." % (a, b, lin(m1, c1), lin(m2, c2)),
          "The system is %s and %s. Without solving, how many solutions does it have? What do the graphs look like?" % (lin(m3, c3), lin(m3, c4))]
    key = ["(%d, %d). The solution is the point that is on both lines, so it makes both equations true." % (a, b),
           "Yes. First equation: when x = %d, y = %d. Second equation: when x = %d, y = %d. Both give y = %d." % (a, m1 * a + c1, a, m2 * a + c2, b),
           "No solutions. The lines have the same slope (%d) and different y-intercepts (%d and %d), so they are parallel and never cross." % (m3, c3, c4)]
    return dict(qs=qs, key=key, dir=D1, dur=200)


def b_salg(lp, r):
    x, y = r.randint(1, 6), r.randint(1, 8)
    m, c1 = r.choice([2, 3, 4]), r.randint(0, 3)
    m2 = m + r.choice([1, 2, -1])
    c2 = (m - m2) * x + c1
    s_, d_ = x + y, x - y
    Y = m * x + c1
    c2b = Y - m2 * x
    qs = ["Solve the system: %s and %s." % (lin(m, c1), lin(m2, c2b)),
          "Solve by elimination: x + y = %d and x − y = %s." % (s_, sg(d_)),
          "Solve: x + y = 6 and 2x + 2y = 12. How many solutions are there?"]
    key = ["x = %d, y = %d. Set the two y's equal: %s = %s. Solve for x, then put x = %d into either equation to get y = %d." % (x, Y, lin(m, c1)[4:], lin(m2, c2b)[4:], x, Y),
           "x = %d, y = %d. Add the equations: 2x = %d, so x = %d. Then y = %d − %d = %d." % (x, y, s_ + d_, x, s_, x, y),
           "Infinitely many solutions. The second equation is the first one times 2, so they are the same line."]
    return dict(qs=qs, key=key, dir=D1, dur=240)


def b_sworld(lp, r):
    n0, n1 = nm(lp, 0), nm(lp, 1)
    A, B = r.randint(20, 40), r.randint(15, 35)
    pa, pc = r.choice([(8, 5), (10, 6), (9, 4)])
    N, T = A + B, pa * A + pc * B
    pr, fee1, fee2, rate1, rate2 = None, r.randint(10, 20), r.randint(25, 40), r.choice([6, 8, 10]), None
    rate2 = rate1 - r.choice([2, 3])
    mm = (fee2 - fee1) // 1
    # plans: cost1 = fee1 + rate1 x ; cost2 = fee2 + rate2 x ; equal at x where (rate1-rate2)x = fee2-fee1
    rd = rate1 - rate2
    while (fee2 - fee1) % rd:
        fee2 += 1
    xe = (fee2 - fee1) // rd
    nk, dm = r.randint(8, 16), r.randint(5, 12)
    tot, val = nk + dm, 5 * nk + 10 * dm
    qs = ["A theater sold %d tickets. Adult tickets cost $%d and child tickets cost $%d. The theater made $%d. How many adult and child tickets were sold? Write a system of equations." % (N, pa, pc, T),
          "Plan 1 costs $%d plus $%d per class. Plan 2 costs $%d plus $%d per class. After how many classes do the plans cost the same? What is that cost?" % (fee1, rate1, fee2, rate2),
          "%s has %d coins, all nickels and dimes, worth $%.2f. How many of each coin? Write a system of equations." % (n0, tot, val / 100.0)]
    key = ["%d adult and %d child tickets. a + c = %d and %d a + %d c = %d." % (A, B, N, pa, pc, T),
           "%d classes. %d + %dx = %d + %dx gives %dx = %d, so x = %d. The cost is $%d." % (xe, fee1, rate1, fee2, rate2, rd, fee2 - fee1, xe, fee1 + rate1 * xe),
           "%d nickels and %d dimes. n + d = %d and 5n + 10d = %d." % (nk, dm, tot, val)]
    return dict(qs=qs, key=key, dir=D1, dur=240)


# ================================================================== F.A.1
def b_fdecide(lp, r):
    a, b, c = r.sample(range(1, 9), 3)
    pairs_f = [(a, b), (c, b), (4 + a, 2 * c)]
    xs = r.sample(range(1, 9), 3)
    pairs_n = [(xs[0], 2), (xs[1], 5), (xs[0], 7)]
    pool_f = [("Input: a student in class. Output: that student's birthday.", "Yes, it is a function. Each student has exactly one birthday."),
              ("Input: a whole number. Output: the number doubled.", "Yes, it is a function. Each number has exactly one double.")]
    pool_n = [("Input: a birthday. Output: the students who have that birthday.", "No. One birthday can match more than one student, so one input has more than one output.")]
    qs = ["Is this a function? Ordered pairs (input, output): %s." % ", ".join("(%d, %d)" % p for p in pairs_f),
          "Is this a function? Ordered pairs (input, output): %s." % ", ".join("(%d, %d)" % p for p in pairs_n),
          pool_f[r.randint(0, 1)][0] if r.random() < 0.5 else pool_n[0][0]]
    last = qs[2]
    ans3 = [k for q, k in pool_f + pool_n if q == last][0]
    key = ["Yes. Each input has exactly one output (no input repeats with a different output).",
           "No. The input %d goes with two outputs (2 and 7)." % pairs_n[0][0], ans3]
    return dict(qs=qs, key=key, dir=D1, dur=180)


def b_frule(lp, r):
    m, c = r.choice([(3, 2), (2, 5), (4, 1), (5, 3)])
    x1, x2 = r.randint(2, 6), r.randint(-4, -1)
    t = m * r.randint(3, 6) + c
    qs = ["A function is f(x) = %dx + %d. Find f(%d)." % (m, c, x1),
          "For f(x) = %dx + %d, what is the output when the input is %s?" % (m, c, MINUS + str(-x2)),
          "For f(x) = %dx + %d, what input gives an output of %d? Then write 3 ordered pairs on the graph of this function." % (m, c, t)]
    key = ["%d. f(%d) = %d × %d + %d = %d." % (m * x1 + c, x1, m, x1, c, m * x1 + c),
           "%s. %d × (%s) + %d = %s." % (sg(m * x2 + c), m, sg(x2), c, sg(m * x2 + c)),
           "x = %d, because %d × %d + %d = %d. Ordered pairs such as (0, %d), (1, %d), (2, %d)." % ((t - c) // m, m, (t - c) // m, c, t, c, m + c, 2 * m + c)]
    return dict(qs=qs, key=key, dir=D1, dur=190)


# ================================================================== F.A.3
def b_fident(lp, r):
    m, c = r.choice([(2, 3), (4, 1), (3, 5), (5, 2)])
    st, ra = r.choice([(2, 3), (3, 4), (1, 5)])
    qs = ["Which of these is a linear function: y = %dx + %d, y = x², or y = 6/x? How do you know?" % (m, c),
          "A table has x: 0, 1, 2, 3 and y: %d, %d, %d, %d. Is this a linear function? What are m and b?" % (c, c + m, c + 2 * m, c + 3 * m),
          "A table has x: 1, 2, 3, 4 and y: 1, 4, 9, 16. Is this a linear function? Explain."]
    key = ["y = %dx + %d. It has the form y = mx + b with m = %d and b = %d, so its graph is a straight line." % (m, c, m, c),
           "Yes. y goes up by %d each time x goes up by 1, so the rate of change is constant. m = %d and b = %d." % (m, m, c),
           "No. y goes up by 3, then 5, then 7, so the rate of change is not constant."]
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_fexamples(lp, r):
    s = r.choice([2, 3, 4, 5])
    qs = ["The area of a square with side s is A = s². Make a table for s = 1, 2, 3, 4. Is this function linear?",
          "Give an example of an equation that is a function but not linear. Show 3 ordered pairs.",
          "A square has a side of %d. A second square has a side twice as long. Is the area function linear? Does the area double?" % s]
    key = ["s: 1, 2, 3, 4 and A: 1, 4, 9, 16. Not linear, because the rate of change is not constant (the differences are 3, 5, 7).",
           "For example y = x². Ordered pairs: (1, 1), (2, 4), (3, 9). The graph is a curve, not a line.",
           "No, it is not linear. The first area is %d and the second is %d, which is 4 times as big, not double." % (s * s, 4 * s * s)]
    return dict(qs=qs, key=key, dir=D1, dur=170)


# ================================================================== G.A.3
def pts_str(p):
    return ", ".join("(%s, %s)" % (sg(x), sg(y)) for x, y in p)


def shape(r, n=3):
    while True:
        p = [(r.randint(-5, 5), r.randint(-5, 5)) for _ in range(n)]
        if len(set(p)) == n and all(x != 0 and y != 0 for x, y in p):
            return p


def b_translate(lp, r):
    p = shape(r)
    dx, dy = r.choice([(3, 2), (-4, 1), (2, -5), (-3, -2)])
    q = shape(r, 4)
    dx2, dy2 = r.choice([(5, 2), (3, -4), (-2, 3)])
    pt = (r.randint(-6, 6), r.randint(-6, 6))
    qs = ["Triangle ABC has vertices %s. Translate it with the rule (x, y) → (x %s, y %s). Give the new vertices." % (pts_str(p), ("+ %d" % dx) if dx >= 0 else "%s %d" % (MINUS, -dx), ("+ %d" % dy) if dy >= 0 else "%s %d" % (MINUS, -dy)),
          "Quadrilateral has vertices %s. Give the new vertices after the translation (x, y) → (x %s, y %s)." % (pts_str(q), ("+ %d" % dx2) if dx2 >= 0 else "%s %d" % (MINUS, -dx2), ("+ %d" % dy2) if dy2 >= 0 else "%s %d" % (MINUS, -dy2)),
          "A point at %s moves to %s after a translation. What is the translation rule?" % (pts_str([pt]), pts_str([(pt[0] + dx, pt[1] + dy)]))]
    key = ["%s. Add %s to each x and %s to each y." % (pts_str([(x + dx, y + dy) for x, y in p]), sg(dx), sg(dy)),
           "%s." % pts_str([(x + dx2, y + dy2) for x, y in q]),
           "(x, y) → (x %s, y %s). The point moved %s in x and %s in y." % (("+ %d" % dx) if dx >= 0 else "%s %d" % (MINUS, -dx), ("+ %d" % dy) if dy >= 0 else "%s %d" % (MINUS, -dy), sg(dx), sg(dy))]
    return dict(qs=qs, key=key, dir=D1, dur=200)


def b_reflect(lp, r):
    p = shape(r)
    q = shape(r, 4)
    pt = shape(r, 1)[0]
    qs = ["Triangle ABC has vertices %s. Reflect it across the x-axis. Give the new vertices." % pts_str(p),
          "Quadrilateral has vertices %s. Reflect it across the y-axis. Give the new vertices." % pts_str(q),
          "Point P is at %s. Where is it after a reflection across the x-axis, and then a reflection across the y-axis?" % pts_str([pt])]
    key = ["%s. Reflecting across the x-axis changes the sign of y: (x, y) → (x, %sy)." % (pts_str([(x, -y) for x, y in p]), MINUS),
           "%s. Reflecting across the y-axis changes the sign of x: (x, y) → (%sx, y)." % (pts_str([(-x, y) for x, y in q]), MINUS),
           "%s, then %s. Both signs changed, so it is the same as a 180° rotation." % (pts_str([(pt[0], -pt[1])]), pts_str([(-pt[0], -pt[1])]))]
    return dict(qs=qs, key=key, dir=D1, dur=190)


def b_rotate(lp, r):
    p = shape(r)
    q = shape(r, 3)
    pt = shape(r, 1)[0]
    qs = ["Triangle ABC has vertices %s. Rotate it 90° counterclockwise about the origin. Give the new vertices." % pts_str(p),
          "Triangle DEF has vertices %s. Rotate it 180° about the origin. Give the new vertices." % pts_str(q),
          "Point P is at %s. Where is it after a 90° clockwise rotation about the origin?" % pts_str([pt])]
    key = ["%s. The rule is (x, y) → (%sy, x)." % (pts_str([(-y, x) for x, y in p]), MINUS),
           "%s. The rule is (x, y) → (%sx, %sy)." % (pts_str([(-x, -y) for x, y in q]), MINUS, MINUS),
           "%s. The rule is (x, y) → (y, %sx)." % (pts_str([(pt[1], -pt[0])]), MINUS)]
    return dict(qs=qs, key=key, dir=D1, dur=200)


def b_dilate(lp, r):
    k1 = r.choice([2, 3])
    k2 = r.choice([F(1, 2), F(1, 3)])
    base = 6 if k2 == F(1, 2) else 6
    p = [(r.choice([-4, -2, 2, 4]) * 1, r.choice([-4, -2, 2, 4]) * 1) for _ in range(3)]
    while len(set(p)) < 3:
        p = [(r.choice([-4, -2, 2, 4]), r.choice([-4, -2, 2, 4])) for _ in range(3)]
    q = [(x * 3, y * 3) for x, y in p]
    k3 = r.choice([2, 3])
    pt = (r.randint(1, 5), r.randint(-5, -1))
    qs = ["Triangle ABC has vertices %s. Dilate it from the origin by a scale factor of %d. Give the new vertices." % (pts_str(p), k1),
          "Triangle DEF has vertices %s. Dilate it from the origin by a scale factor of 1/3. Give the new vertices." % pts_str(q),
          "Point P is at %s. After a dilation from the origin it is at %s. What is the scale factor? Is the image similar or congruent to the original?" % (pts_str([pt]), pts_str([(pt[0] * k3, pt[1] * k3)]))]
    key = ["%s. Multiply each coordinate by %d." % (pts_str([(x * k1, y * k1) for x, y in p]), k1),
           "%s. Multiply each coordinate by 1/3 (divide by 3)." % pts_str(p),
           "%d. %d × %s = %s. A dilation with a scale factor other than 1 makes a similar figure, not a congruent one." % (k3, k3, sg(pt[0]), sg(pt[0] * k3))]
    return dict(qs=qs, key=key, dir=D1, dur=200)


# ================================================================== G.B.7
TRI = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (20, 21, 29), (12, 16, 20)]


def b_pmath(lp, r):
    a, b, c = r.choice(TRI)
    a2, b2, c2 = r.choice([t for t in TRI if t != (a, b, c)])
    l1, l2 = r.choice([(3, 5), (4, 7), (2, 6), (5, 6)])
    qs = ["A right triangle has legs of %d and %d. Find the hypotenuse." % (a, b),
          "A right triangle has a hypotenuse of %d and one leg of %d. Find the other leg." % (c2, a2),
          "A right triangle has legs of %d and %d. Find the hypotenuse. Give the answer as a square root and as a decimal rounded to the nearest tenth." % (l1, l2)]
    key = ["%d. %d² + %d² = %d + %d = %d, and √%d = %d." % (c, a, b, a * a, b * b, c * c, c * c, c),
           "%d. %d² − %d² = %d − %d = %d, and √%d = %d." % (b2, c2, a2, c2 * c2, a2 * a2, b2 * b2, b2 * b2, b2),
           "√%d ≈ %.1f. %d² + %d² = %d." % (l1 * l1 + l2 * l2, math.sqrt(l1 * l1 + l2 * l2), l1, l2, l1 * l1 + l2 * l2)]
    return dict(qs=qs, key=key, dir=D1, dur=190)


def b_preal(lp, r):
    n0, n1 = nm(lp, 0), nm(lp, 1)
    h, base, L = r.choice([(12, 5, 13), (15, 8, 17), (24, 7, 25), (16, 12, 20)])
    w, ht, dg = r.choice([(24, 18, 30), (16, 12, 20), (32, 24, 40)])
    fa, fb, fd = r.choice([(30, 40, 50), (60, 80, 100), (45, 60, 75)])
    qs = ["%s leans a %d foot ladder against a wall. The bottom of the ladder is %d feet from the wall. How high up the wall does the ladder reach?" % (n0, L, base),
          "A TV screen is %d inches wide and %d inches tall. How long is the diagonal of the screen?" % (w, ht),
          "%s walks %d yards east and then %d yards north. How far is %s from the start in a straight line?" % (n1, fa, fb, n1)]
    key = ["%d feet. %d² − %d² = %d, and √%d = %d." % (h, L, base, h * h, h * h, h),
           "%d inches. %d² + %d² = %d, and √%d = %d." % (dg, w, ht, dg * dg, dg * dg, dg),
           "%d yards. %d² + %d² = %d, and √%d = %d." % (fd, fa, fb, fd * fd, fd * fd, fd)]
    return dict(qs=qs, key=key, dir=D1, dur=190)


def b_p3d(lp, r):
    B = [(2, 3, 6, 7), (2, 6, 9, 11), (4, 4, 7, 9), (3, 4, 12, 13), (2, 10, 11, 15), (6, 6, 7, 11)]
    it = pick(B, 3, r)
    ctx = ["A box is %d inches long, %d inches wide, and %d inches tall. Find the longest straight rod that fits inside. First find the diagonal of the bottom.",
           "A room is %d feet long, %d feet wide, and %d feet tall. Find the distance from one bottom corner to the opposite top corner.",
           "A shipping crate is %d feet by %d feet by %d feet. A pole runs from one bottom corner to the opposite top corner. How long is the pole?"]
    unit = ["inches", "feet", "feet"]
    qs, key = [], []
    for (l, w, h, d), c, u in zip(it, ctx, unit):
        qs.append(c % (l, w, h))
        key.append("%d %s. Floor diagonal squared: %d² + %d² = %d. Then %d + %d² = %d, and √%d = %d." % (d, u, l, w, l * l + w * w, l * l + w * w, h, d * d, d * d, d))
    return dict(qs=qs, key=key, dir=D1, dur=220)


# ================================================================== SP.A.1
def scatter(pts, outl=None, col="#2f6fdb"):
    w, h = 270, 230
    ox, oy, pw_, ph = 36, 196, 214, 176
    body = '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (ox, oy, ox + pw_, oy, INK)
    body += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>' % (ox, oy, ox, oy - ph, INK)
    for i in range(0, 11, 2):
        x = ox + pw_ * i / 10.0
        y = oy - ph * i / 10.0
        body += '<text x="%.1f" y="%d" font-size="11" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%d</text>' % (x, oy + 15, INK, i)
        body += '<text x="%d" y="%.1f" font-size="11" font-weight="700" text-anchor="end" fill="%s" font-family="sans-serif">%d</text>' % (ox - 6, y + 4, INK, i)
    for x, y in pts:
        body += '<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="%s" stroke-width="1.5"/>' % (ox + pw_ * x / 10.0, oy - ph * y / 10.0, col, INK)
    return svg(w, h, body, "A scatter plot")


def trend(r, kind, n=9):
    xs = list(range(1, 10))[:n]
    if kind == "pos":
        a, b = r.choice([0.5, 1.0]), r.choice([0.7, 0.9, 1.0])
        pts = [(x, round(min(9.6, max(0.4, a + b * x + r.choice([-1, -0.5, 0, 0.5, 1]))) * 2) / 2.0) for x in xs]
    elif kind == "neg":
        a, b = r.choice([9.5, 9.0]), r.choice([0.7, 0.9, 1.0])
        pts = [(x, round(min(9.6, max(0.4, a - b * x + r.choice([-1, -0.5, 0, 0.5, 1]))) * 2) / 2.0) for x in xs]
    elif kind == "curve":
        pts = [(x, round(min(9.6, max(0.4, 0.15 * (x - 5) ** 2 + 1 + r.choice([-0.5, 0, 0.5]))) * 2) / 2.0) for x in xs]
    else:
        ys = [r.choice([2, 7, 4, 8, 3, 6, 5, 8.5, 2.5]) for _ in xs]
        pts = list(zip(xs, ys))
    return pts


def b_sconstruct(lp, r):
    kind = r.choice(["pos", "neg"])
    pts = trend(r, kind, 8)
    n0 = nm(lp, 0)
    qs = ["Make a scatter plot of these (x, y) pairs on graph paper: %s." % ", ".join("(%s, %s)" % (x, y if float(y) != int(y) else int(y)) for x, y in pts),
          "Look at your scatter plot. Do the points go up, go down, or do neither as x gets larger? What kind of association is that?",
          "Is the association linear or nonlinear? How could you draw one line to describe the pattern?"]
    key = ["Plot each ordered pair with x across and y up. You should have %d points." % len(pts),
           "The points go %s as x gets larger, so it is a %s association." % ("up" if kind == "pos" else "down", "positive" if kind == "pos" else "negative"),
           "Linear. The points stay close to a straight line, so one line that goes through the middle of the points describes the pattern."]
    return dict(qs=qs, key=key, dir="Listen to each question. Plot the points on your paper, then answer.", dur=240)


def b_sdescribe(lp, r):
    kinds = ["pos", "neg", r.choice(["curve", "none"])]
    r.shuffle(kinds)
    figs = [(L, scatter(trend(r, k))) for L, k in zip("ABC", kinds)]
    names = {"pos": "Positive association, linear. As x gets bigger, y gets bigger, and the points are close to a line.",
             "neg": "Negative association, linear. As x gets bigger, y gets smaller, and the points are close to a line.",
             "curve": "The points follow a curve, so it is a nonlinear association.",
             "none": "No association. The points are scattered and do not show a pattern."}
    qs = ["Describe the association in scatter plot %s. Is it positive, negative, or none? Is it linear or nonlinear?" % L for L in "ABC"]
    key = [names[k] for k in kinds]
    return dict(qs=qs, key=key, dir="Look at the three scatter plots. Your teacher asks about one at a time. Say your answer out loud.", dur=210, html=row(figs))


def b_soutlier(lp, r):
    kind = r.choice(["pos", "neg"])
    base = trend(r, kind, 8)
    ox = r.choice([6, 7, 8])
    oy = 9.0 if kind == "neg" else 1.0
    pts = [(x, y) for x, y in base if x != ox] + [(ox, oy)]
    clu = trend(r, "pos", 5)
    figA = scatter(pts)
    cl = [(x * 0.4 + 1, y * 0.3 + 6.5) for x, y in clu] + [(x * 0.35 + 6.5, y * 0.25 + 1.2) for x, y in clu]
    figB = scatter(cl, col="#c0392b")
    qs = ["Plot A has one point far from the pattern. Find its coordinates. What do we call a point like that?",
          "Describe the association in plot A if you ignore that point.",
          "Plot B has points in two groups. Where are the clusters? Is there one overall straight-line pattern?"]
    key = ["About (%s, %s). It is an outlier because it is far from the other points." % (ox, ("%g" % oy)),
           "%s association, close to a line." % ("Positive" if kind == "pos" else "Negative"),
           "One cluster is at the top left and one is at the bottom right. There is no single straight-line pattern for all the points, because the two clusters are separated."]
    return dict(qs=qs, key=key, dir="Look at plots A and B. Your teacher asks about the points. Say your answer out loud.", dur=210, html=row([("A", figA), ("B", figB)]))


BUILD = {
    ("8.NS.A.1", "rational"): b_rational, ("8.NS.A.1", "irrational"): b_irrational, ("8.NS.A.1", "approx"): b_approx,
    ("8.EE.A.1", "product"): b_product, ("8.EE.A.1", "power"): b_power, ("8.EE.A.1", "zeroneg"): b_zeroneg,
    ("8.EE.A.2", "solve"): b_sqsolve, ("8.EE.A.2", "evaluate"): b_sqeval, ("8.EE.A.2", "irrational"): b_sqirr,
    ("8.EE.B.5", "graph"): b_pgraph, ("8.EE.B.5", "slope"): b_pslope, ("8.EE.B.5", "compare"): b_pcompare,
    ("8.EE.C.8", "graph"): b_sgraph, ("8.EE.C.8", "algebra"): b_salg, ("8.EE.C.8", "world"): b_sworld,
    ("8.F.A.1", "decide"): b_fdecide, ("8.F.A.1", "rule"): b_frule,
    ("8.F.A.3", "identify"): b_fident, ("8.F.A.3", "examples"): b_fexamples,
    ("8.G.A.3", "translate"): b_translate, ("8.G.A.3", "reflect"): b_reflect, ("8.G.A.3", "rotate"): b_rotate, ("8.G.A.3", "dilate"): b_dilate,
    ("8.G.B.7", "math"): b_pmath, ("8.G.B.7", "real"): b_preal, ("8.G.B.7", "threed"): b_p3d,
    ("8.SP.A.1", "construct"): b_sconstruct, ("8.SP.A.1", "describe"): b_sdescribe, ("8.SP.A.1", "outlier"): b_soutlier,
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
    L = ["/* G8MATH-STRANDS-BEGIN (generated by source/tools/gen_g8math.py, edit the generator, not this block) */",
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append("var G8PIC=%s;" % json.dumps(data, ensure_ascii=False))
    L.append(P1.APPLY.replace("G1PIC", "G8PIC"))
    L.append("/* G8MATH-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G8, encoding="utf8").read()
    if "G8MATH-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G8MATH-STRANDS-BEGIN.*?G8MATH-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        s = src.rstrip()
        assert s.endswith("})();"), s[-40:]
        src = s[:-5] + block + "\n})();\n"
    open(G8, "w", encoding="utf8").write(src)
    print("parts:", sum(len(p) for std in data.values() for p in std.values()), "block bytes:", len(block))


if __name__ == "__main__":
    main()
