import argparse
from wojak_generator.render import PhotoRender
from wojak_generator.templates import Templates

def render(name: str, texts: list, output: str):
    config = templates.one(name)
    path = f'{templates.base}/{name}'
    parser = PhotoRender(f'{path}/template.jpg', config)
    parser.run(texts)
    parser.saveToDisk(output)
    parser.cleanup()

if __name__ == "__main__":
    templates = Templates()
    cli = argparse.ArgumentParser()
    cli.add_argument('-i', '--input', help='Template name')
    cli.add_argument('-o', '--output', default='out/meme', help='Output file')
    cli.add_argument('--texts', nargs='+', default=[])
    args = cli.parse_args()

    render(args.input, args.texts, args.output)
