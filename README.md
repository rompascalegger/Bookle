# Bookle 📚

A cozy, funny shelving puzzle. Every book on the returns cart has a wish ("Top shelf. I like to look down on people."). The shelves have exactly enough room, so every book matters. Make them all happy 💖.

Play it at https://bookle.dicele.io

## Run locally

Open `index.html` in a browser. To keep your saves, serve the folder (browsers block storage on `file://`/`data:` pages in some setups):

```bash
python -m http.server 8417
```

Then go to http://localhost:8417.

## Modes

- **Daily Bookle**: one seeded puzzle per day (3×5 shelf, 12 books), the same for everyone. Fewer moves earn a better title, and you can share your result.
- **My Library**: endless days. The shelves grow from 2×3 to 4×6, books get pickier (two wishes, then golden Legendary books), and you earn 💧 ink for upgrades: snack jar, lamp, fern, fairy lights, a library cat, a rug, a disco ball and a golden bookmark.

## Things to collect

- **96 books** in the Bookdex, plus golden editions of Legendary books
- **24 bookmark charms** (common to legendary) from perfect days and solved Dailies
- **26 stickers** for things like combos, streaks, witnessing a sneeze or a tantrum

## How puzzles work

Books care about their row, their column, their left and right neighbors, the slot above or below, the decor next to them, or who else is on their shelf. Each puzzle is built from a real solved arrangement, so every puzzle can be solved, and the Hint button uses that arrangement.

Grumpy books don't stay quiet: they complain, argue with neighbors, sneeze at the cat, get a rain cloud and eventually throw a tantrum. Happy books bop to the music, and a perfect shelf starts a dance party.
