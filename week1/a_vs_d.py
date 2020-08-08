import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.io import wavfile

# Set up a couple default values
sr  = 44100;    #Samplerate
ch  = 1;     #Number of channels
plt.ioff();
plt.rcParams["figure.figsize"] = (14,4)

def normalize(a_signal):
    '''
    This funcition normalizes the signal and scales it with 100 as max amplitude
    '''
    max_amp     = max(np.absolute([min(a_signal),max(a_signal)]));
    a_signal    = (100.0/max_amp)*a_signal;
    return a_signal

def a_to_d_conv(a_signal):
    ''' 
    This function converts our sort of analog signal to a discrete signal
    Convert the amplitude from floats to rounded off integers
    Normalize by the largest amplitude and then multiply by hundred
    '''
    d_signal = np.round(a_signal);
    return d_signal;

def SNR_calc(noisy,original):
    '''
    FInd RMS error and then ratio of error to the original signal
    '''
    err_norm = np.linalg.norm(original-noisy);
    sig_norm = np.linalg.norm(original);
    return 10*np.log10(sig_norm/err_norm);

def repeater(signal,noise_amp,attenuation,gain):
    '''
        This function is used to mimic the action of a repeater
        - and attenuates the original signal as it passes through wire
        - it adds noise_amp
        - amplifies the entire signal
    '''
    noise   = np.random.uniform(-noise_amp,noise_amp,len(signal));
    noise   = np.array([ (x,) for x in noise]);
    signal  = signal*attenuation;
    signal  = signal + noise;
    return signal*gain;

def digital_rectify(signal):
    '''
        This function is intended to mimic the action of a digital rectifier
        - we use a simple rounding function
        - in practice it will be a threshold function
        - the high frequency low amplitude new can be filtered out 
        - in this case it is the same as the a_to_d_conv funcition
    '''
    return np.round(signal);

def analog_tx(signal,hops,noise_amp,attenuation,gain):
    print("Simulating analog transfer");
    for i in range(0,hops):
        signal = repeater(signal,noise_amp,attenuation,gain);
    return signal;   

    
def digital_tx(signal,hops,noise_amp,attenuation,gain):
    print("Simulating digital_tx transfer");
    for i in range(0,hops):
        signal = repeater(signal,noise_amp,attenuation,gain);
        digital_rectify(signal);
    return signal;   
    

# Record an Audio
duration = int(input("Enter the duration of your recording :: "));
myrec = sd.rec(int(duration*sr),sr,channels=ch)
sd.wait()
print("Finished recording");
sd.playrec(myrec,sr,channels=ch)
sd.wait()
print("Finished original playback");
myrec = normalize(myrec);
print("Normalized recording");

# Display audio
plt.plot(myrec);
plt.show();
print("Closed the Analog plot");

digital_signal = a_to_d_conv(myrec);
print("Converting to Digital signal");
plt.plot(digital_signal);
plt.show();
sd.playrec(digital_signal,sr,channels=ch);
sd.wait()

# Find SNR of digital signal
print("The SNR of the digital signal is :: %f dB"  %( SNR_calc(digital_signal,myrec)));

# Set the transmission parameters
hops,noise_amp,attenuation,gain = input("Enter the \n1. Number of hops in the line \n2. Noise added for each hop \n3. Attenuation for each hop \n4. Gain at each repeater").split();

## Simulate analog transmission

analog_recvd = analog_tx(myrec,int(hops),float(noise_amp),float(attenuation),float(gain));
print("The SNR of the analog signal is :: %f dB"  %( SNR_calc(analog_recvd,myrec)));
sd.playrec(analog_recvd,sr,channels=ch)
sd.wait()
plt.plot(analog_recvd)
plt.show()

## Simulate digital transmission

digital_recvd = digital_tx(myrec,int(hops),float(noise_amp),float(attenuation),float(gain));
print("The SNR of the analog signal is :: %f dB"  %( SNR_calc(digital_recvd,myrec)));
sd.playrec(digital_recvd,sr,channels=ch)
sd.wait()
plt.plot(digital_recvd)
plt.show()


