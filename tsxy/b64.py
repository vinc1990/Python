def base64encode(string):
    base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    length = len(string)
    i = 0
    out = ""
    while(i < length):
        c1 = ord(string[i]) & 0xff
        i += 1
        if i == length:
            out += base64EncodeChars[c1 >> 2]
            out += base64EncodeChars[(c1 & 0x3) << 4]
            out += "=="
            break
        c2 = ord(string[i])
        i += 1
        if i == length:
            out += base64EncodeChars[c1 >> 2]
            out += base64EncodeChars[((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4)]
            out += base64EncodeChars[(c2 & 0xF) << 2]
            out += "="
            break
        c3 = ord(string[i])
        i += 1
        out += base64EncodeChars[c1 >> 2]
        out += base64EncodeChars[((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4)]
        out += base64EncodeChars[((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6)]
        out += base64EncodeChars[c3 & 0x3F]
    return out

def utf16to8(string):
    out = ""
    length = len(string)
    for i in range(0, length):
        c = ord(string[i])
        if (c >= 0x0001) and (c <= 0x007F):    
            out += string[i]
        elif c > 0x07FF:
            out += String.chr(0xE0 | ((c >> 12) & 0x0F))
            out += String.chr(0x80 | ((c >>  6) & 0x3F))
            out += String.chr(0x80 | ((c >>  0) & 0x3F))
        else:
            out += String.chr(0xC0 | ((c >>  6) & 0x1F))
            out += String.chr(0x80 | ((c >>  0) & 0x3F))
    return out
