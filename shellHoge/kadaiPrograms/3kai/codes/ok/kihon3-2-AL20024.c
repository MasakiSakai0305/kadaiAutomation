#include <stdio.h>
int main(void){
  int a,b,c;
  while(1){
    printf("数値を入力：");
    scanf("%d",&a);
    printf("数値を入力：");
    scanf("%d",&b);
    if(a>b){
      if(a%b==0){
	printf("%dは%dの約数です。\n",b,a);
      }else{
	printf("%dは%dの約数ではありません。\n",b,a);
      }
    }else{
      if(b%a==0){
	printf("%dは%dの約数です。\n",a,b);
      }else{
	printf("%dは%dの約数ではありません。\n",a,b);
      }
    }printf("[続ける:１終了:０]:");
    scanf("%d",&c);
    if(c==0)break;
  }
  return 0;
}
