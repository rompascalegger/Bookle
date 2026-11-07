# Bookle 📚

A cozy, funny shelving puzzle. Every book on the returns cart has a wish ("Top shelf. I like to look down on people."). Put them where they want to be and keep everyone happy 💖.

## Play

Open `index.html` in a browser. To keep your saves, serve the folder (browsers block storage on `file://`/`data:` pages in some setups):

```bash
python -m http.server 8417
```

Then go to http://localhost:8417.

## Modes

- **Daily Bookle**: one seeded puzzle per day, the same for everyone. Fewer moves earn a better title, and you can share your result.
- **My Library**: endless days. Earn 💧 ink, buy upgrades (lamp, fern, fairy lights, a library cat that knocks books off shelves, bigger shelves), keep a perfect-day streak, and collect all 64 books in the Bookdex.

## How puzzles work

Books only care about their left and right neighbors, their row and their column. A 👇 book cares about the slot directly below it. Each puzzle is built from a real solved arrangement, so every puzzle can be solved, and the Hint button uses that arrangement.
