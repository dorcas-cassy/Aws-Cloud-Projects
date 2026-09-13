# Project 3: AI Text Narrator (Amazon Polly)

## Overview
A Python script that converts text files into natural-sounding speech (MP3) using Amazon Polly, tested across multiple voices and languages. Extends the AWS-service-integration pattern from Project 2 (Rekognition) to a different service category — speech synthesis and binary audio output handling.

## Problem Statement
Converting written content into audio manually requires specialized tools or manual recording. This script automates that process, producing downloadable MP3 narration — useful for accessibility (screen-reader alternatives), content repurposing (blog-to-podcast), or language learning.

## Architecture
- **Language:** Python 3
- **AWS SDK:** boto3
- **AWS Service:** Amazon Polly (`synthesize_speech` API, neural engine)
- **Region:** eu-central-1 (Frankfurt)
- **Input:** local `.txt` file (path passed as CLI argument)
- **Output:** MP3 file(s), one per voice tested, written to disk

## How It Works
1. Script reads a local text file's contents.
2. For each configured voice, it calls Polly's `synthesize_speech` API with that text.
3. The returned audio stream is written to a uniquely named MP3 file (e.g. `output_article_Joanna.mp3`), so testing multiple text files never overwrites previous results.
4. Errors (missing file, failed API call, empty audio stream) are caught and reported clearly rather than crashing.

See [narrate.py](./narrate.py) for the full source.

## Testing & Results

Three voices were tested against three different text inputs to evaluate real-world behavior, not just the happy path:

| Voice | Language | Test Input | Result |
|---|---|---|---|
| Joanna | English (US, Female) | Standard article text | Natural, clear narration |
| Matthew | English (US, Male) | Standard article text | Natural, clear narration |
| Joanna | English (US, Female) | Edge case: dates, currency, abbreviations, symbols (`$45.99`, `12/25/2024`, `e.g.`, `&`) | Handled smoothly — all symbols and abbreviations were narrated naturally, no robotic or broken pronunciation |
| Vicki | German (Female) | English article text (language mismatch) | Understandable but with a noticeable German accent and mispronunciation of some English words — confirms Polly voices apply their designated language's phonetic rules rather than adapting to mismatched-language input |
| Vicki | German (Female) | Genuine German text | Natural, fluent — performed as expected when matched to its intended language |

## What I Learned
- Polly's neural voices handle punctuation-heavy, symbol-dense text (currency, dates, abbreviations) more gracefully than expected — no manual text pre-processing was needed for natural output.
- Voice selection matters for multilingual content: a language-mismatched voice (e.g. a German voice reading English text) still produces understandable audio, but with real accent artifacts — not a substitute for using the correctly matched voice/language pair.
- Structuring the script to derive output filenames from the input filename (rather than hardcoding names) meant testing multiple inputs never overwrote previous results — a small design choice that mattered a lot in practice during iterative testing.

## Production Considerations
This script works well for one-off or small-batch narration. To productionize it, I'd consider:
- **S3 integration** — save generated MP3s directly to an S3 bucket instead of local disk, for a web-accessible output
- **Lambda + API Gateway** — expose narration as an API endpoint, triggered on-demand or by a file upload event
- **SSML support** — Polly supports Speech Synthesis Markup Language for finer control over pacing, emphasis, and pronunciation, which would improve output quality for professional use cases
- **Cost awareness** — Polly charges per character processed; a production version would need usage limits or monitoring to avoid unexpected costs (a lesson reinforced by an unrelated AWS cost incident earlier in this project series — see Project 2's repo for that story)

## How to Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install boto3
python3 narrate.py <path_to_text_file>
