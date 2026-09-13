import boto3
import sys
import json

def detect_image_labels(image_path, max_labels=10, min_confidence=70):
    """
    Detects labels (objects, scenes, concepts) in a local image
    using Amazon Rekognition.
    """
    rekognition = boto3.client('rekognition', region_name='eu-central-1')  # Frankfurt region — closest to Germany

    try:
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
    except FileNotFoundError:
        print(f"Error: could not find image file at '{image_path}'")
        sys.exit(1)

    try:
        response = rekognition.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=max_labels,
            MinConfidence=min_confidence
        )
    except Exception as e:
        print(f"Error calling Rekognition: {e}")
        sys.exit(1)

    return response['Labels']


def print_labels(labels):
    print(f"\nDetected {len(labels)} labels:\n")
    for label in labels:
        print(f"  {label['Name']:<20} confidence: {label['Confidence']:.2f}%")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_labels.py <path_to_image>")
        sys.exit(1)

    image_path = sys.argv[1]
    labels = detect_image_labels(image_path)
    print_labels(labels)
