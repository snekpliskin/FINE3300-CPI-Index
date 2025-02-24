import pandas as pd
import os

# Set pandas to display all rows
pd.set_option('display.max_rows', None)

# File paths
file_paths = ['Canada.csv', 'Alberta.csv', 'British Columbia.csv', 'Manitoba.csv', 'New Brunswick.csv','Newfoundland & Labrador.csv', 'Nova Scotia.csv', 'Ontario.csv', 'Prince Edward Island.csv','Quebec.csv', 'Saskatchewan.csv']

# Read and combine data
dfs = []
for file in file_paths:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    jurisdiction = os.path.splitext(file)[0]
    df['Jurisdiction'] = jurisdiction
    dfs.append(df)

combined_dfs = []
for df in dfs:
    melted_df = df.melt(id_vars=['Item', 'Jurisdiction'], var_name='Month', value_name='CPI')
    
    # Correct the order of columns
    melted_df = melted_df[['Item', 'Month', 'Jurisdiction', 'CPI']]
    combined_dfs.append(melted_df)

# Combine all the dataframes
final_df = pd.concat(combined_dfs, ignore_index=True)

# Print columns and final dataframe
print("Combined Dataframe columns: ", final_df.columns)

# Print first 12 rows of data into table - answering Q1 and Q2
print(final_df.head(12))

# Convert 'Month' to datetime format
final_df['Month'] = pd.to_datetime(final_df['Month'], format='%y-%b')

# Sort by jurisdiction, item, and date
final_df.sort_values(by=['Jurisdiction', 'Item', 'Month'], inplace=True)

# Report the average month-to-month change in food, shelter, All-items excluding food and energy
items_of_interest = ["Food", "Shelter", "All-items excluding food and energy"]
filtered_df = final_df[final_df['Item'].isin(items_of_interest)].copy()

# Calculate month-to-month percent change
filtered_df['CPI_Change'] = filtered_df.groupby(['Jurisdiction', 'Item'])['CPI'].pct_change() * 100

# Get the average month-to-month percent change - Q3
average_changes = (
    filtered_df.groupby(['Jurisdiction', 'Item'])['CPI_Change']
    .mean()
    .round(1)
    .reset_index()
)

# Use n string for cleaner formatting: new line space
print("\n Average month-to-month change in food, shelter, All-items excluding food and energy:")
print(average_changes)

# Province with the highest average change - Q4
highest_avg_change = average_changes.loc[average_changes.groupby('Item')['CPI_Change'].idxmax()]
print("\n Province with the highest average change in the above categories:")
print(highest_avg_change)

# Compute the annual change in CPI for services across Canada and all provinces - Q5
services_df = final_df[final_df['Item'] == 'Services'].copy()

# Compute the annual change in CPI for services
services_df['Year'] = services_df['Month'].dt.year
annual_change_services = services_df.groupby(['Jurisdiction', 'Year'])['CPI'].agg(['first', 'last'])
annual_change_services['Annual_CPI_Change'] = ((annual_change_services['last'] - annual_change_services['first']) / annual_change_services['first']) * 100

# Round to one decimal place
annual_change_services['Annual_CPI_Change'] = annual_change_services['Annual_CPI_Change'].round(1)

print("\n Annual change in CPI for services across Canada and all provinces:")
print(annual_change_services[['Annual_CPI_Change']])

# Region with the highest inflation in services - Q6
highest_inflation_region = annual_change_services['Annual_CPI_Change'].idxmax()
print("\n Region with the highest inflation in services:")
print(annual_change_services.loc[highest_inflation_region])
