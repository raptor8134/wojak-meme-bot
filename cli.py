import argparse
from wojak_generator.helpers import pick_render
from wojak_generator.templates import Templates

def render(name: str, texts: list, output: str, mode: str):
    templates = Templates()
    config = templates.one(name)
    parser = pick_render(mode, config)
    parser.run(texts)
    parser.saveToDisk(output)
    parser.cleanup()

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument('mode', help='Choose between ascii or photo')
    cli.add_argument('-i', '--input', help='Template name')
    cli.add_argument('-o', '--output', default='out/meme.jpg', help='Output file')
    cli.add_argument('--texts', nargs='+', default=[])
    args = cli.parse_args()

    render(args.input, args.texts, args.output, args.mode)
