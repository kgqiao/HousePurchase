#Assignment 4X

#Objective: Develop a program to produce a Current Home Availability for the
#sales staff at the Forest Park Development of Linnar Hooten Homes.

"""
### CSV Inputfile: Contains an unknown number of lines of data
- Each line corresponds with one of the available homes in the development
- Each line contains the following info:
    - Status code (A for Available, P for Pending, S for sold)
    - Lot Number
    - Model Name
    - Number of bedrooms
    - Number of bathrooms
    - Price
- No interactive input or output during the execution of this program

### Assumptions:
- Status Code: A, P, or S. Closed homes are those in Pending or Sold status
- Lot: A number from 1-3 digits
- Model Name: Always a length of <=12. Model names will never have a comma actually in the name
- Never more than <= 5 bedrooms
- Never more than <= 4 bathrooms. There are no half baths in the development
- Price <= 4 million dollars, always an integer. Never exceeds 4 million
- Monthly Payments always < $100,000. Display without commas
- Monthly payments should be rounded to the nearest cent
- Price, Down Payments, and Monthly Payments - always right justified, can be smaller than the sample values

- Homes that are closed (P or S) do not appear in the listing of homes on report, but may be part
of some totals in the summary
- Numbers that probably won't change but may change from time to time (and are NOT input) will
be the various number of years, the down payment percentages, the PMI percentage (assume only 1 
of these), the commission percentage, and the 4 different loan rates. 
- The first set of numbers on the line always pertains to the lower down payment percentage
- The down percentage could be under 10% so take this into account when printing it
- 1st character of the largest possible data item always aligns with the first character of 
the name of the column in the header
- All numbers in the summary-Basis for Monthly Payment are printed as is without justification

- No validation needed on the values
- Use the assumptions to help you with formatting and alignment


### Notes for the summary:
- Total Project Inventory Value = Total price of all the homes (all statuses)
- Total Available Inventory Value = Total price of all the homes that are available
- Home Percentage Closed (displays as a 0-100%) = Percentage of homes that have closed (Pending or Sold)
- Unrealized Salesperson Commission = Based on 1.5% of all available inventory


### PMI Additional to base monthly
- On any down payment less than 20%, monthly payments should have PMI (Principal Mortgage Insurance)
added into the base monthly
- Ex: PMI for a year assumed to be 0.22% of the loan amount (not the purchase price);
    Divide that by 12 to get the monthly PMI amount
    Do not assume that either the first or second down is 10% or 20%
    You need to test it to see if it is less than 20% to determine if there is PMI
- Down percentages should be expressed as defined constants




### To calculate base monthly payments:
1. Use pmt() = A special payment function in the *numpty_financial* library
(See instructions below for installing the library into Visual Studio)
Given:
- A periodic rate (such as a monthly interest rate in decimal format)
- A number of periods (such as the months on a loan)
- The principal amount (otherwise known as the balance)

pmt() function = RETURNS the fully amortized monthly payment amount _as a negative number_

REMEMBER that users are generally:
- Asked for years, not months
- Asked for annual percentage rates in percentages, not in decimal percentages
    FUNCTION USES monthly decimal percentages

    FUNCTION RETURNS payment as negative number, since it's money going OUT from a person
    (loan IN, payment OUT)

*Think about what you need to do to convert your values so that they work with this function


### numpy_financial library + nicknaming libraries import

Original Function Call under numpy_financial library:
numpy_financial.pmt(periodic_rate, number_of_periods, principal)

#1. Use the 'as' keyboard to give the library a shorter nickname, ex: numf
import numpy_financial as numf

#2. New Function Call under nicknamed library:
numf.pmt(periodic_rate, number_of_periods, principal)

#3. REMEMBER: this is a function that returns a value, so this call woudl be as or inside
an expression - such as on the right side of an assigment statement




"""

#Import libraries
import math
import csv
import numpy_financial as numpy


##################### Define Constants #####################
percent_salescomm = 0.015 #Unrealized salesperson commission, based on 1.5% of all available inventory, float data type
percent_pmi = 0.0022 #PMI = 0.22% of the loan amount (NOT THE PURCHASE PRICE), float data type

percent_downpay_lower = 0.10 #The LOWER ANNUAL APR down payment percentage 10%, float data type 
percent_downpay_higher = 0.20 #The HIGHER ANNUAL APR down payment percentage 20%, float data type

loan_yrs_higher = 30 #The higher number of years on the loan, 30 years, int data type
loan_yrs_lower = 15 #The lower number of years on the loan, 15 years, int data type

percent_loan_rate1 = 0.0699
percent_loan_rate2 = 0.0649
percent_loan_rate3 = 0.0600

