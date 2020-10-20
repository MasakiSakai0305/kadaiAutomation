#include<stdio.h>

int main(void){
	//printf("test1\n");
	int x;
	scanf("%d", &x);
	if (x == 1)
		printf("%dは閏年です\n", x);
	else
		printf("%dは閏年ではありません\n", x);
	return 0;

}

