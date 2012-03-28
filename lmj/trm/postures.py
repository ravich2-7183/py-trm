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

'''A synthesis wrapper for postures and parameters in the TRM.'''

import itertools
import logging
import numpy
import numpy.random as rng
import os
import scipy.interpolate

from xml.dom import minidom

import tube

PARAMETERS = ('microInt',
              'glotVol',
              'aspVol',
              'fricVol', 'fricPos', 'fricCF', 'fricBW',
              'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8',
              'velum')


class Parameter:
    '''A single control parameter.'''

    def __init__(self, xml):
        self.name = xml.getAttribute('name')
        self.min = float(xml.getAttribute('minimum'))
        self.max = float(xml.getAttribute('maximum'))
        self.default = float(xml.getAttribute('default'))

    def __hash__(self):
        return hash(self.name)

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __str__(self):
        return '<Parameter %s: [%s, %s], %s>' % (
            self.name, self.min, self.max, self.default)

    def clip(self, value=None):
        '''Clip a value to the range for this parameter.'''
        if value is None:
            value = self.default
        return max(self.min, min(self.max, value))

    def clip_to_default(self, value=None):
        '''If value is not within range, return the default.'''
        if value is not None and self.min <= value <= self.max:
            return value
        return default


class Symbol(Parameter):
    '''An abstract attribute of a phoneme, like its typical duration.'''

    def __str__(self):
        return '<Symbol %s: [%s, %s], %s>' % (
            self.name, self.min, self.max, self.default)


class Posture:
    '''A single control frame capable of producing a particular phoneme.

    A posture is a collection of values for each of the 16 control parameters,
    plus some symbols that describe the posture's typical duration, etc. At its
    most naive implementation, postures can be "strung together" one after
    another to produce speech sounds ; usually better synthesis comes from
    altering the overall sequence of parameters according to prosody or other
    constraints. However, a single posture tells us where to start looking if we
    want to produce a particular phoneme.
    '''

    def __init__(self, xml, parameters, symbols):
        self.parameters = parameters
        self.symbols = symbols
        self.symbol = xml.getAttribute('symbol')

        self.categories = set()
        for t in xml.getElementsByTagName('posture-categories'):
            for n in t.getElementsByTagName('category-ref'):
                c = n.getAttribute('name')
                if c != self.symbol:
                    self.categories.add(c)

        def store(d, n):
            d[n.getAttribute('name')] = float(n.getAttribute('value'))

        self.parameter_targets = {}
        for t in xml.getElementsByTagName('parameter-targets'):
            for n in t.getElementsByTagName('target'):
                store(self.parameter_targets, n)

        self.symbol_targets = {}
        for t in xml.getElementsByTagName('symbol-targets'):
            for n in t.getElementsByTagName('target'):
                store(self.symbol_targets, n)

    def __hash__(self):
        return hash(self.symbol)

    def __cmp__(self, other):
        return cmp(self.symbol, other.symbol)

    def __str__(self):
        return '<Posture %s: %s>' % (self.symbol, ', '.join(sorted(self.categories)))

    @property
    def targets(self):
        return [self.parameter_targets[n] for n in PARAMETERS]

    @property
    def transition(self):
        return self.symbol_targets['transition']

    @property
    def duration(self):
        return self.symbol_targets['duration']

    @property
    def is_vocoid(self):
        return 'vocoid' in self.categories

    @property
    def is_elongated(self):
        return self.symbol.endswith("'")

    def create_gaussian(self, symbols, parameters, *args, **kwargs):
        '''Return a gaussian wrapper for this posture.'''
        return GaussianPosture(self, symbols, parameters, *args, **kwargs)


