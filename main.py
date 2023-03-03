import requests
import time
import os
import math
from loguru import logger
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import gui


# function that returns a fraction of specified number "n"
def get_fraction(n, fraction):
    n = math.ceil(n * fraction)
    return n


# function that pushes element into counting summary list
def summary_push(elem):
    if summary_dict.get(elem) is not None:
        summary_dict[elem] += 1
    else:
        summary_dict[elem] = 1


# clear log if exist
if os.path.isfile("log.log"):
    os.remove("log.log")

# initial variables
summary_dict = {}
user_agent = UserAgent()
headers = {
    "Accept": "*/*",
    "User-Agent": user_agent.random
}

# preparing logging
logger.add("log.log", format="{time}   | {level} |   {message}", level="DEBUG")


# main function of parsing algorithm
@logger.catch
def get_statistics():
    global summary_dict
    # deleting output frame if exists
    gui_app.clear_output()
    # creating waiting message
    gui_app.create_waiting()
    # getting response
    search_request = gui_app.string_entry.get()
    logger.info(f'Search request: {search_request}')
    url = f'https://hh.ru/search/vacancy?text={search_request}&area=2'
    response = requests.get(url, headers=headers)
    src = response.text

    # saving html into file
    with open("page.html", 'w') as file:
        file.write(src)
    with open("page.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    # getting a number of amount of all pages
    try:
        pager = soup.find(class_="pager")
        last_page = pager.findChildren('span', recursive=False)[-1]
        last_page_num = int(last_page.find('a').text)
    except AttributeError:
        last_page_num = 1

    # last pages are usually irrelevant, so only 2/3 of all pages will be considered
    num_of_pages = get_fraction(last_page_num, 2 / 3)
    logger.info(f'Total num of pages: {last_page_num}')
    logger.info(f'Pages to be considered: {num_of_pages}')

    # considering progress bar, 20 vacancies on each page
    vacancies = None
    if last_page_num == 1:
        vacancies = soup.findAll('a', class_="serp-item__title")
        num_of_vacancies = len(vacancies)
        gui_app.set_max_value_progress_bar(num_of_vacancies)
    else:
        gui_app.set_max_value_progress_bar(20 * num_of_pages)
    progress_step = 0

    # going through all pages
    for cur_page in range(num_of_pages):
        url = f'https://hh.ru/search/vacancy?text={search_request}&area=2&page={cur_page}'
        if vacancies is None:
            response = requests.get(url, headers=headers)
            src = response.text
            with open("page.html", 'w') as file:
                file.write(src)
            with open("page.html") as file:
                src = file.read()
            soup = BeautifulSoup(src, "lxml")
            vacancies = soup.findAll('a', class_="serp-item__title")

        logger.info(f'Currently on page {cur_page + 1}: {response.url}')
        vacancies_url_list = []
        for vacancy in vacancies:
            vacancies_url_list.append(vacancy['href'])

        time.sleep(1)
        # going through all vacancies on current page
        for vacancy_url in vacancies_url_list:
            response = requests.get(vacancy_url, headers=headers)
            logger.info(f'Current vacancy: {response.url}')
            src = response.text

            # saving html into file
            with open("vacancy.html", 'w') as file:
                file.write(src)
            with open("vacancy.html") as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            keywords = soup.findAll(class_=["bloko-tag__section", "bloko-tag__section_text"])
            for keyword in keywords:
                summary_push(keyword.text)
            # updating progress bar
            progress_step += 1
            gui_app.set_progress_bar(progress_step)
            time.sleep(1)

    # deleting html files
    if os.path.isfile("page.html") and os.path.isfile("vacancy.html"):
        os.remove("page.html")
        os.remove("vacancy.html")
    # preparing data to user
    gui.remove_deviations(summary_dict, 2)
    summary_dict = dict(sorted(summary_dict.items(), key=lambda item: item[1], reverse=True))
    # deleting waiting message
    gui_app.destroy_waiting()
    # showing output frame with summary_dict info
    gui_app.show_results(summary_dict)
    # adding summary_dict info into log
    logger.info(f'Result: {summary_dict}')
    # summary_dict should be reset
    summary_dict = {}


# showing gui window
gui_app = gui.ParserApp(get_statistics)
gui_app.show()
