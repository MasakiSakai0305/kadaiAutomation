#include<stdio.h>
int main(void){
  int x,X,i,a,b;
  printf("正の整数を入力してください:");
  scanf("%d",&x);

  X=x;

  i=1;
  b=0;
  while(x>0){
    a=x%10;
    printf("%dの位は%dです。\n",i,a);
    i=i*10;
    x=x/10;
    b=b+1;
  }
  printf("%dは%d桁の数です\n",X,b);
  return 0;
}

