# Treasure Path Games

Student assessment games for all 10 learning periods, on one site. The first screen is the learning period picker with grade and checks.

## Folders
- `docs/` is the live site. GitHub Pages serves this folder. `index.html` is the game. `docs/data/` has one file per grade per LP (like `lp2-g2.js`), loaded when you start that LP and grade.
- `source/gx/` has the game code (`apply.py` builds everything, `g1.js` to `g8.js` hold the stops for each grade).
- `source/gem/` has every picture the games use, saved as text files (`.b64`) so they can be rebuilt.
- `source/work/patched_base.html` is the base game file the build starts from.
- `source/split/build.py` splits the finished game into `docs/index.html` and the files in `docs/data/`.

## Rebuild after a change
From the `source` folder:

    cd gx && python3 apply.py
    cd ../split && python3 build.py

Then commit and push. The site updates in a minute or two.

## Add or change a picture
1. Keep the original image file somewhere safe. Chat attachments are not kept.
2. Save it as a web image and as text:

       python3 source/tools/add_image.py NAME path/to/image.png 900

   This writes `source/gem/NAME.b64`.
3. The picture still has to be connected to a stop in the code (`source/gx/apply.py` and `g*.js`). Ask Claude to do this: say the grade, LP, stop, and whether it should show only with Picture supports on.
4. Rebuild, commit, push.

## Notes
- The first load is about 14 MB. After you pick an LP and grade, one more file of 1 to 2 MB loads.
- GitHub Pages sites are public. Do not type real student names into the games.
