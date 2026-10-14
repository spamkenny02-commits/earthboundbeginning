import hashlib

ROM_SHA = 'e878b83e9b00b51f8da6d038a5cbaf31cb9dccff5e11f0a7014048f4511f582c'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def records(data):
    if data[:5] != b'PATCH':
        raise ValueError('Invalid IPS header')
    out, i = [], 5
    while True:
        if i + 3 > len(data):
            raise ValueError('Truncated IPS')
        if data[i:i+3] == b'EOF':
            if i + 3 != len(data):
                raise ValueError('Unsupported IPS trailer')
            return out
        p = int.from_bytes(data[i:i+3], 'big')
        i += 3
        if i + 2 > len(data):
            raise ValueError('Truncated size')
        n = int.from_bytes(data[i:i+2], 'big')
        i += 2
        if n:
            if i+n > len(data):
                raise ValueError('Truncated payload')
            b = data[i:i+n]
            i += n
        else:
            if i+3 > len(data):
                raise ValueError('Truncated RLE')
            n = int.from_bytes(data[i:i+2], 'big')
            if not n:
                raise ValueError('Empty RLE')
            b = data[i+2:i+3] * n
            i += 3
        out.append((p, b))

def apply(rom, entries):
    result = bytearray(rom)
    for p, b in entries:
        if p < 0 or p+len(b) > len(result):
            raise ValueError('IPS outside ROM')
        result[p:p+len(b)] = b
    return bytes(result)

def append(prior, entries):
    records(prior)
    out = bytearray(prior[:-3])
    for p, b in entries:
        if p == 0x454F46 or not 0 < len(b) <= 65535:
            raise ValueError('Invalid IPS record')
        out += p.to_bytes(3, 'big') + len(b).to_bytes(2, 'big') + b
    return bytes(out + b'EOF')
