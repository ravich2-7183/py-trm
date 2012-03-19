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

import logging
import numpy

from xml.dom import minidom

PARAMETERS = ('microInt',
              'glotVol', 'aspVol', 'fricVol',
              'fricPos', 'fricCF', 'fricBW',
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

    def __str__(self):
        return '<Parameter %s: [%s, %s], %s>' % (
            self.name, self.min, self.max, self.default)

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def clip(self, value):
        return max(self.min, min(self.max, value))

    def clip_to_default(self, value):
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

    def __str__(self):
        return '<Posture %s: %s>' % (self.symbol, ', '.join(sorted(self.categories)))

    def __cmp__(self, other):
        return cmp(self.symbol, other.symbol)

    @property
    def targets(self):
        return [self.parameter_targets[n] for n in PARAMETERS]

    @property
    def is_vocoid(self):
        return 'vocoid' in self.categories

    @property
    def is_elongated(self):
        return self.symbol.endswith("'")

    def transition(self, following):
        pts = zip(self.targets, following.targets)
        frames = self.symbol_targets['transition'] + following.symbol_targets['transition']
        return numpy.array([numpy.linspace(a, b, frames // 2) for a, b in pts]).T

    def duration(self):
        pts = zip(self.targets, self.targets)
        frames = self.symbol_targets['duration']
        return numpy.array([numpy.linspace(a, b, frames) for a, b in pts]).T


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

    def __init__(self, xml_file='diphones.mxml'):
        self.parameters = {}
        self.symbols = {}
        self.postures = {}

        if xml_file is not None:
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
