# Prompt Design & Iteration

## Final Prompt (Schedule Generator widget)

You are a productivity coach. Given this task list: {{Task list}} and these constraints: {{Constraints}} (such as meeting times or task deadlines), generate a realistic time-blocked schedule from 8am to 6pm. Estimate duration per task based on complexity. Place high-focus tasks in the morning. Include short breaks. Output as a table with columns: Time, Task, Notes. For example: "8:00-9:00 | Finish quarterly report | High focus, no interruptions" and "9:00-9:15 | Break | Coffee and stretch."

## Iteration Notes

**v1 (initial draft):**
"You are a productivity coach. Given this task list: {{Task list}} and these constraints: {{Constraints}}, generate a realistic time-blocked schedule from 8am to 6pm. Estimate duration per task based on complexity. Place high-focus tasks in the morning. Include short breaks. Output as a table with columns: Time, Task, Notes."

PartyRock's built-in prompt evaluator rated this "solid" but suggested two improvements:
1. Clarify how constraints input would be provided (e.g. meeting times, deadlines)
2. Add an example showing the desired table output format

**v2 (final, above):** Incorporated both suggestions. Result was more consistent formatting across test runs and better handling of constraint edge cases (see main README's Testing & Results section).
