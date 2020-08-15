import os.path as check
import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def main():
    #url we want to work with
    user_url = None

    while user_url is None:
        user_url = input('Enter desired SlickDeals URL: ')

    #open connection to url, get info, and close connection
    uClient = uReq(user_url)
    page_info = uClient.read()
    uClient.close()

    # parse the html by calling soup function
    page_soup = soup(page_info, 'html.parser')

    # grabs table containing item info
    containers = page_soup.findAll('div', {'class': 'itemImageAndName'})

    user_response = None

    while user_response not in ('1', '2'):
        user_response = input('Create new file (Enter: 1) OR Append to existing (Enter: 2) ?: ')

    if user_response == '1':
        new_file(containers)
    else:
        open_existing(containers)


def new_file(containers):

    filename = None

    while filename is None:
        filename = input('Enter desired file name: ')

    filename = filename.strip().replace(' ', '_') + '.csv'
    f = open(filename, 'w')
    headers = 'Seller, Product_Info, Date, Time\n'
    f.write(headers)

    file_loop_function(f, containers)

    f.close()
    print("Done ----> \'" + filename + "\' was created!")

def open_existing(containers):
    file_exists = False

    while not file_exists:

        filename = input('Enter name of existing csv file to open: ')
        filename = filename.strip().replace(' ', '_') + '.csv'

        file_exists = check.exists(filename)

        if not file_exists:
            print('File \'' + filename + '\' does not exist!')


    f = open(filename, 'a')
    file_loop_function(f, containers)
    f.close()
    print('Done ----> \'' + filename + '\' was appended to!')

def file_loop_function(f, containers):

    # grab item description along with price
    for container in containers:

        # this code is also working now ... not fully content with it yet but it'll work
        # seller = container.a.text.strip()

        # Better code for above BUT gives error... Handles error now :)
        if container.find('a', {'class': 'itemStore bp-p-storeLink bp-c-link'}) is None:
            seller = 'N/A'
        else:
            seller = container.find('a', {'class': 'itemStore bp-p-storeLink bp-c-link'}).text.strip()

        if seller is 'N/A':
            if container.find('button', {
                'class': 'itemStore bp-p-storeLink bp-c-linkableButton bp-c-button--link bp-c-button'}) is None:
                seller = 'N/A'
            else:
                seller = container.find('button', {
                    'class': 'itemStore bp-p-storeLink bp-c-linkableButton bp-c-button--link bp-c-button'}).text.strip()

        # this code gives no errors so we good :)
        if container.div.img is None:
            item_description = 'N/A'
        else:
            item_description = container.div.img['title'].strip()

        # code test for item info
        # NO ERRORS FROM BOTH THIS AND ABOVE CODE
        # item_info = container.find('a', {'class':'itemTitle bp-c-link'}).text.strip()

        # print(seller)
        # print(item_description)
        # print(item_info)

        #Get current time and date
        curr_date = datetime.datetime.now()
        #date = curr_date.strftime('%a-%b-%d-%Y')
        #time = curr_date.strftime('%I:%M:%S %p')

        f.write(seller.replace(',', '|') + ',' + item_description.replace(',', '|') + ',' +
                curr_date.strftime('%a-%b-%d-%Y') + ',' + curr_date.strftime('%I:%M:%S %p') + '\n')


main()
