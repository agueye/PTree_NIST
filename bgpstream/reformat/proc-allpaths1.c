#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/* reverse words in line except for last word 
E.g.,

293 1273 12541 49600 65535 213.170.59.0/24
65535|49600|12541|1273|293|213.170.59.0/24


gunzip < 2015.allpaths.gz | time ./a.out | gzip -1 > 2015.allpaths1.gz
467.73user 12.61system 8:01.31elapsed 99%CPU (0avgtext+0avgdata 544maxresident)k
"top" reports:
CPU  process
100% a.out
70%  gzip -1
33%  gzip -d

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
       save pointer at each spot
       for now, replace spaces with nulls for easy printing later (could
       instead just do pointer math to find lengths.
    */
    for (w=0, s=line, words[0]=line; *s != 0; ++s) {
      if (*s == ' ') {
	words[++w]=s;
	if (w >= maxwords) {
	  maxwords *= 2;	/*  double word limit */
	  if ((words = realloc(words, sizeof(char *) * maxwords)) == NULL) {
	    /* fprintf(stderr, "no memory for %d more words\n", maxwords); */
	    exit(1);
	  } else
	    fprintf(stderr, "doubled # words to %d\n", maxwords);
	}

	*s=0;			/* put null in place of space */
      }
    }

    /* print string after each null */
    /* print reverse order, except first (no null before it) and last */
    if (w) { 			/* find any words? */
      for (i=w-1; i > 0; --i)
	printf("%s|", words[i]+1);
      /* first word does not have a null before it, so print it */
      printf("%s|", line);
      fputs(words[w]+1, stdout); /* print the last word (has trailing nl) */
    }
  }
  
  return(0);
}
