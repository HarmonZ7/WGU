import pandas as pd
import numpy as np

#function used to avoid a logical error diving by zero in our debt-to-income data frame. Replaces any NaN values with 0 during division
def safe_divide(a, b):
    result = np.nan_to_num(np.divide(a, b), nan=0)
    return result;

#reads data into our dataframe
df = pd.read_excel('D598_Data_Set.xlsx')

#cleans columns
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.rename(columns={"total_long-term_debt" : "total_long_term_debt"})
#stores and drops duplicates
df_duplicated = df[df.duplicated("business_id")]
df.drop_duplicates()

#performs descriptive statistics
df_statistics = df.groupby("business_state").mean(numeric_only=True)

#creates a data frame for businesses with negative debt to equity
df_neg_debt_equity = df[df["debt_to_equity"] < 0]
df_neg_debt_equity[["business_id", "business_state", "debt_to_equity"]]

#creates a data frame for debt to income, and concatenates it onto our main data frame
df_debt_income = pd.DataFrame({"debt_to_income": safe_divide(df["total_long_term_debt"], df["total_revenue"])})

df_debt_income["business_id"] = df["business_id"]

df_combined = pd.concat([df, df_debt_income["debt_to_income"]], axis=1)

