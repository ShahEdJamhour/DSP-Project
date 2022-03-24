import numpy as np
from scipy.fft import fft

# this method takes an array and a value then it returns the nearest
# element of the array to this special value
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def decode_fft(string_data,list_of_chars,fs,list_of_freqs):
    samples_length = len(string_data)
    T = 0.04               # 40ms for each char
    step = int(fs * T)     # 320 sample per char
    start = 0
    end = step
    decoded_string = ''
    number_of_chars = int(samples_length / step)
    for c in range(0, number_of_chars):
        char_string = string_data [start : end]
        char_freqs = fft ( char_string , 256 )   # take the Fourier transform of char_string to find freq w
        char_freqs = abs(char_freqs[0:128]);  # take the magnitude of the spectrum impulses then just take half of
                                              # them Because of the Similarity between the ranges  [0,pi/2] & [pi/2,pi]

        max_four_freq = np.argpartition(char_freqs, -4)[-4:] # get the  indices of 4 max peaks
        max_four_freq = max_four_freq * int(fs / (2 * 128)) # convert w to f

        start += step
        end += step
        freq=[]
        for i in range( 0, int( len(max_four_freq) ) ):   # round the frequencies to the nearest one of the given freqs
            if (max_four_freq[i] == 3069):
                freq.append(4000)
            else:
                freq.append(find_nearest(list_of_freqs, max_four_freq[i]))
        if (len(set(freq))==3):  # if there is repeated freq for some reason related to the high frequency 4000 then:
            freq = set(freq)     # convert it to set to remove the repeated one
            freq = list(freq)    # return it to array
            freq.append(4000)    # add 4000

        freq.sort()
        # ------------------------------------------
        for c, f in  list_of_chars.items():
            tempF = []
            for t in f:
                tempF.append(f[t])  #tempF contains freq of char
            tempF.sort()
            if (tempF[0] == freq[1] and tempF[1] == freq[2] and tempF[2] == freq[3]):
                if freq[0] == 200: #if it has the freq 200 then it upper case
                    decoded_string += c.upper()
                else:
                    decoded_string += c

    return decoded_string