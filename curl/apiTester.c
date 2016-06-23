#include <stdio.h>
#include <string.h>
#include <curl/curl.h>

char *replace(char* szData, int nlen, char srcchar, char deschar)
{
  int nIndex = 0;
  char *tmp = szData;
  if (tmp == NULL)
  {
    return NULL;
  }

  while(*tmp != '\0'&& nIndex<nlen)
  {
    if (*tmp == srcchar)
    {
      *tmp = deschar;
    }
    tmp++; 
    nIndex++;
  }       

  return szData;
}

char *getLine(char *szLine, int len)
{
  fgets(szLine, len, stdin);
  if(szLine == NULL)
	return NULL;
  return replace(szLine, len, '\n', '\0');	
} 

int getUrl()
{
  CURL *curl;
  CURLcode res;
  char szLine[1024] = {0};

  curl = curl_easy_init();

  printf("**************get data start*****************\n");
  if (curl)
  {
    struct curl_slist *head_list = NULL;

   /* no progress meter please */ 
   curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);

   /* send all data to this function */ 
   curl_easy_setopt(curl, CURLOPT_WRITEDATA, stdout);

    while(1)
    {
      printf("please input url...\n");
      getLine(szLine, sizeof(szLine));
     
      if(szLine == NULL || strlen(szLine) ==0)
      {
         continue;
      }
      curl_easy_setopt(curl, CURLOPT_URL, szLine);
      break;
    }

    while (1)
    {
       printf("please input a head like {key: value} input empty line to next ...\n");
       getLine(szLine, sizeof(szLine));
      
       if(szLine==NULL|| strlen(szLine) == 0)
       {
          break;
       }
       head_list = curl_slist_append(head_list, szLine);   
    }

    if (head_list != NULL)
    {
       res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, head_list);
    }

    res = curl_easy_perform(curl);
    if (res != CURLE_OK)
    {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }

    /* free the list again */
    if (head_list != NULL)
    {
        curl_slist_free_all(head_list);
    }

    curl_easy_cleanup(curl);
  }
  else
  {
    printf("error:curl_easy_init() failed!!\n");
    return -1;
  }
  return 0;
} 

int postUrl()
{
  CURL *curl;
  CURLcode res;
  char szLine[1024];
  curl = curl_easy_init();

  printf("**************post data start*****************\n");
  if(curl)
  {
    struct curl_slist *head_list = NULL;

    /* no progress meter please */
   curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);

   /* send all data to this function */
   curl_easy_setopt(curl, CURLOPT_WRITEDATA, stdout);
    
    while(1)
    {
        printf("please input url...\n");

        getLine(szLine, sizeof(szLine));
        if(szLine == NULL || strlen(szLine) == 0)
        {
          continue;
        }
        curl_easy_setopt(curl, CURLOPT_URL, szLine);
        break;
    }
    while(1)
    {
       printf("please input a head data format is {key: value}, input empty line to next...\n");
       getLine(szLine, sizeof(szLine));
       if(szLine==NULL || strlen(szLine) == 0)
       {
          break;
       }
       head_list = curl_slist_append(head_list, szLine);
    }

    if(head_list != NULL)
    {
      res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, head_list);
    }

    printf("please input data to post format is: {name=myname&password=pass}\n");
    getLine(szLine, sizeof(szLine));
    if(szLine != NULL && strlen(szLine) != 0)
    {
         curl_easy_setopt(curl, CURLOPT_POSTFIELDS, szLine);
    }

    /* Perform the request, res will get the return code */
    res = curl_easy_perform(curl);
    /* Check for errors */
    if(res != CURLE_OK)
    {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }

    /* free the list again */
    if (head_list != NULL)
    {
        curl_slist_free_all(head_list);
    }

    /* always cleanup */
    curl_easy_cleanup(curl);
  }
  return 0;
}

void testlogin()
{
  CURL *curl;
  CURLcode res;
//  char szLine[1024];
  curl = curl_easy_init();

  printf("**************post data start*****************\n");
  if(curl)
  {
    struct curl_slist *head_list = NULL;

    /* no progress meter please */
   curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);

   /* send all data to this function */
   curl_easy_setopt(curl, CURLOPT_WRITEDATA, stdout);

    while(1)
    {
       
        curl_easy_setopt(curl, CURLOPT_URL, "localhost:8000/login");
        break;
    }
   
    head_list = curl_slist_append(head_list, "Accept: application/json");
    res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, head_list);

    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "username=yang&password=yang&eauth=pam");

    /* Perform the request, res will get the return code */
    res = curl_easy_perform(curl);
    /* Check for errors */
    if(res != CURLE_OK)
    {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }

    /* free the list again */
    curl_slist_free_all(head_list);

    /* always cleanup */
    curl_easy_cleanup(curl);
  }
}

void testPing()
{
  CURL *curl;
  CURLcode res;
  //char szLine[1024];
  curl = curl_easy_init();

  printf("**************post data start*****************\n");
  if(curl)
  {
    struct curl_slist *head_list = NULL;

    /* no progress meter please */
   curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 1L);

   /* send all data to this function */
   curl_easy_setopt(curl, CURLOPT_WRITEDATA, stdout);

   curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:8000");

   head_list = curl_slist_append(head_list, "Accept: application/x-yaml");
   head_list = curl_slist_append(head_list, "X-Auth-Token: 741386db4a746674dc57dfd3b9ee7e264294ea59");
   res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, head_list);    

   curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "client=local&tgt=*&fun=test.ping");

    /* Perform the request, res will get the return code */
    res = curl_easy_perform(curl);
    /* Check for errors */
    if(res != CURLE_OK)
    {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }

    /* free the list again */
    curl_slist_free_all(head_list);

    /* always cleanup */
    curl_easy_cleanup(curl);
  }
}


int main(void)
{
  char szLine[1024];
  /* In windows, this will init the winsock stuff */ 
  curl_global_init(CURL_GLOBAL_ALL);

  while(1)
  {
    printf("\ng:get,p:post,q:quit\n");
    getLine(szLine, sizeof(szLine));
    if(strcmp(szLine, "g") == 0 || strcmp(szLine, "G") == 0)
    {
      getUrl();
    }
    else if(strcmp(szLine, "p") ==0 || strcmp(szLine, "P") == 0)
    {
      postUrl();
    }
    else if(strcmp(szLine, "q") == 0 || strcmp(szLine, "Q") == 0)
    {
      break;
    }
  }
  curl_global_cleanup();
  return 0;
}
