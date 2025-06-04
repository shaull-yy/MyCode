import pandas as pd

# Sample DataFrame 1 with `customer_id` as the index
df1 = pd.DataFrame({
	'name': ['Alice', 'Bob', 'Charlie'],
	'purchase': [200, 150, 300]
}, index=[1, 2, 3])
df1.index.name = 'customer_id'

# Sample DataFrame 2
df2 = pd.DataFrame({
	'user_id': [1, 2, 4],
	'city': ['New York', 'Los Angeles', 'Chicago'],
	'membership': ['Gold', 'Silver', 'Platinum']
})

# Merge using the index of df1 and the `user_id` column of df2
merged_df = pd.merge(df1, df2, left_on='name', right_on='user_id', how='inner')

print(merged_df)
