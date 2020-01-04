class Caesar:
    def __init__(self, plain="DeMO", key=3):
        self.plain = plain
        self.key = self.keygen(key)

    def keygen(self, key):
        return key

    def encording(self):
        cipher = ""
        for char in self.plain:
            ASCII = ord(char)
            if ord('A') <= ASCII <= ord('Z'):
                cipher += chr((ASCII - ord('A') - self.key) % 26 + ord('A'))
            elif ord('a') <= ASCII <= ord('z'):
                cipher += chr((ASCII - ord('a') - self.key) % 26 + ord('a'))
            elif ord('0') <= ASCII <= ord('9'):
                cipher += chr((ASCII - ord('0') - self.key) % 10 + ord('0'))
            else:
                cipher += char
        print("暗号文: {}".format(cipher))
        return cipher

    def decording(self, cipher):
        plain = ""
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

    def attack(self, cipher):
        for key in range(26):
            self.key = key
            plain = self.decording(cipher)
            print("Key:{}".format(key) + "\n" + plain)
