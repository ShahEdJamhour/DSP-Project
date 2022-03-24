import numpy as np

def encode(string, charsList):
	fs = 8000  # samples per second
	T = 0.04  # sample duration (seconds) =40ms
	n = np.arange(0, fs * T, 1) # create a vector from 0 - 320 and which are samples to give every char 40ms

	encodedString = []
	for i in range(0, len(string)):

		if (string[i].isupper()):
			UpperOrLower = np.cos(2 * np.pi * 200 * n / fs)
		else:
			UpperOrLower = np.cos(2 * np.pi * 100 * n / fs)

		lowerString = string.lower()
		eq = UpperOrLower + np.cos(2 * np.pi * charsList[lowerString[i]]['L'] * n / fs) + np.cos(
			2 * np.pi * charsList[lowerString[i]]['M'] * n / fs) + np.cos(
			2 * np.pi * charsList[lowerString[i]]['H'] * n / fs)

		encodedString = np.concatenate([encodedString,eq ])

	return encodedString
