import gdelt


gd2 = gdelt.gdelt(version=2)

# will pull the last 15 minute interval only unless we set coverage=True
df = gd2.Search("2020-11-24",table='gkg', coverage=True)

# persist to local storage just in case
df.to_csv("gkg_20201124.csv", index=False)