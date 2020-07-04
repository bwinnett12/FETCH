


library(shiny)
library(reticulate)
library(system2)

setwd("/home/bill/Projects/ncbifetcher/")



fun <- system('python //home//bill//Projects//ncbifetcher//test.py hello', 
               intern = TRUE, wait=FALSE)

# Define UI for app that draws a histogram ----
ui <- fluidPage(

  # App title ----
  titlePanel("Hello Shiny!"),

  # Sidebar layout with input and output definitions ----
  sidebarLayout(

    # Sidebar panel for inputs ----
    sidebarPanel(

      # Input: Slider for the number of bins ----
      
      
      # Entrez email - required for parsing
      textInput(inputId = "in_email", 
                label = "Email - Always tell NCBI who you are", value = "")
      
      


    ),

    # Main panel for displaying outputs ----
    mainPanel(

      # Output: ----
      textOutput("test_output"),
      
      selectInput(inputId = "input_type", label = "Type of query", choices = c(
        "Species ID" = "id_species")),
      
      
      textInput(inputId = "input_identifier", label = "", value = ""),
      
      actionButton("gobutton", "start"),
      
      textOutput("actionOutput")
      


    )
  )
)


# Define server logic required to draw a histogram ----

server <- function(input, output) {
  
  
  observeEvent(input$gobutton, {
    
    full_thing <- paste("python fetcher.py", input$input_identifier, sep=" ")

    testing_python <- system(full_thing, 
      intern=TRUE, wait=FALSE)
    
    
    output$actionOutput <-renderText(testing_python)

    
  })
}


shinyApp(ui, server)
 
