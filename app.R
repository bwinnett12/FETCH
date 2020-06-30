

library(shiny)
library(reticulate)

source_python("C:\\Users\\dwinn\\PycharmProjects\\ncbithing\\base.py")

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

  # Histogram of the Old Faithful Geyser Data ----
  # with requested number of bins
  # This expression that generates a histogram is wrapped in a call
  # to renderPlot to indicate that:
  #
  # 1. It is "reactive" and therefore should be automatically
  #    re-executed when inputs (input$bins) change
  # 2. Its output type is a plot
  
  
  observeEvent(input$gobutton, {
    if (test_indiv()) {
      output$actionOutput <- renderText("Worked"
      )
    }
  })
  # 
  # 
  # 
  # output$test_output <- renderText({
  #   test_method(input$bins)
  # 
  # })

}

shinyApp(ui, server)

