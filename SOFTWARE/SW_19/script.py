#!/usr/bin/env python3
from pwn import *

exe = ELF("./chall")

if args.REMOTE:
	p = remote("host", 1234)
else:
	p = process([exe.path])