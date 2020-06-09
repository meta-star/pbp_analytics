Production
==========

In order to security reason, ought not to using without docker_ for decreasing danger on the host server.

.. _docker: https://docker.io

Build and Install with Docker
-----------------------------

- Configure `config.ini` at first.

- Follow these commands:

        sudo docker build -t pbpa .
        
        sudo docker run --network=host --detach pbpa
  
Easy Install
------------

Please register the API key of the public databases Analytics using.

The command will help you create and run Analytics.

        sudo docker run \\

            -e PBP_CFG=1 \\

            -e PBP_MySQL_host=<Database Host> \\

            -e PBP_MySQL_database=<Database Name > \\

            -e PBP_MySQL_user=<Database Username> \\

            -e PBP_MySQL_passwd=<Database Password> \\

            -e PBP_SafeBrowsing_google_api_key=<Google API Token> \\

            -e PBP_PhishTank_username=<PhishTank Username> \\

            -e PBP_PhishTank_api_key=<PhishTank API Token> \\

            -e PBP_WebCapture_capture_type=1 \\

            --name=pbpa --network=host --detach starinc/pbp-analytics
