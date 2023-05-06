import requests
from bs4 import BeautifulSoup

# set the base URL and headers
base_url = 'https://tabelog.com/kr/fukuoka/rstLst/'
headers = {'User-Agent': 'Mozilla/5.0'}

# create a list to store the data
data_list = []

# loop through each page up to page 5
for page in range(1, 6):
    url = base_url + str(page) + '/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # find all the title elements and extract their text
    titles = soup.find_all('a', {'class': 'list-rst__name-main'})
    for title in titles:
        title_text = title.text.strip()

        # extract the link to the restaurant page
        href = title.get('href')

        # visit the restaurant page and extract additional information
        response = requests.get(href, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # extract the address
        address = soup.find(
            'p', {'class': 'rd-detail-info__rst-address'}).text.strip()

        # extract the menu type
        menu_type_tag = soup.find('span', {'property': 'v:category'})
        if menu_type_tag is not None:
            menu_type = ', '.join([tag.text.strip()
                                  for tag in menu_type_tag.find_all('span')])
        else:
            menu_type = None

        # extract the business hours
        # business_hours_tags = soup.find('div', {'class': 'rdheader-subinfo__item--business-hours'}).select('p')
        # if business_hours_tags:
        #     business_hours = ', '.join([tag.text.strip() for tag in business_hours_tags])
        # else:
        #     business_hours = 'N/A'

        # extract the phone number
        phone_number = soup.find(
            'dt', text='TEL').find_next_sibling('dd').text.strip()

        # create a dictionary to store the data for this restaurant
        restaurant_data = {'title': title_text, 'address': address, 'menu_type': menu_type,
                           'phone_number': phone_number}  # 'business_hours': business_hours,

        # add the restaurant data to the list
        data_list.append(restaurant_data)

    # print a message to indicate that the page has been processed
    print(f"Page {page} complete.")

# write the data to a text file
with open('restaurant_data.txt', 'w', encoding='utf-8') as file:
    for data in data_list:
        file.write(f"Title: {data['title']}\n")
        file.write(f"Address: {data['address']}\n")
        if data['menu_type'] is not None:
            file.write(f"Menu type: {data['menu_type']}\n")
        else:
            file.write(f"Menu type: N/A\n")
        # file.write(f"Business hours: {data['business_hours']}\n")
        file.write(f"Phone number: {data['phone_number']}\n\n")

print("Done.")
