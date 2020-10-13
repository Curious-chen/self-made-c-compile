void main( )
{
	int a,b,A,B,i;
 	a = 123;
 	b = 100;
 	A= 0;
 	B= 1;
 	if(A && B || (a>b))//将较小的值赋给i
   	{
        i = b;
    }
 	else{
        i = a;
    }
 	while(a > b) 
 	{    
        a = a -1 ;
        if(A && B || (a>b))//将较小的值赋给i
        {
            i = b;
        }
        else{
        i = a;
        }
    }
    do {    
        a = a -1 ;
    } while(a > b);
    i = (a+b)*(B-A)/B;
}