#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/* (1) reverse words in line except for last word and (2) replace spaces with '|'
E.g.,

293 1273 12541 49600 65535 213.170.59.0/24
65535|49600|12541|1273|293|213.170.59.0/24

gunzip < 2015.allpaths.gz | time ./a.out | gzip -1 > 2015.allpaths2.gz
proc-allpaths1.c: 467.73user 12.61system 8:01.31elapsed 99%CPU (0avgtext+0avgdata 544maxresident)k
proc-allpaths2.c: 414.63user 12.56system 7:09.26elapsed 99%CPU (0avgtext+0avgdata 536maxresident)k
proc-allpaths3.c: 341.47user 11.39system 6:02.28elapsed 97%CPU (0avgtext+0avgdata 512maxresident)k
-O3 proc-allpaths3.c - gzip -1 dominates CPU now!:
                  245.47user 11.34system 5:12.91elapsed 82%CPU (0avgtext+0avgdata 512maxresident)k
gunzip < 2015.allpaths.gz | time ./a.out > /dev/null
                  249.57user 5.97system 4:15.56elapsed 99%CPU (0avgtext+0avgdata 516maxresident)k


*/

#define LINELEN 32768

int main () {
  int maxwords=2;
  char **words = calloc(sizeof(char *), maxwords);
  char line[LINELEN];
  char *s;
  int w, i;

  while (fgets(line, LINELEN, stdin) != NULL) {
    /* make one forward pass through the line to find word boundaries
       save pointer to next character
    */
    for (w=1, s=line, words[0]=line; *s != 0; ++s) {
      /* if we have a space (not just before EOL) */
      if (*s == ' ' && *(s+1) != 0) {
	words[w++]=(s+1);	/* save next position */
	if (w >= maxwords) {
	  maxwords *= 2;	/*  double word limit */
	  if ((words = realloc(words, sizeof(char *) * maxwords)) == NULL) {
	    fprintf(stderr, "no memory for %d more words\n", maxwords);
	    exit(1);
	  }
	  /* else
	     fprintf(stderr, "doubled # words to %d\n", maxwords); */
	}
      }
    }

    if (w) { 			/* find any words? */
      int n;
      /* print reverse order, except last */
      for (i=w-2; i >= 0; --i) {
	/* printf("%.*s|", (int)(words[i+1] - words[i] -1),  words[i]); */
	for (n=0; n < (int)(words[i+1] - words[i] - 1); ++n)
	  putchar(*(words[i]+n));
	putchar('|');
      }
      fputs(words[w-1], stdout); /* print the last word (has trailing nl) */
    }
  }
  
  return(0);
}
