import random
import string
import sys
import itertools
import pandas as pd


class Caesar:
    def __init__(self, text="This is a test encryption", key=3):
        self.text = text
        self.key = self.keygen(key)

    def keygen(self, key):
        return key

    def encording(self):
        cipher = ""
        plain = self.text
        for char in plain:
            ASCII = ord(char)
            if ord('A') <= ASCII <= ord('Z'):
                cipher += chr((ASCII - ord('A') - self.key) % 26 + ord('A'))
            elif ord('a') <= ASCII <= ord('z'):
                cipher += chr((ASCII - ord('a') - self.key) % 26 + ord('a'))
            elif ord('0') <= ASCII <= ord('9'):
                cipher += chr((ASCII - ord('0') - self.key) % 10 + ord('0'))
            else:
                cipher += char
        print("Cryotigram: {}".format(cipher))
        return cipher

    def decording(self):
        plain = ""
        cipher = self.text
        for char in cipher:
            ASCII = ord(char)
            if ord('A') <= ASCII <= ord('Z'):
                plain += chr((ASCII - ord('A') + self.key) % 26 + ord('A'))
            elif ord('a') <= ASCII <= ord('z'):
                plain += chr((ASCII - ord('a') + self.key) % 26 + ord('a'))
            elif ord('0') <= ASCII <= ord('9'):
                plain += chr((ASCII - ord('0') + self.key) % 10 + ord('0'))
            else:
                plain += char
        return plain

    def attack(self):
        for key in range(26):
            self.key = key
            plain = self.decording()
            print("Key:{}".format(key) + "\n" + plain)


class Skytale:
    def __init__(self, text="This is a test encryption", key=3):
        self.text = text.replace(' ', '')
        self.key = self.keygen(key)

    def keygen(self, key):
        return key

    def encording(self):
        cipher = ""
        plain = self.text
        mod = len(plain) % self.key
        block = -(-len(plain) // self.key) + (1 if mod != 0 else 0)
        for j in range(self.key):
            for k in range(block):
                index = k*self.key + j
                if index < len(plain):
                    cipher += plain[index]
                else:
                    cipher += random.choice(string.ascii_letters)
        print("Cryotigram: {}".format(cipher))
        return cipher

    def decording(self):
        plain = ""
        chiper = self.text
        for j in range(self.key):
            for k in range(j, len(chiper), self.key):
                plain += chiper[k]
        return plain

    def attack(self):
        wordcount = len(self.text)
        divisor = [i for i in range(2, wordcount) if wordcount % i == 0]
        print("List of potential keys:{}".format(divisor))
        if divisor:
            for key in divisor:
                self.key = key
                plain = self.decording()
                print("Key:{}".format(self.key) + "\n" + plain)
        else:
            print("This text may not be Skytale encryption, because the number of characters in the text is a prime number.")


class Transposition:
    def __init__(self, text="This is a test encryption", key=3, random_state=21):
        random.seed(random_state)
        self.text = text
        self.length = len(text)
        self.key, self.tau = self.keygen(key)

    def keygen(self, key):
        if key <= self.length:
            tau = list(range(key))
            random.shuffle(tau)
            return key, tau
        else:
            print("ValueError! The key value is invalid. The key value is more than the number of characters in the text.")
            sys.exit()

    def encording(self):
        chiper = ""
        plain = self.text
        blocks = [plain[i: i+self.key]
                  for i in range(0, self.length, self.key)]
        for block in blocks:
            if len(block) != self.key:
                chiper += block
            else:
                for loc in self.tau:
                    chiper += block[loc]
        return chiper

    def decording(self):
        plain = self.encording()
        return plain

    def attack(self):
        for key in range(2, self.length):
            order = list(range(key))
            self.key = key
            print("Key:{}".format(self.key))
            for tau in itertools.permutations(order):
                self.tau = tau
                plain = self.decording()
                print("\t" + plain)


class Substitution:
    def __init__(self, text="This is a test encryption", key=3, mode="single"):
        self.text = text.replace(' ', '')
        self.key, self.sigma = self.keygen(key, mode)
        self.length = len(text)

    def keygen(self, key, mode):
        random.seed(key)
        self.mode = mode
        sigma = {}
        letters = ''.join(random.sample(string.ascii_letters, 52))
        if self.mode == "single":
            for i, j in zip(string.ascii_letters, letters):
                sigma[i] = j
        elif self.mode == "multi":
            multi_letters = []
            for n in range(52):
                multi_letters.append(
                    ''.join(random.choices(string.ascii_letters, k=key)))
            for i, j in zip(string.ascii_letters, multi_letters):
                sigma[i] = j
        return key, sigma

    def encording(self):
        chiper = ""
        plain = self.text
        for i in plain:
            chiper += self.sigma[i]
        return chiper

    def decording(self):
        plain = ""
        chiper = self.text
        if self.mode == "single":
            for i in chiper:
                for key, value in self.sigma.items():
                    if value == i:
                        plain += key
                        break
        elif self.mode == "multi":
            blocks = [chiper[i: i+self.key]
                      for i in range(0, len(chiper), self.key)]
            for i in blocks:
                for key, value in self.sigma.items():
                    if value == i:
                        plain += key
                        break
        return plain


class Vigenere:
    def __init__(self, text="This is a test encryption", key="TEST"):
        self.table = self.tablegen()
        self.text = text.lower().replace(' ', '')
        self.key = self.keygen(key)

    def tablegen(self):
        self.lower = string.ascii_lowercase
        self.upper = string.ascii_uppercase
        table = []
        for i in range(26):
            table.append(self.lower)
            self.lower = self.lower[1:] + self.lower[0]
        return table

    def keygen(self, key):
        return key

    def encording(self):
        chiper = ""
        plain = self.text
        for i, m in enumerate(plain):
            k = self.key[i % len(self.key)]
            chiper += self.table[self.upper.index(k)][self.lower.index(m)]
        return chiper

    def decording(self):
        plain = ""
        chiper = self.text
        for i, c in enumerate(chiper):
            k = self.key[i % len(self.key)]
            plain += self.lower[self.table[self.upper.index(k)].index(c)]
        return plain


def test():
    s = Vigenere(text="I love you")
    tt = s.encording()
    s.text = tt
    print(tt)
    print(s.decording())


if __name__ == "__main__":
    test()
