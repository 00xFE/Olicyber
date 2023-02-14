#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
  void *shellcode;
  size_t size;

  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  puts("*****************************************************************");
  puts("* Benvenuto nella quarta sfida Pwntools                         *");
  puts("* Questa volta dovrai utilizzare le funzioni                    *");
  puts("* di shellcoding che pwntools offre                             *");
  puts("* Mandami un qualsiasi shellcode e io lo eseguirò :)            *");
  puts("*****************************************************************");
  printf("... Invia un qualsiasi carattere per iniziare ...");
  getchar();

  shellcode = mmap(NULL, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
  if (shellcode == MAP_FAILED) {
    perror("[-] Challenge error");
    exit(1);
  }

  printf("Shellcode size (max 4096): ");
  if (scanf("%ld", &size) != 1) {
    puts("[-] Invalid size");
    exit(1);
  }

  if (size > 0x1000) {
    puts("[-] Size too big!");
    exit(1);
  }

  printf("Send me exactly %ld bytes: ", size);
  if (read(0, shellcode, size) != size) {
    puts("[-] Wrong size read");
    exit(1);
  }

  puts("[*] Executing shellcode...");
  asm volatile("jmp *%0" : : "r" (shellcode));

  return 0;
}