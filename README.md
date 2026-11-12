# GSMG 5 BTC — Research Notes for Fresh Eyes

**Status: UNSOLVED since 2019.**

- Prize: **1.25649674 BTC** at `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` (129 transactions, never spent by a solver; verified on-chain, November 2026)
- Second escrow: **3.75055856 BTC** at `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`
- Creator: "Jrk Bgrt", Telegram @SoWut — silent since 16 July 2026
- Puzzle site: `gsmg.io` (the puzzle is the site's only live artifact; the trading bot shut down)

This repository is an independent research record. It is published so that
fresh eyes can see exactly what has been tried, what is closed, and what is
still open — without repeating years of work. **No private key, seed phrase,
or credential is published here.** The work is research only: nothing in
this repo moves money, broadcasts a transaction, or claims the prize.

---

## 1. The puzzle in brief

A poster (a 14×14 grid, a white rabbit, a QR code) leads to a chain of
stages. Each solved stage yields an answer that opens the next AES-256-CBC
blob. The final gate is a single missing string: its lowercase hex SHA-256
opens **four** locked blobs at once (the final Phase 3.2 blob, the
SalPhaseIon blob, the Cosmic Duality blob, and a fourth "urlblob" recovered
in 2026 from a public repository). Everything before that gate is solved.

## 2. The solved trail

| Stage | Answer / result |
|---|---|
| Poster spiral (black/blue = 1, white/yellow = 0, counterclockwise) | `gsmg.io/theseedisplanted` |
| Rebus images → Logic, "The Warning" | `theflowerblossomsthroughwhatseemstobeaconcretesurface` |
| Phase 2 AES password | lowercase SHA-256 hex of `causality` |
| Phase 3 — seven parts concatenated (227 characters) | causality, Safenet, Luna, HSM, 11110, Bitcoin source-code data (main.cpp line 1616), a FEN chess position after the one non-mating move Rc6+ |
| Three riddles | `jacquefresco`, `giveitjustonesecond`, `heisenbergsuncertaintyprinciple` |
| Phase 3.2 plaintext | an Architect monologue (Beaufort, key `thematrixhasyou`), a 149-digit string, a checkerboard riddle |
| 149-digit string → straddling checkerboard | the 91-letter phrase `commonsolutionistointroduecentralauthorityormintthatcheckseverytransactionfordoublespending` (note the puzzle's exact spelling, "introdue") |
| Final page | 1,075 single-character tokens; a 570-letter Bifid segment (keyed square `DBIFHCEG`) whose output begins `BTCSEED` |

## 3. The final gate — the exact rules

- **Password convention** (stated by the creator on the archived Phase 2/3
  page): the password is the **lowercase hex SHA-256 of the answer X**,
  one-round EVP_BytesToKey. Phases 2–3 use the SHA-256 digest; the Cosmic
  blob uses the MD5 digest.
- **The four blobs** (salts, public): final Phase 3.2
  `b45a5e3d827593ca` (80 bytes ciphertext), SalPhaseIon
  `3ab585348552415d` (80 bytes), Cosmic Duality `2d3f6fe06dc950e6`
  (1,328 bytes), urlblob `74c974e3f92e64b5` (96 bytes). The blobs
  themselves are **not** in this repo — they are in the public puzzle kit
  (see §8).
- **What counts as a hit.** A valid PKCS7 padding alone is **never** a
  hit (it happens by chance about 1 time in 256). A real hit requires the
  decrypted plaintext to yield the prize key — checked four ways
  (SHA-256 of the plaintext, first 32 bytes, last 32 bytes, SHA-256 of the
  first 64 bytes) — whose address matches a prize escrow, in either
  compressed or uncompressed form. Every negative in this repo was produced
  by that rule, with the harness certified by acceptance vectors first
  (privkey-1 reproduces both known addresses; a synthetic Salted__ blob
  with a known password and key is recovered through the same code path).
- **Three oracles** were used throughout: (1) the six remaining
  hash-named pages (below), (2) the "neighbours" elliptic-curve oracle
  (the prize key P and 2P, P/2, P+G, P−G — verified by direct EC
  computation), (3) the four blobs.

## 4. What has been tested — the ledger

Honest headline: **more than 30 million blob decryptions and more than
2 million hash comparisons, zero hits.** The table lists the distinct
recorded runs; the per-record files in `records/` carry the detail.

| Run (record) | Scale | Result |
|---|---|---|
| Full-kit audit, Nov 2026 (`records/gsmg-blob4-recovery.md`) | 2,908,328 passwords × SHA-256 + MD5 × 3 blobs ≈ 17.4M decryptions | 0 hits |
| Blob2 corrected readings A+B (`scripts/gsmg_blob2_variants.py`) | 11,633,312 attempts | 0 hits |
| Dynamic replay, reconstructed (`records/gsmg-dynamic-replay.md`) | 15,483 candidates, 650,286 decryptions | 0 hits |
| Closing protocol — self-referential ops + mixed-shape replay (`records/gsmg-closing-protocol.md` summarised in §7; full record withheld, see §8) | 3,719 candidates, 133,884 decryptions | 0 hits |
| "Dual Reading" waves 1–2 (`records/gsmg-dual-reading.md`) | 322 candidates, 11,592 decryptions | 0 hits |
| Mr. Robot + Jacque Fresco harvest (`records/gsmg-mrrobot-fresco.md`) | 4,915 fragments, 176,940 decryptions | 0 hits |
| Creator's own words, full fragment sweep (`records/gsmg-creator-words-sweep.md`) | 937 fragments, 33,732 decryptions | 0 hits |
| Geometric reading (`records/gsmg-geometric-reading.md`) | 66 candidates, 2,376 decryptions | 0 hits |
| Meaning-reconstruction pass (`records/gsmg-meaning-pass.md`) | 68 phrases, 1,216 attempts | 0 hits |
| YOUWON middle block (`records/gsmg-youwon49.md`) | 3,012 phrases, 18,072 attempts | 0 hits |
| Cover audit (`records/gsmg-cover-audit.md`) | 68 candidates, 2,448 decryptions | 0 hits |
| Close reading (`records/gsmg-close-reading.md`) | 84 candidates, 3,024 decryptions | 0 hits |
| Footprint candidates (`records/gsmg-footprint.md` summarised in §7; full record withheld, see §8) | 10 candidates, 792 decryptions | 0 hits |
| Tool-menu test (`records/gsmg-tool-check.md`) | 8,514 transform outputs as passwords | 0 hits |
| Matrix trilogy harvests (`records/gsmg-architect-harvest.md`, `records/gsmg-oracle-smith-merovingian.md`, `records/gsmg-trilogy-227-neighbors.md`, `records/gsmg-phases-123.md`) | 24,000+ fragments, ~87,000 hashes | 0 hits |
| Hash dictionary, cross-domain (`records/gsmg-hash-dictionary.md`) | 30,652 combinations, 153,260 hashes | 0 hits |
| Preimage hunt (`records/gsmg-xor-triangle-preimages.md`) | ~1,784,285 candidate hashes | 0 hits |
| Neighbours EC oracle (`records/gsmg-trilogy-227-neighbors.md`) | 107,915 scalar tests over 73,347 candidates | 0 hits |
| EC combinations (`records/gsmg-ec-combinations.md`) | 3,960 scalar combinations | 0 hits |

## 5. What is closed (do not re-run these)

- **The Matrix trilogy as text.** The full Architect scene, Oracle,
  Smith, Merovingian, and the complete Reloaded script were harvested in
  four shapes (pure text, hex text, raw bytes, "humph" prefix). The
  harvest *did* find two preimages — both Architect quotes (see §6) — but
  neither opens a blob.
- **Mr. Robot and Jacque Fresco as text.** All four seasons of Mr. Robot
  dialogue (2,427 sentences) and Fresco's books, film and interviews
  (80 sentences) — 0 hits.
- **The creator's own words.** Every sentence, sentence pair and whole
  message of his 482 Telegram messages as fragments — 0 hits. If the
  answer is in his words at all, it is not a sentence he typed.
- **The Bifid output, both halves.** The 570-letter output splits into
  two interleaved 285-letter streams. The odd stream (minus I/O) gives
  the 256-symbol object everyone tested. The even stream uses only B, C,
  D, E — a 2-bit encoding — and had never been tested on its own until
  wave 2 of the Dual Reading. It is now tested as a password, as 2-bit
  decodes under all 24 letter mappings, and as a direct key. 0 hits.
- **The 227-character Phase 3 digest as a password.** The digest
  `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5`
  had only been tested as a key scalar; it is now tested as an AES
  password. 0 hits.
- **The geometry of the non-textual objects.** The poster (rabbit is a
  195×195 px line drawing, not a code; QR is version 4; coloured cells
  sit at spiral indices 7, 15, 23, …, 191), the Decentraland scene
  (fully decompiled from its source map: 9 static cubes, one
  click-to-play sound, one blue sign — no hidden behaviour, no
  animation, no second trigger), the audio spectrogram (~64.5 Hz
  odd-harmonic drone with three broadband clicks — no code), and the
  book cover (a yin-yang in the puzzle's two colours). 66 candidates
  derived from the measurements. 0 hits.
- **The split-key idea.** The two "halves" are keys to two now-empty
  public addresses; no combination of them gives the prize. The 1,327-byte
  Cosmic plaintext they came from was retracted as a padding accident.
- **The "SOLVED" claims** in the public issue tracker (issues #69, #120,
  #121) are false. The 79-byte "community canonical" SalPhaseIon
  plaintext is unfounded. SHAKMODEST does not exist anywhere.
- **The filter bug is real but already replayed.** An appearance-based
  acceptance filter in 98 of 213 scripts required decrypted plaintext to
  look like printable ASCII, silently discarding correct passwords whose
  decryption yielded binary key bytes. The dynamic pattern classes were
  reconstructed and re-run under the corrected address-only reader:
  0 hits. What was *not* replayed is the literal generation logic of
  those 213 scripts — they sit in a private folder (see §7).

## 6. The hash-chain pages — six preimages still unknown

Twelve 64-hex pages exist (Wayback CDX listing, 419 URLs). Six are
identified:

| Page hash | Preimage |
|---|---|
| `89727c59…` | SHA-256 of `GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` |
| `4f7a1e4e…` | SHA-256 of the 1,327-byte Cosmic plaintext |
| `e24bd2c0…` | SHA-256 of `ourfirsthintisyourlastcommand` |
| `f9719d6d531e6c3b5129644cd05da57bc6fdd075c9a61267c41d4b9627936096` | SHA-256 of the **raw 32 bytes** of the SalPhaseIon hash |
| `c1780cbb…` | SHA-256 of `hopeisthequintessentialhumandelusion` (Architect) |
| `10d6a2c5…` | SHA-256 of `humphhopeisthequintessentialhumandelusionsimultaneouslythesourceofyourgreateststrengthandyourgreatestweakness` (Architect) |

Six remain unknown. If you can find a preimage for any of these, it may
be the answer or point at it:

```
0b0f37ecaf7107f86ee2f477992f25bc7abe8f799d0dd713658c17d37496ee32
21ef053324184a4db5dc19b760e2d6ef61b07376a6f8a1514bb529d99de1fe0f
673e3b1a60ebe6fc4a8be88acde2600e12afd9efb2543e26b1b30039f8356b0d
a2aefdbb953b70aa20d640effda4accee1e1f48acf1e4fcebdc2fc011418b0b1
aca20ae7c6b5f425bdd9bd809583b28fd086b3380990689e37b6e94f3fb5ed9a
c2eef34b479eb6c89c7aa89c49229ff5f67563da4e56d5782574489c4b776625
```

(The six known pages split 4 internal + 2 quotes, so the remaining six
are likely a mix. The internal side is now exhausted; the quote side is
exhausted for the Matrix trilogy, Mr. Robot and Fresco.)

## 7. Open leads, ranked

1. **The insight / the meaning.** The only unexhausted route. The
   creator's own difficulty note says the third door opens with "a rule
   of the creator's from early 2020 read on a non-textual object". The
   poster's geometry, the scene's behaviour, the spectrogram and the
   cover have all been measured and tested — so if the rule exists, it is
   a reading nobody has yet stated, not another measurement of these
   objects.
2. **The creator speaks again.** Silent since 16 July 2026. His only
   self-declared hint is that his close friends have the best chance —
   which points at personal knowledge, not public material.
3. **The six unknown hash preimages** (§6).
4. **The literal 213 archived scripts.** They live in floflo777's
   private research folder and are not public. A request to share them
   (and the 11,473 outputs file) was drafted — see
   `records/gsmg-ask-floflo777.md` for the exact text — but could not be
   posted from this account (the GitHub App has no write access to that
   repository). Anyone with access can post it.
5. **cosmic_A.** A file referenced by a formula in the public record
   (`k = cc[833:865] XOR ca[280:312]`) that has never been published.
   Without it the formula cannot run.
6. **The 11,473 outputs file.** Still not public. A residual check only.
7. **The "tiny hint".** The phrase recurs (a 2019 promise of "a tiny
   hint at the start of 2020" and a 2026 New Year message), but its
   content has been tested and opens nothing. Still ambiguous.
8. **The honest fallback.** It may not be solvable from public material.
   The creator has said the actual answer sits on a hidden laptop he has
   not touched in years, and that his close friends have the best chance.
   If the final string is personal knowledge, no amount of public work
   will find it.

## 8. What is NOT in this repo, and why

- **The puzzle kit (the four blobs).** Deliberately excluded. The blobs
  are in the public puzzle kit and the public repositories linked from
  the records; reproducing encrypted blobs here adds nothing.
- **The poster image and the Cosmic Duality PDF.** Copyrighted / the
  puzzle's own artifacts; the records describe the measurements made
  from them.
- **Transcript lines.** The Mr. Robot / Fresco working lines file is
  analysis input only (copyrighted transcripts) and is never published.
- **Five records withheld in full.** `gsmg-closing-protocol.md`,
  `gsmg-yinyang-audit.md`, `gsmg-deep-search.md`,
  `gsmg-creator-profile.md` and `gsmg-footprint.md`, plus the scripts
  `gsmg_closing_protocol.py`, `gsmg_dual_reading.py`,
  `gsmg_ec_combinations.py`, `gsmg_internal_audit.py` and
  `gsmg_footprint_test.py`, are withheld because they contain raw
  private-key material (two already-public, swept keys from the retracted
  Cosmic plaintext), a quoted WIF, a third party's real name, or contact
  details. Their *methods and results* are summarised in this README
  and in the included records; the withheld material itself is not
  needed to reproduce any result.
- **No HALV files, no other puzzles.** This repo is GSMG only.

## 9. How to contribute

- Bring a **named hypothesis with a stated test**, not a wordlist. Every
  solved stage in this puzzle was the output of a transformation on that
  stage's own artifacts — the final answer is very likely an output too,
  not a guessed phrase.
- **Prove the negative.** Any claim that something "doesn't work" must
  come with a certified harness: reproduce the privkey-1 acceptance
  vectors through your code path, and re-find a known-good input (the
  Phase 2 blob under SHA-256 of `causality`) before trusting a zero.
- **A hit is an address match, not a valid padding.** See §3. If you
  think you have the key, verify it derives an address matching a prize
  escrow before announcing anything — and remember the prize can be
  swept by anyone who sees the key first, so claim it privately.
- **Do not pay for hints or keys.** Anyone selling a hint, a key, or
  "help" over DMs for this puzzle is running the classic scam shape.
  The prize is real and on-chain; the only legitimate way to it is
  solving the puzzle.

## 10. Sources

- floflo777's public research: `open-crypto-puzzles`,
  `1-big-prizes/gsmg-io-5btc-puzzle/` (analysis, leads, tested,
  puzzle.json) — the foundation this record stands on.
- The public Hosterjack repository (source of the fourth blob).
- The public puzzle repositories and the Wayback Machine CDX listing
  cited in the records.
- The creator's public Telegram messages (quoted in the records only
  where they bear on the puzzle; no contact was made with the creator
  at any point).

*Published November 2026 as a research record. The prize addresses are
public on-chain data; the research is independent and unaffiliated with
the puzzle's creator.*
