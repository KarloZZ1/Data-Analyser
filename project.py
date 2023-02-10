import math
import sys
import pandas as pd

import argparse
from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import re


#create custom dataframe class that inherits from pandas dataframe
class CDF():


    #Set name to default
    name = 'default'


    # Add save to pdf method
    @classmethod
    def to_pdf(cls,df, filename):
        #initialize fpdf object
        pdf = FPDF()

        #set fonts
        pdf.set_font("Arial", size=8)

        #automaticlly break page
        pdf.set_auto_page_break(True, 0)

        #add list of headers
        headers = list(df)


        #add lists of rows
        data = [list(row) for _, row in df.iterrows()]

        #create table
        def create_table(pdf,table):


                #create a list with col widths
                col_widths = [0] * len(headers)

                #determine widths of every column
                for row in table:
                    for i, cell in enumerate(row):
                        width = pdf.get_string_width(str(cell))
                        if width > col_widths[i]:
                            col_widths[i] = width



                #determine row height
                row_height = pdf.font_size + 2

                #add width_page variable
                width_page = 0
                #add new page
                pdf.add_page()

                #create  table list that goes onto the new page and new row list to append to that table list.
                page_table  = list()


                #iterate over every row of a table
                for row in table:
                    page_row = list()
                    #iterate over columns width
                    for i, col_width in enumerate(col_widths):



                        width_page += col_width
                        #print tthe table onlty to the specified width
                        if width_page < 180:
                            pdf.cell(col_width + 5, row_height, str(row[i]), border=1)
                        else:
                            #append new items to the page_row if width is exceeded
                            page_row.append(row[i])

                    #append page_row to the page_table but dont append empty list
                    if not len(page_row) == 0:
                        page_table.append(page_row)
                    pdf.ln(row_height)
                    #set width again to 0
                    width_page = 0

                if len(page_table) > 0:
                    create_table(pdf,page_table)

        create_table(pdf,[headers] + data)
        #Save file to a pdf
        pdf.output(filename)





































def main():


    #get parser object from function
    parser = get_argparser()
    #parse arguments
    args = parser.parse_args()

    #load data frame
    df = load(args.input)

    #get name of the datatset
    if matches:= re.search(r"^.*?/?(\w+)\.csv$",args.input):
        name = matches.group(1)
    #set class name for all the files
    CDF.name = name

    #If --stat == T, print some statstics
    if args.stat:
        statistics(df,args.save)
    #print number of missing values of each column if specified
    if args.missing:
        missing(df,args.save)

    # dropping columns with many unique obcject values( more than 10) or many missing values (more than 50% missing)
    df_drop = drop_col(df)

    #Create some histograms and barplots if specified and save them to pdf file
    if args.histbar:
        hb_pdf(df_drop)

    #Create graphs with respect to taregt variable

    if not args.graphs is None:
        try:
            graphs(df_drop,args.graphs)
        except KeyError:
            print(f"Non existing target variable, check if u typed one of {list(df_drop.columns)}")





#create funnction that gets argparse arguments
def get_argparser():
    #adding argaprse arguments
    parser = argparse.ArgumentParser(description = "Generate basic statistics and data set description")
    parser.add_argument('-d','--input',type = str, required = True , help = "Load a file in a csv format")
    parser.add_argument('--stat',action ="store_true", help = "Give some basic statistics")
    parser.add_argument('-m','--missing',action = "store_true",help = "Print number of missing values of each column")
    parser.add_argument('-s', '--save', type = str,default = 'csv', help = "Save statsitisc in format pdf or csv")
    parser.add_argument('--histbar', action = "store_true", help = "Create histograms and barplots of the variables in df")
    parser.add_argument('-g', '--graphs', type = str, help = "Create 1d graphs versus target variable, arg=name of the target variable, the target variable needs to be binary")

    return parser















# load the dataset
def load(filename):

    if not filename.endswith('.csv'):
        sys.exit("Incorrect file format, check --help")
    try:
        return pd.read_csv(filename)

    except FileNotFoundError:
        sys.exit("Could not find the file")





















def statistics(df,type):

     #round the statistics of the describe
        df = (df.describe().round(2).reset_index())

        #name the column of the variables
        df = (df.rename(columns = {"index" : "Stat"}))



        if type == 'csv':
            #Save to csv
            df.to_csv(f"{CDF.name}_statistics.csv")
        elif type == 'pdf':
            #Save to pdf
            CDF.to_pdf(df,f"{CDF.name}_statistics.pdf")




