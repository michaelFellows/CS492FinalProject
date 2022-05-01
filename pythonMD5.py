def MD5Hasher(password):
    # Key values for each round
    K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
         0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
         0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
         0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
         0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
         0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
         0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
         0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
         0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
         0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
         0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
         0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
         0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
         0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
         0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
         0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]

    # Shift amounts for each round
    s = [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22, 
         5, 9,14,20,5, 9,14,20,5, 9,14,20,5, 9,14,20, 
         4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
         6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]

    # Initial 32-bit values for each quarter of the hash (little endian)
    a0 = 0x67452301   
    b0 = 0xefcdab89   
    c0 = 0x98badcfe   
    d0 = 0x10325476

    # -------------------------------------PADDING STAGE-------------------------------------
    # Convert password to bytes
    passwordAsBytes = bytes(password, "utf-8")
    originalBitLengthOfPassword = len(passwordAsBytes)*8

    # Append 0x80 to the message
    passwordAsBytes = passwordAsBytes + b'\x80'     

    # Pad with 0x00 until message length is === 448mod(512)
    lenDataInBinary = len(passwordAsBytes)*8        
    for i in range(0,int((448-lenDataInBinary%512)/8)):     
        passwordAsBytes = passwordAsBytes + b'\x00'

    # Get original length of password in bytes (the actual length)
    originalLengthInBytes = originalBitLengthOfPassword.to_bytes(8, byteorder='little')
    
    # Append original length of password to the end of passwordAsBytes
    passwordAsBytes = passwordAsBytes + originalLengthInBytes 


    # -----------------------------ROUND FUNCTION FOR EACH CHUNK-----------------------------
    
    numOfChunks = int((len(passwordAsBytes)*8)/512)     # Calculate number of 512-bit chunks
    for i in range(0,numOfChunks):
        A = a0
        B = b0
        C = c0
        D = d0
        # break chunk into sixteen 32-bit words M[j], 0 ≤ j ≤ 15
        startIndex = i*64
        endIndex = (i+1)*64
        currentChunk = passwordAsBytes[startIndex:endIndex]
        # Array that will store 16, 32-bit Ints of currentChunk
        M = [] 
        for chunkIndex in range(0,16):
            chunkString = currentChunk[chunkIndex*4:(chunkIndex+1)*4]
            chunkStringAsInt = int.from_bytes(chunkString, byteorder='little')
            M.append(chunkStringAsInt)
        for i in range(0,64):
            if(0<=i<=15):       # For rounds 0 to 15
                F = (B&C)|((~B)&D)
                g = i
            elif(16<=i<=31):    # For rounds 16 to 31
                F = (D&B)|((~D)&C)
                g = (5*i + 1)%16
            elif(32<=i<=47):    # For rounds 32 to 47
                F = B^C^D
                g = (3*i + 5)%16
            elif(48<=i<=63):    # For rounds 48 to 63
                F = C ^ (B | (~D))
                g = (7*i)%16      
            F = F + A + K[i] + M[g] 
            A = D
            D = C
            C = B
            # Doing the circular leftRotate
            F = F%(2**32)
            leftRotate = (F<<s[i]) | F>>(32-s[i])
            B = B + leftRotate
        # Add this chunk's hash to result so far:
        a0 = a0 + A
        b0 = b0 + B
        c0 = c0 + C
        d0 = d0 + D
    listOfSectionsOfHash = [a0,b0,c0,d0]
    finalHash = ""
    for section in listOfSectionsOfHash:
        section = hex(section%(2**32))[2:]
        while(len(section)%8 != 0):
            section = '0' + section
        finalHash = finalHash + section[6:8] + section[4:6] + section[2:4] + section[0:2]
    return finalHash