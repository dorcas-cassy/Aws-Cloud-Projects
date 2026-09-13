# Project 1: AI Daily Task Scheduler (Amazon PartyRock)

## Overview
A GenAI-powered daily scheduler built with Amazon PartyRock (a no-code app builder on Amazon Bedrock foundation models). Given a list of tasks and personal constraints, it generates a realistic, time-blocked daily schedule — prioritizing high-focus work in the morning and respecting fixed commitments like meetings.

## Problem Statement
Knowledge workers waste time manually planning their day. This app takes a natural-language task list and constraints, then uses generative AI to produce a structured schedule that accounts for task complexity, priority, and fixed time commitments.

## Architecture
- **Platform:** Amazon PartyRock (built on Amazon Bedrock foundation models)
- **Widgets used:**
  - `Task list` (Text Input) — user's raw task list
  - `Constraints` (Text Input) — time constraints, fixed meetings, preferences
  - `Schedule Generator` (AI Output) — chains both inputs into a prompt that generates the schedule
- **Variable chaining:** The AI Output widget references `{{Task list}}` and `{{Constraints}}` directly in its prompt, so the schedule regenerates dynamically as inputs change.

## Prompt Design
See [prompts.md](./prompts.md) for the full prompt text and iteration notes.

Key design decisions:
- Included an explicit example output format (a sample table row) to guide consistent formatting
- Explicitly instructed the model to place high-focus tasks in the morning
- Iterated based on PartyRock's built-in prompt quality evaluator, which suggested clarifying how constraints would be provided and adding an output example — both improved consistency

## Testing & Results

| Test Case | Input Summary | Result |
|---|---|---|
| Light day | 5 simple tasks, no fixed constraints | Clean, well-reasoned schedule with sensible time estimates |
| Heavy day | 11 mixed tasks + 2 fixed-time meetings | Correctly anchored both fixed meetings at their exact times; added unsolicited coaching notes on batching errands and protecting focus time |
| Edge case (conflict) | A task requested at 9am directly conflicted with a "no calls before 10am" constraint | Model explicitly flagged the conflict and rescheduled the task, rather than silently ignoring the constraint or hallucinating a resolution |

Screenshots of each test are in [/screenshots](./screenshots).

## What I Learned
- PartyRock is a strong prototyping layer over Bedrock — it validates a prompt-chaining concept fast, without writing any backend code.
- Explicit output-format examples in a prompt materially improve consistency, more than just describing the desired format in words.
- The model's conflict-flagging behavior (rather than silent failure) is a good example of why testing edge cases matters — you can't assume happy-path behavior generalizes.

## Production Considerations
PartyRock apps aren't meant for production use. If I were to productionize this, I'd rebuild it using:  
- **Amazon Bedrock APIs** directly (instead of PartyRock's no-code layer), for programmatic control
- **AWS Lambda** to handle the prompt orchestration logic
- **API Gateway** to expose it as a callable endpoint for a real front-end
- Persistent storage (e.g. DynamoDB) to save user schedules across sessions

## Live App
[https://partyrock.aws/u/cassylilac/HEOiWphWe/Daily-Task-Scheduler] 
