"""Builds the parts (strands) for the Grade 2 math standards, all 10 LPs, and writes them into source/gx/g2.js.

One part per "I can" line in the gray book (lines that are the same skill with different numbers are one part).
Run:  python3 source/tools/gen_g2math.py
"""
import json, os, re, random, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N
import gen_g1pic as P1

G2 = os.path.join(HERE, '..', 'gx', 'g2.js')
THEME, rng_for, nm, BAD = N.THEME, N.rng_for, N.nm, N.BAD
svg, row, bar_fig = P1.svg, P1.row, P1.bar_fig
INK = P1.INK
LET = "ABCDE"

# ------------------------------------------------------------------ catalog
def C(*parts):
    return list(parts)

CAT = {
    "2.OA.A.1": {"desc": "one- and two-step addition and subtraction word problems within 100, with the unknown in any position", "parts": C(
        ("add1to", "Add: one-step, adding to", "I can add within 100 to solve one-step word problems about adding to, with the unknown in any position"),
        ("add1pt", "Add: one-step, putting together or taking apart", "I can add within 100 to solve one-step word problems about putting together or taking apart, with the unknown in any position"),
        ("add1cmp", "Add: one-step, comparing", "I can add within 100 to solve one-step compare word problems, with the unknown in any position"),
        ("add2to", "Add: two-step, adding to", "I can add within 100 to solve two-step word problems about adding to, with the unknown in any position"),
        ("add2pt", "Add: two-step, putting together or taking apart", "I can add within 100 to solve two-step word problems about putting together or taking apart, with the unknown in any position"),
        ("add2cmp", "Add: two-step, comparing", "I can add within 100 to solve two-step compare word problems, with the unknown in any position"),
        ("sub1from", "Subtract: one-step, taking from", "I can subtract within 100 to solve one-step word problems about taking from, with the unknown in any position"),
        ("sub1pt", "Subtract: one-step, putting together or taking apart", "I can subtract within 100 to solve one-step word problems about putting together or taking apart, with the unknown in any position"),
        ("sub1cmp", "Subtract: one-step, comparing", "I can subtract within 100 to solve one-step compare word problems, with the unknown in any position"),
        ("sub2from", "Subtract: two-step, taking from", "I can subtract within 100 to solve two-step word problems about taking from, with the unknown in any position"),
        ("sub2pt", "Subtract: two-step, putting together or taking apart", "I can subtract within 100 to solve two-step word problems about putting together or taking apart, with the unknown in any position"),
        ("sub2cmp", "Subtract: two-step, comparing", "I can subtract within 100 to solve two-step compare word problems, with the unknown in any position"))},
    "2.OA.C.3": {"desc": "odd and even numbers, and writing an even number as a sum of two equal addends", "parts": C(
        ("oddeven", "Tell if a group (up to 20) is odd or even", "I can determine whether a group of objects (up to 20) has an odd or even number of members, by pairing objects or counting by 2s"),
        ("evaneq", "Write an even number as a sum of two equal addends", "I can write an equation to express an even number as a sum of two equal addends"))},
    "2.OA.C.4": {"desc": "using addition to find the total in rectangular arrays, up to 5 rows and 5 columns", "parts": C(
        ("arrays", "Add to find the total in an array", "I can add to find the total number of objects arranged in rectangular arrays with up to 5 rows and up to 5 columns"),
        ("arrayeq", "Write an equation as a sum of equal addends", "I can write an equation to express the total of an array as a sum of equal addends"))},
    "2.NBT.A.2": {"desc": "counting within 1000 and skip-counting by 2s, 5s, 10s, and 100s", "parts": C(
        ("count1000", "Count within 1000", "I can count within 1000"),
        ("skip2", "Skip-count by 2s", "I can skip-count by 2s"),
        ("skip5", "Skip-count by 5s", "I can skip-count by 5s"),
        ("skip10", "Skip-count by 10s", "I can skip-count by 10s"),
        ("skip100", "Skip-count by 100s", "I can skip-count by 100s"))},
    "2.NBT.A.3": {"desc": "reading and writing numbers to 1000 with numerals, number names, and expanded form", "parts": C(
        ("readnum", "Read numbers using base-ten numerals", "I can read numbers to 1000 using base-ten numerals"),
        ("readname", "Read numbers using number names", "I can read numbers to 1000 using number names"),
        ("readexp", "Read numbers using expanded form", "I can read numbers to 1000 using expanded form"),
        ("writenum", "Write numbers using base-ten numerals", "I can write numbers to 1000 using base-ten numerals"),
        ("writename", "Write numbers using number names", "I can write numbers to 1000 using number names"),
        ("writeexp", "Write numbers using expanded form", "I can write numbers to 1000 using expanded form"))},
    "2.NBT.B.7": {"desc": "adding and subtracting within 1000 with models, strategies, and written methods", "parts": C(
        ("addm", "Add within 1000, with models or drawings", "I can add within 1000, using concrete models or drawings"),
        ("adds", "Add within 1000, with strategies", "I can add within 1000, using strategies based on place value, properties of operations, and/or the relationship between addition and subtraction"),
        ("subm", "Subtract within 1000, with models or drawings", "I can subtract within 1000, using concrete models or drawings"),
        ("subs", "Subtract within 1000, with strategies", "I can subtract within 1000, using strategies based on place value, properties of operations, and/or the relationship between addition and subtraction"),
        ("writtenadd", "Relate the addition strategy to a written method", "I can relate the addition strategy to a written method"),
        ("writtensub", "Relate the subtraction strategy to a written method", "I can relate the subtraction strategy to a written method"),
        ("hto", "Add or subtract hundreds and hundreds, tens and tens, ones and ones", "I can show that in adding or subtracting three-digit numbers, one adds or subtracts hundreds and hundreds, tens and tens, ones and ones"),
        ("compose", "Compose or decompose tens or hundreds", "I can show that sometimes it is necessary to compose or decompose tens or hundreds when adding or subtracting within 1000"))},
    "2.MD.A.1": {"desc": "measuring length with rulers, yardsticks, meter sticks, and measuring tapes", "parts": C(
        ("measure", "Measure the length of an object", "I can measure the length of an object"),
        ("selecttool", "Select the appropriate measuring tool", "I can select the appropriate tool (ruler, yardstick, meter stick, measuring tape) when measuring the length of an object"),
        ("usetool", "Use the appropriate tool to measure", "I can use the appropriate tools such as rulers, yardsticks, meter sticks, and measuring tapes when measuring the length of an object"))},
    "2.MD.C.7": {"desc": "telling and writing time to the nearest five minutes with a.m. and p.m., and the relationships of time", "parts": C(
        ("tell_an", "Tell time to 5 minutes (analog clock)", "I can tell time from analog clocks to the nearest five minutes"),
        ("tell_dg", "Tell time to 5 minutes (digital clock)", "I can tell time from digital clocks to the nearest five minutes"),
        ("write_an", "Write time to 5 minutes (analog clock)", "I can write time from analog clocks to the nearest five minutes"),
        ("write_dg", "Write time to 5 minutes (digital clock)", "I can write time from digital clocks to the nearest five minutes"),
        ("tell_ampm", "Use a.m. and p.m. when telling time", "I can use a.m. and p.m. when telling time"),
        ("write_ampm", "Use a.m. and p.m. when writing time", "I can use a.m. and p.m. when writing time"),
        ("relations", "Know the relationships of time", "I can demonstrate my knowledge of the relationships of time, such as minutes in an hour, days in a month, weeks in a year"))},
    "2.MD.C.8": {"desc": "word problems with dollar bills, quarters, dimes, nickels, and pennies, using $ and cent symbols", "parts": C(
        ("moneyprob", "Solve word problems with bills and coins", "I can solve word problems involving dollar bills, quarters, dimes, nickels, and pennies"),
        ("symbols", "Use the $ and cent symbols appropriately", "I can use the $ and cent symbols appropriately"))},
    "2.MD.D.10": {"desc": "drawing picture graphs and bar graphs, and solving problems with bar graphs", "parts": C(
        ("picgraph", "Draw a picture graph", "I can draw a picture graph (single-unit scale) to represent a data set with up to four categories"),
        ("bargraph", "Draw a bar graph", "I can draw a bar graph (single-unit scale) to represent a data set with up to four categories"),
        ("putogether", "Solve put-together problems with a bar graph", "I can solve simple put-together problems using information presented in a bar graph"),
        ("takeapart", "Solve take-apart problems with a bar graph", "I can solve simple take-apart problems using information presented in a bar graph"),
        ("compare", "Solve compare problems with a bar graph", "I can solve simple compare problems using information presented in a bar graph"))},
    "2.G.A.1": {"desc": "recognizing, drawing, and naming shapes by their attributes", "parts": C(
        ("recognize", "Recognize shapes with given attributes", "I can recognize shapes having specified attributes, such as a given number of angles or a given number of equal faces"),
        ("draw", "Draw shapes with given attributes", "I can draw shapes having specified attributes, such as a given number of angles or a given number of equal faces"),
        ("identify", "Identify triangles, quadrilaterals, pentagons, hexagons, and cubes", "I can identify triangles, quadrilaterals, pentagons, hexagons, and cubes"))},
}

