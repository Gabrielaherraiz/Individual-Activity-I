import pandas as pd
import seaborn as sns

df = sns.load_dataset("diamonds")

df.to_csv("diamonds_dataset.csv")