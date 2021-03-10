import glob
import os

import fmtree
import pathlib2
import argparse
import subprocess as sp

__dir__ = pathlib2.Path(__file__).parent


def main(path: pathlib2.Path):
    target_dir = path.parent
    toc_py = path / 'toc.py'
    gen_md_py = path / 'generate_readme.py'
    if toc_py.exists():
        print("custom toc.py exists")

    else:
        toc_py = __dir__ / 'toc.py'
    if gen_md_py.exists():
        print("custom generate_readme.py exists")
    else:
        gen_md_py = __dir__ / 'generate_readme.py'
    try:
        sp.run(f"python {str(toc_py)} --input {str(target_dir)} > {str(path / 'toc.txt')}", shell=True)
    except Exception as e:
        print(e)
    try:
        sp.run(
            f"python {str(gen_md_py)} --input {str(path / 'toc.txt')} --template_directory {str(path)} > "
            f"{target_dir / 'README.md'}",
            shell=True)
    except Exception as e:
        print(e)
    os.remove(str(path / 'toc.txt'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("md-toc parser")
    parser.add_argument("--custom_dir", default=".md-toc", help="custom md-toc directory")
    args = parser.parse_args()
    print("Input Parameters")
    for k, v in args.__dict__.items():
        print(f"{k}: {v}")
    root = pathlib2.Path(__file__).parent
    md_toc_paths = glob.glob(f"**/{args.custom_dir}", recursive=True)
    md_toc_paths = [root / path for path in md_toc_paths]

    for path in md_toc_paths:
        assert path.exists()
        print(f"Current Path: {path}")
        main(path)
