CC=gcc
CFLAGS=-g -Wall -O2
LIBS=-lcurl
TARGET=apiTester

apiTester:
	$(CC) -o $@ $(CFLAGS) apiTester.c $(LIBS)

all:	$(TARGET)

clean:
	rm  -f *.o $(TARGET)
