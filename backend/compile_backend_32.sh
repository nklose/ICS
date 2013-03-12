# run with './compile_backend_32.sh'
gcc -O3 -std=c99 -fPIC -c backend.c -o backend.o
# using libfftw3_32.a for 32-bit machines 
gcc -shared -Wl,-soname,libbackend.so -o libbackend.so backend.o ../vendor/libfftw3_32.a
rm -f backend.o
