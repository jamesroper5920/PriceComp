# Price Comparison Project
This is a tool which scrapes the search results of selected products from Tesco.com and displays the results in a Shiny dashboard. 
* scraping_tools_tesco.py contains the functions for scraping a particular search result and updating the database. 
* update_products.py contains a function for each type of item which scrapes the latest results and updates pricedata.db accordingly. It also specifies how to directly two products (as this varies for each type of product, for instance toothpaste is always 'per 100ml' whereas apples varies depending on whether they are loose or a larger pack).
* daily_update.py contains all of the functions from update_products.py in one place so they can all be run conveniently (and the current list of available item can be seen more easily).
* pricedata.db is the database of current live products.
* app.r is the shiny dashboard for displaying the latest of each type of item.
