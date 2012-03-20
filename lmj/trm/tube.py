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

'''A high-level wrapper for the gnuspeech Tube Resonance Model (TRM).'''

import array
import itertools
import logging
import os

import gnuspeech


class Parameters(object):
    '''This object holds a number of global synthesis parameters.

    Most parameters describe the configuration of the time-invariant properties
    of the vocal tract: length, temperature, nose and mouth coefficients, gain
    from various portions, nasal passage size, etc.

    A sound is synthesized by combining these parameter settings with a sequence
    of control parameters. See the TubeModel class for information about
    synthesis.
    '''

    DEFAULTS = dict(
        file_format=2,
        sample_rate_hz=44100.,
        control_rate_hz=10.,
        volume_db=10.,
        channels=1,
        balance=0.,
        waveform=gnuspeech.PULSE,
        pulse_rise=40.,
        pulse_fall_min=16.,
        pulse_fall_max=32.,
        breathiness=1.,
        length_cm=17.5,
        temperature_degc=30.,
        loss_factor=0.5,
        aperture_scale_cm=4.,
        mouth_coeff_hz=5000.,
        nose_coeff_hz=5000.,
        nose_radii_cm=5 * (1.5, ),
        throat_lowpass_cutoff_hz=1500.,
        throat_volume_db=5.,
        modulation=1,
        noise_crossmix_offset_db=50.)

    def __init__(self, **kwargs):
        '''Initialize a set of model parameters for a tube synthesizer.'''
        self._params = gnuspeech.TRMInputParameters()
        for attr, default in Parameters.DEFAULTS.items():
            setattr(self, attr, kwargs.get(attr, default))
        extra = set(kwargs) - set(Parameters.DEFAULTS)
        if extra:
            logging.debug('%d extra parameters: %s',
                          len(extra),
                          ', '.join(sorted(extra)))

    def __repr__(self):
        return 'Parameters(\n  %s)' % ',\n  '.join(
            '%s=%s' % (k, getattr(self, k)) for k in sorted(self.DEFAULTS))

    def _set_file_format(self, v): self._params.outputFileFormat = v
    file_format = property(
        lambda self: self._params.outputFileFormat,
        _set_file_format,
        doc='output file format (0=AU, 1=AIFF, 2=WAVE), default 2')

    def _set_sample_rate_hz(self, v): self._params.outputRate = v
    sample_rate_hz = property(
        lambda self: self._params.outputRate,
        _set_sample_rate_hz,
        doc='output sample rate (22050, 44100 Hz), default 44100')

    def _set_control_rate_hz(self, v): self._params.controlRate = v
    control_rate_hz = property(
        lambda self: self._params.controlRate,
        _set_control_rate_hz,
        doc='control rate (1.0-1000.0 input tables/second), default 10.0')

    def _set_volume_db(self, v): self._params.volume = v
    volume_db = property(
        lambda self: self._params.volume,
        _set_volume_db,
        doc='master volume (0-60 dB), default 10.0')

    def _set_channels(self, v): self._params.channels = v
    channels = property(
        lambda self: self._params.channels,
        _set_channels,
        doc='output channels (1 or 2), default 1')

    def _set_balance(self, v): self._params.balance = v
    balance = property(
        lambda self: self._params.balance,
        _set_balance,
        doc='stereo balance (-1 to +1), default 0.0')

    def _set_waveform(self, v): self._params.waveform = v
    waveform = property(
        lambda self: self._params.waveform,
        _set_waveform,
        doc='glottal source waveform type (0=PULSE, 1=SINE), default 0')

    def _set_pulse_rise(self, v): self._params.tp = v
    pulse_rise = property(
        lambda self: self._params.tp,
        _set_pulse_rise,
        doc='glottal pulse rise (5-50 % of GP period), default 40.0')

    def _set_pulse_fall_min(self, v): self._params.tnMin = v
    pulse_fall_min = property(
        lambda self: self._params.tnMin,
        _set_pulse_fall_min,
        doc='glottal pulse fall minimum (5-50 % of GP period), default 16.0')

    def _set_pulse_fall_max(self, v): self._params.tnMax = v
    pulse_fall_max = property(
        lambda self: self._params.tnMax,
        _set_pulse_fall_max,
        doc='glottal pulse fall maximum (5-50 % of GP period), default 32.0')

    def _set_breathiness(self, v): self._params.breathiness = v
    breathiness = property(
        lambda self: self._params.breathiness,
        _set_breathiness,
        doc='glottal source breathiness (0-10 % of GP amplitude), default 1.0')

    def _set_length_cm(self, v): self._params.length = v
    length_cm = property(
        lambda self: self._params.length,
        _set_length_cm,
        doc='nominal tube length (10-20 cm), default 17.5')

    def _set_temperature_degc(self, v): self._params.temperature = v
    temperature_degc = property(
        lambda self: self._params.temperature,
        _set_temperature_degc,
        doc='tube temperature (25-40 C), default 30.0')

    def _set_loss_factor(self, v): self._params.lossFactor = v
    loss_factor = property(
        lambda self: self._params.lossFactor,
        _set_loss_factor,
        doc='junction loss factor (0-5 % unity gain), default 0.5')

    def _set_aperture_scale_cm(self, v): self._params.apScale = v
    aperture_scale_cm = property(
        lambda self: self._params.apScale,
        _set_aperture_scale_cm,
        doc='aperture scale radius (3.05-12 cm), default 4.0')

    def _set_mouth_coeff_hz(self, v): self._params.mouthCoef = v
    mouth_coeff_hz = property(
        lambda self: self._params.mouthCoef,
        _set_mouth_coeff_hz,
        doc='mouth aperture coefficient (100-nyquist Hz), default 5000.0')

    def _set_nose_coeff_hz(self, v): self._params.noseCoef = v
    nose_coeff_hz = property(
        lambda self: self._params.noseCoef,
        _set_nose_coeff_hz,
        doc='nose aperture coefficient (100-nyquist Hz), default 5000.0')

    def _get_nose_radii(self):
        return tuple(
            gnuspeech.double_array_getitem(self._params.noseRadius, i)
            for i in range(1, gnuspeech.TOTAL_NASAL_SECTIONS))

    def _set_nose_radii(self, values):
        assert len(values) == gnuspeech.TOTAL_NASAL_SECTIONS - 1
        radii = gnuspeech.new_double_array(gnuspeech.TOTAL_NASAL_SECTIONS)
        gnuspeech.double_array_setitem(radii, 0, 0.)
        for i, v in enumerate(values):
            gnuspeech.double_array_setitem(radii, i + 1, v)
        self._params.noseRadius = radii
        gnuspeech.delete_double_array(radii)

    nose_radii_cm = property(
        _get_nose_radii,
        _set_nose_radii,
        doc='fixed nose radii (6 values from 0-3 cm), default (1.5, ) * 6')

    def _set_throat_lowpass_cutoff_hz(self, v): self._params.throatCutoff = v
    throat_lowpass_cutoff_hz = property(
        lambda self: self._params.throatCutoff,
        _set_throat_lowpass_cutoff_hz,
        doc='throat low-pass cutoff (50-nyquist Hz), default 1500.0')

    def _set_throat_volume_db(self, v): self._params.throatVol = v
    throat_volume_db = property(
        lambda self: self._params.throatVol,
        _set_throat_volume_db,
        doc='throat volume (0-48 dB), default 5.0')

    def _set_modulation(self, v): self._params.modulation = v
    modulation = property(
        lambda self: self._params.modulation,
        _set_modulation,
        doc='pulse modulation of noise (0=OFF, 1=ON), default 1')

    def _set_noise_crossmix_offset_db(self, v): self._params.mixOffset = v
    noise_crossmix_offset_db = property(
        lambda self: self._params.mixOffset,
        _set_noise_crossmix_offset_db,
        doc='noise crossmix offset (30-60 dB), default 50.0')


