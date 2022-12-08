#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include "hwlib.h"
#include "socal/socal.h"
#include "socal/hps.h"
#include "socal/alt_gpio.h"

#define SOCKET_NAME "/tmp/9Lq7BNBnBycd6nxy.socket"

#define HW_REGS_BASE (ALT_STM_OFST)
#define HW_REGS_SPAN (0x04000000)
#define HW_REGS_MASK (HW_REGS_SPAN - 1)

#define USER_IO_DIR (0x01000000)
#define BIT_LED (0x01000000)
#define BUTTON_MASK (0x02000000)


void *virtual_base;
int fd;
int InitLed(void);
void LedOn(void);
void LedOff(void);

int main(int argc, char *argv[])
{
	uint32_t  scan_input;
	bool status_led;
	status_led = false;
	bool status_bot;
	status_bot= false;
	/*
		INICIALIZAR O LED E O LCD
	*/
	if (InitLed()){return 1;}


	/*
		INICIALIZAR O SOCKET
	*/
	int sock = 0, connfd = 0;
	char sendBuff[1025];
	char recvBuff[1025];
	memset(sendBuff, '0', sizeof(sendBuff));

	unlink(SOCKET_NAME);

	sock = socket(AF_UNIX, SOCK_STREAM, 0);

	struct sockaddr_un name;
	memset(&name, 0, sizeof(struct sockaddr_un));
	name.sun_family = AF_UNIX;
	strncpy(name.sun_path, SOCKET_NAME, sizeof(name.sun_path) - 1);

	bind(sock, (const struct sockaddr *)&name, sizeof(struct sockaddr_un));

	listen(sock, 20);
	connfd = accept(sock, (struct sockaddr *)NULL, NULL);

	





	
	printf("Inicio While");

	printf("11111111111111111\r\n");

	while (1)
	{
		scan_input = alt_read_word((virtual_base + ((uint32_t)(ALT_GPIO1_EXT_PORTA_ADDR) & (uint32_t)(HW_REGS_MASK))));
		// write
		printf("22222222222222222222\r\n");

		if (~scan_input & BUTTON_MASK)
		{printf("!!!!!!!!!!!!!!!!!\r\n");
		snprintf(sendBuff, sizeof(sendBuff), "P");

		if(!status_bot){
			status_led= !status_led;
			status_bot= true;}
		}
		else
		{
			status_bot= false;
			printf("@@@@@@@@@@@@@@@@@@@@@@@@@@@@\r\n");
			snprintf(sendBuff, sizeof(sendBuff), "S");
		}
		write(connfd, sendBuff, strlen(sendBuff));
		printf("3333333333333333\r\n");

		// read and print
		int n = 0;
		if ((n = read(connfd, recvBuff, sizeof(recvBuff) - 1)) >= 0)
		{
			recvBuff[n] = 0;
			if (recvBuff[0] == 'L')
			{
				status_led = true;				
			}
			if (recvBuff[0] == 'D')
			{
				status_led = false;

			}
		}
		printf("4444444444444444\r\n");
	if (status_led){	alt_setbits_word((virtual_base + ((uint32_t)(ALT_GPIO1_SWPORTA_DR_ADDR) & (uint32_t)(HW_REGS_MASK))), BIT_LED);}
	else{alt_clrbits_word((virtual_base + ((uint32_t)(ALT_GPIO1_SWPORTA_DR_ADDR) & (uint32_t)(HW_REGS_MASK))), BIT_LED);
}
	}

	close(fd);

	close(connfd);
	sleep(1);
	return 0;
}

int InitLed(void)
{

	// map the address space for the LED registers into user space so we can interact with them.
	// we'll actually map in the entire CSR span of the HPS since we want to access various registers within that span
	if ((fd = open("/dev/mem", (O_RDWR | O_SYNC))) == -1)
	{
		printf("ERROR: could not open \"/dev/mem\"...\n");
		return (1);
	}

	virtual_base = mmap(NULL, HW_REGS_SPAN, (PROT_READ | PROT_WRITE), MAP_SHARED, fd, HW_REGS_BASE);

	if (virtual_base == MAP_FAILED)
	{
		printf("ERROR: mmap() failed...\n");
		close(fd);
		return (1);
	}
	// initialize the pio controller
	// led: set the direction of the HPS GPIO1 bits attached to LEDs to output
	alt_setbits_word((virtual_base + ((uint32_t)(ALT_GPIO1_SWPORTA_DDR_ADDR) & (uint32_t)(HW_REGS_MASK))), USER_IO_DIR);

	return 0;
}
