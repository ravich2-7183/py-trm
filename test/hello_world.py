#!/usr/bin/env python

import numpy
import scikits.audiolab
import lmj.trm

def play_frames(frames, fixed_params):
    tube_model = lmj.trm.TubeModel(fixed_params)
    out = numpy.array(tube_model.synthesize(frames))
    out /= abs(out).max()
    scikits.audiolab.play(out, fixed_params.sample_rate_hz)

adult_params = lmj.trm.Parameters(
    file_format              = 0,
    sample_rate_hz           = 22050.,
    control_rate_hz          = 25.,
    volume_db                = 60.,
    channels                 = 1,
    balance                  = 0.,
    waveform                 = 0,
    pulse_rise               = 40.,
    pulse_fall_min           = 16.,
    pulse_fall_max           = 32.,
    breathiness              = 1.,
    length_cm                = 17.5,
    temperature_degc         = 25.,
    loss_factor              = 0.5,
    aperture_scale_cm        = 3.05,
    mouth_coeff_hz           = 5000.,
    nose_coeff_hz            = 5000.,
    nose_radii_cm            = (1.35, 1.96, 1.91, 1.3, 0.73),
    throat_lowpass_cutoff_hz = 1500.,
    throat_volume_db         = 6.,
    modulation               = 1,
    noise_crossmix_offset_db = 54.)

child_params = lmj.trm.Parameters(
    file_format              = 0,                             
    sample_rate_hz           = 22050.0,
    control_rate_hz          = 8.,
    volume_db                = 60.0,                          
    channels                 = 1,                             
    balance                  = 0.0,                           
    waveform                 = 0,                             
    pulse_rise               = 40.0,                          
    pulse_fall_min           = 22.0,                          
    pulse_fall_max           = 45.0,                          
    breathiness              = 2.50,                          
    length_cm                = 10.0,                          
    temperature_degc         = 32.,                           
    loss_factor              = 1.00,                          
    aperture_scale_cm        = 3.05,                          
    mouth_coeff_hz           = 5000.0,                        
    nose_coeff_hz            = 5000.0,                        
    nose_radii_cm            = (1.35, 1.96, 1.91, 1.3, 0.73), 
    throat_lowpass_cutoff_hz = 1500.0,
    throat_volume_db         = 6.0,                           
    modulation               = 1,                             
    noise_crossmix_offset_db = 48.0)

example_frames = [[10.0, 0.0, 0.0, 0.0, 4.0, 4400, 600, 0.8, 0.8, 0.4, 0.4, 1.78, 1.78, 1.26, 0.8, 0.0], 
                  [9.5, 54.0, 0.0, 0.0, 4.0, 4400, 600, 0.8, 0.8, 0.4, 0.4, 1.78, 1.78, 1.26, 0.8, 0.0], 
                  [9.0, 60.0, 0.0, 0.0, 4.0, 4400, 600, 0.8, 0.8, 0.6, 0.6, 1.58, 1.58, 1.13, 1.01, 0.1], 
                  [8.5, 60.0, 0.0, 0.0, 4.0, 4450, 550, 0.8, 0.8, 1.28, 1.28, 1.0, 1.0, 1.0, 0.8, 1.0], 
                  [8.0, 54.0, 0.0, 0.0, 4.0, 4500, 500, 0.8, 0.8, 1.68, 1.58, 0.8, 0.8, 0.5, 0.4, 1.0], 
                  [7.0, 51.0, 0.0, 0.0, 4.0, 4500, 500, 0.8, 0.8, 1.78, 1.78, 0.2, 0.2, 0.4, 0.0, 1.0]]

if __name__ == '__main__':
    play_frames(example_frames, child_params) # sounds like a child saying "one"
    
    # loads all the postures in the default repertoire, gnuspeech/Monet/diphones.mxml
    repertoire = lmj.trm.Repertoire()
    
    # for a full list of posture symbols see repertoire.postures
    posture_symbols = ['#', 'h', 'e', 'l', 'uh', 'uu', '^', 'w','er','r','ll','d', '#']
    
    # voice quality is very bad, wonder what is going wrong?
    play_frames(repertoire.interpolate(child_params.control_rate_hz, *posture_symbols), child_params)
    play_frames(repertoire.interpolate(adult_params.control_rate_hz, *posture_symbols), adult_params)
