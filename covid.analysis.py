# covid_analysis_demo.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# ---------- OPTION A: Quick demo (no download needed) ----------
dates = pd.date_range(start="2020-01-01", periods=300)
np.random.seed(0)
new_cases = np.random.poisson(lam=200, size=len(dates)) + np.linspace(0,1000,len(dates)).astype(int)
new_deaths = (new_cases * 0.02).astype(int) + np.random.poisson(5, size=len(dates))
new_recoveries = (new_cases * 0.8).astype(int) + np.random.poisson(10, size=len(dates))

df = pd.DataFrame({
    "date": dates,
    "location": "DemoLand",
    "new_cases": new_cases,
    "new_deaths": new_deaths,
    "new_recoveries": new_recoveries
})

# ---------- OPTION B: Use your own CSV ----------
# df = pd.read_csv('covid_data.csv', parse_dates=['date'])
# Make sure your CSV has at least: date, location (country), new_cases, new_deaths, new_recoveries

# ---------- Basic inspection ----------
print(df.head())
print(df.info())
print("Missing values:\n", df.isnull().sum())

# ---------- Make sure date is datetime ----------
df['date'] = pd.to_datetime(df['date'])

# ---------- Example: plot daily new cases, deaths, recoveries (DemoLand) ----------
country = 'DemoLand'
sub = df[df['location'] == country].sort_values('date').set_index('date')

# compute 7-day moving average
sub['cases_ma7'] = sub['new_cases'].rolling(7, min_periods=1).mean()
sub['deaths_ma7'] = sub['new_deaths'].rolling(7, min_periods=1).mean()
sub['reco_ma7'] = sub['new_recoveries'].rolling(7, min_periods=1).mean()

plt.figure(figsize=(10,5))
plt.plot(sub.index, sub['new_cases'], alpha=0.3, label='Daily cases')
plt.plot(sub.index, sub['cases_ma7'], label='7-day MA')
plt.title(f'COVID: Daily cases - {country}')
plt.xlabel('Date'); plt.ylabel('Cases'); plt.legend()
plt.tight_layout()
plt.savefig('covid_daily_cases.png', dpi=200)
plt.show()
