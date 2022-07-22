import pandas as pd
import numpy as np

dates=['April-20', 'April-21', 'April-22', 'April-23','April-24','April-25']
income=[10,20,10,15,10,12]
expenses=[3,8,4,5,6,10]

df=pd.DataFrame({"Date":dates,
                "Income":income,
                "Expenses":expenses})
df.insert(0, "Empty_1", "")
df.insert(4, "Empty_2", np.nan)
print(df)
