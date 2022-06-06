from random import randint, randrange
from math import gcd

BEGIN = 100
END = 1000

class Cipher:
    def __init__(self):
        self.generate_keys()

    def generate_keys(self):
        p = self.generate_prime_number() # простое число
        q = self.generate_prime_number() # простое число
        # print('p: ', p)
        # print('q: ', q)

        n = p * q # часть открытого и закрытого ключа
        # print('n:', n)

        d = self.generate_coprime_number((p - 1) * (q - 1)) # часть секретного ключа
        # print('d: ', d)

        e = self.generate_multiplier(p, q, d)
        # print('e: ', e)

        self.public_key = {'e': e, 'n': n}
        self.__private_key = {'d': d, 'n': n}

    def generate_prime_number(self):
        prime_number_candidate = randint(BEGIN, END)

        while True:
            is_prime = True
            for num in range(2, int(prime_number_candidate ** 0.5) + 1):
                if prime_number_candidate % num == 0:
                    is_prime = False
                    prime_number_candidate += 1
                    break
            if is_prime:
                return prime_number_candidate
    
    def generate_coprime_number(self, number):
        coprime_number_candidate = randint(BEGIN, END)
        while True:
            if gcd(coprime_number_candidate, number) > 1:
                coprime_number_candidate += 1
            else:
                return coprime_number_candidate

    def generate_multiplier(self, p, q, d):
        e = randrange(BEGIN, END)
        while True:
            if (e * d) % ((p - 1) * (q - 1)) == 1:
                return e
            e += 1

    def cipher_message(self):
        secret_key = open('secret_key.txt')
        message = secret_key.read()

        secret_key_ciphered = open('secret_key_ciphered.txt', 'w')

        for letter in message:
            ciphered_letter = (ord(letter) ** box_1.public_key['e']) % box_1.public_key['n']
            secret_key_ciphered.write(str(ciphered_letter) + '\n')

        secret_key_ciphered.close()

    def decipher_message(self):
        secret_key_ciphered = open('secret_key_ciphered.txt')
        ciphered_message = secret_key_ciphered.read()
        ciphered_letters = ciphered_message.split(('\n'))[:-1]

        secret_key_deciphered = open('secret_key_deciphered.txt', 'w')

        for letter in ciphered_letters:
            deciphered_letter = chr((int(letter) ** self.__private_key['d']) % self.__private_key['n'])
            print("deciphered_letter", deciphered_letter)
            secret_key_deciphered.write(deciphered_letter)
        secret_key_deciphered.close()

box_1 = Cipher()

box_1.cipher_message()

box_1.decipher_message()
