from jinja2 import Environment, FileSystemLoader
import argparse
import pathlib2

__dir__ = pathlib2.Path(__file__).parent.absolute()
parser = argparse.ArgumentParser("generate README parser")
parser.add_argument("-i", "--input", help="input file path")
args = parser.parse_args()

with open(args.input, "r") as f:
    toc = f.read()
file_loader = FileSystemLoader(__dir__)
env = Environment(loader=file_loader)

template = env.get_template('README.template.md')

output = template.render(TOC=toc)
print(output)
