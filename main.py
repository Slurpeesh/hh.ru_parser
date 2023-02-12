import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# function that removes dictionary keys which values are less or equal to "n"
def remove_deviations(dictionary, n):
    keys_for_deleting = []
    for k, v in dictionary.items():
        if v <= n:
            keys_for_deleting.append(k)
    for k in keys_for_deleting:
        del dictionary[k]


# function that returns a fraction of specified number "n"
def get_fraction(n, fraction):
    n = round(n * fraction)
    return n


# function that pushes element into counting summary list
def summary_push(elem):
    if summary_dict.get(elem) is not None:
        summary_dict[elem] += 1
    else:
        summary_dict[elem] = 1


# initial variables
summary_dict = {}
user_agent = UserAgent()
headers = {
    "Accept": "*/*",
    "User-Agent": user_agent.random
}

# getting response
search_request = input("Input search request: ")
url = f'https://hh.ru/search/vacancy?text={search_request}&area=2'
request = requests.get(url, headers=headers)
src = request.text

# saving html into file
with open("page.html", 'w') as file:
    file.write(src)
with open("page.html") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

# getting a number of amount of all pages
last_page = soup.find(class_=["bloko-gap", "bloko-gap_top"]).findAll(class_="pager-item-not-in-short-range")[-1]
last_page_num = int(last_page.find('a').text)

# last pages are usually irrelevant, so only 2/3 of all pages will be considered
num_of_pages = get_fraction(last_page_num, 2 / 3)

# going through all pages
for cur_page in range(num_of_pages):
    print("Currently on page", cur_page + 1,
          f'https://hh.ru/search/vacancy?text={search_request}&area=2&page={cur_page}')
    url = f'https://hh.ru/search/vacancy?text={search_request}&area=2&page={cur_page}'
    request = requests.get(url, headers=headers)
    with open("page.html", 'w') as file:
        file.write(src)
    with open("page.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    vacancies = soup.findAll('a', class_="serp-item__title")
    vacancies_url_list = []
    for vacancy in vacancies:
        vacancies_url_list.append(vacancy['href'])

    time.sleep(1.5)
    # going through all vacancies on current page
    for vacancy_url in vacancies_url_list:
        print("Current vacancy:", vacancy_url)
        request = requests.get(vacancy_url, headers=headers)
        src = request.text

        # saving html into file
        with open("vacancy.html", 'w') as file:
            file.write(src)
        with open("vacancy.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        keywords = soup.findAll(class_=["bloko-tag__section", "bloko-tag__section_text"])
        for keyword in keywords:
            summary_push(keyword.text)
        time.sleep(1.5)

# preparing data to user
remove_deviations(summary_dict, 1)
summary_dict = dict(sorted(summary_dict.items(), key=lambda item: item[1], reverse=True))
print(summary_dict)
