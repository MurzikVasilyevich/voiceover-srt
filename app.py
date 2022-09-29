import audio_helper
import argparse


def main(txt, language):
    audio_helper.create_voice_srt(txt, language)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--text', type=str, default=None, help='Text to be spoken')
    group.add_argument('-f', '--file', type=str, default=None, help='File to be spoken')
    parser.add_argument('-l', '--language', type=str, default="en", help='Language to be spoken')
    args = parser.parse_args()
    if args.file:
        with open(args.file, "r") as f:
            text = f.read()
    else:
        text = args.text
    main(text, args.language)