class GaussianPosture(Posture):
    '''A statistical model that wraps a posture in a multivariate gaussian.'''

    def __init__(self, posture, symbols, parameters,
                 target_covariance=None,
                 transition_variance=1.,
                 duration_variance=1.):
        '''Initialize this wrapper with a posture and covariance values.'''
        self.posture = posture
        self.symbol = posture.symbol
        self.categories = posture.categories

        self.symbols = symbols
        self.parameters = parameters

        targets = numpy.array(self.posture.targets)
        targets.shape += (1, )
        tcov = target_covariance
        if tcov is None:
            tcov = numpy.dot(targets, targets.T)
        elif isinstance(tcov, (int, float)):
            tcov = tcov + numpy.zeros((len(targets), ), float)
        if len(tcov.shape) == 1 and len(tcov) == len(targets):
            tcov = numpy.diag(tcov)

        self.target_covariance = tcov
        self.transition_variance = transition_variance
        self.duration_variance = duration_variance

    @property
    def targets(self):
        zs = rng.multivariate_normal(self.posture.targets, self.target_covariance)
        ps = (self.parameters[p] for p in PARAMETERS)
        return [param.clip(z) for param, z in zip(ps, zs)]

    @property
    def transition(self):
        return self.symbols['transition'].clip(rng.normal(
            self.posture.transition, self.transition_variance))

    @property
    def duration(self):
        return self.symbols['duration'].clip(rng.normal(
            self.posture.duration, self.duration_variance))


DIPHONES_MXML = os.path.join(os.path.dirname(__file__), 'diphones.mxml')

class Repertoire:
    '''A group of postures that are defined for the TRM.

    A repertoire is like the total knowledge of how to control the vocal
    synthesizer to produce phonemes. In Gnuspeech, a repertoire is summarized in
    a single XML file that describes the postures for the synthesizer, plus a
    bunch of equations that are used to combine the different postures into a
    sequence of speech sounds.

    So far, this Python wrapper just encompasses the postures and parameters for
    the synthesizer.
    '''

    def __init__(self, parameters=None, symbols=None, postures=None,
                 xml_file=DIPHONES_MXML):
        self.parameters = parameters or {}
        self.symbols = symbols or {}
        self.postures = postures or {}

        if xml_file:
            self.parse_xml(xml_file)

    def parse_xml(self, xml_file):
        xml = minidom.parse(xml_file)

        # PARAMETERS
        for n in xml.getElementsByTagName('parameter'):
            p = Parameter(n)
            self.parameters[p.name] = p

        for p in sorted(self.parameters):
            logging.info(self.parameters[p])

        # SYMBOLS
        for n in xml.getElementsByTagName('symbol'):
            s = Symbol(n)
            self.symbols[s.name] = s

        for s in sorted(self.symbols):
            logging.info(self.symbols[s])

        # POSTURES
        for n in xml.getElementsByTagName('posture'):
            p = Posture(n, self.parameters, self.symbols)
            self.postures[p.symbol] = p

        for r in sorted(self.postures):
            logging.info(self.postures[r])

    def iter_vocoid(self):
        '''Iterate over all vocoid postures.'''
        for p in self.postures.itervalues():
            if p.is_vocoid:
                yield p

    def iter_non_vocoid(self):
        '''Iterate over all non-vocoid postures.'''
        for p in self.postures.itervalues():
            if not p.is_vocoid:
                yield p

    def iter_vcv(self):
        '''Iterate over triples of vowel-consonant-vowel postures.'''
        for p1 in self.iter_vocoid():
            for p2 in self.iter_non_vocoid():
                for p3 in self.iter_vocoid():
                    yield p1, p2, p3

    def iter_cvc(self):
        '''Iterate over triples of consonant-vowel-consonant postures.'''
        for p1 in self.iter_non_vocoid():
            for p2 in self.iter_vocoid():
                for p3 in self.iter_non_vocoid():
                    yield p1, p2, p3

    def create_gaussian(self, *args, **kwargs):
        '''Create a gaussianized version of the postures in this repertoire.'''
        postures = {}
        for s, p in self.postures.iteritems():
            postures[s] = p.create_gaussian(
                self.symbols, self.parameters, *args, **kwargs)
        return Repertoire(parameters=self.parameters,
                          symbols=self.symbols,
                          postures=postures)

    def interpolate(self, control_rate, *symbols):
        '''Given a sequence of posture symbols, produces interpolated control frames.
        '''
        times = []
        postures = []
        for symbol in itertools.chain.from_iterable(symbols):
            posture = self.postures[symbol]
            t = 0.
            if times:
                t = times[-1] + posture.transition
            times.append(t)
            postures.append(posture.targets)
            times.append(times[-1] + posture.duration)
            postures.append(posture.targets)
        frames = int(numpy.ceil(times[-1] * control_rate / 1000.))
        t = numpy.linspace(0, times[-1], frames)
        interpolators = [
            scipy.interpolate.UnivariateSpline(times, p, k=3)
            for p in numpy.array(postures).T]
        return numpy.array([s(t) for s in interpolators]).T
