import pandas as pd
import sqlite3

# TRANSFORM
df = pd.read_csv("../data/HP_financial_raw_data.csv")

# Filling Null values in DmdCd
# df['DmdCd'] = df['DmdCd'].replace('',np.nan) #changed blank DmdCd data first to Nan
df['DmdCd'].ffill(inplace=True)

# Removing rows which contains Total
df = df[df['DmdCd'].str.contains("Total")==0]
df = df[df['HOA'].str.contains("Total")==0]

# Splitting DmdCd & HOA columns
# split function in our case is creating more than required columns with null values so using iloc to select only required columns
df[['DemandCode ','Demand']] = df['DmdCd'].str.split(pat='-',expand=True).iloc[:,:2]
df[['MajorHead','SubMajorHead','MinorHead','SubMinorHead','DetailHead','SubDetailHead',
    'BudgetHead','PlanNonPlan','VotedCharged','StatementofExpenditure']]=df['HOA'].str.split(pat='-',expand=True).iloc[:,:10]

# Removing Unnamed, DmdCd & HOA columns
df = df.iloc[:,3:]


#LOAD

conn = sqlite3.connect('hp_stat_fscl.db')
cursor = conn.cursor()

table_name = 'HP_FSCL_DATA'
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Testing
cursor.execute("SELECT sql from sqlite_master WHERE type = 'table' and name = 'HP_FSCL_DATA'")
schema = cursor.fetchall()
print(schema)
cursor.execute("SELECT * FROM HP_FSCL_DATA")
row = cursor.fetchone()
print(row)

conn.close()
