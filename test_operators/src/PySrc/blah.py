
import struct
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def hex_to_float(f):
    return struct.unpack('!f', f.decode('hex'))[0]

print float_to_hex( (hex_to_float('49b59706') + hex_to_float('49c27859' )))
print float_to_hex( (hex_to_float('49b59000') + hex_to_float('49c27000' )))
