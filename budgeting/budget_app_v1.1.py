import pandas as pd
import streamlit as st
from datetime import datetime, timedelta


#############################################################

st.sidebar.markdown('### Expense and Income Inputs')

# Expenses Editable Dataframe
exp_df = pd.DataFrame(
    [
       {"Expense": "Rent/Water/Sewer/Internet", "MonthlyCost": 2539, "Include": True},
       {"Expense": "Electric/Gas", "MonthlyCost": 170, "Include": True},
       {"Expense": "Car Gas", "MonthlyCost": 150, "Include": True},
       {"Expense": "Insurance (Car & Renter)", "MonthlyCost": 50 , "Include": True},
       {"Expense": "Groceries", "MonthlyCost": 350, "Include": True},
       {"Expense": "Restaurants", "MonthlyCost": 200 , "Include": True},
       {"Expense": "Loans", "MonthlyCost": 1000, "Include": True},
       {"Expense": "Recurring AMZN Sub", "MonthlyCost": 150, "Include": True},
       {"Expense": "Other Subscriptions", "MonthlyCost": 79, "Include": True},
       {"Expense": "Travel Budget", "MonthlyCost": 200, "Include": True},
       {"Expense": "Misc", "MonthlyCost": 400, "Include": True}
    ]
)
exp_df = exp_df.set_index("Expense")
edited_df = st.sidebar.data_editor(exp_df)

#st.sidebar.markdown('### Inputs')
scol1,scol2,scol3 = st.sidebar.columns(3)

#Initialize input variables
gross_annual_salary = scol1.number_input("Gross Annual Salary: ", step=1000, value=140000)
percent_ret_contrib = scol2.number_input("% To Retirement: ", step = 1, value=6)
paycheck = scol3.number_input("Paycheck: ", step=100, value = 3755)

gross_monthly_income = round(gross_annual_salary / 12,2)
monthly_ret_contrib = round((percent_ret_contrib / 100) * gross_monthly_income,2)
monthly_after_contrib = round(gross_monthly_income - monthly_ret_contrib,2) 

gross_paycheck = round(gross_monthly_income/2,2)
paycheck_ret_contrib = round(monthly_ret_contrib/2,2)
paycheck_before_contrib = round(paycheck + paycheck_ret_contrib,2)
taxes_deductions = round(gross_paycheck - (paycheck_ret_contrib+paycheck),2)
rate_taxes_deductions = (taxes_deductions/gross_paycheck)

# Total Included Expenses
sum_included_expenses = edited_df.loc[edited_df['Include'] == True, 'MonthlyCost'].sum()
monthly_netnet = (paycheck*2) - sum_included_expenses
monthly_nwc = (paycheck*2) - sum_included_expenses + edited_df.loc['Loans']['MonthlyCost']

# st.sidebar.write(sum_included_expenses)
# st.sidebar.write(monthly_netnet)
# st.sidebar.write(monthly_nwc)



#st.sidebar.write(f'Gross Annual Income: ${gross_annual_salary}')
scol1.write(f'Gross Monthly Income: ${gross_monthly_income}')
scol2.write(f'Tax/Deduction Rate: {round(100*rate_taxes_deductions,2)}%')
scol3.write(f'Net Paycheck: ${paycheck}')

##slider selecting number of months or years to calculate
months_ahead = st.sidebar.slider("Months to Calculate",min_value=12,max_value=120,value=24)
sscol1, sscol2 = st.sidebar.columns(2)
emergency_fund_months = sscol1.selectbox("Emergency Fund Months",options=[3,6,9,12])
req_emergency_fund = emergency_fund_months * sum_included_expenses
sscol2.write(f'Req. Emergency Fund: {req_emergency_fund}')





#############################################
# results dataframe
start_date = datetime(2023,9,1)

# Create an empty DataFrame with a datetime index
date_rng = pd.date_range(start=start_date, periods=months_ahead, freq='M')
results_df = pd.DataFrame(index=date_rng)

# Format the index as "MMM-YYYY" (e.g., "Sep-2023")
# results_df.index = datetime.strptime(results_df.index, "%Y-%m-%d %H:%M:%S")
# results_df.index = results_df.index.strftime("%b-%Y")
#results_df.index = [date.strftime("%b-%Y") for date in results_df.index]


# Calculate and add records to the DataFrame
#Add Starting Account Balances
student_loans = 60000
emergency_fund = -5000
savings = 0
cumulative_networthdelta = 0
extra = 0

for i, date in enumerate(date_rng):
    
    # Calculate the cumulative net income
    cumulative_networthdelta += monthly_nwc
    
    # reduce student loans by value in expenses table
    # if loans paid off, add extra to emergency fund
    if emergency_fund >= req_emergency_fund:
        if student_loans <= 0:
            savings += monthly_nwc
        else:
            student_loans -= edited_df.loc['Loans']['MonthlyCost']
            savings += monthly_netnet
    else:
        if student_loans <= 0:
            # extra = edited_df.loc['Loans']['MonthlyCost']
            emergency_fund += monthly_nwc
        else:
            student_loans -= edited_df.loc['Loans']['MonthlyCost']
            emergency_fund += monthly_netnet
    
    
    # Store the cumulative net income in the 'NetWorthDelta' column
    results_df.loc[results_df.index[i], 'MonthlyNetNet'] = monthly_netnet 
    results_df.loc[results_df.index[i], 'NetWorthDelta'] = cumulative_networthdelta
    results_df.loc[results_df.index[i], 'StudentLoanBal'] = student_loans
    results_df.loc[results_df.index[i], 'EmergencyFund'] = emergency_fund
    results_df.loc[results_df.index[i], 'Savings'] = savings
    
# Show Line Chart
st.line_chart(results_df)

### Add Metric
mcol1, mcol2, mcol3, mcol4= st.columns(4)

loans_paid = (results_df['StudentLoanBal'] != 0).sum()
loans_paid_date = (results_df['StudentLoanBal'] == 0).idxmax()
formatted_date = loans_paid_date.strftime("%b-%Y")

mcol1.metric("Months to Pay Off Loans",loans_paid)
mcol2.metric("Payoff Month",formatted_date)

emfunded = (results_df['EmergencyFund'] < req_emergency_fund).sum()
emfunded_date = (results_df['EmergencyFund'] >= req_emergency_fund).idxmax()
emfunded_date = emfunded_date.strftime("%b-%Y")

mcol3.metric("Months to Fill EF",emfunded)
mcol4.metric("Fully Funded On",emfunded_date)
#######
#METRICS SHOW FALSE GOAL COMPLETION WHEN FEWER MONTHS ARE SELECTED WITH THE SLIDER
#######

#Show Results Table
st.table(results_df)


