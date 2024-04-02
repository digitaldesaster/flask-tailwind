import os
import requests
from datetime import datetime
import parse_html

def re_format(results):
  article_list=[]
  now = datetime.now()
  date_format = '%d.%m.%Y %H:%M'
  published = now.strftime(date_format)
  for result in results:
    article = {}
    article['title']=result['title']
    article['link']=result['url']

    try:
      snippet = result['snippet'].split('...')[1].strip()+'...'
    except:
      snippet = result['snippet']
    article['description']=snippet
    article['source']=result['source']
    article['category']='Google'
    article['published']=published
    article['article']=''
    article['article_html']=' '

    article['relevance']=5
    article_list.append(article)
  return article_list


def search(question, num_results=10, days=5, start=0):
    # Read API key and cx from environment variables
    google_search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    google_cse_id = os.getenv("GOOGLE_CSE_ID")

    # API endpoint and parameters
    url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {
        "q": question,
        "key": google_search_api_key,
        "cx": google_cse_id,
        "lr": "lang_de",
        "gl": "de",
        "dateRestrict" : "d" + str(days),
        "num": num_results,  # Get the specified number of search results
        "googlehost": "google.de",  # Search on google.de domain
        "cr": "countryDE",  # Restrict search to Germany
        "start": start  # The index to start the search results from
    }

    # Make request to API and extract news results
    response = requests.get(url, params=params).json()

    # Check if the "items" key exists in the response
    if "items" in response:
        results = response["items"]
    else:
        results = []

    # Extract article URL, title, snippet, source, and image URL for each search result and store in list
    news_results = []
    for result in results:
        news_result = {
            "url": result["link"],
            "title": result["title"],
            "snippet": result["snippet"],
            "source": result["displayLink"]
        }

        # Extract image URL if available
        if "pagemap" in result and "cse_image" in result["pagemap"]:
            news_result["image_url"] = result["pagemap"]["cse_image"][0]["src"]

        news_results.append(news_result)

    return news_results

def handle_search_results(question, num_results, days):
    # Calculate the number of requests needed to get all search results
    num_requests = (num_results - 1) // 10 + 1

    # Make the necessary requests to get all search results
    all_news_results = []
    for i in range(num_requests):
        # Get the current batch of search results
        start_index = i * 10
        num_results_current_request = min(num_results - len(all_news_results), 10)
        news_results = search(question, num_results_current_request, days, start=start_index)

        # If we don't get any results from the current request, break out of the loop early
        if not news_results:
            break

        # Add the current batch of search results to the list of all results
        all_news_results += news_results

        # Break out of the loop if we've gotten all the requested search results
        if len(all_news_results) == num_results:
            break

    # If we didn't get any search results, print a message and return early
    if not all_news_results:
        print("No search results found.")
        return

    # Print all search results
    #for i, result in enumerate(all_news_results):
        #print(f"Result {i+1}:")
        #print(f"Title: {result['title']}")
        #print(f"URL: {result['url']}")
        #print(f"Source: {result['source']}")
        #print(f"Snippet: {result['snippet']}")

        # Print image URL if available
        #if "image_url" in result:
        #print(f"Image URL: {result['image_url']}")

        #print()
    return all_news_results

for result in search('xiaomi su7'):
  article = parse_html.parse_web_page(result['url'])
  print (article)
  

#data = handle_search_results('FCBayern', 10, 2)
#for x in data:
#  print (x['url'])
#  print (x['title'])