#Define Constants in percent format
salescomm_rate = percent_salescomm * 100 #Unrealized salesperson commission, based on 1.5% of all available inventory, float data type
pmi_rate = percent_pmi * 100 #PMI = 0.22% of the loan amount (NOT THE PURCHASE PRICE), float data type

downpay_lower_rate = percent_downpay_lower * 100 #The LOWER ANNUAL APR down payment percentage 10%, float data type 
downpay_higher_rate = percent_downpay_higher * 100  #The HIGHER ANNUAL APR down payment percentage 20%, float data type

loan_rate1 = percent_loan_rate1 * 100
loan_rate2 = percent_loan_rate2 * 100
loan_rate3 = percent_loan_rate3 * 100

#Concatenating header titles for downpayment and monthly combinations
down_header_lower = ""
down_header_higher = ""
mon_header_higher = ""
mon_header_lower = ""


########################################### GLOBAL VARIABLES ###########################################

##################### General Variables #####################
status_code = "" #Status code (A for Available, P for Pending, S for Sold), str data value
lot_num = 0  #Lot number, int data type. Can only be 1-3 digits
model_name = "" #Model Name, str data type
num_bed = 0 #Number of bedrooms, int data type
num_bath = 0 #Number of bathrooms, int data type
price = 0 #House price, int data type


##################### Concatenated Variables  #####################
bed_ba = "" #Concatenation of Number of Bed/Number of Bath PER HOUSE


##################### Accumulative Variables #####################
#Accumulative Variables - for ALL Homes
count_allhomes = 0 #Count of all homes, int data type
total_project_inventory_value = 0.0 #Total Project Inventory Value = Total price of all the homes (all statuses), float data type

#Accumulative Variables - for Available Homes (A)
count_availhomes = 0 #Count of available homes, int data type
total_avail_inventory_value = 0.0 #Total Available Inventory Value = Total price of all the homes that are available, float data type
unrealized_sales_commission = 0.0 #Unrealized Salesperson Commission = Based on 1.5% of all available inventory

#Accumulative Variables - for Closed Homes (S or P)
count_closedhomes = 0 #Count of closed homes, int data type
percent_closedhomes = 0.0 #Home Percentage Closed (displays as a 0-100%) = Percentage of homes that have closed (Pending or Sold), float data type


##################### Calculation for Monthly Payment Variables #####################
percent_downpay = 0.0 #APPLICABLE down payment percentage, float data type
num_loanyears = 0 #APPLICABLE number of loan years, int data type
loan_rate = 0.0 #APPLIABLE loan_rate APR, float data type

periodic_rate = 0.0 #APPLICABLE periodic rate based on APPLICABLE loan rate
num_periods = 0 #APPLICABLE number of periods (months) based on APPLICABLE years in the loan
principal = 0.0 #APPLICABLE principal amount subject to loan, after downpayment

monthly_pmi_amt = 0.0 #APPLICABLE monthly PMI amount to pay extra IF downpayment percentage < 20%
monthly_payment = 0.0 #APPLICABLE MONTHLY PAY CALCULATION


##################### Final Calculation Variables #####################
down_payment_lower = 0.0 #Downpayment w/ LOWER downpayment %
monthly_payment1 = 0.0 #Monthly payment w/ LOWER down payment %, HIGHER loan years, loanrate1 + PMI
monthly_payment2 = 0.0 #Monthly payment w/ LOWER down payment %, LOWER loan years, loanrate2 + PMI

down_payment_higher = 0.0 #Downpayment w/ HIGHER downpayment %
monthly_payment3 = 0.0 #Monthly payment w/ HIGHER down payment %, HIGHER loan years, loanrate2
monthly_payment4 = 0.0 #Monthly payment w/ HIGHER down payment %, LOWER loan years, loanrate3


##################### File Variables #####################
csv_reader = '' #CSV read in variable
inputfile = '' #CSV inputfile, Null string
outputfile = '' #CSV outputfile, Null string




def main():
    input_output() #Open CSV inputfile, open CSV outputfile
    output_header() #Output header, subheader
    output_intro() #Output table headers
    output_content() #Read CSV inputfile into variables, output content rows, do calculations
    output_end() #Output calculations of total values
    output_monthlypay_summary() #Output basis for monthly payments summary


def input_output():
    global inputfile, outputfile, csv_reader
    
    #Create file in VS or Notepad textdocument for inputfile "r" OR outputfile "w"
    #OPEN file (C: drive > class folder > name.txt); (Python \\, file explorer filepath is with \)
    #Open csv inputfile to read
    inputfile = open("H:\\HDD KQ\\coding\\class\\uclasoftwaredevclass\\assignment4x\\homedata.txt", 'r')
    #inputfile = open("C:\\class\\homedata.txt",'r')
    
    #Open CSV outputfile to write
    outputfile = open("H:\\HDD KQ\\coding\\class\\uclasoftwaredevclass\\assignment4x\\kqiao_lh.txt",'w')
    #outputfile = open("C:\\class\\kqiao_lh.txt",'w')

    # CSV Reader
    #Read data from input txt file into program
    #Declare VARIABLE: csv_reader = Stores the data from input file
    csv_reader = csv.reader(inputfile, delimiter = ',')


