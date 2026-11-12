# GSMG 5 BTC — "esrever" + 29-dropped-letters + dbbi/faed balancing test

**Date:** 2026-11-11
**Approved by:** Hazrat (bounded test; no new password generation, no contact
with the creator, no privatekeys.pw key/balance pages)
**Script:** `~/workspace/gsmg_esrever.py` · **Results JSON:**
`~/workspace/gsmg-esrever-results.json` · **Source page (saved):**
`~/workspace/gsmg-salphaseion.html`
**Result: 0 HITS.** (See §6 for the exact counts.)

---

## 1. Step 1 — reconstructing the source data from the live page

The live SalPhaseIon page was fetched with curl (HTTP 200, 4,536 bytes):
`https://gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`
(SHA-256 of `GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`).

The page body is **1,075 single-character tokens** (floflo's count, confirmed
here by direct extraction). Structure (z = separator token):

| Chunk | Tokens | Content |
|---|---|---|
| 0 | 765 | abba stream: 91-token prefix + 104-bit binary run + 570-token segment |
| 1 | 63 | "agda" section |
| 2 | 29 | "cfob" section |
| 3 | 98 | "shabe four first hint is your last command" + blob2 base64 (first half) |
| 4 | 116 | abba run + Dualite base64 + "shabe f a n s t o o" |

Decodes verified from the live page in this run:

- **91-token prefix** (the "91-letter phrase"):
  `dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe`
- **104-bit binary run** (a=0, b=1, tokens 91–195 of chunk 0) → **`matrixsumlist`**
- **"agda" section** (letters o=0, a=1, …, i=9 → decimal integer → bytes) →
  **`lastwordsbeforearchichoice`**
- **"cfob" section** (same encoding) → **`thispassword`**
  (Note: the encoding is a decimal integer → bytes, not hex as the README
  shorthand says; both decodes reproduce exactly.)
- **Blob2 on the page = the kit's blob2**: same salt `3ab585348552415d`,
  80 bytes ciphertext. The kit's three blobs are current and correct.

### The 570-character Bifid segment

The segment is chunk 0, tokens 195–765 (everything after the
`matrixsumlist` binary run) — exactly 570 tokens, alphabet a–i:

`faedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafaecghggcdaihehahbahigceifgbfgefgaifabifagaegeacgbbeagfggeeggafbacgfcdbeiffaafcidahgdeefghhcggaegdebhhegeghcegadfbdiagefcicggifdcgaaggfbigaicfbhecaecbceiaicebgbgiecdeggfgegaedggfiiciiififhggcgfgdcdggefcbeeigefibgibggghhfbcgifdehedfdagicdbhicgaiedaehahghhcihdghfhbiicecbiichihiiigiddgehhdfdchcbafgfbhaheagegecafehgcfggggcagfhhghbaihidiehhfdeggdgcihggggghadahigigbgecgedfcdggaccdehiicigfbffhggaeidbbeibbeiifdgfdhieeeieeecifdgdahdiggfhegfiaffiggbcbcehceabfbedbiibfbfdedeehgigfaaiggagbeiichiedifbehgbccahhbiibibbibdcbahaidhfahiihic`

Bifid decryption (keyed square `DBIFHCEG`, period 570, identity map
a→A … i→I, standard Bifid with interleaved coordinates) gives a 570-char
plaintext **starting with `BTCSEED`** — the known calibration, reproduced
exactly:

`BTCSEEDDEOEMCKEADHBSCHDKBDCSDKDVBXCPCOCHCRDICIBQEEBDDBCNDSBDCPDGCPDNCNCSESCGDDCLENBMCUDUCQCACDELDZELCMEFDFESDODWCKBYCUBWBAESBWBNEMEDEADOBRCPBGBQCOEGBSENESBLBTESDADPDUESCPCREACNCKCSCDCNBEDKCKCTCLBRENENCCEGELCNCUBSBGESEIENDUEFDDBACKDNBSDSESCRBSEBBLBIERDVCOBDCCEGBSEOBVBVCDEMCPCSCGELDIEGDADWDYCACPEGENBYEBCGCLCRDBBRDGDBDMERCNCGDTCDBNCFCLCPDNBRBBEBCNEREREMELDSDADLENCQBOCHDQDGBXEGCFCUEEEIDACIEADOCTDNEIEGDEELDEELBMCKEDBBEACMCODREMCCCMCSCGDBCOCMDTDLBMCDBMBMDPBSDNBSDYEOEOCIENBSEOBICBBBCNCNECDUCIBECCCGDOCMEEDUBNDEELBLBACPCPCMDXDXDRDGCBCMDNDRDDECDWEADHBTDICQCPDOEFDHDGDXDPCIEL`

