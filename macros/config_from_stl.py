import yaml
from functools import reduce

__PREAMBLE = """
# This file was generated by config_from_stl.py
#
# Description: This file is used to define the geometry of the detector.
#             The geometry is defined by a list of parts, each of which
#             is a separate STL file. Each part can have its own material
#             properties, and can be marked as a detector or not.
#
#             Colors are specified in hexadecimal format, with the alpha
#             channel as the first two digits, followed by red, green, and
#             blue. I.e., 0xAARRGGBB.
#
"""

__DETLEVEL_FORMAT = """
target: vacuum
log: true

parts:"""

__PART_FORMAT = """
  - name: {}
    options:
      is_detector: false

      path: {}

      # The scale factor to apply to the STL file
      scale: 1.0

      # The translation to apply to the STL file
      translation: (0,0,0)

      # The rotation to apply to the STL file
      rotation:
        angle: 0          # in degrees
        dir: [0,0,1]

    # Material properties
      material:
        material1: null   # change me!
        material2: null   # change me!
        surface: null     # change me!
        color: 0x00FFFFFF

"""


def part_from_stl(filename):
    name = filename.split('/')[-1].split('.')[0]
    return __PART_FORMAT.format(name, filename)

def config_from_stls(files):
    return reduce(lambda x,y: x+y, map(part_from_stl, files))

def dump_config(config, filename):
    TEXT = __PREAMBLE + __DETLEVEL_FORMAT + config

    # check that the file is correct yaml
    try:
        yaml.load(TEXT, Loader=yaml.SafeLoader)
    except yaml.YAMLError as e:
        print("Error in generated yaml file:")
        print(e)
        return

    with open(filename, 'w') as f:
        f.write(TEXT)

if __name__ == "__main__":
    import argparse
    import os

    # input: python config_from_stl.py out.yaml file1.stl file2.stl file3.stl ...
    # output: out.yaml

    parser = argparse.ArgumentParser(description='Build and view a detector from a yaml file')
    parser.add_argument('output', type=str, help='path to the output yaml file')
    parser.add_argument('files', type=str, nargs='+', help='space separated list of stl files (can use *)')

    args = parser.parse_args()
    args.files = list(map(os.path.abspath, args.files))    

    # create a dictionary with the name of the output file and the list of files
    config = config_from_stls(args.files)
    # dump the dictionary into a yaml file
    dump_config(config, args.output)

