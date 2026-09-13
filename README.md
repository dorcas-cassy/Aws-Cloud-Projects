# Project 2: AI Image Labels Generator (Amazon Rekognition)

## Overview
A Python script that uses Amazon Rekognition to automatically detect objects, scenes, and concepts in a local image, returning labels with confidence scores. Unlike Project 1 (built with the no-code PartyRock tool), this project integrates directly with an AWS service via its SDK — demonstrating hands-on API and error-handling skills, not just prompt design.

## Problem Statement
Manually tagging and categorizing images at scale is slow and inconsistent. This tool automates that process using computer vision, returning structured, confidence-scored labels — useful for content moderation, digital asset management, or generating alt text for accessibility.

## Architecture
- **Language:** Python 3
- **AWS SDK:** boto3
- **AWS Service:** Amazon Rekognition (`detect_labels` API)
- **Region:** eu-central-1 (Frankfurt — closest to my location in Germany)
- **Authentication:** AWS CLI credentials (IAM user), read via boto3's default credential chain

## How It Works
1. The script reads a local image file as raw bytes.
2. It calls Rekognition's `detect_labels` API, passing the image bytes directly (no S3 upload required for this use case).
3. Rekognition returns up to 10 labels (configurable), each with a confidence score.
4. Results are filtered to a minimum 70% confidence threshold to reduce noise, then printed in a readable format.

### Key code decisions
- **Error handling for two failure modes:** a missing/invalid image file (`FileNotFoundError`) and an AWS API failure (e.g. bad credentials, region misconfiguration, network issue) — both fail with a clear message instead of a raw stack trace.
- **`MinConfidence=70`** — filters out low-confidence guesses so results stay meaningful.
- **Configurable parameters** (`max_labels`, `min_confidence`) — the function isn't hardcoded to one use case.

See [detect_labels.py](./detect_labels.py) for the full source.

## Testing & Results

| Test Case | Image Description | Result |
|---|---|---|
| Simple/clean image | A flower held in hand | Correctly identified Flower, Plant, Rose (99.89%), plus contextual labels like Cosmetics and Perfume, suggesting the model inferred a styled/product-photo context |
| Complex image | [describe your test2 image] | Detected Machine, Wheel, Head among other labels — [add your observation about accuracy here] |
| Portrait/edge case | A posed portrait photo | Correctly detected Face, Person, Portrait, Photography at 99.99% confidence; also returned Book/Publication at 99.98%, an unexpected label worth noting as a model quirk |

Screenshots of each test run are in [/screenshots](./screenshots).

## What I Learned
- Calling Rekognition directly via boto3 (vs. a no-code tool) requires handling your own error cases — credential failures, missing files, and malformed responses all need explicit handling for the tool to be trustworthy.
- Confidence thresholds matter: without `MinConfidence` filtering, output gets noisy with low-value guesses.
- Rekognition sometimes returns labels that reveal how the model is reasoning about an image beyond the obvious subject (e.g. inferring "Cosmetics" from context around a flower, or "Publication" from a portrait) — worth noting when evaluating a model's real-world reliability.

## Production Considerations
This script works well for local, one-off image analysis. To productionize it, I'd consider:
- **S3 integration** — for images already stored in S3, Rekognition can reference the object directly instead of reading local bytes, avoiding unnecessary data transfer
- **Lambda + API Gateway** — wrap this logic in a Lambda function triggered by an S3 upload event or an API call, for a fully serverless pipeline
- **Batch processing** — for large image sets, use asynchronous Rekognition operations rather than synchronous calls
- **IAM least-privilege** — scope the IAM role to only `rekognition:DetectLabels`, rather than using a broader admin credential (which I used here for quick local testing)

## How to Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install boto3
python3 detect_labels.py <path_to_image>
```
Requires AWS CLI credentials configured locally (`aws configure`) with Rekognition permissions.
