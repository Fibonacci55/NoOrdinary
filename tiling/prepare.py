#
import tomllib
import argparse

def create_arg_parser():
    parser = argparse.ArgumentParser(
                    prog = 'prepare',
                    description = 'Prepare an image collection for usage for tilings',
                    epilog = ' ')

    parser.add_argument('-f', '--file', type=str,
                        dest="config_file", default='config.toml',
                        help='configuration file')

    return parser


def read_config(config_file: str) -> dict:
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
    return data


if __name__ == '__main__':
    argp = create_arg_parser()

    args = argp.parse_args()
    config = read_config(args.config_file)
    print(config)
