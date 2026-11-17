"""Builds the parts (strands) for the Grade 1 ELA essential standards, all 10 LPs, and writes them into source/gx/g1.js.

One part per "I can" line in the gray book (Grade 1 ELA Standards file). Same-skill lines are merged:
  RL.1.1 / RI.1.1 / SL.1.2: ask, answer
  W.1.1: write an opinion piece, introduce, state opinion, reason, closure
  W.1.2: write an informative piece, name the topic, facts, closure
  W.1.3: write a narrative, recount events, details, temporal words, closure
  RF.1.1: organization of print, basic features of print
  RF.1.2: spoken words, syllables, sounds
  RF.1.3: phonics knowledge, word analysis knowledge, then decoding each in isolation and in text
  RF.1.4: accuracy, fluency
  SL.1.4: people, places, things, events, ideas, feelings
  L.1.1: the two "I can" lines do not split the standard, so it is split by the CCSS list (a to j)
W.1.8 has one "I can" line and stays whole.
Run:  python3 source/tools/gen_g1ela.py
Student-read text is held to 7 words a sentence (grade 1 cap). Teacher-read text is not capped.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g1num as N
import gen_g1pic as P1

G1 = N.G1
BAD = N.BAD
rng_for, nm = N.rng_for, N.nm
STUDENT_CAP = 7

LEFT = "Your teacher reads each question. Tell your answer out loud."


def sents(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def wc(s):
    return len(re.findall(r"[A-Za-z']+", s))


def check_student(text):
    for s in sents(text):
        assert wc(s) <= STUDENT_CAP, ("too long for grade 1", s)


def passage_html(title, text):
    check_student(text)
    return '<p class="big" style="text-align:center;margin:0 0 6px">%s</p><p class="passage">%s</p>' % (title, text)


def lines_html(items):
    out = ""
    for L, t in items:
        check_student(t)
        out += '<p class="big" style="margin:6px 0"><b>%s.</b> %s</p>' % (L, t)
    return out


def pills_html(sets):
    out = ""
    for L, words in sets:
        out += '<div class="row center" style="gap:14px;flex-wrap:wrap;margin:8px 0"><b style="font-size:1.4rem">%s</b>' % L
        for w in words:
            out += '<span class="pill" style="font-size:1.8rem">%s</span>' % w
        out += "</div>"
    return out


def rot(pool, lp, k=3, step=3):
    n = len(pool)
    return [pool[((lp - 1) * step + j) % n] for j in range(k)]


# ================================================================ stories (student-read, 7 words a sentence)
LIT = {
    1: ("Mia Finds a Shell", "Mia went to the beach. She saw a big pink shell. She put it in her red pail. Then a crab came out of it!",
        [("Who", "Who went to the beach?", "Mia"), ("What", "What did Mia see?", "A big pink shell"), ("Where", "Where did Mia put the shell?", "In her red pail"), ("What", "What came out of the shell?", "A crab")]),
    2: ("Ben Picks Apples", "Ben has a tall ladder. He goes up to the top. He picks six red apples. He puts them in a basket. Then his dog Max runs by.",
        [("Who", "Who has a tall ladder?", "Ben"), ("What", "What does Ben pick?", "Six red apples"), ("Where", "Where does Ben put the apples?", "In a basket"), ("Who", "Who runs by?", "His dog Max")]),
    3: ("Jill and the Pumpkin", "Jill grew a big pumpkin. It was too big to lift. She got her pal Russ. Russ had a red wagon. They put the pumpkin in it.",
        [("What", "What did Jill grow?", "A big pumpkin"), ("Who", "Who did Jill get to help?", "Russ"), ("What", "What did Russ have?", "A red wagon"), ("Where", "Where did they put the pumpkin?", "In the wagon")]),
    4: ("Snow Day", "It was a cold snow day. Tom put on his hat. He put on red mittens. He played in the yard. Then he made a snowman.",
        [("Who", "Who played in the snow?", "Tom"), ("What", "What did Tom put on?", "His hat and red mittens"), ("Where", "Where did Tom play?", "In the yard"), ("What", "What did Tom make?", "A snowman")]),
    5: ("Pip the Penguin", "Pip is a small penguin. He lives on the ice. He likes to swim. He dives for fish. He gets a fish for his mom.",
        [("Who", "Who is Pip?", "A small penguin"), ("Where", "Where does Pip live?", "On the ice"), ("What", "What does Pip dive for?", "Fish"), ("Who", "Who gets a fish?", "Pip's mom")]),
    6: ("The Lantern Walk", "Lena has a paper lantern. It is red and gold. She walks with her dad. They go down the hill. The lantern glows in the dark.",
        [("Who", "Who has a paper lantern?", "Lena"), ("What", "What colors is the lantern?", "Red and gold"), ("Who", "Who does Lena walk with?", "Her dad"), ("Where", "Where do they go?", "Down the hill")]),
    7: ("A Card for Gran", "Omar made a card for Gran. He drew a big heart. He used a pink pen. He put it in the mail. Gran was so happy!",
        [("Who", "Who made a card?", "Omar"), ("What", "What did Omar draw?", "A big heart"), ("What", "What did Omar use?", "A pink pen"), ("Where", "Where did Omar put the card?", "In the mail")]),
    8: ("Bee in the Garden", "A bee came to the garden. It sat on a red flower. Then it flew to a tree. A girl named Pia waved.",
        [("What", "What came to the garden?", "A bee"), ("Where", "Where did the bee sit?", "On a red flower"), ("Where", "Where did the bee fly next?", "To a tree"), ("Who", "Who waved?", "Pia")]),
    9: ("Camp by the Lake", "Gus and Kai go to camp. They fish from a log. Gus gets a big fish. Kai gets a boot! They both laugh and laugh.",
        [("Who", "Who goes to camp?", "Gus and Kai"), ("Where", "Where do they fish from?", "A log"), ("What", "What does Gus get?", "A big fish"), ("What", "What does Kai get?", "A boot")]),
    10: ("The Big Party", "Zoe had a party at home. Her friends came at noon. They ate cake and fruit. Then they played in the yard.",
         [("Who", "Who had a party?", "Zoe"), ("What", "What did they eat?", "Cake and fruit"), ("Where", "Where did they play?", "In the yard"), ("When", "When did her friends come?", "At noon")]),
}

INFO = {
    1: ("Sea Shells", "A shell is a home. Snails live in shells. A shell keeps them safe. Some shells are big. Some are very small.",
        [("What", "What is a shell?", "A home"), ("Who", "Who lives in shells?", "Snails"), ("What", "What does a shell do?", "Keeps them safe"), ("How", "How big are shells?", "Some are big and some are small")]),
    2: ("Apples", "Apples grow on trees. They can be red or green. We pick apples in fall. Apples have seeds inside.",
        [("Where", "Where do apples grow?", "On trees"), ("What", "What colors can apples be?", "Red or green"), ("When", "When do we pick apples?", "In fall"), ("What", "What is inside an apple?", "Seeds")]),
    3: ("Pumpkins", "Pumpkins grow on vines. They start out green. They turn orange in fall. Each pumpkin has seeds.",
        [("Where", "Where do pumpkins grow?", "On vines"), ("What", "What color are pumpkins at first?", "Green"), ("When", "When do pumpkins turn orange?", "In fall"), ("What", "What does each pumpkin have?", "Seeds")]),
    4: ("Snow", "Snow is frozen water. It falls from clouds. Snow is cold. It melts in the sun.",
        [("What", "What is snow?", "Frozen water"), ("Where", "Where does snow fall from?", "Clouds"), ("How", "How does snow feel?", "Cold"), ("What", "What happens to snow in the sun?", "It melts")]),
    5: ("Penguins", "Penguins are birds. They cannot fly. They swim fast. They eat fish. Many live where it is cold.",
        [("What", "What are penguins?", "Birds"), ("What", "What can penguins not do?", "Fly"), ("How", "How do penguins swim?", "Fast"), ("Where", "Where do many penguins live?", "Where it is cold")]),
    6: ("Lanterns", "A lantern holds a light. Some are made of paper. People hang them up high. They glow at night.",
        [("What", "What does a lantern hold?", "A light"), ("What", "What are some lanterns made of?", "Paper"), ("Where", "Where do people hang them?", "Up high"), ("When", "When do lanterns glow?", "At night")]),
    7: ("Your Heart", "Your heart is a muscle. It sits in your chest. It pumps blood. It beats all day and night.",
        [("What", "What is your heart?", "A muscle"), ("Where", "Where does your heart sit?", "In your chest"), ("What", "What does your heart pump?", "Blood"), ("When", "When does your heart beat?", "All day and night")]),
    8: ("Bees", "Bees make honey. They live in a hive. They visit flowers. A bee has six legs.",
        [("What", "What do bees make?", "Honey"), ("Where", "Where do bees live?", "In a hive"), ("What", "What do bees visit?", "Flowers"), ("How", "How many legs does a bee have?", "Six")]),
    9: ("Fish", "Fish live in water. They breathe with gills. Fins help them swim. Most fish have scales.",
        [("Where", "Where do fish live?", "In water"), ("How", "How do fish breathe?", "With gills"), ("What", "What helps fish swim?", "Fins"), ("What", "What do most fish have?", "Scales")]),
    10: ("Balloons", "Balloons are full of air. Some float up high. A pin can pop one. A pop is loud.",
         [("What", "What are balloons full of?", "Air"), ("Where", "Where do some balloons float?", "Up high"), ("What", "What can pop a balloon?", "A pin"), ("How", "How is a pop?", "Loud")]),
}
for _d in (LIT, INFO):
    for _lp, (_t, _x, _f) in _d.items():
        check_student(_x)
        assert len({s for s, _, _ in _f}) >= 3, (_t, "need 3 different question starters")


def starters(facts):
    seen, out = set(), []
    for s, q, a in facts:
        if s not in seen:
            seen.add(s)
            out.append((s, q, a))
        if len(out) == 3:
            break
    return out


def story_ask(bank, kind):
    def b(lp, r):
        t, x, facts = bank[lp]
        st = starters(facts)
        qs = ["Read the %s. Then ask me a question that starts with %s." % (kind, s) for s, _, _ in st]
        key = ["Any real question that starts with %s and can be answered from the text. For example: %s (%s)" % (s, q, a) for s, q, a in st]
        return dict(qs=qs, key=key, dir="Read the %s to yourself. Then your teacher asks you to make up questions about it. Say each question out loud." % kind, dur=170, html=passage_html(t, x))
    return b


def story_answer(bank, kind):
    def b(lp, r):
        t, x, facts = bank[lp]
        st = starters(facts)
        qs = [q for _, q, _ in st]
        key = ["%s." % a for _, _, a in st]
        return dict(qs=qs, key=key, dir="Read the %s to yourself. Then your teacher asks you questions about it. Tell your answers out loud." % kind, dur=170, html=passage_html(t, x))
    return b


# ================================================================ writing parts
OPIN = [("pumpkin or a sunflower", "pumpkin", "sunflower"), ("cat or a dog", "cat", "dog"), ("summer or winter", "summer", "winter"), ("apple or a grape", "apple", "grape"),
        ("pizza or a taco", "pizza", "taco"), ("park or a pool", "park", "pool"), ("book or a movie", "book", "movie"), ("swing or a slide", "swing", "slide"),
        ("bike or a scooter", "bike", "scooter"), ("rainy day or a sunny day", "rainy day", "sunny day")]
OPIN_TOPIC = ["your favorite game", "the best snack", "the best pet", "your favorite season", "the best place to play", "your favorite animal", "the best ice cream flavor", "the best day of the week", "your favorite color", "the best thing to do at recess"]
BOOKS = ["a book you like", "a book you read with your family", "a book about animals", "a book that is funny", "a book with a lot of pictures", "a book about a kid", "your favorite picture book", "a book from the library", "a book about a place", "a book you want to read again"]
OPIN_STATES = ["Pizza is the best lunch.", "Recess is the best part of the day.", "Dogs make the best pets.", "Summer is better than winter.", "Reading is fun.", "Apples are a good snack.", "The park is a fun place.", "Bikes are better than scooters.", "Snow days are the best.", "Cake is better than pie."]
CLOSE_OPIN = ["your opinion about dogs", "your opinion about recess", "your opinion about pizza", "your opinion about summer", "your opinion about your favorite book", "your opinion about snow", "your opinion about swimming", "your opinion about cats", "your opinion about parks", "your opinion about apples"]


def b_w1_whole(lp, r):
    it = rot(OPIN, lp)
    qs = ["Which would you rather have: a %s? Write 2 or 3 sentences. Tell which one you pick, tell why, and end it." % a for a, _, _ in it]
    look = "Look for: an opinion (I like, I think, is better), a reason (because or a why), and a closing sentence."
    key = [look + " Either choice is fine." for _ in it]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write your answer on your paper. Then read it to your teacher if asked.", dur=300, mats=["a pencil and paper"])


def b_w1_intro(lp, r):
    tp = rot(BOOKS, lp)
    qs = ["Write one sentence that names %s. Start with: I am writing about." % t for t in tp]
    key = ["Names a real book or topic in a complete sentence, such as: I am writing about the book ___. The name of the book or topic is clear." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write one sentence on your paper.", dur=210, mats=["a pencil and paper"])


def b_w1_state(lp, r):
    tp = rot(OPIN_TOPIC, lp)
    qs = ["The topic is %s. Write one sentence that tells what you think." % t for t in tp]
    key = ["Gives a clear opinion, such as I like, I think, or is the best. A fact alone is not an opinion." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write one sentence on your paper.", dur=210, mats=["a pencil and paper"])


def b_w1_reason(lp, r):
    st = rot(OPIN_STATES, lp)
    qs = ["Here is an opinion: %s Write one sentence that gives a reason." % s for s in st]
    key = ["A reason that fits the opinion, often with because. For example: ... because it is fun. The reason is not just the opinion said again." for _ in st]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write one sentence on your paper.", dur=210, mats=["a pencil and paper"])


def b_w1_close(lp, r):
    tp = rot(CLOSE_OPIN, lp)
    qs = ["You wrote %s. Write one last sentence to end it." % t for t in tp]
    key = ["A closing sentence that wraps up, such as That is why I like it, or Now you know what I think. It does not add a new reason." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write one sentence on your paper.", dur=200, mats=["a pencil and paper"])


TOPICS_INFO = ["dogs", "cats", "bees", "apples", "the moon", "frogs", "rain", "birds", "fish", "trees"]
TEACH = ["an animal", "a food", "a place", "a sport", "a season", "a plant", "a game", "a pet", "a vehicle", "a holiday"]


def b_w2_whole(lp, r):
    tp = rot(TOPICS_INFO, lp)
    qs = ["Write about %s. Name your topic, write two facts, and end it." % t for t in tp]
    key = ["Look for: the topic is named, at least two true facts about it, and a closing sentence. A story or an opinion is not a fact piece." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write your answer on your paper.", dur=300, mats=["a pencil and paper"])


def b_w2_topic(lp, r):
    tp = rot(TEACH, lp)
    qs = ["Pick %s you know a lot about. Write one sentence that names your topic. Start with: I will tell you about." % t for t in tp]
    key = ["The topic is named in a complete sentence, such as I will tell you about frogs. The topic is something the student can teach about." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write one sentence on your paper.", dur=210, mats=["a pencil and paper"])


def b_w2_facts(lp, r):
    tp = rot(TOPICS_INFO, lp)
    qs = ["Write two facts about %s." % t for t in tp]
    key = ["Two different true facts about the topic. A fact can be checked. Words like I like are opinions, not facts." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write your answer on your paper.", dur=220, mats=["a pencil and paper"])


def b_w2_close(lp, r):
    tp = rot(TOPICS_INFO, lp)
    qs = ["You wrote facts about %s. Write one last sentence to end your writing." % t for t in tp]
    key = ["A closing sentence that wraps up the topic, such as Now you know about bees. It does not start a new topic." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write one sentence on your paper.", dur=200, mats=["a pencil and paper"])


NARR = ["a day at the park", "a time you ate with your family", "a trip to the store", "a time you played with a friend", "a rainy day", "a birthday", "a day at the beach", "making something", "a walk outside", "a time you helped someone"]
SEQ = ["making a sandwich", "getting ready for bed", "planting a seed", "washing your hands", "building a block tower", "getting dressed", "making a card", "brushing your teeth", "going to school", "baking cookies"]


def b_w3_whole(lp, r):
    tp = rot(NARR, lp)
    qs = ["Write about %s. Tell two or more things that happened in order. Add some details, use words like first and then, and end it." % t for t in tp]
    key = ["Look for: two or more events in the right order, some details, a time word (first, next, then, last), and a closing sentence." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write your answer on your paper.", dur=320, mats=["a pencil and paper"])


def b_w3_events(lp, r):
    tp = rot(SEQ, lp)
    qs = ["Write two things that happen when you are %s. Put them in order." % t for t in tp]
    key = ["Two or more events that fit the topic, written in an order that makes sense." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write your answer on your paper.", dur=230, mats=["a pencil and paper"])


DETAILS = [("I ate lunch.", "what you ate"), ("We went outside.", "where you went"), ("I saw a dog.", "what the dog looked like"), ("Mom made dinner.", "what she made"), ("I got a gift.", "what the gift was"),
       ("We played a game.", "which game it was"), ("I rode my bike.", "where you rode"), ("The sun came out.", "how it felt"), ("I drew a picture.", "what you drew"), ("We had a snack.", "what the snack was")]


def b_w3_details(lp, r):
    it = rot(DETAILS, lp)
    qs = ["Here is a sentence: %s Write it again and add a detail that tells %s." % (s, d) for s, d in it]
    key = ["The sentence is kept and one or more details are added, such as a color, a number, a place, or a name." for _ in it]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write your answer on your paper.", dur=230, mats=["a pencil and paper"])


def b_w3_temporal(lp, r):
    tp = rot(SEQ, lp)
    qs = ["Write 3 sentences about %s. Use the words first, next, and last." % t for t in tp]
    key = ["Three sentences in order. The time words first, next, and last (or then, after) are used to show the order." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write your answer on your paper.", dur=240, mats=["a pencil and paper"])


def b_w3_close(lp, r):
    tp = rot(NARR, lp)
    qs = ["You wrote about %s. Write one last sentence to end your story." % t for t in tp]
    key = ["A closing sentence that ends the story, such as We went home happy, or It was a great day. It does not start a new event." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Write one sentence on your paper.", dur=200, mats=["a pencil and paper"])


# ================================================================ RF.1.1
SENT_STATE = ["The cat sat on the mat.", "The sun is hot.", "Dad has a red hat.", "The dog ran to the pond.", "We can see a big ship.", "Mom made a cake.", "The frog is on a log.", "A bee sat on the flower.", "Tim has a new bike.", "The bird is in the nest."]
SENT_QUEST = ["Is it time to eat?", "Can we go to the park?", "Do you have a pet?", "Is the dog in the yard?", "Can you see the moon?", "Will it rain today?"]
SENT_BARE = [("The cat is on the bed", "a period", "statement"), ("We can play at the park", "a period", "statement"), ("Is the sun up", "a question mark", "question"), ("Can you see the ship", "a question mark", "question"), ("We won the game", "a period or an exclamation mark", "statement or exclamation")]


def b_rf11_org(lp, r):
    a, b, c = rot(SENT_STATE, lp)
    ws = lambda s: re.findall(r"[A-Za-z']+", s)
    qs = ["Look at sentence A. Say the first word.", "Look at sentence B. Say the last word.", "Look at sentence C. How many words are in it?"]
    key = ["%s." % ws(a)[0], "%s." % ws(b)[-1], "%d words." % len(ws(c))]
    return dict(qs=qs, key=key, dir="Look at the three sentences. Your teacher asks about the words in each one. Tell your answers.", dur=130, html=lines_html([("A", a), ("B", b), ("C", c)]))


def b_rf11_basic(lp, r):
    a = rot(SENT_STATE, lp, 1)[0]
    q = rot(SENT_QUEST, lp, 1, 2)[0]
    bare = SENT_BARE[(lp - 1) % len(SENT_BARE)]
    ws = lambda s: re.findall(r"[A-Za-z']+", s)
    qs = ["Look at sentence A. What mark is at the end?", "Look at sentence B. Which word begins with a capital letter? Why does it start with a capital letter?", "Look at sentence C. It has no end mark. What mark should go at the end?"]
    key = ["A period. It is a telling sentence.", "%s. A sentence starts with a capital letter. The mark at the end is a question mark." % ws(q)[0], "%s." % bare[1].capitalize()]
    return dict(qs=qs, key=key, dir="Look at the three sentences. Your teacher asks about the capital letters and end marks. Tell your answers.", dur=140, html=lines_html([("A", a), ("B", q), ("C", bare[0])]))


# ================================================================ RF.1.2
BLEND = [("s t o p", "stop"), ("f r o g", "frog"), ("j u m p", "jump"), ("s n a p", "snap"), ("c l a p", "clap"), ("m i l k", "milk"), ("n e s t", "nest"), ("f l a g", "flag"), ("g l a d", "glad"), ("s w i m", "swim"), ("c r a b", "crab"), ("t r i p", "trip"), ("d r u m", "drum")]
LONGSHORT = [("tap or tape", "tape"), ("kit or kite", "kite"), ("hop or hope", "hope"), ("cub or cube", "cube"), ("rain or ran", "rain"), ("bone or bun", "bone"), ("mad or made", "made"), ("pin or pine", "pine")]
SHORTLONG = [("cake", "long"), ("hat", "short"), ("boat", "long"), ("sun", "short"), ("feet", "long"), ("dog", "short"), ("rope", "long"), ("pen", "short")]


def b_rf12_words(lp, r):
    bl = rot(BLEND, lp, 2, 4)
    ls = LONGSHORT[(lp - 1) % len(LONGSHORT)]
    sl = SHORTLONG[(lp * 3) % len(SHORTLONG)]
    qs = ["Listen to the sounds. Blend them into a word: %s." % bl[0][0].replace(" ", ", "),
          "Which word has a long vowel sound: %s?" % ls[0],
          "Listen to the sounds. Blend them into a word: %s." % bl[1][0].replace(" ", ", ")]
    key = ["%s." % bl[0][1], "%s." % ls[1].capitalize(), "%s." % bl[1][1]]
    return dict(qs=qs, key=key, dir="Your teacher says sounds and words. Listen and tell your answer out loud. You do not need to read.", dur=140)


SYL1 = ["dog", "jump", "tree", "frog", "book", "cake"]
SYL2 = ["pencil", "rabbit", "window", "basket", "apple", "tiger", "napkin", "sunset"]
SYL3 = ["banana", "potato", "umbrella", "dinosaur", "butterfly", "elephant"]


def b_rf12_syl(lp, r):
    w1 = SYL1[(lp - 1) % len(SYL1)]
    w2 = SYL2[(lp - 1) % len(SYL2)]
    w3 = SYL3[(lp - 1) % len(SYL3)]
    order = [(w1, 1), (w2, 2), (w3, 3)]
    if lp % 2 == 0:
        order = [order[1], order[2], order[0]]
    qs = ["Clap the parts in the word %s. How many syllables?" % w for w, _ in order]
    key = ["%d syllable%s." % (n, "" if n == 1 else "s") for _, n in order]
    return dict(qs=qs, key=key, dir="Your teacher says words. Clap the parts and tell how many syllables. You do not need to read.", dur=130)


INIT = [("ship", "/sh/"), ("frog", "/f/"), ("moon", "/m/"), ("stop", "/s/"), ("chin", "/ch/"), ("drum", "/d/")]
MED = [("cat", "/a/ (short a)"), ("sit", "/i/ (short i)"), ("hop", "/o/ (short o)"), ("bug", "/u/ (short u)"), ("pen", "/e/ (short e)")]
FINAL = [("dog", "/g/"), ("sun", "/n/"), ("bus", "/s/"), ("map", "/p/"), ("nest", "/t/"), ("fish", "/sh/")]
SEG = [("fish", "/f/ /i/ /sh/"), ("stop", "/s/ /t/ /o/ /p/"), ("jam", "/j/ /a/ /m/"), ("ship", "/sh/ /i/ /p/"), ("chin", "/ch/ /i/ /n/"), ("frog", "/f/ /r/ /o/ /g/"), ("nest", "/n/ /e/ /s/ /t/")]


PHON = {"ship": ["sh", "i", "p"], "frog": ["f", "r", "o", "g"], "moon": ["m", "oo", "n"], "stop": ["s", "t", "o", "p"], "chin": ["ch", "i", "n"], "drum": ["d", "r", "u", "m"],
        "cat": ["k", "a", "t"], "sit": ["s", "i", "t"], "hop": ["h", "o", "p"], "bug": ["b", "u", "g"], "pen": ["p", "e", "n"], "dog": ["d", "o", "g"], "sun": ["s", "u", "n"],
        "bus": ["b", "u", "s"], "map": ["m", "a", "p"], "nest": ["n", "e", "s", "t"], "fish": ["f", "i", "sh"], "jam": ["j", "a", "m"]}


def elk_html(items):
    out = ""
    for num, w, ph in items:
        out += '<div class="elk" style="margin:10px 0;display:flex;align-items:center;gap:6px;flex-wrap:wrap"><b style="font-size:1.4rem;margin-right:6px">%d.</b>' % num
        for _ in ph:
            out += '<span class="elk-box" role="button" tabindex="0" aria-label="sound box" style="display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;border:3px solid var(--ink);border-radius:8px;font-size:2.2rem;cursor:pointer"></span>'
        out += '<span class="no-key small" style="margin-left:10px">%s: %s</span></div>' % (w, " ".join("/%s/" % x for x in ph))
    return out


def b_rf12_sounds(lp, r):
    kinds = ["initial", "medial", "final", "segment"]
    ks = [kinds[(lp - 1 + j) % 4] for j in range(3)]
    qs, key, items, mk = [], [], [], []
    for n, k in enumerate(ks, 1):
        if k == "initial":
            w, a = INIT[(lp - 1) % len(INIT)]
            qs.append("What is the first sound in the word %s?" % w)
            key.append("%s." % a)
        elif k == "medial":
            w, a = MED[(lp - 1) % len(MED)]
            qs.append("What is the vowel sound in the middle of the word %s?" % w)
            key.append("%s." % a)
        elif k == "final":
            w, a = FINAL[(lp - 1) % len(FINAL)]
            qs.append("What is the last sound in the word %s?" % w)
            key.append("%s." % a)
        else:
            w, a = SEG[(lp - 1) % len(SEG)]
            qs.append("Say each sound in the word %s, one at a time." % w)
            key.append("%s. Every sound is said in order." % a)
            mk.append(dict(l=w, w=["/%s/" % x for x in PHON[w]], allow=0, noun="sounds"))
        items.append((n, w, PHON[w]))
    d = dict(qs=qs, key=key, dir="Your teacher says words. Use the sound boxes: one box for each sound. Tap a box as you say the sound. You do not need to read.", dur=150, html=elk_html(items), elk=True)
    if mk:
        d["mk"] = mk
        d["auto"] = False
    return d


# ================================================================ RF.1.3
DIG = ["ship", "shop", "chat", "chin", "thin", "this", "when", "whip", "much", "fish", "bath", "wish", "rich", "shut", "then", "chop"]
REG = ["stop", "frog", "jump", "nest", "flag", "drum", "crab", "trip", "swim", "plan", "grin", "clap", "milk", "hand", "lamp", "step"]
LONGV = ["cake", "bike", "hope", "cube", "like", "home", "rain", "boat", "feet", "play", "seed", "snow", "tree", "coat", "day", "mail", "rope", "five"]
TWO = ["pencil", "rabbit", "window", "basket", "napkin", "sunset", "picnic", "happy", "tiger", "finger", "kitten", "muffin"]
INFL = ["jumped", "jumping", "looks", "hunted", "walks", "helping", "wished", "lifted", "playing", "asked", "rested", "jumps"]
IRREG = ["the", "said", "were", "they", "was", "have", "come", "some", "once", "give", "could", "your"]

PHON_K = [("What sound do the letters sh make in ship?", "/sh/."), ("What sound do the letters ch make in chin?", "/ch/."), ("What sound do the letters th make in this?", "/th/."),
          ("What sound do the letters wh make in when?", "/w/."), ("What does the e at the end of cake do?", "It is silent and makes the a say its name (long a)."),
          ("What does the e at the end of bike do?", "It is silent and makes the i say its name (long i)."), ("What sound do the letters ai make in rain?", "Long a."),
          ("What sound do the letters ee make in feet?", "Long e."), ("What sound do the letters oa make in boat?", "Long o."), ("What sound do the letters ay make in play?", "Long a."),
          ("Which two letters make the /ch/ sound at the start of chop?", "c and h (ch)."), ("What sound does ck make at the end of duck?", "/k/.")]
WORD_K = [("How many vowel sounds do you hear in the word rabbit? So how many syllables are there?", "2 vowel sounds, so 2 syllables."), ("How many vowel sounds do you hear in the word pencil? So how many syllables?", "2 vowel sounds, so 2 syllables."),
          ("What ending is on the word jumped? What is the root word?", "The ending is -ed. The root word is jump."), ("What ending is on the word looking? What is the root word?", "The ending is -ing. The root word is look."),
          ("What ending is on the word walks? What is the root word?", "The ending is -s. The root word is walk."), ("How many syllables are in the word window? How do you know?", "2 syllables. There are two vowel sounds."),
          ("How many vowel sounds do you hear in the word cat? So how many syllables?", "1 vowel sound, so 1 syllable."), ("What ending is on the word helped? What is the root word?", "The ending is -ed. The root word is help."),
          ("How many syllables are in the word napkin? How do you know?", "2 syllables. There are two vowel sounds."), ("What ending is on the word playing? What is the root word?", "The ending is -ing. The root word is play."),
          ("Does every syllable have a vowel sound? Tell how you know using the word basket.", "Yes. Basket has 2 syllables and each one has a vowel sound (bas, ket)."), ("What ending is on the word wishes? What is the root word?", "The ending is -es. The root word is wish.")]


def b_rf13_kphon(lp, r):
    it = rot(PHON_K, lp)
    return dict(qs=[q for q, _ in it], key=[a for _, a in it], dir="Your teacher reads each question. Think about letters and sounds. Tell your answer out loud.", dur=140)


def b_rf13_kword(lp, r):
    it = rot(WORD_K, lp)
    return dict(qs=[q for q, _ in it], key=[a for _, a in it], dir="Your teacher reads each question. Think about word parts. Tell your answer out loud.", dur=150)


def sets5(pool, lp, j):
    n = len(pool)
    return [pool[((lp - 1) * 5 + j * 3 + k) % n] for k in range(5)]


def b_rf13_iphon(lp, r):
    sa, sb, sc = sets5(DIG, lp, 0), sets5(REG, lp, 1), sets5(LONGV, lp, 2)
    qs = ["Read the words in set %s out loud." % L for L in "ABC"]
    key = ["All 5 words read correctly: %s." % ", ".join(s) for s in (sa, sb, sc)]
    mk = [dict(l=L, w=list(x), allow=0) for L, x in zip("ABC", (sa, sb, sc))]
    return dict(qs=qs, key=key, dir="Look at the three sets of words. Read the words in each set out loud when your teacher asks.", dur=140, html=pills_html([("A", sa), ("B", sb), ("C", sc)]), mk=mk, auto=True)


TXT_PHON = ["We rode the bike to the lake.", "Beth ate fish on the beach.", "The boat floats on the pond.", "I like to play in the rain.", "Chip has a big shell.", "Dad made a cake for me.", "The green tree has a nest.", "We hope it will snow.", "The coat is on the chair.", "The mail came in the rain.", "Seth got a thin white rope.", "The ship will sail at six."]
TXT_WORD = ["The rabbit jumped in the basket.", "Mom is helping me pack a picnic.", "The kitten napped by the window.", "We played tag at sunset.", "He asked for a muffin.", "The tiger rested in the shade.", "Dad is fixing my pencil.", "She looked at the happy tiger.", "The rabbit hunted for a carrot.", "We are jumping on the trampoline."]


def b_rf13_tphon(lp, r):
    it = rot(TXT_PHON, lp)
    qs = ["Read sentence %s out loud." % L for L in "ABC"]
    key = ["Reads every word correctly: %s" % s for s in it]
    mk = [dict(l=L, t=x, allow=0) for L, x in zip("ABC", it)]
    return dict(qs=qs, key=key, dir="Look at the three sentences. Read each one out loud when your teacher asks.", dur=140, html=lines_html(list(zip("ABC", it))), mk=mk, auto=True)


def b_rf13_iword(lp, r):
    sa, sb, sc = sets5(TWO, lp, 0), sets5(INFL, lp, 1), sets5(IRREG, lp, 2)
    qs = ["Read the words in set %s out loud." % L for L in "ABC"]
    key = ["All 5 words read correctly: %s." % ", ".join(s) for s in (sa, sb, sc)]
    mk = [dict(l=L, w=list(x), allow=0) for L, x in zip("ABC", (sa, sb, sc))]
    return dict(qs=qs, key=key, dir="Look at the three sets of words. Read the words in each set out loud when your teacher asks.", dur=140, html=pills_html([("A", sa), ("B", sb), ("C", sc)]), mk=mk, auto=True)


def b_rf13_tword(lp, r):
    it = rot(TXT_WORD, lp)
    qs = ["Read sentence %s out loud." % L for L in "ABC"]
    key = ["Reads every word correctly: %s" % s for s in it]
    mk = [dict(l=L, t=x, allow=0) for L, x in zip("ABC", it)]
    return dict(qs=qs, key=key, dir="Look at the three sentences. Read each one out loud when your teacher asks.", dur=140, html=lines_html(list(zip("ABC", it))), mk=mk, auto=True)


# ================================================================ RF.1.4
ACC = ["Ben and Pam go to the lake. They get in a red boat. The boat is not big.", "A fox ran up the hill. It saw a hen in the grass. The hen did not run.",
       "Jen has a pet frog. The frog can jump far. It hops on a log.", "Dad made a big snack. We ate it on the porch. It was so good.",
       "I see a ship at sea. The ship has a flag. The flag is blue.", "The sun is up. Kids run to the park. They play on the swings.",
       "Mom got a new plant. She put it by the window. It likes the sun.", "My dog digs in the sand. He finds a stick. Then he runs back to me.",
       "A duck swims in the pond. Her babies swim too. They quack and quack.", "We bake a cake at home. Dad stirs in the milk. Then we wait for it."]
FLU = ["Can you see the moon? It is up in the sky! It is big and bright.", "Look at that fish! Is it a big one? Yes, it is huge!",
       "Where is my hat? I put it on the bed. Oh, here it is!", "Do you like rain? I like to jump in it. Splash, splash, splash!",
       "A bee sat on my arm! Dad said to stay still. It flew away.", "Who can run fast? I can run fast! Let us race to the tree.",
       "Is it time to eat? Yes, it is! We will have soup and bread.", "Wow, look at the snow! Can we go out? Get your hat and coat.",
       "Will you help me dig? We can plant a seed. It will grow big!", "What is in the box? It is a gift! Open it and see."]


def b_rf14_acc(lp, r):
    ps = rot(ACC, lp)
    for p in ps:
        check_student(p)
    qs = ["Read passage %s out loud." % L for L in "ABC"]
    key = []
    for L, p in zip("ABC", ps):
        n = wc(p)
        key.append("%d words. Count the words read correctly. At least %d of %d (95 percent) is accurate. Note any word that was skipped, changed, or sounded out wrongly. If the student rereads to fix a word, that is self-correcting." % (n, int(round(n * 0.95 + 0.4)), n))
    html = lines_html(list(zip("ABC", ps)))
    mk = [dict(l=L, t=p, timed=True, allow=wc(p) - int(round(wc(p) * 0.95 + 0.4))) for L, p in zip("ABC", ps)]
    return dict(qs=qs, key=key, dir="Look at the three short passages. Read each one out loud when your teacher asks.", dur=200, html=html, mk=mk, auto=True)


def b_rf14_flu(lp, r):
    ps = rot(FLU, lp)
    qs = ["Read passage %s out loud. Make it sound like talking." % L for L in "ABC"]
    key = []
    for L, p in zip("ABC", ps):
        key.append("%d words. Listen for: smooth reading (not word by word), a pause at each period, voice going up at a question mark, and strong voice at an exclamation mark. Use the timer under the passage to get words correct per minute." % wc(p))
    mk = [dict(l=L, t=p, timed=True, allow=wc(p) - int(round(wc(p) * 0.95 + 0.4))) for L, p in zip("ABC", ps)]
    return dict(qs=qs, key=key, dir="Look at the three short passages. Read each one out loud like you are talking, when your teacher asks.", dur=200, html=lines_html(list(zip("ABC", ps))), mk=mk, auto=False)


# ================================================================ SL.1.4
PEOPLE = ["your best friend", "someone in your family", "your teacher", "a helper in your town", "a person you like to play with", "a neighbor", "a character from a book", "someone who is funny", "someone who is kind", "a person you admire"]
PLACES = ["your bedroom", "the park", "your kitchen", "a place you like to visit", "the library", "the grocery store", "a beach or a lake", "the playground", "your yard", "a place that is quiet"]
THINGS = ["your favorite toy", "a pet or an animal you like", "something in your room", "your favorite food", "something you use every day", "a tool in the kitchen", "a piece of clothing you like", "a book you own", "a sport ball", "something that is round"]
EVENTS = ["your last birthday", "a trip you took", "what you did yesterday", "a time you were at a party", "a day at school", "a time it rained", "a holiday", "a time you cooked something", "a time you played outside", "a time you met someone new"]
IDEAS = ["what you think is the best way to spend a weekend", "why people need friends", "what you want to be when you grow up", "what makes a good pet", "why it is good to share", "what you would do on a snow day", "why we need sleep", "what makes a good game", "what you would build if you could build anything", "why we should be kind"]
FEEL = ["a time you felt happy", "a time you felt nervous", "a time you felt proud", "a time you felt surprised", "a time you felt sad", "a time you felt excited", "a time you felt silly", "a time you felt brave", "a time you felt tired", "a time you felt left out"]


def mk_sl4(pool, what, lookfor, dir_):
    def b(lp, r):
        tp = rot(pool, lp)
        qs = ["Tell me about %s." % t if what != "feel" else "Tell me about %s. What happened and how did you feel?" % t for t in tp]
        key = [lookfor for _ in tp]
        return dict(qs=qs, key=key, dir=dir_, dur=170)
    return b


b_sl4_people = mk_sl4(PEOPLE, "p", "Look for: a clear picture of the person with at least 2 relevant details (looks, actions, what they like), in complete sentences, spoken so the listener can follow.", "Your teacher asks you to tell about a person. Speak in full sentences and give details.")
b_sl4_places = mk_sl4(PLACES, "pl", "Look for: a clear picture of the place with at least 2 relevant details (what is there, what it looks like, what you do), in complete sentences.", "Your teacher asks you to tell about a place. Speak in full sentences and give details.")
b_sl4_things = mk_sl4(THINGS, "t", "Look for: a clear picture of the thing with at least 2 relevant details (what it looks like, what it does, why it matters), in complete sentences.", "Your teacher asks you to tell about a thing. Speak in full sentences and give details.")
b_sl4_events = mk_sl4(EVENTS, "e", "Look for: what happened in an order that makes sense, with at least 2 relevant details (who, where, what), in complete sentences.", "Your teacher asks you to tell about an event. Speak in full sentences and give details.")


def b_sl4_ideas(lp, r):
    tp = rot(IDEAS, lp)
    qs = ["Tell me %s. Explain your idea so I understand." % t for t in tp]
    key = ["Look for: the idea is stated clearly, with a reason or example, spoken in complete sentences so the listener can follow." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher asks you to share your ideas. Say your idea clearly and tell why.", dur=170)


def b_sl4_feel(lp, r):
    tp = rot(FEEL, lp)
    qs = ["Tell me about %s. What happened and how did you feel?" % t for t in tp]
    key = ["Look for: the feeling is named (for example happy, nervous) and tied to what happened, in complete sentences, spoken clearly." for _ in tp]
    return dict(qs=qs, key=key, dir="Your teacher asks you to share your feelings. Say how you felt and tell why.", dur=170)


# ================================================================ SL.1.2 (teacher reads aloud)
def sl2_ask(bank, kind):
    def b(lp, r):
        t, x, facts = bank[lp % 10 + 1]
        st = starters(facts)
        qs = ["Ask me a question that starts with %s about the %s I read." % (s, kind) for s, _, _ in st]
        key = ["Read this aloud once, and again if the student asks: %s | Any real question that starts with %s about the %s. For example: %s (%s)" % (x, s, kind, q, a) if i == 0
               else "Any real question that starts with %s about the %s. For example: %s (%s)" % (s, kind, q, a) for i, (s, q, a) in enumerate(st)]
        return dict(qs=qs, key=key, dir="Your teacher reads a %s out loud. Listen carefully. Then make up questions about it and say them out loud. You do not need to read." % kind, dur=170)
    return b


def sl2_answer(bank, kind):
    def b(lp, r):
        t, x, facts = bank[lp % 10 + 1]
        st = starters(facts)
        qs = [q for _, q, _ in st]
        key = ["Read this aloud once, and again if the student asks: %s | %s." % (x, a) if i == 0 else "%s." % a for i, (_, _, a) in enumerate(st)]
        return dict(qs=qs, key=key, dir="Your teacher reads a %s out loud. Listen carefully. Then answer the questions out loud. You do not need to read." % kind, dur=170)
    return b


# ================================================================ L.1.1
def pairs(lst, lp):
    return rot(lst, lp)


def mk_l(pool, dur=140):
    def b(lp, r):
        it = rot(pool, lp)
        return dict(qs=[q for q, _ in it], key=[a for _, a in it], dir=LEFT, dur=dur)
    return b


NOUNS = [("Which word is a proper noun, the name of one special person: girl or Mia?", "Mia."), ("Which word is a common noun: dog or Max?", "Dog."), ("Which word names a place: park or ran?", "Park."),
         ("Which word shows that the ball belongs to Sam: Sam's or Sams?", "Sam's (possessive noun)."), ("Which word names a thing: apple or jump?", "Apple."), ("Which word is the name of a person: teacher or sing?", "Teacher."),
         ("Which word is a proper noun: city or Chicago?", "Chicago."), ("Which one means the hat belongs to the girl: girl's hat or girls hat?", "Girl's hat."), ("Which word is a common noun: Pam or girl?", "Girl."),
         ("Tell me one common noun and one proper noun.", "Any common noun (a kind of thing, like dog) and any name (like Max)."), ("Which word names an animal: duck or run?", "Duck."), ("Which is right: the dogs bone or the dog's bone?", "The dog's bone.")]
PLUR = [("Which sounds right: The dogs run or the dogs runs?", "The dogs run."), ("Which sounds right: He hops or he hop?", "He hops."), ("Which sounds right: We hop or we hops?", "We hop."),
        ("Which sounds right: The cat jumps or the cat jump?", "The cat jumps."), ("Make the word box mean more than one.", "Boxes."), ("Make the word dog mean more than one.", "Dogs."),
        ("Which sounds right: The birds sing or the birds sings?", "The birds sing."), ("Which sounds right: She plays or she play?", "She plays."), ("Make the word dish mean more than one.", "Dishes."),
        ("Which sounds right: The children play or the children plays?", "The children play."), ("Which sounds right: They run or they runs?", "They run."), ("Make the word cup mean more than one.", "Cups.")]
PRON = [("Mia is my friend. ___ is kind. Which word fits: She or Her?", "She."), ("Give the toy to ___. Which word fits: I or me?", "Me."), ("That is ___ book. It belongs to me. Which word fits: my or me?", "My."),
        ("Tom and Sam ran. ___ ran fast. Which word fits: They or Them?", "They."), ("Look at the dog. Pet ___. Which word fits: it or they?", "It."), ("Which sounds right: Me see a duck or I see a duck?", "I see a duck."),
        ("Is ___ at the door? Which word fits: anyone or any?", "Anyone."), ("Dan lost ___ hat. Which word fits: his or him?", "His."), ("The kids ate. ___ were full. Which word fits: They or Them?", "They."),
        ("Give the book to ___. It belongs to them. Which word fits: they or them?", "Them."), ("The girls shared ___ toys. Which word fits: their or they?", "Their."), ("___ can help me. Which word fits: Everyone or Every?", "Everyone.")]
TENSE = [("Today I walk. Yesterday I ___.", "Walked."), ("Today I jump. Tomorrow I ___ jump.", "Will."), ("Say this sentence in the past: I play outside today.", "I played outside yesterday (or I played outside)."),
         ("Say this sentence about tomorrow: I wash the dish today.", "I will wash the dish tomorrow."), ("Today I look. Yesterday I ___.", "Looked."), ("Which is about the past: I cook or I cooked?", "I cooked."),
         ("Which is about the future: I will help or I helped?", "I will help."), ("Today I climb. Yesterday I ___.", "Climbed."), ("Say this in the future: I paint a picture today.", "I will paint a picture."),
         ("Which tells about right now: She walks or she walked?", "She walks."), ("Today we clean. Yesterday we ___.", "Cleaned."), ("Say this sentence in the past: We help Mom today.", "We helped Mom.")]
ADJ = [("In the big red ball, which words tell what the ball is like?", "Big and red."), ("Which word tells what the cat is like: The soft cat?", "Soft."), ("Say a word that tells what the sun is like.", "Any describing word (hot, bright, yellow)."),
       ("In the tall green tree, which words are adjectives?", "Tall and green."), ("Which word tells how many: three dogs?", "Three."), ("Add a word to tell about the dog: The ___ dog ran.", "Any adjective (big, brown, fast)."),
       ("Which word tells what the soup is like: The hot soup?", "Hot."), ("Tell me a word that describes snow.", "Any describing word (cold, white, soft)."), ("Which word tells about the shoe: The wet shoe?", "Wet."),
       ("In a small blue cup, which words describe the cup?", "Small and blue."), ("Which word tells about the cake: The sweet cake?", "Sweet."), ("Add a word to tell about the bird: The ___ bird sang.", "Any adjective (little, red, loud).")]
CONJ = [("I like cake ___ pie. Which word fits: and or but?", "And."), ("I like tea ___ I do not like milk. Which word fits: but or and?", "But."), ("We can run ___ walk. Which word fits: or or so?", "Or."),
        ("It rained, ___ we stayed home. Which word fits: so or or?", "So."), ("I smiled ___ I was happy. Which word fits: because or but?", "Because."), ("Finish it: I put on a coat because ___.", "Any real reason (it was cold)."),
        ("I want a snack ___ I am hungry. Which word fits: because or or?", "Because."), ("Join the sentences with and: I like dogs. I like cats.", "I like dogs and cats."), ("I am tired, ___ I will go to bed. Which word fits: so or but?", "So."),
        ("The sun is out, ___ it is cold. Which word fits: but or because?", "But."), ("Do you want milk ___ juice? Which word fits: or or and?", "Or."), ("Finish it: I like to swim, but ___.", "Any contrast (I do not like cold water).")]
DET = [("I see ___ apple. Which word fits: a or an?", "An."), ("I see ___ dog. Which word fits: a or an?", "A."), ("___ is my hat, right here in my hand. Which word fits: This or Those?", "This."),
       ("Look at ___ birds far away. Which word fits: that or those?", "Those."), ("___ cookie in my hand is good. Which word fits: This or These?", "This."), ("I ate ___ orange. Which word fits: a or an?", "An."),
       ("Which is right: The dog ran or Dog ran?", "The dog ran."), ("Look at ___ flowers right here by me. Which word fits: these or that?", "These."), ("Give me ___ pencil over there. Which word fits: that or these?", "That."),
       ("She has ___ umbrella. Which word fits: a or an?", "An."), ("___ shoes on my feet are new. Which word fits: These or That?", "These."), ("I want ___ ball on the shelf, the one far away. Which word fits: that or this?", "That.")]
PREP = [("The ball went ___ the fence. Which word fits: beyond or during?", "Beyond."), ("We play outside ___ recess. Which word fits: during or toward?", "During."), ("The dog ran ___ me. Which word fits: toward or during?", "Toward."),
        ("The cat is ___ the box. Which word fits: in or because?", "In."), ("The book is ___ the table. Which word fits: on or and?", "On."), ("We walked ___ the store. Which word fits: to or but?", "To."),
        ("The bird flew ___ the tree. Which word fits: over or so?", "Over."), ("The sock fell ___ the bed. Which word fits: under or or?", "Under."), ("Tell me where the pencil is. Use on, in, or under.", "Any sentence with a place word that makes sense."),
        ("The kids sleep ___ the night. Which word fits: during or beyond?", "During."), ("The mouse hid ___ the chair. Which word fits: behind or but?", "Behind."), ("We walked ___ the park. Which word fits: through or because?", "Through.")]
SENT = [("Make this sentence longer: The dog ran.", "Any longer sentence that keeps the idea (The big dog ran fast)."), ("Is this a complete sentence: Ran fast. Why or why not?", "No. It does not tell who ran."),
        ("Turn this into a question: You are tired.", "Are you tired?"), ("Turn this into a telling sentence: Is the cat sleeping?", "The cat is sleeping."), ("Join these two sentences with and: I like pizza. I like tacos.", "I like pizza and I like tacos."),
        ("Say a sentence that shows a strong feeling.", "An exclamation, such as I won the game! (strong feeling, spoken with feeling)."), ("Give a command to a friend.", "An imperative, such as Please sit down."),
        ("Which is a complete sentence: The bird or The bird sang?", "The bird sang."), ("Make this sentence longer: Mom cooked.", "Any longer sentence that keeps the idea (Mom cooked soup for dinner)."),
        ("Turn this into a question: She can swim.", "Can she swim?"), ("Join these two sentences with but: I like rain. I do not like wind.", "I like rain, but I do not like wind."), ("Say a complete sentence about your day.", "Any complete sentence with a who and a what.")]


def b_l_print(lp, r):
    groups = ["A to I", "J to R", "S to Z"]
    lgroups = ["a to i", "j to r", "s to z"]
    qs = ["Print the capital letters %s on your paper." % groups[(lp - 1) % 3],
          "Print the lowercase letters %s on your paper." % lgroups[lp % 3],
          "Print your first and last name on your paper. Use capital and lowercase letters."]
    key = ["Look for: every letter is a capital, made the right way, starting at the top, and sitting on the line. Note any reversals.",
           "Look for: every letter is lowercase, made the right way, with tall and short letters sized correctly. Note any reversals.",
           "Look for: a capital at the start of each name, lowercase after, letters formed correctly, spaced evenly."]
    return dict(qs=qs, key=key, dir="Your teacher reads each question. Print the letters on your paper.", dur=240, mats=["a pencil and paper"])


BUILD = {
    ("RL.1.1", "ask"): story_ask(LIT, "story"), ("RL.1.1", "answer"): story_answer(LIT, "story"),
    ("RI.1.1", "ask"): story_ask(INFO, "text"), ("RI.1.1", "answer"): story_answer(INFO, "text"),
    ("W.1.1", "whole"): b_w1_whole, ("W.1.1", "intro"): b_w1_intro, ("W.1.1", "state"): b_w1_state, ("W.1.1", "reason"): b_w1_reason, ("W.1.1", "close"): b_w1_close,
    ("W.1.2", "whole"): b_w2_whole, ("W.1.2", "topic"): b_w2_topic, ("W.1.2", "facts"): b_w2_facts, ("W.1.2", "close"): b_w2_close,
    ("W.1.3", "whole"): b_w3_whole, ("W.1.3", "events"): b_w3_events, ("W.1.3", "details"): b_w3_details, ("W.1.3", "temporal"): b_w3_temporal, ("W.1.3", "close"): b_w3_close,
    ("RF.1.1", "org"): b_rf11_org, ("RF.1.1", "basic"): b_rf11_basic,
    ("RF.1.2", "words"): b_rf12_words, ("RF.1.2", "syl"): b_rf12_syl, ("RF.1.2", "sounds"): b_rf12_sounds,
    ("RF.1.3", "kphon"): b_rf13_kphon, ("RF.1.3", "kword"): b_rf13_kword, ("RF.1.3", "iphon"): b_rf13_iphon, ("RF.1.3", "tphon"): b_rf13_tphon, ("RF.1.3", "iword"): b_rf13_iword, ("RF.1.3", "tword"): b_rf13_tword,
    ("RF.1.4", "acc"): b_rf14_acc, ("RF.1.4", "flu"): b_rf14_flu,
    ("SL.1.2", "ask"): sl2_ask(LIT, "story"), ("SL.1.2", "answer"): sl2_answer(INFO, "text"),
    ("SL.1.4", "people"): b_sl4_people, ("SL.1.4", "places"): b_sl4_places, ("SL.1.4", "things"): b_sl4_things, ("SL.1.4", "events"): b_sl4_events, ("SL.1.4", "ideas"): b_sl4_ideas, ("SL.1.4", "feel"): b_sl4_feel,
    ("L.1.1", "print"): b_l_print, ("L.1.1", "nouns"): mk_l(NOUNS), ("L.1.1", "plural"): mk_l(PLUR), ("L.1.1", "pron"): mk_l(PRON), ("L.1.1", "tense"): mk_l(TENSE), ("L.1.1", "adj"): mk_l(ADJ),
    ("L.1.1", "conj"): mk_l(CONJ), ("L.1.1", "det"): mk_l(DET), ("L.1.1", "prep"): mk_l(PREP), ("L.1.1", "sent"): mk_l(SENT),
}

CAT = {
    "RL.1.1": {"desc": "asking and answering questions about key details in a story", "parts": [
        ("ask", "Ask questions about key details in a story", "Asking questions about key details in a story"),
        ("answer", "Answer questions about key details in a story", "Answering questions about key details in a story")]},
    "RI.1.1": {"desc": "asking and answering questions about key details in an informational text", "parts": [
        ("ask", "Ask questions about key details in an informational text", "Asking questions about key details in an informational text"),
        ("answer", "Answer questions about key details in an informational text", "Answering questions about key details in an informational text")]},
    "W.1.1": {"desc": "writing an opinion piece", "parts": [
        ("whole", "Write an opinion piece", "Writing an opinion piece with an opinion, a reason, and a closing"),
        ("intro", "Introduce the topic or name the book", "Introducing the topic or naming the book in an opinion piece"),
        ("state", "State an opinion", "Stating an opinion in an opinion piece"),
        ("reason", "Give a reason for the opinion", "Giving a reason for the opinion"),
        ("close", "Provide a sense of closure", "Providing a sense of closure in an opinion piece")]},
    "W.1.2": {"desc": "writing an informative or explanatory text", "parts": [
        ("whole", "Write an informative text", "Writing an informative text that names a topic, gives facts, and has a closing"),
        ("topic", "Name the topic", "Naming the topic in an informative text"),
        ("facts", "Supply some facts about the topic", "Supplying some facts about the topic"),
        ("close", "Provide a sense of closure", "Providing a sense of closure in an informative text")]},
    "W.1.3": {"desc": "writing a narrative", "parts": [
        ("whole", "Write a narrative", "Writing a narrative with events in order, details, time words, and a closing"),
        ("events", "Recount two or more events in order", "Recounting two or more appropriately sequenced events"),
        ("details", "Include details about what happened", "Including some details regarding what happened"),
        ("temporal", "Use time words to show the order", "Using temporal words to signal event order"),
        ("close", "Provide a sense of closure", "Providing a sense of closure in a narrative")]},
    "RF.1.1": {"desc": "understanding the organization and basic features of print", "parts": [
        ("org", "Organization of print", "Understanding the organization of print (first word, last word, words in a sentence)"),
        ("basic", "Basic features of print", "Understanding the basic features of a sentence (capital letter, end mark)")]},
    "RF.1.2": {"desc": "understanding spoken words, syllables, and sounds", "parts": [
        ("words", "Spoken words", "Blending sounds into spoken words and telling long from short vowel sounds"),
        ("syl", "Syllables", "Telling the number of syllables in spoken words"),
        ("sounds", "Sounds (phonemes)", "Isolating and segmenting the sounds (phonemes) in spoken words")]},
    "RF.1.3": {"desc": "grade-level phonics and word analysis skills", "parts": [
        ("kphon", "Know grade-level phonics", "Knowing grade-level phonics skills (digraphs, final e, vowel teams)"),
        ("kword", "Know grade-level word analysis", "Knowing grade-level word analysis skills (syllables and endings)"),
        ("iphon", "Decode phonics words alone", "Decoding words with grade-level phonics skills in isolation"),
        ("tphon", "Decode phonics words in a sentence", "Decoding words with grade-level phonics skills in text"),
        ("iword", "Decode word analysis words alone", "Decoding words with grade-level word analysis skills in isolation"),
        ("tword", "Decode word analysis words in a sentence", "Decoding words with grade-level word analysis skills in text")]},
    "RF.1.4": {"desc": "reading with accuracy and fluency to support comprehension", "parts": [
        ("acc", "Read with accuracy", "Reading on-level text with sufficient accuracy"),
        ("flu", "Read with fluency", "Reading on-level text with sufficient fluency (smooth, with expression)")]},
    "SL.1.2": {"desc": "asking and answering questions about a text read aloud", "parts": [
        ("ask", "Ask questions about key details read aloud", "Asking questions about key details in a text read aloud"),
        ("answer", "Answer questions about key details read aloud", "Answering questions about key details in a text read aloud")]},
    "SL.1.4": {"desc": "describing with relevant details when speaking", "parts": [
        ("people", "Describe people", "Describing people with relevant details when speaking"),
        ("places", "Describe places", "Describing places with relevant details when speaking"),
        ("things", "Describe things", "Describing things with relevant details when speaking"),
        ("events", "Describe events", "Describing events with relevant details when speaking"),
        ("ideas", "Express ideas clearly", "Expressing ideas clearly when speaking"),
        ("feel", "Express feelings clearly", "Expressing feelings clearly when speaking")]},
    "L.1.1": {"desc": "the conventions of standard English grammar and usage", "parts": [
        ("print", "Print upper- and lowercase letters", "Printing all upper- and lowercase letters"),
        ("nouns", "Common, proper, and possessive nouns", "Using common, proper, and possessive nouns"),
        ("plural", "Singular and plural nouns with matching verbs", "Using singular and plural nouns with matching verbs"),
        ("pron", "Pronouns", "Using personal, possessive, and indefinite pronouns"),
        ("tense", "Past, present, and future verbs", "Using verbs to show past, present, and future"),
        ("adj", "Adjectives", "Using frequently occurring adjectives"),
        ("conj", "Conjunctions", "Using frequently occurring conjunctions"),
        ("det", "Determiners", "Using determiners (articles and demonstratives)"),
        ("prep", "Prepositions", "Using frequently occurring prepositions"),
        ("sent", "Produce and expand sentences", "Producing and expanding complete sentences")]},
}

APPLY = r"""Object.keys(G1ELA).forEach(function(std){A({std:std,op:"strands",make:function(lp){return G1ELA[std][String(lp)].map(function(s){var o={std:std,strand:s.id,title:s.title,n:3,dur:s.dur,dir:s.dir,desc:s.desc,rows:s.qs.map(function(q,j){return[q,s.key[j]]})};if(s.mats&&s.mats.length)o.mats=s.mats;if(s.html){(function(h){o.html=function(){return h}})(s.html)}var p=P(o);if(s.mk||s.elk){p.after=function(v,ctx){if(s.elk)TPELK(v,ctx);if(s.mk)TPMARK(v,ctx,s.mk,s.auto)}}return p})}})});"""


def build():
    out = {}
    for std, c in CAT.items():
        for lp in range(1, 11):
            parts = []
            for pid, label, desc in c["parts"]:
                d = BUILD[(std, pid)](lp, rng_for(lp, std + pid))
                assert len(d["qs"]) == 3 and len(d["key"]) == 3, (std, pid, lp)
                for t in d["qs"] + d["key"] + [d["dir"]] + ([d["html"]] if d.get("html") else []):
                    assert not BAD.search(t), (std, pid, lp, t[:80])
                part = {"id": pid, "title": label, "desc": desc, "qs": d["qs"], "key": d["key"], "dir": d["dir"], "dur": d["dur"]}
                if d.get("html"):
                    part["html"] = d["html"]
                if d.get("mats"):
                    part["mats"] = d["mats"]
                if d.get("elk"):
                    part["elk"] = True
                if d.get("mk"):
                    part["mk"] = d["mk"]
                    part["auto"] = bool(d.get("auto"))
                parts.append(part)
            out.setdefault(std, {})[str(lp)] = parts
    return out


TPMARK_JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tpmark.js"), encoding="utf8").read()


def js(data):
    L = ["/* G1ELA-STRANDS-BEGIN (generated by source/tools/gen_g1ela.py, edit the generator, not this block) */",
         "window.TP_STRANDS=window.TP_STRANDS||{};"]
    for std, cat in CAT.items():
        L.append("window.TP_STRANDS[%s]=%s;" % (json.dumps(std), json.dumps({"desc": cat["desc"], "parts": [{"id": p[0], "label": p[1], "desc": p[2]} for p in cat["parts"]]}, ensure_ascii=False)))
    L.append(TPMARK_JS)
    L.append("var G1ELA=%s;" % json.dumps(data, ensure_ascii=False))
    L.append(APPLY)
    L.append("/* G1ELA-STRANDS-END */")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block and "–" not in block
    src = open(G1, encoding="utf8").read()
    if "G1ELA-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* G1ELA-STRANDS-BEGIN.*?G1ELA-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        marker = "/* G1PIC-STRANDS-END */"
        assert marker in src
        src = src.replace(marker, marker + "\n" + block)
    open(G1, "w", encoding="utf8").write(src)
    print("parts:", sum(len(p) for std in data.values() for p in std.values()), "block bytes:", len(block))


if __name__ == "__main__":
    main()
