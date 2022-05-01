# tushare
import tushare as ts

from Quant.libs.utility.time_util import TimeHelper

TOKEN = "e8ca7cc25f3c308987d6884d29f144c81a1e4f1ffb5a7670bed15f33"
ts.set_token(TOKEN)
ts.pro_api(TOKEN)


def test_tushare(one_ts, end_day=TimeHelper.today(), day_count=60):
    # ts.get_hist_data("600848")
    # ts.get_hist_data("600848", ktype="W")
    code = one_ts["symbol"]
    if one_ts["market"] == "主板":
        high_limit = 9.95  # 涨停板标准
    elif one_ts["market"] == "创业板" or one_ts["market"] == "科创板":
        high_limit = 19.90
    else:
        return False
    # elif one_ts["market"] == "CDR":
    #     ...
    # elif one_ts["market"] == "北交所":
    #     ...

    start_day = TimeHelper.time2str(TimeHelper.add_day(-day_count, TimeHelper.str2time(end_day, "%Y-%m-%d")),
                                    "%Y-%m-%d")
    df = ts.get_hist_data(code, start=start_day, end=end_day)
    range_count = len(df)  # 结果数组的长度， 即这段时间里有多少个交易日
    is_has_three = False  # 是否有连续三天的涨停
    limit_arr = []  # 涨停的天数。 应该是3天。如果是4天， 证明连涨之后有过涨停
    continue_day_count = 0
    for i in range(0, range_count):
        p_change = df.iloc[i]['p_change']
        if p_change >= high_limit:
            continue_day_count = continue_day_count + 1
            limit_arr.append(i)
        else:
            continue_day_count = 0
        if continue_day_count >= 3:
            is_has_three = True
            print(i)
            break
    result = len(limit_arr) <= 4 and is_has_three  # 不能出现涨停， 并且有连续三个涨停
    return result


def outside(end_day=TimeHelper.today(), day_count=60):
    # 获取全部的股票代码
    result = []
    pro = ts.pro_api(TOKEN)
    all_ts_df = pro.stock_basic(list_status="L")
    range_count = len(all_ts_df)
    for i in range(0, range_count):
        one_ts = all_ts_df.iloc[i]
        is_has_three = test_tushare(one_ts, end_day, day_count)
        if is_has_three:
            result.append(one_ts["symbol"])
    print(result)
    return result


code = "002800"
test_tushare(code)
ts.get_stock_basics()
outside(day_count=30)
