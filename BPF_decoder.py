import numpy as np
from scipy.signal import butter, lfilter
from scipy.fft import fft



#  lowcut(float): the low cutoff frequency of the filter.
#  highcut(float): the high cutoff frequency of the filter.
#  fs(float): then sampling rate.
#  order(int): order of the filter, by default defined to 5.

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs   # calculate the Nyquist frequency
    low = lowcut / nyq	# design filter
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a  # returns the filter coefficients: numerator and denominator

# Filter a data sequence, using a digital filter. This works for many fundamental
# data types (including Object type). The filter is a direct form II transposed
# implementation of the standard difference equation.
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y



# freq to check are:100 200 400 600 800 1000 1200 1600 2000 2400 4000
def check_freq(data, center, start, end):

	if (center <300):
		lowcut = center - 50
		highcut = center + 50

	elif (center <=1200):
		lowcut = center - 100
		highcut = center + 100

	else:
		lowcut = center - 200
		highcut = center + 200

	fs = 8000.0
	x = data[start:end] # the 320 sample that represents the 40ms for each char in string
	y = butter_bandpass_filter(x, lowcut, highcut, fs, order=5) # pass data to filter to check frequencies
	z = np.array(y)
	yf = fft(z, 256)
	yf = abs(yf[0:128]);  # take the magnitude of the spectrum impulses then just take half of
	# them Because of the Similarity between the ranges  [0,pi/2] & [pi/2,pi]
	index = int((center * 2 * 128) / 8000)
	if (pow(yf[index],2) > 200):   # if freq passes throw filter
		return True
	return False


def decode_by_BPF(string_data,chars,fs,T ,frequencies):
	samples_length = len(string_data)
	step = int(fs * T)  # 320 sample per char
	start = 0
	end = step
	decoded_string = ''
	number_of_chars = int(samples_length / step)
	for c in range(0, number_of_chars):
		existFreqs = []
		for f in frequencies:
			if check_freq (string_data,f,start,end):
				existFreqs.append(f)
		start += step
		end += step
		existFreqs.sort()

		# ------------------------------------------
		for c, f in chars.items():
			tempF = []
			for t in f:
				tempF.append(f[t])
			tempF.sort()
			if (len(set(existFreqs)) == 3):
				existFreqs.append(4000)

			if (tempF[0] == existFreqs[1] and tempF[1] == existFreqs[2] and tempF[2] == existFreqs[3]):
				if existFreqs[0] == 200:
					decoded_string += c.upper()

				else:
					decoded_string += c

	return decoded_string

