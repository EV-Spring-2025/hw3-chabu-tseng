from moviepy import VideoFileClip
import argparse

def convert_mp4_to_gif(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_gif(output_path, fps=clip.fps)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert MP4 to GIF")
    parser.add_argument("--input_mp4", required=True, help="Path to the input MP4 file")
    parser.add_argument("--output_gif", required=True, help="Path to the output GIF file")
    args = parser.parse_args()

    convert_mp4_to_gif(args.input_mp4, args.output_gif)
