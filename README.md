# eBay Listing Title Modifier
The eBay Listing Title Modifier is a Python program that allows you to modify the title of multiple eBay listings using the eBay Trading API. It is a simple and convenient tool that helps you update the titles of your eBay listings efficiently.

## Installation
To use the eBay Listing Title Modifier, you need to have Python 3 installed on your system. You also need to install the following packages: ebaysdk.trading, pprint, re, os, and dotenv. You can install these packages by running the following command in your terminal or command prompt:
```shell
pip install -r requirements.txt
```

## Usage
To use the eBay Listing Title Modifier, you need to create a text file named "url.txt" in the same directory as the program. This file should contain the URLs of the eBay listings whose titles you want to modify, with one URL per line.

Before running the program, you need to set up your eBay Trading API credentials in a .env file located in the same directory as the program. The .env file should contain the following variables:

* EBAY_APP_ID: Your eBay Trading API App ID
* EBAY_DEV_ID: Your eBay Trading API Dev ID
* EBAY_CERT_ID: Your eBay Trading API Cert ID
* EBAY_TOKEN: Your eBay Trading API token

Once you have the input file and API credentials ready, you can run the program by navigating to the directory where the program is stored and running the following command:
```shell
$ python3 ebay-listing-title-updater.py
```
This will loop through each URL in the input file, extract the ItemID from the URL, modify the corresponding eBay listing title, and update the listing title using the eBay Trading API.

Here's an example output for the given sample:
```shell
Original title: Red Motorcycle Toy
Modified title: Red Motorcycle Toy
The listing title has been successfully updated!
```
This output shows that one eBay listing title has been modified using the eBay Trading API. The original title contained a few formatting issues which were corrected in the modified title.

Please note that modifying eBay listing titles using the eBay Trading API is a permanent action and cannot be undone. Please use this tool with caution and make sure that you have reviewed your changes before proceeding.
