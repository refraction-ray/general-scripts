import math
import sys


def f1(n, byte, c):
    for bitIndex in range(8):
        bit = (byte >> bitIndex) & 1
        if bit + ((n - bit) & ~1) == n:
            n = (n - bit) >> 1
        else:
            n = ((c - bit) ^ n) >> 1
    return n


def genPassword(MathID, ActivationKey):
    string = MathID + "$1&" + ActivationKey

    hash0 = 0xA439
    for byteIndex in reversed(range(len(string))):
        hash0 = f1(hash0, ord(string[byteIndex]), 0x105C3)

    n1 = 0
    while (f1(f1(hash0, n1 & 0xFF, 0x105C3), n1 >> 8, 0x105C3) != 0xA5B6):
        n1 += 1
        if n1 >= 0XFFFF:
            raise Exception("Error")
    n1 = math.floor(((n1 + 0x72FA) & 0xFFFF) * 99999.0 / 0xFFFF)
    n1str = "0000" + str(n1)
    n1str = n1str[-5:]

    temp = int(n1str[:-3] + n1str[-2:] + n1str[-3:-2])
    temp = math.ceil((temp / 99999.0) * 0xFFFF)
    temp = f1(f1(0, temp & 0xFF, 0x1064B), temp >> 8, 0x1064B)
    for byteIndex in reversed(range(len(string))):
        temp = f1(temp, ord(string[byteIndex]), 0x1064B)

    n2 = 0

    while f1(f1(temp, n2 & 0xFF, 0x1064B), n2 >> 8, 0x1064B) != 0xA5B6:
        n2 += 1
        if n2 >= 0xFFFF:
            raise Exception("Error")
    n2 = math.floor((n2 & 0xFFFF) * 99999.0 / 0xFFFF)

    n2str = ("0000" + str(n2))[-5:]
    password = n2str[3] + n1str[3] + n1str[1] + n1str[0] + "-" + n2str[4] + n1str[2] + n2str[0] + "-" + n2str[2] + \
               n1str[4] + n2str[1] + "::1"

    return password


if __name__ == "__main__":
    genPassword(sys.argv[1], sys.argv[2])
