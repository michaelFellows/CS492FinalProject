def crackHash(hashToCrack):
        with open("15-Million-Passwords.txt") as words:
                listOfPasswords = words.read().splitlines()
        with open("15-Million-Hashes.txt") as hashes:
                listOfHashes = hashes.read().splitlines()
        try:
                passwordIndex = listOfHashes.index(hashToCrack)
                return [True, listOfPasswords[passwordIndex]]
        except:
                return [False, ("Password not found in list of " + str(len(listOfPasswords)) + " passwords.")]