import pandas as pd

df = pd.read_csv("Dataset/student-por.csv")

print(df.describe())

print("\n\nStudy Time")
print(df["studytime"].value_counts())

print("\n\nFailures")
print(df["failures"].value_counts())

print("\n\nGender")
print(df["sex"].value_counts())