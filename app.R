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
      
      checkboxGroupInput("output_type", "Type of output: ", 
                        c("Genebank" = "gb", "Fasta" = "fasta")),
      
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
      
      # Action button that triggers python execution
      actionButton("gobutton", "start"),
    
      # Code for broadcasting errors
      textOutput("errorOutput"),
      
      # Code for tests. Will either delete or repurpose late
      textOutput("testOutput")
      
    )
  )
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    if (input$species_input != "" && input$gene_input != ""){
      arguments <- paste(arguments, input$boolean, sep=" ")
    }
    
    # Gene
    if (input$gene_input == "") {
      errors_full <- paste(errors_full, "missing gene", sep="\n")
      arguments <- paste(arguments, "gene::null", sep=" ")
    } else {
      arguments <- paste(arguments, input$gene_input, sep="\n")
    }
    
    # Email
    if (input$email_input == "") {
      errors_full <- paste(errors_full, "missing email", sep="\n")
    }
    
    # Output type
    if (input$output_type == "") {
      errors_full <- paste(errors_full, "missing output Type", sep="\n")
    }
    
    print(errors_full)
    print("before if")
    
    # if (errors_full == "") {
    #   print(errors_full)
    #   print("Still went here")
    #   # Sources the folder for python to work
    #   setwd("/home/bill/Projects/ncbifetcher/")
    #   source_python("fetcher.py")
    #   
    #   # Reports how many files were fetched
    #   python_output <- battery(arguments, input$email_input, "gb", ".")
    #   
    #   # An output for the ease of testing
    #   output$testOutput <- renderText(python_output)
    # }
    
    
    # Outputs errors
    output$errorOutput <- renderText(errors_full)
    
    
    
  })
  
  # Deletes the folder where files are being dropped
  observeEvent(input$button_delete, {
    delete_output <- delete_folder_contents()
    output$testOutput <- renderText(delete_output)
  })
  
}


shinyApp(ui, server)

