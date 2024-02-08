import sys, math

EN_SYMBOLS	= "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?@#$%^&*()'\"_+-=[]{}/|\:;.,"

UA_SYMBOLS = "А а, Б б, В в, Г г, Ґ ґ, Д д, Е е, Є є, Ж ж, З з, И и, І і, Ї ї, Й й, К к, Л л, М м, Н н, О о, П п, Р р, С с, Т т, У у, Ф ф, Х х, Ц ц, Ч ч, Ш ш, Щ щ, ь, Ю ю, Я я !?@#$%^&*()'\"_+-=[]{}/|\:;.,"

def main():
	filename = 'encrypted_file.txt'
	mode = 'decrypt' # encrypt or decrypt
	
	if mode == 'encrypt':
		message = "формально не входить до української абетки, відображає твердість звучання попереднього приголосного перед йотованими і є обов'язковим до використання. "
		pubKeyFilename = 'al_sweigart_pubkey.txt'
		print('Encrypting and writing to %s...' % (filename))
		encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)
		
		print('Encrypted text:')
		print(encryptedText)
		
	elif mode == 'decrypt':
		privKeyFilename = 'al_sweigart_privkey.txt'
		encryptedBlocks = []
		print('Reading from %s and decrypting...' % (filename))
		decryptedText = readFromFileAndDecrypt(encryptedBlocks, filename, privKeyFilename)
		
		print('Decrypted text:')
		print(decryptedText)

def getBlockFromText(message, blockSize):
	for character in message:
		if character not in UA_SYMBOLS:
			print('ERROR: The symbol set does not have the character %s' % (character))
			sys.exit()
	blockInts = []
	for blockStart in range(0, len(message), blockSize):
		blockInt = 0
		for i in range(blockStart, min(blockStart + blockSize, len(message))):
			blockInt += (UA_SYMBOLS.index(message[i])) * (len(UA_SYMBOLS) **
			(i % blockSize))
		blockInts.append(blockInt)
	return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize):
	message = []
	for blockInt in blockInts:
		blockMessage = []
		for i in range(blockSize -1, -1, -1):
			if len(message) + i < int(messageLength):
				charIndex = blockInt // (len(UA_SYMBOLS) ** i)
				blockInt = blockInt % (len(UA_SYMBOLS) ** i)
				blockMessage.insert(0, UA_SYMBOLS[charIndex])
		message.extend(blockMessage)
	return ''.join(message)


def encryptMessage(message, key, blockSize):
	encryptedBlocks = []
	n, e = key
	
	for block in getBlockFromText(message, blockSize):
		encryptedBlocks.append(pow(block, e, n))
	return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize):
	decryptedBlocks = []
	n, d = key
	for block in encryptedBlocks:
		decryptedBlocks.append(pow(block, d, n))
	return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
	fo = open(keyFilename)
	content = fo.read()
	fo.close()
	keySize, n, EorD = content.split(',')
	return (int(keySize), int(n), int(EorD))


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=None):
	keySize, n, e = readKeyFile(keyFilename)
	if blockSize == None:
		blockSize = int(math.log(2 ** keySize, len(UA_SYMBOLS)))
	if not (math.log(2 ** keySize, len(UA_SYMBOLS)) >= blockSize):
		sys.exit('ERROR: Block size is too large for the key and symbol set size. Did you specify the correct key file and encrypted file?')
	
	encryptedBlocks = encryptMessage(message, (n, e),  blockSize)

	for i in range(len(encryptedBlocks)):
		encryptedBlocks[i] = str(encryptedBlocks[i])
	encryptedContent = ','.join(encryptedBlocks)

	encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
	fo = open(messageFilename, 'w')
	fo.write(encryptedContent)
	fo.close()
	return encryptedContent


def readFromFileAndDecrypt(encryptedBlocks , messageFilename, keyFilename):
	keySize, n, d = readKeyFile(keyFilename)
	fo = open(messageFilename)
	content = fo.read()
	messageLength, blockSize, encryptedMessage = content.split('_')
	blockSize = int(blockSize)

	if not (math.log(2 ** keySize, len(UA_SYMBOLS)) >= blockSize):
		sys.exit('ERROR: Block size is too large for the key and symbol set size.Did you specify the correct key file and encrypted file?')
	
	for block in encryptedMessage.split(','):
		encryptedBlocks.append(int(block))

	return decryptMessage(encryptedBlocks, messageLength, (n, d),
		blockSize)


if __name__ == '__main__':
	main()







