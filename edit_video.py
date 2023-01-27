from moviepy.editor import *
import openai
from gtts import gTTS

openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")


# get the clip
clip = VideoFileClip("league_clip_1.mp4")

# remove the audio
new_clip = clip.without_audio()

# get the length of the video  (seconds)
total_length_of_vid = clip.duration


# get a text script from an ai text api with the request:
x = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"write a script for an interesting story to keep users engaged and it should take {total_length_of_vid} seconds total for a text-to-speech reader to read",
    max_tokens=1000,
    temperature=0,
)

story_script = x["choices"][0]["text"]


# generate an ai voice reading this text
language = "en"
speech = gTTS(text=story_script, lang=language)
speech.save("audio_clip.mp3")

# set the audio clip to the movie and save as new mp4
audioclip = AudioFileClip("audio_clip.mp3")
new_audioclip = CompositeAudioClip([audioclip])
new_clip.audio = new_audioclip
new_clip.write_videofile("final_clip.mp4")

# now need to delete the files
