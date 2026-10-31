# Goodreads More Tags

## About this fork

This is a fork of [MaienM/calibre-plugin-goodread-more-tags](https://github.com/MaienM/calibre-plugin-goodread-more-tags).
Upstream has had no commits since version 1.2.1 in November 2020, and the plugin needs fixes to keep working with
current calibre and the current Goodreads site. This fork exists to carry those fixes.

### Where 1.2.1.2 came from

The calibre plugin index offers version 1.2.1.2, but that version was never committed upstream. It exists only as the
zip on the [plugin index](https://plugins.calibre-ebook.com/), which mirrors the attachment on the first post of the
[MobileRead thread](https://www.mobileread.com/forums/showthread.php?p=3875236). The thread's version history stops at
1.2.1, and the index still credits the original author, so who made 1.2.1.2 is unknown. The files inside the zip are
dated May and July 2022.

The `v1.2.1.2` tag is that zip's contents, committed verbatim on top of upstream's `v1.2.1`. Before importing it, I
checked two things:

- The 1.2.1 zip previously served by the index is byte-identical to upstream's `v1.2.1` source.
- The 1.2.1.2 changes are limited to a Qt6 port of the settings dialog and a fix to how the shelves page is read (see
  the version history below). They add no network, filesystem, `exec`, or subprocess calls.

Tags up to `v1.2.1` are upstream's. Later tags belong to this fork.

## Overview

This plugin scrapes the shelves page of Goodreads to provide more tags than the top 4 (which are shown on the main page
and scraped by the Goodreads plugin).

This plugin will only provide tags. It is meant to be used as a companion to the
[Goodreads plugin](https://www.mobileread.com/forums/showthread.php?t=130638), and it is essentially an extended version
of the genre -> tag mapping included in that plugin.

## Main Features

- Can retrieve the shelves page of Goodreads to provide more tags.
- Customizable mapping from shelf name -> tags. A shelf can be mapped to multiple tags, and multiple shelves can map to the same tag(s).
- Fine-grained filtering to only keep tags that enough people agree on.
- Integrates with the Goodreads plugin to provide tags for all of its results.

## Special Notes

- Requires calibre 5.0 or later.
- If used without the base Goodreads plugin, it will only get tags for books that have a Goodreads identifier.

## Installation Notes

- Download the attached zip file and install the plugin as described in the [Introduction to plugins thread](https://www.mobileread.com/forums/showthread.php?t=118680).
- Note that this is not a GUI plugin so it is not intended/cannot be added to context menus/toolbars etc.
- Customize your desired genre -> tag mappings and other options from the metadata download configuration screen. Hover over the ? symbols to get an explanation of what the various options do.

## Version History

<b>Version 1.2.1.3</b> - 31 October 2026

- Fixed the settings dialog failing to open on calibre 9
  ([#1](https://github.com/garie/calibre-plugin-goodreads-more-tags/issues/1)).
- Fixed error logging when fetching or parsing a shelves page fails.

<b>Version 1.2.1.2</b> - 2022 (exact date unknown; not an upstream release, see "Where 1.2.1.2 came from")

- Ported the settings dialog to Qt6, for calibre 6 and later.
- Fixed reading shelf counts after Goodreads changed the shelves page markup.
- Raised the minimum calibre version to 5.0.

<b>Version 1.2.1</b> - 15 November 2020

- Fixed an error in adding a new shelf to the mapping.
- Fixed an error in removing a shelf from the mapping.
- Fixed an error in saving the preferences.

<b>Version 1.2.0</b> - 14 November 2020

- Update to work with Calibre 5/Python 3.
- Speed up the case where the Goodreads plugin is installed but not currently enabled as a metadata source.
- Don't provide any results if the list of tags after mapping + filtering is empty.

<b>Version 1.1.0</b> - 15 December 2019

- Large internal changes that should resolve the problems with hanging/reliability.
- There are now some settings for the integration with the base Goodreads plugin.

<b>Version 1.0.1</b> - 04 August 2019

- Fixed the spelling of threshold.

<b>Version 1.0.0</b> - 04 August 2019

- Initial release.

