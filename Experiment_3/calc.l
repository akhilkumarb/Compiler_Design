%{

#include<stdio.h>

#include<stdlib.h>

void yyerror(char *);

15

Vishnu Institute of Technology

CSE D

#include "y.tab.h" int yylval;

%}

%%

[a-z] {yylval=*yytext='&'; return VARIABLE;}

[0-9]+ {yylval atoi(yytext); return INTEGER;}

CALC.Y

[\];

%%

int yywrap(void){

return 1;

}

%token INTEGER VARIABLE

%left'+'

%left/

%{

int yylex(void);

void yyerror(char *);

int sym[26];

%}

%%

PROG:

PROG STMT '\n'

STMT: EXPR {printf("\n %d",$1);}

| VARIABLE '=' EXPR {sym[$1] = $3;}

EXPR: INTEGER

| VARIABLE {$$ = sym[$1];}

| EXPR '+' EXPR {$$ = $1 + $3;}

I '('EXPR')' {$$$2;}

%%
void yyerror(char *s){

printf("\n %s",s);

return;

}

int main(void)

{

printf("\n Enter the Expression:");

yyparse();

return 0;

}

Output:

$ lex calc.l

$ yacc -d calc.y

$ ccy.tab.c lex.yy.c-ll-ly-Im

$ ./a.out

Enter the Expression: (5+4)* 3

Answer: 27