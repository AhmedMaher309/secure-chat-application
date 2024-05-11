def left_circular_shift(bits, shift):
    shift %= len(bits)
    return bits[shift:] + bits[:shift]

def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    return ''.join(format(byte, '08b') for byte in data)

def write_binary_file(file_path, bits):
    with open(file_path, 'wb') as file:
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            file.write(bytes([int(byte, 2)]))


if __name__ == "__main__":
    input_file = 'bits.txt'
    output_file = 'shifted_bits.txt'

    bits = read_binary_file(input_file)
    shifted_bits = left_circular_shift(bits, 1)
    write_binary_file(output_file, shifted_bits)
