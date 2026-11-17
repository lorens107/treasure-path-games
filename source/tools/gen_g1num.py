"""Builds the parts (strands) for the Grade 1 number standards, all 10 LPs, and writes them into source/gx/g1.js.

Standards: 1.OA.B.3, 1.OA.C.5, 1.NBT.A.1, 1.NBT.C.4, 1.NBT.C.6
Run from anywhere:  python3 source/tools/gen_g1num.py
Every problem is checked as it is built (answer in range, numbers appear in the text, no dashes
other than the plain minus sign, no "hold it up" directions).
"""
import json, os, re, random, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
G1 = os.path.join(HERE, '..', 'gx', 'g1.js')

THEME = {  # LP: (things for stories, colour for dot pictures)
    1: (["coins", "gems", "shells"], "#e0a526"),
    2: (["apples", "pears", "baskets"], "#d9534f"),
    3: (["pumpkins", "gourds", "hay bales"], "#e8832a"),
    4: (["snowballs", "mittens", "icicles"], "#5b9bd5"),
    5: (["fish", "flags", "penguins"], "#2f7fa8"),
    6: (["lanterns", "balloons", "streamers"], "#d9455f"),
    7: (["hearts", "cards", "stickers"], "#e0607e"),
    8: (["seeds", "flowers", "bees"], "#5aa05a"),
    9: (["logs", "shells", "fish"], "#7a5a3a"),
    10: (["ribbons", "cupcakes", "chairs"], "#a05bb5"),
}
NAMES = ["Mia", "Leo", "Ana", "Sam", "Rosa", "Kai", "Zoe", "Dev", "Pia", "Tam", "Ben", "Omar", "Lena", "Gus", "Max", "Teo"]

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


