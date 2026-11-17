"""Builds the parts (strands) for the Grade 7 math standards, all 10 LPs, and writes them into source/gx/g7.js.

No Grade 7 gradebook "I can" lines exist in the project, so each standard is split by the sub-skills written inside
the CCSS wording (Loren chose this approach for Grade 6 onward).
Run:  python3 source/tools/gen_g7math.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N
import gen_g1pic as P1
import gen_g5math as G5

G7 = os.path.join(HERE, '..', 'gx', 'g7.js')
THEME, rng_for, nm, BAD = N.THEME, N.rng_for, N.nm, N.BAD
mixed, fstr = G5.mixed, G5.fstr
MINUS = "−"


def C(*p):
    return list(p)


def sg(n):
    if isinstance(n, F):
        s = mixed(abs(n)) if n.denominator != 1 else str(abs(n.numerator))
        return (MINUS + s) if n < 0 else s
    return (MINUS + str(-n)) if n < 0 else str(n)


def dec(x, nd=2):
    s = ("%." + str(nd) + "f") % x
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def money(x):
    x = float(x)
    return "$%d" % round(x) if abs(x - round(x)) < 1e-9 else "$%.2f" % x


def pick(pool, k, r):
    p = pool[:]
    r.shuffle(p)
    return p[:k]


CAT = {
    "7.RP.A.2": {"desc": "proportional relationships in tables, graphs, equations, and situations", "parts": C(
        ("decide", "Decide if a relationship is proportional", "Deciding whether two quantities are in a proportional relationship using tables and graphs"),
        ("constant", "Find the constant of proportionality", "Identifying the constant of proportionality (unit rate) in tables, graphs, equations, and verbal descriptions"),
        ("equation", "Write an equation y = kx", "Representing proportional relationships by equations"),
        ("points", "Explain a point on a proportional graph", "Explaining what a point (x, y) on the graph of a proportional relationship means, including (0, 0) and (1, r)"))},
    "7.RP.A.3": {"desc": "multistep ratio and percent problems", "parts": C(
        ("markup", "Tax, tips, markups, markdowns, and commissions", "Solving multistep percent problems involving sales tax, tips, markups, markdowns, and commissions"),
        ("interest", "Simple interest and fees", "Solving multistep percent problems involving simple interest and fees"),
        ("change", "Percent increase and decrease", "Solving multistep percent problems involving percent increase and percent decrease"),
        ("error", "Percent error", "Solving multistep percent problems involving percent error"))},
    "7.NS.A.3": {"desc": "real-world problems with the four operations on rational numbers", "parts": C(
        ("addsub", "Add and subtract rational numbers in problems", "Solving real-world problems involving addition and subtraction of rational numbers"),
        ("muldiv", "Multiply and divide rational numbers in problems", "Solving real-world problems involving multiplication and division of rational numbers"),
        ("complex", "Complex fractions and mixed operations", "Solving problems with complex fractions and with more than one operation on rational numbers"))},
    "7.EE.B.3": {"desc": "multistep problems with positive and negative rational numbers", "parts": C(
        ("solve", "Solve multistep problems", "Solving multistep real-life and mathematical problems with positive and negative rational numbers"),
        ("convert", "Convert between fractions, decimals, and percents", "Converting between forms of a rational number (fractions, decimals, and percents) to solve problems"),
        ("estimate", "Check answers with estimation", "Assessing the reasonableness of answers using mental computation and estimation strategies"))},
    "7.EE.B.4": {"desc": "equations and inequalities from word problems", "parts": C(
        ("pxq", "Solve px + q = r problems", "Solving word problems leading to equations of the form px + q = r"),
        ("paren", "Solve p(x + q) = r problems", "Solving word problems leading to equations of the form p(x + q) = r"),
        ("ineq", "Solve and graph inequalities", "Solving word problems leading to inequalities of the form px + q > r or px + q < r and interpreting the solution set"))},
    "7.G.A.2": {"desc": "drawing triangles from given conditions", "parts": C(
        ("exist", "Tell if a triangle can be made", "Deciding whether three given side lengths or angle measures make a triangle"),
        ("unique", "Tell if conditions make one, many, or no triangles", "Deciding whether given conditions determine a unique triangle, more than one triangle, or no triangle"))},
    "7.G.B.4": {"desc": "circle area and circumference", "parts": C(
        ("circ", "Circumference of a circle", "Using the formula for the circumference of a circle"),
        ("area", "Area of a circle", "Using the formula for the area of a circle"),
        ("relate", "How circumference and area are related", "Describing the relationship between the circumference and area of a circle"))},
    "7.G.B.6": {"desc": "area, volume, and surface area of two- and three-dimensional objects", "parts": C(
        ("area", "Area of figures made of triangles and rectangles", "Solving real-world and mathematical problems involving the area of two-dimensional objects composed of triangles, quadrilaterals, and polygons"),
        ("volume", "Volume of prisms", "Solving real-world and mathematical problems involving the volume of right prisms"),
        ("surface", "Surface area of prisms", "Solving real-world and mathematical problems involving the surface area of cubes and right prisms"))},
    "7.SP.B.4": {"desc": "comparing two populations with center and variability", "parts": C(
        ("center", "Compare two data sets by center", "Comparing two populations using measures of center"),
        ("variability", "Compare two data sets by variability", "Comparing two populations using measures of variability"),
        ("inference", "Draw informal comparative inferences", "Drawing informal comparative inferences about two populations"))},
    "7.SP.C.8": {"desc": "probability of compound events", "parts": C(
        ("fraction", "Find the probability of a compound event", "Finding the probability of a compound event as the fraction of outcomes in the sample space"),
        ("space", "List sample spaces", "Representing sample spaces for compound events using organized lists, tables, and tree diagrams"),
        ("simulate", "Design a simulation", "Designing and using a simulation to generate frequencies for compound events"))},
}

D1 = "Listen to each question. Show your work on your paper."


# ================================================================== RP.A.2
def tbl(xs, ys):
    return "x: %s. y: %s." % (", ".join(map(str, xs)), ", ".join(map(str, ys)))


def b_decide(lp, r):
    k = r.choice([3, 4, 5, 6])
    a = r.choice([2, 3, 4])
    c = r.choice([2, 3, 5])
    xs = [1, 2, 3, 4]
    t1 = [k * x for x in xs]
    t2 = [a * x + c for x in xs]
    qs = ["Is the relationship proportional? %s Tell how you know." % tbl(xs, t1),
          "Is the relationship proportional? %s Tell how you know." % tbl(xs, t2)]
    key = ["Yes. y ÷ x is %d for every pair, so the ratio is constant." % k,
           "No. y ÷ x is %s, so the ratio is not constant." % ", ".join(dec(F(y, x), 2) for x, y in zip(xs, t2))]
    kind = r.choice(["line0", "linenot0", "curve"])
    if kind == "line0":
        qs.append("A graph is a straight line that goes through the point (0, 0). Is the relationship proportional? Why?")
        key.append("Yes. A straight line through the origin shows a proportional relationship.")
    elif kind == "linenot0":
        qs.append("A graph is a straight line that crosses the y-axis at (0, 3). Is the relationship proportional? Why?")
        key.append("No. A proportional graph must go through (0, 0), and this line does not.")
    else:
        qs.append("A graph is a curve that goes through (0, 0). Is the relationship proportional? Why?")
        key.append("No. A proportional graph is a straight line through (0, 0), and this one is curved.")
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_constant(lp, r):
    k = r.choice([F(3), F(5), F(7, 2), F(9, 4), F(5, 2)])
    xs = [2, 4, 6, 8]
    ys = [k * x for x in xs]
    gx, kk = r.choice([4, 5, 8]), r.choice([F(5, 2), F(3), F(7, 2)])
    price, lb = r.choice([(6, 4), (9, 3), (7, 2), (15, 6)])
    n0 = nm(lp, 0)
    qs = ["Find the constant of proportionality. %s" % tbl(xs, [sg(y) for y in ys]),
          "The graph of a proportional relationship passes through the point (%d, %s). What is the constant of proportionality?" % (gx, sg(kk * gx)),
          "%s paid $%d for %d pounds of grapes. What is the constant of proportionality (the price per pound)?" % (n0, price, lb)]
    key = ["%s. y ÷ x = %s ÷ 2 = %s for every pair." % (sg(k), sg(ys[0]), sg(k)),
           "%s. %s ÷ %d = %s." % (sg(kk), sg(kk * gx), gx, sg(kk)),
           "$%.2f per pound. %d ÷ %d = %.2f." % (price / float(lb), price, lb, price / float(lb))]
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_equation(lp, r):
    k1 = r.choice([4, 6, 8, 12])
    k2 = r.choice([3, 5, 7])
    xs = [1, 2, 3, 4]
    k3 = r.choice([F(7, 2), F(5, 2), F(9, 2)])
    qs = ["Movie tickets cost $%d each. Let t be the number of tickets and c be the total cost. Write an equation that relates c and t." % k1,
          "Write an equation for y in terms of x. %s" % tbl(xs, [k2 * x for x in xs]),
          "A hiker walks %s miles in 1 hour at a steady pace. Let h be hours and d be distance in miles. Write an equation and find d when h = 4." % dec(k3, 2)]
    key = ["c = %dt." % k1, "y = %dx." % k2, "d = %sh. When h = 4, d = %s miles." % (dec(k3, 2), dec(k3 * 4, 2))]
    return dict(qs=qs, key=key, dir=D1, dur=160)


def b_points(lp, r):
    rr = r.choice([3, 4, 5, 6, 8])
    n = r.choice([3, 5, 6, 10])
    items = [("a store sells apples for $%d per pound" % rr, "(1, %d): 1 pound of apples costs $%d. This is the unit rate." % (rr, rr)),
             ("a store sells apples for $%d per pound" % rr, "(0, 0): 0 pounds of apples cost $0."),
             ("a store sells apples for $%d per pound" % rr, "(%d, %d): %d pounds of apples cost $%d." % (n, n * rr, n, n * rr))]
    q1 = "The graph of cost (y) and pounds (x) for apples is a line through the origin, and %s. What does the point (1, %d) mean in this situation?" % (items[0][0], rr)
    q2 = "On the same graph, what does the point (0, 0) mean?"
    q3 = "On the same graph, what does the point (%d, %d) mean?" % (n, n * rr)
    return dict(qs=[q1, q2, q3], key=[items[0][1], items[1][1], items[2][1]], dir=D1, dur=150)


# ================================================================== RP.A.3
def b_markup(lp, r):
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    p1, t1 = r.choice([(40, 8), (60, 5), (80, 7), (50, 6)])
    p2, g2 = r.choice([(40, 15), (60, 20), (80, 15), (50, 18)])
    p3, m3 = r.choice([(40, 25), (60, 50), (80, 25), (30, 40)])
    p4, d4 = r.choice([(60, 25), (80, 30), (40, 20), (120, 15)])
    sold, com = r.choice([(500, 6), (800, 5), (1200, 4)])
    pool = [("A jacket costs $%d. The sales tax is %d%%. What is the total cost?" % (p1, t1), "%s. Tax: %d%% of %d = %s. Total: %d + %s = %s." % (money(p1 * (1 + F(t1, 100))), t1, p1, money(p1 * F(t1, 100)), p1, money(p1 * F(t1, 100)), money(p1 * (1 + F(t1, 100))))),
            ("%s's meal costs $%d. %s leaves a %d%% tip. How much is the tip, and what is the total?" % (n0, p2, n0, g2), "Tip %s, total %s. Tip: %d%% of %d = %s. Total: %d + %s = %s." % (money(p2 * F(g2, 100)), money(p2 * (1 + F(g2, 100))), g2, p2, money(p2 * F(g2, 100)), p2, money(p2 * F(g2, 100)), money(p2 * (1 + F(g2, 100))))),
            ("A store buys a backpack for $%d and marks it up %d%%. What is the selling price?" % (p3, m3), "%s. Markup: %d%% of %d = %s. Selling price: %d + %s = %s." % (money(p3 * (1 + F(m3, 100))), m3, p3, money(p3 * F(m3, 100)), p3, money(p3 * F(m3, 100)), money(p3 * (1 + F(m3, 100))))),
            ("A pair of shoes costs $%d. It is on sale for %d%% off. What is the sale price?" % (p4, d4), "%s. Discount: %d%% of %d = %s. Sale price: %d − %s = %s." % (money(p4 * (1 - F(d4, 100))), d4, p4, money(p4 * F(d4, 100)), p4, money(p4 * F(d4, 100)), money(p4 * (1 - F(d4, 100))))),
            ("%s earns a %d%% commission on sales. %s sells $%d of goods. How much commission does %s earn?" % (n1, com, n1, sold, n1), "%s. %d%% of %d = %s." % (money(sold * F(com, 100)), com, sold, money(sold * F(com, 100))))]
    it = pick(pool, 3, r)
    return dict(qs=[q for q, _ in it], key=[k for _, k in it], dir=D1, dur=190)


def b_interest(lp, r):
    n0, n1 = nm(lp, 0), nm(lp, 1)
    P1_, r1, t1 = r.choice([(500, 4, 3), (800, 5, 2), (1000, 3, 4), (600, 5, 3)])
    P2, r2, t2 = r.choice([(2000, 3, 5), (1500, 4, 2), (900, 5, 4)])
    fee_p, fee_r, fee_t = r.choice([(240, 5, 1), (400, 3, 1), (600, 2, 1), (800, 4, 1)])
    qs = ["%s puts $%d in a savings account that earns %d%% simple interest each year. How much interest does %s earn in %d years? What is the total in the account?" % (n0, P1_, r1, n0, t1),
          "%s borrows $%d at %d%% simple interest per year. How much interest does %s owe after %d years? How much must %s pay back in all?" % (n1, P2, r2, n1, t2, n1),
          "A store charges a %d%% fee on a $%d layaway purchase. How much is the fee? What is the total cost with the fee?" % (fee_r, fee_p)]
    i1, i2, i3 = P1_ * r1 * t1 // 100, P2 * r2 * t2 // 100, fee_p * fee_r * fee_t // 100
    key = ["Interest $%d. I = P × r × t = %d × %s × %d = %d. Total $%d." % (i1, P1_, dec(F(r1, 100), 2), t1, i1, P1_ + i1),
           "Interest $%d. I = %d × %s × %d = %d. Pay back $%d." % (i2, P2, dec(F(r2, 100), 2), t2, i2, P2 + i2),
           "Fee $%s. %d%% of %d = %s. Total $%s." % (dec(F(fee_p * fee_r, 100), 2), fee_r, fee_p, dec(F(fee_p * fee_r, 100), 2), dec(fee_p + F(fee_p * fee_r, 100), 2))]
    return dict(qs=qs, key=key, dir=D1, dur=190)


def b_change(lp, r):
    its = pick([(40, 50), (80, 60), (20, 35), (50, 40), (60, 75), (200, 150), (25, 30), (90, 72)], 3, r)
    qs, key = [], []
    ctx = ["The price of a game went from $%d to $%d. What is the percent change? Is it an increase or a decrease?", "A town's population went from %d to %d people. What is the percent change? Is it an increase or a decrease?",
           "The number of students in a club went from %d to %d. What is the percent change? Is it an increase or a decrease?"]
    for (a, b), c in zip(its, ctx):
        qs.append(c % (a, b))
        ch = F(abs(b - a) * 100, a)
        key.append("%s%% %s. Change %d, and %d ÷ %d = %s." % (dec(ch, 2), "increase" if b > a else "decrease", abs(b - a), abs(b - a), a, dec(F(abs(b - a), a), 3)))
    return dict(qs=qs, key=key, dir=D1, dur=180)


def b_error(lp, r):
    its = pick([(50, 48), (200, 190), (40, 42), (25, 20), (80, 76), (125, 120)], 3, r)
    ctx = ["A student measured a desk as %d cm long. The real length is %d cm. What is the percent error?", "A scale shows %d pounds for a package that really weighs %d pounds. What is the percent error?", "%d minutes was the estimate for a trip that actually took %d minutes. What is the percent error?"]
    qs, key = [], []
    for (act, meas), c in zip(its, ctx):
        qs.append(c % (meas, act))
        e = F(abs(meas - act) * 100, act)
        key.append("%s%%. Error is %d, and %d ÷ %d × 100 = %s." % (dec(e, 2), abs(meas - act), abs(meas - act), act, dec(e, 2)))
    return dict(qs=qs, key=key, dir="Listen to each question. Percent error compares the error to the actual value. Show your work.", dur=170)


# ================================================================== NS.A.3
def b_addsub(lp, r):
    a = F(-r.randint(2, 9)) - F(1, 2)
    b = F(r.randint(5, 12)) + F(1, 4)
    c1, c2, c3 = F(r.randint(2000, 6000), 100), F(r.randint(1000, 5000), 100), F(r.randint(500, 2500), 100)
    h, d = F(r.randint(100, 400)) + F(1, 2), F(r.randint(20, 90)) + F(3, 4)
    qs = ["The temperature is %s°F and then rises %s°F. What is the new temperature?" % (sg(a), mixed(b)),
          "An account has $%s. A withdrawal of $%s is made and then a deposit of $%s. What is the new balance?" % (dec(c1, 2), dec(c2, 2), dec(c3, 2)),
          "A hill is %s feet above sea level. A cave is %s feet below sea level. How far apart are the top of the hill and the bottom of the cave?" % (mixed(h), mixed(d))]
    key = ["%s°F. %s + %s = %s." % (sg(a + b), sg(a), mixed(b), sg(a + b)),
           "$%s. %s − %s + %s = %s." % (dec(c1 - c2 + c3, 2), dec(c1, 2), dec(c2, 2), dec(c3, 2), dec(c1 - c2 + c3, 2)),
           "%s feet. Add the distances from sea level: %s + %s = %s." % (mixed(h + d), mixed(h), mixed(d), mixed(h + d))]
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_muldiv(lp, r):
    yrs = r.randint(3, 6)
    per = F(r.randint(3, 9)) + F(1, 2)
    wk = r.randint(4, 8)
    loss = r.randint(1500, 3500) / 100.0
    share = r.randint(3, 6)
    each = r.randint(500, 1500) / 100.0
    debt = each * share
    qs = ["A glacier gets shorter by %s feet each year. What is the total change in length after %d years? Write it with a sign." % (mixed(per), yrs),
          "An account loses $%.2f each week for %d weeks. What is the total change in the balance?" % (loss, wk),
          "%d friends share a debt of $%.2f equally. What is each person's share of the debt, written as a signed number?" % (share, debt)]
    key = ["%s feet. %d × (%s) = %s." % (sg(-per * yrs), yrs, sg(-per), sg(-per * yrs)),
           "\u2212$%.2f. %d × (\u2212%.2f) = \u2212%.2f." % (loss * wk, wk, loss, loss * wk),
           "\u2212$%.2f each. \u2212%.2f ÷ %d = \u2212%.2f." % (each, debt, share, each)]
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_complex(lp, r):
    a, b = r.choice([(F(3, 4), F(1, 2)), (F(5, 6), F(2, 3)), (F(3, 8), F(3, 4))])
    c, d, e = F(-r.randint(2, 5), r.choice([2, 3])), F(r.randint(1, 3), 4), r.randint(2, 4)
    f1, f2 = F(r.randint(1, 3), 2), F(r.randint(2, 7), 3)
    expr3 = -f1 * f2 + F(1, 2)
    qs = ["Simplify the complex fraction (%s) ÷ (%s)." % (fstr(a), fstr(b)),
          "Evaluate %s ÷ %d + %s." % (sg(c), e, fstr(d)),
          "Evaluate %s × %s + 1/2." % (sg(-f1), sg(f2))]
    key = ["%s. %s × %s = %s." % (mixed(a / b), fstr(a), fstr(F(b.denominator, b.numerator)), mixed(a / b)),
           "%s. First %s ÷ %d = %s, then %s + %s = %s." % (sg(c / e + d), sg(c), e, sg(c / e), sg(c / e), fstr(d), sg(c / e + d)),
           "%s. First %s × %s = %s, then add 1/2: %s." % (sg(-f1 * f2 * -1 * -1 + F(1, 2)) if False else sg(f1 * f2 * -1 * -1 * -1 + F(1, 2)) if False else sg((-f1) * f2 + F(1, 2)), sg(-f1), sg(f2), sg((-f1) * f2), sg((-f1) * f2 + F(1, 2)))]
    return dict(qs=qs, key=key, dir=D1, dur=190)


# ================================================================== EE.B.3
def b_ee3_solve(lp, r):
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    w, hr = r.choice([F(37, 2), F(75, 4), F(65, 4)]), r.choice([32, 36, 40])
    p = r.choice([F(1, 4), F(1, 5)])
    a, b, c = r.choice([(F(5, 2), F(3, 2), F(3, 4)), (F(7, 2), F(3, 2), F(1, 2))])
    t0, d0, rise = r.choice([(-6, 4, F(5, 2)), (-8, 5, F(3, 2)), (-10, 6, F(3, 4))])
    qs = ["%s earns $%s per hour and works %d hours. %s spends %s of the pay on rent. How much is left after rent?" % (n0, dec(w, 2), hr, n0, fstr(p)),
          "A recipe needs %s cups of flour. %s makes %s times the recipe, and then uses %s of that flour for the crust. How many cups are used for the crust?" % (mixed(a), n1, mixed(b), fstr(c)),
          "The temperature at 6 a.m. is %s°F. It rises %s°F each hour for %d hours. What is the temperature then?" % (sg(t0), mixed(rise), d0)]
    key = ["$%s. Pay: %s × %d = %s. Rent: %s × %s = %s. Left: %s − %s = %s." % (dec(w * hr * (1 - p), 2), dec(w, 2), hr, dec(w * hr, 2), fstr(p), dec(w * hr, 2), dec(w * hr * p, 2), dec(w * hr, 2), dec(w * hr * p, 2), dec(w * hr * (1 - p), 2)),
           "%s cups. %s × %s = %s cups total, then %s × %s = %s." % (mixed(a * b * c), mixed(a), mixed(b), mixed(a * b), mixed(a * b), fstr(c), mixed(a * b * c)),
           "%s°F. %s × %d = %s, then %s + %s = %s." % (sg(t0 + rise * d0), mixed(rise), d0, mixed(rise * d0), sg(t0), mixed(rise * d0), sg(t0 + rise * d0))]
    return dict(qs=qs, key=key, dir=D1, dur=200)


def b_ee3_convert(lp, r):
    f1 = r.choice([F(3, 8), F(5, 8), F(7, 8), F(1, 8)])
    f2 = r.choice([F(3, 20), F(7, 20), F(9, 20), F(11, 20)])
    d3 = r.choice([F(125, 100), F(175, 100), F(225, 100)])
    d4 = r.choice([F(3, 5), F(2, 5), F(4, 5)])
    qs = ["Write %s as a decimal and as a percent." % fstr(f1),
          "Write %s as a decimal and as a fraction in simplest form." % (dec(f2 * 100) + "%"),
          "Write %s as a mixed number and as a percent. Then use the decimal to find 1.5 × %s." % (dec(d3, 3), dec(d3, 3)),
          ]
    key = ["%s and %s%%." % (dec(f1, 3), dec(f1 * 100, 1)),
           "%s and %s. %s%% means %s out of 100." % (dec(f2, 2), fstr(f2), dec(f2 * 100), dec(f2 * 100)),
           "%s and %s%%. 1.5 × %s = %s." % (mixed(d3), dec(d3 * 100), dec(d3, 3), dec(d3 * F(3, 2), 4))]
    qs = qs[:3]
    return dict(qs=qs, key=key, dir=D1, dur=160)


def rnd10(x):
    return int((x + 5) // 10 * 10)


def b_estimate(lp, r):
    p = r.randint(31, 89)
    base = rnd10(p)
    a, b = r.randint(2, 6), r.randint(2, 7)
    fa, fb = F(r.randint(1, 7), 8), F(r.randint(3, 9), 10)
    claim = r.choice([F(2, 10), F(15, 100)])
    q = r.randint(60, 90)
    qs = ["Estimate a 15%% tip on a $%d bill using mental math. Then tell if $%s is a reasonable tip." % (p, dec(F(p * 15, 100) * 2, 2)),
          "Estimate %d %s × %d %s by rounding each number to the nearest whole number." % (a, fstr(fa), b, fstr(fb)),
          "A student says 20%% of %d is %d. Is that reasonable? Use an estimate to decide." % (q, q * 2)]
    est1 = F(base) * F(15, 100)
    key = ["About $%s: round $%d to $%d, 10%% is $%s, and half of that is $%s, so 15%% is about $%s. A tip of $%s is not reasonable, since it is about double." % (dec(est1, 2), p, base, dec(base / 10), dec(base / 20), dec(est1, 2), dec(F(p * 15, 100) * 2, 2)),
           "About %d. %d %s rounds to %d and %d %s rounds to %d, so %d × %d = %d." % (a * b if False else (a + (1 if fa > F(1, 2) else 0)) * (b + (1 if fb > F(1, 2) else 0)), a, fstr(fa), a + (1 if fa > F(1, 2) else 0), b, fstr(fb), b + (1 if fb > F(1, 2) else 0), a + (1 if fa > F(1, 2) else 0), b + (1 if fb > F(1, 2) else 0), (a + (1 if fa > F(1, 2) else 0)) * (b + (1 if fb > F(1, 2) else 0))),
           "Not reasonable. 20%% is 1/5, so 20%% of %d is about %d ÷ 5 = %s. %d is too big because it is more than the whole amount." % (q, q, dec(F(q, 5), 1), q * 2)]
    return dict(qs=qs, key=key, dir="Listen to each question. Estimate with friendly numbers. Say how you got it.", dur=180)


# ================================================================== EE.B.4
def b_pxq(lp, r):
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    p, q, x = r.randint(3, 9), r.randint(10, 40), r.randint(3, 12)
    p2, q2, x2 = r.randint(2, 6), r.randint(5, 25), r.randint(4, 10)
    p3, q3, x3 = r.randint(4, 12), r.randint(8, 30), r.randint(3, 9)
    qs = ["A gym charges $%d to join and $%d per month. %s paid $%d in all. Write an equation and find the number of months." % (q, p, n0, p * x + q),
          "%s has $%d. A pack of cards costs $%d. After buying some packs, %s has $%d left. Write an equation px + q = r and find the number of packs." % (n1, q2 + p2 * x2 + 0, p2, n1, q2),
          "A phone plan costs $%d a month plus $%d for each extra gigabyte. The bill was $%d. Write an equation and find the extra gigabytes." % (q3, p3, p3 * x3 + q3)]
    key = ["%dx + %d = %d. x = %d months (%d − %d = %d, %d ÷ %d = %d)." % (p, q, p * x + q, x, p * x + q, q, p * x, p * x, p, x),
           "%dx + %d = %d. x = %d packs (%d − %d = %d, %d ÷ %d = %d)." % (p2, q2, q2 + p2 * x2, x2, q2 + p2 * x2, q2, p2 * x2, p2 * x2, p2, x2),
           "%dx + %d = %d. x = %d gigabytes (%d − %d = %d, %d ÷ %d = %d)." % (p3, q3, p3 * x3 + q3, x3, p3 * x3 + q3, q3, p3 * x3, p3 * x3, p3, x3)]
    qs[1] = "%s has $%d. A pack of cards costs $%d. After buying some packs, %s has $%d left. Write an equation of the form q − px = r, then solve it." % (n1, q2 + p2 * x2, p2, n1, q2)
    key[1] = "%d − %dx = %d. x = %d packs (%d − %d = %d, %d ÷ %d = %d)." % (q2 + p2 * x2, p2, q2, x2, q2 + p2 * x2, q2, p2 * x2, p2 * x2, p2, x2)
    return dict(qs=qs, key=key, dir=D1, dur=200)


def b_paren(lp, r):
    p, q, x = r.randint(3, 6), r.randint(2, 6), r.randint(4, 15)
    p2, q2, x2 = r.randint(2, 5), r.randint(3, 8), r.randint(5, 12)
    p3, q3, x3 = r.randint(2, 5), r.randint(1, 5), r.randint(3, 10)
    qs = ["%d friends each buy a shirt that costs $x plus $%d for printing. They spend $%d in all. Write p(x + q) = r and find x." % (p, q, p * (x + q)),
          "A rectangle's length is x + %d and its width is %d. Its area is %d. Write an equation of the form p(x + q) = r and find x." % (q2, p2, p2 * (x2 + q2)),
          "A club orders %d boxes. Each box has x pencils and %d extra pencils are added to each box. There are %d pencils in all. Write an equation and find x." % (p3, q3, p3 * (x3 + q3))]
    key = ["%d(x + %d) = %d. x + %d = %d, so x = %d dollars." % (p, q, p * (x + q), q, x + q, x),
           "%d(x + %d) = %d. x + %d = %d, so x = %d." % (p2, q2, p2 * (x2 + q2), q2, x2 + q2, x2),
           "%d(x + %d) = %d. x + %d = %d, so x = %d pencils." % (p3, q3, p3 * (x3 + q3), q3, x3 + q3, x3)]
    return dict(qs=qs, key=key, dir=D1, dur=200)


def b_ineq(lp, r):
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    p, q, k = r.randint(3, 8), r.randint(10, 40), r.randint(5, 14)
    p2, q2, k2 = r.randint(4, 9), r.randint(20, 60), r.randint(3, 10)
    p3, q3, k3 = r.randint(2, 6), r.randint(10, 50), r.randint(4, 12)
    qs = ["%s has $%d and saves $%d each week. %s wants more than $%d. Write and solve an inequality px + q > r. Graph the answer on a number line (say where the circle and arrow go)." % (n0, q, p, n0, q + p * k),
          "A taxi costs $%d to start and $%d per mile. %s has at most $%d to spend. Write and solve an inequality. What does the answer mean?" % (q2 // 2, p2, n1, q2 // 2 + p2 * k2),
          "%s wants the total to stay under %d points. %s starts with %d points and earns %d points per level. Write and solve an inequality for the number of levels." % (n2, q3 + p3 * k3, n2, q3, p3)]
    key = ["%dx + %d > %d. x > %d. Open circle at %d with an arrow to the right. %s needs more than %d weeks, so at least %d weeks." % (p, q, q + p * k, k, k, n0, k, k + 1),
           "%dx + %d ≤ %d. x ≤ %d. %s can ride at most %d miles." % (p2, q2 // 2, q2 // 2 + p2 * k2, k2, n1, k2),
           "%dx + %d < %d. x < %d, so %s can play at most %d whole levels." % (p3, q3, q3 + p3 * k3, k3, n2, k3 - 1)]
    return dict(qs=qs, key=key, dir=D1, dur=220)


# ================================================================== G.A.2
def b_exist(lp, r):
    a, b = r.randint(3, 6), r.randint(4, 7)
    yes = (a + b) - r.randint(1, 2)
    no = a + b + r.randint(1, 4)
    ang = r.choice([(50, 60, 80), (40, 70, 80), (90, 45, 50), (100, 40, 50)])
    sides_yes = r.random() < 0.5
    s3 = yes if sides_yes else no
    qs = ["Can a triangle have side lengths %d, %d, and %d? Tell how you know." % (a, b, s3),
          "Can a triangle have angles of %d°, %d°, and %d°? Tell how you know." % ang,
          "Can a triangle have angles of %d°, %d°, and %d°? Tell how you know." % (60, 60, 60)]
    key = ["%s. %d + %d = %d, which is %s %d, so %s." % ("Yes" if sides_yes else "No", a, b, a + b, "greater than" if sides_yes else "less than or equal to", s3, "the two short sides reach past the long side" if sides_yes else "the two short sides cannot meet"),
           "%s. %d + %d + %d = %d, and a triangle's angles must add to 180." % ("Yes" if sum(ang) == 180 else "No", ang[0], ang[1], ang[2], sum(ang)),
           "Yes. 60 + 60 + 60 = 180, so it makes a triangle (an equilateral triangle)."]
    return dict(qs=qs, key=key, dir=D1, dur=160)


def b_unique(lp, r):
    pool = [("Three side lengths: 4, 5, and 6.", "Exactly one triangle. Three side lengths fit together only one way."),
            ("Two sides of 3 and 3 with a 40° angle between them.", "Exactly one triangle. Two sides and the angle between them fix the shape."),
            ("Three angles: 30°, 60°, and 90°.", "More than one triangle. The angles fix the shape, but the sides can be any size."),
            ("Three side lengths: 2, 3, and 8.", "No triangle. 2 + 3 is not greater than 8."),
            ("Angles of 70° and 50° with the side between them 6 inches long.", "Exactly one triangle. Two angles and the side between them fix the triangle."),
            ("Only one side that is 5 inches long and one angle of 60°.", "More than one triangle. That is not enough information to fix a single triangle."),
            ("Three angles of 80°, 70°, and 50°.", "More than one triangle. Angles alone give the same shape in many sizes."),
            ("Angles of 100°, 90°, and 20°.", "No triangle. The angles add to 210°, not 180°.")]
    it = pick(pool, 3, r)
    qs = ["Do these conditions make one triangle, more than one triangle, or no triangle? %s" % t for t, _ in it]
    return dict(qs=qs, key=[k for _, k in it], dir=D1, dur=170)


# ================================================================== G.B.4
def b_circ(lp, r):
    rad = r.choice([3, 5, 7, 10])
    d = r.choice([4, 6, 8, 12])
    dd = r.choice([10, 20, 30])
    n0 = nm(lp, 0)
    qs = ["A circle has a radius of %d cm. Find the circumference. Use 3.14 for π." % rad,
          "A circle has a diameter of %d inches. Find the circumference in terms of π, and then with 3.14 for π." % d,
          "A circular track has a circumference of %s feet. Use 3.14 for π and find its diameter." % dec(F(314, 100) * dd, 2)]
    key = ["%s cm. C = 2πr = 2 × 3.14 × %d = %s." % (dec(F(314, 100) * 2 * rad, 2), rad, dec(F(314, 100) * 2 * rad, 2)),
           "%dπ inches, which is about %s inches. C = πd." % (d, dec(F(314, 100) * d, 2)),
           "%d feet. C = πd, so d = %s ÷ 3.14 = %d." % (dd, dec(F(314, 100) * dd, 2), dd)]
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_carea(lp, r):
    rad = r.choice([2, 3, 4, 5, 10])
    d = r.choice([6, 8, 12, 20])
    rr = r.choice([4, 5, 6])
    n0 = nm(lp, 0)
    qs = ["A circle has a radius of %d cm. Find its area. Use 3.14 for π." % rad,
          "A circle has a diameter of %d inches. Find its area. Use 3.14 for π." % d,
          "%s has a round rug with a radius of %d feet. How many square feet of floor does the rug cover? Use 3.14 for π." % (n0, rr)]
    key = ["%s square cm. A = πr² = 3.14 × %d² = 3.14 × %d = %s." % (dec(F(314, 100) * rad * rad, 2), rad, rad * rad, dec(F(314, 100) * rad * rad, 2)),
           "%s square inches. The radius is %d, so A = 3.14 × %d² = %s." % (dec(F(314, 100) * (d // 2) ** 2, 2), d // 2, d // 2, dec(F(314, 100) * (d // 2) ** 2, 2)),
           "%s square feet. A = 3.14 × %d² = %s." % (dec(F(314, 100) * rr * rr, 2), rr, dec(F(314, 100) * rr * rr, 2))]
    return dict(qs=qs, key=key, dir=D1, dur=170)


def b_crelate(lp, r):
    rad = r.choice([2, 3, 4, 5])
    rr = r.choice([2, 3, 4])
    qs = ["A circle has a circumference of 22 cm and a diameter of 7 cm. What is C ÷ d? Will C ÷ d be about the same for every circle?",
          "A circle has a radius of %d. A second circle has a radius of %d. How do their circumferences compare? How do their areas compare?" % (rad, 2 * rad),
          "A circle has an area of %s square cm. Use A = πr² with π = 3.14 to find the radius." % dec(F(314, 100) * rr * rr, 2)]
    key = ["About 3.14. C ÷ d = 22 ÷ 7 ≈ 3.14. Yes, C ÷ d is π for every circle.",
           "The circumference is 2 times as large (it grows with the radius). The area is 4 times as large (it grows with the radius squared).",
           "%d cm. r² = %s ÷ 3.14 = %d, so r = %d." % (rr, dec(F(314, 100) * rr * rr, 2), rr * rr, rr)]
    return dict(qs=qs, key=key, dir=D1, dur=180)


# ================================================================== G.B.6
def b_area2(lp, r):
    w, h, th = r.choice([(10, 6, 4), (8, 5, 6), (12, 4, 6)])
    W, H, nw, nh = r.choice([(12, 9, 5, 4), (10, 8, 4, 3), (14, 10, 6, 4)])
    pw, ph, d = r.choice([(12, 8, 3), (10, 7, 2), (14, 9, 4)])
    qs = ["A shape is made of a rectangle that is %d units wide and %d units tall, with a triangle on top that has a base of %d units and a height of %d units. Find the total area." % (w, h, w, th),
          "A floor is an L shape. It is %d feet wide and %d feet long, with a %d foot by %d foot corner cut out. Find the area of the floor." % (W, H, nw, nh),
          "A wall is %d feet wide and %d feet tall. A square window that is %d feet on each side is cut out of it. How many square feet of wall are left?" % (pw, ph, d)]
    key = ["%s square units. Rectangle %d × %d = %d, triangle ½ × %d × %d = %s, total %s." % (mixed(F(w * h) + F(w * th, 2)), w, h, w * h, w, th, mixed(F(w * th, 2)), mixed(F(w * h) + F(w * th, 2))),
           "%d square feet. %d × %d = %d, minus %d × %d = %d, so %d − %d = %d." % (W * H - nw * nh, W, H, W * H, nw, nh, nw * nh, W * H, nw * nh, W * H - nw * nh),
           "%d square feet. Wall %d × %d = %d, window %d × %d = %d, so %d − %d = %d." % (pw * ph - d * d, pw, ph, pw * ph, d, d, d * d, pw * ph, d * d, pw * ph - d * d)]
    return dict(qs=qs, key=key, dir=D1, dur=190)


def b_vol(lp, r):
    l, w, h = r.randint(4, 12), r.randint(3, 8), r.randint(2, 6)
    b, th, ln = r.choice([(6, 4, 10), (8, 3, 9), (10, 6, 5)])
    s = r.randint(3, 7)
    qs = ["A right rectangular prism is %d cm long, %d cm wide, and %d cm tall. Find its volume." % (l, w, h),
          "A triangular prism has a triangle base with a base of %d cm and a height of %d cm. The prism is %d cm long. Find its volume." % (b, th, ln),
          "A cube-shaped box has edges of %d inches. How many cubic inches of space are inside?" % s]
    key = ["%d cubic cm. V = l × w × h = %d × %d × %d = %d." % (l * w * h, l, w, h, l * w * h),
           "%s cubic cm. Base area = ½ × %d × %d = %s. V = B × h = %s × %d = %s." % (mixed(F(b * th * ln, 2)), b, th, mixed(F(b * th, 2)), mixed(F(b * th, 2)), ln, mixed(F(b * th * ln, 2))),
           "%d cubic inches. V = s³ = %d³ = %d." % (s ** 3, s, s ** 3)]
    return dict(qs=qs, key=key, dir=D1, dur=190)


def b_surf(lp, r):
    l, w, h = r.randint(4, 10), r.randint(3, 7), r.randint(2, 6)
    s = r.randint(3, 8)
    ln = r.choice([6, 8, 10, 12])
    qs = ["Find the surface area of a rectangular prism that is %d cm long, %d cm wide, and %d cm tall." % (l, w, h),
          "Find the surface area of a cube with edges of %d inches." % s,
          "A triangular prism has a right triangle base with sides of 3 cm, 4 cm, and 5 cm. The prism is %d cm long. Find its surface area." % ln]
    key = ["%d square cm. 2(%d × %d) + 2(%d × %d) + 2(%d × %d) = %d + %d + %d = %d." % (2 * (l * w + l * h + w * h), l, w, l, h, w, h, 2 * l * w, 2 * l * h, 2 * w * h, 2 * (l * w + l * h + w * h)),
           "%d square inches. 6 × %d² = 6 × %d = %d." % (6 * s * s, s, s * s, 6 * s * s),
           "%d square cm. Two triangles: 2 × (½ × 3 × 4) = 12. Three rectangles: (3 + 4 + 5) × %d = %d. Total %d + %d = %d." % (12 + 12 * ln, ln, 12 * ln, 12, 12 * ln, 12 + 12 * ln)]
    return dict(qs=qs, key=key, dir=D1, dur=200)


# ================================================================== SP.B.4
def mean_set(r, n, m, spread):
    while True:
        s = [m + r.randint(-spread, spread) for _ in range(n)]
        if sum(s) == n * m:
            return s
        s[-1] += n * m - sum(s)
        if all(m - spread - 2 <= x <= m + spread + 2 for x in s):
            return s


def median(s):
    s = sorted(s)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def b_scenter(lp, r):
    ma, mb = r.randint(60, 80), r.randint(60, 80)
    while mb == ma:
        mb = r.randint(60, 80)
    A, B = mean_set(r, 8, ma, 6), mean_set(r, 8, mb, 6)
    qs = ["Team A scored these points: %s. Team B scored: %s. Find the mean of each team. Which team has the greater mean and by how much?" % (", ".join(map(str, A)), ", ".join(map(str, B))),
          "Find the median of each data set. Team A: %s. Team B: %s. Which median is greater?" % (", ".join(map(str, A)), ", ".join(map(str, B))),
          "The mean height of a group of 12-year-olds is %d inches and of 8-year-olds is %d inches. What does this tell you about the two groups?" % (ma - 3, ma - 3 - 8)]
    ga = "A" if ma > mb else "B"
    mdA, mdB = median(A), median(B)
    key = ["Mean A = %d and mean B = %d. Team %s is greater by %d." % (ma, mb, ga, abs(ma - mb)),
           "Median A = %s and median B = %s. %s." % (mixed(mdA), mixed(mdB), "Team A's median is greater" if mdA > mdB else "Team B's median is greater" if mdB > mdA else "They are equal")]
    key.append("The 12-year-olds are taller on average, by %d inches." % 8)
    return dict(qs=qs, key=key, dir=D1, dur=200)


def mad_of(s):
    m = F(sum(s), len(s))
    return sum(abs(F(x) - m) for x in s) / len(s)


def b_svar(lp, r):
    A = mean_set(r, 5, r.randint(20, 30), 3)
    B = mean_set(r, 5, r.randint(20, 30), 8)
    mA, mB = F(sum(A), 5), F(sum(B), 5)
    madA, madB = mad_of(A), mad_of(B)
    ca = r.choice([(60, 66, 3), (40, 46, 2), (50, 58, 4)])
    qs = ["Find the mean absolute deviation (MAD) of each data set. Set A: %s. Set B: %s." % (", ".join(map(str, A)), ", ".join(map(str, B))),
          "Which data set in the last question is more spread out? How do you know?",
          "Group 1 has a mean of %d and group 2 has a mean of %d. Both have a MAD of %d. The difference in the means is how many times the MAD?" % (ca[0], ca[1], ca[2])]
    key = ["Set A: mean %s, MAD %s. Set B: mean %s, MAD %s." % (mixed(mA), mixed(madA), mixed(mB), mixed(madB)),
           "%s is more spread out because its MAD (%s) is greater than the other MAD (%s)." % ("Set A" if madA > madB else "Set B" if madB > madA else "Neither (the MADs are equal)", mixed(max(madA, madB)), mixed(min(madA, madB))),
           "%s times. The difference is %d − %d = %d, and %d ÷ %d = %s." % (mixed(F(ca[1] - ca[0], ca[2])), ca[1], ca[0], ca[1] - ca[0], ca[1] - ca[0], ca[2], mixed(F(ca[1] - ca[0], ca[2])))]
    return dict(qs=qs, key=key, dir=D1, dur=220)


def b_sinfer(lp, r):
    def sc(k, m, mad, who, what):
        return "%s: group 1 has a mean of %d and group 2 has a mean of %d. Both have a MAD of %d. What can you say about the two %s?" % (who, m, m + k * mad, mad, what)
    k1, k2, k3 = 1, 2, 3
    m1, m2, m3 = r.randint(50, 70), r.randint(30, 50), r.randint(20, 40)
    d1, d2, d3 = r.randint(3, 5), r.randint(2, 4), r.randint(2, 5)
    qs = [sc(k1, m1, d1, "Test scores", "classes"), sc(k2, m2, d2, "Minutes spent reading", "grades"), sc(k3, m3, d3, "Heights in inches", "teams")]
    desc = {1: "The difference in the means is 1 MAD, so the two groups overlap a lot, and there is only weak evidence one group is higher.",
            2: "The difference in the means is 2 MADs, so the groups overlap a little, and group 2 is clearly higher on average.",
            3: "The difference in the means is 3 MADs, so the groups hardly overlap, and group 2 is much higher."}
    key = [desc[1], desc[2], desc[3]]
    return dict(qs=qs, key=key, dir="Listen to each question. Compare the difference in the means to the MAD. Say what you can infer.", dur=200)


# ================================================================== SP.C.8
def outcomes(kind):
    if kind == "two dice":
        return [(a, b) for a in range(1, 7) for b in range(1, 7)]
    if kind == "three coins":
        return list(itertools.product("HT", repeat=3))
    if kind == "two spinners":
        return [(a, b) for a in range(1, 5) for b in range(1, 5)]
    if kind == "coin and die":
        return [(c, d) for c in "HT" for d in range(1, 7)]


def b_pfrac(lp, r):
    s = r.choice([6, 7, 8, 9])
    k = r.choice([1, 2])
    ev3 = r.choice([5, 6, 7])
    o1 = outcomes("two dice")
    o2 = outcomes("three coins")
    o3 = outcomes("two spinners")
    c1 = sum(1 for a, b in o1 if a + b == s)
    c2 = sum(1 for o in o2 if o.count("H") == k + 1)
    c3 = sum(1 for a, b in o3 if a + b == ev3)
    qs = ["Two fair number cubes (1 to 6) are rolled. What is the probability that the sum is %d?" % s,
          "A fair coin is flipped 3 times. What is the probability of getting exactly %d heads?" % (k + 1),
          "A spinner has 4 equal parts numbered 1 to 4. It is spun twice. What is the probability that the sum of the two spins is %d?" % ev3]
    key = ["%s. There are 36 outcomes, and %d of them have a sum of %d." % (fstr(F(c1, 36)), c1, s),
           "%s. There are 8 outcomes, and %d of them have exactly %d heads." % (fstr(F(c2, 8)), c2, k + 1),
           "%s. There are 16 outcomes, and %d of them have a sum of %d." % (fstr(F(c3, 16)), c3, ev3)]
    return dict(qs=qs, key=key, dir=D1, dur=190)


def b_pspace(lp, r):
    cols = r.choice([["red", "blue", "green"], ["circle", "square", "star"], ["1", "2", "3"]])
    br, fl = r.choice([(["white", "wheat"], ["ham", "turkey", "cheese"]), (["plain", "sesame"], ["egg", "tuna", "veggie"])])
    qs = ["A coin is flipped and a spinner with 3 equal parts (%s) is spun. List the sample space as an organized list." % ", ".join(cols),
          "A sandwich has 1 bread (%s) and 1 filling (%s). Draw a tree diagram or make a table. How many different sandwiches are possible?" % (" or ".join(br), ", ".join(fl)),
          "Two 4-sided dice (1 to 4) are rolled. Make a table of the sample space. How many outcomes are there?"]
    key = ["6 outcomes: H-%s, H-%s, H-%s, T-%s, T-%s, T-%s." % (cols[0], cols[1], cols[2], cols[0], cols[1], cols[2]),
           "%d sandwiches (%d breads × %d fillings): %s." % (len(br) * len(fl), len(br), len(fl), ", ".join("%s-%s" % (b, f) for b in br for f in fl)),
           "16 outcomes (4 × 4). A 4 by 4 table, with one die along the top and the other along the side."]
    return dict(qs=qs, key=key, dir=D1, dur=190)


def b_psim(lp, r):
    pool = [("A family has 3 children. Design a simulation with coins to estimate the probability that all 3 are girls.", "Let heads be a girl. Flip 3 coins for one trial. Repeat many times (like 50). The probability is about (trials with 3 heads) ÷ (total trials). The real probability is 1/8."),
            ("A quiz has 3 true/false questions and a student guesses. Design a simulation to estimate the chance of getting all 3 right.", "Flip a coin for each question (heads is right). Do 3 flips per trial and repeat many times. Count trials with 3 heads. The real probability is 1/8."),
            ("A cereal box has 1 of 4 equally likely toys. Design a simulation to estimate how many boxes it takes to get a toy you want.", "Use a number cube and reroll if you get 5 or 6, so numbers 1 to 4 stand for the toys. Let 1 be the toy you want. Roll until you get 1 and record the number of rolls. Repeat many times and find the mean."),
            ("A basketball player makes 50%% of free throws. Design a simulation to estimate the chance of making 2 in a row.", "Flip a coin for each shot (heads is made). Do 2 flips per trial and repeat many times. Count trials with 2 heads. The real probability is 1/4.")]
    it = pick(pool, 3, r)
    return dict(qs=[q.replace("%%", "%") for q, _ in it], key=[k for _, k in it], dir="Listen to each problem. Say or write how you would set up the simulation.", dur=200)


BUILD = {
    ("7.RP.A.2", "decide"): b_decide, ("7.RP.A.2", "constant"): b_constant, ("7.RP.A.2", "equation"): b_equation, ("7.RP.A.2", "points"): b_points,
    ("7.RP.A.3", "markup"): b_markup, ("7.RP.A.3", "interest"): b_interest, ("7.RP.A.3", "change"): b_change, ("7.RP.A.3", "error"): b_error,
    ("7.NS.A.3", "addsub"): b_addsub, ("7.NS.A.3", "muldiv"): b_muldiv, ("7.NS.A.3", "complex"): b_complex,
    ("7.EE.B.3", "solve"): b_ee3_solve, ("7.EE.B.3", "convert"): b_ee3_convert, ("7.EE.B.3", "estimate"): b_estimate,
    ("7.EE.B.4", "pxq"): b_pxq, ("7.EE.B.4", "paren"): b_paren, ("7.EE.B.4", "ineq"): b_ineq,
    ("7.G.A.2", "exist"): b_exist, ("7.G.A.2", "unique"): b_unique,
    ("7.G.B.4", "circ"): b_circ, ("7.G.B.4", "area"): b_carea, ("7.G.B.4", "relate"): b_crelate,
    ("7.G.B.6", "area"): b_area2, ("7.G.B.6", "volume"): b_vol, ("7.G.B.6", "surface"): b_surf,
    ("7.SP.B.4", "center"): b_scenter, ("7.SP.B.4", "variability"): b_svar, ("7.SP.B.4", "inference"): b_sinfer,
    ("7.SP.C.8", "fraction"): b_pfrac, ("7.SP.C.8", "space"): b_pspace, ("7.SP.C.8", "simulate"): b_psim,
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
    L = ["/* G7MATH-STRANDS-BEGIN (generated by source/tools/gen_g7math.py, edit the generator, not this block) */",
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append("var G7PIC=%s;" % json.dumps(data, ensure_ascii=False))
    L.append(P1.APPLY.replace("G1PIC", "G7PIC"))
    L.append("/* G7MATH-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G7, encoding="utf8").read()
    if "G7MATH-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G7MATH-STRANDS-BEGIN.*?G7MATH-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        s = src.rstrip()
        assert s.endswith("})();"), s[-40:]
        src = s[:-5] + block + "\n})();\n"
    open(G7, "w", encoding="utf8").write(src)
    print("parts:", sum(len(p) for std in data.values() for p in std.values()), "block bytes:", len(block))


if __name__ == "__main__":
    main()
