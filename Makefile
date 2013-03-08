UNAME := $(shell uname)
BACK_END := backend
MID_END := midend
FRONT_END := local_GUI
BIN := bin

EXECUTABLE = $(BIN)/ICS

PYTHON = python

C_SRC = $(BACK_END)/backend.c
DLL_32 = 0
DLL_64 = 0
UNIX_BACKEND = $(BACK_END)/libfftw3_32.a
BACKEND_ARGS = -shared -Wl,-soname,$(BACK_END)/libbackend.so -o \
	$(BACK_END)/libbackend.so $(BACK_END)/backend.o $(UNIX_BACKEND)
WINDOWS_EXE = windowsexe.py
OS = Unix
# I Don't know if Mac's need something different?
ifeq ($(UNAME), MINGW32_NT-6.1)
	# Windows 7, 32-bit compile
	DLL_32 = 1
	EXECUTABLE = $(BIN)/ICS.exe
	PYTHON = "/c/Python27/python"
	OS = Windows 32
	BACKEND_ARGS = -shared -Wl,-soname,$(BACK_END)/libbackend.dll -o \
		$(BACK_END)/libbackend.dll $(BACK_END)/backend.o \
		$(BACK_END)/libfftw3.dll.a
else
ifeq ($(UNAME), MINGW64_NT-6.1)
	# Windows 7, 64-bit compile
	DLL_64 = 1
	EXECUTABLE = $(BIN)/ICS.exe
	PYTHON = "/c/Python27/python"
	OS = Windows 64
	BACKEND_ARGS = -shared -Wl,-soname,$(BACK_END)/libbackend.dll -o \
		$(BACK_END)/libbackend.dll $(BACK_END)/backend.o \
		$(BACK_END)/libfftw3.dll.a
else
	# Linux compile
	LBITS := $(shell getconf LONG_BIT)
	ifeq ($(LBITS),64)
		# do 64 bit stuff here, like set some CFLAGS
		UNIX_BACKEND = $(BACK_END)/libfftw3_64.a
	else
		# do 32 bit stuff here
		UNIX_BACKEND = $(BACK_END)/libfftw3_32.a
	endif
endif

endif

all: clean $(EXECUTABLE)

libbackend:
ifeq ($(DLL_32), 1)
	@cp $(BACK_END)/fftw3.h_32 $(BACK_END)/fftw3.h
	@cp $(BACK_END)/libfftw3-3.dll_32 $(BACK_END)/libfftw3-3.dll
	@cp $(BACK_END)/libfftw3-3.dll_32 $(BACK_END)/libfftw3.dll.a
else
	ifeq ($(DLL_64), 1)
		@cp $(BACK_END)/fftw3.h_64 $(BACK_END)/fftw3.h
		@cp $(BACK_END)/libfftw3-3.dll_64 $(BACK_END)/libfftw3-3.dll
		@cp $(BACK_END)/libfftw3-3.dll_64 $(BACK_END)/libfftw3.dll.a
	else
		cp $(BACK_END)/fftw3.h_ux $(BACK_END)/fftw3.h
	endif
endif
	@echo "=== Start: Compiling $(OS) backend ==="
	gcc -O3 -std=c99 -fPIC -c $(C_SRC) -o $(BACK_END)/backend.o
	gcc $(BACKEND_ARGS)
	@echo "=== End: Compiling $(OS) backend ==="
	@echo

frontend:
	@echo "=== Start: Compiling frontend ==="
	# TODO
	@echo "=== End: Compiling frontend ==="
	
$(EXECUTABLE): clean_backend frontend
	@echo "=== Start: Compiling executable ==="
ifeq ($(DLL_32), 1)
	@# Windows 32 specific stuff here
	@$(PYTHON) $(WINDOWS_EXE) py2exe
else
	ifeq ($(DLL_64), 1)
		@# Windows 64 specific stuff here
		@$(PYTHON) $(WINDOWS_EXE) py2exe
	else
		@# Linux specific stuff here
	endif
endif
	@# OS Independant stuff here
	@echo "=== End: Compiling executable ==="
	

clean_backend: libbackend
	@# After running the backend, cleans up a bit, moves any windows dlls.
	@mv -f $(BACK_END)/libfftw3-3.dll  $(BIN)/libfftw3-3.dll
	@cp -f $(BACK_END)/libbackend.dll  $(BIN)/libbackend.dll
	@rm -f $(BACK_END)/libfftw3.dll.a
	@rm -f $(BACK_END)/fftw3.h
	@rm -f backend.o
	
clean:
	@echo "=== Begin clean ==="
	@rm -f $(BACK_END)/libbackend.so
	@rm -f $(BACK_END)/libbackend.dll
	@rm -f $(BIN)/libbackend.dll
	@rm -f $(BIN)/libfftw3-3.dll
	@rm -f backend.o
	@echo "=== End clean ==="
	@echo