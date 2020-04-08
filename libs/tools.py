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

check_file = ".alive"


class Tools:
    @staticmethod
    def get_time(time_format: str = "%b %d %Y %H:%M:%S %Z"):
        """
        Get datetime with format
        :param time_format: string of format codes
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
        filename, line, _, text = tb_info[-1]
        error_info = "occurred in\n{}\non line {}\nin statement {}".format(filename, line, text)
        return "%s\nSystem Error:\n%s\n%s\n%s\n%s\n" % (occur_time, err1, err2, err3, error_info)

    @staticmethod
    def logger(error_msg, silent: bool = True):
        """
        Journal or print error message
        :return:
        """
        if silent:
            with open("service.log", "a+") as log:
                log.write(error_msg + "\n")
        else:
            print(error_msg)

    @staticmethod
    def set_ready(status: bool):
        """
        Set status whether service is ready or not
        :param status: bool of status
        :return:
        """
        if status and not os.path.exists(check_file):
            with open(check_file, "w") as f:
                f.write("")
        elif not status and os.path.exists(check_file):
            os.remove(check_file)

    @staticmethod
    def check_ready():
        """
        Check status that service is ready or not
        :return: bool of status
        """
        return os.path.isfile(check_file)

    @staticmethod
    def lists_separate(lists: list, numbers: int):
        """
        Split lists to average
        :param lists: list you want to separate
        :param numbers: numbers in part you want
        :return:
        """
        for count in range(0, len(lists), numbers):
            yield lists[count:count + numbers]
