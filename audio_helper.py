import codecs
import os
import random
import textwrap
from datetime import timedelta
import uuid

from google.cloud.texttospeech_v1beta1 import VoiceSelectionParams, AudioConfig, AudioEncoding, \
    SynthesizeSpeechRequest, SynthesisInput, TextToSpeechClient, SsmlVoiceGender
from srt import Subtitle, compose

import settings as s


def text_to_ssml(t):
    text_split = textwrap.wrap(t, s.CLIP.TEXT_WRAP)
    ret = {"text": text_split}
    text_ssml = []
    for i in range(len(text_split)):
        text_ssml.append(f"<mark name=\"{i}\"/>{text_split[i]}")
    text_joined = f"<speak>{' '.join(text_ssml)}.<mark name=\"{i + 1}\"/></speak>"
    ret['ssml'] = text_joined
    return ret


def create_voice_srt(text, language):
    uid = uuid.uuid1()
    voice_file = os.path.join(s.LOCAL.SOUND, f"{uid}_{language}.mp3")
    srt_file = os.path.join(s.LOCAL.VIDEO, f"{uid}_{language}.srt")

    client = TextToSpeechClient()
    text_ssml = text_to_ssml(text)
    synthesis_input = SynthesisInput(ssml=text_ssml["ssml"])
    voice = VoiceSelectionParams(language_code=s.LINGUISTIC.LANGUAGE_CODES[language],
                                 ssml_gender=random.choice(list(SsmlVoiceGender)))
    audio_config = AudioConfig(audio_encoding=AudioEncoding.MP3)
    request = SynthesizeSpeechRequest(input=synthesis_input, voice=voice, audio_config=audio_config,
                                      enable_time_pointing=[SynthesizeSpeechRequest.TimepointType.SSML_MARK])
    response = client.synthesize_speech(request=request)
    time_points = list(response.timepoints)
    with open(voice_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{voice_file}"')
    subs = []
    for i in range(len(time_points) - 1):
        point = time_points[i]
        point_next = time_points[i + 1]
        subs.append(Subtitle(
            index=int(point.mark_name),
            start=timedelta(seconds=point.time_seconds + s.CLIP.AUDIO_START),
            end=timedelta(seconds=point_next.time_seconds - 0.2 + s.CLIP.AUDIO_START),
            content=text_ssml['text'][i]
        ))
    composed = compose(subs)
    with codecs.open(srt_file, "w", "utf-8") as out:
        out.write(composed)
        print(f'Subtitles written to file {srt_file}')
    return voice_file, srt_file


