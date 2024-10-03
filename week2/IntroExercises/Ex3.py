def shift_by_one(word):
	newWord = ""
	for i in word:
		ascii = ord(i)
		newWord += chr(ascii+1)
	return newWord

print(shift_by_one("Hello"))
