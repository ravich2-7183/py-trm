import glob
import setuptools

setuptools.setup(
    name='lmj.trm',
    version='0.1',
    namespace_packages=['lmj'],
    packages=setuptools.find_packages(),
    ext_modules=[setuptools.Extension(
            'lmj.trm._gnuspeech',
            sources=glob.glob('gnuspeech/Tube/*.c') + ['lmj/trm/gnuspeech_wrap.c'],
            include_dirs=['./gnuspeech'],
            define_macros=[('GNUSTEP', '1')])],
    author='Leif Johnson',
    author_email='leif@leifjohnson.net',
    description='Python bindings for the gnuspeech tube resonance model',
    long_description=open('README.rst').read(),
    license='MIT',
    keywords=('speech-synthesis '
              'gnuspeech '
              'tube-resonance-model'),
    url='http://github.com/lmjohns3/py-trm',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        ],
    )