### The two interleaved streams

Splitting the plaintext by position:

- **Stream A** (1-based odd positions, 285 chars) — alphabet **{B, C, D, E}**
  only:
  `BCEDEECEDBCDBCDDBCCCCDCBEBDCDBCDCDCCECDCEBCDCCCEDECEDEDDCBCBBEBBEEEDBCBBCEBEEBBEDDDECCECCCCCBDCCCBEECEECCBBEEEDEDBCDBDECBEBBEDCBCEBEBBCECCCEDEDDDCCEEBECCCDBDDDECCDCBCCCDBBECEEEEDDDECBCDDBECCEEDCEDCDEEDEDEBCEBECCDECCCCDCCDDBCBBDBDBDEECEBEBCBCCEDCBCCDCEDBDEBBCCCDDDDCCDDDEDEDBDCCDEDDDDCE`
- **Stream B** (1-based even positions, 285 chars) — full 25-letter alphabet
  (A–Z minus J):
  `TSEDOMKAHSHKDSKVXPOHRIIQEDBNSDPGPNNSSGDLNMUUQADLZLMFFSOWKYUWASWNMDAORPGQOGSNSLTSAPUSPRANKSDNEKKTLRNNCGLNUSGSINUFDAKNSSSRSBLIRVODCGSOVVDMPSGLIGAWYAPGNYBGLRBRGBMRNGTDNFLPNRBBNRRMLSALNQOHQGXGFUEIAIAOTNIGELELMKDBAMORMCMSGBOMTLMDMMPSNSYOOINSOIBBNNCUIECGOMEUNELLAPPMXXRGBMNRDCWAHTIQPOFHGXPIL`

(Note on naming: floflo's "odd-position stream" is 0-based odd indices =
Stream B here; the audit's "even stream over {B,C,D,E}" is Stream A here.
The substance — one 285-char stream over the full alphabet, one over
{B,C,D,E} — is verified either way.)

### The 256-symbol object and the 29 dropped letters

Stream B contains **13 × I and 16 × O = 29 letters**. Removing them gives
the **256-symbol object** (256 chars, 23 letters, A–Z minus J, I, O):

`TSEDMKAHSHKDSKVXPHRQEDBNSDPGPNNSSGDLNMUUQADLZLMFFSWKYUWASWNMDARPGQGSNSLTSAPUSPRANKSDNEKKTLRNNCGLNUSGSNUFDAKNSSSRSBLRVDCGSVVDMPSGLGAWYAPGNYBGLRBRGBMRNGTDNFLPNRBBNRRMLSALNQHQGXGFUEAATNGELELMKDBAMRMCMSGBMTLMDMMPSNSYNSBBNNCUECGMEUNELLAPPMXXRGBMNRDCWAHTQPFHGXPL`

The **29 dropped letters, in extraction order**:

`OOIIOOOIIOOIOIIOIOOOOIOIIOIOI`

Dropped positions in Stream B (0-based):
4, 18, 21, 22, 54, 67, 72, 108, 123, 126, 131, 140, 182, 191, 193, 195,
198, 210, 218, 231, 232, 233, 236, 237, 244, 248, 274, 277, 283.

**What the 29 letters spell: nothing legible.** They are only I's and O's —
no English word, no fragment. As bits (I=1, O=0):
`00110001100101101000010110101` (= 103,993,525 = 0x632D0B5);
with the opposite assignment (O=1, I=0):
`11001110011010010111101001010` (= 432,877,386 = 0x19CD2F4A).
Both 29-bit values were tested as keys (§4). Neither hits.

---

## 2. Step 2 — "esrever" tests

