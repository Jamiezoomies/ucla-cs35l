# Make x86-64 random byte generators.

# Copyright 2015, 2020, 2021 Paul Eggert

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE = -O2

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd

# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --gzip --transform 's,^,randall/,'
TAREXT = tgz

default: randall

FILES = options.c output.c rand64-hw.c rand64-sw.c rand64-lrand48.c

randall: randall.c
	$(CC) $(CFLAGS) $@.c $(FILES) -o $@

assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile randall.c
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission-tarball: randall-submission.$(TAREXT)
submission-files = $(assignment-files) \
  notes.txt options.h options.c output.h output.c rand64-hw.h rand64-hw.c \
  rand64-lrand48.h rand64-lrand48.c rand64-sw.h rand64-sw.c
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

repository-tarball:
	$(TAR) -czf randall-git.tgz .git

.PHONY: default clean assignment submission-tarball repository-tarball

check: randall
	@./randall 100 | wc -c | grep -q '100' && \
	echo "Default Test Passed" || "Default Test Failed";
	@if [ $$? -eq 0 ]; then echo "Result Test Passed."; \
	else echo "Result Test Failed."; fi
	@./randall 0; if [ $$? -eq 1 ]; then echo "Exception Test Passed."; \
	else echo "Exception Test Failed."; fi

check-rdrand: randall
	@echo "Testing RDRAND..."
	@./randall -i rdrand 100 | wc -c | grep -q '100' && \
	echo "RDRAND Test Passed." || echo "RDRAND Test Failed."
	@if [ $$? -eq 0 ]; then echo "Result Test Passed."; \
	else echo "Result Test Failed."; fi
	@./randall -i rdrand 0; if [ $$? -eq 1 ]; then echo "Exception Test Passed."; \
	else echo "Exception Test Failed."; fi	
	
check-lrand48: randall
	@echo "Testing lrand48_r..."
	@./randall -i lrand48_r 100 | wc -c | grep -q '100' && \
	echo "lrand48_r Test Passed." || echo "lrand48_r Test Failed."
	@if [ $$? -eq 0 ]; then echo "Result Test Passed."; \
	else echo "Result Test Failed."; fi
	@./randall -i lrand48_r 0; if [ $$? -eq 1 ]; then echo "Exception Test Passed."; \
	else echo "Exception Test Failed."; fi

check-file-input: randall
	@echo "Testing file input (/dev/urandom)..."
	@./randall -i /dev/urandom 100 | wc -c | grep -q '100' && \
	echo "File Input Test Passed." || echo "File Input Test Failed."
	@if [ $$? -eq 0 ]; then echo "Result Test Passed."; \
	else echo "Result Test Failed."; fi
	@./randall -i /dev/urandom 0; if [ $$? -eq 1 ]; then echo "Exception Test Passed."; \
	else echo "Exception Test Failed."; fi

check-stdio-output: randall
	@echo "Testing stdio output..."
	@./randall -o stdio 100 | wc -c | grep -q '100' && \
	echo "Stdio Output Test Passed." || echo "Stdio Output Test Failed."
	@if [ $$? -eq 0 ]; then echo "Result Test Passed."; \
	else echo "Result Test Failed."; fi
	@./randall -o stdio 0; if [ $$? -eq 1 ]; then echo "Exception Test Passed."; \
	else echo "Exception Test Failed."; fi

check-block-output: randall
	@echo "Testing block output..."
	@./randall -o 20 100 | wc -c | grep -q '100' && \
	echo "Nbytes Output Test Passed." || echo "Nbytes Output Test Failed."
	@if [ $$? -eq 0 ]; then echo "Result Test Passed."; \
	else echo "Result Test Failed."; fi
	@./randall -o 20 0; if [ $$? -eq 1 ]; then echo "Exception Test I Passed."; \
	else echo "Exception Test I Failed."; fi
	@./randall -o 0 100; if [ $$? -eq 1 ]; then echo "Exception Test II Passed."; \
	else echo "Exception Test II Failed."; fi


clean:
	rm -f *.o *.$(TAREXT) randall