# Skill phrases used in the picker and in the gradebook lines ("Secure with <phrase> (3 of 3 correct)").
# They must read after "with", so no "I can".
DESC = {
    "add1to": "One-step addition word problems about adding to (within 100)",
    "add1pt": "One-step addition word problems about putting together or taking apart (within 100)",
    "add1cmp": "One-step addition compare word problems (within 100)",
    "add2to": "Two-step addition word problems about adding to (within 100)",
    "add2pt": "Two-step addition word problems about putting together or taking apart (within 100)",
    "add2cmp": "Two-step addition compare word problems (within 100)",
    "sub1from": "One-step subtraction word problems about taking from (within 100)",
    "sub1pt": "One-step subtraction word problems about putting together or taking apart (within 100)",
    "sub1cmp": "One-step subtraction compare word problems (within 100)",
    "sub2from": "Two-step subtraction word problems about taking from (within 100)",
    "sub2pt": "Two-step subtraction word problems about putting together or taking apart (within 100)",
    "sub2cmp": "Two-step subtraction compare word problems (within 100)",
    "oddeven": "Deciding if a group of up to 20 objects is odd or even, by pairing or counting by 2s",
    "evaneq": "Writing an equation for an even number as a sum of two equal addends",
    "arrays": "Adding to find the total in a rectangular array (up to 5 rows and 5 columns)",
    "arrayeq": "Writing an equation for the total of an array as a sum of equal addends",
    "count1000": "Counting within 1000",
    "skip2": "Skip-counting by 2s", "skip5": "Skip-counting by 5s", "skip10": "Skip-counting by 10s", "skip100": "Skip-counting by 100s",
    "readnum": "Reading numbers to 1000 in base-ten numerals",
    "readname": "Reading numbers to 1000 as number names",
    "readexp": "Reading numbers to 1000 in expanded form",
    "writenum": "Writing numbers to 1000 in base-ten numerals",
    "writename": "Writing numbers to 1000 as number names",
    "writeexp": "Writing numbers to 1000 in expanded form",
    "addm": "Adding within 1000 with models or drawings",
    "adds": "Adding within 1000 with strategies",
    "subm": "Subtracting within 1000 with models or drawings",
    "subs": "Subtracting within 1000 with strategies",
    "writtenadd": "Relating the addition strategy to a written method",
    "writtensub": "Relating the subtraction strategy to a written method",
    "hto": "Adding or subtracting hundreds with hundreds, tens with tens, and ones with ones",
    "compose": "Composing or decomposing tens or hundreds when adding or subtracting within 1000",
    "measure": "Measuring the length of an object",
    "selecttool": "Selecting the appropriate tool to measure length",
    "usetool": "Using rulers, yardsticks, meter sticks, and measuring tapes to measure length",
    "tell_an": "Telling time to the nearest five minutes on analog clocks",
    "tell_dg": "Telling time to the nearest five minutes on digital clocks",
    "write_an": "Writing time to the nearest five minutes from analog clocks",
    "write_dg": "Writing time to the nearest five minutes from digital clocks",
    "tell_ampm": "Using a.m. and p.m. when telling time",
    "write_ampm": "Using a.m. and p.m. when writing time",
    "relations": "Knowing the relationships of time, such as minutes in an hour, days in a month, and weeks in a year",
    "moneyprob": "Word problems with dollar bills, quarters, dimes, nickels, and pennies",
    "symbols": "Using the $ and cent symbols appropriately",
    "picgraph": "Drawing a picture graph (single-unit scale, up to four categories)",
    "bargraph": "Drawing a bar graph (single-unit scale, up to four categories)",
    "putogether": "Solving put-together problems with a bar graph",
    "takeapart": "Solving take-apart problems with a bar graph",
    "compare": "Solving compare problems with a bar graph",
    "recognize": "Recognizing shapes with specified attributes",
    "draw": "Drawing shapes with specified attributes",
    "identify": "Identifying triangles, quadrilaterals, pentagons, hexagons, and cubes",
}
for _s, _c in CAT.items():
    _c["parts"] = [(p[0], p[1], DESC[p[0]]) for p in _c["parts"]]
    assert all(p[0] in DESC for p in _c["parts"])

DIR_EQ = "Listen to each problem. Solve it on your paper. Write an equation with a box or a letter for the number you do not know."
DIR_TALK = "Listen to each question. You can use your paper and pencil. Say your answer out loud."


# ------------------------------------------------------------------ OA.A.1 word problems
def pool(lp, r, k=3):
    nouns = THEME[lp][0]
    return [nouns[i % 3] for i in r.sample(range(3), 3)][:k]


def names(lp):
    return nm(lp, 0), nm(lp, 1), nm(lp, 2)


def ex(eq):
    return " Example equation: %s." % eq


