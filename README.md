# py-trm

This package is a Python wrapper for the [gnuspeech][] Tube Resonance Model
(TRM).

## Installation

Install with the setup script :

    python setup.py install

Or with pip :

    pip install lmj.trm

## Usage

The primary interface provided by the package is the `lmj.trm.synthesize`
function. This function converts a numpy array containing a sequence of control
parameters into a numpy array containing sound samples, using the functionality
provided by the TRM. Under the covers, the control parameters are serialized
into the data structures used by the gnuspeech code, and the resulting tube
model synthesizes audio samples that are produced by the vocal tract model when
using those control parameters.

The `lmj.trm.TubeModel` class performs the waveguide simulation, and the
`lmj.trm.Parameters` class wraps the tube configuration parameters with some
documentation.

## Gnuspeech wrapper

The gnuspeech C code is copied verbatim from `gnuspeech/Frameworks/Tube/`
(available from [http://svn.savannah.gnu.org/viewvc/osx/trunk/?root=gnuspeech][]),
then swigged to provide a low-level Python wrapper, and finally wrapped again in
a higher-level Python library that integrates numpy and performs memory and data
structure conversions between user code and the wrapped gnuspeech library.

Many, many thanks go to the gnuspeech folks, who have released gnuspeech as open
source and provided a well-written, usable library for acoustic simulation. This
package would not exist without gnuspeech.

[gnuspeech]: http://gnu.org/software/gnuspeech
[http://svn.savannah.gnu.org/viewvc/osx/trunk/?root=gnuspeech]: http://svn.savannah.gnu.org/viewvc/osx/trunk/?root=gnuspeech

**NB**: The code here does not wrap the entire gnuspeech project !!
The TRM is just a small part of the overall project : it is just one of the
boxes in the block diagram on the gnuspeech web site.

## License

### TRM library

All gnuspeech code (everything under the `./gnuspeech` directory) is available
under the terms of the [GNU General Public License][].

[GNU General Public License]: http://gnu.org/copyleft/

## Python

My part of this work (everything under the `./lmj` directory) is available under
the MIT license :

(The MIT License)

Copyright (c) 2010 Leif Johnson <leif@leifjohnson.net>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the 'Software'), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
