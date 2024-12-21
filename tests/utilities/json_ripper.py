#!/usr/bin/env python3
import argparse
import json
import sys


def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "json_index",
        help="The index of the json object to be returned separated by periods",
    )
    parser.add_argument(
        "--indent",
        help="The indent to be used when printing the json object",
        type=int,
        default=None,
    )

    parser.add_argument("--json_file", help="The json file to be read")

    return parser


def main():
    args = argparser().parse_args()

    # check piped input for JSON
    if not args.json_file:
        json_object = json.load(sys.stdin)
    else:
        with open(args.json_file) as json_file:
            json_object = json.load(json_file)

    keys = args.json_index.split(".")
    current_object = json_object
    try:
        for key in keys:
            # check for [index] in key 
            if "[" in key and "]" in key:
                key, index = key.split("[")
                index = index.replace("]", "")
                current_object = current_object[key][int(index)]
            else:
                current_object = current_object[key]
    except KeyError:
        sys.exit(1)
        
    if args.indent:
        print(json.dumps(current_object, indent=args.indent))
    else:
        print(current_object, sep="")
        
if __name__ == "__main__":
    main()
