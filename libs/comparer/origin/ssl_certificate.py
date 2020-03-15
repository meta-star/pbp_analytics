from cryptography import x509
from cryptography.hazmat.backends import default_backend

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Certificate:
    """
    """

    @staticmethod
    def __dns_resolver_result(pem_data):
        cert = x509.load_pem_x509_certificate(pem_data, default_backend())
        return cert.serial_number
