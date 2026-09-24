# 01 · Project Brief

## The problem

Animation feedback from Japanese clients arrives as Japanese videos and meetings. Only one person in the studio understands Japanese, so every piece of feedback waits for them. This creates a bottleneck in production.

## The goal

An internal tool that:

1. **Recorded videos (main priority):** takes a Japanese feedback video and produces an accurate English translation with the context intact, as subtitles, a timecoded transcript, a structured retake list, and optionally a dubbed video.
2. **Live meetings (later):** translates Japanese meeting audio to English in near real time, and our English speech to Japanese.
3. **Any language:** auto-detects the spoken language and translates to a chosen language. Japanese → English is the main case.

## Who uses it

Fahim and the studio team. Internal use only.

## Priorities (in order)

1. **Translation quality and context.** The translator must understand what the feedback is about (cut, character, animation terms), because the same word means different things in different contexts. Example: タメ in animation means hold/anticipation, not "for the sake of."
2. **Open-source and local.** Runs fully on the studio PC, no paid services.
3. **Improves over time.** Corrections from the Japanese-speaking colleague are saved and used to make the tool better.
4. **Speed is not a priority.** Delay is acceptable for recorded videos. For live meetings, a few seconds is fine.

## Constraints

- **Hardware:** one PC, RTX 5070 (12 GB VRAM), 64 GB RAM, Windows.
- **Confidential:** client videos and feedback must not leave the studio.
- **Licenses:** tools and models must allow commercial (business) use.
- **Solo developer:** Fahim builds everything, step by step.

## What success looks like

- The Japanese-speaking colleague reviews the tool's output instead of translating from scratch, and mostly finds only small fixes.
- Artists get clear retake notes per cut without waiting.
- Quality is measured against a gold set (clips with correct translations), not guessed.

## Out of scope for now

- Dubbing into Bangla (no mature open-source Bangla voice yet). Bangla subtitles are fine.
- Paid APIs.
