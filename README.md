# Treasure Path Games

Student assessment games, one page per learning period (LP 1 to 10).

## Folders
- `docs/` is the live site. GitHub Pages serves this folder. `index.html` is the page with links to each LP.
- `source/gx/` has the game code (`apply.py` builds everything, `g1.js` to `g8.js` hold the stops for each grade).
- `source/gem/` has every picture the games use, saved as text files (`.b64`) so they can be rebuilt.
- `source/work/patched_base.html` is the base game file the build starts from.
- `source/split/build.py` cuts the finished game into the 10 LP pages and writes them to `docs/`.

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
- Each LP page is one self-contained file, 10 to 16 MB. They load fine but take a few seconds on a slow connection.
- GitHub Pages sites are public. Do not type real student names into the games.
