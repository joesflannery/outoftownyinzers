"""Next-game lookup for the homepage scoreboard strip.

Uses ESPN's public (unofficial, no key required) endpoints:
- the team endpoint's "nextEvent" field for opponent/date/logos
- the event summary endpoint's "pickcenter" field for the moneyline, when
  a book has posted one yet (often empty for games far out)

Same team abbreviation ("pit") happens to work for Steelers/Pirates/
Penguins since Pittsburgh's abbreviation is consistent across NFL/MLB/NHL;
Pitt football uses "pitt" under college-football.
"""

import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import requests

CACHE_SECONDS = 1800
BASE = "https://site.api.espn.com/apis/site/v2/sports"

# team display name -> (ESPN sport path, team slug)
_TEAMS = {
    "Steelers": ("football/nfl", "pit"),
    "Pirates": ("baseball/mlb", "pit"),
    "Penguins": ("hockey/nhl", "pit"),
    "Pitt": ("football/college-football", "pitt"),
}

_cache = {"games": [], "fetched_at": 0}


def _format_when(iso_date):
    dt = datetime.strptime(iso_date, "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)
    local = dt.astimezone(ZoneInfo("America/New_York"))
    return local.strftime("%b %-d, %-I:%M %p ET")


def _get_json(url):
    # No custom User-Agent here on purpose -- ESPN's endpoint 403s on a
    # "Mozilla/..."-style header (even a fully realistic one) but accepts
    # requests' own default, so overriding it does more harm than good.
    resp = requests.get(url, timeout=8)
    resp.raise_for_status()
    return resp.json()


def _fetch_odds(sport_path, event_id):
    try:
        data = _get_json(f"{BASE}/{sport_path}/summary?event={event_id}")
        pickcenter = data.get("pickcenter") or []
        if pickcenter and pickcenter[0].get("details"):
            return pickcenter[0]["details"]
    except Exception:
        pass
    return None


def _fetch_one(team, sport_path, slug):
    data = _get_json(f"{BASE}/{sport_path}/teams/{slug}")
    next_events = data.get("team", {}).get("nextEvent")
    if not next_events:
        return None
    event = next_events[0]
    competition = event["competitions"][0]
    competitors = competition["competitors"]
    my_id = data["team"]["id"]
    me = next(c for c in competitors if c["team"]["id"] == my_id)
    opponent = next(c for c in competitors if c["team"]["id"] != my_id)
    return {
        "team": team,
        "my_logo": me["team"]["logos"][0]["href"] if me["team"].get("logos") else None,
        "opponent_name": opponent["team"]["displayName"],
        "opponent_logo": opponent["team"]["logos"][0]["href"] if opponent["team"].get("logos") else None,
        "home_away": me["homeAway"],
        "when": _format_when(event["date"]),
        "odds": _fetch_odds(sport_path, event["id"]),
    }


def get_upcoming_games():
    now = time.time()
    if now - _cache["fetched_at"] < CACHE_SECONDS:
        return _cache["games"]

    games = []
    for team, (sport_path, slug) in _TEAMS.items():
        try:
            game = _fetch_one(team, sport_path, slug)
        except Exception:
            game = None
        if game:
            games.append(game)

    _cache["games"] = games
    _cache["fetched_at"] = now
    return games
