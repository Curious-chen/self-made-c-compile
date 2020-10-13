%{
#include<math.h>
#include<stdlib.h>
#include<stdio.h>
%}
DIGIT [0-9]
ID [a-z][a-z0-9]* 
%%
{DIGIT}+ {printf("整数: %s(%d)\n",yytext,atoi(yytext);} 
{DIGIT}+"."+{DIGIT}* {printf("整数: %s(%d)\n",yytext,atoi(yytext);}
auto|int|double|long|char|float|short|signed|unsigned|struct|union|enum|static|switch|case|default|
break|register|const|volatitle|typedef|extern|void|continue|do|while|if|else|for|goto|sizeof {
		printf("关键字: %s\n",yytext);
		}
{ID} {printf("标识符：%s\n",yytext}
"("|")"|"["|"]"|"->"|"!"|"~"|"++"|"--"|"+"|"-"|"*"|"&"|"/"|"%"|"."|"<<"|">>"|"<"|"<="|">"|">="|"=="|"!="|"|"|"&&"|"||"|"="|"+="|"-="|"/="|"&="|"%="|"^="|"|="|"<<="|">>="|"**"|{
		printf("运算符: %s\n",yytext);
		}
//[^\n]* /*删除单行注释*/
[\t\n\x20]+
. {printf("不能识别的字符：%s\n",yytext);}
%%
int main(int argc,char *argv[])
{
	++argv;--argc;
	if(argc>0) yyin = fopen(argv[0],"r");
	else yyin = stdin;
	yylex();
	return 0;
}
int yywrap()
{
	return 1;
}