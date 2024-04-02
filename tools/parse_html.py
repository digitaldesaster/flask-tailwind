
from newspaper import Article
import rss_config
import nltk
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from readabilipy import simple_json_from_html_string

nltk.download('punkt')

from bs4 import BeautifulSoup


def fixSomeHTML(html, remove_img=False, lib='html5lib'):
  #change the h-tags to h5
  for tag_name in ['h1', 'h2', 'h3']:
    html = html.replace(tag_name, 'h5')
  html = html.replace('<p>Skip to main content</p>', '')

  try:
    soup = BeautifulSoup(html, lib)
  except:
    #print(html)
    return (html)

  # Remove all links and keep only the text inside them
  # reason is that the full url is missing
  for tag in soup.find_all():
    if tag.name == 'a' or tag.find_parent('a'):
      tag.replace_with(tag.text)

  # Remove all images if remove_img is True
  if remove_img:
    images = soup.find_all('img')
    for image in images:
      image.extract()

  # Extract the contents of the 'body' tag
  try:
    result_html = ''.join(str(content) for content in soup.body.contents)
    return result_html
  except:
    return html

def parse_web_page(link,category="Search"):
  article = get_article(link)
  result={}
  now = datetime.now()
  date_format = '%d.%m.%Y %H:%M'
  result['title'] = article.title
  result['description']=article.summary
  result['category']=category
  result['published'] = now.strftime(date_format)
  result['link'] = link
  result['source']=category
  result['article']=article.text
  result['article_html']=article.article_html
  result['relevance']=5
  article, result = check_article(article,result)  
  return result



def readability_py(url):
  req = requests.get(url)
  article = simple_json_from_html_string(req.text, use_readability=True)
  return article


def get_article(url, write_new=False):
  article = Article(url, language='de', keep_article_html=True)
  article.download()
  article.parse()
  article.nlp()
  #if write_new:
  #  article.text = writeNewArticle(article.text)
  #else:
  #article.text=readability_api(url)

  return article

def check_article(article,result):
  if article.text != None and article.text != '' and article.text !='None':
    result['article'] = article.text
    result['article_html'] = fixSomeHTML(article.article_html,remove_img=True)
  else:
    py_article = readability_py(result['link'])
    result['article'] = ''
    result['article_html'] = fixSomeHTML(py_article['plain_content'])
  return article,result


#def writeNewArticle(text):
  #system_message, prompt = rss_config.write_new_prompt()

  #data, message = chat_gpt.askChatGPT(prompt + text, system_message)
  #return message
