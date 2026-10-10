# Caddie round handshake — 2026-10-10

Status: product requirement proposed for incorporation into DEC-017 and the New Chat Starter.

## Purpose

The pre-round start should reconnect the golfer with their active Caddie experiment. This makes the recommendation → commitment → on-course execution → measured result → improved recommendation loop usable in real play, rather than leaving the experiment buried in Stats.

## Pre-round handshake

At the start of a round, keep the check-in brief and contextual:

1. Ask when the golfer last played.
2. Ask whether they have practised since then.
3. If an active Caddie experiment exists, remind them what they agreed to test and when it applies. Example: “Last time we agreed to try one club more on suitable approach shots where you tend to miss short.”
4. Confirm the reminder without making the golfer feel judged or forcing an experiment they no longer want to run.

Do not repeat questions unnecessarily if the information is already known and current. Allow the golfer to skip or change the experiment.

## During and after the round

- Surface the active experiment only when a relevant shot situation occurs.
- Record shot context and outcome so the result can be reviewed.
- After the round, compare like-for-like shots and decide whether to retain, revise or discard the experiment.

## Evidence and safety guardrails

- Show the relevant club/distance sample and sample size.
- Never infer a club change from an overall miss rate alone.
- Account for material context where available, including distance, lie, wind and elevation.
- Treat small samples as provisional, not proof.
- Keep the golfer in control; prompts should be relevant and unobtrusive.

## Source-of-truth follow-up

Incorporate this handshake into DEC-017 in `docs/project/DECISION-LOG.md` and the Caddie recommendation loop section of `docs/project/NEW-CHAT-STARTER.md` when the normal file-update route is available.

Related tracking issue: https://github.com/mccrystal111-design/uido-live-test/issues/11

No GitHub Actions should be manually dispatched for this documentation change.
