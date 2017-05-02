CC=gcc
INC1 = 
INC2 = 
INCDIRS = -I${INC1} -I${INC2}
LIBDIR1 = 
LIBDIR2 = 
CFLAGS=-g  ${INCDIRS}	
LDFLAGS = -lwiringPi

SOURCES=xbee_echo.c
OBJECTS=$(SOURCES:.c=.o)

SOURCES1=xbee_echo_api_mode1.c
OBJECTS1=$(SOURCES1:.c=.o)


EXECUTABLE=xbee_echo
EXECUTABLE1=xbee_echo_api_mode1

all:$(EXECUTABLE) $(EXECUTABLE1)
$(EXECUTABLE):$(OBJECTS) 
	$(CC) $(CFLAGS) $(OBJECTS) $(LDFLAGS) -o $@   
$(EXECUTABLE1):$(OBJECTS1) 
	$(CC) $(CFLAGS) $(OBJECTS1) $(LDFLAGS) -o $@   
clean:
	rm -f $(OBJECTS) $(OBJECTS1) $(EXECUTABLE) $(EXECUTABLE1)
