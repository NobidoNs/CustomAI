from pydub import AudioSegment

def change_pitch(audio_path, semitones):
    audio = AudioSegment.from_file(audio_path)
    pitch_change = 2 ** (semitones / 12.0)
    filtered = audio._spawn(audio.raw_data, overrides={
        'frame_rate': int(audio.frame_rate * pitch_change)
    })
    filtered.export(audio_path, format='mp3')

audio_path = 'C:/work/git/CustomAI/output.mp3'
semitones = 3

change_pitch(audio_path, semitones)