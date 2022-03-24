from Encoder import *
from scipy.io import wavfile
import scipy
from ReadCharsFile import *
from BPF_decoder import *
from FFT_decoder import *

chars = readChars()
String = "abcdefghijklmnopqrstuvwxz ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#String = "AbDEghJknm m MMMMC"
Fs = 8000
T = 0.04
y = encode(String, readChars())
scipy.io.wavfile.write("string_0.wav",Fs , y)
s_rate,signal = wavfile.read("string_0.wav")
freq = [100,200,400,600,800,1000,1200,1600,2000,2400,4000]

chars = readChars()
print(decode_fft(signal,chars,s_rate,freq))
print(decode_by_BPF(signal,chars,s_rate,T,freq[:10]))
