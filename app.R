library(shiny)
library(reticulate)

# These two need to be replaced with your python directory
use_python("usr/bin/python")

# This needs to be replaced by your project directory (where you pulled from)
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
  
  observeEvent(input$gobutton, {
    
    errors_full <- ""
    arguments <- ""
    
    # Species
    if (input$species_input == "") {
      errors_full <- paste(errors_full, "missing species", sep="\n")
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
    } else {
      arguments <- paste(arguments, input$gene_input, sep=" ")
    }
    
    # Email
    if (input$email_input == "") {
      errors_full <- paste(errors_full, "missing email", sep=" ")
    }
    
    # Output type
    if (input$output_type == "") {
      errors_full <- paste(errors_full, "missing output Type", sep=" ")
    }
    
    print(errors_full)
    print("before if")
    
    # If there are no arguments, doesn't search and just shows error
    # TODO - Fix this so it doesn't freak out if there is nothing inserted
    if (arguments == "" || length(unlist(strsplit(arguments, ""))) == 0) {
      output$errorOutput <- renderText("Arguments are empty")
    }
    else if (errors_full == "" && arguments != "") {

      # Reports how many files were fetched
      python_output <- battery(arguments, input$email_input, "gb", "./output/")

      # Outputs file names fetched from python
      output$errorOutput <- renderText(python_output)
    } 
    
    # If not all of the blanks are filled; outputs what errors there are
    else {
      output$errorOutput <- renderText(errors_full)
    }
  
  })
  
  # Deletes the folder where files are being dropped
  observeEvent(input$button_delete, {
    delete_output <- delete_folder_contents()
    output$errorOutput <- renderText(delete_output)
  })
}


shinyApp(ui, server)

