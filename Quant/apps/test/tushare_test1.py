# _*_ coding: utf-8 _*_
#  示例：突破信号
# 突破55日前高，作为买入信号
# 细节：当日突破/前日未突破，日线复权处理
"""

"""

import tushare as ts
import pandas as pd

TOKEN = "e8ca7cc25f3c308987d6884d29f144c81a1e4f1ffb5a7670bed15f33"
ts.set_token(TOKEN)
ts.pro_api(TOKEN)

windows_size = 55
code = "000001"

temp = ts.get_k_data(code, start="2021-03-01", ktype="D", autype="qfq")  # D日线 前复权
# 设置dataframe的索引
temp.index = temp.pop("date")

df = temp.loc[:, ["close", "high"]]  # 所有行的close和high这两列取出来

df["hhv"] = df["high"].rolling(windows_size).max()  # 每一个滑动窗口里的最高价，赋值给dataframe
df["pre_hhv"] = df["hhv"].shift(1)  # 前移一格，即前一天的hhv
df["signals"] = (df["close"].shift(1) <= df["pre_hhv"].shift(1)) and (
            df["close"] > df["pre_hhv"])  # 收盘价大于前一天的hhv（55日前高）,并且前一天没有产生信号， 就产生信号
results = df(df["signals"])  # 将信号为true的行拿出来
print(results)
print(list(results.index))  # 只打印日期
print(df)

# 获取股票列表
# stock_list = ts.get_stock_basics()
pro = ts.pro_api(TOKEN)
stock_list = pro.stock_basic()
for code, name in stock_list.iteritems():
    ...
