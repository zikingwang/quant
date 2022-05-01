import pandas as pd
import pymongo

cursor = daily_tbl.find({"code": "002157", "trade_status": "交易", "time": {"$gte": "2016-01-01", "$lte": "2018-05-25"}},
                        {"_id": 0, "date": 1, "close": 1, "adjfator": 1})
cursor.sort("date", pymongo.ASCENDING)
df = pd.DataFrame.from_records(cursor)
lf = df.iloc[-1]["adjfactor"]
df["hfq"] = df["close"] * df["adjfactor"]
df["qfq"] = df["close"] * df["adjfactor"] / lf

df.index = df.pop("date")
df.pop("adjfactor")
