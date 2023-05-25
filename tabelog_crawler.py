import requests
from bs4 import BeautifulSoup
import os

# set the base URL and headers
base_url = 'https://tabelog.com/kr/fukuoka/rstLst/'
headers = {'User-Agent': 'Mozilla/5.0'}

# create a list to store the data
data_list = []

# Create a directory to store images
os.makedirs("restaurant_images", exist_ok=True)

# loop through each page up to page 20
for page in range(1, 21):
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

        # Find and save the second image
        image_tags = soup.find_all('img', {'class': 'c-img c-img--frame'})
        if len(image_tags) > 1:
            image_url = image_tags[1].get('src')
            # Request and save image
            image_data = requests.get(image_url).content
            with open(os.path.join("restaurant_images", f"{title_text}.jpg"), 'wb') as image_file:
                image_file.write(image_data)
        else:
            image_url = None

        # create a dictionary to store the data for this restaurant
        restaurant_data = {'title': title_text, 'address': address, 'menu_type': menu_type, 'image_url': image_url}

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
        if data['image_url'] is not None:
            file.write(f"Image URL: {data['image_url']}\n\n")
        else:
            file.write(f"Image URL: N/A\n\n")

print("Done.")