class TubeModel(object):
    '''A Tube Resonance Model (TRM) synthesizes sound from a vocal tract model.

    The vocal tract model is parameterized by a set of static parameters, plus a
    number of frames of control parameters. The static parameters are
    encapsulated in the Parameters class, while the frame data is provided as an
    argument to the synthesize method of this class.
    '''

    def __init__(self, parameters):
        '''Initialize this tube model with static tube configuration parameters.
        '''
        self._model = gnuspeech.TRMTubeModelCreate(parameters._params)
        self._parameters = parameters

    def __del__(self):
        '''Free up the memory for this tube model.'''
        gnuspeech.TRMTubeModelFree(self._model)

    def synthesize(self, *controls):
        '''Synthesize a sound from the given control variables.

        Controls is expected to be a list or numpy array containing controls for
        each frame of the sound synthesis. If it is a numpy array, frames are
        read from the 0 axis (the "rows") of the array.

        The variables for each frame, in order, are:

        glotPitch - glottal pitch, 0 == middle C
        glotVol - glottal volume, dB
        aspVol - aspirate volume, dB
        fricVol - fricative volume, dB
        fricPos - fricative position, cm
        fricCF - fricative filter center frequency, Hz
        fricBW - fricative filter bandwidth, Hz
        radius[0] - radius of vocal tract, region 0, cm
        ...
        radius[7] - radius of vocal tract, region 7, cm
        velum - radius of velar opening, cm
        '''
        # convert control frames into TRM linked list structure
        data = gnuspeech.TRMData()
        data.inputParameters = self._parameters._params

        radii = gnuspeech.new_double_array(gnuspeech.TOTAL_REGIONS)
        for frame in itertools.chain.from_iterable(controls):
            glot_pitch, glot_vol, asp_vol, fric_vol, fric_pos, fric_cf, fric_bw = frame[:7]
            for i, v in enumerate(frame[7:15]):
                gnuspeech.double_array_setitem(radii, i, v)
            velum = frame[15]
            gnuspeech.addInput(data, glot_pitch, glot_vol, asp_vol,
                               fric_vol, fric_pos, fric_cf, fric_bw,
                               radii, velum)
        gnuspeech.delete_double_array(radii)

        # run the synthesizer
        gnuspeech.synthesize(self._model, data)

        # now return the synthesized sound data as an array of doubles
        converter = self._model.sampleRateConverter
        converter.tempFilePtr.seek(0)
	logging.debug('number of samples: %d', converter.numberSamples)
	logging.debug('maximum sample value: %.4f', converter.maximumSampleValue)
        arr = array.array('d')
        arr.fromstring(converter.tempFilePtr.read())
        return arr


def parse_input_file(filename):
    '''Parse a control file and return the parameter and control data.'''
    assert os.path.exists(filename), '%s: file does not exist' % filename
    return gnuspeech.parseInputFile(filename)


def synthesize(input_filename, output_filename):
    '''Synthesize the control data from input_filename into output_filename.'''
    frames = parse_input_file(input_filename)
    t = gnuspeech.TRMTubeModelCreate(frames.inputParameters)
    logging.info('Calculating floating point samples...')
    gnuspeech.synthesize(t, frames)
    gnuspeech.writeOutputToFile(t.sampleRateConverter, frames, output_filename)
    logging.info('Wrote scaled samples to file: %s', output_filename)
    gnuspeech.TRMTubeModelFree(t)
