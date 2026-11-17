"""Builds the parts (strands) for the Grade 4 math standards that have more than one gray-book "I can" line, all 10 LPs,
and writes them into source/gx/g4.js.

4.NBT.A.1, 4.NBT.A.3 and 4.NF.C.6 have one "I can" line each, so they stay whole standards.
Run:  python3 source/tools/gen_g4math.py
"""
import json, os, re, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N
import gen_g1pic as P1
import gen_g3math as G3

G4 = os.path.join(HERE, '..', 'gx', 'g4.js')
THEME, rng_for, nm, BAD = N.THEME, N.rng_for, N.nm, N.BAD
svg, row = P1.svg, P1.row
INK = P1.INK
colour = G3.colour
bar_frac, qfrac = G3.bar_frac, G3.qfrac


def C(*p):
    return list(p)


CAT = {
    "4.OA.A.1": {"desc": "multiplication equations as comparisons", "parts": C(
        ("interpret", "Interpret a multiplication equation as a comparison", "Interpreting a multiplication equation as a comparison"),
        ("represent", "Write multiplication equations for comparisons", "Representing verbal statements of multiplicative comparisons as multiplication equations"))},
    "4.NF.A.1": {"desc": "equivalent fractions with visual models, recognizing them, and making them", "parts": C(
        ("explain", "Explain equivalent fractions with models", "Explaining why a fraction a/b is equivalent to (n × a)/(n × b) by using visual fraction models"),
        ("recognize", "Recognize equivalent fractions", "Recognizing equivalent fractions"),
        ("generate", "Generate equivalent fractions", "Generating equivalent fractions"))},
    "4.NF.A.2": {"desc": "comparing fractions with different numerators and denominators", "parts": C(
        ("diffnum", "Compare fractions with different numerators", "Comparing two fractions with different numerators"),
        ("diffden", "Compare fractions with different denominators", "Comparing two fractions with different denominators"),
        ("diffboth", "Compare fractions with different numerators and denominators", "Comparing two fractions with different numerators and different denominators"),
        ("samewhole", "Know comparisons need the same whole", "Recognizing that comparisons are valid only when the two fractions refer to the same whole"),
        ("symbols", "Record comparisons with >, =, or <", "Recording the results of fraction comparisons with the symbols >, =, or <"),
        ("justify", "Justify a comparison with a model", "Justifying fraction comparisons by using a visual fraction model"))},
    "4.NF.C.7": {"desc": "comparing decimals to hundredths", "parts": C(
        ("reason", "Compare decimals by reasoning about size", "Comparing two decimals to hundredths by reasoning about their size"),
        ("samewhole", "Know decimal comparisons need the same whole", "Recognizing that decimal comparisons are valid only when the two decimals refer to the same whole"),
        ("symbols", "Record decimal comparisons with >, =, or <", "Recording the results of decimal comparisons with the symbols >, =, or <"),
        ("justify", "Justify a decimal comparison with a number line", "Justifying decimal comparisons by using the number line or another visual model"))},
    "4.MD.A.1": {"desc": "relative sizes of measurement units, converting to smaller units, and conversion tables", "parts": C(
        ("metric_len", "Metric length units (km, m, cm)", "Knowing the relative sizes of metric length units (km, m, cm)"),
        ("metric_mass", "Metric mass units (kg, g)", "Knowing the relative sizes of metric mass units (kg, g)"),
        ("cust_wt", "Customary weight units (lb, oz)", "Knowing the relative sizes of customary weight units (lb, oz)"),
        ("liquid", "Liquid volume units (l, ml)", "Knowing the relative sizes of liquid volume units (l, ml)"),
        ("time", "Units of time (hr, min, sec)", "Knowing the relative sizes of units of time (hr, min, sec)"),
        ("express", "Express a larger unit in a smaller unit", "Expressing measurements in a larger unit in terms of a smaller unit within a single system of measurement"),
        ("table", "Record equivalents in a two-column table", "Recording measurement equivalents in a two-column table"))},
    "4.MD.A.3": {"desc": "area and perimeter formulas for rectangles in real-world and mathematical problems", "parts": C(
        ("area_real", "Area of rectangles, real-world problems", "Applying the area formula for rectangles in real-world problems"),
        ("area_math", "Area of rectangles, mathematical problems", "Applying the area formula for rectangles in mathematical problems"),
        ("per_real", "Perimeter of rectangles, real-world problems", "Applying the perimeter formula for rectangles in real-world problems"),
        ("per_math", "Perimeter of rectangles, mathematical problems", "Applying the perimeter formula for rectangles in mathematical problems"))},
    "4.G.A.2": {"desc": "classifying two-dimensional figures and right triangles", "parts": C(
        ("classify", "Classify figures by parallel lines, perpendicular lines, and angles", "Classifying two-dimensional figures based on the presence or absence of parallel or perpendicular lines, or angles of a specified size"),
        ("rtcat", "Recognize right triangles as a category", "Recognizing right triangles as a category"),
        ("rtid", "Identify right triangles", "Identifying right triangles"))},
}

LET = "ABCDE"
TELL = "Look at the three shapes. Your teacher asks about one at a time. Say your answer out loud."


def noun(lp, r):
    n = list(THEME[lp][0])
    r.shuffle(n)
    return n


def cmp_sym(a, b, c, d):
    x, y = a * d, c * b
    return ">" if x > y else "<" if x < y else "="


