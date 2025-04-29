import os
import tempfile
from pydub import AudioSegment
from imageio_ffmpeg import get_ffmpeg_exe


async def convert_webm_to_mp3(file_data: bytes) -> bytes:
    """Converts WebM audio bytes to MP3 bytes using a bundled FFmpeg binary."""
    # write incoming bytes to a temp .webm file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_in:
        temp_in.write(file_data)
        temp_in.flush()
        input_path = temp_in.name

    output_path = input_path.replace(".webm", ".mp3")

    try:
        # point pydub at the bundled ffmpeg binary
        AudioSegment.converter = get_ffmpeg_exe()

        # load WebM and export as MP3
        audio = AudioSegment.from_file(input_path, format="webm")
        audio.export(output_path, format="mp3")

        # read back the mp3 bytes
        with open(output_path, "rb") as f:
            return f.read()

    finally:
        # clean up
        os.unlink(input_path)
        if os.path.exists(output_path):
            os.unlink(output_path)