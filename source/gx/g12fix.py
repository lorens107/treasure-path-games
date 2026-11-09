# Rewrites G1 read-aloud passages (RL.1.1/RI.1.1) into natural read-aloud prose. Facts that the keys test are unchanged.
FIX=[
("Fox had a big red hat","Fox had a big red hat, and he wore it every sunny day. It was his very best hat. One windy morning, Fox went for a walk by the pond. Whoosh! The wind snatched the hat right off his head and tossed it up into a tall tree. Fox jumped and jumped, but he could not reach it. Duck saw what happened. She flew up to the branch, grabbed the hat, and brought it back down. “Thank you, Duck!” said Fox. “You are a good friend.”"),
("Frogs live near ponds. They like the wet grass","Frogs live near ponds, where the grass is wet and the water is close. A frog starts its life as an egg. The egg floats in the water until it hatches, and out comes a tadpole. A tadpole has a tail and swims like a fish. As it gets bigger, it grows legs, and its tail gets shorter. At last it hops out of the water and onto land. A frog has a long, sticky tongue. It flicks its tongue out very fast to catch bugs."),
("Meg had a big tin tub","Meg had a big tin tub, and she set it on the grass under the plum tree. Plop! A red plum fell right in. Then, plop, plop, plop! Lots of plums dropped into the tub, one after another. Meg was so pleased. Just then a fat pink pig trotted up the path. It sniffed the tub, grabbed ten juicy plums, and had a big snack. Plum juice ran down its chin. Meg looked at her tub and at the happy pig, and she had to grin."),
("A hen sits on a nest","A mother hen sits on her nest. She has five eggs under her warm feathers, and she sits on them for a long time to keep them safe and warm. One day the eggs begin to crack. Out pop the chicks! A new chick is soft and wet, but it dries off fast and turns fluffy. Soon the chicks can peck at the ground and run around the yard behind their mother."),
("Jill had the best pumpkin","Jill grew the best pumpkin in the whole patch. But it was so big! She tried to lift it, but it would not budge. “I need help,” said Jill. She ran down the road to get her friend Russ. Russ had a red wagon. Together they rolled the pumpkin up a board and set it in the wagon. Then they had to tug and tug. Up the hill they went, one slow step at a time, all the way to the fair."),
("A pumpkin sits on a stem","A pumpkin grows on a long stem that stays joined to the vine. It has thick skin that keeps it safe. Sun and wet mud help it get big. Some pumpkins can get as big as a dog! When you cut one open, you will see wet pulp and lots of seeds inside."),
("Some animals sleep all winter","Some animals sleep through the whole winter, and a groundhog is one of them. In the fall, a groundhog eats and eats. It eats a lot of food so that its body has plenty of fat. Then it digs a den under the ground. The den stays warm even when the air gets cold. The groundhog curls up in a ball and sleeps for months. It does not need to eat at all. In the spring it wakes up and comes out to look for fresh grass."),
("Rosa and Pim work at the camp","Rosa and Pim work at a camp out on the ice. One windy day, the wind took Pim's red hat and blew it away. “My hat!” Pim cried. Rosa ran to help him look. They dug through the soft snow by the tents. At last Pim found his hat. It was under a crate, which is a big box that holds camp food. Pim brushed off the snow and put the hat on his head. Then he sat down to rest, warm and happy."),
("A seal lives in the cold sea","A seal lives in the cold sea. It has a thick layer of fat, and the fat keeps it warm. A seal can hold its breath for a long time. It swims down deep to find fish. When it needs to breathe, it comes up to a hole in the ice, because that is where it can get air. After a big meal, seals like to rest on flat ice in the sun."),
("Noor made a lantern","Noor made a lantern out of red paper and thin sticks. She carried it down to the river to hang it up with all the others. But the last hook on the rope was too high, and she could not reach it. She stretched up on her toes, but it was no use. Then Tam ran over with a crate. Noor could stand on it! She climbed up and hooked her lantern on at the end of the rope. Then the two friends sat on the bridge and watched the lantern swing."),
("Stars are very big","Stars are very big, and they are very hot. But stars look small to us. That is because they are very far away. Our sun is a star too. The sun looks big and bright because it is much closer to us than any other star."),
("Ines could not reach the top shelf","Ines could not reach the top shelf in the tool shed. The trowel she wanted was up there, right at the top, next to a ball of string. She stretched up on her toes, but her fingers only brushed the edge. Dev saw her trying. He brought the step stool over from behind the door and held it steady while she climbed. At last Ines got her trowel. Then she reached back up and got one down for Dev too."),
("Our street has a little book box","Our street has a little book box on a post. Anyone may open it. If you see a book you want to read, you take it, and you do not pay. When you are done, you bring the book back. Or you can put in a book of your own for someone else to enjoy. The box is open all day, so you can visit it any time."),
("Mina found one last seed","Mina found one last seed at the bottom of the seed packet. But the garden rows were already full, and there was no room left. So Mina got an old cup and filled it with soil. She planted the seed on the windowsill. Every day she gave it one spoonful of water. For a long time nothing happened. Then one morning a thin green loop pushed up out of the soil. It stood up straight and tall. Mina carried the cup to school, because she wanted to show her class."),
("A seed is a tiny plant","A seed is a tiny plant that has its own lunch packed around it. The seed stays dry and still until three things reach it. First it needs water. The coat around the seed is hard, and water makes it soften. Next it needs air. That is why good soil is never packed down too tight, so that air can get through. Last it needs warmth. When water, air, and warmth have all arrived, the coat splits open, and a small white root pushes down into the soil."),
("Teo made a paddle","Teo made a paddle in the camp workshop. He cut a flat board for the blade and added a long handle. He sanded the edges until they were smooth. Then he carried the paddle down to the dock. But the handle was too long, and his hands were too far apart to hold it well. Luz held the paddle up against him and marked the spot with a pencil. The camp leader got a saw and cut the end off at the mark. Then Teo climbed into the canoe and pushed off. The paddle fit him just right."),
("Most trees drop all their leaves","Most trees drop all their leaves when the cold comes. A pine tree does not. Its leaves are thin, hard needles, and each needle has a waxy coat. The coat keeps the water inside. Because of that, a needle can stay on the branch for two years or more. A pine tree lets only a few needles go at a time, so it is never bare. That is why a pine tree looks green in every season."),
("Rosa made a long paper chain","Rosa made a long paper chain for the last day of school. She wanted to hang it across the whole yard. But the chain kept slipping off the hook at the far end, and it would not stay up. Omar ran over with a roll of tape. He climbed two steps up the ladder and taped the chain tight. Rosa held the bottom so it would not twist. When they were done, the chain swung over the tables. It looked like a bridge of color."),
("You blow into a horn","When you blow into a horn, the air inside starts to shake very fast. Shaking air is what sound is. A horn is shaped like a cone. It is narrow where you blow and wide at the other end. The wide end pushes the shaking air out toward the crowd. A longer horn makes a lower sound. That is why the big horns in a band sound deep, and the little ones sound high."),
]
import re as _re
for _st,_new in FIX:
    _i=s.find(_st); assert _i>=0 and s.count(_st)>=1,_st
    _e=s.find('"',_i); _old=s[_i:_e]
    assert '\n' not in _old and len(_old)>30,(_st,len(_old))
    assert '"' not in _new
    s=s.replace(_old,_new)
