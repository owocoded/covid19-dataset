import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
from fpdf import FPDF

df = pd.read_csv("owid-covid-data.csv")
#
try:
    df = pd.read_csv("owid-covid-data.csv")
except FileNotFoundError:
    print("Error: File not found! Check the path or filename.")



# Filter the dataset to include countries of interest
countries_of_interest = ["Kenya", "United States", "India", "Nigeria"]
df_filtered = df[df["location"].isin(countries_of_interest)]
df_filtered = df_filtered.copy()
df_filtered["date"] = pd.to_datetime(df_filtered["date"])
#
print(df_filtered.head())  # Display a preview of the filtered data

# Drop rows where critical columns like "date" are missing
critical_columns = ["date", "new_cases", "new_deaths", "people_fully_vaccinated"]
df_cleaned = df.dropna(subset=critical_columns)
#
print("Rows with missing critical values removed ✅")

print(df.head())  # Show first 5 rows
print(df.columns) #check column
print(df.isnull().sum()) #identify the missing value
df.ffill( inplace=True)  # Forward fill missing values
df['date'] = pd.to_datetime(df['date']) # Convert date column to datetime format
df['continent'] = df['location'].str.strip().str.lower() #Normalize country names (example)
df.drop_duplicates(inplace=True) # Drop duplicates

print("Data Cleaning Completed ✅")


# Summary statistics
print(df.describe())

# Remove rows where continent is missing
df = df[df["continent"].notna()]

# Plot COVID-19 case trends over time
plt.figure(figsize=(12,6))
sns.lineplot(x=df["date"], y=df["total_cases"], hue=df["continent"])
plt.title("COVID-19 Cases Over Time by Continent")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.xticks(rotation=45)
plt.legend(title="Continent")
plt.show()

print("EDA Completed ✅")

# # Finding peak infection periods
peak_periods = df.groupby("date")["new_cases"].sum().sort_values(ascending=False).head(10)
print("Peak Infection Periods:", peak_periods)

# Vaccination effectiveness over time
df['vaccination_rate'] = (df['people_fully_vaccinated'] / df['population']) * 100
df['vaccination_rate'] = df['vaccination_rate'].clip(0, 100)  # Cap at 100%
#
avg_vaccine_effect = df.groupby("date")["vaccination_rate"].mean()
print("Corrected Average Vaccination Rate Over Time:", avg_vaccine_effect)
# #
print("Insights Generated ✅")

# Plot total cases over time for selected countries
plt.figure(figsize=(12, 6))
sns.lineplot(x=df_filtered["date"], y=df_filtered["total_cases"], hue=df_filtered["location"])
#
# # Formatting the plot
plt.title("COVID-19 Total Cases Over Time (Kenya, USA, India, Nigeria)")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.xticks(rotation=45)
plt.legend(title="Country")
plt.grid(True)
plt.show()

# Plot total deaths over time for selected countries
plt.figure(figsize=(12, 6))
sns.lineplot(x=df_filtered["date"], y=df_filtered["total_deaths"], hue=df_filtered["location"])
#
# # Formatting the plot
plt.title("COVID-19 Total Deaths Over Time (Kenya, USA, India, Nigeria)")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.xticks(rotation=45)
plt.legend(title="Country")
plt.grid(True)
plt.show()

# Plot daily new cases over time for selected countries
plt.figure(figsize=(12, 6))
sns.lineplot(x=df_filtered["date"], y=df_filtered["new_cases"], hue=df_filtered["location"])

# Formatting the plot
plt.title("Daily New COVID-19 Cases Comparison (Kenya, USA, India, Nigeria)")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.xticks(rotation=45)
plt.legend(title="Country")
plt.grid(True)
plt.show()


# # Plot death rate over time for selected countries
df_filtered["death_rate"] = (df_filtered["total_deaths"] / df_filtered["total_cases"]) * 100  # Convert to percentage
plt.figure(figsize=(12, 6))
sns.lineplot(x=df_filtered["date"], y=df_filtered["death_rate"], hue=df_filtered["location"])

# Formatting the plot
plt.title("COVID-19 Death Rate Over Time (Kenya, USA, India, Nigeria)")
plt.xlabel("Date")
plt.ylabel("Death Rate (%)")
plt.xticks(rotation=45)
plt.legend(title="Country")
plt.grid(True)
plt.show()

# Get the latest available data for each country
latest_data = df[df["date"] == df["date"].max()]  # Filter for most recent date

# Select top 10 countries by total cases
top_countries = latest_data.nlargest(10, "total_cases")

# # Plot bar chart
plt.figure(figsize=(12, 6))
plt.barh(top_countries["location"], top_countries["total_cases"], color="skyblue")
plt.xlabel("Total Cases")
plt.ylabel("Country")
plt.title("Top 10 Countries by Total COVID-19 Cases")
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.grid(axis="x", linestyle="--", alpha=0.7)
print(top_countries.head())  # Check top 10 countries data


# Identify peak infection periods for reporting
peak_periods = df.groupby("date")["new_cases"].sum().sort_values(ascending=False).head(10)

# Generate PDF report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="COVID-19 Data Analysis Report", ln=True, align="C")

# Add peak infection dates to the report
for index, row in peak_periods.items():
    pdf.cell(200, 10, txt=f"Peak Infection Date: {index.strftime('%Y-%m-%d')}, Cases: {int(row):,}", ln=True)

pdf.output("Covid19_Report.pdf")
print("Report Generated ✅")