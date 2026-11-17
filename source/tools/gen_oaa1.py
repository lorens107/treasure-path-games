"""Builds the 1.OA.A.1 strand problems for Grade 1 (all 10 LPs) and writes them into source/gx/g1.js.

Run from anywhere:  python3 source/tools/gen_oaa1.py
It checks every problem (known numbers appear in the text, answer is 1 to 20, no em dashes)
and rewrites the block between the OAA1 markers in g1.js.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
G1 = os.path.join(HERE, '..', 'gx', 'g1.js')

STRANDS = [
    ("addto",   "Adding to",
     "Addition: word problems about adding to, with the result, the change, or the start unknown"),
    ("addpt",   "Putting together or taking apart (addition)",
     "Addition: word problems about putting together or taking apart, with the total, one part, or both parts unknown"),
    ("addcmp",  "Comparing (addition)",
     "Addition: compare word problems, with the difference or the bigger amount unknown"),
    ("subfrom", "Taking from",
     "Subtraction: word problems about taking from, with the result, the change, or the start unknown"),
    ("subpt",   "Putting together or taking apart (subtraction)",
     "Subtraction: word problems about putting together or taking apart, with one part or both parts unknown"),
    ("subcmp",  "Comparing (subtraction)",
     "Subtraction: compare word problems, with the difference or the smaller amount unknown"),
]

# type code -> (strand index, key tag)
TYPES = ["AR", "AC", "AS", "PT", "PA", "PB", "CDA", "CB", "CBF",
         "TR", "TC", "TS", "S1", "S2", "S3", "CDS", "CS", "CSF"]
TAG = {"AR": "Result unknown", "AC": "Change unknown", "AS": "Start unknown",
       "PT": "Total unknown", "PA": "One part unknown", "PB": "Both parts unknown",
       "CDA": "Difference unknown", "CB": "Bigger unknown", "CBF": "Bigger unknown, fewer wording",
       "TR": "Result unknown", "TC": "Change unknown", "TS": "Start unknown",
       "S1": "One part unknown", "S2": "One part unknown, other part given",
       "S3": "Both parts unknown",
       "CDS": "Difference unknown", "CS": "Smaller unknown", "CSF": "Smaller unknown, fewer wording"}

# Each problem: (known numbers in the order shown below, unit, text)
#  AR(a,b)  a+b=?        AC(a,c)  a+?=c       AS(b,c)  ?+b=c
#  PT(a,b)  a+b=?        PA(a,c)  a+?=c       PB(c)    any pair
#  CDA(a,c) a+?=c        CB(a,b)  a+b=?       CBF(a,b) a+b=?
#  TR(a,b)  a-b=?        TC(a,c)  a-?=c       TS(b,c)  ?-b=c
#  S1(c,a)  c-a=?        S2(c,b)  c-?=b       S3(c)    any pair
#  CDS(a,c) c-a=?        CS(c,b)  c-b=?       CSF(c,b) c-b=?
LP = {
1: [  # Treasure Map
 ((6, 5), "coins", "Eli finds 6 gold coins on the beach. Then he finds 5 more coins in the sand. How many coins does Eli have now?"),
 ((8, 14), "shells", "Rosa has 8 shells in her bucket. She finds some more shells. Now she has 14 shells. How many shells did she find?"),
 ((5, 13), "gems", "Some gems were in the treasure chest. Kai put in 5 more gems. Now there are 13 gems in the chest. How many gems were in the chest at the start?"),
 ((7, 8), "flags", "Lee has 7 red flags and 8 blue flags on his treasure map. How many flags does Lee have in all?"),
 ((9, 16), "silver coins", "There are 16 coins in the chest. 9 coins are gold. The rest are silver. How many coins are silver?"),
 ((12,), "gems", "Tam has 12 gems. He puts some in a red box and the rest in a blue box. How many gems could be in each box? Show one way."),
 ((7, 15), "shells", "Mia has 7 shells. Ben has 15 shells. How many more shells does Mia need to have as many as Ben?"),
 ((9, 4), "coins", "Ana has 4 more coins than Ben. Ben has 9 coins. How many coins does Ana have?"),
 ((6, 5), "keys", "Leo has 5 fewer keys than Zoe. Leo has 6 keys. How many keys does Zoe have?"),
 ((13, 5), "gems", "A treasure chest has 13 gems. Pia takes out 5 gems. How many gems are left in the chest?"),
 ((15, 9), "ropes", "The crew has 15 ropes. They use some ropes to tie up the boat. Now 9 ropes are left. How many ropes did they use?"),
 ((4, 10), "coins", "Some coins were in a bag. Omar spent 4 coins. Now there are 10 coins in the bag. How many coins were in the bag at the start?"),
 ((14, 6), "shells", "There are 14 shells in two buckets. 6 shells are in the red bucket. How many shells are in the blue bucket?"),
 ((17, 9), "green gems", "There are 17 gems in all. Some are green. 9 are blue. How many gems are green?"),
 ((10,), "coins", "Dev puts 10 coins in his two pockets. How many coins could be in each pocket? Use subtraction to show one way."),
 ((8, 17), "flags", "Noor has 8 flags. Gus has 17 flags. How many more flags does Gus have than Noor?"),
 ((16, 7), "coins", "Ivy has 7 more coins than Jin. Ivy has 16 coins. How many coins does Jin have?"),
 ((14, 6), "maps", "Jin has 6 fewer maps than Ivy. Ivy has 14 maps. How many maps does Jin have?"),
],
2: [  # Apple Orchard
 ((4, 9), "apples", "Kai picks 4 apples from the low branch. Then he picks 9 more apples. How many apples does Kai have now?"),
 ((7, 15), "jars", "Rosa has 7 jars of jam. She makes some more jars. Now she has 15 jars. How many jars did she make?"),
 ((6, 14), "apples", "Some apples were in the basket. Lee put in 6 more apples. Now there are 14 apples in the basket. How many apples were in the basket at the start?"),
 ((8, 7), "trees", "The orchard has 8 red apple trees and 7 green apple trees. How many apple trees is that in all?"),
 ((6, 13), "green apples", "There are 13 apples on the table. 6 are red. The rest are green. How many apples are green?"),
 ((11,), "apples", "Mia has 11 apples. She puts some in a red bag and the rest in a green bag. How many apples could be in each bag? Show one way."),
 ((9, 16), "apples", "Tam has 9 apples. Zoe has 16 apples. How many more apples does Tam need to have as many as Zoe?"),
 ((7, 5), "apples", "Ana has 5 more apples than Sam. Sam has 7 apples. How many apples does Ana have?"),
 ((8, 6), "pears", "Sam has 6 fewer pears than Ana. Sam has 8 pears. How many pears does Ana have?"),
 ((14, 6), "apples", "Maya has 14 apples. She gives 6 apples to her friends. How many apples does Maya have left?"),
 ((16, 9), "bees", "There were 16 bees on the apple blossoms. Some bees flew away. Now 9 bees are on the blossoms. How many bees flew away?"),
 ((5, 8), "pears", "Some pears were in the crate. The cook took out 5 pears. Now there are 8 pears in the crate. How many pears were in the crate at the start?"),
 ((15, 7), "apples", "There are 15 apples in two baskets. 7 apples are in the big basket. How many apples are in the small basket?"),
 ((18, 11), "old trees", "A farmer has 18 apple trees in all. Some trees are old. 11 trees are young. How many trees are old?"),
 ((12,), "pears", "Gus puts 12 pears in two boxes. How many pears could be in each box? Use subtraction to show one way."),
 ((6, 14), "jugs", "Pim has 6 jugs of cider. Eli has 14 jugs. How many more jugs does Eli have than Pim?"),
 ((15, 6), "jars", "Eli has 6 more jars than Pim. Eli has 15 jars. How many jars does Pim have?"),
 ((13, 5), "apples", "Pim has 5 fewer apples than Eli. Eli has 13 apples. How many apples does Pim have?"),
],
3: [  # Pumpkin Patch
 ((9, 8), "pumpkins", "Ivy has 9 pumpkins in her wagon. She puts 8 more pumpkins in the wagon. How many pumpkins are in the wagon now?"),
 ((6, 15), "sunflowers", "Gus has 6 sunflowers. He picks some more sunflowers. Now he has 15 sunflowers. How many sunflowers did he pick?"),
 ((7, 16), "crows", "Some crows sat on the fence. Then 7 more crows came. Now there are 16 crows. How many crows were on the fence at the start?"),
 ((9, 5), "pumpkins", "The farm stand has 9 round pumpkins and 5 tall pumpkins. How many pumpkins is that in all?"),
 ((8, 17), "hay bales", "There are 17 hay bales. 8 are in the barn. The rest are in the field. How many hay bales are in the field?"),
 ((9,), "corn cobs", "Nell has 9 corn cobs. She puts some in a pot and the rest in a bowl. How many corn cobs could be in each one? Show one way."),
 ((8, 15), "gourds", "Omar has 8 gourds. Lena has 15 gourds. How many more gourds does Omar need to have as many as Lena?"),
 ((6, 7), "ears of corn", "Lena has 7 more ears of corn than Omar. Omar has 6 ears of corn. How many ears of corn does Lena have?"),
 ((9, 5), "pumpkins", "Omar has 5 fewer pumpkins than Lena. Omar has 9 pumpkins. How many pumpkins does Lena have?"),
 ((15, 7), "pumpkins", "There are 15 pumpkins on the vine. Ben picks 7 pumpkins. How many pumpkins are still on the vine?"),
 ((17, 8), "ducks", "There were 17 ducks at the pond. Some ducks swam away. Now 8 ducks are at the pond. How many ducks swam away?"),
 ((6, 9), "pumpkins", "Some pumpkins were in the wagon. The kids took out 6 pumpkins. Now there are 9 pumpkins in the wagon. How many pumpkins were in the wagon at the start?"),
 ((16, 9), "white pumpkins", "There are 16 pumpkins at the patch. 9 are orange. The rest are white. How many pumpkins are white?"),
 ((13, 6), "red leaves", "Teo has 13 leaves in all. Some are red. 6 are yellow. How many leaves are red?"),
 ((14,), "seeds", "Rosa has 14 seeds in two cups. How many seeds could be in each cup? Use subtraction to show one way."),
 ((7, 16), "pumpkins", "Dev has 7 pumpkins. Luz has 16 pumpkins. How many more pumpkins does Luz have than Dev?"),
 ((14, 5), "apples", "Luz has 5 more apples than Dev. Luz has 14 apples. How many apples does Dev have?"),
 ((12, 4), "seeds", "Dev has 4 fewer seeds than Luz. Luz has 12 seeds. How many seeds does Dev have?"),
],
4: [  # Snowy Village
 ((8, 6), "snowballs", "Ruby makes 8 snowballs. Then she makes 6 more snowballs. How many snowballs does Ruby have now?"),
 ((9, 17), "snowflakes", "Leo has 9 paper snowflakes. He makes some more snowflakes. Now he has 17 snowflakes. How many snowflakes did he make?"),
 ((5, 12), "kids", "Some kids were on the hill. Then 5 more kids came. Now there are 12 kids on the hill. How many kids were on the hill at the start?"),
 ((6, 9), "sleds", "The village has 6 red sleds and 9 blue sleds. How many sleds is that in all?"),
 ((7, 15), "red hats", "There are 15 hats on the hooks. 7 hats are green. The rest are red. How many hats are red?"),
 ((13,), "logs", "Maya has 13 logs. Some are by the door and the rest are by the fire. How many logs could be in each place? Show one way."),
 ((6, 13), "snowballs", "Sam has 6 snowballs. Pim has 13 snowballs. How many more snowballs does Sam need to have as many as Pim?"),
 ((8, 6), "cups of cocoa", "Pim has 6 more cups of cocoa than Sam. Sam has 8 cups of cocoa. How many cups of cocoa does Pim have?"),
 ((7, 5), "scarves", "Sam has 5 fewer scarves than Pim. Sam has 7 scarves. How many scarves does Pim have?"),
 ((16, 7), "marshmallows", "Tam has 16 marshmallows. He eats 7 marshmallows. How many marshmallows does Tam have left?"),
 ((15, 7), "snowballs", "Ruby rolled 15 snowballs. Some of them broke apart. Now she has 7 snowballs left. How many snowballs broke apart?"),
 ((4, 9), "icicles", "Some icicles hung on the roof. 4 icicles fell off. Now 9 icicles hang on the roof. How many icicles were on the roof at the start?"),
 ((12, 5), "kids watching", "There are 12 kids at the pond. 5 kids are skating. The rest are watching. How many kids are watching?"),
 ((17, 8), "full cups", "There are 17 cups on the table. Some are full. 8 are empty. How many cups are full?"),
 ((11,), "pinecones", "Lee puts 11 pinecones in two baskets. How many pinecones could be in each basket? Use subtraction to show one way."),
 ((5, 14), "steps", "Leo cleared 5 steps. Maya cleared 14 steps. How many more steps did Maya clear than Leo?"),
 ((13, 4), "snowballs", "Maya has 4 more snowballs than Leo. Maya has 13 snowballs. How many snowballs does Leo have?"),
 ((15, 6), "hats", "Leo has 6 fewer hats than Maya. Maya has 15 hats. How many hats does Leo have?"),
],
5: [  # Polar Expedition
 ((9, 7), "boxes", "The team packs 9 boxes of food on one sled. Then they pack 7 more boxes on the sled. How many boxes are on the sled now?"),
 ((7, 15), "miles", "Rosa has skied 7 miles. She skis some more miles. Now she has skied 15 miles. How many more miles did she ski?"),
 ((6, 14), "seals", "Some seals rested on the ice. Then 6 more seals came up. Now there are 14 seals. How many seals were on the ice at the start?"),
 ((8, 9), "flags", "The camp has 8 red flags and 9 yellow flags. How many flags is that in all?"),
 ((7, 16), "gray dogs", "There are 16 dogs on the team. 7 are brown. The rest are gray. How many dogs are gray?"),
 ((10,), "fish", "Pim has 10 fish for the seals. He puts some in a red tub and the rest in a blue tub. How many fish could be in each tub? Show one way."),
 ((6, 14), "flags", "Dev has 6 flags. Pim has 14 flags. How many more flags does Dev need to have as many as Pim?"),
 ((7, 8), "penguins", "The red group has 8 more penguins than the blue group. The blue group has 7 penguins. How many penguins are in the red group?"),
 ((9, 4), "boxes", "The blue sled has 4 fewer boxes than the red sled. The blue sled has 9 boxes. How many boxes are on the red sled?"),
 ((14, 8), "bags", "There were 14 bags of dog food. The dogs ate 8 bags. How many bags are left?"),
 ((17, 8), "flags", "There were 17 flags on the sled. The team put some flags in the snow. Now 8 flags are on the sled. How many flags did they put in the snow?"),
 ((7, 9), "boxes", "Some boxes were on the sled. The team took off 7 boxes. Now there are 9 boxes on the sled. How many boxes were on the sled at the start?"),
 ((16, 9), "blue flags", "There are 16 flags in all. 9 flags are red. The rest are blue. How many flags are blue?"),
 ((15, 6), "baby seals", "15 seals are on the ice. Some are babies. 6 are grown-ups. How many seals are babies?"),
 ((12,), "socks", "Teo puts 12 socks in two bags. How many socks could be in each bag? Use subtraction to show one way."),
 ((7, 17), "miles", "Tam skied 7 miles. Luz skied 17 miles. How many more miles did Luz ski than Tam?"),
 ((16, 7), "miles", "Luz skied 7 more miles than Tam. Luz skied 16 miles. How many miles did Tam ski?"),
 ((13, 5), "flags", "Tam has 5 fewer flags than Luz. Luz has 13 flags. How many flags does Tam have?"),
],
6: [  # New Year's
 ((7, 8), "lanterns", "Mia hangs 7 lanterns on the rope. Then she hangs 8 more lanterns. How many lanterns are on the rope now?"),
 ((6, 13), "balloons", "There are 6 balloons in the room. Teo blows up some more balloons. Now there are 13 balloons. How many balloons did Teo blow up?"),
 ((6, 15), "lanterns", "Some lanterns were on the rope. Then 6 more lanterns went up. Now there are 15 lanterns. How many lanterns were on the rope at the start?"),
 ((9, 6), "stars", "Ana has 9 gold stars and 6 silver stars. How many stars does Ana have in all?"),
 ((7, 16), "red hats", "There are 16 party hats. 7 hats are blue. The rest are red. How many hats are red?"),
 ((14,), "stars", "Lee has 14 stars. Some are on the window and the rest are on the door. How many stars could be in each place? Show one way."),
 ((8, 15), "noisemakers", "Gus has 8 noisemakers. Zoe has 15 noisemakers. How many more noisemakers does Gus need to have as many as Zoe?"),
 ((6, 9), "stickers", "Zoe has 9 more stickers than Gus. Gus has 6 stickers. How many stickers does Zoe have?"),
 ((9, 7), "balloons", "Gus has 7 fewer balloons than Zoe. Gus has 9 balloons. How many balloons does Zoe have?"),
 ((15, 6), "lanterns", "There were 15 lanterns lit. The wind blew out 6 lanterns. How many lanterns are still lit?"),
 ((18, 10), "balloons", "There were 18 balloons at the party. Some balloons popped. Now there are 10 balloons. How many balloons popped?"),
 ((5, 12), "stars", "Some stars were on the string. Dev took down 5 stars. Now there are 12 stars on the string. How many stars were on the string at the start?"),
 ((13, 5), "kids eating", "There are 13 kids at the party. 5 kids are dancing. The rest are eating. How many kids are eating?"),
 ((16, 7), "gold lanterns", "16 lanterns hang in the street. Some are gold. 7 are red. How many lanterns are gold?"),
 ((10,), "stickers", "Ivy puts 10 stickers on two cards. How many stickers could be on each card? Use subtraction to show one way."),
 ((6, 15), "stars", "Noor counted 6 stars. Dev counted 15 stars. How many more stars did Dev count than Noor?"),
 ((14, 6), "lanterns", "Dev has 6 more lanterns than Noor. Dev has 14 lanterns. How many lanterns does Noor have?"),
 ((17, 8), "hats", "Noor has 8 fewer hats than Dev. Dev has 17 hats. How many hats does Noor have?"),
],
7: [  # Hearts / kindness
 ((5, 9), "hearts", "The club has 5 hearts on the string. Then the kids hang 9 more hearts. How many hearts are on the string now?"),
 ((8, 15), "cards", "Luz has 8 cards for her friends. She makes some more cards. Now she has 15 cards. How many cards did she make?"),
 ((7, 16), "hearts", "Some hearts were on the wall. Then 7 more hearts went up. Now there are 16 hearts. How many hearts were on the wall at the start?"),
 ((7, 9), "hearts", "Omar has 7 pink hearts and 9 purple hearts. How many hearts does Omar have in all?"),
 ((9, 17), "pink flowers", "There are 17 flowers in the vase. 9 are yellow. The rest are pink. How many flowers are pink?"),
 ((13,), "notes", "Pim has 13 notes. Some go in the red bag and the rest go in the blue bag. How many notes could go in each bag? Show one way."),
 ((7, 16), "flowers", "Lena has 7 flowers. Omar has 16 flowers. How many more flowers does Lena need to have as many as Omar?"),
 ((8, 5), "notes", "Omar has 5 more notes than Lena. Lena has 8 notes. How many notes does Omar have?"),
 ((6, 8), "cards", "Lena has 8 fewer cards than Omar. Lena has 6 cards. How many cards does Omar have?"),
 ((17, 9), "hearts", "There were 17 hearts on the string. The wind blew 9 hearts off. How many hearts are still up?"),
 ((15, 6), "cards", "The club had 15 thank-you cards. They gave away some cards. Now they have 6 cards. How many cards did they give away?"),
 ((8, 7), "flowers", "Some flowers were in the vase. Kai took out 8 flowers. Now there are 7 flowers in the vase. How many flowers were in the vase at the start?"),
 ((14, 6), "pink hearts", "There are 14 hearts on the wall. 6 hearts are red. The rest are pink. How many hearts are pink?"),
 ((18, 10), "first graders", "18 kids are in the club. Some are first graders. 10 are second graders. How many are first graders?"),
 ((16,), "cards", "Ana puts 16 cards in two piles. How many cards could be in each pile? Use subtraction to show one way."),
 ((9, 17), "notes", "Ivy wrote 9 notes. Max wrote 17 notes. How many more notes did Max write than Ivy?"),
 ((15, 7), "cards", "Max wrote 7 more cards than Ivy. Max wrote 15 cards. How many cards did Ivy write?"),
 ((13, 4), "hearts", "Ivy has 4 fewer hearts than Max. Max has 13 hearts. How many hearts does Ivy have?"),
],
8: [  # Spring
 ((6, 8), "seeds", "There are 6 seeds in a tray. Jin plants 8 more seeds in the tray. How many seeds are in the tray now?"),
 ((9, 17), "tulips", "Ada has 9 tulips. She picks some more tulips. Now she has 17 tulips. How many tulips did she pick?"),
 ((8, 15), "seeds", "Some seeds were in the row. Then 8 more seeds went in. Now there are 15 seeds. How many seeds were in the row at the start?"),
 ((7, 9), "plants", "The garden has 7 bean plants and 9 pea plants. How many plants is that in all?"),
 ((8, 18), "pots", "There are 18 pots on the shelf. 8 pots hold herbs. The rest hold flowers. How many pots hold flowers?"),
 ((9,), "seeds", "Lia has 9 seeds. She plants some in a pot and the rest in the ground. How many seeds could go in each place? Show one way."),
 ((9, 16), "robins", "Beni saw 9 robins. Ada saw 16 robins. How many more robins does Beni need to see to have as many as Ada?"),
 ((9, 6), "seeds", "Ada has 6 more seeds than Beni. Beni has 9 seeds. How many seeds does Ada have?"),
 ((7, 9), "bees", "Beni saw 9 fewer bees than Ada. Beni saw 7 bees. How many bees did Ada see?"),
 ((16, 9), "sprouts", "There were 16 sprouts in the tray. Jin moved 9 sprouts to the big bed. How many sprouts are still in the tray?"),
 ((14, 5), "pots", "There were 14 pots on the tray. Lia took away some pots. Now 5 pots are on the tray. How many pots did Lia take away?"),
 ((6, 8), "ladybugs", "Some ladybugs were on the leaf. 6 ladybugs flew away. Now there are 8 ladybugs on the leaf. How many ladybugs were on the leaf at the start?"),
 ((17, 8), "daisies", "There are 17 flowers in the garden. 8 are tulips. The rest are daisies. How many flowers are daisies?"),
 ((15, 9), "blue birds", "15 birds sit in the tree. Some are blue. 9 are brown. How many birds are blue?"),
 ((13,), "seeds", "Gus puts 13 seeds in two bags. How many seeds could be in each bag? Use subtraction to show one way."),
 ((7, 18), "bees", "Lena counted 7 bees on Monday. She counted 18 bees on Friday. How many more bees did she count on Friday?"),
 ((17, 8), "seeds", "Tam has 8 more seeds than Zoe. Tam has 17 seeds. How many seeds does Zoe have?"),
 ((14, 6), "pots", "Zoe has 6 fewer pots than Tam. Tam has 14 pots. How many pots does Zoe have?"),
],
9: [  # Summer camp
 ((9, 8), "logs", "There are 9 logs by the fire. Teo carries 8 more logs to the fire. How many logs are by the fire now?"),
 ((6, 14), "fish", "Omar has caught 6 fish. He catches some more fish. Now he has 14 fish. How many more fish did he catch?"),
 ((6, 13), "frogs", "Some frogs sat on the log. Then 6 more frogs hopped on. Now there are 13 frogs. How many frogs were on the log at the start?"),
 ((9, 8), "canoes", "The camp has 9 red canoes and 8 green canoes. How many canoes is that in all?"),
 ((9, 16), "kids on the dock", "There are 16 kids at the lake. 9 kids are swimming. The rest are on the dock. How many kids are on the dock?"),
 ((12,), "shells", "Dev has 12 shells. He puts some in a cup and the rest in a bag. How many shells could be in each place? Show one way."),
 ((8, 17), "shells", "Ruby has 8 shells. Max has 17 shells. How many more shells does Ruby need to have as many as Max?"),
 ((7, 9), "rocks", "Max has 9 more rocks than Ruby. Ruby has 7 rocks. How many rocks does Max have?"),
 ((8, 6), "sticks", "Ruby has 6 fewer sticks than Max. Ruby has 8 sticks. How many sticks does Max have?"),
 ((17, 8), "frogs", "There were 17 frogs on the bank. 8 frogs hopped into the water. How many frogs are still on the bank?"),
 ((18, 11), "fireflies", "Sam caught 18 fireflies in a jar. He let some go. Now 11 fireflies are in the jar. How many fireflies did he let go?"),
 ((7, 9), "logs", "Some logs were on the rack. Kai took 7 logs. Now there are 9 logs on the rack. How many logs were on the rack at the start?"),
 ((15, 6), "brown birds", "There are 15 birds in the tree. 6 birds are blue. The rest are brown. How many birds are brown?"),
 ((14, 8), "kids with hats", "14 kids sit around the fire. Some kids wear hats. 8 kids do not wear hats. How many kids wear hats?"),
 ((11,), "pinecones", "Pia puts 11 pinecones in two buckets. How many pinecones could be in each bucket? Use subtraction to show one way."),
 ((6, 15), "birds", "Teo saw 6 birds. Pia saw 15 birds. How many more birds did Pia see than Teo?"),
 ((16, 7), "stones", "Pia has 7 more stones than Teo. Pia has 16 stones. How many stones does Teo have?"),
 ((13, 6), "shells", "Teo has 6 fewer shells than Pia. Pia has 13 shells. How many shells does Teo have?"),
],
10: [  # Celebration
 ((8, 9), "chairs", "There are 8 chairs on the stage. Dev puts out 9 more chairs. How many chairs are on the stage now?"),
 ((7, 15), "name cards", "Rosa has 7 name cards. She makes some more name cards. Now she has 15 name cards. How many name cards did she make?"),
 ((5, 12), "balloons", "Some balloons were in the hall. Then 5 more balloons came in. Now there are 12 balloons. How many balloons were in the hall at the start?"),
 ((6, 9), "instruments", "The class has 6 drums and 9 horns. How many instruments is that in all?"),
 ((8, 17), "pink cupcakes", "There are 17 cupcakes on the table. 8 have blue frosting. The rest have pink frosting. How many cupcakes have pink frosting?"),
 ((14,), "ribbons", "Kai has 14 ribbons. He puts some on the stage and the rest on the door. How many ribbons could be in each place? Show one way."),
 ((7, 16), "ribbons", "Ana has 7 ribbons. Sam has 16 ribbons. How many more ribbons does Ana need to have as many as Sam?"),
 ((9, 7), "tickets", "Sam has 7 more tickets than Ana. Ana has 9 tickets. How many tickets does Sam have?"),
 ((8, 5), "programs", "Ana has 5 fewer programs than Sam. Ana has 8 programs. How many programs does Sam have?"),
 ((16, 9), "chairs", "There were 16 chairs in the front row. The helpers carry away 9 chairs. How many chairs are left in the front row?"),
 ((14, 9), "cupcakes", "There were 14 cupcakes on the tray. Some cupcakes were eaten. Now there are 9 cupcakes. How many cupcakes were eaten?"),
 ((6, 10), "balloons", "Some balloons were on the ceiling. 6 balloons popped. Now there are 10 balloons on the ceiling. How many balloons were on the ceiling at the start?"),
 ((13, 5), "kids who dance", "There are 13 kids in the show. 5 kids sing. The rest dance. How many kids dance?"),
 ((17, 9), "kids with hats", "17 kids are at the party. Some kids wear hats. 9 kids do not wear hats. How many kids wear hats?"),
 ((15,), "ribbons", "Zoe puts 15 ribbons in two boxes. How many ribbons could be in each box? Use subtraction to show one way."),
 ((6, 13), "name cards", "Dev has 6 name cards. Rosa has 13 name cards. How many more name cards does Rosa have than Dev?"),
 ((17, 8), "tickets", "Rosa has 8 more tickets than Dev. Rosa has 17 tickets. How many tickets does Dev have?"),
 ((12, 5), "cups", "Dev has 5 fewer cups than Rosa. Rosa has 12 cups. How many cups does Dev have?"),
],
}


def solve(t, k):
    """Return (answer, equation text) for a type and its known numbers."""
    if t in ("AR", "PT", "CB", "CBF"):
        a, b = k; return a + b, "%d + %d = []" % (a, b)
    if t in ("AC", "PA", "CDA"):
        a, c = k; return c - a, "%d + [] = %d or %d - %d = []" % (a, c, c, a)
    if t == "AS":
        b, c = k; return c - b, "[] + %d = %d or %d - %d = []" % (b, c, c, b)
    if t == "TR":
        a, b = k; return a - b, "%d - %d = []" % (a, b)
    if t == "TC":
        a, c = k; return a - c, "%d - [] = %d or %d - %d = []" % (a, c, a, c)
    if t == "TS":
        b, c = k; return b + c, "[] - %d = %d or %d + %d = []" % (b, c, c, b)
    if t == "S1":
        c, a = k; return c - a, "%d - %d = []" % (c, a)
    if t == "S2":
        c, b = k; return c - b, "%d - [] = %d or %d - %d = []" % (c, b, c, b)
    if t == "CDS":
        a, c = k; return c - a, "%d - %d = []" % (c, a)
    if t in ("CS", "CSF"):
        c, b = k; return c - b, "%d - %d = []" % (c, b)
    raise ValueError(t)


def build():
    out = {}
    for lp, rows in LP.items():
        assert len(rows) == 18, lp
        parts = []
        for si, (sid, label, desc) in enumerate(STRANDS):
            qs, key = [], []
            for j in range(3):
                t = TYPES[si * 3 + j]
                known, unit, text = rows[si * 3 + j]
                assert "—" not in text and "–" not in text
                for n in known:
                    assert re.search(r"(?<![\d])%d(?![\d])" % n, text), (lp, t, n, text)
                if t in ("PB", "S3"):
                    c = known[0]
                    assert 2 <= c <= 20
                    ex = c // 2 - 1 if c // 2 - 1 >= 1 else 1
                    if t == "PB":
                        line = "%s: any two numbers that make %d, like %d + %d = %d. Check that the two parts add up to %d." % (TAG[t], c, ex, c - ex, c, c)
                    else:
                        line = "%s: any two numbers that make %d, like %d - %d = %d. Check that the two parts add up to %d." % (TAG[t], c, c, ex, c - ex, c)
                else:
                    ans, eq = solve(t, known)
                    assert 1 <= ans <= 20, (lp, t, ans)
                    eq = eq.replace("[]", "□")
                    line = "%s: %d %s (%s)" % (TAG[t], ans, unit, eq)
                qs.append(text); key.append(line)
            parts.append({"id": sid, "title": label, "desc": desc, "qs": qs, "key": key})
        out[str(lp)] = parts
    return out


def js(data):
    L = []
    L.append("/* OAA1-STRANDS-BEGIN (generated by source/tools/gen_oaa1.py, edit the generator, not this block) */")
    L.append("window.TP_STRANDS=window.TP_STRANDS||{};")
    st = {"desc": "addition and subtraction word problems within 20, with the unknown in any position",
          "parts": [{"id": s[0], "label": s[1], "desc": s[2]} for s in STRANDS]}
    L.append("window.TP_STRANDS[\"1.OA.A.1\"]=" + json.dumps(st, ensure_ascii=False) + ";")
    L.append("var OA1=" + json.dumps(data, ensure_ascii=False) + ";")
    L.append("""var OA1DIR="Listen to each story problem. You can draw. Write a number sentence with a box for the number you do not know. Say your answer.";
