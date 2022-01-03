from scraping_tools_tesco import get_products_search_tesco


def update_apple():
    import sqlite3
    con = sqlite3.connect("C:\\Users\\james\\Documents\\Projects\\PriceComp\\pricedata.db")
    cur = con.cursor()
    get_products_search_tesco("https://www.tesco.com/groceries/en-GB/search?query=apple&department=Fresh%20Fruit&viewAll=department%2Caisle&aisle=Apples%20%26%20Pears")
    
    # Setting equiv_price for apples
    cur.execute('UPDATE Products SET equiv_price=priceperunit WHERE searchID=1 AND units="each"')
    cur.execute('UPDATE Products SET equiv_price=price WHERE searchID=1 AND units="kg"')
    con.commit()
    con.close()


def update_toothpaste():
    import sqlite3
    con = sqlite3.connect("C:\\Users\\james\\Documents\\Projects\\PriceComp\\pricedata.db")
    cur = con.cursor()
    get_products_search_tesco("https://www.tesco.com/groceries/en-GB/search?query=toothpaste&department=Toothpaste%2C%20Mouthwash%20%26%20Toothbrush&viewAll=department")
    
    # Setting equiv_price for toothpaste
    cur.execute('UPDATE Products SET equiv_price=priceperunit WHERE searchID=2')
    con.commit()
    con.close()


def update_toilet_roll():
    import sqlite3
    con = sqlite3.connect("C:\\Users\\james\\Documents\\Projects\\PriceComp\\pricedata.db")
    cur = con.cursor()
    get_products_search_tesco("https://www.tesco.com/groceries/en-GB/search?query=toilet%20roll&department=Toilet%20Roll&viewAll=department")
    
    # Setting equiv_price for toilet roll
    cur.execute('UPDATE Products SET equiv_price=priceperunit WHERE searchID=3 AND units="100sht"')
    cur.execute('UPDATE Products SET equiv_price=priceperunit*0.66 WHERE searchID=3 AND units="each"')
    con.commit()
    con.close()

