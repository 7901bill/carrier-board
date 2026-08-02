# Journal — Wireless Watchdog: CM5 Carrier Board

Running append-only log of session-by-session notes. Raw record of what was
discussed, not the canonical spec — CLAUDE.md is the authoritative current
state; entries here get reconciled into it same-session, then left alone as
history. Replaces the old per-session `Session-Log-*.md` file pattern
(retired 2026-07-30) and the old `documentation.md`/`status.md` split
(retired same day, both were pure re-narrations of CLAUDE.md with no new
information).

---

## 2026-07-30 — Power tree correction + doc consolidation

Reconciled into CLAUDE.md same-day. See CLAUDE.md's "Session log" recap
(Session 3) for the summary — corrected power budget (~20-23W → ~13W),
PD sink CH224K → CH224A, buck TPS54560 → MP2329GG-Z, and a since-corrected
detour where the Hailo-8L M.2 rail was briefly (and wrongly) called an LDO
candidate before re-checking the datasheet confirmed the 6.6W/2A max figure
already locked in CLAUDE.md was right — buck POL requirement stands.

Also merged `documentation.md` and `status.md` into CLAUDE.md (no new info,
both deleted) and retired the dated session-log pattern in favor of this
file.
