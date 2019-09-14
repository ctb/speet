import argparse
import os
import sys

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


def sketchall(args):
    "Create scaled MinHashes for everything under this directory."

    n = 0
    for root, _, files in os.walk(args.directory):
        for name in files:
            print(u'\r\033[K', end='')
            print("... sketch #{} from file {} ".format(n, name), end='\r')
            filename = os.path.join(root, name)
            with open(filename, 'rt') as fp:
                try:
                    text = fp.read()
                except UnicodeDecodeError:
                    continue

            mh = ScaledMinHash(name=filename)
            mh.add_text(text)

            mh.save(filename + '.sketch')
            n += 1

    print('\nsketched {}'.format(n))


def fragment_query(args):
    "Fragment query into many pieces, find in directory of sketches."
    # first, fragment the query.
    fragments = []

    chunk = args.fragment_size
    with open(args.query, 'rt') as fp:
        n = 0
        while 1:
            text = fp.read(chunk)
            if not text:
                break

            name = '{} fragment {}-{}'.format(args.query, chunk*n, chunk*(n+1))
            sketch = ScaledMinHash(name=name)
            sketch.add_text(text)
            fragments.append(sketch)

            n += 1

    print("got {} fragments of size {} from {}".format(len(fragments),
                                                       chunk, args.query))

    # now, load all the subject sketches
    subjects = []
    for root, _, files in os.walk(args.directory):
        for name in files:
            if not name.endswith('.sketch'):
                continue

            filename = os.path.join(root, name)

            print(u'\r\033[K', end='')
            print("... loading sketch {}".format(name), end='\r')
            sketch = ScaledMinHash.load(filename)

            subjects.append(sketch)

    print("\nloaded {} sketches from {}".format(len(subjects), args.directory))

    # now... search!!
    for query in fragments:
        matches = []
        for subject in subjects:
            cont = query.contained_by(subject)
            if cont > args.threshold:
                matches.append((cont, subject))

        if len(matches) > 0.9*len(subjects):
            print('found {} in 90% or more; not reporting'.format(query.name))

        if len(matches):
            print('found {} matches to {}'.format(len(matches), query.name))

            matches.sort(reverse=True, key=lambda x: x[0])

            for i in range(min(args.num_to_report, len(matches))):
                cont, match = matches[i]
                print("   {:.1f}% {}".format(cont*100, match.name))


def search(args):
    "Find Jaccard similarities between query and subjects."
    query = ScaledMinHash.load(args.query)
    subjects = [ScaledMinHash.load(filename) for filename in args.subjects]

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
    subjects = [ScaledMinHash.load(filename) for filename in args.subjects]

    results = []
    for ss in subjects:
        cont = query.contained_by(ss)
        if cont:
            results.append((cont, ss))

    results.sort(reverse=True)
    for cont, ss in results:
        print('{:.3f} {}'.format(cont, ss.name))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

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

    sketchall_p = subparsers.add_parser('sketchall')
    sketchall_p.add_argument("directory")
    sketchall_p.set_defaults(func=sketchall)

    fragment_query_p = subparsers.add_parser('fragment_query')
    fragment_query_p.add_argument("query")
    fragment_query_p.add_argument("directory")
    fragment_query_p.add_argument("--fragment-size", default=5000,
                                  help='size (in char) of query fragments')
    fragment_query_p.add_argument("--threshold", default=0.2,
                                  help='fraction of query fragment required')
    fragment_query_p.add_argument("--num-to-report", default=5)
    fragment_query_p.set_defaults(func=fragment_query)

    args = p.parse_args(argv)
    if args.func:
        return args.func(args) or 0
    else:
        print("Please specify a subcommand - use --help for options.")
        return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
