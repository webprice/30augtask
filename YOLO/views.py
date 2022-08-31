from django.shortcuts import render,redirect
from django.conf import settings
from django.http import JsonResponse
from YOLO.models import Data
import requests, random
import concurrent.futures
from bs4 import BeautifulSoup


#This function will be a decorator, checking if user logged in or not
def require_login(func):
    def login_result(request, *args, **kwargs):
        if not request.user.is_authenticated:
            print("user is not logged in, redirected: ",{request})
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            print(f"user: {request.user.username} logged in, return views function: {func.__name__}")
            return func(request, *args, **kwargs)
    return login_result


#Index.html function, send the user role in context.
#Role needed to display specific parts of HTML code via DJANGO Tags
@require_login
def index(request):
    role = None
    if request.user.groups.filter(name='hundred').exists():
        role = 'hundred'
    if request.user.groups.filter(name='twohundred').exists():
        role = 'twohundred'
    if request.user.groups.filter(name='threehundred').exists():
        role = 'threehundred'
    return render(request,'index.html',context = {'role':role})


#The trigger function/route. When user clicking on "refresh button" - load_data invokes
#it checks the user group, then cleaning the DB, triggering the next function "get_links"
#after success - grabs the new data from the DB, converts it to list and return it as a JSON response
#Finally JS script on the front-end parsing that JSON data and build HTML table out of it.
@require_login
def load_data(request):
    if request.user.groups.filter(name='hundred').exists():
        # delete all data
        Data.objects.all().delete()
        # invoke scrape
        get_links('hundred')
        # send the new data to the front
        data = list(Data.objects.values('id', 'title', 'price', 'photo', 'seller').order_by('id')[:100])
    if request.user.groups.filter(name='twohundred').exists():
        # delete all data
        Data.objects.all().delete()
        # invoke scrape
        get_links('twohundred')
        # send the new data to the front
        data = list(Data.objects.values('id', 'title', 'price', 'photo', 'seller').order_by('id')[:200])
    if request.user.groups.filter(name='threehundred').exists():
        # delete all data
        Data.objects.all().delete()
        # invoke scrape
        get_links('threehundred')
        # send the new data to the front
        data = list(Data.objects.values('id', 'title', 'price', 'photo', 'seller').order_by('id')[:300])
    #qs_json = serializers.serialize('json', data)
    return  JsonResponse(data,safe=False)


#Shows the existing data from the database.
#This function invoke by clicking on "existing data" button on the front-end
@require_login
def existing_data(request):
    if request.user.groups.filter(name='hundred').exists():
        data = list(Data.objects.values('id', 'title', 'price', 'photo', 'seller').order_by('id')[:100])
    if request.user.groups.filter(name='twohundred').exists():
        data = list(Data.objects.values('id', 'title', 'price', 'photo', 'seller').order_by('id')[:200])
    if request.user.groups.filter(name='threehundred').exists():
        data = list(Data.objects.values('id', 'title', 'price', 'photo', 'seller').order_by('id')[:300])
    #qs_json = serializers.serialize('json', data)
    return  JsonResponse(data,safe=False)


#Removed the row from the database by it's <id>
#This function invoke by clicking on "delete" button in the table at the front-end
@require_login
def test_delete(request,id):
    Data.objects.filter(id=id).delete()
    data = list(Data.objects.values('id', 'title', 'price', 'photo', 'seller').order_by('id'))
    return  JsonResponse(data,safe=False)


''' Scrapper functions code next '''

BASE_URL = 'https://www.olx.ua'
UA_LIST = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


def headers():
    # Pick a random user agent
    user_agent = random.choice(UA_LIST)
    # Set the headers
    headers = {'User-Agent': user_agent}
    return  headers


#global var for counting number of items that will be scrapped from the OLX
COUNTER = 0


#Before start scraping - form the list of links of pages' links
#hardcoded
#this list will be set to run in the threadpoolexecutor and send as an argument to the next function:"get_ad_list"
def get_links(group):
    global COUNTER
    url_list = []
    pages = 0
    if group == "hundred":
        pages = 3
        COUNTER = 100
    if group == "twohundred":
        pages = 5
        COUNTER = 200
    if group == "threehundred":
        pages = 7
        COUNTER = 300
    for each in range(pages):
        #print(each)
        url_list.append(f'https://www.olx.ua/d/uk/transport/?page={each+1}')
    print(url_list)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_ad_list, url_list)
    return None


#Here we scrapping all the links to the individual Ads(posts)
#COUNTER controlling(according to the accounts' types) how many links the request gonna get in the next function
def get_ad_list(page_url):
    global COUNTER
    title_urls = []
    # for link in page_url:
    page = requests.get(page_url, headers=headers())
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find_all('div',attrs={'data-cy':'l-card'})
    #print(len(items))
    for item in items:
            if COUNTER < 0:
                break
            link = item.a.get('href')
            if not link.startswith('https://'):
                title_urls.append(link)
                COUNTER -=1
    print(len(title_urls))
    with concurrent.futures.ThreadPoolExecutor() as executor2:
        executor2.map(get_final, title_urls)
    return None


#Here we get the data from the individual Ad(post), parsing it and saving it to the DataBase
def get_final(url):
    page = requests.get(f'{BASE_URL}{url}', headers=headers())
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find(id='root')
    xxx = items.find_all('div', {'class': 'swiper-zoom-container'}, limit=1)
    title = items.h1.get_text()
    seller = items.h4.get_text()
    price =items.h3.get_text()
    photo = xxx[0].find_next('img')['src']
    try:
        dataload = Data(
            title=title,
            price=price,
            photo=photo,
            seller=seller,
        )
        dataload.save()
    except Exception as e:
        print(e)
    return None
    # print(title)
    # print(seller)
    # print(price)
    # print(photo)