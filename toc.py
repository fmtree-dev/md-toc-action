import sys
import argparse
import pathlib2

from fmtree.scraper import Scraper
from fmtree.filter import MarkdownFilter
from fmtree.format import GithubMarkdownContentFormatter

if __name__ == '__main__':
    parser = argparse.ArgumentParser("md-toc parser")
    parser.add_argument("-i", "--input", required=True, help="input directory")

    args = parser.parse_args()
    scraper = Scraper(pathlib2.Path(args.input),
                      scrape_now=False, keep_empty_dir=False)
    scraper.add_filter(MarkdownFilter(ignore_list=['build-tools']))
    scraper.run()
    formatter = GithubMarkdownContentFormatter(scraper.get_tree(),
                                               no_readme_link=True,
                                               dir_link=True,
                                               full_dir_link=False,
                                               remove_md_ext=True,
                                               ignore_root_dir=True,
                                               link_dir_readme=True)
    stringio = formatter.generate()
    formatter.to_stream(sys.stdout)
