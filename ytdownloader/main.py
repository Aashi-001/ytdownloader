import argparse
import subprocess
import sys
import os
import shutil

def check_dependencies():
    if shutil.which("yt-dlp") is None:
        print("Error: yt-dlp not installed. Install it via 'pip install yt-dlp'.")
        sys.exit(1)
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg not installed. Install it via package manager.")
        sys.exit(1)

# def download_video(url, output_path):
#     subprocess.run([
#         "yt-dlp",
#         "-f", "bestvideo+bestaudio/best",
#         "-o", output_path,
#         url
#     ], check=True)
def download_video(url, output_path):
    subprocess.run([
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mkv",    # <------ FORCE MKV
        "-o", output_path,
        url
    ], check=True)


def trim_video(input_path, start_time, end_time, output_path):
    subprocess.run([
        "ffmpeg",
        "-i", input_path,
        "-ss", start_time,
        "-to", end_time,
        "-c", "copy",
        output_path
    ], check=True)

def convert_to_mp4(input_mkv_path, final_mp4_path):
    # Step 3: Re-encode or remux to MP4
    subprocess.run([
        "ffmpeg",
        "-i", input_mkv_path,
        "-c:v", "copy",
        "-c:a", "aac",   # Convert audio if needed
        "-strict", "experimental",
        final_mp4_path
    ], check=True)

def main():
    parser = argparse.ArgumentParser(description="Download and trim YouTube videos easily.")
    parser.add_argument('--url', type=str, required=True, help='YouTube video URL')
    parser.add_argument('--start-time', type=str, required=True, help='Start time (HH:MM:SS)')
    parser.add_argument('--end-time', type=str, required=True, help='End time (HH:MM:SS)')
    parser.add_argument('--dest', type=str, default='.', help='Destination folder')

    args = parser.parse_args()

    check_dependencies()

    os.makedirs(args.dest, exist_ok=True)

    full_video_path = os.path.join(args.dest, "full_video.mkv")
    trimmed_mkv_path = os.path.join(args.dest, "trimmed_video.mkv")
    final_mp4_path = os.path.join(args.dest, "final_output.mp4")

    print("\n▶️ Downloading full video...")
    download_video(args.url, full_video_path)

    print("\n✂️ Trimming the video...")
    trim_video(full_video_path, args.start_time, args.end_time, trimmed_mkv_path)

    print("\n🎥 Converting trimmed video to MP4...")
    convert_to_mp4(trimmed_mkv_path, final_mp4_path)

    print(f"\n✅ Saved final trimmed video at: {final_mp4_path}")


if __name__ == "__main__":
    main()
