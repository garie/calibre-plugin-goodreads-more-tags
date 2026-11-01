# Fetch Goodreads pages without Camoufox

## Status

Accepted

## Context

calibre 9.17 ships Camoufox, a headless browser that metadata sources can use to get past bot protection such as
Cloudflare. calibre's Amazon source uses it. A user proposed it for the Kobo Metadata plugin, whose source site is
behind Cloudflare
([NotSimone/Kobo-Metadata#19](https://github.com/NotSimone/Kobo-Metadata/issues/19)).

The plugin fetches each book's shelves page (`https://www.goodreads.com/book/shelves/<id>`) with calibre's standard
browser, `plugin.browser.clone_browser()`. The Goodreads plugin, version 1.10.0, also uses the standard browser for
the book pages that the integration depends on.

What calibre 9.17 offers a third-party source:

- Setting `uses_camoufox_worker` on a source doesn't help by itself. calibre's shared Camoufox worker for metadata
  only has handlers for `amazon` and `google_images`, and reports "There is no camoufox handler for the metadata
  source" for anything else.
- `calibre.web.automate.recipes.Browser`, which news recipes use, has `open`, `open_novisit`, and `clone_browser`,
  so it could stand in for the standard browser. It lives in calibre's recipe code and isn't documented as an API for
  plugins, so it may change without notice.

Using Camoufox has costs. In the test suite it took 18 to 20 seconds to start. Before its first request, it warms up
by visiting unrelated sites (Wikipedia, BBC, Reddit, amazon.com). On macOS it can trigger a system prompt asking to
allow notifications. It requires calibre 9.17, and the plugin supports calibre 5.0 and later.

On 2026-11-01, Goodreads did not challenge plain requests. Fetching the shelves page with `curl` returned HTTP 200,
following a redirect to `/work/shelves/<work id>`, with all 100 `div.shelfStat` entries and no challenge page.

## Decision

Keep fetching Goodreads pages with calibre's standard browser. Don't use Camoufox.

Revisit this if Goodreads starts challenging or blocking requests. A `curl` of a shelves page will show it: a
non-200 status, a challenge page, or no `div.shelfStat` entries. If the plugin switches then, use
`calibre.web.automate.recipes.Browser` when it is available, and fall back to the standard browser on older calibre
versions or when Camoufox fails.

## Consequences

Fetching tags adds no browser startup time and visits no unrelated sites, and the plugin keeps working on calibre
versions before 9.17.

If Goodreads adds bot protection, fetching shelves fails until the plugin switches. The Goodreads plugin would likely
break at the same time, since it fetches Goodreads book pages the same way, so integration would stop working
whatever this plugin does.
