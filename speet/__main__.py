import sys
import argparse
from . import ScaledMinHash


def sketch(args):
    with open(args.textfile, 'rt') as fp:
        text = fp.read()

    mh = ScaledMinHash()
    mh.add_text(text)

    mh.save(args.output)
    print('read {}, hashed to {}, saved into {}'.format(len(text),
                                                        len(mh),
                                                        args.output))


def search(args):
    query = ScaledMinHash.load(args.query)
    subjects = [ ScaledMinHash.load(filename) for filename in args.subjects ]

    results = []
    for ss in subjects:
        similarity = query.similarity(ss)
        if similarity:
            results.append((similarity, ss))

    results.sort(reverse=True)
    for (similarity, ss), filename in zip(results, args.subjects):
        print('{} {}'.format(similarity, filename))


def main(argv):
    p = argparse.ArgumentParser()
    subparsers = p.add_subparsers()

    sketch_p = subparsers.add_parser("sketch")
    sketch_p.add_argument("textfile")
    sketch_p.add_argument("output")
    sketch_p.set_defaults(func=sketch)

    search_p = subparsers.add_parser("search")
    search_p.add_argument("query")
    search_p.add_argument("subjects", nargs='+')
    search_p.set_defaults(func=search)

    args = p.parse_args(argv)
    return args.func(args) or 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
