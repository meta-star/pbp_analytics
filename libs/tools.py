import sys
import time
import traceback

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Tools:
    @staticmethod
    def get_time(time_format: str = "%b %d %Y %H:%M:%S %Z"):
        """

        :param time_format:
        :return:
        """
        time_ = time.localtime(time.time())
        return time.strftime(time_format, time_)

    @staticmethod
    def error_report():
        """
        Report errors as message
        :return: string
        """
        occur_time = Tools.get_time()
        err1, err2, err3 = sys.exc_info()
        traceback.print_tb(err3)
        tb_info = traceback.extract_tb(err3)
        filename, line, func, text = tb_info[-1]
        error_info = "occurred in\n{}\n\non line {}\nin statement {}".format(filename, line, text)
        return "%s\nSystem Error:\n\n%s\n%s\n%s\n\n%s\n" % (occur_time, err1, err2, err3, error_info)

    @staticmethod
    def logger(error_msg, write=True):
        if write:
            with open("service.log", "a+") as log:
                log.write(error_msg + "\n")
        else:
            print(error_msg)
