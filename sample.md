# Sample `toc.py`

```python
import re
import sys
import argparse
import pathlib2
from typing import List, Iterable
from functools import cmp_to_key

from fmtree.scraper import Scraper
from fmtree.filter import MarkdownFilter
from fmtree.format import GithubMarkdownContentFormatter
from fmtree import sorter
from fmtree.node import FileNode


class OSCPExerciseSorter(sorter.BaseSorter):
    exercise_re_pattern = re.compile("^(\\d+\\.)+\\d+$")

    def sorted(self, nodes: List[FileNode]) -> Iterable:
        relative_path = nodes[0].get_path(
        ).parent.relative_to(nodes[0].get_root())
        filenames = [node.get_filename() for node in nodes]
        max_num_count = max([len(filename.split("."))
                             for filename in filenames])

        def comparator(node1: FileNode, node2: FileNode):
            filename1, filename2 = node1.get_filename(), node2.get_filename()
            nums1, nums2 = list(map(int, filename1.split("."))), list(map(int, filename2.split("."))) 
            i = -1
            while i < max_num_count and i < len(nums1) and i < len(nums2):
                i += 1
                if nums1[i] == nums2[i]:
                    continue
                elif nums1[i] < nums2[i]:
                    return -1
                else:
                    return 1
            return 0

        if relative_path.name == "Exercises":
            nodes = list(filter(lambda node: OSCPExerciseSorter.exercise_re_pattern.match(
                node.get_filename()), nodes))
            nodes = sorted(nodes, key=cmp_to_key(comparator))
            for i in range(len(nodes) - 1):
                assert int(nodes[i].get_filename().split('.')[0]) <= int(
                    nodes[i + 1].get_filename().split('.')[0])
            return nodes
        else:
            return sorted(nodes, key=lambda node: node.get_filename())



if __name__ == '__main__':
    parser = argparse.ArgumentParser("md-toc parser")
    parser.add_argument("-i", "--input", required=True, help="input directory")
    args = parser.parse_args()
    scraper = Scraper(pathlib2.Path(args.input),
                      scrape_now=False, keep_empty_dir=False)
    scraper.add_filter(MarkdownFilter(ignore_list=['build-tools']))
    scraper.run()
    sorter_ = OSCPExerciseSorter()
    tree = sorter_(scraper.get_tree())
    formatter = GithubMarkdownContentFormatter(tree,
                                               no_readme_link=True,
                                               dir_link=True,
                                               full_dir_link=False,
                                               remove_md_ext=True,
                                               ignore_root_dir=True,
                                               link_dir_readme=False)
    stringio = formatter.generate()
    formatter.to_stream(sys.stdout)
```

In this example I wrote a custom sorter which I personally use.

The structure of file system I scraped is like

```
OSCP
├── Exercises
│   ├── 1.0.0
│   │   └── README.md
│   ├── 1.0.1
│   │   └── README.md
│   ├── 10.2.1
│   │   └── README.md
│   ├── 10.2.3
│   │   └── README.md
│   ├── 11.1.0
│   │   └── README.md
│   ├── 11.5.1
│   │   └── README.md
│   ├── 2.0.1
│   │   └── README.md
│   ├── 2.0.2
│   │   └── README.md
│   ├── 3.0.0
│   │   └── README.md
│   ├── 4.3.8
│   │   └── README.md
│   ├── 4.5.7
│   │   └── README.md
│   ├── 5.6.0
│   │   └── README.md
│   ├── 5.9.0
│   │   └── README.md
│   ├── 6.0.0
│   │   └── README.md
│   ├── 7.3.3
│   │   └── README.md
│   ├── 7.3.6
│   │   └── README.md
│   ├── 8.1.3
│   │   └── README.md
│   ├── 8.1.5
│   │   └── README.md
│   └── 9.2.0
│       └── README.md
└── Notes
    ├── Bash.md
    ├── common.md
    ├── FileTransfer.md
    ├── README.md
    ├── Service.md
    └── Tools
        ├── Metasploit.md
        ├── Netcat.md
        ├── nmap.md
        └── Python.md
```

The directories in the **Exercises** directory contains `.`, thus cannot be easily sorted.

Regular sort function doesn't work.

In order for the Table of Content to be sorted, I wrote the Sorter.

The Tree Output looks like

