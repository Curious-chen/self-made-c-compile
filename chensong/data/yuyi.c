const int a = 12, b = 13;
const char k = 'b';
// b,a重复定义
const double b = 12.5, a = 4.1, t = 5.54;
int globa_a;
double if_fuc(int a, int b)
{
	//b重复定义
	int b, c;
	if(a>b)
	{
		c=1;
	}
	else
	{
		c=2;
	}
	return a + c;
}
void loop_fun(int a, int b, int c)
{
	int i = 0, j = 0;
	for(i = 0; i < 10; i++)
	{
		for(j = 0; j < 10; j++)
		{
			if(j < b)
			{
				break;
			}
		}
		if(a > i)
		{
			break;
		}
		else
		{
			continue;
		}
	}
	switch(b)
	{
		case 1 : a = c; break;
		case 2 : break;
		//continue使用错误
		case 3 : continue;
	}
	while(c > 0)
	{
		if(c > 10)
		{
			break;
		}
		else
		{
			c--;
		}
	}
	//break使用错误
	break;
}
//函数名重复定义
void if_fuc()
{
	int c;
	if(c > 0)
	{
		c = 0;
	}
	else
	{
		c = 1;
	}
}
//函数名与全局变量名相同
void a()
{
	//break使用错误
	break;
}
double return_test()
{
	return 1;
}
int main()
{
	int accc;
	int a=10;
	int b=20, y = 8, k = 6;
	//b重复定义
	int b=12;
	double e = 11;
	loop_fun(accc, a, b);
	loop_fun(accc, a, e);
	loop_fun(accc, a);
	loop_f();
	accc = a + k;
	accc = a - e;
	if(a<b)
	{
		if(a == b)
		{
			//c未定义就使用
			c = 12;
			//continue使用错误
			continue;
		}
		else
		{
			c = 2;
		}
	}
	else
	{	
		int d;
		//错误赋值
		5 = a + b;
	}
	return 0;
}