import sys
import argparse
import pathlib2
from typing import List, Iterable

from fmtree.scraper import Scraper
from fmtree.filter import MarkdownFilter
from fmtree.format import GithubMarkdownContentFormatter
from fmtree import sorter
from fmtree.node import FileNode


class OSCPExerciseSorter(sorter.BaseSorter):
    def sorted(self, nodes: List[FileNode]) -> Iterable:
        # TODO: Write your implementation here
        return sorted(nodes, key=lambda node: node.get_filename())


if __name__ == '__main__':
    parser = argparse.ArgumentParser("md-toc parser")
    parser.add_argument("-i", "--input", required=True, help="input directory")
    args = parser.parse_args()
    # Write your custom implementation below
    scraper = Scraper(pathlib2.Path(args.input), scrape_now=False, keep_empty_dir=False, depth=4)
    scraper.add_filter(MarkdownFilter())                # TODO: Your Custom Filter, as many as you need
    scraper.run()
    sorter_ = OSCPExerciseSorter()                      # TODO: Your Custom Sorter
    tree = sorter_(scraper.get_tree())

    # TODO: Custom Formatter, GithubMarkdownContentFormatter should be enough for GitHub
    formatter = GithubMarkdownContentFormatter(tree,
                                               no_readme_link=True,
                                               dir_link=True,
                                               full_dir_link=False,
                                               remove_md_ext=True,
                                               ignore_root_dir=True,
                                               link_dir_readme=True)
    stringio = formatter.generate()
    # custom implementation end here
    formatter.to_stream(sys.stdout)         # must output to stdout