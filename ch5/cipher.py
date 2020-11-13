from string import ascii_letters as al
from random import sample

al = al + ' .!?@#$%^&*()-_+=><,/\\:;\'"][{}|~'


class AlphaShiftCipher:
    def __init__(self, shift, base_chars=al):
        self._shift = shift
        self._base_chars = sample(base_chars, k=len(base_chars))
        self._mod = len(self._base_chars)

    def encrypt(self, strings):
        strings_list = list(strings)
        shift, base, modulo = self._shift, self._base_chars, self._mod

        for i in range(len(strings_list)):
            char = strings_list[i]
            if char in base:
                index = (base.index(char) + shift) % modulo
                strings_list[i] = base[index]
        return ''.join(strings_list)

    def decrypt(self, strings):
        strings_list = list(strings)
        shift, base, modulo = self._shift, self._base_chars, self._mod

        for i in range(len(strings_list)):
            char = strings_list[i]
            if char in base:
                index = (base.index(char) - shift) % modulo
                strings_list[i] = base[index]
        return ''.join(strings_list)

    def lookup_table(self):
        return ''.join(self._base_chars)


if __name__ == '__main__':
    code = AlphaShiftCipher(5)
    words = 'This is a test for cipher.'
    print('Lookup table:', code.lookup_table())
    encrypt = code.encrypt(words)
    print('Encrypted message:', encrypt)
    decrypt = code.decrypt(encrypt)
    print('Original message: ', decrypt)