def words(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        t, o = divmod(n, 10)
        return TENS[t] + ("-" + ONES[o] if o else "")
    r = n - 100
    return "one hundred" + (" " + words(r) if r else "")


def rng_for(lp, pid):
    return random.Random(lp * 7919 + zlib.crc32(pid.encode()))


def nm(lp, k):
    return NAMES[(lp * 3 + k * 5) % len(NAMES)]


# ---------------------------------------------------------------- catalogs
CAT = {
    "1.OA.B.3": {
        "desc": "using properties of operations as strategies to add and subtract",
        "parts": [
            ("propadd", "Add with properties", "Use the order and grouping of numbers to add, such as switching two numbers or adding two numbers that make a ten first"),
            ("propsub", "Subtract with strategies", "Use the link between adding and subtracting, or take away to make a ten, to subtract"),
        ]},
    "1.OA.C.5": {
        "desc": "relating counting to addition and subtraction",
        "parts": [
            ("counton", "Count on to add", "Count on to add, such as counting on 2 to add 2"),
            ("countback", "Count back to subtract", "Count back to subtract, such as counting back 2 to subtract 2"),
        ]},
    "1.NBT.A.1": {
        "desc": "counting to 120, and reading, writing, and showing numbers with numerals",
        "parts": [
            ("countfrom", "Count to 120 from any number", "Count to 120, starting at any number less than 120"),
            ("readnum", "Read numerals to 120", "Read numerals up to 120"),
            ("writenum", "Write numerals to 120", "Write numerals up to 120"),
            ("showobj", "Show a number of objects with a numeral", "Show a number of objects with a written numeral up to 120"),
        ]},
    "1.NBT.C.4": {
        "desc": "adding within 100, with a two-digit number and a one-digit number or a multiple of 10",
        "parts": [
            ("add1", "Two-digit plus one-digit", "Add a two-digit number and a one-digit number within 100"),
            ("add10", "Two-digit plus a multiple of 10", "Add a two-digit number and a multiple of 10 within 100"),
            ("tensones", "Tens and ones, and making a ten", "Understand that you add tens and tens, ones and ones, and sometimes make a new ten"),
            ("explain", "Written method and explaining", "Relate the adding strategy to a written method and explain the reasoning"),
        ]},
    "1.NBT.C.6": {
        "desc": "subtracting multiples of 10 from multiples of 10, in the range 10 to 90",
        "parts": [
            ("sub10", "Subtract multiples of 10", "Subtract multiples of 10 from multiples of 10 (10 to 90), with a positive or zero difference"),
            ("subexplain", "Written method and explaining", "Relate the subtracting strategy to a written method and explain the reasoning"),
        ]},
}

DIR_TALK = "Listen to each question. Say your answer out loud. You can use your paper and pencil."
DIR_TENS = "Listen to each question. You can draw tens and ones on your paper. Say your answer out loud."
DIR_WRITE = "Listen to each question. Write on your paper if you want to. Say your answer out loud."
DIR_EXPL = "Listen to each question. Draw tens and ones, write the number sentence on your paper, then tell your teacher how you solved it."


# ---------------------------------------------------------------- builders
# each returns dict(qs=[...], key=[...], dir=..., html=None|'DOTS'|'NUMS' + data, dur=int)

def b_propadd(lp, r):
    th = THEME[lp][0]
    a, b = r.sample(range(3, 10), 2)
    while a + b > 18:
        a, b = r.sample(range(3, 10), 2)
    q1 = "%d + %d = %d. So what is %d + %d? How do you know without adding?" % (a, b, a + b, b, a)
    k1 = "%d. The same two numbers added in a different order give the same total (switching the numbers)." % (a + b)
    p = r.randint(2, 8)          # b + c = 10 pair
    c3 = r.randint(3, 9)
    q2 = "Add %d + %d + %d. Which two numbers would you add first? Why?" % (c3, p, 10 - p)
    k2 = "%d. Add %d + %d first because they make 10, then add %d. Any order that gets %d also counts." % (c3 + 10, p, 10 - p, c3, c3 + 10)
    x, y = r.sample(range(3, 10), 2)
    n1, n2 = nm(lp, 0), nm(lp, 1)
    t1, t2 = th[0], th[1]
    q3 = "%s has %d %s and %d %s. %s has %d %s and %d %s. Do they have the same number of things in all? How do you know?" % (n1, x, t1, y, t2, n2, y, t1, x, t2)
    k3 = "Yes, %d each. The same two numbers are added in a different order (switching the numbers)." % (x + y)
    return dict(qs=[q1, q2, q3], key=[k1, k2, k3], dir=DIR_TALK, dur=120,
                nums=[(a, b), (c3, p, 10 - p), (x, y)])


def b_propsub(lp, r):
    a, b = r.sample(range(3, 12), 2)
    while a + b > 20 or a + b < 11:
        a, b = r.sample(range(3, 12), 2)
    q1 = "%d + %d = %d. Use that to find %d - %d." % (a, b, a + b, a + b, b)
    k1 = "%d. Adding and subtracting undo each other, so %d - %d = %d because %d + %d = %d." % (a, a + b, b, a, a, b, a + b)
    cc = r.randint(12, 18)
    d = r.randint(cc - 10 + 1, 9)
    while cc - d >= 10 or d < 3:
        cc = r.randint(12, 18); d = r.randint(cc - 10 + 1, 9)
    step = cc - 10
    q2 = "Find %d - %d. Take away to make a ten first. What is %d - %d?" % (cc, d, cc, d)
    k2 = "%d. For example %d - %d = 10, then 10 - %d = %d. Any strategy that works counts." % (cc - d, cc, step, d - step, cc - d)
    e, f = r.sample(range(4, 12), 2)
    while e + f > 20:
        e, f = r.sample(range(4, 12), 2)
    q3 = "%d + %d = %d. What two subtraction sentences can you make with those three numbers?" % (e, f, e + f)
    k3 = "%d - %d = %d and %d - %d = %d." % (e + f, e, f, e + f, f, e)
    return dict(qs=[q1, q2, q3], key=[k1, k2, k3], dir=DIR_TALK, dur=120,
                nums=[(a, b), (cc, d), (e, f)])


def b_counton(lp, r):
    th = THEME[lp][0]
    s1 = r.randint(5, 14); k1n = r.randint(1, 3)
    q1 = "Start at %d. Count on %d. Where do you land? What adding sentence is that?" % (s1, k1n)
    k1 = "%d (%d + %d = %d). The student says %s." % (s1 + k1n, s1, k1n, s1 + k1n, ", ".join(str(s1 + i) for i in range(1, k1n + 1)))
    s2 = r.randint(7, 16); k2n = r.randint(2, 3)
    n1 = nm(lp, 2)
    q2 = "%s has %d %s. Then %d more %s come. Count on from %d. How many %s are there now?" % (n1, s2, th[0], k2n, th[0], s2, th[0])
    k2 = "%d (%d + %d = %d). Counts on %s." % (s2 + k2n, s2, k2n, s2 + k2n, ", ".join(str(s2 + i) for i in range(1, k2n + 1)))
    small = r.randint(2, 3); big = r.randint(6, 9)
    q3 = "To add %d + %d by counting on, which number is easier to start at? Show how you count on." % (small, big)
    k3 = "Start at %d (the bigger number) and count on %d: %s. The answer is %d." % (big, small, ", ".join(str(big + i) for i in range(1, small + 1)), big + small)
    return dict(qs=[q1, q2, q3], key=[k1, k2, k3], dir=DIR_TALK, dur=100, nums=[(s1, k1n), (s2, k2n), (small, big)])


def b_countback(lp, r):
    th = THEME[lp][0]
    s1 = r.randint(10, 19); k1n = r.randint(1, 3)
    q1 = "Start at %d. Count back %d. Where do you land? What subtracting sentence is that?" % (s1, k1n)
    k1 = "%d (%d - %d = %d). The student says %s." % (s1 - k1n, s1, k1n, s1 - k1n, ", ".join(str(s1 - i) for i in range(1, k1n + 1)))
    s2 = r.randint(11, 19); k2n = r.randint(2, 3)
    n1 = nm(lp, 3)
    q2 = "%s has %d %s. Then %d %s are given away. Count back from %d. How many %s are left?" % (n1, s2, th[1], k2n, th[1], s2, th[1])
    k2 = "%d (%d - %d = %d). Counts back %s." % (s2 - k2n, s2, k2n, s2 - k2n, ", ".join(str(s2 - i) for i in range(1, k2n + 1)))
    s3 = r.randint(12, 18); k3n = r.randint(3, 4)
    q3 = "Count back to find %d - %d. Say the numbers you say as you count back." % (s3, k3n)
    k3 = "%d. The student says %s." % (s3 - k3n, ", ".join(str(s3 - i) for i in range(1, k3n + 1)))
    return dict(qs=[q1, q2, q3], key=[k1, k2, k3], dir=DIR_TALK, dur=100, nums=[(s1, k1n), (s2, k2n), (s3, k3n)])


def crossing_note(s, e):
    marks = []
    for n in range(s, e):
        if n % 10 == 9:
            marks.append("%d to %d" % (n, n + 1))
    return (" Watch the turns: %s." % ", ".join(marks[:3])) if marks else ""


def b_countfrom(lp, r):
    s1 = r.randint(78, 94); e1 = s1 + r.randint(14, 20)
    q1 = "Count out loud from %d to %d." % (s1, e1)
    k1 = "Counts %d, %d, %d ... up to %d in order.%s" % (s1, s1 + 1, s1 + 2, e1, crossing_note(s1, e1))
    s2 = r.randint(101, 114); e2 = 120
    q2 = "Count out loud. Start at %d and keep going until you reach 120." % s2
    k2 = "Counts %d, %d, %d ... up to 120 in order.%s" % (s2, s2 + 1, s2 + 2, crossing_note(s2, e2))
    s3 = r.randint(21, 58); e3 = s3 + r.randint(10, 15)
    q3 = "Count out loud. Start at %d and stop when you say %d." % (s3, e3)
    k3 = "Counts %d, %d, %d ... up to %d in order.%s" % (s3, s3 + 1, s3 + 2, e3, crossing_note(s3, e3))
    return dict(qs=[q1, q2, q3], key=[k1, k2, k3], dir="Listen to each question. Count out loud.", dur=100, nums=[(s1, e1), (s2, e2), (s3, e3)])


def b_readnum(lp, r):
    a = r.choice([n for n in range(21, 99) if n % 10 not in (0, 1)])
    b = r.randint(101, 109)
    c = r.randint(111, 120)
    ns = [a, b, c]
    r.shuffle(ns)
    qs = ["Read the number in box %s out loud." % L for L in "ABC"]
    key = ["%s: %s (%d)." % (L, words(n), n) for L, n in zip("ABC", ns)]
    return dict(qs=qs, key=key, dir="Look at the three boxes. Your teacher will ask you to read one number at a time out loud.", dur=75,
                html=("NUMS", ns), nums=[tuple(ns)])


def b_writenum(lp, r):
    a = r.choice([n for n in range(21, 99) if n % 10 not in (0, 1)])
    b = r.randint(101, 109)
    c = r.randint(111, 120)
    ns = [a, b, c]
    r.shuffle(ns)
    qs = ["Write the number %s on your paper. Then tell me the digits you wrote, in order." % words(n) for n in ns]
    key = []
    for n in ns:
        ds = ", ".join(str(d) for d in str(n))
        extra = " The zero goes in the middle." if 101 <= n <= 109 else ""
        key.append("%d. The digits in order are %s.%s" % (n, ds, extra))
    return dict(qs=qs, key=key, dir="Listen to each number. Write it on your paper. Then tell your teacher the digits you wrote.", dur=100, nums=[tuple(ns)])


def b_showobj(lp, r):
    a = r.randint(23, 49)
    b = r.randint(52, 89)
    c = r.randint(101, 119)
    ns = [a, b, c]
    r.shuffle(ns)
    qs = ["Count the dots in picture %s. Write the number that tells how many." % L for L in "ABC"]
    key = ["%s: %d dots. Counting by tens and ones is fine. Look for the numeral written the right way round." % (L, n) for L, n in zip("ABC", ns)]
    return dict(qs=qs, key=key, dir="Look at the three pictures. Count the dots in each one and write the number on your paper.", dur=130,
                html=("DOTS", ns), nums=[tuple(ns)])


def b_add1(lp, r):
    th = THEME[lp][0]
    t1 = r.randint(2, 7); o1 = r.randint(1, 4); d1 = r.randint(1, 9 - o1)
    n1 = t1 * 10 + o1
    q1 = "%d + %d" % (n1, d1)
    k1 = "%d (%d + %d = %d). No new ten is needed." % (n1 + d1, n1, d1, n1 + d1)
    t2 = r.randint(2, 7); o2 = r.randint(5, 9); d2 = r.randint(10 - o2 + 1, 9)
    n2 = t2 * 10 + o2
    q2 = "%d + %d" % (n2, d2)
    k2 = "%d (%d + %d = %d). The ones make a new ten." % (n2 + d2, n2, d2, n2 + d2)
    t3 = r.randint(3, 8); o3 = r.randint(3, 9); d3 = r.randint(2, 9)
    n3 = t3 * 10 + o3
    nme = nm(lp, 4)
    q3 = "%s has %d %s. %s gets %d more %s. How many %s does %s have now?" % (nme, n3, th[2], nme, d3, th[2], th[2], nme)
    k3 = "%d (%d + %d = %d)." % (n3 + d3, n3, d3, n3 + d3)
    return dict(qs=[q1, q2, q3], key=[k1, k2, k3], dir=DIR_TENS, dur=130, nums=[(n1, d1), (n2, d2), (n3, d3)])


def b_add10(lp, r):
    th = THEME[lp][0]
    n1 = r.randint(11, 59); m1 = r.choice([10, 20, 30, 40])
    q1 = "%d + %d" % (n1, m1)
    k1 = "%d (%d + %d = %d). The ones stay the same and the tens add." % (n1 + m1, n1, m1, n1 + m1)
    n2 = r.randint(14, 48); m2 = r.choice([10, 20, 30, 50])
    q2 = "%d + %d" % (n2, m2)
    k2 = "%d (%d + %d = %d). The ones stay the same and the tens add." % (n2 + m2, n2, m2, n2 + m2)
    n3 = r.randint(12, 55); m3 = r.choice([20, 30, 40])
    nme = nm(lp, 5)
    q3 = "%s has %d %s. Then %d more %s come. How many %s are there now?" % (nme, n3, th[1], m3, th[1], th[1])
    k3 = "%d (%d + %d = %d)." % (n3 + m3, n3, m3, n3 + m3)
    for n, m in ((n1, m1), (n2, m2), (n3, m3)):
        assert n + m <= 100
    return dict(qs=[q1, q2, q3], key=[k1, k2, k3], dir=DIR_TENS, dur=130, nums=[(n1, m1), (n2, m2), (n3, m3)])


def b_tensones(lp, r):
    n1 = r.randint(12, 58); m1 = r.choice([20, 30, 40])
    q1 = "In %d + %d, do you add the %d to the tens or to the ones? How do you know?" % (n1, m1, m1)
    k1 = "To the tens. %d is %d tens, so %d tens + %d tens = %d tens. The ones stay %d. Answer %d." % (m1, m1 // 10, n1 // 10, m1 // 10, n1 // 10 + m1 // 10, n1 % 10, n1 + m1)
    o2 = r.randint(6, 9); d2 = r.randint(10 - o2 + 2, 9); t2 = r.randint(2, 7)
    n2 = t2 * 10 + o2
    s2 = o2 + d2
    q2 = "In %d + %d, add the ones first. What is %d + %d? What do you do with that number?" % (n2, d2, o2, d2)
    k2 = "%d. Make a new ten: %d is 1 ten and %d ones. Then %d tens + 1 ten = %d tens, and %d ones. Answer %d." % (s2, s2, s2 - 10, t2, t2 + 1, s2 - 10, n2 + d2)
    o3 = r.randint(5, 9); d3 = r.randint(10 - o3 + 1, 9); t3 = r.randint(3, 8)
    n3 = t3 * 10 + o3
    q3 = "In %d + %d, how many tens and how many ones are in the answer? How do you know?" % (n3, d3)
    k3 = "%d, so %d tens and %d ones. The ones add to %d, which makes a new ten (%d tens + 1 ten = %d tens, and %d ones)." % (n3 + d3, (n3 + d3) // 10, (n3 + d3) % 10, o3 + d3, t3, t3 + 1, (n3 + d3) % 10)
    for v in (n1 + m1, n2 + d2, n3 + d3):
        assert v <= 100
    return dict(qs=[q1, q2, q3], key=[k1, k2, k3], dir=DIR_TENS, dur=140, nums=[(n1, m1), (n2, d2), (n3, d3)])


def b_explain(lp, r):
    qs, key, nums = [], [], []
    specs = [("ones", r.randint(2, 7), r.randint(1, 3), r.randint(2, 5)),
             ("regroup", r.randint(2, 7), r.randint(5, 9), r.randint(5, 9)),
             ("tens", r.randint(2, 6), r.randint(2, 8), 0)]
    r.shuffle(specs)
    for kind, t, o, d in specs:
        n = t * 10 + o
        if kind == "tens":
            d = r.choice([10, 20, 30])
        if kind == "regroup" and o + d < 10:
            d = 10 - o + r.randint(1, 3)
            d = min(d, 9)
        s = n + d
        assert s <= 100
        qs.append("Add %d + %d. Draw tens and ones, write the number sentence, and tell how you added." % (n, d))
        look = "an equation written correctly and an explanation that uses tens and ones"
        if kind == "regroup":
            look += " (for example, the ones made a new ten)"
        key.append("%d (%d + %d = %d). Look for %s." % (s, n, d, s, look))
        nums.append((n, d))
    return dict(qs=qs, key=key, dir=DIR_EXPL, dur=210, nums=nums)


def b_sub10(lp, r):
    th = THEME[lp][0]
    a1 = r.choice([50, 60, 70, 80, 90]); b1 = r.choice([x for x in (10, 20, 30) if x < a1])
    q1 = "%d - %d" % (a1, b1)
    k1 = "%d (%d - %d = %d). %d tens take away %d tens is %d tens." % (a1 - b1, a1, b1, a1 - b1, a1 // 10, b1 // 10, (a1 - b1) // 10)
    a2 = r.choice([60, 70, 80, 90]); b2 = r.choice([x for x in (30, 40, 50, 60) if x < a2])
    q2 = "%d - %d" % (a2, b2)
    k2 = "%d (%d - %d = %d). %d tens take away %d tens is %d tens." % (a2 - b2, a2, b2, a2 - b2, a2 // 10, b2 // 10, (a2 - b2) // 10)
    nme = nm(lp, 6)
    if lp in (3, 6, 9):   # zero difference
        a3 = r.choice([30, 40, 50, 60, 70]); b3 = a3
        q3 = "%s has %d %s. All of the %s are given away. How many %s are left?" % (nme, a3, th[0], th[0], th[0])
        k3 = "0 (%d - %d = 0). All the tens are taken away, so none are left." % (a3, b3)
    else:
        a3 = r.choice([50, 60, 70, 80, 90]); b3 = r.choice([x for x in (20, 30, 40) if x < a3])
        q3 = "%s has %d %s. %d %s are given away. How many %s are left?" % (nme, a3, th[0], b3, th[0], th[0])
        k3 = "%d (%d - %d = %d)." % (a3 - b3, a3, b3, a3 - b3)
    return dict(qs=[q1, q2, q3], key=[k1, k2, k3], dir=DIR_TENS, dur=100, nums=[(a1, b1), (a2, b2), (a3, b3)])


def b_subexplain(lp, r):
    qs, key, nums = [], [], []
    for i in range(3):
        a = r.choice([50, 60, 70, 80, 90]); b = r.choice([x for x in (10, 20, 30, 40, 50) if x < a])
        qs.append("Subtract %d - %d. Write the number sentence and tell how you know." % (a, b))
        key.append("%d (%d - %d = %d). Look for a number sentence written correctly and an explanation such as: %d tens take away %d tens is %d tens, counting back by tens, or %d + %d = %d." % (a - b, a, b, a - b, a // 10, b // 10, (a - b) // 10, b, a - b, a))
        nums.append((a, b))
    return dict(qs=qs, key=key, dir="Listen to each question. Write the number sentence on your paper. Then tell your teacher how you know.", dur=130, nums=nums)


BUILD = {
    ("1.OA.B.3", "propadd"): b_propadd, ("1.OA.B.3", "propsub"): b_propsub,
    ("1.OA.C.5", "counton"): b_counton, ("1.OA.C.5", "countback"): b_countback,
    ("1.NBT.A.1", "countfrom"): b_countfrom, ("1.NBT.A.1", "readnum"): b_readnum,
    ("1.NBT.A.1", "writenum"): b_writenum, ("1.NBT.A.1", "showobj"): b_showobj,
    ("1.NBT.C.4", "add1"): b_add1, ("1.NBT.C.4", "add10"): b_add10,
    ("1.NBT.C.4", "tensones"): b_tensones, ("1.NBT.C.4", "explain"): b_explain,
    ("1.NBT.C.6", "sub10"): b_sub10, ("1.NBT.C.6", "subexplain"): b_subexplain,
}

BAD = re.compile(r"hold it up|show (me|your teacher) your (paper|work)|camera|—|–")


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
                    part["html"] = list(d["html"])
                    part["html"][1] = list(d["html"][1])
                parts.append(part)
            out.setdefault(std, {})[str(lp)] = parts
    return out


def check_numbers(data):
    """sanity checks that only look at the finished data"""
    for std, lps in data.items():
        for lp, parts in lps.items():
            for p in parts:
                for q, k in zip(p["qs"], p["key"]):
                    m = re.match(r"^(\d+) ([+-]) (\d+)$", q)
                    if m:
                        a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
                        v = a + b if op == "+" else a - b
                        assert k.startswith("%d " % v), (std, lp, p["id"], q, k)
                        assert 0 <= v <= 100
                    m = re.match(r"^Add (\d+) \+ (\d+)\.", q)
                    if m:
                        v = int(m.group(1)) + int(m.group(2))
                        assert k.startswith("%d " % v) and v <= 100, (q, k)
                    m = re.match(r"^Subtract (\d+) - (\d+)\.", q)
                    if m:
                        v = int(m.group(1)) - int(m.group(2))
                        assert k.startswith("%d " % v) and v >= 0, (q, k)


JS_HELPERS = r"""
function G1NUMS(a){return function(){return'<div style="display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin:10px 0">'+a.map(function(n,i){return'<div style="border:3px solid var(--line);border-radius:14px;background:var(--card,#fff);padding:8px 22px;text-align:center"><div class="small" style="font-weight:700">'+"ABC".charAt(i)+'</div><div style="font-size:2.6rem;font-weight:800">'+n+'</div></div>'}).join("")+'</div>'}}
function G1DOTS(a,col){return function(){return'<div style="display:flex;gap:22px;justify-content:center;flex-wrap:wrap;margin:10px 0">'+a.map(function(n,i){var rows=Math.ceil(n/10),w=10*20+8,h=rows*20+8,s='<svg viewBox="0 0 '+w+' '+h+'" width="'+Math.round(w*1.15)+'" role="img" aria-label="Picture '+"ABC".charAt(i)+', dots in rows of ten">';for(var k=0;k<n;k++)s+='<circle cx="'+(14+(k%10)*20)+'" cy="'+(14+Math.floor(k/10)*20)+'" r="7.5" fill="'+col+'" stroke="#4a3b32" stroke-width="1.4"/>';s+='</svg>';return'<div style="text-align:center"><div class="small" style="font-weight:700">'+"ABC".charAt(i)+'</div>'+s+'</div>'}).join("")+'</div>'}}
"""


def js(data):
    L = []
    L.append("/* G1NUM-STRANDS-BEGIN (generated by source/tools/gen_g1num.py, edit the generator, not this block) */")
    L.append("window.TP_STRANDS=window.TP_STRANDS||{};")
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append(JS_HELPERS.strip())
    L.append("var G1COL=%s;" % json.dumps({str(k): v[1] for k, v in THEME.items()}))
    L.append("var G1NUM=%s;" % json.dumps(data, ensure_ascii=False))
    L.append("""Object.keys(G1NUM).forEach(function(std){A({std:std,op:"strands",make:function(lp){return G1NUM[std][String(lp)].map(function(s){var o={std:std,strand:s.id,title:s.title,n:3,dur:s.dur,dir:s.dir,desc:s.desc,mats:["a pencil and paper"],rows:s.qs.map(function(q,j){return[q,s.key[j]]})};if(s.html){o.html=s.html[0]==="NUMS"?G1NUMS(s.html[1]):G1DOTS(s.html[1],G1COL[String(lp)])}return P(o)})}})});""")
    L.append("/* G1NUM-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    check_numbers(data)
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G1, encoding="utf8").read()
    if "G1NUM-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G1NUM-STRANDS-BEGIN.*?G1NUM-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        marker = "/* OAA1-STRANDS-END */"
        assert marker in src
        src = src.replace(marker, marker + "\n" + block)
    open(G1, "w", encoding="utf8").write(src)
    n = sum(len(p["qs"]) for std in data.values() for parts in std.values() for p in parts)
    print("wrote", n, "problems in", sum(len(p) for std in data.values() for p in std.values()), "parts")


if __name__ == "__main__":
    main()
