import re
import argparse
import os
import glob
import ffmpeg
import sys
from tqdm import tqdm

# Helpers
def format_timestamp(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def split_into_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)

def main():
    parser = argparse.ArgumentParser(description="Audio to SRT Subtitle Generator")
    parser.add_argument('--test', action='store_true', help='Process only the first 3 minutes of audio')
    parser.add_argument('--backend', choices=['whisper', 'faster-whisper'], default='whisper', help='Backend model to use')
    parser.add_argument('--model', default='large', help='Model size: tiny, base, small, medium, large, large-v3')
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cpu', help='Device to run model on')
    args = parser.parse_args()

    # Get input file
    audio_files = glob.glob('input/*.mp3') + glob.glob('input/*.wav')
    if not audio_files:
        raise FileNotFoundError("No mp3 or wav files found in the 'input' folder.")
    input_file = audio_files[0]
    basename = os.path.splitext(os.path.basename(input_file))[0]
    print(f"Input file: {input_file}")

    # Handle test clip
    if args.test:
        clipped_file = os.path.join('input', f"{basename}_3min_test.wav")
        if not os.path.exists(clipped_file):
            print("Creating 3-minute test clip...")
            try:
                ffmpeg.input(input_file, t=180).output(clipped_file).overwrite_output().run(cmd='C:\\ffmpeg\\bin\\ffmpeg.exe', quiet=True)
            except Exception as e:
                print(f"FFmpeg clipping failed: {e}")
                sys.exit(1)
        transcribe_file = clipped_file
        output_file = os.path.join('output', f"{basename}-subtitles-test.srt")
    else:
        transcribe_file = input_file
        output_file = os.path.join('output', f"{basename}-subtitles.srt")

    # Transcription
    segments = []

    if args.backend == 'whisper':
        print(f"Using OpenAI Whisper ({args.model}) on {args.device}...")
        import whisper
        try:
            model = whisper.load_model(args.model)
        except RuntimeError as e:
            if "checksum does not not match" in str(e):
                print("\nChecksum failed. Clearing cache...")
                cache_dir = os.path.expanduser("~/.cache/whisper")
                if os.path.exists(cache_dir):
                    import shutil
                    shutil.rmtree(cache_dir)
                    print("Cache cleared. Please rerun the script.")
                sys.exit(1)
            else:
                raise
        print(f"Transcribing {transcribe_file}...")
        result = model.transcribe(transcribe_file, verbose=True)
        segments = result["segments"]

    elif args.backend == 'faster-whisper':
        print(f"Using Faster-Whisper ({args.model}) on {args.device}...")
        from faster_whisper import WhisperModel
        model = WhisperModel(args.model, device=args.device)
        segments_generator, info = model.transcribe(transcribe_file, beam_size=5)

        print(f"Audio duration: {info.duration:.2f}s | Language: {info.language}")
        progress_bar = tqdm(total=info.duration, desc="Transcribing", unit="sec", dynamic_ncols=True)

        last_end = 0.0
        for segment in segments_generator:
            segments.append(segment)
            progress_bar.update(segment.end - last_end)
            last_end = segment.end

        progress_bar.close()

    else:
        print("Unknown backend specified.")
        sys.exit(1)

    # Write SRT file
    print(f"Saving subtitles to {output_file}...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as srt_file:
        index = 1
        for segment in segments:
            if args.backend == 'whisper':
                start_time, end_time, text = segment["start"], segment["end"], segment["text"]
            else:  # faster-whisper object
                start_time, end_time, text = segment.start, segment.end, segment.text

            sentences = split_into_sentences(text)
            for sentence in sentences:
                if not sentence.strip():
                    continue

                duration = (end_time - start_time) / len(sentences)
                segment_end = start_time + duration

                srt_file.write(f"{index}\n")
                srt_file.write(f"{format_timestamp(start_time)} --> {format_timestamp(segment_end)}\n")

                wrapped = re.findall(r'.{1,80}(?:\s+|$)', sentence.strip())
                wrapped = wrapped[:2]
                srt_file.write('\n'.join(wrapped).strip() + "\n\n")

                start_time = segment_end
                index += 1

    print(f"✅ Done. Subtitles saved to {output_file}")

if __name__ == "__main__":
    main()
