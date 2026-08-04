# Out of Town Yinzers

Website for the Out of Town Yinzers podcast (Joe Flannery & Justin Boland)
-- Pittsburgh sports: Steelers, Pirates, Penguins, Pitt Athletics.

## Pages

- **Home** -- scoreboard strip (next game + odds when posted), hero,
  latest YouTube upload (clicking a secondary video swaps it into the
  main player instead of leaving the site), latest blog post, aggregated
  team news, and a merch teaser
- **Episodes** -- recent full episodes from YouTube (Shorts excluded;
  YouTube's feed only ever returns the last 15 uploads total, so this is
  "recent," not a full archive)
- **Blog** -- public posts with a sidebar post list and an author bio card;
  "New Post"/edit/delete gated behind a shared admin login (see
  `DEPLOY.md`)
- **Shop** -- real products pulled from the Printful store, linking out to
  Printful for checkout

News headlines (Steelers/Pirates from official team RSS, Penguins/Pitt
from a filtered Google News search) refresh automatically via a scheduled
task rather than a manual button -- see `DEPLOY.md`.

## Running locally

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Visit `http://127.0.0.1:5051` (use `127.0.0.1`, not `localhost` -- and note
port 5060 is blocked by browsers as an unsafe/reserved port, which is why
this uses 5051 instead). No login is required locally -- the admin gate on
Blog posting only activates when `ADMIN_PASSWORD` is set in the
environment (see `DEPLOY.md`). It's session-based (a real login page at
`/admin/login`), not a browser popup.

## Deploying

See `DEPLOY.md` for PythonAnywhere setup instructions, including the
scheduled task for automatic news refresh.