def oa_set(lp, r, kind):
    n1, n2, n3 = names(lp)
    xs = pool(lp, r)
    qs, key = [], []

    def add(q, k):
        qs.append(q); key.append(k)

    if kind == "add1to":
        a = r.randint(14, 58); b = r.randint(11, min(40, 98 - a))
        add("%s has %d %s. Then %s gets %d more %s. How many %s does %s have now?" % (n1, a, xs[0], n1, b, xs[0], xs[0], n1), "%d.%s" % (a + b, ex("%d + %d = ?" % (a, b))))
        a = r.randint(15, 55); b = r.randint(11, min(38, 98 - a)); c = a + b
        add("%s has %d %s. %s gets some more %s. Now %s has %d %s. How many %s did %s get?" % (n2, a, xs[1], n2, xs[1], n2, c, xs[1], xs[1], n2), "%d.%s" % (b, ex("%d + ? = %d" % (a, c))))
        b = r.randint(11, 38); a = r.randint(14, min(55, 98 - b)); c = a + b
        add("%s had some %s. Then %s got %d more %s. Now %s has %d %s. How many %s did %s have at the start?" % (n3, xs[2], n3, b, xs[2], n3, c, xs[2], xs[2], n3), "%d.%s" % (a, ex("? + %d = %d" % (b, c))))
    elif kind == "add1pt":
        a = r.randint(14, 55); b = r.randint(12, min(40, 98 - a))
        add("%s has %d big %s and %d small %s. How many %s does %s have in all?" % (n1, a, xs[0], b, xs[0], xs[0], n1), "%d.%s" % (a + b, ex("%d + %d = ?" % (a, b))))
        a = r.randint(15, 50); b = r.randint(12, min(40, 98 - a)); c = a + b
        add("There are %d %s in all. %d are big. The rest are small. How many are small?" % (c, xs[1], a), "%d.%s" % (b, ex("%d + ? = %d" % (a, c))))
        c = r.randint(30, 90); k = r.randint(12, c - 12)
        add("%s has %d %s. Some are big and the rest are small. How many could be big and how many could be small? Show one way." % (n3, c, xs[2]), "Any two numbers that add to %d, such as %d + %d = %d." % (c, k, c - k, c))
    elif kind == "add1cmp":
        a = r.randint(14, 55); c = r.randint(a + 12, min(98, a + 40))
        add("%s has %d %s. %s has %d %s. How many more %s does %s have than %s?" % (n1, a, xs[0], n2, c, xs[0], xs[0], n2, n1), "%d.%s" % (c - a, ex("%d + ? = %d" % (a, c))))
        a = r.randint(14, 55); b = r.randint(11, min(38, 98 - a))
        add("%s has %d %s. %s has %d more %s than %s. How many %s does %s have?" % (n1, a, xs[1], n2, b, xs[1], n1, xs[1], n2), "%d.%s" % (a + b, ex("%d + %d = ?" % (a, b))))
        a = r.randint(14, 55); b = r.randint(11, min(38, 98 - a))
        add("%s has %d fewer %s than %s. %s has %d %s. How many %s does %s have?" % (n1, b, xs[2], n2, n1, a, xs[2], xs[2], n2), "%d.%s" % (a + b, ex("%d + %d = ?" % (a, b))))
    elif kind == "sub1from":
        a = r.randint(40, 95); b = r.randint(11, min(38, a - 6))
        add("%s has %d %s. %s gives away %d %s. How many %s does %s have left?" % (n1, a, xs[0], n1, b, xs[0], xs[0], n1), "%d.%s" % (a - b, ex("%d - %d = ?" % (a, b))))
        a = r.randint(40, 95); c = r.randint(12, a - 12)
        add("%s has %d %s. %s uses some. Now %s has %d %s left. How many %s did %s use?" % (n2, a, xs[1], n2, n2, c, xs[1], xs[1], n2), "%d.%s" % (a - c, ex("%d - ? = %d" % (a, c))))
        b = r.randint(11, 38); c = r.randint(14, min(58, 98 - b))
        add("%s had some %s. %s gave away %d %s. Now %s has %d %s left. How many %s did %s have at the start?" % (n3, xs[2], n3, b, xs[2], n3, c, xs[2], xs[2], n3), "%d.%s" % (c + b, ex("? - %d = %d" % (b, c))))
    elif kind == "sub1pt":
        c = r.randint(40, 95); a = r.randint(12, c - 12)
        add("There are %d %s in two baskets. %d %s are in the red basket. How many %s are in the blue basket?" % (c, xs[0], a, xs[0], xs[0]), "%d.%s" % (c - a, ex("%d - %d = ?" % (c, a))))
        c = r.randint(40, 95); b = r.randint(12, c - 12)
        add("%s has %d %s in two groups. One group has %d %s. How many %s are in the other group?" % (n1, c, xs[1], b, xs[1], xs[1]), "%d.%s" % (c - b, ex("%d - %d = ?" % (c, b))))
        c = r.randint(30, 90); k = r.randint(12, c - 12)
        add("%s puts %d %s into two boxes. How many could be in each box? Use subtraction to show one way." % (n2, c, xs[2]), "Any pair that works, such as %d - %d = %d (so %d in one box and %d in the other)." % (c, k, c - k, k, c - k))
    elif kind == "sub1cmp":
        c = r.randint(40, 95); a = r.randint(12, c - 12)
        add("%s has %d %s. %s has %d %s. How many fewer %s does %s have than %s?" % (n1, c, xs[0], n2, a, xs[0], xs[0], n2, n1), "%d.%s" % (c - a, ex("%d - %d = ?" % (c, a))))
        c = r.randint(40, 95); b = r.randint(11, min(38, c - 8))
        add("%s has %d more %s than %s. %s has %d %s. How many %s does %s have?" % (n1, b, xs[1], n2, n1, c, xs[1], xs[1], n2), "%d.%s" % (c - b, ex("%d - %d = ?" % (c, b))))
        c = r.randint(40, 95); b = r.randint(11, min(38, c - 8))
        add("%s has %d fewer %s than %s. %s has %d %s. How many %s does %s have?" % (n2, b, xs[2], n1, n1, c, xs[2], xs[2], n2), "%d.%s" % (c - b, ex("%d - %d = ?" % (c, b))))
    elif kind == "add2to":
        a = r.randint(12, 40); b = r.randint(10, 28); d = r.randint(10, min(28, 98 - a - b))
        add("%s has %d %s. In the morning %s gets %d more. In the afternoon %s gets %d more. How many %s does %s have now?" % (n1, a, xs[0], n1, b, n1, d, xs[0], n1), "%d.%s" % (a + b + d, ex("%d + %d + %d = ?" % (a, b, d))))
        a = r.randint(12, 36); b = r.randint(10, 26); d = r.randint(10, 26); t = a + b + d
        add("%s has %d %s. %s gets some more in the morning and %d more in the afternoon. Now %s has %d %s. How many did %s get in the morning?" % (n2, a, xs[1], n2, d, n2, t, xs[1], n2), "%d.%s" % (b, ex("%d + ? + %d = %d" % (a, d, t))))
        a = r.randint(12, 36); b = r.randint(10, 26); d = r.randint(10, 26); t = a + b + d
        add("%s had some %s. %s got %d more in the morning and %d more in the afternoon. Now %s has %d %s. How many %s did %s have at the start?" % (n3, xs[2], n3, b, d, n3, t, xs[2], xs[2], n3), "%d.%s" % (a, ex("? + %d + %d = %d" % (b, d, t))))
    elif kind == "add2pt":
        a = r.randint(12, 36); b = r.randint(12, 30); d = r.randint(12, min(30, 98 - a - b))
        add("%s has %d %s in a red box, %d in a blue box, and %d in a green box. How many %s is that in all?" % (n1, a, xs[0], b, d, xs[0]), "%d.%s" % (a + b + d, ex("%d + %d + %d = ?" % (a, b, d))))
        a = r.randint(12, 34); b = r.randint(12, 30); d = r.randint(12, 30); t = a + b + d
        add("There are %d %s in three boxes. The red box has %d and the blue box has %d. How many %s are in the green box?" % (t, xs[1], a, b, xs[1]), "%d.%s" % (d, ex("%d + %d + ? = %d" % (a, b, t))))
        a = r.randint(12, 34); b = r.randint(12, 30); d = r.randint(12, 30); t = a + b + d
        add("%s has %d %s in three bags. The first bag has %d. The third bag has %d. How many %s are in the second bag?" % (n2, t, xs[2], a, d, xs[2]), "%d.%s" % (b, ex("%d + ? + %d = %d" % (a, d, t))))
    elif kind == "add2cmp":
        a = r.randint(15, 40); b = r.randint(10, 24); d = r.randint(10, min(24, 98 - a - b))
        add("%s has %d %s. %s has %d more than %s. %s has %d more than %s. How many %s does %s have?" % (n1, a, xs[0], n2, b, n1, n3, d, n2, xs[0], n3), "%d.%s" % (a + b + d, ex("%d + %d + %d = ?" % (a, b, d))))
        a = r.randint(15, 40); b = r.randint(8, 20)
        add("%s has %d %s. %s has %d more %s than %s. How many %s do %s and %s have together?" % (n1, a, xs[1], n2, b, xs[1], n1, xs[1], n1, n2), "%d.%s" % (2 * a + b, ex("%d + (%d + %d) = ?" % (a, a, b))))
        a = r.randint(8, 18); b = r.randint(5, 12); d = r.randint(5, 12)
        add("%s has %d %s. %s has %d more %s than %s. %s has %d more %s than %s. How many %s do the three kids have in all?" % (n1, a, xs[2], n2, b, xs[2], n1, n3, d, xs[2], n2, xs[2]), "%d.%s" % (a + (a + b) + (a + b + d), ex("%d + %d + %d = ?" % (a, a + b, a + b + d))))
    elif kind == "sub2from":
        a = r.randint(60, 96); b = r.randint(11, 26); d = r.randint(11, min(26, a - b - 6))
        add("%s has %d %s. %s gives away %d, then gives away %d more. How many %s does %s have left?" % (n1, a, xs[0], n1, b, d, xs[0], n1), "%d.%s" % (a - b - d, ex("%d - %d - %d = ?" % (a, b, d))))
        a = r.randint(60, 96); d = r.randint(11, 26); c = r.randint(12, a - d - 12); b = a - d - c
        add("%s has %d %s. %s gives some away, then gives away %d more. Now %s has %d left. How many did %s give away the first time?" % (n2, a, xs[1], n2, d, n2, c, n2), "%d.%s" % (b, ex("%d - ? - %d = %d" % (a, d, c))))
        b = r.randint(11, 26); d = r.randint(11, 26); c = r.randint(14, min(50, 98 - b - d))
        add("%s had some %s. %s gave away %d, then gave away %d more. Now %s has %d left. How many %s did %s have at the start?" % (n3, xs[2], n3, b, d, n3, c, xs[2], n3), "%d.%s" % (c + b + d, ex("? - %d - %d = %d" % (b, d, c))))
    elif kind == "sub2pt":
        t = r.randint(60, 96); a = r.randint(12, 28); b = r.randint(12, min(28, t - a - 8))
        add("There are %d %s in all. %d are red and %d are blue. The rest are green. How many are green?" % (t, xs[0], a, b), "%d.%s" % (t - a - b, ex("%d - %d - %d = ?" % (t, a, b))))
        t = r.randint(60, 96); a = r.randint(12, 28); b = r.randint(12, min(28, t - a - 8))
        add("%s has %d %s in three baskets. The first basket has %d. The second basket has %d. How many %s are in the third basket?" % (n1, t, xs[1], a, b, xs[1]), "%d.%s" % (t - a - b, ex("%d - %d - %d = ?" % (t, a, b))))
        t = r.randint(60, 96); a = r.randint(12, 28); b = r.randint(12, min(28, t - a - 8))
        add("There are %d %s in all. %d are red. Of the rest, %d are blue and the others are yellow. How many are yellow?" % (t, xs[2], a, b), "%d.%s" % (t - a - b, ex("%d - %d - %d = ?" % (t, a, b))))
    elif kind == "sub2cmp":
        t = r.randint(60, 96); b = r.randint(10, 24); d = r.randint(8, min(24, t - b - 8))
        add("%s has %d %s. %s has %d fewer than %s. %s has %d fewer than %s. How many %s does %s have?" % (n1, t, xs[0], n2, b, n1, n3, d, n2, xs[0], n3), "%d.%s" % (t - b - d, ex("%d - %d - %d = ?" % (t, b, d))))
        t = r.randint(40, 60); b = r.randint(8, 20)
        add("%s has %d %s. %s has %d fewer %s than %s. How many %s do %s and %s have together?" % (n1, t, xs[1], n2, b, xs[1], n1, xs[1], n1, n2), "%d.%s" % (t + t - b, ex("%d + (%d - %d) = ?" % (t, t, b))))
        y = r.randint(30, 50); b = r.randint(10, 24); d = r.randint(8, 24)
        add("%s has %d %s. %s has %d more than %s. %s has %d fewer than %s. How many %s does %s have?" % (n2, y, xs[2], n1, b, n2, n3, d, n1, xs[2], n3), "%d.%s" % (y + b - d, ex("%d + %d - %d = ?" % (y, b, d))))
    return qs, key


def b_oa1(kind):
    def f(lp, r):
        qs, key = oa_set(lp, r, kind)
        return dict(qs=qs, key=key, dir=DIR_EQ, dur=190 if "2" in kind else 150)
    return f


