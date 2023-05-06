# crawling-tabelog

This repository contains Python code for crawling restaurant information from [Tabelog](https://tabelog.com/kr/fukuoka/rstLst/), a popular restaurant review website in Japan.

## Installation

Before running the script, you need to install the following Python packages:

- `requests`
- `beautifulsoup4`

You can install these packages using `pip`. For example, run the following command to install both packages:
  
  ```bash
  pip install requests beautifulsoup4
  ```

## Usage

To run the script, simply run the `tabelog_crawler.py` file. The script will crawl the first 50 pages of restaurant listings in Fukuoka, Japan, and extract the following information for each restaurant:

- Title
- Address
- Menu type
<!-- - Business hours -->
- Phone number

The script will store the data in a text file named `restaurant_data.txt` in the same directory.

## Disclaimer

The script is intended for educational purpose only. Please use it responsibly and in accordance with the terms of use of [Tabelog](https://tabelog.com/kr/fukuoka/rstLst/).