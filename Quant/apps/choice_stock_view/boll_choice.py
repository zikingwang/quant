# 布林线选股

from jqdatasdk import *
from jqdatasdk.technical_analysis import *


# 方法一， 每天的收盘之后统计符合“1红柱以上”的票。第二天2点再做进一步筛选
from Quant.libs.utility.time_util import TimeHelper


def boll_choice_view(request):
    """
    布林选股
    :param request:
    :return:
    """
    result = get_two_at_once(today_date=TimeHelper.today())
    ...


def get_two_at_once(today_date=TimeHelper.today()):
    # 获取最近的两个交易日
    two_day_list = get_trade_days(end_date=today_date, count=2)
    date = two_day_list[1]
    per_date = two_day_list[0]
    result = filter_two_red_boll(filter_one_red_boll(per_date), date=date)
    return result


def filter_one_red_boll(date):
    print(TimeHelper.now())
    # 所有股票
    all_stocks = get_all_securities(types=["stock"], date=date)
    stock_code_list = list(all_stocks.index.values)
    df_price = _create_df_price(stock_code_list, date)
    result = []
    for stock_code in stock_code_list:
        if _is_red_one(stock_code, df_price):
            result.append(stock_code)
    print(result)
    print(TimeHelper.now())
    return result


def filter_two_red_boll(one_red_stock_list, date="2022-04-29"):
    # 下午的时候使用这个方法， 精确查找双红的股
    df_price = _create_df_price(one_red_stock_list, date)
    result = []
    for stock_code in one_red_stock_list:
        if _is_red_one(stock_code, df_price):
            result.append(stock_code)
    print(result)
    return result


def _create_df_price(stock_code_list, date):
    """
    构造一个一天的带boll三轨的数据集
    :param stock_code_list:
    :param date:
    :return:
    """
    df_price = get_price(stock_code_list, end_date=date, count=1, frequency='daily', fields=None,
                         skip_paused=False, fq='pre', panel=False)
    df_price = df_price.set_index("code")
    df_price["upper_band"], df_price["middle_band"], df_price["lower_band"] = "", "", ""
    upper_band, middle_band, lower_band = Bollinger_Bands(stock_code_list, check_date=date)

    # 补充上轨， 中轨， 下轨
    for stock_code in stock_code_list:
        df_price.loc[stock_code, "upper_band"] = upper_band[stock_code]
        df_price.loc[stock_code, "middle_band"] = middle_band[stock_code]
        df_price.loc[stock_code, "lower_band"] = lower_band[stock_code]
    return df_price


def _is_red_one(stock_code, df_price, approach_rate=0.8):
    stock_price = df_price.loc[stock_code]
    open_price = float(stock_price["open"])
    close_price = float(stock_price["close"])
    high_price = float(stock_price["high"])
    low_price = float(stock_price["low"])
    middle_band_price = float(stock_price["middle_band"])
    lower_band_price = float(stock_price["lower_band"])
    upper_band_price = float(stock_price["upper_band"])
    # 计算带偏移的中轴
    middle_lower_with_approach = middle_band_price - (
            middle_band_price - lower_band_price) * (1 - approach_rate)
    middle_upper_with_approach = middle_band_price + (
            upper_band_price - middle_band_price) * (1 - approach_rate)
    # 是不是红柱
    is_red = bool(close_price > open_price)
    # 是不是在偏移范围内
    is_up_and_approach = bool(middle_band_price <= close_price <= middle_upper_with_approach)
    # 最高值不超过上轨
    not_high = bool(high_price < upper_band_price)
    if is_red and is_up_and_approach and not_high:
        return True
    return False
