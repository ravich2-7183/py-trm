#!/usr/bin/env python

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

import numpy
import logging
import subprocess
import numpy.random as rng

from scikits.audiolab import play

import lmj.trm


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    p = lmj.trm.Parameters(
        file_format=0,
        sample_rate_hz=22050.,
        control_rate_hz=25.,
        volume_db=60.,
        channels=1,
        balance=0.,
        waveform=0,
        pulse_rise=40.,
        pulse_fall_min=16.,
        pulse_fall_max=32.,
        breathiness=1.,
        length_cm=17.5,
        temperature_degc=25.,
        loss_factor=0.5,
        aperture_scale_cm=3.05,
        mouth_coeff_hz=5000.,
        nose_coeff_hz=5000.,
        nose_radii_cm=(1.35, 1.96, 1.91, 1.3, 0.73),
        throat_lowpass_cutoff_hz=1500.,
        throat_volume_db=6.,
        modulation=1,
        noise_crossmix_offset_db=54.)
    print p

    m = lmj.trm.TubeModel(p)
    f = m.synthesize([
        [-12, -0.120652, -0.0131552, 0.000148631, 3.02425, 1390.1, 279.381, 0.440155, 0.497409, 0.554558, 0.454035, 0.42397, 0.555063, 0.681276, 0.034265, 0.0631023],
        [-12, 0.11304, 0.0108587, -0.000148243, 5.98451, 2702.21, 539.201, 0.870217, 0.955787, 1.06148, 0.868119, 0.817728, 1.17695, 1.33037, -0.0329175, 0.0960169],
        [-12, -0.219, -0.00806997, 0.000148577, 5.24192, 2403.43, 481.751, 0.762705, 0.893061, 0.997703, 0.81865, 0.752644, 0.888064, 1.19738, 0.154064, 0.139161],
        [-12, 2.56921, 0.00476418, -0.000150234, 5.66998, 2553.68, 509.908, 0.824499, 1.31988, 1.49874, 1.25736, 1.0098, 0.132359, 1.46507, 1.24856, 0.484619],
        [-12, 42.8582, -0.000919793, 0.000154038, 5.37747, 2470.88, 494.689, 0.782377, 1.29215, 1.47123, 1.23242, 0.98917, 0.01115, 1.41995, 1.32511, 0.502091],
        [-12, 61.8157, -0.00348068, -0.000161157, 5.59239, 2512.3, 502.342, 0.813273, 1.32652, 1.50751, 1.26905, 1.00542, 0.0809808, 1.44935, 1.3009, 0.498921],
        [-12, 58.612, 0.0084501, 0.000173331, 5.42872, 2500.59, 499.739, 0.789756, 1.31794, 1.50091, 1.27792, 0.975147, 0.0380858, 1.38348, 1.3284, 0.501083],
        [-12, 61.1312, -0.0139959, -0.000193278, 5.55552, 2488.76, 498.743, 0.808002, 1.52833, 1.74339, 1.69047, 0.787496, 0.210969, 0.94663, 1.40673, 0.495633],
        [-12, 58.989, 0.0201195, 0.000225514, 5.45673, 2520.53, 502.366, 0.793718, 1.65943, 1.89795, 1.97259, 0.633019, 0.268894, 0.585621, 1.49406, 0.399062],
        [-12, 60.9543, -0.0268146, -0.000278089, 5.53348, 2470.96, 496.849, 0.804933, 1.66619, 1.90554, 1.98008, 0.638929, 0.299966, 0.603338, 1.48059, 0.262913],
        [-12, 59.0656, 0.0340664, 0.000366624, 5.47446, 2537.2, 503.651, 0.796131, 1.69068, 1.87597, 1.88703, 0.65526, 0.360483, 0.640871, 1.42392, 0.239105],
        [-12, 60.9421, -0.0418488, -0.000525042, 5.51903, 2454.5, 496.108, 0.803033, 1.75847, 1.73168, 1.46509, 0.779415, 0.690055, 0.95939, 1.13208, 0.191942],
        [-12, 59.0207, 0.0501209, 0.000840648, 5.48635, 2554.66, 503.88, 0.79761, 1.83648, 1.58787, 1.03476, 0.896911, 0.996907, 1.24554, 0.845971, 0.148589],
        [-12, 61.0691, -0.0588209, -0.00162663, 5.50909, 2433.82, 496.385, 0.801913, 1.90018, 1.45739, 0.653615, 1.00535, 1.29864, 1.52989, 0.585408, 0.104115],
        [-12, 58.398, 0.0678559, 0.00801878, 5.49513, 2584.1, 503.088, 0.798411, 1.90384, 1.44329, 0.612329, 1.01709, 1.30643, 1.5384, 0.560051, 0.102344],
        [-12, 58.1282, -0.0770835, 0.0391217, 5.49927, 2374.82, 497.716, 0.801403, 1.88149, 1.43979, 0.625468, 1.01567, 1.28775, 1.51369, 0.586579, 0.0976503],
        [-12, 43.657, 0.0862755, 0.201883, 5.52524, 2865.47, 501.169, 0.798652, 1.75618, 1.45495, 0.770813, 0.987832, 1.03016, 1.25533, 0.740417, 0.102236],
        [-12, 10.3548, -0.0950456, 0.680794, 5.79356, 5315.03, 500.314, 0.801417, 1.40392, 1.48089, 1.14573, 0.919835, 0.385726, 0.587562, 1.20079, 0.0979321],
        [-12, -0.394881, 0.102688, 0.780489, 5.79459, 5594.09, 497.703, 0.798394, 1.31567, 1.48965, 1.24365, 0.900246, 0.203358, 0.406455, 1.2852, 0.101868],
        [-12, 1.30799, -0.107779, 0.822941, 5.81101, 5389.04, 505.148, 0.80191, 1.31808, 1.49677, 1.26002, 0.900181, 0.215266, 0.413344, 1.2873, 0.0983526],
        [-12, -1.52704, 0.107008, 0.668792, 5.77274, 5679.06, 489.624, 0.797668, 1.34557, 1.53307, 1.32862, 0.8885, 0.221463, 0.42741, 0.784301, 0.101409],
        [-12, 2.02356, -0.090766, -0.0265786, 6.19917, 4187.48, 575.678, 0.802868, 1.42662, 1.62262, 1.48196, 0.874043, 0.302706, 0.511677, 0.0893865, 0.0988436],
        [-12, -3.41672, 0.0162316, 0.0680242, 7.12928, 1914.69, 707.314, 0.796474, 1.50667, 1.71846, 1.65847, 0.846687, 0.354325, 0.575671, 0.140095, 0.100891],
        [-12, 16.0217, 2.36331, 0.151462, 6.2577, 2295.98, 614.831, 0.80431, 1.60145, 1.8245, 1.8373, 0.832248, 0.444953, 0.671848, 0.664881, 0.0993871],
        [-12, 55.8366, 0.591923, -0.02722, 5.34712, 2513.69, 460.645, 0.794764, 1.64483, 1.87722, 1.94201, 0.80983, 0.469025, 0.701948, 1.36649, 0.100323],
        [-12, 58.5214, -0.448925, 0.013885, 5.60332, 2498.36, 539.471, 0.806323, 1.6737, 1.90901, 1.98537, 0.817279, 0.501886, 0.740232, 1.45146, 0.0999809],
        [-12, 59.9655, 0.438486, -0.00911093, 5.40836, 2497.41, 452.571, 0.792391, 1.64345, 1.88704, 1.97305, 0.810446, 0.454063, 0.720752, 1.4588, 0.0996983],
        [-12, 49.3266, -0.465215, 0.00669799, 5.59228, 2506.42, 562.858, 0.809152, 1.60705, 1.87666, 1.96538, 0.849748, 0.391025, 0.759315, 1.30988, 0.100646],
        [-12, 18.1282, 0.520405, -0.00501896, 5.39967, 2488.55, 406.339, 0.78894, 1.4451, 1.77875, 1.89589, 0.887862, 0.141397, 0.75315, 1.01718, 0.0989738],
        [-12, 2.22709, -0.615666, 0.0025473, 5.64094, 2518.53, 1187.9, 0.813524, 1.40047, 1.77117, 1.89445, 0.943704, 0.0548771, 0.806182, 0.839183, 0.101466],
        [-12, 0.733967, 0.793145, 0.0172693, 5.45811, 2471.1, 2316.01, 0.78307, 1.34412, 1.72004, 1.85292, 0.921577, -0.00849037, 0.762973, 0.802398, 0.0979881],
        [-12, -0.201343, -1.21956, 0.164671, 5.77113, 2545.27, 2798.41, 0.822155, 1.35851, 1.7255, 1.83304, 0.951667, 0.0887088, 0.849571, 0.742676, 0.102774],
        [-12, 0.0790298, 4.48401, 0.144665, 5.31437, 2424.68, 1322.22, 0.768336, 1.22142, 1.53669, 1.60628, 0.870119, 0.188809, 0.836472, 0.620848, 0.0959391]
        ])
    w = numpy.array(f)
    w /= abs(w).max()
    play(w, 22050)

    for target in 'music oi'.split():
        print 'synthesizing %s.gnuspeech' % target
        lmj.trm.synthesize(target + '.gnuspeech', target + '.wav')
        subprocess.call(['aplay', target + '.wav'])
