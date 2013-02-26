gcc -O3 -std=c99 -fPIC -c batch.c -o batch.o
gcc -shared -Wl,-soname,libbatch.so -o libbatch.so batch.o libfftw3.a
rm -f batch.o
