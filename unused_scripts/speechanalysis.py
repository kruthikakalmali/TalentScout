import librosa

def extract_audio_features(mp3_file_path):
    """Extract audio features like MFCC, pitch, and energy from MP3."""
    y, sr = librosa.load(mp3_file_path, sr=None)  # Load the MP3 file
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    pitch, mag = librosa.core.piptrack(y=y, sr=sr)
    energy = librosa.feature.rms(y=y)

    # Example: Extracting average pitch and energy
    avg_pitch = pitch.mean()  # Could use other techniques for more precise pitch detection
    avg_energy = energy.mean()

    return {
        'mfcc': mfcc,
        'pitch': avg_pitch,
        'energy': avg_energy
    }

# Example usage:
features = extract_audio_features("interview1.mp3")
print(features)