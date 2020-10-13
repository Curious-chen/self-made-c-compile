#include<stdio.h>
int add_fun(int e,int f)
{
    return e+f;
}
int main()
{
    int i,j;
    i = 3+4/2-2*2;
    j = 2;
    if(i>j)
    {
        i = add_fun(i,j)
    }
    else
    {
        j = add_fun(i,j);
        do
        {
            j = j -1;
        }
        while(j<2);

    }
    for(i=0;i<10;i=i+1)
    {
        j = add_fun(i,j);
    }
}