# line references that no longer exist
for _a,_b in [("Because they are far away. Line 4 says it.","Because they are very far away."),("A star. Line 5 says our sun is a star too.","A star. The text says our sun is a star too.")]:
    if _a in s: s=s.replace(_a,_b)
    else: print('MISSING key',_a)
s=s.replace("Listen while your teacher reads the six lines. Then answer out loud.","Listen while your teacher reads the facts. Then answer out loud.")
for _a,_b,_n in [("Look back at the story if you need to. Then answer each question out loud.","Your teacher can read the story again if you need it. Then answer each question out loud.",8),("Use the story above. Answer out loud.","Listen while your teacher reads the story again if you need it. Answer out loud.",1)]:
    assert s.count(_a)==_n,(_a,s.count(_a)); s=s.replace(_a,_b)

# G4 and G6 passages that were a little light for students who read them alone
for _a,_b in [
("When the flower is fully grown, the turning stops. A grown sunflower faces east all day. The morning sun warms it, and warm flowers get more visits from bees.",
 "The stem does the work. The side of the stem away from the sun grows a little faster than the side facing the sun, so the bud bends toward the light. When the flower is fully grown, the turning stops, because the stem has become thick and stiff. A grown sunflower faces east all day. The morning sun warms it, and warm flowers get more visits from bees."),
("Mrs. Okonkwo crossed the street.</p>",
 "Mrs. Okonkwo crossed the street.</p><p>Priya had moved to Elkhorn in August, and so far the village felt like a play she was watching from the wings. People waved to her mother at the post office and said her name wrong. Nobody had asked her for anything, and she had not offered.</p>"),
("“Push it,” she said. “Do not carry it. Snow goes where you point it.”</p>",
 "“Push it,” she said. “Do not carry it. Snow goes where you point it.”</p><p>Priya tried it. The blade slid under the drift, and the heavy pile slid away instead of fighting her. The work began to go faster.</p>"),
("The walk took an hour. Her mittens soaked through and her cheeks stung.",
 "The walk took an hour. Her arms shook, and twice she thought about leaving the last stretch for the sun to melt. Her mittens soaked through and her cheeks stung."),
]:
    assert s.count(_a)>=1,_a[:50]; s=s.replace(_a,_b)

