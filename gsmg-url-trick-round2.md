# GSMG — URL-hashing trick, round 2

**Date:** 2026-11-12 ~21:25 CST. At Hazrat's word ("Yes, run the same trick on the
remaining lists"). Same method as the fresh-eyes pass: SHA-256 a candidate string,
compare against the unknown hash-page preimages.

## Targets (3 still-unknown hash pages, full SHA-256)

- `673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d`
- `a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1`
- `aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a`

## Controls — harness proven first

All three known preimages re-found by the script before the main loop ran
(and independently verified with `sha256sum`):

- `anstoo` → `21ef0533…`
- `hopeitisthequintessentialhumandelusion` → `0b0f37ec…`
- `youmeizandself` → `c2eef34b…`

## Sources hashed

| Source | Items | Forms hashed |
|---|---|---|
| (a) Repo file paths — `gsmg-repo`, `floflo-repo`, `apple-repo`, `naddiseo-repo`, `rarsn4-repo` (`.git` internals dropped) | 2,136 paths | as-written, basename, lowercase of both |
| (a2) Publication staging paths (`gsmg-publication/`, 53 files) + puzzle-kit paths (`your_files/gsmg-puzzle-kit/`) | walked | as-written, basename, lowercase of both |
| (b) GitHub issue titles, `floflo777/open-crypto-puzzles` (read-only `list_issues`, all 37 issues, `hasNextPage: false`) | 37 titles | as-written, lowercase |
| (c) Branch names from the 5 local repos | 16 forms | as-written, lowercase, `remotes/origin/` stripped |
| (c) Project/owner names (`gsmg-5btc-research`, `open-crypto-puzzles`, `floflo777`, `H-BILAL-coder`, `gsmg.io`, …) | 9 strings | as-written |

**Total: 4,961 distinct forms hashed. 0 target matches.**

## Result

**0 matches.** The three unknown preimages remain unknown:
`673e3b1a…`, `a2aefdbb…`, `aca20ae7…`.

No oracle run was needed — a match is the only trigger for oracle testing, and
there was none. (A valid padding alone is never a hit; a hit requires a derived
address matching `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` or
`17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`.)

## Explicitly NOT re-run

- The 414 CDX URLs and the 9,192 JS-bundle strings (fresh-eyes pass already hashed
  those — that is where the two identifications came from).
- No closed wave, no large sweep. This was a cheap hash-comparison pass only.

## Not covered (noted, not attempted)

- Issue titles of any other GSMG-related GitHub repo (e.g. the "puzzlehunt" repo
  cited in the deep-research notes) — owner/name not confirmed from local records,
  so no list was fetched. If a repo name is confirmed, its titles are one more
  cheap list for the same trick.
- Reddit/X post titles — no read access used; same caveat.

## Files

- Script: `gsmg_url_trick_round2.py`
- Log: `gsmg-url-trick-round2.log`
- Inputs: `urltrick_paths.txt` (2,136 paths), `urltrick_issue_titles.txt` (37 titles),
  `urltrick_issues.json` (raw `list_issues` result)
