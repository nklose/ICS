# run with './compile_backend_64.sh'
gcc -O3 -std=c99 -fPIC -c backend.c -o backend.o
# using libfftw3_64.a for 64-bit machines 
gcc -shared -Wl,-soname,libbackend.so -o libbackend.so backend.o ../vendor/libfftw3_64.a
rm -f backend.o
