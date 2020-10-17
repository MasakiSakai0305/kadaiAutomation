#include <stdio.h>
int main(void)
{
  int x;
  printf("正の整数を入力してください：");
  scanf("%d",&x);
  if(x<=0){
    printf("%dは正の整数ではありません。\n",x);
  }else if(x%2==0){
    printf("%dは偶数です。\n",x);
  }else{
    printf("%dは奇数です。\n",x);
  }
  return 0;
}
