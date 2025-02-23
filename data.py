import pandas as pd

# Get the filenames
import os 

file_paths = ['Canada.csv', 'Alberta.csv', 'British Columbia.csv', 'Manitoba.csv', 'New Brunswick.csv', 'Newfoundland & Labrador.csv', 'Nova Scotia.csv', 'Ontario.csv', 'Prince Edward Island.csv', 'Quebec.csv', 'Saskatchewan.csv']

dfs = []
for file in file_paths:
    # Read each CSV file into pandas
    df = pd.read_csv(file)

    # Clean the column names
    df.columns = df.columns.str.strip()

    # Retrieve jurisdiction column from the filename (and remove '.csv')
    jurisdiction = os.path.splitext(file)[0]

    # Add jurisdiction column in column 3
    df['Jurisdiction'] = jurisdiction
    dfs.append(df)

combined_dfs = []

for df in dfs:
    # Melt the datafram to get column names
    melted_df = df.melt(id_vars = ['Item', 'Jurisdiction'], var_name = 'Month', value_name = 'CPI')
    
    # Correct the order of columns
    melted_df = melted_df[['Item', 'Month', 'Jurisdiction', 'CPI']]
    combined_dfs.append(melted_df)

# Combine all the dataframes - answering Q1
final_df = pd.concat(combined_dfs, ignore_index=True)

# Print columns and final dataframe
print("Combined Dataframe columns: ", final_df.columns)

# Print first 12 rows of data into table - answering Q2
print(final_df.head(12))