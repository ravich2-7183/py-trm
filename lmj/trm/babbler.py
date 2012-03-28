# Copyright (c) 2011 Leif Johnson <leif@leifjohnson.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''Classes for babbling using the postures in a repertoire.'''


class Babbler(list):
    '''A babbler generates sequences of phone symbols from a repertoire.'''

    def __init__(self, repertoire):
        self.extend(sorted(repertoire.postures))

    def generate(self, n=7):
        for _ in range(n):
            yield self[self.index()]

    def index(self):
        raise NotImplementedError


class Uniform(Babbler):
    '''A uniform babbler selects phones randomly.'''

    def index(self):
        return rng.randint(len(self))


class Unigram(Babbler):
    '''A unigram babbler samples from a discrete distribution.'''

    def __init__(self, repertoire, pmf):
        super(Unigram, self).__init__(repertoire)

        pmf = numpy.asarray(pmf)
        assert len(pmf) == len(self)
        assert numpy.allclose(pmf.sum(), 1)
        self.cdf = pmf.cumsum()

    def index(self):
        return self.cdf.searchsorted(rng.random())


class Bigram(Babbler):
    '''A bigram babbler samples from a discrete distribution for each phone.'''

    def __init__(self, repertoire, unigrams, bigrams):
        super(Bigram, self).__init__(repertoire)

        unigrams = numpy.asarray(unigrams)
        assert len(unigrams) == len(self)
        assert numpy.allclose(unigrams.sum(), 1)
        self.unigram_cdf = unigrams.cumsum()

        bigrams = numpy.asarray(bigrams)
        assert bigrams.shape == (len(self), len(self))
        assert numpy.allclose(bigrams.sum(axis=1), numpy.ones(len(bigrams)))
        self.bigram_cdfs = [p.cumsum() for p in bigrams]

        self.idx = None

    def generate(self, *args, **kwargs):
        self.idx = None
        return super(Bigram, self).generate(*args, **kwargs)

    def index(self):
        cdf = self.unigram_cdf
        if self.idx is not None:
            cdf = self.bigram_cdfs[self.idx]
        self.idx = cdf.searchsorted(rng.random())
        return self.idx
