  # Data Analyser
  #### Video Demo:  <URL HERE>
  #### Description:
  Data Analyser is a tool that works on datasets. Its functions are:
  1) Presenting basic statistics of the data in a user-specified format,
  2) Creating histograms of the variables in the dataset,
  3) Creating graphs with variables in the dataset.

  ## Prerequisites
  This program uses following libraries:
  - pandas
  - argparse
  - fpdf
  - matplotlib

  ## CDF Class

  This class converts a pandas dataframe to a PDF file.

  The name class variable is set to a default value of "default".

  The to_pdf class method takes in two arguments: df, which is a pandas dataframe, and filename, which is the name of the PDF file to be generated. The method initializes a FPDF object, sets the font and auto page break, and creates a table with the data from the dataframe.

  The create_table function takes in a pdf object and a table list, and adds each item of the table to the PDF object as a new cell. The function recursively calls itself if the width of the table exceeds the specified value, to break the table into multiple pages if necessary.

  Finally, the method calls the create_table function with the headers and data from the dataframe, and saves the PDF to the specified filename.


  ## Main

  This program takes command line arguments using the get_argparser() function and uses the argparse library. The code then loads a data frame using the load() function, with the input specified in the command line arguments. Load function allows only csv files.

  The code checks if the --stat argument is specified and if it is, the data generated by dataframe.describe method are either saved as a CSV file or as a PDF file, depending on the --save argument.

  The code then calls the drop_col() function to drop index columns, columns that have too many unique values or too many missing values. If the --histbar argument is specified, the code calls the hb_pdf() function to create histograms and bar plots and saves them as a PDF file.

  Finally, if the --graphs argument is specified, the code calls the graphs() function to create graphs with respect to the target variable which has to be binary. If the specified target variable does not exist, an error message is displayed with a list of existing columns in the data frame.

  ## Functions

  ### **get_argparser()**
  function sets up the command line arguments using the argparse library. The function creates a parser object and adds several arguments to it:

    -d or --input: This is a required argument that specifies the input file in CSV format.
    --stat: This is an optional argument that, if specified, will generate some basic statistics about the data set.
    -s or --save: This is an optional argument that specifies the format to save the statistics in (CSV or PDF). The default is CSV.
    --histbar: This is an optional argument that, if specified, will create histograms and bar plots for the variables in the data frame.
    -g or --graphs: This is an optional argument that specifies the target variable for creating 1D graphs. The target variable needs to be binary.

  The function returns the parser object that contains the specified arguments.

  ### **load(filename)**
  function loads a data set from a file. It takes in a filename as an argument and loads the data from a csv file into a pandas dataframe.

  The function first uses a regular expression to extract the name of the dataset from the filename, and sets the name class variable in the CDF class to the extracted name.

  Then, the function checks if the filename ends with the '.csv' extension, and exits the program with an error message if it doesn't.

  Finally, the function tries to read the data from the filename using the pandas.read_csv function and returns the dataframe. If the file is not found, it exits the program with an error message.

  ### **statistics_pdf(df)**
  function generates a PDF file containing some basic statistics of a data set represented by a Pandas DataFrame df.

  The code uses the fpdf library to generate the PDF file. The function first initializes an fpdf object and sets the font to Arial with size 8.

  Then the function sets the auto page break property to True and the margin to 0, which means that a new page will be automatically created whenever the current page is full.

  The function rounds the statistics of the df to 2 decimal places so the data do not exceed cell borders and renames the column index to Stat. Finally the function outputs a file in the format specified in the command line argument


  ### **missing(df,type)**
  This function creates a missing value count and percetage of missing values for each column in a pandas dataframe , df, and stores it in a dictionary. The dictionary is then transformed into a pandas DataFrame and sorted in descending order based on the number of missing values. If the type argument is set to 'csv', the missing value count DataFrame is saved as a CSV file. If the type argument is set to 'pdf', the missing value count DataFrame is saved as a PDF file using the to_pdf method of the CDF class.


  ### **drop_col(df)**

  This function takes a pandas dataframe df as input and returns the same dataframe with columns dropped based on the following conditions:

  If more than 50% of values in a column are missing, then the column is dropped.
  If the number of unique values in a column of type 'object' is greater than 50, then the column is dropped.
  If a column is determined to be an index column (meaning that its values are sorted and contiguous), then the column is dropped.

  The function starts by creating an empty list col_to_drop to keep track of the columns that need to be dropped. Then it iterates over each column in the dataframe and performs the checks mentioned above to determine if a column needs to be dropped or not. The index column check is performed by assuming that the values in the column are sorted and contiguous, and iterating over the rows in the dataframe to check if the values satisfy this condition. If any value fails the check, the flag variable is set to False and the loop is broken. If the loop completes without setting flag to False, then the column is added to the col_to_drop list. Finally, the function returns the original dataframe with the columns specified in col_to_drop dropped.

  ### **hb_pdf(df)**
  This function creates a histogram or a bar plot of each column in the given dataframe df. The type of plot is determined based on the data type of the column. If the column is of type object, a bar plot is created. If the column is of numeric type, a histogram is created. The plots are saved as a single PDF file with the name [dataset_name_histbars.pdf.] The title of each plot is also set to indicate the type of plot and the name of the column.

  The function uses the PdfPages class from the matplotlib.backends.backend_pdf module to save all the plots in a single PDF file. The savefig method is used to save each plot to the PDF file. The plt.close method is used to close each plot after it is saved to the PDF file to prevent memory leakage. The bbox_inches and pad_inches parameters are used to adjust the size of the plots to minimize the white space around them.

  ### **graphs(df,target_column)**

  This function graphs takes two arguments: df, which is a pandas dataframe containing the data, and target_column, which is the name of the column that you want to use as a target variable. The function first asserts that the values in the target column are binary (i.e. only contain 0s and 1s).

  The function then creates a list of columns (cols) from the dataframe after dropping target column and a list of columns (binned_cols) that have more than 30 unique values. The function also creates a dictionary (bins) of bins for each column in binned_cols, dividing the data into 10 bins.

  Finally, the function creates bar plots of the target variable (0/1) mean for each column in both cols and binned_cols, grouping the data by the column and saving the plots to a single pdf file using the PdfPages class from matplotlib. Note that for columns in binned_cols, the function first creates a new column with the data cut into the bins defined in the bins dictionary, before creating the bar plots.











