#include  <stdio.h>
int main (void)
{
  int n;
  printf("西暦(1868年以降)を入力してください:");
  scanf("%d",&n);
  if(1868<=n&&n<=1911){
    if(n-1868){
      printf("%d年は明治%d年です。\n",n,n-1867);
    }else{
      printf("1868年は明治元年です。\n");
    }
  }

  if(1912<=n&&n<=1925){
    if(n-1912){
      printf("%d年は大正%d年です。\n",n,n-1911);
    }else{
      printf("1912年は大正元年です。\n");
    }
  }

  if(1926<=n&&n<=1988){
    if(n-1926){
      printf("%d年は昭和%d年です。\n",n,n-1925);
    }else{
      printf("1926年は昭和元年です。\n");
    }
  }

  if(1989<=n&&n<=2018){
    if(n-1989){
      printf("%d年は平成%d年です。\n",n,n-1988);
    }else{
      printf("1989年は平成元年です。\n");
    }
  }

  if(2019<=n){
    if(n-2019){
      printf("%d年は令和%d年です。\n",n,n-2018);
    }else{
      printf("2019年は令和元年です。\n");
    }
  }

  return 0;
}
