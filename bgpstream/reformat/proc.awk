{ # reverse-print the first n-1 words
  for (i=NF-1; i > 0; --i)
    printf("%s|", $i);
  # print last word
  print $NF
}
