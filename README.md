# Out of Town Yinzers

Website for the Out of Town Yinzers podcast (Joe Flannery & Justin Boland)
-- Pittsburgh sports: Steelers, Pirates, Penguins, Pitt Athletics.

## Pages

- **Home** -- hero, latest YouTube upload embed, social links, latest
  blog/news teasers
- **News** -- aggregated headlines per team, filterable, manual refresh
  button (Steelers/Pirates from official team RSS, Penguins/Pitt from
  Google News search since no official feed was found)
- **Blog** -- public posts; "New Post"/edit/delete gated behind a shared
  admin login (see `DEPLOY.md`)
- **Shop** -- placeholder for now; real merch store is a separate future
  project

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
Blog posting only activates when `ADMIN_USERNAME`/`ADMIN_PASSWORD` are set
in the environment (see `DEPLOY.md`).

## Still needed before this looks "real"

- Domain registration + PythonAnywhere custom domain setup (see
  `DEPLOY.md`)
- Merch shop (separate project)

## Deploying

See `DEPLOY.md` for PythonAnywhere setup instructions.
