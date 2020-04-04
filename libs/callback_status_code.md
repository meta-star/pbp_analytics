- `200` Success With `url` And `trust-score` Tag
- `201` Success With `msg` Tag
- `202` Success Without Any Response or Server Not Ready
- `400` No `version` Tag Found From Request
- `401` Request Decode Error
- `403` urllib3 Got Error
- `404` URL Request Not Found
- `500` Empty Response

Correct Response:

    {
        "version":1,
        "url": "https://example.org/"
    }
