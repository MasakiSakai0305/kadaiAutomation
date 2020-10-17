#include <stdio.h>

int main(void){
  int x;
  printf("金額を入力して下さい：");
  scanf("%d",&x);
  x = x*1.1;
  printf("消費税を含めた金額は%d円です\n",x);
  return 0;
}