```
OSCP
├── Exercises
│   ├── 1.0.0
│   │   └── README.md
│   ├── 1.0.1
│   │   └── README.md
│   ├── 2.0.1
│   │   └── README.md
│   ├── 2.0.2
│   │   └── README.md
│   ├── 3.0.0
│   │   └── README.md
│   ├── 4.3.8
│   │   └── README.md
│   ├── 4.5.7
│   │   └── README.md
│   ├── 5.6.0
│   │   └── README.md
│   ├── 5.9.0
│   │   └── README.md
│   ├── 6.0.0
│   │   └── README.md
│   ├── 7.3.3
│   │   └── README.md
│   ├── 7.3.6
│   │   └── README.md
│   ├── 8.1.3
│   │   └── README.md
│   ├── 8.1.5
│   │   └── README.md
│   ├── 9.2.0
│   │   └── README.md
│   ├── 10.2.1
│   │   └── README.md
│   ├── 10.2.3
│   │   └── README.md
│   ├── 11.1.0
│   │   └── README.md
│   └── 11.5.1
│       └── README.md
└── Notes
    ├── Bash.md
    ├── FileTransfer.md
    ├── README.md
    ├── Service.md
    ├── Tools
    │   ├── Metasploit.md
    │   ├── Netcat.md
    │   ├── Python.md
    │   └── nmap.md
    └── common.md
```

The GitHub MarkDown TOC Format is,

```markdown
- OSCP
        - Exercises
                - [1.0.0](./Exercises/1.0.0)
                - [1.0.1](./Exercises/1.0.1)
                - [2.0.1](./Exercises/2.0.1)
                - [2.0.2](./Exercises/2.0.2)
                - [3.0.0](./Exercises/3.0.0)
                - [4.3.8](./Exercises/4.3.8)
                - [4.5.7](./Exercises/4.5.7)
                - [5.6.0](./Exercises/5.6.0)
                - [5.9.0](./Exercises/5.9.0)
                - [6.0.0](./Exercises/6.0.0)
                - [7.3.3](./Exercises/7.3.3)
                - [7.3.6](./Exercises/7.3.6)
                - [8.1.3](./Exercises/8.1.3)
                - [8.1.5](./Exercises/8.1.5)
                - [9.2.0](./Exercises/9.2.0)
                - [10.2.1](./Exercises/10.2.1)
                - [10.2.3](./Exercises/10.2.3)
                - [11.1.0](./Exercises/11.1.0)
                - [11.5.1](./Exercises/11.5.1)
        - [Notes](./Notes)
                - [Bash](./Notes/Bash.md)
                - [FileTransfer](./Notes/FileTransfer.md)
                - [Service](./Notes/Service.md)
                - Tools
                        - [Metasploit](./Notes/Tools/Metasploit.md)
                        - [Netcat](./Notes/Tools/Netcat.md)
                        - [Python](./Notes/Tools/Python.md)
                        - [nmap](./Notes/Tools/nmap.md)
                - [common](./Notes/common.md)
```

Sample Table of Content

- OSCP
  - Exercises
    - [1.0.0](./Exercises/1.0.0)
    - [1.0.1](./Exercises/1.0.1)
    - [2.0.1](./Exercises/2.0.1)
    - [2.0.2](./Exercises/2.0.2)
    - [3.0.0](./Exercises/3.0.0)
    - [4.3.8](./Exercises/4.3.8)
    - [4.5.7](./Exercises/4.5.7)
    - [5.6.0](./Exercises/5.6.0)
    - [5.9.0](./Exercises/5.9.0)
    - [6.0.0](./Exercises/6.0.0)
    - [7.3.3](./Exercises/7.3.3)
    - [7.3.6](./Exercises/7.3.6)
    - [8.1.3](./Exercises/8.1.3)
    - [8.1.5](./Exercises/8.1.5)
    - [9.2.0](./Exercises/9.2.0)
    - [10.2.1](./Exercises/10.2.1)
    - [10.2.3](./Exercises/10.2.3)
    - [11.1.0](./Exercises/11.1.0)
    - [11.5.1](./Exercises/11.5.1)
  - [Notes](./Notes)
    - [Bash](./Notes/Bash.md)
    - [FileTransfer](./Notes/FileTransfer.md)
    - [Service](./Notes/Service.md)
    - Tools
      - [Metasploit](./Notes/Tools/Metasploit.md)
      - [Netcat](./Notes/Tools/Netcat.md)
      - [Python](./Notes/Tools/Python.md)
      - [nmap](./Notes/Tools/nmap.md)
    - [common](./Notes/common.md)