import os
import sys
import time
import traceback

"""
    Copyright (c) 2020 Star Inc.(https://starinc.xyz)

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
        error_info = "occurred in\n{}\non line {}\nin statement {}".format(filename, line, text)
        return "%s\nSystem Error:\n%s\n%s\n%s\n%s\n" % (occur_time, err1, err2, err3, error_info)

    @staticmethod
    def logger(error_msg, silence: bool = True):
        if silence:
            with open("service.log", "a+") as log:
                log.write(error_msg + "\n")
        else:
            print(error_msg)

    @staticmethod
    def set_ready(status: bool):
        check_file = ".alive"
        if status and not os.path.exists(check_file):
            with open(check_file, "w") as f:
                return f.write("")
        elif not status and os.path.exists(check_file):
            return os.remove(check_file)

    @staticmethod
    def check_ready():
        check_file = ".alive"
        return os.path.isfile(check_file)
