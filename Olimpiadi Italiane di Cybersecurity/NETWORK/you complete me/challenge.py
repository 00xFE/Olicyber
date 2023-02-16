from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secret import key
import os


with open('./words.txt') as f:
    words = list(sorted([word.strip().encode('utf-8') for word in f.readlines()]))


# 100% sicuro!
aes = AES.new(key, AES.MODE_ECB)
BLOCK_LENGTH = 16


def encrypt_word(word):
    # Cifriamo la parola
    return aes.encrypt(pad(word, BLOCK_LENGTH)).hex()


def decrypt_char(char):
    # L'input dell'utente è un carattere ASCII cifrato.
    # Qui lo decifriamo e verifichiamo che effettivamente sia solo un carattere
    ch = unpad(aes.decrypt(bytes.fromhex(char)), BLOCK_LENGTH)
    assert(len(ch) == 1)
    return ch


def next_char(char):
    return (ord(char) + 1).to_bytes(1, 'big')


def get_words_by_prefix(prefix):
    # In un mondo ideale qui userei una struttura ad albero, ma sono troppo pigro per farlo
    # Estraggo l'ultimo carattere del prefisso
    prefix, last_char = prefix[:-1], prefix[-1].to_bytes(1, 'big')

    # Esempio: se il prefisso è mal allora voglio tutte le parole W tali per cui mal <= W < mam
    # Quindi lower_bound = mal e upper_bound = mam
    lower_bound = prefix + last_char
    upper_bound = prefix + next_char(last_char)

    return [w for w in words if lower_bound <= w < upper_bound]

def handle():
    curr_prefix = b''
    while True:
        # L'input del client è un singolo carattere cifrato
        char = input()
        curr_prefix += decrypt_char(char)

        # Cifro tutte le parole prima di inviarle: la sicurezza prima di tutto!
        words = [encrypt_word(w) for w in get_words_by_prefix(curr_prefix)]
        print('\n'.join(words))
        print('end')


if __name__ == "__main__":
    handle()
