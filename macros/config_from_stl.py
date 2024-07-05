#!/usr/bin/env python3

import yaml
import argparse
import os
from typing import List
from datetime import datetime

PREAMBLE = """
# This file was generated by config_from_stl.py on {date}
#
# Description: This file is used to define the geometry of the detector.
#             The geometry is defined by a list of parts, each of which
#             is a separate STL file. Each part can have its own material
#             properties, and can be marked as a detector or not.
#
#             Colors can be specified in hexadecimal, e.g. 0x00ff00 for green,
#             as a string, e.g. 'green', or as a uint32, e.g. 0x00ff00ff for
#             green with full opacity. All matplotlib colors are supported.
#
"""

DETLEVEL_FORMAT = """
target: vacuum
log: true

parts:"""

PART_TEMPLATE = """
  - name: {name}
    is_detector: false
    path: {path}
    scale: 1.0
    translation: [0,0,0]
    rotation:
      angle: 0
      dir: [0,0,1]
    material:
      surface: null
      material1: null
      material2: null
      color: lightgrey
"""

def generate_part_config(path: str) -> str:
    name = os.path.splitext(os.path.basename(path))[0]
    return PART_TEMPLATE.format(name=name, path=path)

def generate_config(files: List[str]) -> str:
    return ''.join(map(generate_part_config, files))

def validate_and_dump_config(config: str, output_path: str) -> None:
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_config = PREAMBLE.format(date=current_date) + DETLEVEL_FORMAT + config
    try:
        yaml.safe_load(full_config)
    except yaml.YAMLError as e:
        print(f"Error in generated yaml file: {e}")
        return

    with open(output_path, 'w') as f:
        f.write(full_config)

def main():
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Build and view a detector from a yaml file')
    parser.add_argument('name', type=str, help='yaml file name')
    parser.add_argument('files', type=str, nargs='+', help='space separated list of stl files (can use *)')

    args = parser.parse_args()
    stl_files = [os.path.abspath(f) for f in args.files]

    output_path = Path('config') / f"{args.name}.yaml"
    config = generate_config(stl_files)
    validate_and_dump_config(config, output_path.resolve())

if __name__ == "__main__":
    main()
