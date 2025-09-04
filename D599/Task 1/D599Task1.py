import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as skl
import missingno as msno
from sklearn.impute import SimpleImputer

df = pd.read_csv('Employee Turnover Dataset.csv')

#the above code sets our environment and imports our data
#the below code removes duplicates based on the EmployeeNumber column
df_drop_duplicates = pd.DataFrame(data=df)
df_drop_duplicates = df.drop_duplicates(subset=["EmployeeNumber"])

#Imputes 0 or Unknown onto the appropriate columns with missing values.
zero_imputer = SimpleImputer(strategy='constant', fill_value=0.0)
unknown_imputer = SimpleImputer(strategy='constant', fill_value="Unknown")
cols_to_impute = ["NumCompaniesPreviouslyWorked", "AnnualProfessionalDevHrs"]

df_imputation = pd.DataFrame(data=df_drop_duplicates)
df_imputation[cols_to_impute] = zero_imputer.fit_transform(df_imputation[cols_to_impute])
df_imputation[["TextMessageOptIn"]] = unknown_imputer.fit_transform(df_imputation[["TextMessageOptIn"]])

#removes negative values from inappropriate columns
df_abs = pd.DataFrame(data=df_imputation)
df_abs["DrivingCommuterDistance"] = df_abs["DrivingCommuterDistance"].abs()
df_abs["AnnualSalary"] = df_abs["AnnualSalary"].abs()

#recalculates annual salary column due to excessive inconsistancies. 
df_cleaned = pd.DataFrame(data=df_abs)

df_cleaned.rename(columns={"HourlyRate ": "HourlyRate"}, inplace=True)
df_cleaned["HourlyRate"] = df_cleaned["HourlyRate"].astype(str).str.replace(r"[\$,]", "", regex=True)
df_cleaned["HourlyRate"] = pd.to_numeric(df_cleaned["HourlyRate"], errors='coerce')

df_cleaned["AnnualSalary"] = df_cleaned["HourlyRate"] * df_cleaned["HoursWeekly"] * 52

#exports our cleaned data frame to csv format to 
df_cleaned.to_csv("cleaned_dataset.csv", index=False)