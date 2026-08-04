"""Recent-YouTube-uploads lookup for the home page.

Uses YouTube's public per-channel RSS feed (no API key needed) so the
homepage always reflects whatever was actually posted most recently,
instead of hardcoded video IDs that go stale. Falls back to an empty list
if the fetch fails, e.g. no outbound internet.

The feed mixes Shorts in with full episodes (Shorts links look like
/shorts/<id> instead of /watch?v=<id>), so get_latest_long_form() digs
past however many Shorts came most recently to find the last real episode.

YouTube's per-channel RSS feed only ever returns the 15 most recent
uploads total (Shorts included) -- there's no pagination without the paid/
quota-limited YouTube Data API, so the Episodes page is a "recent
episodes" list, not a full lifetime archive.
"""

import time

import feedparser

CHANNEL_ID = "UC0Z8IpS0GJnO2GAuknEVvtg"  # Out of Town Yinzers
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
CACHE_SECONDS = 1800
POOL_SIZE = 15

_cache = {"entries": [], "fetched_at": 0}


def _get_entries():
    now = time.time()
    if now - _cache["fetched_at"] < CACHE_SECONDS:
        return _cache["entries"]

    entries = []
    try:
        parsed = feedparser.parse(FEED_URL)
        for entry in parsed.entries[:POOL_SIZE]:
            video_id = entry.get("yt_videoid")
            if not video_id:
                continue
            thumbnails = entry.get("media_thumbnail", [])
            link = entry.get("link", "")
            entries.append(
                {
                    "id": video_id,
                    "title": entry.get("title", ""),
                    "thumbnail": thumbnails[0]["url"] if thumbnails else None,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "is_short": "/shorts/" in link,
                }
            )
    except Exception:
        entries = []

    _cache["entries"] = entries
    _cache["fetched_at"] = now
    return entries


def get_recent_videos(limit=4):
    return _get_entries()[:limit]


def get_latest_long_form():
    for entry in _get_entries():
        if not entry["is_short"]:
            return entry
    return None


def get_all_long_form():
    return [entry for entry in _get_entries() if not entry["is_short"]]
