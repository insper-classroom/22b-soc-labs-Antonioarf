#
senha = 1234
TARGET = desliga
ALT_DEVICE_FAMILY ?= soc_cv_av
SOCEDS_ROOT ?= $(SOCEDS_DEST_ROOT)
HWLIBS_ROOT = $(SOCEDS_ROOT)/ip/altera/hps/altera_hps/hwlib
CROSS_COMPILE = arm-linux-gnueabihf-
CFLAGS = -g -Wall   -D$(ALT_DEVICE_FAMILY) -I$(HWLIBS_ROOT)/include/$(ALT_DEVICE_FAMILY)   -I$(HWLIBS_ROOT)/include/
LDFLAGS =  -g -Wall 
CC = $(CROSS_COMPILE)gcc
ARCH= arm

build: $(TARGET)

$(TARGET): $(TARGET).o 
	$(CC) $(LDFLAGS)   $^ -o $@ 

%.o : %.c
	$(CC) $(CFLAGS) -c $< -o $@

deploy: $(TARGET)
	sshpass -p $(senha) scp $(TARGET) root@169.254.0.13:/root/sem_socket
	sshpass -p $(senha) scp app.py root@169.254.0.13:/root/sem_socket
	sshpass -p $(senha) scp -r templates root@169.254.0.13:/root/sem_socket

	
run:	
	sshpass -p $(senha) ssh -t root@169.254.0.13 /root/sem_socket/$(TARGET)


all: build deploy run


.PHONY: clean
clean:
	rm -f $(TARGET) *.a *.o *~

