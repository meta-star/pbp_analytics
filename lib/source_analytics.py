import whois
from dns import resolver
"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class DomainResolve:
    @staticmethod
    def __dns_resolver_result(handle):
        result = {}

        for message in handle.response.answer:
            for ans in message.items:
                result["address"] = ans.address

        return result

    def host_compare(self, target, compare, debug=False):
        target_handle = resolver.query(target)
        compare_handle = resolver.query(compare)

        target_info = self.__dns_resolver_result(target_handle)
        compare_info = self.__dns_resolver_result(compare_handle)

        score = 0
        level = 1

        if debug:
            print(
                target_info,
                "\n",
                compare_info
            )

        if target_info == compare_info:
            score = 1

        result = score / level

        return round(result, 2)

    @staticmethod
    def info_compare(target, compare, debug=False):
        tests_list = [
            "registrar",
            "whois_server",
            "referral_url",
            "name_servers",
            "emails",
            "org",
            "dnssec",
            "name",
            "address",
            "city",
            "state",
            "country",
        ]

        target_info = whois.whois(target)
        compare_info = whois.whois(compare)

        if debug:
            print(
                target_info,
                "\n",
                compare_info
            )

        score = 0

        for tests in tests_list:
            if target_info.get(tests) == compare_info.get(tests):
                score += 1

        result = score / len(tests_list)

        return round(result, 2)

    @staticmethod
    def _guess():
        result = None
        return result
