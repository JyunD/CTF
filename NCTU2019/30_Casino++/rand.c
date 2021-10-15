#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>

int main(){

	    srand( 0x0 );
	    for (int i=0;i<25;i++)
		    printf("%x\n",rand() % 100);

}
