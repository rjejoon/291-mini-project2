#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


char** filterTerms(char*);

char** filterTerms(char s[])
{

    if (strlen(s) == 0) 
        return NULL;

    int n = 100;
    int curr = 0;
    char** terms = calloc(n, sizeof(char *));
    int start, i = 0;
    for (; i<strlen(s); i++) 
    {
        if (isalnum(s[i]) && i - start >= 3) 
        {
            char temp[i - start];
            int pp = 0;
            for (int j = start; j < i; j++) 
                temp[pp++] = tolower(s[j]);

            terms[curr++] = temp;
            if (curr == n)
            {
                n *= 2;
                terms = realloc(terms, n * sizeof(char *));
            }
        }
    }
    if (isalnum(s[--i]) && i+1 - start >= 3)
    {
        char temp[i - start];
        int pp = 0;
        for (int j = start; j < i; j++) 
            temp[pp++] = tolower(s[j]);

        terms[curr] = temp;
    }


    return terms;
}

int main() {
    char* s = "<abc><def>";
    char** terms = filterTerms(s);
    for (int i=0; terms[i] != 0; i++)
        printf("%s \n", terms[i]);
}


