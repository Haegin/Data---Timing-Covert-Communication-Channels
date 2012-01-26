import os, stat, sys

def encrypt(msg, prefix):
    # the input should be a sequence of bits
    plaintext = ""
    print(msg)
    for c in msg:
        plaintext += charToBitword(c)
    numb = 0
    print("Encrypting...")
    print(plaintext)
    while (plaintext != ""):
        bits = plaintext[0:9]
        filename = "{1}_{0}".format(numb, prefix)
        mode = bitsToMode(bits)
        file = open(filename, 'w')
        # not sure if the file needs content but hey, 4 bytes won't hurt
        file.write("test")
        file.close()
        os.chmod(filename, mode)
        numb += 1
        plaintext = plaintext[9:]
    print("Done")

def decrypt(prefix, numbFiles):
    numb = 0
    msg = ""
    print(numbFiles)
    print("Decrypting...")
    while (numb < numbFiles):
        filename = "{0}_{1}".format(prefix, numb)
        print(filename)
        mode = os.stat(filename).st_mode
        bits = modeToBits(mode)
        msg += bits
        numb += 1
    print("Done")
    plaintext = ""
    for i in range(0, len(msg), 7):
        plaintext += bitwordToChar(msg[i:i+7])
    print("\n{0}".format(plaintext))

def bitsToMode(bits):
    assert len(bits) <= 9
    if (len(bits) < 9):
        # need 9 bits so pad with zeros if necessary
        bits = "{0}{1}".format(bits, (9 - len(bits)) * '0')
    mask = 0
    if (bits[0] == '1'):
        mask = stat.S_IRUSR
    if (bits[1] == '1'):
        mask = mask ^ stat.S_IWUSR
    if (bits[2] == '1'):
        mask = mask ^ stat.S_IXUSR
    if (bits[3] == '1'):
        mask = mask ^ stat.S_IRGRP
    if (bits[4] == '1'):
        mask = mask ^ stat.S_IWGRP
    if (bits[5] == '1'):
        mask = mask ^ stat.S_IXGRP
    if (bits[6] == '1'):
        mask = mask ^ stat.S_IROTH
    if (bits[7] == '1'):
        mask = mask ^ stat.S_IWOTH
    if (bits[8] == '1'):
        mask = mask ^ stat.S_IXOTH
    return mask

def modeToBits(mode):
    bits = ""
    if (mode & stat.S_IRUSR) != 0:
        bits += "1"
    else:
        bits += "0"
    if (mode & stat.S_IWUSR) != 0:
        bits += "1"
    else:
        bits += "0"
    if (mode & stat.S_IXUSR) != 0:
        bits += "1"
    else:
        bits += "0"
    if (mode & stat.S_IRGRP) != 0:
        bits += "1"
    else:
        bits += "0"
    if (mode & stat.S_IWGRP) != 0:
        bits += "1"
    else:
        bits += "0"
    if (mode & stat.S_IXGRP) != 0:
        bits += "1"
    else:
        bits += "0"
    if (mode & stat.S_IROTH) != 0:
        bits += "1"
    else:
        bits += "0"
    if (mode & stat.S_IWOTH) != 0:
        bits += "1"
    else:
        bits += "0"
    if (mode & stat.S_IXOTH) != 0:
        bits += "1"
    else:
        bits += "0"
    return bits

def charToBitword(char):
    return bin(ord(char))[2:]

def bitwordToChar(bs):
    return chr(int("0b{0}".format(bs), 2))

if __name__ == "__main__":
    print(sys.argv)
    #print(charToBitword('H'))
    #print(bitwordToChar(charToBitword('H')))
    if (len(sys.argv) >= 4):
        if (sys.argv[1] == "enc"):
            encrypt(sys.argv[2], sys.argv[3])
            sys.exit(0)
        elif (sys.argv[1] == "dec"):
            decrypt(sys.argv[2], int(sys.argv[3]))
            sys.exit(0)
    print("Usage:")
    print("\tdata.py enc $MESSAGE $PREFIX")
    print("\tdata.py dec $PREFIX $NUMBER_OF_FILES\n")
    print("When encrypting you need to pass the message to encrypt\nand the prefix for the storage files.\n")
    print("When decrypting you need to pass the prefix for the storage\nfiles and the number of files the message is stored in.\n")
