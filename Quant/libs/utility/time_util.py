import datetime


class TimeHelper(object):
    @staticmethod
    def now():
        """
        获取当前时间
        :return: datetime实例
        """
        return datetime.datetime.now()

    @staticmethod
    def today():
        """
        获取今天日期 YYYY-MM-DD
        :return:
        """
        t = TimeHelper.now()
        return datetime.datetime.strftime(t, "%Y-%m-%d")

    @staticmethod
    def time2str(t=None, f='%Y-%m-%d %H:%M:%S'):
        """
        将日期转成字符串

        :param t:
        :param f:
        :return:
        """

        if not t:
            t = TimeHelper.now()

        return datetime.datetime.strftime(t, f)

    @staticmethod
    def str2time(s, f='%Y-%m-%d %H:%M:%S'):
        """
        将字符串转成日期格式

        :param t:
        :param f:
        :return:
        """

        return datetime.datetime.strptime(s, f)

    @staticmethod
    def add_day(n, d=None):
        """
        日期加n天
        :param n: 天数
        :param d: datetime实例 "2018-08-10 12:35:40"
        :return:
        """
        if d is None:
            d = TimeHelper.now()
        return d + datetime.timedelta(days=n)
