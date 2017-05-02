CC=gcc
INC1 = 
INC2 = 
INCDIRS = -I${INC1} -I${INC2}
LIBDIR1 = 
LIBDIR2 = 
CFLAGS=-g  ${INCDIRS}	
LDFLAGS = -lwiringPi

SOURCES=stepper_wave.c
OBJECTS=$(SOURCES:.c=.o)

SOURCES1=stepper_full_step.c
OBJECTS1=$(SOURCES1:.c=.o)


EXECUTABLE=stepper_wave
EXECUTABLE1=stepper_full_step

all:$(EXECUTABLE) $(EXECUTABLE1) $(EXECUTABLE2)
$(EXECUTABLE):$(OBJECTS) 
	$(CC) $(CFLAGS) $(OBJECTS) $(LDFLAGS) -o $@   

$(EXECUTABLE1):$(OBJECTS1) 
	$(CC) $(CFLAGS) $(OBJECTS1) $(LDFLAGS) -o $@   


clean:
	rm -f $(OBJECTS) $(EXECUTABLE) $(OBJECTS1) $(EXECUTABLE1)

