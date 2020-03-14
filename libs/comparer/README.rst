PBP Comparer
============

What are these?
---------------
These are the libraries for PBP to analytics information of URL.

How these work?
---------------
The libraries will trigger after database checking.

    - target

    Check if content of target is in the database or not.

    - origin

    If the content found, comparing the content with the origin website.

If the URL is not in the phishing records,
PBP_analytics will rank it by the-trust-score.

    the-trust-score:

    - Higher => Safe
    - Lower => Danger
