#include <stdio.h>
int main(void)
{
  int x;
  printf("西暦（1582年以降）を入力してください：");
  scanf("%d",&x);
  if(x%4==0){
    if(x%100==0){
      if(x%400==0){
	printf("%d年は閏年です。\n",x);
      }else{
	printf("%d年は閏年ではありません。\n",x);
      }
    }else{
      printf("%d年は閏年です。\n",x);
    }
  }else{
    printf("%d年は閏年ではありません。\n",x);
  }
  return 0;
}
