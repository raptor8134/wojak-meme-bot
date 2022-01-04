import argparse
from wojak_generator.helpers import isValidMode, pickRender
from wojak_generator.templates import Templates

def render(name: str, texts: list, output: str, mode: str):
    templates = Templates()
    config = templates.one(name)
    if not isValidMode(mode):
        raise Exception('Invalid mode')
    parser = pickRender(mode, config)
    parser.run(texts)
    parser.saveToDisk(output)
    parser.cleanup()

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument('mode', help='Choose between ascii or photo')
    cli.add_argument('-i', '--input', help='Template name')
    cli.add_argument('-o', '--output', default='out/meme', help='Output file')
    cli.add_argument('--texts', nargs='+', default=[])
    args = cli.parse_args()

    render(args.input, args.texts, args.output, args.mode)
