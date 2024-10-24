# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl

# %%
# We're going to use a new dataset here, to demonstrate how to deal with larger datasets. This is a subset of the of 311 service requests from [NYC Open Data](https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9).
# because of mixed types we specify dtype to prevent any errors
pl_complaints = pl.read_csv("../data/311-service-requests.csv", infer_schema_length=0)
pl_complaints.head()

# %%
# TODO: rewrite the above using the polars library and call the data frame pl_complaints
# Hint: we need the dtype argument reading all columns in as strings above in Pandas due to the zip code column containing NaNs as "NA" and some zip codes containing a dash like 1234-456
# you cannot exactly do the same in Polars but you can read about some other solutions here:
# see a discussion about dtype argument here: https://github.com/pola-rs/polars/issues/8230

# %%
# Selecting columns:
pl_complaints.select("Complaint Type")

# %%
# TODO: rewrite the above using the polars library

# %%
# Get the first 5 rows of a dataframe
pl_complaints.head(5)

# %%
# TODO: rewrite the above using the polars library

# %%
# Combine these to get the first 5 rows of a column:
pl_complaints.select("Complaint Type").head(5)
# %%
# TODO: rewrite the above using the polars library


# %%
# Selecting multiple columns
pl_complaints.select(["Complaint Type", "Borough"])

# %%
# TODO: rewrite the above using the polars library

# %%
# What's the most common complaint type?
pl_complaint_counts = pl_complaints.groupby("Complaint Type").agg(pl.count()).sort("count", reverse=True)
pl_complaint_counts.head(10)

# %%
# TODO: rewrite the above using the polars library

# %%
# Plot the top 10 most common complaints
top_10_complaints = pl_complaint_counts.head(10).to_pandas()
top_10_complaints.plot(kind="bar", x="Complaint Type", y="count")
plt.title("Top 10 Complaint Types")
plt.xlabel("Complaint Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
# %%
# TODO: please do the same with Polars