# ------------------------------------------------------------------ OA.A.1
EQS = [(24, 4, 6), (35, 5, 7), (18, 3, 6), (32, 4, 8), (45, 5, 9), (42, 6, 7), (36, 4, 9), (28, 4, 7), (54, 6, 9), (27, 3, 9), (56, 7, 8), (30, 5, 6)]


def b_interpret(lp, r):
    es = r.sample(EQS, 3)
    (p1, a1, b1), (p2, a2, b2), (p3, a3, b3) = es
    qs = ["Interpret the equation %d = %d × %d as a comparison. Use the words \"times as many\"." % (p1, a1, b1),
          "Interpret the equation %d = %d × %d as a comparison. Say it two ways." % (p2, a2, b2),
          "A student says, \"In %d = %d × %d, %d is %d more than %d.\" Is that right? Explain." % (p3, a3, b3, p3, a3, b3)]
    key = ["%d is %d times as many as %d, and %d is %d times as many as %d." % (p1, a1, b1, p1, b1, a1),
           "%d is %d times as many as %d. Also, %d is %d times as many as %d." % (p2, a2, b2, p2, b2, a2),
           "No. It is a multiplication comparison, not an addition one. %d is %d times as many as %d, and %d is %d times as many as %d." % (p3, a3, b3, p3, b3, a3)]
    return dict(qs=qs, key=key, dir="Listen to each question. Tell your teacher what the equation says as a comparison.", dur=140)


def b_represent(lp, r):
    xs = noun(lp, r)
    a1, k1 = r.randint(3, 9), r.randint(3, 8)
    a2, k2 = r.randint(3, 9), r.randint(3, 8)
    a3, k3 = r.randint(4, 9), r.randint(3, 8)
    n0, n1 = nm(lp, 0), nm(lp, 1)
    qs = ["A blue ribbon is %d feet long. A red ribbon is %d times as long as the blue ribbon, so it is %d feet long. Write a multiplication equation for this comparison." % (a1, k1, a1 * k1),
          "%s saved %d dollars. %s saved %d times as much. Use the letter s for how much %s saved. Write a multiplication equation." % (n0, a2, n1, k2, n1),
          "Write a multiplication equation for this statement: %d is %d times as many as %d." % (a3 * k3, k3, a3)]
    key = [("%d × %d = %d (or %d × %d = %d)." % (k1, a1, a1 * k1, a1, k1, a1 * k1)) if a1 != k1 else "%d × %d = %d." % (k1, a1, a1 * k1),
           "%d × %d = s, so s = %d." % (k2, a2, a2 * k2),
           ("%d × %d = %d (or %d × %d = %d)." % (k3, a3, a3 * k3, a3, k3, a3 * k3)) if a3 != k3 else "%d × %d = %d." % (k3, a3, a3 * k3)]
    return dict(qs=qs, key=key, dir="Listen to each question. Write a multiplication equation on your paper for the comparison.", dur=150)


# ------------------------------------------------------------------ NF.A.1
PAIRS = [(1, 2, 2), (2, 3, 2), (3, 4, 2), (1, 3, 4), (2, 3, 3), (3, 4, 3), (1, 4, 3), (1, 2, 3), (2, 5, 2), (3, 5, 2), (1, 2, 4), (1, 3, 2), (2, 4, 2), (5, 6, 2), (1, 6, 2)]


def b_explain(lp, r):
    col = colour(lp)
    ps = r.sample(PAIRS, 3)
    html = ""
    qs, key = [], []
    for i, (a, b, n) in enumerate(ps):
        html += row([("%d: top bar" % (i + 1), bar_frac(b, set(range(a)), col)), ("%d: bottom bar" % (i + 1), bar_frac(b * n, set(range(a * n)), col))])
        qs.append("Pair %d. The top bar shows %d/%d. The bottom bar shows %d/%d. Why are these fractions the same size even though the parts look different? Talk about how many parts and how big the parts are." % (i + 1, a, b, a * n, b * n))
        key.append("Each of the %d parts in the top bar is cut into %d smaller parts. So there are %d times as many parts shaded (%d × %d = %d) and %d times as many parts in all (%d × %d = %d). The parts are smaller, but the shaded amount of the whole is the same: %d/%d = %d/%d." % (b, n, n, n, a, a * n, n, n, b, b * n, a, b, a * n, b * n))
    return dict(qs=qs, key=key, dir="Look at the three pairs of bars. Your teacher asks about one pair at a time. Explain out loud.", dur=210, html=html)


