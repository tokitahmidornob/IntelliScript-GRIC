import os

# Failsafe Import: Handles both new (v2.x) and legacy (v1.x) MoviePy versions
try:
    from moviepy import VideoFileClip, concatenate_videoclips
except ImportError:
    from moviepy.editor import VideoFileClip, concatenate_videoclips

def engineer_demo(input_path, output_path):
    print("Watson: Initializing the video extraction protocol...")
    
    if not os.path.exists(input_path):
        print(f"Error: Cannot find '{input_path}'. Please ensure the file name is exact.")
        return

    # Load the master recording
    video = VideoFileClip(input_path)
    
    # The blueprint of our cuts (in seconds)
    cuts = [
        (25, 43),    # Setup
        (116, 148),  # AI Deprescribing
        (149, 197),  # Sentinel Override
        (213, 225)   # Crypto Resolution
    ]
    
    clips = []
    for i, (start, end) in enumerate(cuts, 1):
        print(f"Watson: Extracting Segment {i} ({start}s to {end}s)...")
        # Handle MoviePy v2.x (subclipped) vs v1.x (subclip) API changes
        if hasattr(video, "subclipped"):
            clip = video.subclipped(start, end)
        else:
            clip = video.subclip(start, end)
        clips.append(clip)
    
    print("Watson: Splicing the master sequence together...")
    final_video = concatenate_videoclips(clips)
    
    print(f"Watson: Rendering the final payload to '{output_path}'. This may take a moment...")
    
    # Rendering with standard codec for maximum compatibility
    final_video.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac",
        fps=video.fps,
        preset="fast"
    )
    
    # Free up system memory
    video.close()
    for clip in clips:
        clip.close()
        
    print("Watson: Operation complete. The GRIC Demo is ready for submission.")

if __name__ == "__main__":
    # Ensure this matches your exact video file name
    INPUT_FILE = "Demo.mp4"
    OUTPUT_FILE = "IntelliScript_GRIC_Demo.mp4"
    
    engineer_demo(INPUT_FILE, OUTPUT_FILE)