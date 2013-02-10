# compiles loop.c using the gcc compiler
gcc -O3 -std=c99 -fopenmp -lgomp -fPIC -DMULTI_THREAD=${1} -c loop.c -o loop.o
gcc -fopenmp -lgomp -shared -Wl,-soname,libloop.so -o libloop.so loop.o
rm -f loop.o
