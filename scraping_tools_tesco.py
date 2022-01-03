"""
OVERALL PLAN (IDEAS)

- For each category of product (e.g. beer, apples, toothpaste, shower gel,
  toilet paper, hand wash etc.), find all products from either sainsbury's,
  tesco, coop, m and s, and find the cheapest per unit (sort by price). Would
  be good to also have photos of the products.
- Create database (SQLite) to store these results so it isn't necessary to
  scrape every time we want to access the data. Update this database every day.
- Create a UI which allows us to scan this DB more easily, plus create new item
  requests (e.g. 'red wine') and automatically scrape this. Also allow the user
  to remove items from a certain category if it is not applicable (e.g.
  'bananabread' coming up for 'banana's). **Do this tweaking myself for now**
- Add a search function to the UI which mirrors Tesco's search function (so you
  can subset if needs be). **Currently just having premade options**
- Make a mobile app version of this UI.

------------------------------------------------------------------------------------------

SUMMARY 12/12/21

- The update functions are working for Tesco, the SQLite db is working and a simple UI is 
  complete which allows to to search for all of a certain item ordered by equiv_price (so
  you can compare them directly, the units differ for each product, each of which has its 
  own function in update_products). Then daily_update can be scheduled on Windows to run
  daily.
- The most immediate next steps are to get Sainsbury's to the same standard on the Python
  side, so a checkbox group can be added to the UI allowing you to choose which supermarkets
  you would like to see. **Harder than expected, will revisit**

Other To-do List:
- Make the UI more aesthetic
- Look into using Pyppeteer for getting product images
- Look into including clubcard prices for Tesco (doesn't appear to be equivalent for Sainsburys)


------------------------------------------------------------------------------------------

21/11/21

- Based on the data I am currently extracting, it doesn't look as if PART 1 is
  needed as all this info is displayed on the search results page. This may
  change if new fields turn out to be useful so will keep the get_product
  function just in case.**Also, need to update this function so it refers to the
  page sections by name rather than index as this is less stable.**

- In get_products, image data needs decoding from base64. **Look into Pyppeteer**

**DONE**
- Set timer delay for multiple page search
- Need to update to search all pages - this just does the first one.
  This can be done by changing the count and page attributes of the URL
  (count should be set to 48 in future, but can be 24 for testing if better).
  Can also find how many pages by finding the total number of results on page
  1 and hence only changing the page attribute the correct number of times.
  


22/11/21

- Need to update to include clubcard price, "new" products, sponsored etc.

**DONE**
- The search function currently sometimes returns an extra value (pretty sure a
  duplicate) when there are sponsored products in the search results. Easiest
  would probably be to just check for duplicates afterwards.
- I've checked the robots.txt for tesco.com and the code isn't in violation.



24/11/21

- SQL: I seem to be able to store text in a field assigned REAL type (such as
  price), not sure if this is an issue. **Not an issue**
- When it comes to refreshing the database every day will I need to run the code
  from IDLE or can it be done automatically (scheduled)? **Look into scheduling in Windows**
- I've made the name field unique in the Products table (SQL), this may be an
  issue when it comes to including other supermarkets.



28/11/21

- SQL now all works except adding a new search URL **(for now this can be left to 
  manual)**
- Look into Pyppeteer for running through the image JS to find when they are 
  rendered and get the URLs
  
  **DONE**
  making products inactive when they no longer exist under a given 
  search.
- In current state, no need for a Products-Search table as it isn't many-many
  so can instead just add searchID as a foreign key in the products table.

- Add shiny app and Python and NodeJS to Github for Billy to look at (private)



30/11/21

- Not sure how to open R terminal in VSCode

--------------------------------------------------------------------------------------------

"""

#PART 1 - webscraping a product

def get_product(url):
    
    import requests
    from bs4 import BeautifulSoup

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    if soup.find_all("div", {"class":"controls--unit-toggle"}) == []:

        #When there is no choice of "by quantity or by weight"
        
        name = soup.select("h1")[0].get_text()
        price = soup.select("form div span span")[2].get_text()
        pricePerItem = soup.select("form div span span")[4].get_text()
        image = soup.select("img")[0]["src"]
        units = soup.find_all("span", {"class":"weight"})[0].get_text()[1:]

        print(name)
        print(price)
        print(pricePerItem, "per", units)
        print(image)
        
    else:

        #When there is an option "by quantity or by weight", such as loose fruit
        
        name = soup.select("h1")[0].get_text()
        price = soup.select("form div span span")[10].get_text()
        pricePerItem = soup.select("form div span span")[8].get_text()
        image = soup.select("img")[0]["src"]
        units = soup.find_all("span", {"class":"weight"})[0].get_text()[1:]

        print(name)
        print(price)
        print(pricePerItem, "per", units)
        print(image)







#PART 2 - webscraping all products from a search


def get_products_page_tesco(page_url, search_url):
    import requests
    import sqlite3
    from bs4 import BeautifulSoup


    con = sqlite3.connect("C:\\Users\\james\\Documents\\Projects\\PriceComp\\pricedata.db")
    cur = con.cursor()
    

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"} 
    page = requests.get(page_url, headers=headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')

    page_results = []
    for i in soup.find_all("li", {"class":"product-list--list-item"}):

        #Continues if the item is out of stock (shown by no prices given)
        if i.find_all("span", {"data-auto":"price-value"}) == []:
            continue
        
        name = i.find_all("a", {"data-auto":"product-tile--title"})[0].get_text()        
        first_value = i.find_all("span", {"data-auto":"price-value"})[0].get_text()
        second_value = i.find_all("span", {"data-auto":"price-value"})[1].get_text()
        units = i.find_all("span", {"class":"weight"})[0].get_text()[1:]
        url_end = i.find_all("a", {"class":"product-image-wrapper"})[0]["href"]
        url_start = "https://www.tesco.com"
        url = url_start + url_end


        cur.execute("SELECT searchID FROM Search_Results WHERE search_url=?", (search_url,))
        searchID = cur.fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO Products (name, price, priceperunit, units, url, company, searchID, active) VALUES (?, ?, ?, ?, ?, 'Tesco', ?, 1)", (name, first_value, second_value, units, url, searchID))
        cur.execute("UPDATE Products SET price=?, priceperunit=?, units=?, url=?, company='Tesco', searchID=?, active=1 WHERE name=?", (first_value, second_value, units, url, searchID, name))
        page_results.append(name)

    con.commit()
    con.close()
    return page_results







def get_products_search_tesco(search_url):
    import requests 
    import sqlite3
    import pandas as pd
    from bs4 import BeautifulSoup
    import math
    import time

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

    search_url_48 = search_url + "&count=48"
    page = requests.get(search_url_48, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    #Total number of results
    results_count = int(soup.find_all("div", {"data-auto":"product-bin-count"})[0].get_text().split(" ")[5])

    #Total number of pages (plus 2 just in case the special offers take up enough space to overflow the results)
    page_count = results_count//48 + 2

    all_results = []
    
    for i in range(page_count):
        time.sleep(3)
        url = search_url_48 + "&page=" + str(i+1)
        all_results = all_results + get_products_page_tesco(url, search_url)


    # Code for making old entries inactive from this particular search
    con = sqlite3.connect("C:\\Users\\james\\Documents\\Projects\\PriceComp\\pricedata.db")
    cur = con.cursor()
    cur.execute('UPDATE Products SET active=0 WHERE name NOT IN (%s) AND searchID=(SELECT searchID FROM Search_Results WHERE search_url=?)' %','.join('?'*(len(all_results))), all_results+[search_url])
    con.commit()
    con.close()

    

    
