# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl

# %%
# We're going to use a new dataset here, to demonstrate how to deal with larger datasets. This is a subset of the of 311 service requests from [NYC Open Data](https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9).
# because of mixed types we specify dtype to prevent any errors
##complaints = pd.read_csv("../data/311-service-requests.csv", dtype="unicode")
##complaints.head()

pl_complaints = pl.read_csv("../data/311-service-requests.csv", infer_schema = False)
# schema is the polars word for column types, and infer means guess. This means don't guess, treat every column as text.

# %%
# TODO: rewrite the above using the polars library and call the data frame pl_complaints
# Hint: we need the dtype argument reading all columns in as strings above in Pandas due to the zip code column containing NaNs as "NA" and some zip codes containing a dash like 1234-456
# you cannot exactly do the same in Polars but you can read about some other solutions here:
# see a discussion about dtype argument here: https://github.com/pola-rs/polars/issues/8230

# %%
# Selecting columns:
pl_complaints["Complaint Type"]

# %%
# TODO: rewrite the above using the polars library

# %%
# Get the first 5 rows of a dataframe
#complaints[:5]
pl_complaints.head(5)

# %%
# TODO: rewrite the above using the polars library

# %%
# Combine these to get the first 5 rows of a column:
#complaints["Complaint Type"][:5]
pl_complaints["Complaint Type"].head(5)

# %%
# TODO: rewrite the above using the polars library


# %%
# Selecting multiple columns
#complaints[["Complaint Type", "Borough"]]
pl_complaints.select("Complaint Type", "Borough")
# %%
# TODO: rewrite the above using the polars library

# %%
# What's the most common complaint type?
#complaint_counts = complaints["Complaint Type"].value_counts()
#complaint_counts[:10]
complaint_counts = pl_complaints["Complaint Type"].value_counts(sort=True)
complaint_counts.head(10)
# %%
# TODO: rewrite the above using the polars library
# polars doesn't sort by default, so we need the sort argument

# %%
# Plot the top 10 most common complaints
plt.bar(complaint_counts.head(10)["Complaint Type"], complaint_counts.head(10)["count"])
#since the output in a polars value count is a table rather than a series as it is in pandas, we need to use the column names to plot x and y. 
plt.title("Top 10 Complaint Types")
plt.xlabel("Complaint Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# %%
# TODO: please do the same with Polars
