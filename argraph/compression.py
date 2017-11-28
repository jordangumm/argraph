

mappings = {
'A': '00',
'00': 'A',
'C': '01',
'01': 'C',
'G': '10',
'10': 'G',
'T': '11',
'11': 'T'}


def split(seq, num):
    return [ seq[start:start+num] for start in range(0, len(seq), num) ]

def encode_nuc(seq):
    """ Maps nucleotide string to 4x smaller bytechar representation """
    encoded_string = ''
    for kmer in split(seq, 4):
        while len(kmer) < 4: kmer = '{}A'.format(kmer) # fill in kmer to full byte
        binary_string = ''
        for bp in kmer:
            binary_string += mappings[bp]
        encoded_string += chr(int(binary_string, 2))
    return encoded_string

def decode_nuc(encoded_seq, length):
    """ Maps bytechar string to nucleotide string """
    seq = ''
    for c in encoded_seq:
        binary_string = '{0:08b}'.format(ord(c))
        while len(binary_string) < 8: binary_string = '0{}'.format(binary_string) # fill in binary string to full byte
        for bp in split(binary_string, 2):
            seq += mappings[bp]
            if len(seq) == length:
                break # escape if length of original sequence is met, avoiding extended A encoding (see above)
    return seq


if __name__ == "__main__":
    orig_seq = 'ATCGATCGT'
    len_orig_seq = len(orig_seq)
    print('encoding')
    new_seq = encode_nuc(orig_seq)
    print('created {}'.format(new_seq))
    print('decoding')
    old_seq = decode_nuc(new_seq, len_orig_seq)

    print('{} -> {} -> {}'.format(orig_seq, new_seq, old_seq))
