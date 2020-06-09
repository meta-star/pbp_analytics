Callback Status Code
====================

- `200` Success With `url` And `trust_score` Tag
- `201` Success With `msg` Tag
- `202` Success Without Any Response
- `400` No `version` Tag Found From Request
- `401` Request Decode Error
- `403` `requests` Got Error
- `404` URL Requested Not Found
- `405` URL Requested Was Not HTML
- `500` Empty Response

Correct Request:

    {

        "version":1,

        "url": "https://example.org/"

    }
