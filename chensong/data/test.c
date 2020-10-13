#include<stdio.h>
const int t = 3;
int add_fun(int para_1,int para_2)
{
    return para_1+para_2;
}
int Demo(int e,int f){
    int t1;
    t1 = add_fun(e,f);
	return t1;
}

void main(){
	int a,b,cc;
	a = 1;
	b = 2;
	cc = Demo(a,b);
}