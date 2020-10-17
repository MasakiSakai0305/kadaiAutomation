#include <stdio.h>
int main(void)
{
  int money,zeikomi;
  printf("金額を入力してください。：")
  scanf("%d",&money);
  zeikomi=money*1.1;
  printf("消費税を含めた金額は%d円です。\n",zeikomi);
  return 0;
}
