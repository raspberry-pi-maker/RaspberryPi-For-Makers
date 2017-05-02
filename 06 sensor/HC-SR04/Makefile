CC=gcc
INC1 = 
INC2 = 
INCDIRS = -I${INC1} -I${INC2}
LIBDIR1 = 
LIBDIR2 = 
#CFLAGS=-g -Wall ${INCDIRS}	
CFLAGS=-g  ${INCDIRS}	
#LDFLAGS = -L${LIBDIR1} -L${LIBDIR2} -lwiringPi -lm -lrt
LDFLAGS = -lwiringPi -lm -lrt
LDFLAGS2 = -lpigpio -lm -lrt -lpthread

SOURCES=hc_sr04.c
OBJECTS=$(SOURCES:.c=.o)

SOURCES1=hc_sr04_async.c
OBJECTS1=$(SOURCES1:.c=.o)

EXECUTABLE=hc_sr04
EXECUTABLE1=hc_sr04_async

all:$(EXECUTABLE) $(EXECUTABLE1)
$(EXECUTABLE):$(OBJECTS) 
	$(CC) $(CFLAGS) $(OBJECTS) $(LDFLAGS) -o $@   
$(EXECUTABLE1):$(OBJECTS1) 
	$(CC) $(CFLAGS) $(OBJECTS1) $(LDFLAGS2) -o $@   
clean:
	rm -f $(OBJECTS) $(OBJECTS1)
