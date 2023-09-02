# distutils: language=c++
# cython: language_level=3
import requests
from bs4 import BeautifulSoup
import cython


@cython.annotation_typing(True)
def extract_blog_posts(content):
    soup = BeautifulSoup(content, 'html.parser')
    blog_posts = soup.find_all('article', class_='archive__item')

    for post in blog_posts:
        """
        <h2 class="archive__item-title no_toc" itemprop="headline">
<a href="/function-calling-openai/" rel="permalink">Demystifying Function Calling in OpenAI: An In-Depth Guide
</a>
</h2>
        """
        title = post.find('h2', class_='archive__item-title').text.strip()
        link = post.find('a')['href']
        print(f'Title: {title}\nLink: {link}\n')


@cython.annotation_typing(True)
def extract_url(url):
    response = requests.get(url)
    extract_blog_posts(response.text)
