# Digital vs Analog Signals

A digital signal can be created from any signal by sampling and thresholding. This causes
a small loss in information but as long as we the use the nyquist theorem to find an 
appropriate sampling rate we can provide the illusion of an almost exact replica of the 
original signal.

But why do we use such a method if it incurs any sort of loss of information at all.

## Benefits of Digital

As communication technologies found widespread use in society it is only natural that 
people demanded long distance communication. For long distance communication noise and 
attenuation becomes a major problem.

The problem of attenuation is solve by using one or more repeaters along the path of 
transmission, these repeaters do nothing but repeat the signal amplifying it to compensate
for attenuation. But when using analog signals it introduces the problem of amplifying the 
noise as well. The noise being added on each hop and getting amplified each time might even
overpower the original signal. This leads to a detriment in SNR.

This is where digital comes in, the levels of the signal are restricted to certain discrete
values, in digital signals there generally are only two possible values i.e binary. The signal
voltage values are assigned threshold value over and above which the signal will be assigned 
as a 0 or 1. This way at each step in the repeater we can recover the signal and reduce the noise.
The noise is hence not cascaded. This leads to an improvement in SNR as long as the max noise
remains within a critical limit after this limit the noise can completely obfuscate the original
signal with no way to regenerate it.

## The demo
The demo uses the following libraries in python and uses python3
* scipy
* numpy
* matplotlib
* sounddevice

All the above modules can be install using the `pip3` installer. Simply run `python3 a_vs_d.py`.
And follow instruction given by the command line prompt.
