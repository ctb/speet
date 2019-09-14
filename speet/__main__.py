import sys
import argparse
from . import ScaledMinHash


def sketch(args):
    "Create scaled MinHashes for the given textfile."
    with open(args.textfile, 'rt') as fp:
        text = fp.read()

    mh = ScaledMinHash(name=args.textfile)
    mh.add_text(text)

    mh.save(args.output)
    print('read {}, hashed to {}, saved into {}'.format(len(text),
                                                        len(mh),
                                                        args.output))


def search(args):
    "Find Jaccard similarities between query and subjects."
    query = ScaledMinHash.load(args.query)
    subjects = [ ScaledMinHash.load(filename) for filename in args.subjects ]

    results = []
    for ss in subjects:
        similarity = query.similarity(ss)
        if similarity:
            results.append((similarity, ss))

    results.sort(reverse=True)
    for similarity, ss in results:
        print('{:.3f} {}'.format(similarity, ss.name))


def contained_by(args):
    "Find containment of query in subjects."
    query = ScaledMinHash.load(args.query)
    subjects = [ ScaledMinHash.load(filename) for filename in args.subjects ]

    results = []
    for ss in subjects:
        cont = query.contained_by(ss)
        if cont:
            results.append((cont, ss))

    results.sort(reverse=True)
    for cont, ss in results:
        print('{:.3f} {}'.format(cont, ss.name))


def main(argv):
    p = argparse.ArgumentParser()
    p.set_defaults(func=None)
    subparsers = p.add_subparsers()

    sketch_p = subparsers.add_parser("sketch")
    sketch_p.add_argument("textfile")
    sketch_p.add_argument("output")
    sketch_p.set_defaults(func=sketch)

    search_p = subparsers.add_parser("search")
    search_p.add_argument("query")
    search_p.add_argument("subjects", nargs='+')
    search_p.set_defaults(func=search)

    cont_p = subparsers.add_parser("contained_by")
    cont_p.add_argument("query")
    cont_p.add_argument("subjects", nargs='+')
    cont_p.set_defaults(func=contained_by)

    args = p.parse_args(argv)
    if args.func:
        return args.func(args) or 0
    else:
        print("Please specify a subcommand - use --help for options.")
        return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
