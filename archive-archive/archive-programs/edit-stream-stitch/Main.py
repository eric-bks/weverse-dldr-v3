import subprocess

def main():
    # User input
    video_segments = input("Enter the paths of the video segments separated by commas: ").split(",")
    transition_text = input("Enter the transition text (default: 'Her stream crashed here for a moment...'): ") or "Her stream crashed here for a moment..."
    output_file = input("Enter the output file name (default: 'output.mp4'): ") or "output.mp4"

    # Create transition
    transition_script = "create_transition.sh"
    transition_file = "transition.mp4"
    subprocess.run([transition_script, transition_text, transition_file])

    # Stitch videos
    subprocess.run(["stitch_videos.sh"] + video_segments + [transition_file, output_file])

if __name__ == "__main__":
    main()
