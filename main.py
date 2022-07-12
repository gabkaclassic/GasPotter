import pandas as pn
import statsmodels.formula.api as sm
from database import DB

db = DB()
query='''
    SELECT DISTINCT ON (d.id) d.value, t.k
    FROM data AS d INNER JOIN (
    SELECT d.id, (d.area * d_t.different) AS k FROM data AS d INNER JOIN different_temperature AS d_t ON d.date = d_t.date  
    ) AS t ON d.id = t.id;
'''
result = db.request(query)
value = []
k = []

for x in result:
    value.append(x[0])
    k.append(x[1])
data1 = {
    "value": value,
    "k": k,
}
df1 = pn.DataFrame(data1)
result = sm.ols(formula="value ~ k", data=df1.dropna()).fit()
print(result.params)
print(df1.dropna().corr())
