#!/usr/bin/env python3
"""Regenerate rss.xml from the post list in blog/index.html."""

import re
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_INDEX = ROOT / "blog" / "index.html"
FEED_PATH = ROOT / "rss.xml"

SITE_URL = "https://charles-young.com"
FEED_TITLE = "Charles Young"
FEED_DESCRIPTION = "Blog posts from charles-young.com"

POST_RE = re.compile(
    r'<li>([A-Za-z]{3} \d{2}, \d{4}): <a href="(/blog/[^"]+)">([^<]+)</a></li>'
)


def strip_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)


def load_posts():
    html = strip_comments(BLOG_INDEX.read_text())
    posts = []
    for date_str, href, title in POST_RE.findall(html):
        date = datetime.strptime(date_str, "%b %d, %Y")
        posts.append({"date": date, "href": href, "title": title})
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def render_feed(posts) -> str:
    items = []
    for post in posts:
        url = SITE_URL + post["href"]
        pub_date = post["date"].strftime("%a, %d %b %Y 00:00:00 GMT")
        items.append(
            "\t<item>\n"
            f"\t\t<title>{escape(post['title'])}</title>\n"
            f"\t\t<link>{escape(url)}</link>\n"
            f"\t\t<guid>{escape(url)}</guid>\n"
            f"\t\t<pubDate>{pub_date}</pubDate>\n"
            "\t</item>"
        )
    items_xml = "\n".join(items)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
\t<title>{escape(FEED_TITLE)}</title>
\t<link>{SITE_URL}/blog/</link>
\t<description>{escape(FEED_DESCRIPTION)}</description>
\t<language>en-us</language>
\t<atom:link xmlns:atom="http://www.w3.org/2005/Atom" href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{items_xml}
</channel>
</rss>
"""


def main():
    posts = load_posts()
    FEED_PATH.write_text(render_feed(posts))
    print(f"Wrote {FEED_PATH} with {len(posts)} post(s).")


if __name__ == "__main__":
    main()
