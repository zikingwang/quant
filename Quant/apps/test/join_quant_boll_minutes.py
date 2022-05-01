from jqdatasdk import *
from jqdatasdk.technical_analysis import *

from Quant.libs.utility.time_util import TimeHelper
DEV_VALUE = 0.999


def check_boll_15min():
    stock_code = '000014.XSHE'
    # upper_band, middle_band, lower_band = Bollinger_Bands([stock_code], check_date="2022-04-29", unit="15m",  include_now=True)
    df = Bollinger_Bands([stock_code], check_date="2022-04-29", unit="15m", include_now=True, timeperiod=20, nbdevup=2,
                         nbdevdn=2)
    df2 = get_bars(stock_code, 10, unit='15m',
                   fields=['date', 'open', 'high', 'low', 'close'],
                   include_now=True, end_dt=None, fq_ref_date=None, df=True)
    print("test")
