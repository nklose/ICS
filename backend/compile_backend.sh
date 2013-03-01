# run with './compile_backend.sh'
gcc -O3 -std=c99 -fPIC -c backend.c -o backend.o
# change libfftw3_64.a to libfftw3_32.a for 32-bit machines 
gcc -shared -Wl,-soname,libbackend.so -o libbackend.so backend.o libfftw3_64.a
rm -f backend.o