# ------------------------------------------------------------------ OA.C.3 / OA.C.4
def dots_grid(n, col, cols=5):
    body = ""
    rows = (n + cols - 1) // cols
    for k in range(n):
        body += '<circle cx="%d" cy="%d" r="8" fill="%s" stroke="%s" stroke-width="1.5"/>' % (16 + (k % cols) * 22, 16 + (k // cols) * 22, col, INK)
    return svg(12 + cols * 22, 10 + rows * 22, body, "A group of dots")


def b_oddeven(lp, r):
    col = THEME[lp][1]
    ns = r.sample([x for x in range(7, 21)], 3)
    while all(x % 2 == 0 for x in ns) or all(x % 2 == 1 for x in ns):
        ns = r.sample([x for x in range(7, 21)], 3)
    figs = [(L, dots_grid(n, col)) for L, n in zip("ABC", ns)]
    qs = ["Look at group %s. Is the number of dots odd or even? Show me how you know, by pairing them up or counting by 2s." % L for L in "ABC"]
    key = []
    for n in ns:
        if n % 2 == 0:
            key.append("%d is even. The dots make pairs with none left over, or counting by 2s lands on %d." % (n, n))
        else:
            key.append("%d is odd. When the dots make pairs, 1 is left over, or counting by 2s skips %d." % (n, n))
    return dict(qs=qs, key=key, dir="Look at the three groups of dots. Your teacher asks about one at a time. Say odd or even, and show how you know.", dur=130, html=row(figs))


def b_evaneq(lp, r):
    a, b = r.sample([x for x in range(4, 10)], 2)
    x = 2 * r.randint(3, 9); y = 2 * r.randint(2, 10)
    while y == x:
        y = 2 * r.randint(2, 10)
    z = 2 * r.randint(3, 10) + 1
    qs = ["Write an equation that shows %d is even, as the sum of two equal addends." % x,
          "Write an equation that shows %d is even, as the sum of two equal addends." % y,
          "Can you write %d as the sum of two equal addends? What does that tell you about the number?" % z]
    key = ["%d + %d = %d." % (x // 2, x // 2, x), "%d + %d = %d." % (y // 2, y // 2, y),
           "No. There are no two equal addends that make %d, so %d is odd." % (z, z)]
    return dict(qs=qs, key=key, dir="Listen to each question. Write your equation on your paper. Say your answer out loud.", dur=110)


def array_svg(rw, cl, col):
    body = ""
    for i in range(rw):
        for j in range(cl):
            body += '<circle cx="%d" cy="%d" r="8" fill="%s" stroke="%s" stroke-width="1.5"/>' % (16 + j * 22, 16 + i * 22, col, INK)
    return svg(12 + cl * 22, 10 + rw * 22, body, "An array of dots with %d rows and %d columns" % (rw, cl))


def pick_arrays(r):
    dims = []
    while len(dims) < 3:
        d = (r.randint(2, 5), r.randint(2, 5))
        if d not in dims and d[0] != d[1] or (len(dims) == 2 and d not in dims):
            dims.append(d)
    return dims


def b_arrays(lp, r):
    col = THEME[lp][1]
    dims = pick_arrays(r)
    figs = [(L, array_svg(a, b, col)) for L, (a, b) in zip("ABC", dims)]
    qs = ["Look at array %s. Use addition to find how many dots there are in all. Tell me how you added." % L for L in "ABC"]
    key = ["%d dots. For example %s = %d (%d rows of %d)." % (a * b, " + ".join([str(b)] * a), a * b, a, b) for a, b in dims]
    return dict(qs=qs, key=key, dir="Look at the three arrays. Your teacher asks about one at a time. Add to find how many in all.", dur=130, html=row(figs))


def b_arrayeq(lp, r):
    col = THEME[lp][1]
    dims = pick_arrays(r)
    figs = [(L, array_svg(a, b, col)) for L, (a, b) in zip("ABC", dims)]
    qs = ["Look at array %s. Write an equation on your paper that shows the total as a sum of equal addends." % L for L in "ABC"]
    key = ["%s = %d. Adding the rows (%d + ... ) or the columns both work: %s = %d." % (" + ".join([str(b)] * a), a * b, b, " + ".join([str(a)] * b), a * b) for a, b in dims]
    return dict(qs=qs, key=key, dir="Look at the three arrays. Write an equation for each one on your paper. Then tell your teacher about it.", dur=150, html=row(figs))


# ------------------------------------------------------------------ NBT.A.2 counting
def seq(s, step, n):
    return [s + step * i for i in range(n)]


def sq(l):
    return ", ".join(str(x) for x in l) if len(l) <= 12 else ", ".join(str(x) for x in l[:5]) + ", ... , " + ", ".join(str(x) for x in l[-3:])


def b_count1000(lp, r):
    h = r.choice([300, 400, 500, 600, 700, 800, 900])
    s1 = h - r.randint(3, 6); e1 = h + r.randint(4, 8)
    s2 = r.randint(990, 994); e2 = 1000
    s3 = r.randint(121, 780)
    while s3 % 10 > 6 or s3 % 100 > 85:
        s3 = r.randint(121, 780)
    e3 = s3 + r.randint(11, 16)
    qs = ["Count out loud from %d to %d." % (s1, e1), "Count out loud from %d to %d." % (s2, e2), "Count out loud from %d to %d." % (s3, e3)]
    key = ["%s. Watch the turn at %d." % (sq(seq(s1, 1, e1 - s1 + 1)), h), "%s. Watch the turn to 1000." % sq(seq(s2, 1, e2 - s2 + 1)), "%s." % sq(seq(s3, 1, e3 - s3 + 1))]
    return dict(qs=qs, key=key, dir="Listen to each question. Count out loud.", dur=100)


def b_skip(step):
    def f(lp, r):
        specs = []
        if step == 2:
            s1 = 2 * r.randint(5, 20); specs = [(s1, 8), (2 * r.randint(8, 30) + 1, 8)]
            h = r.choice([200, 300, 400, 500, 600]); specs.append((h - 6, 7))
        elif step == 5:
            specs = [(5 * r.randint(3, 12), 9), (5 * r.randint(16, 19), 9), (5 * r.randint(96, 100), 8)]
        elif step == 10:
            specs = [(10 * r.randint(2, 7), 8), (r.randint(2, 9) * 10 + r.randint(1, 9), 7), (10 * r.randint(20, 80), 8)]
        else:
            specs = [(100, 6), (100 * r.randint(2, 4), 6), (r.randint(1, 3) * 100 + r.randint(11, 98), 6)]
        qs, key = [], []
        for s, n in specs:
            l = seq(s, step, n)
            assert l[-1] <= 1000, (step, s, n)
            qs.append("Count by %ds out loud. Start at %d and say %d numbers." % (step, s, n))
            key.append("%s." % sq(l))
        return dict(qs=qs, key=key, dir="Listen to each question. Skip-count out loud.", dur=100)
    return f


# ------------------------------------------------------------------ NBT.A.3 read and write numbers
def words3(n):
    if n == 1000:
        return "one thousand"
    h, rest = divmod(n, 100)
    out = []
    if h:
        out.append(N.ONES[h] + " hundred")
    if rest:
        out.append(N.words(rest))
    return " ".join(out)


def exp_form(n):
    parts = [("%d" % (d * 10 ** (len(str(n)) - 1 - i))) for i, d in enumerate(int(c) for c in str(n)) if d]
    return " + ".join(parts)


def pick3(r):
    a = r.choice([x for x in range(101, 1000) if x % 100 != 0 and x % 10 != 0 and (x // 10) % 10 not in (0,)])
    b = 100 * r.randint(1, 9) + r.randint(1, 9)
    c = 100 * r.randint(1, 9) + 10 * r.randint(1, 9)
    ns = [a, b, c]
    r.shuffle(ns)
    return ns


def box_fig(vals):
    return '<div style="display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin:10px 0">%s</div>' % "".join(
        '<div style="border:3px solid %s;border-radius:14px;background:#fffaf0;padding:8px 20px;text-align:center"><div class="small" style="font-weight:700">%s</div><div style="font-size:%s;font-weight:800;color:%s">%s</div></div>' % (INK, L, "2.2rem" if len(v) < 8 else "1.4rem", INK, v) for L, v in zip("ABC", vals))


def b_readnum(lp, r):
    ns = pick3(r)
    qs = ["Read the number in box %s out loud." % L for L in "ABC"]
    key = ["%s: %s." % (L, words3(n)) for L, n in zip("ABC", ns)]
    return dict(qs=qs, key=key, dir="Look at the three boxes. Your teacher asks about one at a time. Read the number out loud.", dur=90, html=box_fig([str(n) for n in ns]))


def b_readname(lp, r):
    ns = pick3(r)
    qs = ["Read the number name in box %s. Tell me the number with digits." % L for L in "ABC"]
    key = ["%s: %d." % (L, n) for L, n in zip("ABC", ns)]
    return dict(qs=qs, key=key, dir="Look at the three boxes. Your teacher asks about one at a time. Read the number name and say the digits.", dur=100, html=box_fig([words3(n) for n in ns]))


def b_readexp(lp, r):
    ns = pick3(r)
    qs = ["Read the expanded form in box %s. Say the whole number." % L for L in "ABC"]
    key = ["%s: %s (%d)." % (L, words3(n), n) for L, n in zip("ABC", ns)]
    return dict(qs=qs, key=key, dir="Look at the three boxes. Your teacher asks about one at a time. Read the expanded form and say the whole number.", dur=100, html=box_fig([exp_form(n) for n in ns]))


def b_writenum(lp, r):
    ns = pick3(r)
    qs = ["Write this number with digits on your paper: %s." % words3(n) for n in ns]
    key = ["%d." % n for n in ns]
    return dict(qs=qs, key=key, dir="Listen to each number. Write it with digits on your paper.", dur=90)


def b_writename(lp, r):
    ns = pick3(r)
    qs = ["Write the number name for %d on your paper." % n for n in ns]
    key = ["%s. Check that the hundreds, tens, and ones words are in the right order." % words3(n) for n in ns]
    return dict(qs=qs, key=key, dir="Listen to each number. Write the number name with words on your paper.", dur=130)


def b_writeexp(lp, r):
    ns = pick3(r)
    qs = ["Write %d in expanded form on your paper." % n for n in ns]
    key = ["%s." % exp_form(n) for n in ns]
    return dict(qs=qs, key=key, dir="Listen to each number. Write it in expanded form on your paper.", dur=110)


# ------------------------------------------------------------------ NBT.B.7
def dg(n):
    return n // 100, (n // 10) % 10, n % 10


def pick_add3(r, kind):
    for _ in range(500):
        a = r.randint(101, 899); b = r.randint(101, 899)
        ah, at, ao = dg(a); bh, bt, bo = dg(b)
        c1 = ao + bo >= 10
        c2 = at + bt + (1 if c1 else 0) >= 10
        if a + b > 999:
            continue
        ok = {"nc": not c1 and not c2, "c1": c1 and not c2, "c2": c2 and not c1, "c12": c1 and c2}[kind]
        if ok:
            return a, b
    raise RuntimeError(kind)


def pick_sub3(r, kind):
    for _ in range(800):
        a = r.randint(201, 999); b = r.randint(101, a - 60)
        ah, at, ao = dg(a); bh, bt, bo = dg(b)
        d1 = ao < bo
        d2 = at - (1 if d1 else 0) < bt
        if kind == "d0":
            if not (at == 0 and d1):
                continue
            return a, b
        ok = {"nd": not d1 and not d2, "d1": d1 and not d2, "d2": d2 and not d1, "d12": d1 and d2}[kind]
        if ok:
            return a, b
    raise RuntimeError(kind)


def add_note(a, b):
    ah, at, ao = dg(a); bh, bt, bo = dg(b)
    notes = []
    if ao + bo >= 10:
        notes.append("the ones make a new ten")
    if at + bt + (1 if ao + bo >= 10 else 0) >= 10:
        notes.append("the tens make a new hundred")
    return notes


def sub_note(a, b):
    ah, at, ao = dg(a); bh, bt, bo = dg(b)
    notes = []
    d1 = ao < bo
    if d1:
        notes.append("a ten is broken into 10 ones")
    if at - (1 if d1 else 0) < bt:
        notes.append("a hundred is broken into 10 tens")
    return notes


def tail(notes):
    return (" Look for: " + " and ".join(notes) + ".") if notes else ""


def b_addm(lp, r):
    ps = [pick_add3(r, k) for k in ("nc", "c1", "c2")]
    qs = ["Draw hundreds, tens, and ones to show %d + %d. How many in all?" % p for p in ps]
    key = ["%d (%d + %d = %d). Look for the drawing to show %d hundreds, %d tens, and %d ones.%s" % (a + b, a, b, a + b, (a + b) // 100, (a + b) // 10 % 10, (a + b) % 10, ((" The drawing shows " + " and ".join(add_note(a, b)) + ".") if add_note(a, b) else "")) for a, b in ps]
    return dict(qs=qs, key=key, dir="Listen to each question. Draw hundreds, tens, and ones on your paper. Say your answer out loud.", dur=180)


def b_adds(lp, r):
    ps = [pick_add3(r, k) for k in ("nc", "c1", "c12")]
    qs = ["Solve %d + %d. Use a strategy and tell me what you did." % p for p in ps]
    key = ["%d (%d + %d = %d). Any strategy that works counts, such as adding the hundreds, tens, and ones, or counting on in chunks.%s" % (a + b, a, b, a + b, tail(add_note(a, b))) for a, b in ps]
    return dict(qs=qs, key=key, dir="Listen to each question. Solve it any way you like. Then tell your teacher what you did.", dur=160)


def b_subm(lp, r):
    ps = [pick_sub3(r, k) for k in ("nd", "d1", "d2")]
    qs = ["Draw hundreds, tens, and ones to show %d - %d. How many are left?" % p for p in ps]
    key = ["%d (%d - %d = %d). Look for a drawing that starts with %d and crosses out %d.%s" % (a - b, a, b, a - b, a, b, tail(sub_note(a, b))) for a, b in ps]
    return dict(qs=qs, key=key, dir="Listen to each question. Draw hundreds, tens, and ones on your paper. Say your answer out loud.", dur=180)


def b_subs(lp, r):
    ps = [pick_sub3(r, k) for k in ("nd", "d1", "d12")]
    qs = ["Solve %d - %d. Use a strategy and tell me what you did." % p for p in ps]
    key = ["%d (%d - %d = %d). Any strategy that works counts, such as subtracting the hundreds, tens, and ones, counting up from %d, or using %d + %d = %d.%s" % (a - b, a, b, a - b, b, b, a - b, a, tail(sub_note(a, b))) for a, b in ps]
    return dict(qs=qs, key=key, dir="Listen to each question. Solve it any way you like. Then tell your teacher what you did.", dur=160)


def b_writtenadd(lp, r):
    ps = [pick_add3(r, k) for k in ("c1", "c2", "nc")]
    r.shuffle(ps)
    qs = ["Solve %d + %d. Write the equation or the written method on your paper that matches how you added." % p for p in ps]
    key = ["%d (%d + %d = %d). Look for a written method that matches the strategy, such as %d + %d = %d, then %d + %d = %d, or the standard way with the digits lined up.%s" % (a + b, a, b, a + b, a, b // 100 * 100, a + b // 100 * 100, a + b // 100 * 100, b % 100, a + b, tail(add_note(a, b))) for a, b in ps]
    return dict(qs=qs, key=key, dir="Listen to each question. Solve it, then write the method on your paper. Tell your teacher how it matches what you did.", dur=190)


def b_writtensub(lp, r):
    ps = [pick_sub3(r, k) for k in ("d1", "d2", "nd")]
    r.shuffle(ps)
    qs = ["Solve %d - %d. Write the equation or the written method on your paper that matches how you subtracted." % p for p in ps]
    key = ["%d (%d - %d = %d). Look for a written method that matches the strategy, such as %d - %d = %d, then %d - %d = %d, or the standard way with the digits lined up.%s" % (a - b, a, b, a - b, a, b // 100 * 100, a - b // 100 * 100, a - b // 100 * 100, b % 100, a - b, tail(sub_note(a, b))) for a, b in ps]
    return dict(qs=qs, key=key, dir="Listen to each question. Solve it, then write the method on your paper. Tell your teacher how it matches what you did.", dur=190)


def b_hto(lp, r):
    a1, b1 = pick_add3(r, "nc")
    a2, b2 = pick_sub3(r, "nd")
    a3, b3 = pick_add3(r, "c1")
    qs = ["In %d + %d, which digits do you add to each other? Tell me what you add to the hundreds, to the tens, and to the ones." % (a1, b1),
          "In %d - %d, which digits do you subtract from each other? Tell me what you subtract in the hundreds, the tens, and the ones." % (a2, b2),
          "In %d + %d, which digits do you add to each other? Tell me what you add to the hundreds, to the tens, and to the ones." % (a3, b3)]
    (h1, t1, o1), (g1, u1, p1) = dg(a1), dg(b1)
    (h2, t2, o2), (g2, u2, p2) = dg(a2), dg(b2)
    (h3, t3, o3), (g3, u3, p3) = dg(a3), dg(b3)
    key = ["Hundreds with hundreds (%d + %d), tens with tens (%d + %d), ones with ones (%d + %d). Answer %d." % (h1, g1, t1, u1, o1, p1, a1 + b1),
           "Hundreds from hundreds (%d - %d), tens from tens (%d - %d), ones from ones (%d - %d). Answer %d." % (h2, g2, t2, u2, o2, p2, a2 - b2),
           "Hundreds with hundreds (%d + %d), tens with tens (%d + %d), ones with ones (%d + %d). The ones make a new ten. Answer %d." % (h3, g3, t3, u3, o3, p3, a3 + b3)]
    return dict(qs=qs, key=key, dir="Listen to each question. You can draw hundreds, tens, and ones. Say your answer out loud.", dur=150)


def b_compose(lp, r):
    a1, b1 = pick_add3(r, "c1")
    a2, b2 = pick_add3(r, "nc")
    a3, b3 = pick_sub3(r, "d1")
    a4, b4 = pick_sub3(r, "d0")
    plan = [("add", a1, b1), ("add", a2, b2), ("sub", a3, b3)] if lp % 2 else [("sub", a3, b3), ("add", a1, b1), ("add", a2, b2)]
    if lp % 3 == 0:
        plan[2] = ("sub", a4, b4)
    qs, key = [], []
    for op, a, b in plan:
        if op == "add":
            qs.append("Do you need to make a new ten or a new hundred when you add %d + %d? How do you know?" % (a, b))
            n = add_note(a, b)
            key.append("%s. The answer is %d." % (("Yes: " + " and ".join(n)) if n else "No. The ones and the tens each make less than 10 in their place", a + b))
        else:
            qs.append("Do you need to break apart a ten or a hundred when you subtract %d - %d? How do you know?" % (a, b))
            n = sub_note(a, b)
            key.append("%s. The answer is %d." % (("Yes: " + " and ".join(n)) if n else "No. Every digit on top is at least as big as the digit below it", a - b))
    return dict(qs=qs, key=key, dir="Listen to each question. You can draw hundreds, tens, and ones. Say your answer out loud.", dur=150)


# ------------------------------------------------------------------ MD.A.1
def ruler_svg(start, end, units=10, bad_zero=False):
    u = 40
    x0 = 20
    w = units * u + 40
    body = '<rect x="%d" y="8" width="%d" height="18" rx="5" fill="#f3e3b3" stroke="%s" stroke-width="2"/>' % (x0 + start * u, (end - start) * u, INK)
    body += '<rect x="%d" y="38" width="%d" height="38" fill="#fffaf0" stroke="%s" stroke-width="2"/>' % (x0, units * u, INK)
    for i in range(units + 1):
        body += '<line x1="%d" y1="38" x2="%d" y2="58" stroke="%s" stroke-width="2"/>' % (x0 + i * u, x0 + i * u, INK)
        if i < units:
            body += '<line x1="%d" y1="38" x2="%d" y2="48" stroke="%s" stroke-width="1.2"/>' % (x0 + i * u + u // 2, x0 + i * u + u // 2, INK)
        body += '<text x="%d" y="72" font-size="13" text-anchor="middle" fill="%s" font-family="sans-serif">%d</text>' % (x0 + i * u, INK, i)
    body += '<text x="%d" y="96" font-size="12" text-anchor="middle" fill="%s" font-family="sans-serif">inches</text>' % (x0 + units * u // 2, INK)
    return svg(w, 102, body, "An object above a ruler marked in inches")


def b_measure(lp, r):
    things = r.sample(["pencil", "ribbon", "crayon", "stick", "paper strip", "leaf", "key"], 3)
    ns = r.sample(range(3, 10), 3)
    figs = [(L + ": " + t, ruler_svg(0, n)) for L, t, n in zip("ABC", things, ns)]
    qs = ["How long is the %s in picture %s? Say the length with the unit." % (t, L) for L, t in zip("ABC", things)]
    key = ["%d inches. The left end of the %s is at 0 and the right end is at %d." % (n, t, n) for n, t in zip(ns, things)]
    return dict(qs=qs, key=key, dir="Look at the three pictures. Your teacher asks about one at a time. Say how long each object is.", dur=110, html=row(figs))


TOOLS = [("the length of a pencil", "a ruler"), ("the length of a crayon", "a ruler"), ("the width of a classroom door", "a yardstick or a meter stick"),
         ("the height of a table", "a yardstick or a meter stick"), ("the length of a hallway", "a measuring tape"), ("how far around a pumpkin", "a measuring tape"),
         ("how far you can jump", "a measuring tape or a meter stick"), ("the length of a playground", "a measuring tape"),
         ("the length of a paper clip", "a ruler"), ("the height of a bookshelf", "a yardstick or a meter stick")]


def b_selecttool(lp, r):
    items = r.sample(TOOLS, 3)
    qs = ["Which tool would you pick to measure %s: a ruler, a yardstick, a meter stick, or a measuring tape? Why?" % o for o, t in items]
    key = ["%s. It fits the size of what is being measured. A longer object needs a longer tool or one that can bend." % t.capitalize() for o, t in items]
    return dict(qs=qs, key=key, dir="Listen to each question. Pick the tool you would use and tell your teacher why.", dur=100)


def b_usetool(lp, r):
    things = r.sample(["pencil", "ribbon", "crayon", "stick", "paper strip", "leaf"], 3)
    n1 = r.randint(3, 8)
    s2 = r.randint(1, 3); e2 = s2 + r.randint(3, 6)
    s3 = r.randint(1, 2); e3 = s3 + r.randint(3, 6)
    figs = [("A: " + things[0], ruler_svg(0, n1)), ("B: " + things[1], ruler_svg(s2, e2)), ("C: " + things[2], ruler_svg(s3, e3))]
    qs = ["The %s in picture A is on the ruler. Show me where you start and where you stop, and tell me how long it is." % things[0],
          "The %s in picture B starts at %d, not at 0. How long is it? Tell me how you figured it out." % (things[1], s2),
          "The %s in picture C does not start at 0. What is the length? What is the best way to place it on the ruler?" % things[2]]
    key = ["%d inches. Start at 0, stop at %d." % (n1, n1),
           "%d inches. Count the inches from %d to %d, or subtract %d - %d." % (e2 - s2, s2, e2, e2, s2),
           "%d inches (count from %d to %d). Best way: line the left end up with the 0 mark." % (e3 - s3, s3, e3)]
    return dict(qs=qs, key=key, dir="Look at the three pictures. Your teacher asks about one at a time. Tell how you use the ruler.", dur=150, html=row(figs))


# ------------------------------------------------------------------ MD.C.7
def clock_m(h, m):
    cx = cy = 60
    body = '<circle cx="60" cy="60" r="54" fill="#fffaf0" stroke="%s" stroke-width="3"/>' % INK
    for k in range(1, 13):
        a = math.radians(k * 30)
        body += '<text x="%.1f" y="%.1f" font-size="12" font-weight="700" text-anchor="middle" fill="%s" font-family="sans-serif">%d</text>' % (cx + 41 * math.sin(a), cy - 41 * math.cos(a) + 4, INK, k)
    for k in range(60):
        a = math.radians(k * 6)
        L = 5 if k % 5 == 0 else 2.5
        body += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (cx + (54 - L) * math.sin(a), cy - (54 - L) * math.cos(a), cx + 54 * math.sin(a), cy - 54 * math.cos(a), INK)
    ha = math.radians(((h % 12) + m / 60.0) * 30)
    ma = math.radians(m * 6)
    body += '<line x1="60" y1="60" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (cx + 24 * math.sin(ha), cy - 24 * math.cos(ha), INK)
    body += '<line x1="60" y1="60" x2="%.1f" y2="%.1f" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/>' % (cx + 36 * math.sin(ma), cy - 36 * math.cos(ma))
    body += '<circle cx="60" cy="60" r="4" fill="%s"/>' % INK
    return svg(120, 120, body, "An analog clock")


def digital_m(h, m, ap=None):
    t = "%d:%02d" % (h, m)
    body = '<rect x="4" y="4" width="112" height="52" rx="10" fill="#2b2b2b" stroke="%s" stroke-width="3"/>' % INK
    body += '<text x="60" y="42" font-size="30" font-weight="700" text-anchor="middle" fill="#9ef0a0" font-family="monospace">%s</text>' % t
    return svg(120, 60, body, "A digital clock")


def times(r, n=3):
    hs = r.sample(range(1, 13), n)
    ms = [r.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]) for _ in range(n)]
    return list(zip(hs, ms))


def tsay(h, m):
    return "%d:%02d (%s)" % (h, m, "half past %d" % h if m == 30 else "quarter past %d" % h if m == 15 else "quarter to %d" % (h % 12 + 1) if m == 45 else "%d minutes after %d" % (m, h))


def b_time(kind, mode):
    def f(lp, r):
        ts = times(r)
        mk = clock_m if kind == "an" else digital_m
        figs = [(L, mk(h, m)) for L, (h, m) in zip("ABC", ts)]
        if mode == "tell":
            qs = ["What time does clock %s show? Say the time out loud." % L for L in "ABC"]
            if kind == "an":
                key = ["%s. The short hand is at or just past %d. The long hand points to %d, which is %d minutes." % (tsay(h, m), h, m // 5 or 12, m) if m else tsay(h, m) for h, m in ts]
            else:
                key = ["%s. The display reads %d:%02d." % (tsay(h, m), h, m) for h, m in ts]
            d = "Look at the three clocks. Your teacher asks about one at a time. Say the time out loud."
        else:
            qs = ["Write the time clock %s shows on your paper." % L for L in "ABC"]
            key = ["%d:%02d. Look for the hour, a colon, then two digits for the minutes." % (h, m) for h, m in ts]
            d = "Look at the three clocks. Write the time each one shows on your paper, with a colon."
        return dict(qs=qs, key=key, dir=d, dur=110, html=row(figs))
    return f


def b_write_dg(lp, r):
    ts = times(r)
    # teacher says a time, student writes it the way a digital clock shows it
    def say(h, m):
        if m == 30:
            return "half past %s" % N.ONES[h]
        if m == 15:
            return "quarter past %s" % N.ONES[h]
        if m == 45:
            return "quarter to %s" % N.ONES[h % 12 + 1]
        return "%s minutes after %s" % (N.words(m), N.ONES[h])
    figs = [(L, digital_m(h, m)) for L, (h, m) in zip("ABC", ts)]
    qs = ["Look at clock %s. Write the time in words on your paper, such as half past or minutes after." % L for L in "ABC"]
    key = ["%s. The display reads %d:%02d." % (say(h, m), h, m) for h, m in ts]
    return dict(qs=qs, key=key, dir="Look at the three digital clocks. Write each time in words on your paper.", dur=120, html=row(figs))


AMPM = [("wakes up for school", "a.m.", (6, 8)), ("eats breakfast", "a.m.", (6, 8)), ("has recess in the morning", "a.m.", (9, 10)),
        ("eats lunch", "p.m.", (12, 1)), ("gets home from school", "p.m.", (2, 4)), ("eats dinner", "p.m.", (5, 7)), ("goes to bed", "p.m.", (7, 9)),
        ("watches the sunrise", "a.m.", (5, 7)), ("plays outside after school", "p.m.", (3, 5))]


def ampm_set(lp, r):
    acts = r.sample(AMPM, 3)
    out = []
    for act, ap, (lo, hi) in acts:
        if lo > hi:
            h = r.choice([12, 1])
        else:
            h = r.randint(lo, hi)
        m = r.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        out.append((act, ap, h, m))
    return out


def b_tell_ampm(lp, r):
    st = ampm_set(lp, r)
    nme = nm(lp, 0)
    qs, key = [], []
    figs = []
    for L, (act, ap, h, m) in zip("ABC", st):
        figs.append((L, digital_m(h, m)))
        qs.append("Clock %s shows when %s %s. Tell the time with a.m. or p.m." % (L, nme, act))
        key.append("%d:%02d %s (%s)." % (h, m, ap, "morning" if ap == "a.m." else "afternoon or evening"))
    return dict(qs=qs, key=key, dir="Look at the three clocks. Your teacher asks about one at a time. Tell the time and say a.m. or p.m.", dur=120, html=row(figs))


def b_write_ampm(lp, r):
    st = ampm_set(lp, r)
    nme = nm(lp, 1)
    figs, qs, key = [], [], []
    for L, (act, ap, h, m) in zip("ABC", st):
        figs.append((L, clock_m(h, m)))
        qs.append("Clock %s shows when %s %s. Write the time on your paper with a.m. or p.m." % (L, nme, act))
        key.append("%d:%02d %s" % (h, m, ap))
    return dict(qs=qs, key=key, dir="Look at the three clocks. Write each time on your paper with a.m. or p.m.", dur=130, html=row(figs))


REL = [("How many minutes are in one hour?", "60 minutes."), ("How many hours are in one day?", "24 hours."), ("How many days are in one week?", "7 days."),
       ("About how many days are in one month?", "About 30 days. A month has 28, 29, 30, or 31 days."), ("How many weeks are in one year?", "52 weeks."),
       ("How many months are in one year?", "12 months."), ("How many minutes are in half an hour?", "30 minutes."), ("How many days are in one year?", "365 days (366 in a leap year).")]


def b_relations(lp, r):
    base = [(lp + i) % len(REL) for i in range(3)]
    items = [REL[i] for i in [base[0], (base[1] + 3) % len(REL), (base[2] + 5) % len(REL)]]
    seen, out = set(), []
    for q, k in items:
        if q not in seen:
            seen.add(q); out.append((q, k))
    for q, k in REL:
        if len(out) >= 3:
            break
        if q not in seen:
            seen.add(q); out.append((q, k))
    return dict(qs=[q for q, k in out], key=[k for q, k in out], dir="Listen to each question. Say your answer out loud.", dur=70)


# ------------------------------------------------------------------ MD.C.8
pl = lambda n, one, many: "%d %s" % (n, one if n == 1 else many)


def money_amt(r, qn, dm, nk, pn):
    return qn * 25 + dm * 10 + nk * 5 + pn


def cents(v):
    return "%d%s" % (v, "¢")


def dollars(v):
    return "$%d.%02d" % (v // 100, v % 100)


def b_moneyprob(lp, r):
    nme1, nme2, nme3 = names(lp)
    d, p = r.randint(2, 6), r.randint(1, 4)
    v1 = d * 10 + p
    q, n = r.randint(1, 3), r.randint(1, 3)
    v2 = q * 25 + n * 5
    price = r.choice([45, 55, 60, 65, 70, 85])
    q3, d3, n3 = r.randint(1, 3), r.randint(1, 3), r.randint(0, 1)
    have = q3 * 25 + d3 * 10 + n3 * 5
    while have == price:
        d3 += 1
        have = q3 * 25 + d3 * 10 + n3 * 5
    held = ", ".join([pl(q3, "quarter", "quarters"), pl(d3, "dime", "dimes")] + ([pl(n3, "nickel", "nickels")] if n3 else []))
    qs = ["%s has %s and %s. How many cents does %s have?" % (nme1, pl(d, "dime", "dimes"), pl(p, "penny", "pennies"), nme1),
          "%s has %s and %s. How many cents does %s have in all?" % (nme2, pl(q, "quarter", "quarters"), pl(n, "nickel", "nickels"), nme2),
          "A sticker costs %d cents. %s has %s. Does %s have enough money? How much more or how much extra?" % (price, nme3, held, nme3)]
    if have >= price:
        k3 = "%d cents. Yes, enough, with %d cents extra (%d - %d = %d)." % (have, have - price, have, price, have - price)
    else:
        k3 = "%d cents. Not enough, %d cents more is needed (%d - %d = %d)." % (have, price - have, price, have, price - have)
    key = ["%d cents (%d + %d = %d)." % (v1, d * 10, p, v1), "%d cents (%d + %d = %d)." % (v2, q * 25, n * 5, v2), k3]
    return dict(qs=qs, key=key, dir="Listen to each problem. Solve it on your paper. You can draw coins. Say your answer out loud.", dur=160)


def b_symbols(lp, r):
    nme = nm(lp, 2)
    d, p = r.randint(2, 7), r.randint(1, 4)
    v1 = d * 10 + p
    b, q = r.randint(1, 4), r.randint(1, 3)
    v2 = b * 100 + q * 25
    v3 = r.choice([135, 150, 175, 205, 240, 260])
    qs = ["Write the amount of %s and %s on your paper. Use the cent symbol." % (pl(d, "dime", "dimes"), pl(p, "penny", "pennies")),
          "%s has %s and %s. Write the amount on your paper. Use the dollar sign." % (nme, pl(b, "dollar bill", "dollar bills"), pl(q, "quarter", "quarters")),
          "Write %d cents using the dollar sign." % v3]
    key = ["%s." % cents(v1), "%s." % dollars(v2), "%s. Look for the dollar sign in front and a decimal point before the last two digits." % dollars(v3)]
    return dict(qs=qs, key=key, dir="Listen to each question. Write the amount on your paper with the right symbol.", dur=110)


# ------------------------------------------------------------------ MD.D.10 graphs
DS4 = [("Favorite pets", ["cats", "dogs", "fish", "birds"]), ("Favorite fruit", ["apples", "bananas", "grapes", "oranges"]),
       ("Favorite snack", ["crackers", "cheese", "carrots", "popcorn"]), ("Weather this week", ["sunny", "rainy", "cloudy", "windy"]),
       ("Favorite color", ["red", "blue", "green", "yellow"]), ("Favorite playground toy", ["swings", "slide", "sandbox", "seesaw"]),
       ("Favorite book", ["animals", "space", "trucks", "dinosaurs"]), ("Favorite season", ["summer", "winter", "spring", "fall"])]


def counts4(r, k=4, lo=1, hi=9, tot=24):
    while True:
        c = [r.randint(lo, hi) for _ in range(k)]
        if len(set(c)) == k and sum(c) <= tot:
            return c


def b_draw_graph(kind):
    def f(lp, r):
        sets = r.sample(DS4, 3)
        qs, key = [], []
        for i, (title, cats) in enumerate(sets):
            k = 4 if i != 1 else 3
            cs = cats[:k]
            cts = counts4(r, k, 1, 7, 18)
            lst = [c for c, n in zip(cs, cts) for _ in range(n)]
            r.shuffle(lst)
            what = "a picture graph" if kind == "pic" else "a bar graph"
            qs.append("%s. Here are the answers: %s. Draw %s on your paper to show the data." % (title, ", ".join(lst), what))
            if kind == "pic":
                look = "a title, %d labeled rows or columns, one picture or symbol for each answer, and the right number in each" % k
            else:
                look = "a title, %d labeled bars, bars that go up one square for each answer, and the right height for each" % k
            key.append("%s. Look for %s." % (", ".join("%s %d" % (c, n) for c, n in zip(cs, cts)), look))
        d = "Listen to each set of answers. Draw the graph on your paper. Use one picture or one square for each answer."
        return dict(qs=qs, key=key, dir=d, dur=240)
    return f


def graphs4(lp, r):
    sets = r.sample(DS4, 3)
    col = THEME[lp][1]
    out = []
    for title, cats in sets:
        cts = counts4(r, 4, 1, 9, 24)
        out.append((title, cats, cts))
    figs = [(L, bar_fig(t, c, n, col)) for L, (t, c, n) in zip("ABC", out)]
    return out, row(figs)


def b_putogether(lp, r):
    g, h = graphs4(lp, r)
    qs, key = [], []
    for L, (t, c, n) in zip("ABC", g):
        i, j = r.sample(range(4), 2)
        qs.append("Look at graph %s. How many chose %s and %s in all?" % (L, c[i], c[j]))
        key.append("%d (%d + %d = %d)." % (n[i] + n[j], n[i], n[j], n[i] + n[j]))
    return dict(qs=qs, key=key, dir="Look at the three graphs. Your teacher asks about one at a time. Solve the problem out loud.", dur=140, html=h)


def b_takeapart(lp, r):
    g, h = graphs4(lp, r)
    qs, key = [], []
    for L, (t, c, n) in zip("ABC", g):
        i = r.randrange(4)
        tot = sum(n)
        qs.append("Look at graph %s. There are %d answers in all. How many did NOT choose %s?" % (L, tot, c[i]))
        key.append("%d (%d - %d = %d)." % (tot - n[i], tot, n[i], tot - n[i]))
    return dict(qs=qs, key=key, dir="Look at the three graphs. Your teacher asks about one at a time. Solve the problem out loud.", dur=140, html=h)


def b_compare(lp, r):
    g, h = graphs4(lp, r)
    qs, key = [], []
    for k, (L, (t, c, n)) in enumerate(zip("ABC", g)):
        i, j = r.sample(range(4), 2)
        hi, lo = (i, j) if n[i] > n[j] else (j, i)
        if k == 1:
            qs.append("Look at graph %s. How many fewer chose %s than %s?" % (L, c[lo], c[hi]))
        else:
            qs.append("Look at graph %s. How many more chose %s than %s?" % (L, c[hi], c[lo]))
        key.append("%d (%d - %d = %d)." % (n[hi] - n[lo], n[hi], n[lo], n[hi] - n[lo]))
    return dict(qs=qs, key=key, dir="Look at the three graphs. Your teacher asks about one at a time. Solve the problem out loud.", dur=140, html=h)


# ------------------------------------------------------------------ G.A.1 shapes
def poly_pts(n, cx, cy, rad, rot, r, jitter):
    pts = []
    for i in range(n):
        a = math.radians(rot + i * 360.0 / n)
        rr = rad * (1 + (r.uniform(-jitter, jitter)))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def poly_svg(n, r, col="#fffaf0"):
    if n == 4 and r.random() < 0.6:
        w, h = r.choice([(54, 54), (66, 40), (40, 66)])
        pts = [(50 - w / 2, 50 - h / 2), (50 + w / 2, 50 - h / 2), (50 + w / 2, 50 + h / 2), (50 - w / 2, 50 + h / 2)]
    else:
        pts = poly_pts(n, 50, 50, 36, r.randint(0, 359), r, 0.18 if n != 4 else 0.12)
    d = " ".join("%.1f,%.1f" % p for p in pts)
    return svg(100, 100, '<polygon points="%s" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (d, col, INK), "A shape with %d sides" % n)


def cube_svg():
    body = '<rect x="18" y="34" width="46" height="46" fill="#fffaf0" stroke="%s" stroke-width="3"/>' % INK
    body += '<polygon points="18,34 36,16 82,16 64,34" fill="#f3e3b3" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % INK
    body += '<polygon points="64,34 82,16 82,62 64,80" fill="#e6d3a0" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % INK
    return svg(100, 100, body, "A cube")


SHAPES = [("triangle", 3), ("quadrilateral", 4), ("pentagon", 5), ("hexagon", 6), ("cube", 0)]


def shape_set(r, k=5):
    sel = SHAPES[:] if k == 5 else r.sample(SHAPES, k)
    r.shuffle(sel)
    figs = []
    for L, (nme, n) in zip(LET, sel):
        figs.append((L, cube_svg() if nme == "cube" else poly_svg(n, r)))
    return sel, row(figs)


def b_g_recognize(lp, r):
    sel, h = shape_set(r)
    letter = {nme: L for L, (nme, n) in zip(LET, sel)}
    attrs = [("has exactly 3 angles", "triangle"), ("has exactly 4 angles", "quadrilateral"), ("has exactly 5 angles", "pentagon"), ("has exactly 6 angles", "hexagon"), ("has 6 equal square faces", "cube")]
    picks = r.sample(attrs, 3)
    qs = ["Which shape %s?" % a for a, s in picks]
    key = ["Shape %s, the %s." % (letter[s], s) for a, s in picks]
    return dict(qs=qs, key=key, dir="Look at the five shapes. Your teacher asks about one at a time. Point to the shape and say its letter.", dur=110, html=h)


def b_g_draw(lp, r):
    asks = [("a shape that has exactly 3 angles", "A triangle: 3 sides and 3 angles."), ("a shape that has exactly 4 angles", "A quadrilateral: 4 sides and 4 angles. Rectangle, square, or any four-sided shape works."),
            ("a shape that has exactly 5 angles", "A pentagon: 5 sides and 5 angles."), ("a shape that has exactly 6 angles", "A hexagon: 6 sides and 6 angles."),
            ("one face of a cube. Tell how many of these faces a cube has", "A square. A cube has 6 equal square faces.")]
    picks = r.sample(asks, 3)
    qs = ["Draw %s on your paper. Tell me the name of your shape if you can." % a for a, k in picks]
    key = ["%s Look for straight sides that meet at corners and a closed shape." % k for a, k in picks]
    return dict(qs=qs, key=key, dir="Listen to each question. Draw the shape on your paper with a pencil. Then tell your teacher about it.", dur=150)


def b_g_identify(lp, r):
    sel, h = shape_set(r)
    qs = ["What is the name of shape %s?" % L for L in LET[:5]]
    qs = qs[:3]
    # choose 3 shapes to ask about
    idx = r.sample(range(5), 3)
    qs = ["What is the name of shape %s?" % LET[i] for i in idx]
    key = []
    for i in idx:
        nme, n = sel[i]
        key.append("%s%s." % (nme.capitalize(), " (4 sides and 4 angles, so a rectangle or a square also fits)" if nme == "quadrilateral" else ""))
    return dict(qs=qs, key=key, dir="Look at the five shapes. Your teacher asks about one at a time. Name the shape.", dur=100, html=h)


BUILD = {}
for _k, _p in (("add1to", "add1to"), ("add1pt", "add1pt"), ("add1cmp", "add1cmp"), ("add2to", "add2to"), ("add2pt", "add2pt"), ("add2cmp", "add2cmp"),
               ("sub1from", "sub1from"), ("sub1pt", "sub1pt"), ("sub1cmp", "sub1cmp"), ("sub2from", "sub2from"), ("sub2pt", "sub2pt"), ("sub2cmp", "sub2cmp")):
    BUILD[("2.OA.A.1", _k)] = b_oa1(_p)
BUILD.update({
    ("2.OA.C.3", "oddeven"): b_oddeven, ("2.OA.C.3", "evaneq"): b_evaneq,
    ("2.OA.C.4", "arrays"): b_arrays, ("2.OA.C.4", "arrayeq"): b_arrayeq,
    ("2.NBT.A.2", "count1000"): b_count1000, ("2.NBT.A.2", "skip2"): b_skip(2), ("2.NBT.A.2", "skip5"): b_skip(5),
    ("2.NBT.A.2", "skip10"): b_skip(10), ("2.NBT.A.2", "skip100"): b_skip(100),
    ("2.NBT.A.3", "readnum"): b_readnum, ("2.NBT.A.3", "readname"): b_readname, ("2.NBT.A.3", "readexp"): b_readexp,
    ("2.NBT.A.3", "writenum"): b_writenum, ("2.NBT.A.3", "writename"): b_writename, ("2.NBT.A.3", "writeexp"): b_writeexp,
    ("2.NBT.B.7", "addm"): b_addm, ("2.NBT.B.7", "adds"): b_adds, ("2.NBT.B.7", "subm"): b_subm, ("2.NBT.B.7", "subs"): b_subs,
    ("2.NBT.B.7", "writtenadd"): b_writtenadd, ("2.NBT.B.7", "writtensub"): b_writtensub, ("2.NBT.B.7", "hto"): b_hto, ("2.NBT.B.7", "compose"): b_compose,
    ("2.MD.A.1", "measure"): b_measure, ("2.MD.A.1", "selecttool"): b_selecttool, ("2.MD.A.1", "usetool"): b_usetool,
    ("2.MD.C.7", "tell_an"): b_time("an", "tell"), ("2.MD.C.7", "tell_dg"): b_time("dg", "tell"),
    ("2.MD.C.7", "write_an"): b_time("an", "write"), ("2.MD.C.7", "write_dg"): b_write_dg,
    ("2.MD.C.7", "tell_ampm"): b_tell_ampm, ("2.MD.C.7", "write_ampm"): b_write_ampm, ("2.MD.C.7", "relations"): b_relations,
    ("2.MD.C.8", "moneyprob"): b_moneyprob, ("2.MD.C.8", "symbols"): b_symbols,
    ("2.MD.D.10", "picgraph"): b_draw_graph("pic"), ("2.MD.D.10", "bargraph"): b_draw_graph("bar"),
    ("2.MD.D.10", "putogether"): b_putogether, ("2.MD.D.10", "takeapart"): b_takeapart, ("2.MD.D.10", "compare"): b_compare,
    ("2.G.A.1", "recognize"): b_g_recognize, ("2.G.A.1", "draw"): b_g_draw, ("2.G.A.1", "identify"): b_g_identify,
})


def fixgram(t):
    t = re.sub(r"\b1 tens\b", "1 ten", t)
    t = re.sub(r"\b1 ones\b", "1 one", t)
    t = re.sub(r"\b1 hundreds\b", "1 hundred", t)
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
    L = ["/* G2MATH-STRANDS-BEGIN (generated by source/tools/gen_g2math.py, edit the generator, not this block) */",
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append("var G2PIC=%s;" % json.dumps(data, ensure_ascii=False))
    L.append(P1.APPLY.replace("G1PIC", "G2PIC"))
    L.append("/* G2MATH-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G2, encoding="utf8").read()
    if "G2MATH-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G2MATH-STRANDS-BEGIN.*?G2MATH-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        s = src.rstrip()
        assert s.endswith("})();")
        src = s[:-5] + block + "\n})();\n"
    open(G2, "w", encoding="utf8").write(src)
    print("parts:", sum(len(p) for std in data.values() for p in std.values()), "block bytes:", len(block))


if __name__ == "__main__":
    main()
