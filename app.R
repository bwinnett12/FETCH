library(shiny)
library(reticulate)

repl

setwd("/home/bill/Projects/ncbifetcher/")


# Define UI for app that draws a histogram ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("Hello Shiny!"),
  
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    
    # Sidebar panel for inputs ----
    sidebarPanel(
      
      textInput(inputId = "email_input", 
                label = "Email - Always tell NCBI who you are", value = ""),
      
      radioButtons("boolean", "Boolean Operator for search: ", c("And" = "AND",
                                                                 "Or" = "OR"))
      
      # Input: Slider for the number of bins ----
      
      
      # Entrez email - required for parsing
      
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      
      # Output: ----
      textOutput("test_output"),
      
      # Species Input
      textInput(inputId = "species_input", label = "Species", value = ""),
      
      # Gene Input
      textInput(inputId = "gene_input", label = "Gene: ", value = ""),
      
      actionButton("gobutton", "start"),
    
      
      textOutput("errorOutput"),
      
      textOutput("testOutput")
      
    )
  )
)


# Define server logic required to draw a histogram ----

server <- function(input, output) {
  
  
  observeEvent(input$gobutton, {
    
    # full_thing <- paste("python fetcher.py",
    #                     input$species_input, # Species
    #                     input$gene_input,    # Gene
    #                     input$boolean,       # Boolean Operator
    #                     # input$email, 	     # Email address (Required by Entrez)
    #                     
    #                     sep=" ")
    # 
    # testing_python <- system(full_thing, 
    #                          intern=TRUE, wait=FALSE)
    # 
    # 
    # output$actionOutput <-renderText(testing_python)
    })
    
  
  errors_full <- ""
  arguments <- ""
  
  observeEvent(input$gobutton, {
    
    
    # Species
    if (input$species_input == "") {
      errors_full <- paste(errors_full, "missing species", sep=" ")
      arguments <- paste(arguments, "species::null", sep=" ")
    } else {
      arguments <- paste(arguments, input$species_input, sep=" ")
    }
    
    # Boolean Operator
    arguments <- paste(arguments, input$boolean, sep=" ")
    
    # Gene
    if (input$gene_input == "") {
      errors_full <- paste(errors_full, "missing gene", sep=" ")
      arguments <- paste(arguments, "gene::null", sep=" ")
    } else {
      arguments <- paste(arguments, input$gene_input, sep=" ")
    }
    
    # Email
    if (input$email_input == "") {
      errors_full <- paste(errors_full, "missing email", sep=" ")
      arguments <- paste(arguments, "email::null", sep=" ")
    } 
    else {
      arguments <- paste(arguments, input$email_input, sep=" ")
    }
    
    arguments <- paste("python fetcher.py", arguments, sep=" ")
    
    
    
    output$errorOutput <- renderText(errors_full)
    
    output$testOutput <- renderText(arguments)
    
  })
  
}


shinyApp(ui, server)

