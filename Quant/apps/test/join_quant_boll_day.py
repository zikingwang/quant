from jqdatasdk import *
from jqdatasdk.technical_analysis import *

from Quant.libs.utility.time_util import TimeHelper

auth('13554053099', 'Wzj8023479')

"""
get_current_data
get_security_info
get_bars
"""


def choose_stock_by_boll():
    all_stocks = get_all_securities(types=["stock"], date=TimeHelper.now())
    stock_codes = list(all_stocks.index.values)
    result = []
    for stock_code in stock_codes:
        if check_one_stock_with_boll(stock_code=stock_code):
            print(stock_code)
            result.append(stock_code)
    print(result)
    return result


def temp_test():
    # 临时测试， 找到一个就退出
    all_stocks = get_all_securities(types=["stock"], date=TimeHelper.now())
    stock_codes = list(all_stocks.index.values)
    result = []
    for stock_code in stock_codes:
        if check_one_stock_with_boll2(stock_code=stock_code):
            print(stock_code)
            result.append(stock_code)
            # break
    print(result)
    return result


def check_one_stock_with_boll(unit="1d", stock_code="000001.XSHE", approach_rate=0.80, trade_count=5):
    """
    security_list：股票列表
    check_date：要查询数据的日期
    timeperiod：统计的天数timeperiod
    nbdevup：统计的天数 nbdevup
    nbdevdn：统计的天数 nbdevdn
    unit：统计周期，默认为 '1d', 支持如下周期: '1m', '5m', '15m', '30m', '60m', '120m', '1d', '1w', '1M'. '1w' 表示一周, ‘1M' 表示一月
    include_now：是否包含当前周期，默认为 True
    fq_ref_date：复权基准日，默认为 None
    由下转上表明股价由弱转强， 是第一个买入信号
    开口和缩口表示股价的波动幅度
    boll线有明显的滞后性
    :param unit:
    :param stock_code:
    :param approach_rate: 接近率，100%是触碰布林线才算。默认0.80
    :return:
    """
    df_price = _create_df_price(stock_code, trade_count)

    # 判断条件：前面4天的close皆小于中轴偏移approach_rate， 最后一天高于中轴偏移approach_rate
    is_up = False
    for index in range(0, 5):
        day_price = df_price.iloc[[index]]
        close_price = float(day_price["close"])
        middle_band_price = float(day_price["middle_band"])
        lower_band_price = float(day_price["lower_band"])
        # 计算带偏移的中轴
        middle_lower_with_approach = middle_band_price - (
                middle_band_price - lower_band_price) * (1 - approach_rate)
        if index <= 3:
            # 前4天要求全都小于middle_lower_with_approach,不然就跳出循环
            if close_price >= middle_lower_with_approach:
                break
        else:
            # 最后一天越过带偏移的中轴
            if close_price >= middle_lower_with_approach:
                is_up = True
    return is_up


def check_one_stock_with_boll2(stock_code, approach_rate=0.80, stable_count=2):
    df_price = _create_df_price(stock_code, stable_count)
    is_stable = True
    for index in range(0, 2):
        day_price = df_price.iloc[[index]]
        open_price = float(day_price["open"])
        close_price = float(day_price["close"])
        high_price = float(day_price["high"])
        low_price = float(day_price["low"])
        middle_band_price = float(day_price["middle_band"])
        lower_band_price = float(day_price["lower_band"])
        upper_band_price = float(day_price["upper_band"])
        # 计算带偏移的中轴
        middle_lower_with_approach = middle_band_price - (
                middle_band_price - lower_band_price) * (1 - approach_rate)
        middle_upper_with_approach = middle_band_price + (
                upper_band_price - middle_band_price) * (1 - approach_rate)
        # 这5天最高和最低都在偏移量之内
        if (close_price > open_price) and (close_price > middle_band_price) and middle_lower_with_approach <= close_price <= middle_upper_with_approach and close_price > middle_band_price and high_price < upper_band_price:
            # if middle_lower_with_approach <= low_price <= middle_upper_with_approach and middle_lower_with_approach <= high_price <= middle_upper_with_approach and close_price>middle_band_price:
            continue
        else:
            is_stable = False
            break
    return is_stable


def _create_df_price(stock_code, day_count):
    """
    构造一个n天的带boll三轨的数据集
    :param stock_code:
    :param day_count:
    :return:
    """
    # 取最近n个交易日,时间类型
    date_list = get_trade_days(count=day_count)
    date_list = ["2022-04-28", "2022-04-29"]
    # 获取这n个交易日的price
    # start_date = TimeHelper.time2str(date_list[0], "%Y-%m-%d")
    # end_date = TimeHelper.time2str(date_list[-1], "%Y-%m-%d")
    start_date = "2022-04-28"
    end_date = "2022-04-29"
    df_price = get_price(stock_code, start_date=start_date, end_date=end_date, frequency='daily', fields=None,
                         skip_paused=False, fq='pre', panel=False)
    # 构造这几天的上轨， 中轨， 下轨
    upper_band_list = []
    middle_band_list = []
    lower_band_list = []
    for one_date in date_list:
        upper_band, middle_band, lower_band = Bollinger_Bands([stock_code], check_date=one_date)
        # print("upper_band:{}".format(upper_band[stock_code]))
        # print("middle_band:{}".format(middle_band[stock_code]))
        # print("lower_band:{}".format(lower_band[stock_code]))
        upper_band_list.append(upper_band[stock_code])
        middle_band_list.append(middle_band[stock_code])
        lower_band_list.append(lower_band[stock_code])
    df_price["upper_band"] = upper_band_list
    df_price["middle_band"] = middle_band_list
    df_price["lower_band"] = lower_band_list
    return df_price


def _check_is_stable():
    ...
