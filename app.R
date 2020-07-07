library(shiny)
library(reticulate)

use_python("usr/bin/python")

setwd("/home/bill/Projects/ncbifetcher/")
source_python("fetcher.py")


ui <- fluidPage(
  
  # App title ----
  titlePanel("An interesting title"),
  
  # Sidebar
  sidebarLayout(
    
    # Sidebar panel (Email, Boolean operator, delete)
    # Will include instructions
    sidebarPanel(
      
      # Email input
      textInput(inputId = "email_input", 
                label = "Email - Always tell NCBI who you are", value = ""),
      
      # Boolean operator to refine search
      radioButtons("boolean", "Boolean Operator for search: ", c("And" = "AND",
                                                                 "Or" = "OR")),
      # Button for deleting file contents
      actionButton("button_delete", "delete")
      
      
    ),
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # Main panel for meat and potatoes of user input
    mainPanel(
      
      # Species Input
      textInput(inputId = "species_input", label = "Species: ", value = ""),
      
      # Gene Input
      textInput(inputId = "gene_input", label = "Gene: ", value = ""),
      
      actionButton("gobutton", "start"),
    
      
      textOutput("errorOutput"),
      
      textOutput("testOutput")
      
    )
  )
)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Server

server <- function(input, output) {
    
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
    } 
    
    setwd("/home/bill/Projects/ncbifetcher/")
    source_python("fetcher.py")
    
    # Reports how many files were fetched
    python_output <- battery(arguments, input$email_input, "esame", ".")
    
    #Outputs errors
    output$errorOutput <- renderText(errors_full)
    
    # An output for the ease of testing
    output$testOutput <- renderText(python_output)
    
  })
  
  observeEvent(input$button_delete, {
    delete_folder_contents()
    
  })
  
}


shinyApp(ui, server)

