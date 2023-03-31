import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewlist = []

'''
def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
'''


def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
                'product': soup.title.text.replace('Amazon.co.uk:Customer reviews:', '').strip(),
                'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'rating': float(
                    item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except():
        pass


for x in range(1, 999):
    '''
    soup = get_soup(
        f'https://www.amazon.co.uk/product-reviews/B07WD58H6R/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    '''
    source = requests.get(
        'https://www.amazon.co.uk/product-reviews/B07WD58H6R/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}'
    )

    source.raise_for_status()

    soup = BeautifulSoup(source.text, 'html.parser')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

df = pd.DataFrame(reviewlist)
df.to_excel('sony-headphones.xlsx', index=False)
print('Fin.')

"""
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
headers = {"Accept-Language": "en-US, en;q=0.5"}
results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

#initiate data storage
titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')

#our loop through each container
for container in movie_div:

        #name
        name = container.h3.a.text
        titles.append(name)
        
        #year
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        # runtime
        runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime').text else '-'
        time.append(runtime)

        #IMDb rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        #metascore
        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(m_score)

        #there are two NV containers, grab both of them as they hold both the votes and the grosses
        nv = container.find_all('span', attrs={'name': 'nv'})
        
        #filter nv for votes
        vote = nv[0].text
        votes.append(vote)
        
        #filter nv for gross
        grosses = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(grosses)

#pandas dataframe        
movies = pd.DataFrame({
'movie': titles,
'year': years,
'timeMin': time,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
'us_grossMillions': us_gross,
})

#cleaning data 
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(int)
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')

#add dataframe to csv file named 'movies.csv'
movies.to_csv('movies.csv')
"""
