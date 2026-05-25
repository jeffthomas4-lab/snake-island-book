# The Old Roar — Story Map (CYOA Structure v3)

This is the structural source of truth. Every passage, choice, and consequence lives here. When this changes, `prototype.html` and `flowchart.mermaid` change with it.

**Status:** v3 LOCKED. Decisions made:
- Time pressure: HYBRID — no visible tokens, Harbor Keeper says "you have time for four" out loud, reader counts in their head
- Strategy choice: ALL THREE (Stay / Split / Solo) kept
- Endings: TWO ONLY — Crown (full) and Silver (partial). Sun ending dropped.

---

## What changed from v2 (the current prototype.html)

v2 had 3 cosmetic choices per problem that all converged to the same showdown with the same 8 items. Reader's only real choice was order.

v3 introduces:
- **Strategy choice** that gates how the kids approach the world (changes the whole playthrough)
- **Time pressure** (4 tokens — you can't visit everything in one playthrough)
- **Branching within regions** (multiple paths to multiple versions of each item)
- **State-tracked showdown** (beats only fire if you have the prereqs)
- **Three endings** (Crown / Silver / Sun) based on what you brought back
- **Replay hooks** (each ending hints at what you missed)

Real consequences. Real replay value. Still no kid ever looks bad.

---

## State variables

The book tracks five things across passages:

```
kids_played:    Set of {Madison, Chayten, Carson, Reid, Kellen, Keira, Ella, Aiden}
items_earned:   Set of {Map, Voice, Charm, Staff, Stone, Brush, Crown, Pegasus}
allies:         Set of {Branch, Otto, BigCoulee, OldSpeak, Skim, Cliffy, FrogHerald, Hush}
flags:          Set of special discoveries (CanyonSinger, HarborKeeperRecognized, etc.)
```

(No on-page time token. The Harbor Keeper tells the kids "you have time for four" out loud. Reader counts in their head — same gating, no game-ifying.)

For a print book the rest is tracked the old-school way: a single page in the back with a checklist. Kids tick boxes as they earn things. "If you have the Map AND the Crown, turn to 89."

---

## Act-by-act flow

### ACT 1 — REAL WORLD (always read, no branching)

```
P-001  The Synchronized Jump        (NEW — opening ritual, all 8 kids in action)
P-002  Drystone arrives                (dock threat, sign goes up)
P-003  The kids can't fix this      (false starts, adults busy)
P-004  Drift to the sunroom         (unicorn raft bobbing in no wind)
P-005  The C-130                    (portal triggers)
```

**Word count: ~2,000.** Read aloud as Chapter 1.

### ACT 2 — ARRIVAL (always read, ends in a real choice)

```
P-010  Eight rafts land in the meadow
P-011  The Harbor Keeper            (replaces Tomby)
       - Big, warm, cedar-and-brisket smell
       - Knows the kids without being told their names
       - Tells them: 8 things must be earned across The Old Roar
       - Tells them out loud: "You'll have time for four. Pick well, or pick clever."
       - Hints at family memory without explaining it
P-012  The Strategy Choice          ← FIRST REAL BRANCH
       A. Stay together   → P-100  (4 regions deep, all 8 along)
       B. Split in two    → P-200  (8 regions covered, groups of 4)
       C. Each go alone   → P-300  (8 regions deepest, kids solo)
```

Note on the Harbor Keeper line: "time for four" is the gating mechanic. If they stay together, that means 4 regions and 4 items. If they split, each group of 4 gets 4 regions (8 total). If they each go alone, they each get one — but together that's 8. The arithmetic does the work without tokens on the page.

---

### ACT 3 — THE BRANCHES

#### Strategy A: STAY TOGETHER (4 regions, deep, mutual support)

All 8 kids visit 4 regions together. Reader picks which 4 of the 8 regions to visit. Each region's focal kid is the "lead" but the others contribute. Items earned: 4 base versions.

```
P-100  Pick your 4 regions          (Pool, Stage, Wood, Plains, Lake, Cliff, Court, Meadow)
P-110  Quiet Pool (Madison lead)    → Map (base) + possible Branch ally
P-120  Driftwood Stage (Chayten)    → Voice (base) + possible Otto ally
P-130  Old Speak Wood (Reid)        → Staff (base) + possible OldSpeak ally
P-140  Coulee Plains (Carson)       → Charm (base) + possible BigCoulee ally
P-150  Skip-Stone Lake (Kellen)     → Stone (base) + possible Skim ally
P-160  Painted Cliff (Keira)        → Brush (base) + possible Cliffy ally
P-170  Bright Water Court (Ella)    → Crown (base) + possible FrogHerald ally
P-180  Unicorn Meadow (Aiden)       → Pegasus + possible Hush ally
```

You leave with 4 items, 0–4 allies. SILVER ending likely. Replay to visit the others.

#### Strategy B: SPLIT IN TWO (8 regions, faster, group-of-4 dynamics)

The 8 kids split into two groups of 4. Reader picks the grouping. Each group covers 4 regions in parallel. All 8 items earned but the depth per region is shallower — base versions only, fewer allies.

```
P-200  Pick the split               (4+4 — many groupings; default suggested)
P-210  Group 1 path                 → 4 items
P-250  Group 2 path                 → 4 items
P-290  Meet at the Halfway Hill     (share items, compare scars)
```

You leave with 8 items, 0–3 allies. SILVER or CROWN ending. The "default" grouping suggestion is in-story (Madison organizes it) so kids don't have to think too hard.

#### Strategy C: EACH GOES ALONE (8 regions, deepest, hardest)

Each kid goes to their own region solo. Maximum depth, maximum risk, requires the right path choice in each region to unlock the BEST version of each item. Failure loops back to a Harbor Keeper rescue (no humiliation — the world is gentle even when choices are wrong).

```
P-300  Split into 8 paths
P-310  Madison's solo branch        → Map (base/enhanced/full) + possible ally
P-320  Chayten's solo branch        → Voice (base/enhanced/full) + possible ally
...
P-380  Aiden's solo branch          → Pegasus + possible Hush + possible CanyonSinger flag
```

You leave with 8 items in their best versions, up to 8 allies. CROWN ending likely. Hardest path, most replay reward.

---

### ACT 4 — RETURN (always read, branches by state)

```
P-400  All kids gather              (whoever has Pegasus arrives with her)
P-401  How to get home              ← CHOICE GATED BY STATE
       - If Pegasus earned:    P-410 Unicorn Chain
       - If Lake Sisters allied: P-420 Water Slide
       - If Cliffy allied:      P-430 Basalt Bridge
       - Default:               P-440 Harbor Keeper boat (safe fallback)
```

The return passage is short (~600 words) and pays off whichever allies/items the reader earned. This is where the world feels alive — the choices you made come back to help you.

---

### ACT 5 — SHOWDOWN (state-tracked, conditional beats)

The showdown is **modular**. Each beat fires only if its prereq is met. Missing beats get a soft narrative substitute so the showdown still flows.

```
P-500  Return to the sunroom        (everyone shows what they have)
P-501  Walk to the dock
P-502  Drystone mid-speech

  BEAT 1 — MADISON  (requires: Map)
    P-510  Map reveal: bank fraud exposed
    P-511  (fallback if no Map): Madison improvises — Drystone shaken but not pinned

  BEAT 2 — CHAYTEN  (requires: Voice)
    P-520  Voice + Otto: crowd silenced, listens
    P-521  (fallback): Chayten speaks plainly — works partially

  BEAT 3 — CARSON   (requires: Charm + 5+ kids present)
    P-530  Eight-in-a-line in front of bulldozer
    P-531  (fallback): Three kids stand together — less weight but still real

  BEAT 4 — REID     (requires: Staff)
    P-540  Staff blocks bulldozer
    P-541  (fallback): Reid stands calmly — bulldozer driver hesitates

  ─── CRUMB PUSHBACK (always) ───
    P-550  The bank offer ace
    P-551  ★ The chosen-family pivot ★  (NEW — Drystone tries to peel the families apart)
    P-552  A kid takes it apart (Madison or Carson, depending on state)

  BEAT 5 — KELLEN   (requires: Stone)
    P-560  Stone skip exposes third clipboard
    P-561  (fallback): Kellen tackles Drystone's logic, no skip but still wins

  BEAT 6 — KEIRA    (requires: Brush)
    P-570  Truth Brush — "he's lying"
    P-571  (fallback): Keira sees it without the brush, says it anyway

  BEAT 7 — ELLA     (requires: Crown)
    P-580  Invisible crown moment — "the answer is NO"
    P-581  (fallback): Ella stands up to Drystone without the crown — still wins

  BEAT 8 — AIDEN    (requires: Pegasus)
    P-590  ★ Pegasus visible to Drystone ★ (THE moment — never cut this)
    P-591  (fallback): Aiden looks Drystone in the eye, says it's not right, Drystone breaks anyway
```

The fallbacks are important. The book never punishes the kid for a missing item by making the kid look weak. Instead, the kid wins the beat through *who they are*, just smaller in scale.

---

### ACT 6 — ENDING (one of two, gated by state)

```
P-600  Count items
P-601  CROWN ending   (8 items + all 8 kids played + Pegasus visible)
       → P-610: Dock heals overnight. Magic stays. Pegasus stays.
       → "LOOK AT THIS" coda

P-602  SILVER ending  (fewer than 8 items, OR some kid didn't play)
       → P-620: Drystone loses but dock still partly threatened.
       → Family decides to come back next summer to finish what they started.
       → Kids share secret. Pegasus stays visible in sunroom.
       → "We have to come back" coda — naturally hooks replay
```

Both endings are emotionally complete and safe for the youngest readers. SILVER is the natural floor — it's still a win, it just leaves room to grow. The CROWN ending is the keepsake fantasy that rewards replay.

---

## Crossover rule (locked)

Which allies physically cross from The Old Roar into the real world for the showdown, and who can see them:

- **Pegasus ALWAYS crosses** if Aiden's branch was played. She comes back through the sunroom with Aiden, period. She is the centerpiece. This is non-negotiable.
- **Other allies cross IF the reader earned them on a Path B (enhanced) or Path C (hidden).** Going deep earns the ally's physical presence at the dock.
- **Base path allies appear as echoes** — distant cheers, faint humming, atmospheric flickers. They participated, but they're not on the dock.

**Visibility rule (same for ALL allies, including Pegasus):**
- The **eight kids can see them all.**
- **No adults can see them** — even when Big Coulee the mammoth is standing on the dock, the adults see nothing.
- **EXCEPTION: Mr. Drystone can see them.** Aiden's belief forces the magical world into Drystone's perception. As more allies cross, Drystone sees more — a unicorn, then an otter in a velvet cape, then a beaver in a bow tie, then a wooly mammoth, then a sleeping cliff giant standing where there shouldn't be one. The other adults see nothing. Drystone has to choose, second by second, between admitting magic and pretending to be sane. Either choice destroys him.

What this gives us:
- Showdown stays manageable from the *adult* POV (clean, no spectacle they can't explain)
- Maximum keepsake spectacle from the *kid* POV (everything the reader earned shows up)
- Pegasus is always the centerpiece
- The villain breaks specifically because he's the only adult who can see what the kids see
- Real tactical reason to replay (different allies = different Drystone breakdown each time)
- CROWN ending: Drystone sees a small zoo. SILVER: Drystone sees Pegasus plus a couple of friends.

---

## Hidden replay rewards

These trigger only under specific conditions, and the book never tells the reader they exist. Kids discover them.

| Reward | Trigger | Payoff |
|---|---|---|
| Canyon Singer reveal | Aiden + Chayten branches + specific path | Madison/Kellen mom mythologized as the singer in the canyon — kids who know the real-life story get the easter egg |
| Harbor Keeper = Uncle Bill echo | Reid branch + sit with the Harbor Keeper longer | Reid notices the Keeper laughs like Uncle Bill, smells like cedar smoke |
| Bingo blackout | All 8 items + all 8 allies + all 8 kids played | A note from the Harbor Keeper appears in the coda saying "the bingo card is full — come back next year" |
| Screw Your Neighbor echo | Specific path in Quiet Pool (trade your cookie for the Sisters' pondweed cookie) | The trade mechanic becomes a recurring magical motif |

---

## Estimated total word count

- Act 1 framing: 2,000
- Act 2 arrival: 1,500
- Act 3 branches: ~22,000 (8 regions × ~2,700 each, with multiple paths each)
- Act 4 return: 1,500 (4 variants × ~400)
- Act 5 showdown: 5,000 (modular beats + fallbacks)
- Act 6 endings: 2,500 (3 variants)

**Total: ~35,000 words.** At 3rd-grade pacing with one illustration per passage, roughly 240–280 pages. KDP cost: ~$3.75–$4.25 per B&W paperback author copy.

---

## Next step

Macro structure is locked. Next move is to build out ONE region as the template for the other seven. Madison's Quiet Pool is the natural test case — it's mentioned in every strategy variant and it's where the chosen-family theme first surfaces (Lake Sisters: "tell our older sister hi").

The region template needs:
- A base path (any kid can succeed)
- An enhanced path (yields ally + bonus item version)
- A hidden path (unlocks a hidden flag)
- Failure loops that don't humiliate the kid
- Crossover hooks (what does this region notice from other branches)
- All three "wrapper" variants (Madison + 7 kids together, vs Madison + 3 kids, vs Madison alone)
