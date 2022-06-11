from random import randint, randrange
from math import gcd

BEGIN = 100
END = 1000

class Cipher:
    def __init__(self):
        self.p = self.generate_prime_number()
        self.q = self.generate_prime_number()
        self.n = self.p * self.q
        self.d = self.generate_coprime_number((self.p - 1) * (self.q - 1))
        self.e = self.generate_multiplier(self.p, self.q, self.d)

        self.generate_private_key()

    def generate_sert(self, name):
        self.sert = {'e': self.e, 'n': self.n}
        sert = open(name + '_sert.txt', 'w+')
        sert.write(str(self.e) + ' ' + str(self.n))
        sert.close()

    def upload_sert(self, file_name):
        sert = open(file_name)
        blocks =  sert.read().split(' ')
        neighbour_e = blocks[0]
        neighbour_n = blocks[1]

        self.neighbour_sert = {'e': int(neighbour_e), 'n': int(neighbour_n)}
        sert.close()

    def generate_private_key(self):
        self.__private_key = {'d': self.d, 'n': self.n}

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

    def cipher_message(self, file_name, file_name_ciphered):
        secret_key = open(file_name)
        message = secret_key.read()

        secret_key_ciphered = open(file_name_ciphered, 'w+')

        for letter in message:
            ciphered_letter = (ord(letter) ** self.neighbour_sert['e']) % self.neighbour_sert['n']
            secret_key_ciphered.write(str(ciphered_letter) + '\n')

        secret_key_ciphered.close()

    def decipher_message(self, file_name_ciphered, file_name_deciphered):
        secret_key_ciphered = open(file_name_ciphered)
        ciphered_message = secret_key_ciphered.read()
        ciphered_letters = ciphered_message.split(('\n'))[:-1]

        secret_key_deciphered = open(file_name_deciphered, 'w+')

        for letter in ciphered_letters:
            deciphered_letter = chr((int(letter) ** self.__private_key['d']) % self.__private_key['n'])
            secret_key_deciphered.write(deciphered_letter)
        secret_key_deciphered.close()

client = Cipher()
client.generate_sert('client')

server = Cipher()
server.generate_sert('server')

server.upload_sert('client_sert.txt')
client.upload_sert('server_sert.txt')

client.cipher_message('secret_key.txt', 'secret_key_ciphered.txt') #

server.decipher_message('secret_key_ciphered.txt', 'secret_key_deciphered.txt') #

