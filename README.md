# Hisha

## Introduction

Hisha (飛車, lit. "rook") is a utility module to fetch \[airing\] anime show information from Anilist.
It accepts a string (that is assumed to be the show's name on Anilist, or a close match thereof), and finds the show information.
If the show is found, a Hisha object is created and returned. If the show is not found, a default Hisha object is created and returned.

This module is designed to simplify fetching show information. It is not guaranteed to be 100% accurate, but should be able to fetch airing show information with high confidence. It contains all errors within itself.

## Usage

Hisha has a single public method that returns a Hisha object:

- `def search(show)`

`def search(show)` accepts a single parameter:

- `show` (required): A String that is the same as a given show's name on Anilist. **This means Hisha cannot automatically identify a show name. You should do this manually or get it beforehand.**

Calling `search()` will request Hisha to make up to (3) calls to Anilist's GraphQL API to attempt to find the show's information. In any case, a Hisha object will be returned. It contains various properties:

| Property             | Type     | Default Value      | Notes            |
| -------------------- | -------- | ------------------ | ---------------- |
| id                   | int      | -1                 |
| id_ani               | int      | -1                 | Same as `id`     |
| id_anilist           | int      | -1                 | Same as `id`     |
| id_mal               | int      | -1                 |
| id_myanimelist       | int      | -1                 | Same as `id_mal` |
| id_kitsu             | int      | -1                 |
| episodes             | int      | -1                 |
| duration             | int      | -1                 |
| popularity           | int      | -1                 |
| average_score        | int      | -1                 |
| banner_image         | str      | ""                 |
| cover_image          | str      | ""                 |
| title                | str      | "Unknown"          |
| title_user_preferred | str      | "Unknown"          | Same as `title`  |
| title_native         | str      | "不明"             |
| title_english        | str      | "Unknown"          |
| title_romaji         | str      | "Unknown"          |
| start_year           | datetime | `datetime.time(0)` |
| end_year             | datetime | `datetime.time(0)` |
