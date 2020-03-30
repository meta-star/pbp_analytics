- `200` Success With `trust-score` Tag
- `201` Success With `msg` Tag
- `202` Success Without Any Response
- `400` No `version` Tag Found From Request
- `401` Request Decode Error
- `403` urllib3 Got Error
- `404` URL Request Not Found
- `500` Empty Response

To shutdown PBP Server, type:
> curl -d '{"version":1,"shutdown":1}' http://localhost:2020

The halt command will be removed in production.
