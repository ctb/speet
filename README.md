# speet

Compute scaled MinHash sketches for text comparisons.

See
[our F1000 Research paper on DNA sketches](https://f1000research.com/articles/8-1006)
for some background information, and
[this Tweet thread](https://twitter.com/ctitusbrown/status/1171098539079766022)
for proximal motivation.

## Quick start - use speet to search the CPython source code for dups

1. Install speet.

2. Download the CPython master:

```
curl -O -L https://github.com/python/cpython/archive/master.zip
mkdir work && cd work && unzip -v ../master.zip
```

3. Sketch all the files:

```
speet sketchall work
```

This sketches all ~5000 files and takes about 30 seconds on my laptop.

4. Search all the files with a fragmented `configure` file:

```
speet fragment_query work/cpython-master/configure work
```