"esrever" = "reverse" spelled backwards, the earliest author hint. Already
explained for the image URL (the 192 bits of `gsmg.io/theseedisplanted`
reversed = the private key of the second "Good job, Neo!" address), but not
exhausted on the final-gate objects. Tested as passwords (each through
crack.py's forms: as-is, lowercased, spaceless, SHA-256 hex of each):

| # | Candidate (password phrase) |
|---|---|
| E1 | 256-symbol object, reversed |
| E2 | 570-char segment, reversed |
| E3 | Stream B (285), reversed |
| E4 | Stream A ({B,C,D,E}), reversed |
| E5 | Bifid plaintext (570), reversed |
| E6 | 91-letter prefix, reversed |
| E7 | 256-symbol object, forward (re-test) |
| E8 | Segment, forward (re-test) |
| E9 | Stream B, forward (re-test) |
| E10 | Stream A, forward (re-test) |
| E11 | Bifid plaintext, forward (re-test) |
| E12 | 91-letter prefix, forward (re-test) |
| E13 | Dualite blob base64, reversed |
| E14 | Dualite blob ciphertext hex, reversed |
| E15 | Blob1 base64, reversed |
| E16 | Blob2 base64, reversed |

Each was tried against **all three blobs × both digests (SHA-256 + MD5)**
with the corrected reader (floflo `readings()`, both address forms, prize +
second escrow). Additionally, every valid-padding plaintext produced during
this test was also read **reversed and bit-reversed** through `readings()`
(the "esrever" reading of the locks' plaintexts), plus the 2k/k/2 neighbours
and the 8 split-key combinations for ≥64-byte plaintexts — the same
corrected standard as the audit re-run.

---

## 3. Step 3 — the 29 dropped letters as passwords and as keys

Passwords (through crack.py's forms, both digests, all three blobs,
corrected reader):

| # | Candidate |
|---|---|
| S1 | `OOIIOOOIIOOIOIIOIOOOOIOIIOIOI` (as-is) |
| S2 | Same string reversed: `IOIOIIOIIOOOIOIIOIIOOOIIOO` |

Direct key checks (32-byte keys, both address forms, prize + second
escrow) — 7 keys:

| # | Key |
|---|---|
| D1 | SHA-256 of the 29 ASCII bytes |
| D2 | 29 ASCII bytes left-padded with 3 zero bytes to 32 |
| D3 | 29 ASCII bytes right-padded with 3 zero bytes to 32 |
| D4 | 29-bit integer (I=1, O=0) as 32-byte big-endian |
| D5 | 29-bit integer (O=1, I=0) as 32-byte big-endian |
| D6 | Same as D4 for the reversed string |
| D7 | Same as D5 for the reversed string |

---

## 4. Addition — dbbi / faed balancing

The kit file `dbbi_faed_cands.txt` holds two blocks over the a–i alphabet:

- **dbbi** (canonical lowercase form) = the 91-letter prefix:
  `dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcccgbfbeeggecbedcibfbffgigbeeeabe`
  (also present uppercase, as digits a=0..i=8, and as hex — line 4 is
  SHA-256 of the prefix, `71fe4625…`; line 1 is the prefix minus its first
  4 chars "dbbi"; line 5 is SHA-256 of an unidentified variant.)
- **faed** (canonical lowercase form) = the 570-char segment (see §1).
  (Also present uppercase, as digits, and as hex — line 10 is SHA-256 of
  the segment, `066191b4…`; line 7 is the segment minus its first 4 chars
  "faed"; line 11 is SHA-256 of an unidentified variant.)

Hypothesis: the yinyang operation is a balancing translation between these
two blocks, which share the nine-symbol alphabet. Operations tested,
aligned from the start, on digit values (a=0 … i=8):

| Alignment | dbbi form | faed form |
|---|---|---|
| A1 prefix91 | 91 chars | first 91 chars |
| A2 tiled570 | dbbi repeated to 570 chars | 570 chars |
| A3 padded570 | dbbi + 'a' padding to 570 chars | 570 chars |

Operations per alignment: letterwise **add mod 9**, **subtract
(dbbi−faed) mod 9**, **subtract (faed−dbbi) mod 9**, **XOR on digit values
then mod 9** (plus the XOR values as a hex string), **interleave**
(alternating dbbi/faed), **concatenation both orders**. Each result was
tested as a letter string (a=0 convention), as a digit string in both
conventions (digits 0–8 and digits 1–9), and each of those **reversed**.
Also tested, per operation: the concatenation
`matrixsumlist` + `lastwordsbeforearchichoice` + <result letters>.

Resulting letter strings (21; digit-string and reversed forms are derived
from these):

| Alignment / operation | Result (letters) |
|---|---|
| A1 add-mod9 | `ibfchcfcfhdfabafhhbdecagiaabchhfhadehchhegfgafhafhbhiccifdca` + `…` (91) |
| A1 sub-dbbi-faed-mod9 | `hbgfeigdigiddbhacehiefffaddhbbedecaehdbebiffagdgaehdccedghce` + `…` (91) |
| A1 sub-faed-dbbi-mod9 | `cidefbdgbdbggicahfcbfeeeaggciifgfhafcgifibeeadgdafcghhfgdchf` + `…` (91) |
| A1 xor-mod9 | `gbfchdfdbhdffbaahhcdecfeaffcdhhfhaaehdhhbgfeafhfahchgccgfccf` + `…` (91) |
| A1 interleave | `dfbabeidbgfgbehecdcfbcebgdbaibhhahbgegbceaidhcbfeegdgdeggfed` + `…` (182) |
| A1 concat-dbbi+faed | `dbbibfbhccbegbihabebeihbeggegebebbgehhebhhfbabfdhbeffcdbbfcc` + `…` (182) |
| A1 concat-faed+dbbi | `faedggeedfcbdabhhggcadcfeddgfdgbgigaaedggiafaecghggcdaihehah` + `…` (182) |
| A2 add-mod9 | (570 chars; full string in `gsmg-esrever-results.json`) |
| A2 sub-dbbi-faed-mod9 | (570 chars; full string in results JSON) |
| A2 sub-faed-dbbi-mod9 | (570 chars; full string in results JSON) |
| A2 xor-mod9 | (570 chars; full string in results JSON) |
| A2 interleave | (1,140 chars; full string in results JSON) |
| A2 concat-dbbi+faed | (1,140 chars; full string in results JSON) |
| A2 concat-faed+dbbi | (1,140 chars; full string in results JSON) |
| A3 add-mod9 | (570 chars; full string in results JSON) |
| A3 sub-dbbi-faed-mod9 | (570 chars; full string in results JSON) |
| A3 sub-faed-dbbi-mod9 | (570 chars; full string in results JSON) |
| A3 xor-mod9 | (570 chars; full string in results JSON) |
| A3 interleave | (1,140 chars; full string in results JSON) |
| A3 concat-dbbi+faed | (1,140 chars; full string in results JSON) |
| A3 concat-faed+dbbi | (1,140 chars; full string in results JSON) |

(Note: add/sub mod 9 give the same letter strings under the a=1..i=9
convention as under a=0..i=8 — the two conventions differ only in the
digit strings, which were both tested.)

---

## 5. Oracle and self-checks

- Self-checks PASS: privkey-1 vectors exact (compressed
  `1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH`, uncompressed
  `1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm`); the escrow's known on-chain public
  key hashes to the prize address.
- Every password was tried against all three blobs with **both** digests
  (SHA-256 and MD5 — Cosmic Duality uses MD5, the small blobs' digest is
  unknown) and read with the corrected reader: floflo `readings()`
  (SHA-256, first32, last32, SHA-256(first64), hex, WIF) on the plaintext,
  its reverse, and its bit-reverse; 2k/k/2 neighbours; 8 split-key
  combinations for ≥64-byte plaintexts. Every key reading was checked
  against **both** the prize address
  `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` **and** the second escrow
  `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`, in **both** compressed and
  uncompressed forms.
- Bonus: every candidate phrase was also checked against the unmessaged
  planted address `1NULY7DhzuNvSDtPkFzNo6oRTZQWBqXNE9` (SHA-256 of the
  phrase, bit-reversed SHA-256, phrase padded to 32 bytes) — the exact
  offline oracle from floflo leads §1.

---

## 6. Counts and result

| Measure | Count |
|---|---|
| Password phrases | 171 (16 esrever + 2 twenty-nine-letter + 153 dbbi/faed) |
| Password forms (crack.py expansion) | 368 |
| Decrypt attempts (forms × 3 blobs × 2 digests) | 2,208 |
| Valid-padding plaintexts | 8 |
| Key readings checked | 359 |
| Direct 29-letter key checks | 7 |
| Third-door checks | 684 |
| Long entirely-printable plaintexts (>64 bytes) | 0 |
| **Hits (prize or second escrow, either form)** | **0** |
| Third-door hits | 0 |

The 8 valid-padding plaintexts are exactly the chance rate (2,208 / 256 ≈
8.6 expected) — padding accidents, none of which yielded a key under any
reading. Run time 0.8 s.

**Verdict:** the "esrever" readings of the 256-symbol object, the segment,
both streams, the Bifid plaintext, the 91-letter prefix, and the blob
base64/ciphertexts do not open any blob; the 29 dropped letters spell
nothing and do not open any blob as a password or as a key; the dbbi/faed
balancing operations (add, subtract both ways, XOR, interleave,
concatenation, reversed, both digit conventions, plus the
matrixsumlist+lastwords concatenation) do not open any blob. The two
floflo leads §5–§6 are now exhausted as specified — the only remaining
prerequisite they named (reconstructing the segment from the live page)
is done here, and the readings themselves are negative.

**What remains open** (unchanged from the audit): the final password
itself ("in front of your eyes but youre not seeing it"); the single tool
that built every phase (unnamed publicly); the 11,473 valid-padding
plaintexts (file not public); the "tiny hint" (2026-01-01); `NOTES`
(2026-07-16); the Cosmic Duality PDF (19.5 MB, unexamined, in the
gitignored Telegram export).