def output_header(): #Output report headers, subheaders
    global outputfile
    print("Linnar Hooten Homes", file = outputfile)
    print("Forest Park Development", file = outputfile)
    print("\nCurrent Home Availability List", file = outputfile)


def output_intro(): #Output table headers
    global outputfile
    global down_lower_rate, down_higher_rate
    global loan_yrs_higher, loan_yrs_lower
    global down_header_lower, down_header_higher, mon_header_higher, mon_header_lower

    #Concatenating header titles for downpayment and monthly combinations
    down_header_lower = f'Down({downpay_lower_rate:.0f}%)'
    down_header_higher = f'Down({downpay_higher_rate:.0f}%)'
    mon_header_higher = f'Mon({loan_yrs_higher}yr)'
    mon_header_lower = f'Mon({loan_yrs_lower}yr)'

    #Print output for table headers
    print(f'\n{"Lot":<4}{"Model":<13}{"Bed/Ba":<9}{"Price":<8}{down_header_lower:>11}{mon_header_higher:>11}{mon_header_lower:>11}{"|":>2}{down_header_higher:>11}{mon_header_higher:>10}{mon_header_lower:>11}', file = outputfile)
    print(f'{"|":>69}', file = outputfile)



def  calc_downpayment (percent_downpay): #Calculating downpayment based on applicable downpayment rate
    global price
    downpay = price * percent_downpay
    return downpay


def  calc_monthly_payment (percent_downpay, down_payment, num_loanyears, percent_loan_rate):
    global price, percent_pmi
    global periodic_rate, num_periods, principal
    global monthly_pmi_amt, monthly_payment

    num_periods = num_loanyears * 12
    principal = price - down_payment
    periodic_rate = (percent_loan_rate / 12)

    #Calculating periodic_rate DEPENDING ON if there is additional PMI percentage
    if percent_downpay < 0.20: #Down payment percentage is 20%
        monthly_pmi_amt = principal * (percent_pmi / 12)
        monthly_payment = (-1 * numpy.pmt(periodic_rate, num_periods, principal)) + monthly_pmi_amt #Calculating monthly payment
    else: #Down payment percentage is above 20%
        monthly_payment = -1 * numpy.pmt(periodic_rate, num_periods, principal) #Calculating monthly payment

    return monthly_payment #returning end result monthly_payment



