# %%
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt


# %%
# Reading data from a csv file
# You can read data from a CSV file using the `read_csv` function. By default, it assumes that the fields are comma-separated.

# We're going to be looking at some cyclist data from Montréal. Here's the [original page](http://donnees.ville.montreal.qc.ca/dataset/velos-comptage) (in French), but it's already included in this repository. We're using the data from 2012.

# This dataset is a list of how many people were on 7 different bike paths in Montreal, each day.

broken_df = pd.read_csv("../data/bikes.csv", encoding="ISO-8859-1")

# Polars: same call name. For non-UTF8 encodings Polars decodes the file in
# Python first, then parses it, so "ISO-8859-1" works here.
pl_broken_df = pl.read_csv("../data/bikes.csv", encoding="ISO-8859-1")

# %%
# Look at the first 3 rows
broken_df[:3]

# Polars: .head(3) is the idiomatic way. Slicing with pl_broken_df[:3] also works.
pl_broken_df.head(3)

# %%
# You'll notice that this is totally broken! `read_csv` has a bunch of options that will let us fix that, though. Here we'll

# * change the column separator to a `;`
# * Set the encoding to `'latin1'` (the default is `'utf8'`)
# * Parse the dates in the 'Date' column
# * Tell it that our dates have the day first instead of the month first
# * Set the index to be the 'Date' column

fixed_df = pd.read_csv(
    "../data/bikes.csv",
    sep=";",
    encoding="latin1",
    parse_dates=["Date"],
    dayfirst=True,
    index_col="Date",
)
fixed_df[:3]

# Polars differences:
# * the separator argument is `separator`, not `sep`
# * there is no index in Polars, so "Date" stays a normal column
# * there is no `dayfirst` flag, so we parse the dates ourselves with an explicit format
pl_fixed_df = pl.read_csv(
    "../data/bikes.csv",
    separator=";",
    encoding="latin1",
).with_columns(pl.col("Date").str.to_date("%d/%m/%Y"))
pl_fixed_df.head(3)


# %%
# Selecting a column
# When you read a CSV, you get a kind of object called a `DataFrame`, which is made up of rows and columns. You get columns out of a DataFrame the same way you get elements out of a dictionary.

# Here's an example:
fixed_df["Berri 1"]

# Polars: the same bracket syntax returns a Series.
pl_fixed_df["Berri 1"]

# Or use .select(), which returns a one-column DataFrame and is the more
# "Polars way" because it works inside lazy queries too.
pl_fixed_df.select("Berri 1")


# %%
# Plotting is quite easy in Pandas
fixed_df["Berri 1"].plot()

# Polars has no built-in matplotlib plotting, so pass the columns to matplotlib directly.
# Without an index we use the Date column as the x axis.
plt.figure()
plt.plot(pl_fixed_df["Date"], pl_fixed_df["Berri 1"])
plt.xlabel("Date")
plt.ylabel("Cyclists")
plt.title("Berri 1")
plt.show()

# Newer Polars versions also have `.plot` (needs `altair` installed):
# pl_fixed_df.plot.line(x="Date", y="Berri 1")


# %%
# We can also plot all the columns just as easily. We'll make it a little bigger, too.
# You can see that it's more squished together, but all the bike paths behave basically the same -- if it's a bad day for cyclists, it's a bad day everywhere.

fixed_df.plot(figsize=(15, 10))

# Polars: loop over every column except Date and draw each as a line.
fig, ax = plt.subplots(figsize=(15, 10))
for col in pl_fixed_df.columns:
    if col != "Date":
        ax.plot(pl_fixed_df["Date"], pl_fixed_df[col], label=col)
ax.legend()
plt.show()

# Seaborn alternative: convert the wide table to long format first.
# import seaborn as sns
# long_df = pl_fixed_df.unpivot(index="Date", variable_name="path", value_name="cyclists")
# sns.lineplot(data=long_df.to_pandas(), x="Date", y="cyclists", hue="path")