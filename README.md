# vGOAL Interpreter — Test Version (offline / SAT_V2)

**Offline test version** of the vGOAL agent-reasoning interpreter. It reads each AMR's
state from **pre-recorded sensor-trace files** (`MG_*.txt` / `STORY_*.txt`), so it can
run and reproduce multi-agent decision scenarios **without any real robot**.

> The real-robot version lives in `../vGOAL_Interpreter_SAT_Integration_02(Refinment)/`.
> The two `Interpreter.py` files are **logically identical except for the input source**
> (this one reads files; the real-robot one connects to the robots).

## Dependencies
- `python3.9` (the prebuilt stormpy/pysat wheels target cpython-3.9)
- `pysat` (`from pysat.formula import CNF` / `from pysat.solvers import Solver`)
```bash
/opt/homebrew/bin/python3.9 -c "import pysat; print('ok')"
```

## Directory structure

**Interpreter core**
- `Interpreter.py` — the interpreter itself: the reasoning cycle, least-fixpoint
  derivation, action/event/communication analysis, and a best-effort SAT
  cross-check (`_sat_verify`). Optional `sensor_files={agent: file}` makes each
  agent read its own trace file (story mode).
- `Interpreter_V2.py` / `Interpreter_Improve_back.py` — alternative/legacy variants
  (`AMR_V2.py` uses the former).

**Specs + entry points** (each does `import Interpreter` and calls `DG.interpreter(...)`)
- `New_01.py` / `New_02.py` — minimal nullary-holding 3+1 agent example that runs to
  completion. `python3.9 New_01.py`, then enter `1`.
- `AMR_Spec.py` — AMR delivery spec (`holding(w)`, P1–P8 topology). Prompts for input
  `1/2/3` to pick a test case; reads the shared `MG_0*.txt` files.
- `AMR_Spec2.py` / `AMR_Spec3.py` — 3-agent variants of the above.
- `AMR_Story.py` — **the three-agent story** (recommended demo): nullary holding,
  input `1/2/3` = error-free / non-fatal error / fatal error, using dedicated
  `STORY_*.txt` traces; all three cases run to `No active goals!`.
  See `THREE_AGENT_STORY_NOTES.md`.
- `AMR_Story_A1.py` — single-agent story test.
- `AMR_V2.py` / `AMR_back.py` — other legacy specs.

**Sensor traces** (one `{'Position':..., 'Docked':..., 'Holding':..., 'Battery':..., 'Error':...}` per line)
- `MG_0*.txt` — **shared** traces, read by `New_01/AMR_Spec*` via a built-in `T` mapping.
  ⚠️ **Do not overwrite them** — several entry points depend on them.
- `STORY_A1.txt` / `STORY_A2.txt` / `STORY_A3.txt` / `STORY_A1_ef.txt` /
  `STORY_A3_ef.txt` / `STORY_A3_nf.txt` — used only by `AMR_Story.py` (selected per case).
- `MG_original_backup/` — pristine backup of the `MG_*.txt` files.

**Other**
- `THREE_AGENT_STORY_NOTES.md` — detailed notes on the three-agent story (mechanisms,
  the three cases, a known spec-level caveat).
- `Interpreter.py.preport.bak` / `Interpreter.py.prebugfix.bak` — rollback backups from
  before the interpreter changes.
- `Record*.txt` — run timing output.

## How to run
Use `python3.9`; pipe the interactive input:
```bash
# Three-agent story (recommended) — 1=error-free, 2=non-fatal error, 3=fatal error (crash + goal redistribution)
echo 3 | /opt/homebrew/bin/python3.9 AMR_Story.py

# Minimal example (runs to completion)
echo 1 | /opt/homebrew/bin/python3.9 New_01.py

# AMR delivery spec (reads the shared MG files)
echo 1 | /opt/homebrew/bin/python3.9 AMR_Spec.py
```
Output is, per reasoning cycle (`CycleN`), each agent's decision (e.g. `A1 pickup(1)`,
`A2 move3(4,2)`), any error/crash/redistribution events, ending at `No active goals!`.

## Notes
- Fully offline: no robot connection; all state comes from the trace files.
- The SAT check in `Interpreter.py` is a best-effort cross-check (`_sat_verify` wraps it
  in try/except, so an encoding failure never aborts the run); story mode
  (`sensor_files`) skips it for speed.