def output_content():
    global status_code, lot_num, model_name, num_bed, num_bath, price
    global count_allhomes, total_project_inventory_value
    global count_availhomes, total_avail_inventory_value, unrealized_sales_commission, percent_salescomm
    global count_closedhomes, percent_closedhomes
    global down_payment_lower, down_payment_higher
    global monthly_payment1, monthly_payment2, monthly_payment3, monthly_payment4
    global bed_ba

    #FOR loop for variables
    #Reads in data row by row
    #Rows [0, n]: 
    #Row [0]: firstname, VARIABLE data type: str
    # Row [1]: age, VARIABLE data type: math.floor()
    for row in csv_reader:
        status_code = str(row[0]) #Status code (A for Available, P for Pending, S for sold)
        lot_num = int(row[1]) #Lot Number --> OUTPUT AS IS
        model_name = str(row[2]) #Model Name --> OUTPUT AS IS
        num_bed = int(row[3]) #Number of bedrooms ---> OUTPUT bed/bath number together, concatenate
        num_bath = int(row[4]) #Number of bathrooms --> see bed
        price = int(row[5]) #Price of house --> OUTPUT AS IS, WITH COMMAS

        #Add to accumulative variables - ALL
        count_allhomes += 1 #Add to count of all homes
        total_project_inventory_value = total_project_inventory_value + price #Add to total price value of all homes

        if status_code == "A": #Available Homes (A): Add to accumulative variables (Available) AND print output table row
            #Add to accumulative variables - Available Homes (A)
            count_availhomes += 1 #Add to count of available homes
            total_avail_inventory_value = total_avail_inventory_value + price  #Add to total price value of available homes
            unrealized_sales_commission = percent_salescomm * total_avail_inventory_value #Calculating unrealized sales commmission as __% of all available inventory

            ##Calculate Down Payment AND Monthly Payments
            ### 10% downpayment amount
            down_payment_lower = calc_downpayment(percent_downpay_lower)
            ### 10% downpayment, 30 years loan, 6.99% loan (loanrate1) + PMI of 0.22%
            monthly_payment1 = calc_monthly_payment(percent_downpay_lower, down_payment_lower, loan_yrs_higher, percent_loan_rate1)
            ### 10% downpayment, 15 years loan, 6.49% loan (loanrate2) + PMI of 0.22%
            monthly_payment2 = calc_monthly_payment(percent_downpay_lower, down_payment_lower, loan_yrs_lower, percent_loan_rate2)
            
            ### 20% downpayment amount
            down_payment_higher = calc_downpayment(percent_downpay_higher)
            ### 20% downpayment, 30 years loan, 6.49% loan (loanrate2)
            monthly_payment3 = calc_monthly_payment(percent_downpay_higher, down_payment_higher, loan_yrs_higher, percent_loan_rate2)
            ### 20% downpayment, 15 years loan, 6.00% loan (loanrate3)
            monthly_payment4 = calc_monthly_payment(percent_downpay_higher, down_payment_higher, loan_yrs_lower, percent_loan_rate3)


            ##PRINT OUT TABLE ROW
            #Lot Number, Model Name: Output print as is
            bed_ba = f'{num_bed}bd/{num_bath}ba' #Establishing output for Bed/Ba, by concatenating
            #Price, 2 downpayments, 4 monthlypayments: output as is, WITH COMMAS

            #Variables input for:
            #print(f'{lot_num}{model_name}{bed_ba{price}{"Down(10%)"}{"Mon(30yr)"}{"Mon(15yr)"}{"|"}{"Down(20%)"}{"Mon(30yr)"}{"Mon(15yr)"', file = outputfile)
            print(f'{lot_num:<4}{model_name:<13}{bed_ba:>7}{price:>11,.0f}{down_payment_lower:>9,.0f}{monthly_payment1:>11.2f}{monthly_payment2:>11.2f}{"|":>3}{down_payment_higher:>9,.0f}{monthly_payment3:>11.2f}{monthly_payment4:>11.2f}', file = outputfile)
            

        else: #Closed Homes (S or P): Add to accumulative variables (CLOSED) ONLY, do not print output
            #Add to accumulative variables - Closed Homes (S or P)
            count_closedhomes += 1 #Add to count of closed homes


def output_end():
    global total_project_inventory_value, total_avail_inventory_value, home_percent_closed, unrealized_sales_commission, percent_closedhomes

    percent_closedhomes = math.floor(count_closedhomes / count_allhomes * 100) #Calculate percentage of closed homes out of all homes

    print(f'\nTotal Project Inventory Value: ${total_project_inventory_value:,.0f} ({count_allhomes} homes)', file = outputfile) #Total price of all the homes (all statuses)
    print(f'Total Available Inventory Value: ${total_avail_inventory_value:,.0f} ({count_availhomes} homes)', file = outputfile) #Total price of all the homes that are available
    print(f'Home Percentage Closed: {percent_closedhomes:,.1f}%', file = outputfile) #Percentage of homes that have closed (Pending or Sold)
    print(f'Unrealized Salesperson Commission: ${unrealized_sales_commission:,.0f}', file = outputfile) #Unrealized Salesperson Commission = Based on 1.5% of all available inventory
    
    """ How to print number in comma format without rserving extra spaces. May combine this
    with a preceding justification symbol (< or >) and width value, and/or a subsequent decimal
    specification to round to (such as ,2f)
    """



def output_monthlypay_summary(): #Output final summary values
    global output_monthlypay_summary
    global downpay_lower_rate, downpay_higher_rate
    global loan_yrs_higher, loan_yrs_lower


    print("\nBasis for Monthly Payments", file = outputfile) #Header
    
    #Print out summary monthly payment basis(s) at each permutation of values
    ### 10% downpayment, 30 years loan, 6.99% loan (loanrate1) + PMI of 0.22%
    print(f'{downpay_lower_rate}% down {loan_yrs_higher} year - {loan_rate1:.2f}% plus PMI of {pmi_rate:.2f}%', file = outputfile)
    ### 10% downpayment, 15 years loan, 6.49% loan (loanrate2) + PMI of 0.22%
    print(f'{downpay_lower_rate}% down {loan_yrs_lower} year - {loan_rate2:.2f}% plus PMI of {pmi_rate:.2f}%', file = outputfile)
    ### 20% downpayment, 30 years loan, 6.49% loan (loanrate2)
    print(f'{downpay_higher_rate}% down {loan_yrs_higher} year - {loan_rate2:.2f}%', file = outputfile)
    ### 20% downpayment, 15 years loan, 6.00% loan (loanrate3)
    print(f'{downpay_higher_rate}% down {loan_yrs_lower} year - {loan_rate3:.2f}%', file = outputfile)

    print("\nAll percentages are for well-qualified buyers.", file = outputfile)


main()