def missing(df,type):
    #count missing values of each column and store them in a dict
    count = dict()
    for column in list(df.columns):
        counter = df[column].isna().sum()
        percent = counter/df.shape[0]
        count[column] = [counter, f"{percent:.2%}"]


    #create dataframe adn transpose it
    missing = pd.DataFrame(count).transpose()



    #Add column name
    missing.columns = ["Count","Percent"]

    #Sort values in descending order
    missing = missing.sort_values("Count", ascending = False).reset_index()

    


    if type == 'csv':
            #Save to csv
            missing.to_csv(f"{CDF.name}_missing.csv")
    elif type == 'pdf':
            #Save to pdf
            CDF.to_pdf(missing,f"{CDF.name}_missing.pdf")













# dropping columns with many unique obcject values( more than 50) or many missing values (more than 50% missing) and index columns
def drop_col(df):

    #create list with colums to drop

    col_to_drop = list()

    for column in list(df.columns):
        #Count missing values
        missing_values_count = df[column].isna().sum()
        #drop if the number higher than 50%
        if missing_values_count / df.shape[0] >0.5:
            col_to_drop.append(column)


        elif df[column].dtype == object:
            #count unique object values
            unique_values_count = df[column].nunique()
            #drop if the number higher than 50
            if unique_values_count > 50:
                col_to_drop.append(column)

    #search for index columns(it does not work with missing rows)

    #set flag to False
    flag = False
    #iterate over every column
    for column in list(df.columns):
        #Exclude object columns form the search
        if not df[column].dtype == 'object':
            #Check if column is an index, assuming its sorted
            for index, row in df.iterrows():
                if index < len(df) - 1:
                    flag = (row[column] == df.iloc[index+1][column] - 1)

                    if flag == False:
                        break

            if flag == True:
                col_to_drop.append(column)

    #drop columns to drop

    return df.drop(columns = col_to_drop)











def hb_pdf(df):

    #open pdf
    with PdfPages(f"{CDF.name}_histbars.pdf") as pdf:
        for column in list(df.columns):

            if df[column].dtype == 'object':
                #create barplot
                df[column].value_counts().plot(kind='bar')
                plt.title(f"Barplot of {column}")

                pdf.savefig(bbox_inches="tight", pad_inches =0.5)
                plt.close()
            else:
                #create histogram
                df[column].plot.hist(edgecolor = 'black',title = f"Histogram of {column}")
                #save them to files
                pdf.savefig(bbox_inches="tight", pad_inches =0.5)
                plt.close()













def graphs(df,target_column):

    #assert that target value is 0,1 variable
    assert all((df[target_column] == 0) | (df[target_column] == 1)), "Values in target column are not binary"

    #make a list with columns and drop tareget_column
    cols = list(df.drop(columns = target_column).columns)

    #make list with columns that should go with bins
    binned_cols = list()

    for column in cols:
        if df[column].nunique() > 30:

            binned_cols.append(column)

    #subtract binned_cols from cols
    cols = list(set(cols) - set(binned_cols))

    #create a dict of bins for each column in the binned_cols, lets assume that we divide data over 10 diffrent bins
    bins = dict()

    #add bins
    for column in binned_cols:

        #round min and max values to tens.
        min = (math.floor(df[column].min()/10) *10)
        max = (math.ceil(df[column].max()/10)*10)

        #create temporary list
        b = list()
        for i in range(min,max+1,int((max-min)/10)):
            b.append(i)
        #append that list to the bins
        bins[column] = b

    #create some labels

    labels = {key: [f"{bins[key][i]}-{bins[key][i+1]}" for i in range(len(bins[key])-1)] for key in list(bins.keys())}


    #open pdf pages

    with PdfPages(f"{CDF.name}_graphs.pdf") as pdf:
        #create graphs form cols
        for column in cols:

            df[[df[column].name,target_column]].groupby(df[column].name).mean().plot(kind='bar')

            pdf.savefig(bbox_inches="tight", pad_inches =0.5)
            plt.close()
        #create graphs from binned_cols
        for column in binned_cols:
            #cut dataframe into bins
            df[column +'binned'] = pd.cut(df[column], bins[column], labels = labels[column])

            df.groupby(column +'binned').mean(numeric_only = True)[target_column].dropna().plot(kind='bar')
            pdf.savefig(bbox_inches="tight", pad_inches =0.5)
            plt.close()


if __name__ == "__main__":
    main()