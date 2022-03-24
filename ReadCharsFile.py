###
# this method reads the table of characters frequencies and store them in a set
# of the char itself as a key and the value is a set of 3 frequencies (high,low,medium)
###

def readChars():
	charsList = {}
	chars_file = open('charactersList.txt', "r+")
	for i in range(0, 27):
		line = chars_file.readline()
		ArrayOfChars = line.split(' ')
		charsList[ArrayOfChars[0]] = {'L': int(ArrayOfChars[1]), 'M': int(ArrayOfChars[2]), 'H': int(ArrayOfChars[3])}

	charsList[' '] = charsList.pop('space') # add space char
	return charsList
