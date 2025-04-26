# import subprocess

# def extract_audio_from_webm(webm_file, output_file):
#     command = [
#         "ffmpeg",
#         "-i", webm_file,  # Input WebM file
#         "-vn",             # No video
#         "-acodec", "pcm_s16le",  # Audio codec
#         "-ar", "44100",          # Sampling rate
#         "-ac", "2",              # Number of audio channels (stereo)
#         output_file            # Output file name
#     ]
#     subprocess.run(command)

# # Example usage:
# extract_audio_from_webm("videoplayback.webm", "output_audio.wav")
