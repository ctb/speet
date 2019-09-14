import pickle

import mmh3

MAX_HASH = 2 ** 64 - 1


def hashme(kmer):
    "hash string of length k"
    return mmh3.hash64(kmer, seed=42)[0]


class ScaledMinHash(object):
    def __init__(self, scaled=500, ksize=5, name=""):
        self.scaled = scaled
        self.ksize = ksize
        self.hashes = set()
        self.name = name

    def add_text(self, text):
        ksize = self.ksize
        max_hash = MAX_HASH / self.scaled
        hashes = self.hashes

        # kmerize, hash, and add everything under 2**64/scaled
        for i in range(0, len(text) - ksize + 1):
            kmer = text[i:i+ksize]
            hashval = hashme(kmer)
            if hashval < max_hash:
                hashes.add(hashval)

    def similarity(self, other):
        if self.scaled != other.scaled or self.ksize != other.ksize:
            raise ValueError("incompatible ScaledMinHash comparison")

        intersection = self.hashes.intersection(other.hashes)
        union = self.hashes.union(other.hashes)
        if not len(union):
            return 0

        return len(intersection) / len(union)

    def contained_by(self, other):
        if self.scaled != other.scaled or self.ksize != other.ksize:
            raise ValueError("incompatible ScaledMinHash comparison")

        if not len(self):
            return 0.

        intersection = self.hashes.intersection(other.hashes)
        return len(intersection) / len(self)

    def __len__(self):
        return len(self.hashes)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as fp:
            return pickle.load(fp)

    def save(self, filename):
        with open(filename, 'wb') as fp:
            pickle.dump(self, fp)
