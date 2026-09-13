import boto3
import sys
import os

def synthesize_speech(text, voice_id, output_filename, output_engine="neural"):
    """
    Converts text to speech using Amazon Polly and saves it as an MP3 file.
    """
    polly = boto3.client('polly', region_name='eu-central-1')  # Frankfurt region

    try:
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine=output_engine
        )
    except Exception as e:
        print(f"Error calling Polly for voice '{voice_id}': {e}")
        return False

    if "AudioStream" in response:
        with open(output_filename, 'wb') as file:
            file.write(response['AudioStream'].read())
        print(f"✓ Saved: {output_filename} (voice: {voice_id})")
        return True
    else:
        print(f"Error: no audio stream returned for voice '{voice_id}'")
        return False


def read_text_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: file '{file_path}' not found")
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 narrate.py <path_to_text_file>")
        sys.exit(1)

    text_file_path = sys.argv[1]
    text_content = read_text_file(text_file_path)
    base_name = os.path.splitext(os.path.basename(text_file_path))[0]  # e.g. "article" or "edge_case"

    voices_to_test = [
        {"id": "Joanna", "label": "English (US, Female)"},
        {"id": "Matthew", "label": "English (US, Male)"},
        {"id": "Vicki", "label": "German (Female)"},
    ]

    print(f"Narrating text from '{text_file_path}' using {len(voices_to_test)} voices...\n")

    for voice in voices_to_test:
        output_file = f"output_{base_name}_{voice['id']}.mp3"
        synthesize_speech(text_content, voice['id'], output_file)
