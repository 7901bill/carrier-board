# Documentation workflow for Codex sessions

## Purpose

This project uses two shared Markdown files as its durable memory across Codex sessions. The goal is to preserve decisions and reversals as they happen, without separate handoff agents, conflict reports, or a complicated GitHub workflow.

## The two source-of-truth files

- `Documentation/documentation.md` contains the **current approved design**: selected parts, architecture, implementation plan, and current open items.
- `Documentation/Journal.md` is the **append-only history**: research notes, discussions, decisions, corrections, and reversals, recorded in date order.

`documentation.md` answers: "What are we doing now?"
`Journal.md` answers: "What did we learn, decide, or change, and why?"

## Normal sequential workflow

Agents work one at a time against the same GitHub branch. At the beginning of each session, the agent pulls the latest changes and reads both documentation files. That makes the previous agent's recorded conclusions available before new work begins.

```text
Agent starts
  -> pull latest changes
  -> read documentation.md + recent Journal.md entries
  -> research / discuss / make progress with Bill
  -> record material decisions as they occur in Journal.md
  -> compare final outcome against documentation.md
  -> Bill resolves any conflict
  -> update documentation.md + Journal.md
  -> commit and push
  -> next agent starts from those same files
```

No separate GitHub repository, handoff folder, reconciliation agent, or Decision Register is required while agents are working sequentially.

## Rolling Journal checkpoints

During a session, append a concise Journal entry immediately after any material event:

- Bill explicitly makes or reverses a design decision.
- A component, topology, interface, requirement, or scope changes.
- Research disproves an earlier assumption.
- Work moves to a new hardware subsystem with conclusions worth preserving.

Each checkpoint should include the decision or finding, its status (`Proposed`, `Confirmed`, or `Superseded`), the reason or evidence, and the older choice it replaces when applicable.

Do not wait until the end of a long conversation to record a meaningful decision. This makes the Journal a useful summary even if a session is later interrupted.

## Handling disagreements or reversals

An agent must never silently overwrite an existing design decision.

If a session reaches a conclusion that conflicts with `documentation.md` or a recent Journal decision, the agent must show Bill:

1. The current documented choice.
2. The new proposed choice.
3. Evidence and tradeoffs for both.
4. The exact choice Bill needs to make.

Only after Bill explicitly confirms the outcome may the agent change the current design in `documentation.md`. It must append a Journal entry stating that the older decision is superseded; history is never deleted.

## End-of-session checklist

Before ending a normal session, the agent must:

1. Review the decisions, corrections, and open questions from the current conversation.
2. Read `Documentation/documentation.md` and recent relevant entries in `Documentation/Journal.md`.
3. Check whether the session's conclusion changes the current design.
4. Ask Bill to resolve any unresolved conflict rather than deciding on Bill's behalf.
5. After Bill confirms, update `documentation.md` and append the dated Journal entry.
6. Commit and push the documentation changes.
7. State clearly if no documentation update was needed.

## Reusable agent instruction

```text
Before starting, pull the latest branch and read Documentation/documentation.md and the recent entries in Documentation/Journal.md.

During this session, immediately append a concise dated Journal checkpoint when Bill confirms or reverses a material design decision, or when research changes an important assumption. Mark it Proposed, Confirmed, or Superseded and include the evidence and any decision it replaces.

Before ending, compare this session's final conclusions with the current documentation. If there is a conflict, show me the old decision, new proposal, evidence, tradeoffs, and exact choice needed. Do not choose for me.

After I explicitly confirm a choice, update documentation.md, append the final dated Journal entry, commit, and push. If no current decision changed, say that no documentation update was needed.
```
