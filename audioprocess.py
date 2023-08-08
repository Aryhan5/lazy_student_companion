import whisper
from pydub import AudioSegment

# Python code to convert video to audio
import moviepy.editor as mp

def extract_audio(video_file):
    clip = mp.VideoFileClip(video_file)
    clip.audio.write_audiofile("./test.wav",codec='pcm_s16le')

def audio_transcript(path, prompt=""):
    model = whisper.load_model("base")
    result = model.transcribe(path)
    return(result["text"])

def audio_segment(path, lengh=3): #lengh in minutes
    song = AudioSegment.from_file(path)

    # PyDub handles time in milliseconds
    newAudio = AudioSegment.from_wav(path)
    newAudio = newAudio[:(lengh*1000*60)]
    newAudio.export('segment.wav', format="wav") #Exports to a wav file in the current path.

short = audio_segment("test.wav", 5)
transcript = audio_transcript("segment.wav")
print(transcript)