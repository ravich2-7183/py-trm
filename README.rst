This package is a Python wrapper for the gnuspeech_ Tube Resonance Model (TRM).

The primary interface provided by the package is the "lmj.trm.synthesize"
function. This function converts a numpy array containing a sequence of control
parameters into a numpy array containing sound samples, using the functionality
provided by the TRM. Under the covers, the control parameters are serialized
into the data structures used by the gnuspeech code, and the resulting tube
model synthesizes audio samples that are produced by the vocal tract model when
using those control parameters.

The gnuspeech C code is copied verbatim from gnuspeech/Frameworks/Tube/
(available from http://svn.savannah.gnu.org/viewvc/osx/trunk/?root=gnuspeech),
then swigged to provide a low-level Python wrapper, and finally wrapped again in
a higher-level Python library that integrates numpy and performs memory and data
structure conversions between user code and the wrapped gnuspeech library.

Many, many thanks go to the gnuspeech folks, who have released gnuspeech as open
source and provided a well-written, extensible library for acoustic speech
synthesis. This package would be completely impossible without gnuspeech.

.. _gnuspeech: http://gnu.org/software/gnuspeech

**Important note**: The code here does not wrap the entire gnuspeech project !!
The TRM is just a small part of the overall project : it is just one of the
boxes in the block diagram on the gnuspeech web site.
