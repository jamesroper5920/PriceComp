library(shiny)
library(RSQLite)
library(tibble)     # For add_column function
library(reactable)
library(htmltools)
library(priceR)


# Opens pricedata.db and reads the Products and Search_Results tables

con <- dbConnect(RSQLite::SQLite(), "pricedata.db")


# Orders Products by searchID (so they are grouped by item) then equiv_price (so they are shown lowest to highest price)
Products <- dbGetQuery(con, 'SELECT * FROM Products ORDER BY searchID ASC, equiv_price ASC')

# Leaves only active products
Products <- Products[Products$active == 1, ]

# Adds the pound sign to price and priceperunit (behaves weirdly without the UTF-8 code)
Products$price <- sprintf("%s%.2f", enc2utf8("\u00A3"), Products$price)
Products$priceperunit <- sprintf("%s%.2f", enc2utf8("\u00A3"), Products$priceperunit)
Products <- add_column(Products, ppu = paste(Products$priceperunit, ' per ', Products$units), .after = 'price')



Search_Results <- dbReadTable(con, "Search_Results")


# Gets time pricedata.db was last updated

lastupdate <- toString(file.info("pricedata.db")$mtime)



# UI layout

ui <- fluidPage(
  fluidRow(
    column(4, offset = 1,
           h2("Select your item")
           )
  ),
  fluidRow(
    column(2, offset = 1,
           selectInput("item","Item",choices=c("", sort(Search_Results$phrase)), selected = ""),
           actionButton("reset", "Reset Inputs", width = 120, style = 'background-color: #a8a7fc'),
           textOutput("updatedate")
           )
  ),
  fluidRow(
    column(1),
    column(10,
           reactableOutput("table")
           )
  ) 

)

server <- function(input, output, session) {
  
  
  # Gets 'last updated' time for pricedata.db
  output$updatedate <- renderText({paste("Last Updated: ", lastupdate)})

  observeEvent(input$reset, {
    
    #When the reset button is clicked, every input box is returned to its initial blank state.
    updateSelectInput(session, "item", selected = "")
  })
  
  finding <- reactive({
    
    # When item selected from drop down, filters the table to only display the relevant products.
    if (input$item != "") {
      search <- Search_Results$searchID[Search_Results$phrase==input$item]
      Products <- Products[Products$searchID == search, ]
    }
    
    
    Products
    
  })


  #Outputs a table containing the final Products table created above.
  
  output$table <- renderReactable({
    reactable(finding()[,c(2:4)],
              defaultColDef = colDef(align = "center"),
              defaultPageSize = 20, showPageSizeOptions = TRUE, pageSizeOptions = c(5, 10, 20, 50), 
              columns = list(     # Selecting only relevant columns
      name = colDef(align = "left", cell = function(value, index) {                # Adds the correct link to each product name
        url <- finding()[index, "url"]
        htmltools::tags$a(href = as.character(url), target = "_blank", as.character(value))
      })
    ))
  })
  
  
  # Shuts session down when closed, and closes connection to pricedata.db
  
  shinyServer(function(input, output, session){
    session$onSessionEnded(function() {
      dbDisconnect()
      stopApp()
    })
  })
  
}

shinyApp(ui = ui, server = server)