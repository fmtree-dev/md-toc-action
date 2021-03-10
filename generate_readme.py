from jinja2 import Environment, FileSystemLoader
import argparse
import pathlib2

__dir__ = pathlib2.Path(__file__).parent.absolute()
parser = argparse.ArgumentParser("generate README parser")
parser.add_argument("-i", "--input", required=True, help="toc.txt path")
parser.add_argument("-d", "--template_directory", required=True, help="Template Directory")
args = parser.parse_args()
# The arguments above are necessary

# TODO: below is what you can customize
with open(args.input, "r") as f:
    toc = f.read()
file_loader = FileSystemLoader(args.template_directory)
env = Environment(loader=file_loader)

template = env.get_template('README.template.md')

output = template.render(TOC=toc)
print(output)
# output to stdout