# Grade 8 LP2 "One Clean Cut" and LP3 "The Weigh-Off": more complex sentences, all quoted evidence lines untouched
for _a,_b in [
("The storm had split the old Harlow tree down the middle. Half of it lay in the grass like a dropped coat.",
 "The storm had split the old Harlow tree clean down the middle during the night, and by morning half of it lay in the grass like a dropped coat, its leaves still green and trembling."),
("He did not look up from his clipboard. “A tree that can’t bear fruit is just a tall bill.”",
 "He did not look up from his clipboard, where a long column of chores was already half crossed out. “A tree that can’t bear fruit is just a tall bill.”"),
("Lucia had picked from that tree every fall since she was six. Its apples were small and lumpy",
 "Lucia had picked from that tree every fall since she was six, standing on an upturned crate until she was tall enough to reach the lowest branches. Its apples were small and lumpy"),
("“We cut a few twigs and join them to a young tree. In time, the young tree grows Harlow apples.”",
 "“We could cut a few twigs from the living half and join them to a young tree. In time, the young tree would bear Harlow apples.”"),
("He studied the broken tree, and then he studied her.",
 "For a long moment he studied the broken tree, and then he studied her, as though weighing one against the other."),
("Lucia’s hands were not steady, but the blade was sharp.",
 "Lucia’s hands were not steady, though the blade was sharp enough to forgive her."),
("For five months, Emeka had fed, watered, and shaded one pumpkin. Now it sat",
 "For five months, Emeka had fed, watered, and shaded one pumpkin, and he had come to know its moods the way some people know a pet’s. Now it sat"),
("a forklift driver waved them into line. Emeka’s cousin Noor ran her hand",
 "a forklift driver waved them into a line that crept toward the scales. Emeka’s cousin Noor, who had come along to help, ran her hand"),
("Near the stem, the skin gave under his thumb. It was a soft spot",
 "Near the stem, the skin gave under his thumb, faintly damp and warm, the way fruit feels when it has begun to turn. It was a soft spot"),
("Emeka looked down the line. Old Mr. Brandt was polishing a pumpkin half the size of his.",
 "Emeka looked down the line, weighing what he saw against what he knew. Old Mr. Brandt was polishing a pumpkin half the size of his, rubbing it with a rag as if it were a trophy already."),
("Noor followed his eyes. She did not answer.",
 "Noor followed his eyes. She opened her mouth, then closed it, and she did not answer."),
("All of it had shrunk to a spot the size of a coin. No fairy godmother",
 "All of it had shrunk to a spot the size of a coin, which seemed to grow larger the longer he stared at it. No fairy godmother"),
]:
    assert s.count(_a)>=1,_a[:60]; s=s.replace(_a,_b)