var OA1DIRB="Listen to each story problem. You can draw. Write a number sentence with boxes for the numbers you do not know. Say your answer.";
A({std:"1.OA.A.1",op:"strands",make:function(lp){return OA1[String(lp)].map(function(s,i){return P({std:"1.OA.A.1",strand:s.id,title:s.title,n:3,dur:130,dir:(s.id==="addpt"||s.id==="subpt")?OA1DIRB:OA1DIR,desc:s.desc,mats:["a pencil and paper"],rows:s.qs.map(function(q,j){return[q,s.key[j]]})})})}});
/* OAA1-STRANDS-END */""")
    return "\n".join(L)


def main():
    data = build()
    block = js(data)
    assert "—" not in block
    src = open(G1, encoding="utf8").read()
    if "OAA1-STRANDS-BEGIN" in src:
        src = re.sub(r"/\* OAA1-STRANDS-BEGIN.*?OAA1-STRANDS-END \*/", lambda m: block, src, flags=re.S)
    else:
        lines = src.split("\n")
        # lines 114 to 118 (1-based) hold the old start-unknown problems
        assert lines[113].startswith("var SU=") and lines[116].startswith('A({std:"1.OA.A.1"'), "old block not where expected"
        assert lines[118] == "})();" or lines[118].startswith("})")
        lines[113:118] = block.split("\n")
        src = "\n".join(lines)
    open(G1, "w", encoding="utf8").write(src)
    print("wrote", sum(len(p["qs"]) for v in data.values() for p in v), "problems")


if __name__ == "__main__":
    main()
