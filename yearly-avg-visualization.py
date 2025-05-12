import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from dbconfig import db_config

# Connect to the database
database = mysql.connector.connect(**db_config)

event = "100m"
top_amount = "50"

query = f"""
    WITH RankedResults AS (
        SELECT *,
               RANK() OVER (PARTITION BY YEAR(race_date) ORDER BY mark_in_seconds ASC) AS rnk
        FROM results
        WHERE event = '{event}'
        /*AND TIMESTAMPDIFF(YEAR, date_of_birth, race_date) <= 22
        --AND nationality = 'USA'*/
    )
    SELECT
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1980 THEN mark_in_seconds END), 2) AS `1980`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1981 THEN mark_in_seconds END), 2) AS `1981`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1982 THEN mark_in_seconds END), 2) AS `1982`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1983 THEN mark_in_seconds END), 2) AS `1983`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1984 THEN mark_in_seconds END), 2) AS `1984`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1985 THEN mark_in_seconds END), 2) AS `1985`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1986 THEN mark_in_seconds END), 2) AS `1986`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1987 THEN mark_in_seconds END), 2) AS `1987`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1988 THEN mark_in_seconds END), 2) AS `1988`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1989 THEN mark_in_seconds END), 2) AS `1989`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1990 THEN mark_in_seconds END), 2) AS `1990`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1991 THEN mark_in_seconds END), 2) AS `1991`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1992 THEN mark_in_seconds END), 2) AS `1992`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1993 THEN mark_in_seconds END), 2) AS `1993`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1994 THEN mark_in_seconds END), 2) AS `1994`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1995 THEN mark_in_seconds END), 2) AS `1995`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1996 THEN mark_in_seconds END), 2) AS `1996`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1997 THEN mark_in_seconds END), 2) AS `1997`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1998 THEN mark_in_seconds END), 2) AS `1998`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 1999 THEN mark_in_seconds END), 2) AS `1999`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2000 THEN mark_in_seconds END), 2) AS `2000`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2001 THEN mark_in_seconds END), 2) AS `2001`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2002 THEN mark_in_seconds END), 2) AS `2002`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2003 THEN mark_in_seconds END), 2) AS `2003`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2004 THEN mark_in_seconds END), 2) AS `2004`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2005 THEN mark_in_seconds END), 2) AS `2005`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2006 THEN mark_in_seconds END), 2) AS `2006`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2007 THEN mark_in_seconds END), 2) AS `2007`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2008 THEN mark_in_seconds END), 2) AS `2008`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2009 THEN mark_in_seconds END), 2) AS `2009`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2010 THEN mark_in_seconds END), 2) AS `2010`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2011 THEN mark_in_seconds END), 2) AS `2011`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2012 THEN mark_in_seconds END), 2) AS `2012`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2013 THEN mark_in_seconds END), 2) AS `2013`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2014 THEN mark_in_seconds END), 2) AS `2014`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2015 THEN mark_in_seconds END), 2) AS `2015`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2016 THEN mark_in_seconds END), 2) AS `2016`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2017 THEN mark_in_seconds END), 2) AS `2017`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2018 THEN mark_in_seconds END), 2) AS `2018`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2019 THEN mark_in_seconds END), 2) AS `2019`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2020 THEN mark_in_seconds END), 2) AS `2020`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2021 THEN mark_in_seconds END), 2) AS `2021`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2022 THEN mark_in_seconds END), 2) AS `2022`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2023 THEN mark_in_seconds END), 2) AS `2023`,
        ROUND(AVG(CASE WHEN YEAR(race_date) = 2024 THEN mark_in_seconds END), 2) AS `2024`
    FROM RankedResults
    WHERE rnk <= {top_amount}
"""

# Load into DataFrame
df_wide = pd.read_sql(query, database)

# Transpose the wide-format DataFrame
df_long = df_wide.transpose().reset_index()
df_long.columns = ['year', 'avg_time']
df_long['year'] = df_long['year'].astype(int)

# Plotting
plt.figure(figsize=(14, 6))
plt.plot(df_long['year'], df_long['avg_time'], marker='o', linewidth=2, label=f'Avg Top {top_amount} Times')

plt.grid(axis='x')
plt.xticks(ticks=df_long['year'], rotation=45)
plt.title(f'Average Top {top_amount} {event} Times by Year')
plt.xlabel('Year')
plt.ylabel('Average Time (seconds)')

plt.tight_layout()
plt.show()
