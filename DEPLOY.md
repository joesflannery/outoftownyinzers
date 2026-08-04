# Deploying to PythonAnywhere

Same playbook as your fantasy football app -- code comes from GitHub, the
site runs on PythonAnywhere, and updates are a `git pull` + Reload. The
difference here: this site is public (no login), except the "New Post"
button on the Blog, which is gated behind one admin login for you and
Justin.

## 1. Sign up / reuse your account

If you don't already have a PythonAnywhere account, sign up at
[pythonanywhere.com](https://www.pythonanywhere.com). You can run this
site on the same account as your fantasy app -- PythonAnywhere lets one
account host multiple separate web apps.

You'll need a **paid plan** (Developer, $10/month, is fine) for two
reasons: outbound internet access (needed for the News page's RSS fetches)
and custom domain support (needed to point `outoftownyinzers.com` here --
free accounts are stuck on `yourusername.pythonanywhere.com`).

## 2. Add a deploy key for this repo

In a PythonAnywhere **Bash console** (Consoles tab → Bash) -- if you
already did this for the fantasy app, you can reuse that same SSH key and
just add it as a deploy key on this new repo too:
```
cat ~/.ssh/id_ed25519.pub
```
Copy the output. On GitHub, go to this repo → **Settings → Deploy keys →
Add deploy key**, paste it in, leave "Allow write access" unchecked, save.

## 3. Clone the code

```
git clone git@github.com:YOURUSERNAME/outoftownyinzers.git yinzers
```

## 4. Create the virtualenv

```
mkvirtualenv --python=/usr/bin/python3.10 yinzers-venv
pip install -r yinzers/requirements.txt
```

## 5. Create the web app

1. **Web** tab → **Add a new web app**.
2. **Manual configuration** (not a Flask quickstart).
3. Python 3.10 (matching the virtualenv).
4. In the **Virtualenv** section, type `yinzers-venv` and hit enter.

## 6. Edit the WSGI file

Click the WSGI configuration file link on the Web tab. Delete everything
in it and replace with this, filling in your own values:

```python
import sys
import os

path = '/home/YOURUSERNAME/yinzers'
if path not in sys.path:
    sys.path.insert(0, path)

# Marks this as a real deployment rather than local dev -- without this,
# the app silently falls back to a hardcoded local-only SECRET_KEY instead
# of requiring you to set a real one below.
os.environ['FLASK_ENV'] = 'production'

# Gates just the Blog's "New Post"/"Edit"/"Delete" actions -- reading the
# site (Home/News/Blog/Shop) stays fully public with no login at all.
# One shared password, not a username/password pair -- give this to
# Justin too so he can post, rather than making him his own login.
os.environ['ADMIN_PASSWORD'] = 'choose-a-real-password'
os.environ['SECRET_KEY'] = 'choose-any-long-random-string'

from run import app as application
```

Log in at `outoftownyinzers.com/admin/login` with that password to post,
edit, or delete blog entries -- share the password with Justin so he can
post too.

## 7. Set the working directory

Web tab → **Source code** / **Working directory**:
`/home/YOURUSERNAME/yinzers`

## 8. Reload

Hit **Reload**. Visit `https://YOURUSERNAME.pythonanywhere.com` -- the
site should load with no login prompt. Only `/blog/new` (and edit/delete)
will prompt for the admin login.

## 9. Point outoftownyinzers.com at it

Once you've registered the domain (any registrar -- Namecheap, GoDaddy,
Google Domains, etc.):

1. On PythonAnywhere, **Web** tab → your app → **Add a new domain** (or
   the domain field near the top) → enter `outoftownyinzers.com` (and
   `www.outoftownyinzers.com` if you want both to work).
2. PythonAnywhere will show you a CNAME record to add. In your registrar's
   DNS settings, add that CNAME (for the root domain, some registrars
   require an ALIAS/ANAME record instead of CNAME -- their support docs
   will say which).
3. DNS changes can take anywhere from a few minutes to a few hours to
   propagate.
4. Once it resolves, PythonAnywhere can also provision a free HTTPS
   certificate for the custom domain -- there's a checkbox for that on
   the same Web tab domain settings.

## Pushing future updates

```
cd yinzers
git pull
```
then hit **Reload** on the Web tab.

## Troubleshooting

- **Something won't load**: check the **Error log** link on the Web tab.
- **News page shows no headlines**: hit "Refresh headlines" on the News
  page once manually after first deploy -- the cache starts empty.
- **`git clone` fails**: re-check the deploy key step.
