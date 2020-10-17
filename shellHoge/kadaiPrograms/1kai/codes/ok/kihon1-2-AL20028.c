#include <stdio.h>

int main (void) {
  int n;
  printf("正の整数を入力してください:");
  scanf("%d",&n);
  if(n<=0){
    printf("%dは正の整数ではありません。\n",n);
  }else{
    if(n%2){
      printf("%dは奇数です。\n",n);
    }else{
      printf("%dは偶数です。\n",n);
    }
  }
  return 0;
}
