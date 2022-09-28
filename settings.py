import ast
import os


def eval_bool(value):
    return eval((os.environ[value]).capitalize())


class LOCAL:
    SOUND = "./sounds/"
    VIDEO = "./videos/"
    STORAGE = "./results/"
    CLEAR_EACH_RUN = False


class LINGUISTIC:
    LANGUAGES = ["en", "uk"]
    PARTS_OF_SPEECH = ["ADJ", "ADV", "NOUN", "VERB"]
    LANGUAGE_CODES = {"en": "en-US", "uk": "uk-UA", "ru": "ru-RU"}


class CLIP:
    AUDIO_START = 2
    TEXT_WRAP = 50
