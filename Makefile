CC ?= gcc
CFLAGS += -std=c++11 -Wall -O3
LDFLAGS += -llodepng -s
SRC = src/dct_double.cc src/gamma_correct.cc src/jpeg_data.cc src/jpeg_data_reader.cc src/output_image.cc src/quantize.cc src/decode.cc src/idct.cc src/jpeg_data_decoder.cc src/jpeg_huffman_decode.cc src/preprocess_downsample.cc
MAKE ?= make
PREFIX ?= /usr/local
INSTALL = install

UNAME_S := $(shell uname -s)

all: knusperli

knusperli: $(SRC)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

install: all
	$(INSTALL) -d $(PREFIX)/bin
	$(INSTALL) -m 0755 knusperli $(PREFIX)/bin/

clean:
	rm -rf knusperli

.PHONY: test install clean
