#include <stdio.h>
#include "bgpstream.h"




int main()
{
  /* Allocate memory for a bgpstream instance */
  bgpstream_t *bs = bs = bgpstream_create();
  if(!bs) {
    fprintf(stderr, "ERROR: Could not create BGPStream instance\n");
    return -1;
  }

  /* Allocate memory for a re-usable bgprecord instance */
  bgpstream_record_t *bs_record = bgpstream_record_create();
  if(bs_record == NULL)
    {
      fprintf(stderr, "ERROR: Could not create BGPStream record\n");
      return -1;
    }

  /* The broker interface is set by default */

  /* Select bgp data from RRC06 and route-views.jinx collectors only */
  bgpstream_add_filter(bs, BGPSTREAM_FILTER_TYPE_COLLECTOR, "rrc19");
  bgpstream_add_filter(bs, BGPSTREAM_FILTER_TYPE_COLLECTOR, "route-views.linx");

  //bgpstream_add_filter(bs, BGPSTREAM_FILTER_TYPE_COLLECTOR, "route-views4");

  //bgpstream_add_filter(bs, BGPSTREAM_FILTER_TYPE_ELEM_IP_VERSION, "4");

  /* Process updates only */
  bgpstream_add_filter(bs, BGPSTREAM_FILTER_TYPE_RECORD_TYPE, "updates");

  /* Select a time interval to process:
   * Sun, 10 Oct 2010 10:10:10 GMT -  Sun, 10 Oct 2010 11:11:11 GMT */
  bgpstream_add_interval_filter(bs,1286705410,1286709071);

  /* Start bgpstream */
  if(bgpstream_start(bs) < 0) {
    fprintf(stderr, "ERROR: Could not init BGPStream\n");
    return -1;
  }

  int get_next_ret = 0;
  int elem_counter = 0;

  /* Pointer to a bgpstream elem, memory is borrowed from bgpstream,
   * use the elem_copy function to own the memory */
  bgpstream_elem_t *bs_elem = NULL;
  
  char buf[4096] = "";
  char pfx_buf[128] = "";
  bgpstream_addr_storage_t  *ip_addr_strg=NULL;
  bgpstream_addr_version_t ver;
  int ip_version=0;
  

  /* Read the stream of records */
  do
    {
      /* Get next record */
      get_next_ret = bgpstream_get_next_record(bs, bs_record);
      /* Check if there are new records and if they are valid records */
      if(get_next_ret && bs_record->status == BGPSTREAM_RECORD_STATUS_VALID_RECORD)
        {
	  //fprintf(stderr, "********************************** A VALID RECORD............................\n");
          /* Get next elem in the record */
          while((bs_elem = bgpstream_record_get_next_elem (bs_record)) != NULL)
            {
	      ip_addr_strg=(bgpstream_addr_storage_t *)&bs_elem->peer_address;
	      ver=ip_addr_strg->version;
	      ip_version=bgpstream_ipv2number(ver);
	      //fprintf(stderr,"IP Version = %d\n", ip_version);
	      if (ip_version==4){
		if (bgpstream_as_path_snprintf(buf, 4096, bs_elem->aspath) < 4096)
		  {
		    if (buf && buf[0]){
		      //fprintf(stderr, "Very long path.....\n");
		      //}
		      //else
		      //{
		      bgpstream_pfx_snprintf(pfx_buf, 128, (bgpstream_pfx_t *)&bs_elem->prefix);
		      //fprintf(stderr, "IP Version:  IPv%d\n",bgpstream_ipv2number((bgpstream_pfx_t *)&bs_elem->prefix->address));
		      fprintf(stderr, "%s %s\n",buf,pfx_buf);
		      //reverse(buf);
		      //fprintf(stderr, "%s %s\n",buf,pfx_buf);
		    }
		  }
		//elem_counter++;
	      }
	    }
        }
    }
  while(get_next_ret > 0);

  /* Print the number of elems */
  // printf("\tRead %d elems\n", elem_counter);

  /* De-allocate memory for the bgpstream record */
  bgpstream_record_destroy(bs_record);

  /* De-allocate memory for the bgpstream */
  bgpstream_destroy(bs);

  return 0;
}

/*

 
int string_length(char *pointer)
{
   int c = 0;
 
   while( *(pointer + c) != '\0' )
      c++;
 
   return c;
}



void reverse(char *string) 
{
   int length, c;
   char *begin, *end, temp;
 
   length = string_length(string);
   begin  = string;
   end    = string;
 
   for (c = 0; c < length - 1; c++)
      end++;
 
   for (c = 0; c < length/2; c++)
   {        
      temp   = *end;
      *end   = *begin;
      *begin = temp;
 
      begin++;
      end--;
   }
}



*/
