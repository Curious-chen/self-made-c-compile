// 单行注释
/*
多行注释
*/
const int a_global = 2;
const int b_global = 3;
double c_global = 2.4;
extern unsigned int d_global = 3;
register long e_global = 5;
static short f_global = 2;

void if_fuc()
{
	int a=10;
	int b=1;
	int c;
	if(a>b && a==b)
		c=1;
	else
		c=2;
}

int switch_fuc(int a, int b)
{
	int c;
	a=10;
	switch(a)
	{
		case 1 c=1;break
		case 2 : c=2;break;
		default : c=3;
	}
	return c;
}
void while_fuc()
{
	int a,b;
	a=10;
	b=1;
	while(b<10
	{
		a++;
	}
 }

void do_while_fuc()
{
	int a,b;
	a=10;
	b=1;
	do
	{
		++a;
	}(b<10);
}

int for_fuc()
{
	int ,i;
	a=10;
	for(i=1 i<10;i++)
	{
		a++;
	}
	return a;
}
int main()
{
	int a,b,c;
	float e =0.5;
	char d='2';

	a = 10
	b = 10;
	c = a*b+a-b;
	c *= b;
	c = a|b;
	c = a&b;

	c = !a;
	c = c<<1;
	c = switch_fuc(int a, int b)++;
	c = ++switch_fuc(a,b);
	c = sizeof(switch_fuc(a, b);

	printf ("c=%d\n",c;
	return 1
}
