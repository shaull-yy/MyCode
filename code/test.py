import pandas as pd

variants = pd.DataFrame({
	"strain": ["strain1", "strain2", "strain1", "strain3"],
	"position": [100, 200, 150, 300]
})
print('-------fd------')
print(variants)

vv = variants["strain"] != 'strain1'
print('------boolear ser------')
print(vv)

print('---df by vv -------')

v = variants[~vv]
print(v)
