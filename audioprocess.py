import whisper
import math
import glob, os
import pandas as pd
from pydub import AudioSegment
import scipy.io.wavfile as wav

# Python code to convert video to audio
import moviepy.editor as mp

#should be moved to videoprocess
def extract_audio(video_file, output_path="./source/test.wav"):
    clip = mp.VideoFileClip(video_file)
    clip.audio.write_audiofile(output_path,codec='pcm_s16le')

def audio_transcript(path, prompt=""):
    model = whisper.load_model("base")
    result = model.transcribe(path)
    return(result["text"])

def audio_transcript_all(source_folder="./source", output_file="transcript.csv"):
    filelist = glob.glob(source_folder+"/segment*.wav")
    transcripts = []
    
    count = 1
    nb = len(filelist)
    
    for file in filelist:
        print("processing file "+str(count)+"/"+str(nb))
        transcripts.append(audio_transcript(file))
        count+=1

    print(transcripts)

    dict = {'text': transcripts}
    df = pd.DataFrame(dict)
    df.to_csv('transcript.csv', encoding="utf-8")

    print("Done")


def audio_segment(path, lengh=5, timestamp=None, output_path="source/segment.wav"): #lengh in minutes
    if timestamp is None:
        song = AudioSegment.from_file(path)
        (source_rate, source_sig) = wav.read(path)
        duration_seconds = len(source_sig) / float(source_rate)

        nfrag = int(math.ceil(duration_seconds/60)/lengh)

        for i in range (nfrag):

            # PyDub handles time in milliseconds
            newAudio = AudioSegment.from_wav(path)
            newAudio = newAudio[((i)*1000*60*lengh):((i+1)*1000*60*lengh)]
            newAudio.export("source/segment"+str(i)+".wav", format="wav") #Exports to a wav file in the current path.

audio_transcript_all()