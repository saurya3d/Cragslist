from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.utils import requote_uri
from . import models

# Create your views here.
BASE_CRAGSLIST_URL = 'https://pune.craigslist.org/d/for-sale/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # print(requote_uri(search))

    final_url = BASE_CRAGSLIST_URL.format(requote_uri(search))
    # print(final_url)
    response = requests.get(final_url)
    data = response.text
    # print(data)
    soup = BeautifulSoup(data, features='html.parser')

    post_listing = soup.find_all('li', {'class': 'result-row'})
    # post_titles = post_listing[0].find(class_= 'result-title').text
    # post_url = post_listing[0].find('a').get('href')
    # post_price = post_listing[0].find(class_= 'result-price').text

    # print(post_titles)
    # print(post_url)
    # print(post_price)

    final_postings = []
    for post in post_listing:
        post_titles = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(':')[1].replace(",3", "")
            print(post_image_id)
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_titles, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)