def b_recognize(lp, r):
    cases = []
    (a, b, n) = r.choice(PAIRS)
    cases.append((a, b, a * n, b * n, True))
    (a, b, n) = r.choice(PAIRS)
    cases.append((a, b, a * n, b * n + 1 if b * n + 1 != b * n else b * n + 2, False))
    (a, b, n) = r.choice([p for p in PAIRS if p[2] >= 2])
    cases.append((a, b, a * n, b * n, True))
    if lp % 2:
        cases = [cases[1], cases[0], cases[2]]
    qs, key = [], []
    for (a, b, c, d, ok) in cases:
        qs.append("Are %d/%d and %d/%d equivalent fractions? How do you know?" % (a, b, c, d))
        if ok:
            n = c // a
            key.append("Yes. %d × %d = %d and %d × %d = %d, so you multiplied the top and bottom by the same number." % (a, n, c, b, n, d))
        else:
            key.append("No. The top is %d × %d = %d, but %d × %d is not %d. The top and bottom were not multiplied by the same number." % (a, c // a, c, b, c // a, d))
    return dict(qs=qs, key=key, dir="Listen to each question. Say yes or no and tell how you know.", dur=140)


def b_generate(lp, r):
    a, b, n = r.choice([(2, 5, 2), (3, 4, 2), (1, 3, 2), (3, 8, 2), (2, 3, 2), (5, 6, 2)])
    a2, b2 = r.choice([(3, 4), (2, 3), (1, 2), (3, 5), (5, 6)]); m2 = r.choice([2, 3, 4])
    a3, b3 = r.choice([(2, 5), (3, 4), (1, 3), (3, 5)]); m3 = r.choice([3, 4, 5])
    qs = ["Write two fractions that are equivalent to %d/%d. Tell what you multiplied by." % (a, b),
          "Write a fraction equivalent to %d/%d that has %d on the bottom." % (a2, b2, b2 * m2),
          "Fill in the missing number: %d/%d = ?/%d. Tell how you found it." % (a3, b3, b3 * m3)]
    key = ["Any (n × %d)/(n × %d), such as %d/%d (n = 2) and %d/%d (n = 3)." % (a, b, 2 * a, 2 * b, 3 * a, 3 * b),
           "%d/%d. Multiply the top and the bottom by %d." % (a2 * m2, b2 * m2, m2),
           "%d. The bottom was multiplied by %d, so multiply the top %d × %d = %d." % (a3 * m3, m3, a3, m3, a3 * m3)]
    return dict(qs=qs, key=key, dir="Listen to each question. Write your answer on your paper. Tell your teacher what you did.", dur=150)


# ------------------------------------------------------------------ NF.A.2
SAME_DEN = [(3, 5, 8), (2, 7, 9), (5, 3, 8), (4, 9, 11), (7, 4, 8), (3, 7, 12), (5, 11, 12), (2, 5, 6)]  # n1, n2, d


def b_diffnum(lp, r):
    ps = r.sample([(3, 5, 8), (2, 7, 9), (5, 3, 8), (4, 9, 11), (7, 4, 8), (3, 7, 10), (5, 11, 12), (2, 5, 6), (4, 7, 12)], 3)
    qs, key = [], []
    for n1, n2, d in ps:
        qs.append("Which is greater, %d/%d or %d/%d? Tell how you know without using a drawing." % (n1, d, n2, d))
        g = max(n1, n2)
        key.append("%d/%d is greater. The denominators are the same, so the parts are the same size and %d parts is more than %d parts." % (g, d, g, min(n1, n2)))
    return dict(qs=qs, key=key, dir="Listen to each question. Say which fraction is greater and tell how you know.", dur=120)


def b_diffden(lp, r):
    n1, d1, d2 = r.choice([(3, 4, 8), (3, 5, 8), (2, 3, 6), (5, 6, 8), (1, 3, 8)])
    n2, d3, d4 = r.choice([(2, 3, 7), (3, 4, 6), (5, 8, 12), (4, 5, 9)])
    qs = ["Which is greater, %d/%d or %d/%d? Tell how you know." % (n1, d1, n1, d2),
          "Which is greater, %d/%d or %d/%d? Tell how you know." % (n2, d3, n2, d4),
          "Compare 2/3 and 4/9. Make the numerators the same to compare them. Which is greater?"]
    g1 = d1 if d1 < d2 else d2
    g2 = d3 if d3 < d4 else d4
    key = ["%d/%d is greater. The numerators are the same, so the one with the smaller denominator has bigger parts." % (n1, g1),
           "%d/%d is greater. The numerators are the same, so the one with the smaller denominator has bigger parts." % (n2, g2),
           "2/3 = 4/6, and 4/6 > 4/9 because sixths are bigger than ninths. So 2/3 is greater."]
    return dict(qs=qs, key=key, dir="Listen to each question. Say which fraction is greater and tell how you know.", dur=150)


def b_diffboth(lp, r):
    pool = [((3, 4), (5, 8), "Common denominator 8: 3/4 = 6/8, and 6/8 > 5/8, so 3/4 is greater."),
            ((4, 7), (3, 8), "Benchmark 1/2: 4/7 is more than 1/2 and 3/8 is less than 1/2, so 4/7 is greater."),
            ((5, 6), (7, 12), "Common denominator 12: 5/6 = 10/12, and 10/12 > 7/12, so 5/6 is greater."),
            ((2, 5), (3, 8), "Benchmark 1/2: 2/5 is less than 1/2 (half of 5 is 2 1/2) and 3/8 is less than 1/2 (half of 8 is 4). Use a common denominator of 40: 16/40 > 15/40, so 2/5 is greater."),
            ((5, 8), (2, 3), "Common denominator 24: 5/8 = 15/24 and 2/3 = 16/24, so 2/3 is greater."),
            ((3, 10), (4, 5), "Benchmark 1/2: 3/10 is less than 1/2 and 4/5 is more than 1/2, so 4/5 is greater."),
            ((7, 8), (5, 6), "Common denominator 24: 7/8 = 21/24 and 5/6 = 20/24, so 7/8 is greater.")]
    ps = r.sample(pool, 3)
    qs, key = [], []
    for (a, b), (c, d), how in ps:
        qs.append("Compare %d/%d and %d/%d. Which is greater? Use a common denominator or compare each to 1/2." % (a, b, c, d))
        key.append(how)
    return dict(qs=qs, key=key, dir="Listen to each question. Say which fraction is greater and tell how you know.", dur=190)


def b_samewhole_f(lp, r):
    col = colour(lp)
    figs = [("A", bar_frac(4, {0}, col, w=300)), ("B", bar_frac(2, {0}, col, w=110))]
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    qs = ["Bar A is %s's ribbon. Bar B is %s's ribbon. %s says, \"1/2 is more than 1/4, so the shaded part of B is longer.\" Is %s right? Look at the bars." % (n0, n1, n2, n2),
          "%s ate 1/2 of a small pizza. %s ate 1/3 of a very large pizza. Can you tell who ate more pizza just by comparing 1/2 and 1/3? Explain." % (n0, n1),
          "%s ate 3/8 of a pizza. %s ate 5/8 of the same pizza. Can you compare these fractions to tell who ate more? Why?" % (n0, n1)]
    key = ["No. The wholes are different sizes. 1/4 of the long ribbon is longer than 1/2 of the short ribbon. A comparison only works when both fractions are parts of the same whole.",
           "No. The pizzas are different sizes. Comparing 1/2 and 1/3 only works for the same whole. Here 1/3 of a very large pizza could be more.",
           "Yes. Both fractions are parts of the same pizza, so %s ate more with 5/8 than 3/8." % n1]
    return dict(qs=qs, key=key, dir="Look at the bars for the first question. Then your teacher asks two more. Say your answers out loud.", dur=170, html=row(figs))


def b_symbols_f(lp, r):
    pool = [((2, 3), (4, 6)), ((5, 8), (3, 4)), ((4, 5), (7, 10)), ((1, 2), (3, 8)), ((3, 4), (9, 12)), ((2, 5), (1, 2)), ((5, 6), (4, 6)), ((7, 10), (3, 5)), ((2, 3), (3, 4))]
    ps = r.sample(pool, 3)
    qs, key = [], []
    for (a, b), (c, d) in ps:
        qs.append("Write >, =, or < to compare %d/%d and %d/%d. Show your work." % (a, b, c, d))
        key.append("%d/%d %s %d/%d." % (a, b, cmp_sym(a, b, c, d), c, d))
    return dict(qs=qs, key=key, dir="Listen to each question. Write the comparison with a symbol on your paper.", dur=150)


def b_justify_f(lp, r):
    col = colour(lp)
    pool = [((3, 8), (1, 2)), ((2, 3), (5, 8)), ((3, 4), (5, 6)), ((2, 5), (3, 10)), ((7, 8), (3, 4)), ((1, 3), (2, 8))]
    ps = r.sample(pool, 3)
    html = ""
    qs, key = [], []
    for i, ((a, b), (c, d)) in enumerate(ps):
        html += row([("%d: bar A" % (i + 1), bar_frac(b, set(range(a)), col)), ("%d: bar B" % (i + 1), bar_frac(d, set(range(c)), col))])
        qs.append("Pair %d. Bar A shows %d/%d. Bar B shows %d/%d. The bars are the same size. Which fraction is greater? Use the bars to explain." % (i + 1, a, b, c, d))
        s = cmp_sym(a, b, c, d)
        gr = "A (%d/%d)" % (a, b) if s == ">" else "B (%d/%d)" % (c, d)
        key.append("%d/%d %s %d/%d. Bar %s has more of the same-size whole shaded." % (a, b, s, c, d, gr[0]))
    return dict(qs=qs, key=key, dir="Look at the three pairs of bars. Your teacher asks about one pair at a time. Compare and explain with the bars.", dur=200, html=html)


# ------------------------------------------------------------------ NF.C.7 decimals
def numline_dec(lo, pts, w=380):
    x0 = 24; L = w - 48
    body = '<line x1="%d" y1="56" x2="%d" y2="56" stroke="%s" stroke-width="3"/>' % (x0, x0 + L, INK)
    for i in range(11):
        x = x0 + L * i / 10.0
        body += '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="2.5"/>' % (x, 46 if i in (0, 10) else 49, x, 66 if i in (0, 10) else 63, INK)
    body += '<text x="%d" y="86" font-size="15" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%.1f</text>' % (x0, INK, lo)
    body += '<text x="%d" y="86" font-size="15" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%.1f</text>' % (x0 + L, INK, lo + 0.1)
    for L_, k in pts.items():
        x = x0 + L * k / 10.0
        body += '<circle cx="%.1f" cy="56" r="7" fill="#c0392b" stroke="%s" stroke-width="2"/>' % (x, INK)
        body += '<text x="%.1f" y="36" font-size="16" font-weight="800" text-anchor="middle" fill="%s" font-family="sans-serif">%s</text>' % (x, INK, L_)
    return svg(w, 96, body, "A number line from %.1f to %.1f in hundredths" % (lo, lo + 0.1))


def dec(v):
    s = ("%.2f" % v)
    return s[:-1] if s.endswith("0") and s != "0.00" else s


def b_reason(lp, r):
    pool = [(0.4, 0.38), (0.7, 0.07), (0.56, 0.65), (0.9, 0.89), (0.2, 0.19), (0.45, 0.5), (0.08, 0.1), (0.63, 0.6), (0.31, 0.4)]
    ps = r.sample(pool, 3)
    qs, key = [], []
    for a, b in ps:
        qs.append("Which is greater, %s or %s? Tell how you know by thinking about the digits and their places." % (dec(a), dec(b)))
        g, l = (a, b) if a > b else (b, a)
        key.append("%s is greater. For example, %s is %d hundredths and %s is %d hundredths, so %d hundredths is more than %d hundredths." % (dec(g), dec(g), round(g * 100), dec(l), round(l * 100), round(g * 100), round(l * 100)))
    return dict(qs=qs, key=key, dir="Listen to each question. Say which decimal is greater and tell how you know.", dur=140)


def b_samewhole_d(lp, r):
    col = colour(lp)
    figs = [("A", bar_frac(10, set(range(5)), col, w=110)), ("B", bar_frac(10, set(range(3)), col, w=300))]
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    qs = ["Bar A is %s's ribbon with 0.5 shaded. Bar B is %s's ribbon with 0.3 shaded. %s says, \"0.5 is more than 0.3, so A has more shaded.\" Is that always a fair comparison? Look at the bars." % (n0, n1, n2),
          "%s drank 0.6 of a small juice box. %s drank 0.4 of a large bottle. Can you tell who drank more just by comparing 0.6 and 0.4? Explain." % (n0, n1),
          "%s ate 0.45 of a pizza. %s ate 0.54 of the same pizza. Can you compare these decimals to tell who ate more? Why?" % (n0, n1)]
    key = ["No. The wholes are different sizes. Here 0.3 of the long ribbon is longer than 0.5 of the short ribbon. Decimals can only be compared when they are parts of the same whole.",
           "No. The containers are different sizes. 0.4 of the large bottle could be more than 0.6 of the small box.",
           "Yes. They are parts of the same pizza. 0.54 > 0.45, so %s ate more." % n1]
    return dict(qs=qs, key=key, dir="Look at the bars for the first question. Then your teacher asks two more. Say your answers out loud.", dur=170, html=row(figs))


def b_symbols_d(lp, r):
    pool = [(0.6, 0.60), (0.09, 0.1), (0.72, 0.7), (0.35, 0.53), (0.4, 0.04), (0.50, 0.5), (0.81, 0.18), (0.2, 0.25)]
    ps = r.sample(pool, 3)
    if not any(a == b for a, b in ps):
        ps[2] = r.choice([p for p in pool if p[0] == p[1]])
    qs, key = [], []
    for a, b in ps:
        qs.append("Write >, =, or < to compare %s and %s." % (dec(a) if a != 0.60 else "0.60", dec(b) if b != 0.60 else "0.60"))
        s = ">" if a > b else "<" if a < b else "="
        key.append("%s %s %s." % (dec(a), s, dec(b)))
    return dict(qs=qs, key=key, dir="Listen to each question. Write the comparison with a symbol on your paper.", dur=120)


def b_justify_d(lp, r):
    html = ""
    qs, key = [], []
    for i in range(3):
        lo = r.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
        ka, kb = r.sample(range(1, 10), 2)
        html += '<div class="small" style="text-align:center;font-weight:700;margin-top:6px">%d</div>' % (i + 1) + numline_dec(lo, {"A": ka, "B": kb})
        a, b = lo + ka / 100.0, lo + kb / 100.0
        qs.append("Number line %d goes from %.1f to %.1f in hundredths. Name the decimal at point A and at point B. Which is greater? Use the number line to explain." % (i + 1, lo, lo + 0.1))
        g = "A" if ka > kb else "B"
        key.append("A = %.2f, B = %.2f. Point %s is greater because it is farther to the right on the number line." % (a, b, g))
    return dict(qs=qs, key=key, dir="Look at the three number lines. Your teacher asks about one at a time. Name the decimals and explain with the line.", dur=200, html=html)


# ------------------------------------------------------------------ MD.A.1
def pick3(pool, lp, r):
    p = pool[:]
    r.shuffle(p)
    return p[:3]


METRIC_LEN = [("How many centimeters are in 1 meter?", "100 centimeters."), ("How many meters are in 1 kilometer?", "1000 meters."),
              ("Which is longer, 1 meter or 1 centimeter? How many times as long?", "1 meter. It is 100 times as long."),
              ("Which is longer, 1 kilometer or 1 meter? How many times as long?", "1 kilometer. It is 1000 times as long."),
              ("Which unit would you use to measure the length of a pencil: km, m, or cm? Why?", "Centimeters (cm). A pencil is short, so a small unit fits."),
              ("Which unit would you use to measure how far it is to the next town: km, m, or cm?", "Kilometers (km). It is a long distance.")]
METRIC_MASS = [("How many grams are in 1 kilogram?", "1000 grams."), ("Which is heavier, 1 kilogram or 1 gram? How many times as heavy?", "1 kilogram. It is 1000 times as heavy."),
               ("Which unit would you use to measure a paper clip: kg or g? Why?", "Grams (g). A paper clip is very light."),
               ("Which unit would you use to measure a bag of dog food: kg or g? Why?", "Kilograms (kg). It is heavy."),
               ("Is 1 kilogram more or less than 500 grams? How do you know?", "More. 1 kilogram is 1000 grams, and 1000 > 500.")]
CUST_WT = [("How many ounces are in 1 pound?", "16 ounces."), ("Which is heavier, 1 pound or 1 ounce? How many times as heavy?", "1 pound. It is 16 times as heavy."),
           ("Which unit would you use to weigh a slice of cheese: lb or oz? Why?", "Ounces (oz). It is light."),
           ("Which unit would you use to weigh a watermelon: lb or oz? Why?", "Pounds (lb). It is heavy."),
           ("Is 1 pound more or less than 10 ounces? How do you know?", "More. 1 pound is 16 ounces, and 16 > 10.")]
LIQUID = [("How many milliliters are in 1 liter?", "1000 milliliters."), ("Which is more, 1 liter or 1 milliliter? How many times as much?", "1 liter. It is 1000 times as much."),
          ("Which unit would you use to measure a spoonful of medicine: l or ml? Why?", "Milliliters (ml). It is a small amount."),
          ("Which unit would you use to measure water in a fish tank: l or ml? Why?", "Liters (l). It is a large amount."),
          ("Is 1 liter more or less than 800 milliliters? How do you know?", "More. 1 liter is 1000 milliliters, and 1000 > 800.")]
TIME = [("How many minutes are in 1 hour?", "60 minutes."), ("How many seconds are in 1 minute?", "60 seconds."),
        ("Which is longer, 1 hour or 1 minute? How many times as long?", "1 hour. It is 60 times as long."),
        ("Which is longer, 1 minute or 1 second? How many times as long?", "1 minute. It is 60 times as long."),
        ("Which unit would you use to time how long a movie lasts: hr, min, or sec? Why?", "Hours (hr), or minutes (min). Seconds would be a very large number."),
        ("Is 1 hour more or less than 100 minutes? How do you know?", "Less. 1 hour is 60 minutes, and 60 < 100.")]


def b_pool(pool, dur=100):
    def f(lp, r):
        it = pick3(pool, lp, r)
        return dict(qs=[q for q, k in it], key=[k for q, k in it], dir="Listen to each question. Say your answer out loud.", dur=dur)
    return f


CONV = [(4, "meters", "centimeters", 400, "m", "cm", 100), (3, "kilometers", "meters", 3000, "km", "m", 1000), (5, "kilograms", "grams", 5000, "kg", "g", 1000),
        (6, "liters", "milliliters", 6000, "l", "ml", 1000), (3, "pounds", "ounces", 48, "lb", "oz", 16), (2, "hours", "minutes", 120, "hr", "min", 60),
        (5, "minutes", "seconds", 300, "min", "sec", 60), (4, "feet", "inches", 48, "ft", "in", 12), (7, "meters", "centimeters", 700, "m", "cm", 100),
        (2, "kilograms", "grams", 2000, "kg", "g", 1000), (9, "pounds", "ounces", 144, "lb", "oz", 16), (8, "liters", "milliliters", 8000, "l", "ml", 1000)]


def b_express(lp, r):
    it = pick3(CONV, lp, r)
    qs = ["Express %d %s in %s. Tell how you figured it out." % (n, big, small) for n, big, small, ans, bu, su, f in it]
    key = ["%d %s. 1 %s = %d %s, so %d × %d = %d." % (ans, small, bu, f, su, n, f, ans) for n, big, small, ans, bu, su, f in it]
    return dict(qs=qs, key=key, dir="Listen to each question. Write the equal measurement on your paper. Say how you found it.", dur=130)


TABLES = [("feet", "inches", 12, "ft", "in"), ("hours", "minutes", 60, "hr", "min"), ("meters", "centimeters", 100, "m", "cm"), ("kilograms", "grams", 1000, "kg", "g"),
          ("liters", "milliliters", 1000, "l", "ml"), ("pounds", "ounces", 16, "lb", "oz"), ("minutes", "seconds", 60, "min", "sec"), ("kilometers", "meters", 1000, "km", "m")]


def b_table(lp, r):
    it = pick3(TABLES, lp, r)
    qs, key = [], []
    for big, small, f, bu, su in it:
        qs.append("Make a two-column table that shows how many %s are in 1, 2, 3, and 4 %s." % (small, big))
        key.append("%s | %s: (1, %d), (2, %d), (3, %d), (4, %d)." % (bu, su, f, 2 * f, 3 * f, 4 * f))
    return dict(qs=qs, key=key, dir="Listen to each question. Draw the table on your paper and fill it in. Then tell your teacher the pattern.", dur=190)


# ------------------------------------------------------------------ MD.A.3
def b_area_real(lp, r):
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    l1, w1 = r.randint(8, 15), r.randint(6, 12)
    l2, w2 = r.randint(6, 14), r.randint(4, 9)
    L3, w3 = r.randint(20, 40), r.randint(5, 9)
    qs = ["%s's bedroom floor is a rectangle %d feet long and %d feet wide. How many square feet of carpet cover the whole floor?" % (n0, l1, w1),
          "%s plants a rectangular garden that is %d meters long and %d meters wide. How many square meters of soil are needed to cover it?" % (n1, l2, w2),
          "A rectangular poster is %d inches long and %d inches wide. %s wants to cover it with a sheet of clear plastic the same size. How many square inches of plastic does %s need?" % (L3, w3, n2, n2)]
    key = ["%d square feet (%d × %d = %d)." % (l1 * w1, l1, w1, l1 * w1), "%d square meters (%d × %d = %d)." % (l2 * w2, l2, w2, l2 * w2), "%d square inches (%d × %d = %d)." % (L3 * w3, L3, w3, L3 * w3)]
    return dict(qs=qs, key=key, dir="Listen to each problem. Solve it on your paper. Write the area formula you used.", dur=150)


def b_area_math(lp, r):
    l1, w1 = r.randint(7, 14), r.randint(4, 9)
    w2 = r.randint(4, 9); l2 = r.randint(6, 12)
    w3 = r.randint(5, 9); l3 = r.randint(8, 16)
    qs = ["A rectangle has a length of %d cm and a width of %d cm. What is its area?" % (l1, w1),
          "A rectangle has an area of %d square cm and a width of %d cm. What is its length? Write a multiplication equation with an unknown factor." % (l2 * w2, w2),
          "A rectangle has an area of %d square inches and a length of %d inches. What is its width? Write a multiplication equation with an unknown factor." % (l3 * w3, l3)]
    key = ["%d square cm (%d × %d = %d)." % (l1 * w1, l1, w1, l1 * w1), "%d cm. ? × %d = %d, so ? = %d." % (l2, w2, l2 * w2, l2), "%d inches. %d × ? = %d, so ? = %d." % (w3, l3, l3 * w3, w3)]
    return dict(qs=qs, key=key, dir="Listen to each problem. Solve it on your paper. Write the equation you used.", dur=150)


def b_per_real(lp, r):
    n0, n1, n2 = nm(lp, 0), nm(lp, 1), nm(lp, 2)
    l1, w1 = r.randint(10, 20), r.randint(6, 12)
    l2, w2 = r.randint(8, 16), r.randint(5, 10)
    l3, w3 = r.randint(30, 60), r.randint(15, 25)
    qs = ["%s wants to put a fence all the way around a rectangular garden that is %d meters long and %d meters wide. How many meters of fence does %s need?" % (n0, l1, w1, n0),
          "%s is gluing ribbon around the edge of a rectangular picture frame that is %d inches long and %d inches wide. How many inches of ribbon does %s need?" % (n1, l2, w2, n1),
          "A rectangular field is %d yards long and %d yards wide. %s jogs once around the outside edge. How many yards does %s jog?" % (l3, w3, n2, n2)]
    key = ["%d meters (2 × %d + 2 × %d = %d)." % (2 * (l1 + w1), l1, w1, 2 * (l1 + w1)), "%d inches (2 × %d + 2 × %d = %d)." % (2 * (l2 + w2), l2, w2, 2 * (l2 + w2)), "%d yards (2 × %d + 2 × %d = %d)." % (2 * (l3 + w3), l3, w3, 2 * (l3 + w3))]
    return dict(qs=qs, key=key, dir="Listen to each problem. Solve it on your paper. Write the perimeter formula you used.", dur=150)


def b_per_math(lp, r):
    l1, w1 = r.randint(8, 15), r.randint(4, 9)
    l2, w2 = r.randint(8, 14), r.randint(4, 8)
    l3, w3 = r.randint(9, 16), r.randint(5, 9)
    qs = ["A rectangle has a length of %d cm and a width of %d cm. What is its perimeter?" % (l1, w1),
          "A rectangle has a perimeter of %d cm and a length of %d cm. What is its width? Write an equation with an unknown." % (2 * (l2 + w2), l2),
          "A rectangle has a width of %d inches and a perimeter of %d inches. What is its length? Write an equation with an unknown." % (w3, 2 * (l3 + w3))]
    key = ["%d cm (2 × %d + 2 × %d = %d)." % (2 * (l1 + w1), l1, w1, 2 * (l1 + w1)),
           "%d cm. 2 × %d + 2 × ? = %d, so 2 × ? = %d and ? = %d." % (w2, l2, 2 * (l2 + w2), 2 * w2, w2),
           "%d inches. 2 × ? + 2 × %d = %d, so 2 × ? = %d and ? = %d." % (l3, w3, 2 * (l3 + w3), 2 * l3, l3)]
    return dict(qs=qs, key=key, dir="Listen to each problem. Solve it on your paper. Write the equation you used.", dur=150)


# ------------------------------------------------------------------ G.A.2
def poly(pts, fill="#fffaf0"):
    d = " ".join("%.1f,%.1f" % p for p in pts)
    return svg(100, 100, '<polygon points="%s" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (d, fill, INK), "A shape")


SHAPES = {
    "square": ([(22, 22), (78, 22), (78, 78), (22, 78)], "Yes, both pairs of opposite sides are parallel.", "Yes, the sides meet at right angles.", "4 right angles"),
    "rectangle": ([(8, 28), (92, 28), (92, 72), (8, 72)], "Yes, both pairs of opposite sides are parallel.", "Yes, the sides meet at right angles.", "4 right angles"),
    "parallelogram": ([(26, 28), (96, 28), (74, 72), (4, 72)], "Yes, both pairs of opposite sides are parallel.", "No, there are no square corners.", "no right angles"),
    "rhombus": ([(50, 8), (92, 50), (50, 92), (8, 50)], "Yes, both pairs of opposite sides are parallel.", "No, the sides do not meet at right angles.", "no right angles"),
    "trapezoid": ([(32, 28), (68, 28), (94, 72), (6, 72)], "Yes, one pair of opposite sides is parallel (the top and bottom).", "No, there are no square corners.", "no right angles"),
    "right triangle": ([(14, 82), (86, 82), (14, 22)], "No, no sides are parallel.", "Yes, two sides meet at a right angle.", "1 right angle"),
}


def b_classify(lp, r):
    names = r.sample(list(SHAPES), 3)
    figs = [(L, poly(SHAPES[n][0])) for L, n in zip("ABC", names)]
    qs = ["Look at shape %s. Does it have parallel sides? Does it have perpendicular sides? Does it have a right angle? What shape is it?" % L for L in "ABC"]
    key = ["%s Perpendicular: %s It has %s. The shape is a %s." % (SHAPES[n][1], SHAPES[n][2], SHAPES[n][3], n) for n in names]
    return dict(qs=qs, key=key, dir=TELL, dur=190, html=row(figs))


TRI = {
    "right scalene": [(10, 86), (90, 86), (10, 26)],
    "right isosceles": [(16, 86), (86, 86), (16, 16)],
    "obtuse": [(6, 82), (94, 82), (80, 50)],
    "acute": [(10, 86), (90, 86), (52, 18)],
}


def b_rtcat(lp, r):
    figs = [("A", poly(TRI["right scalene"])), ("B", poly(TRI["acute"])), ("C", poly(TRI["right isosceles"]))]
    qs = ["What does a triangle need to have to be called a right triangle?",
          "Is triangle A a right triangle? Is triangle B a right triangle? Tell how you know.",
          "Triangle C has two sides the same length and also is a right triangle. Can a triangle be in both groups? Explain."]
    key = ["One right angle, a square corner of 90 degrees. Right triangles are a category.",
           "A is a right triangle because it has a square corner. B is not, because all of its angles are smaller than a square corner.",
           "Yes. Right triangles are a category, and a right triangle can also be isosceles (two sides the same) or scalene (no sides the same)."]
    return dict(qs=qs, key=key, dir="Look at the three triangles. Your teacher asks the questions. Say your answers out loud.", dur=160, html=row(figs))


def b_rtid(lp, r):
    kinds = ["right scalene", "right isosceles", "obtuse", "acute"]
    r.shuffle(kinds)
    figs = [(L, poly(TRI[k])) for L, k in zip("ABCD", kinds)]
    pos = {k: L for L, k in zip("ABCD", kinds)}
    rights = sorted([pos["right scalene"], pos["right isosceles"]])
    qs = ["Which of these triangles are right triangles? How can you tell?",
          "Is triangle %s a right triangle? Tell how you know." % pos["obtuse"],
          "Which triangle is a right triangle with two sides the same length?"]
    key = ["Triangles %s and %s. Each has one square corner (a right angle)." % (rights[0], rights[1]),
           "No. It has an angle bigger than a square corner, so it is an obtuse triangle.",
           "Triangle %s. It is a right triangle and an isosceles triangle." % pos["right isosceles"]]
    return dict(qs=qs, key=key, dir="Look at the four triangles. Your teacher asks about them. Say your answers out loud.", dur=150, html=row(figs))


BUILD = {
    ("4.OA.A.1", "interpret"): b_interpret, ("4.OA.A.1", "represent"): b_represent,
    ("4.NF.A.1", "explain"): b_explain, ("4.NF.A.1", "recognize"): b_recognize, ("4.NF.A.1", "generate"): b_generate,
    ("4.NF.A.2", "diffnum"): b_diffnum, ("4.NF.A.2", "diffden"): b_diffden, ("4.NF.A.2", "diffboth"): b_diffboth,
    ("4.NF.A.2", "samewhole"): b_samewhole_f, ("4.NF.A.2", "symbols"): b_symbols_f, ("4.NF.A.2", "justify"): b_justify_f,
    ("4.NF.C.7", "reason"): b_reason, ("4.NF.C.7", "samewhole"): b_samewhole_d, ("4.NF.C.7", "symbols"): b_symbols_d, ("4.NF.C.7", "justify"): b_justify_d,
    ("4.MD.A.1", "metric_len"): b_pool(METRIC_LEN), ("4.MD.A.1", "metric_mass"): b_pool(METRIC_MASS), ("4.MD.A.1", "cust_wt"): b_pool(CUST_WT),
    ("4.MD.A.1", "liquid"): b_pool(LIQUID), ("4.MD.A.1", "time"): b_pool(TIME), ("4.MD.A.1", "express"): b_express, ("4.MD.A.1", "table"): b_table,
    ("4.MD.A.3", "area_real"): b_area_real, ("4.MD.A.3", "area_math"): b_area_math, ("4.MD.A.3", "per_real"): b_per_real, ("4.MD.A.3", "per_math"): b_per_math,
    ("4.G.A.2", "classify"): b_classify, ("4.G.A.2", "rtcat"): b_rtcat, ("4.G.A.2", "rtid"): b_rtid,
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
                    assert "—" not in d["html"]
                    part["html"] = d["html"]
                parts.append(part)
            out.setdefault(std, {})[str(lp)] = parts
    return out


def js(data):
    L = ["/* G4MATH-STRANDS-BEGIN (generated by source/tools/gen_g4math.py, edit the generator, not this block) */",
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append("var G4PIC=%s;" % json.dumps(data, ensure_ascii=False))
    L.append(P1.APPLY.replace("G1PIC", "G4PIC"))
    L.append("/* G4MATH-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G4, encoding="utf8").read()
    if "G4MATH-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G4MATH-STRANDS-BEGIN.*?G4MATH-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        s = src.rstrip()
        assert s.endswith("})();"), s[-40:]
        src = s[:-5] + block + "\n})();\n"
    open(G4, "w", encoding="utf8").write(src)
    print("parts:", sum(len(p) for std in data.values() for p in std.values()), "block bytes:", len(block))


if __name__ == "__main__":
    main()
