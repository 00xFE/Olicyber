#!/usr/bin/env python3

# Importa la libreria di pwntools
from pwn import *


def main():
    '''
    remote(hostname, port) apre una socket e ritorna un object
    che può essere usato per inviare e ricevere dati sulla socket  
    '''
    HOST = "hostname"
    PORT = 1234
    r = remote(HOST, PORT)

    # .send() può essere invocato sull'oggetto ritornato da remote() per inviare dati
    r.send(b"Ciao!")

    # .sendline() è identico a .send(), però appende un newline dopo i dati
    r.sendline(b"Ciao!")

    # .sendafter() e .sendlineafter() inviano la stringa "Ciao!"
    r.sendafter(b"something", b"Ciao!")

    # solo dopo che viene ricevuta la stringa "something"
    r.sendlineafter(b"something", b"Ciao!")

    # .recv() riceve e ritorna al massimo 1024 bytes dalla socket
    data = r.recv(1024)

    # .recvline() legge dalla socket fino ad un newline
    data = r.recvline()

    # .recvuntil() legge dalla socket finchè non viene incontrata la stringa "something"
    data = r.recvuntil(b"something")

    # permette di interagire con la connessione direttamente dalla shell
    r.interactive()

    # chiude la socket
    r.close()


if __name__ == "__main__":
    main()
