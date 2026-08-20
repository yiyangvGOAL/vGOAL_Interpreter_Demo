# Three-Agent Story (offline reproduction) — complete

Offline reproduction (reads MG trace files, no real robot) of the README's three-agent
story, **running end-to-end to `No active goals!`**.

## How to run
```bash
/opt/homebrew/bin/python3.9 AMR_Story.py    # prompts for 1 / 2 / 3, ~6s each
```
- `AMR_Story.py`: nullary-holding spec (P1–P8 topology), `Agents=[A1,A2,A3,C]`, error
  grading E1/E2/E3→nonfatal, E4→fatal (matches the README). Reads input 1/2/3 and selects
  a different STORY trace set.
- Dedicated sensor traces (one set per case):
  - shared: `STORY_A2.txt`
  - case 1/2: `STORY_A1_ef.txt` (A1 delivers object 1 only);
    `STORY_A3_ef.txt` (A3 delivers object 3) / `STORY_A3_nf.txt` (A3 hits E1)
  - case 3: `STORY_A1.txt` (A1 does two deliveries); `STORY_A3.txt` (A3 hits E4, crashes)
  - ⚠️ **Do not reuse the shared `MG_0*.txt`** — New_01/AMR_Spec* depend on them, and
    overwriting silently breaks those demos. The story uses
    `interpreter(..., sensor_files={name: file})` to read its own files instead.
    Pristine MG backup is in `MG_original_backup/`.

## The three test cases (all reach `No active goals!`, ~6s, no crash)

**Input 1 — error-free**: all three agents deliver their own object.
```
A1 move3(6,3)→pickup(1)→move3(3,2)→dropoff(1,2)→move4(2,5)   # object 1
A2 pickup(2)→move3(4,2)→dropoff(2,2)→move4(2,5)             # object 2
A3 move3(7,3)→pickup(3)→move3(3,2)→dropoff(3,2)→move4(2,5)   # object 3
No active goals!
```

**Input 2 — non-fatal error**: A3 hits E1 (docking error), abandons its current delivery
and retreats to the waiting point.
```
A1 / A2 deliver object 1 / object 2 normally
A3 move3(7,3)  →  "Drop the current goal due to a nonfatal error"  →  A3 move4(3,5)   # retreats to P5
No active goals!
```

**Input 3 — fatal error**: A3 hits E4, crashes; its goal is redistributed to A1, which then
completes a second delivery.
```
A3 crashed!  →  A1 received new goals
A2 delivers object 2; A1 delivers object 1; A1 move2(5,3)→pickup(3)→dropoff(3,2)   # A1 also delivers the redistributed object 3
No active goals!
```

Counts (input 3): crash×1, redistribution×1, pickup(1/2/3) ×1 each, dropoff(1/2/3) ×1 each,
No active goals×1.
Regression: New_01=12 decisions and all 7 oracles pass (the `interpreter` changes are gated
on the `sensor_files`/reactive path; the error grading / input selection live only in
`AMR_Story.py`, so none of them affect those demos).
(Minor: in input 2 the "Drop the current goal" line prints a few times — the interpreter
prints it each cycle while `goal_change` persists; correct, just verbose.)

## Key mechanisms that make it close
1. **Reactive sensor** (only in `sensor_files` mode): each agent advances through its own
   trace only while still executing a commanded action, and holds once its sensed state
   reaches the target — mirroring the real robot's causality. Fixes the impedance mismatch
   between fixed MG frames and the reactive decision loop.
2. **`sensor_files` parameter** + `info_parse_file()`: the story uses its own trace files
   and never touches the shared MG files.
3. **carried-object world-model tracking**: on pickup/dropoff it adds/removes `on(w,pos)`, so
   `delivered` is derived correctly and agents stop re-delivering in a loop.
4. **"settle → release" hook (Direction 1, main loop, reactive only)**: when an agent has no
   goals left (DONE) it releases the `reserved(agent,loc)` entries it still holds in the dummy
   manager C (→ `idle(loc)`). Otherwise a settled agent never moves, and release is
   movement-triggered, so it would hold the spot forever and deadlock the others.
5. **`at(5) implies located(charging)`**: lets an agent finish charging in one move at P5 and
   become DONE quickly. Combined with (4) this frees the P5 waypoint: A2 finishes → releases
   P5 → A1 can charge there and complete its two deliveries → termination.
6. Quantifier fix (a body-only variable must use `exists`), over-generation fix (`A(w)` tied
   to `a-goal-on(w,2)+on(w,pos)`), and SAT robustness (`_sat_verify` try/except; story mode
   skips SAT via `_SKIP_SAT` for speed).

## Known spec-level caveat (worked around here, worth noting)
The built-in charge-spot assignment rule is broken for pre-reserved spots:
`sent!(x) idle(_) and idle(6) and reserved(x,6) implies send:(x) assigned(6)` requires both
`idle(6)` and `reserved(x,6)`, which are mutually exclusive (a spot is either idle or
reserved). So an agent can never get `assigned` for a directly pre-reserved charge spot
(P6/7/8) and charging there never completes. The story sidesteps this with
`at(5)→charging` (one-step charge at P5). If you later want to use the real P6/7/8 charge
spots, that rule needs fixing.

## Deliverables
`AMR_Story.py`, `STORY_A1.txt`, `STORY_A2.txt`, `STORY_A3.txt`, `STORY_A1_ef.txt`,
`STORY_A3_ef.txt`, `STORY_A3_nf.txt`, and this file.
All related `interpreter()` changes are gated on `sensor_files`/reactive, are
backward-compatible, and do not affect any existing demo.
