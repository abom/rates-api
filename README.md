# Rates API
An API server to query current BTC/USD exchange rate, actual rates are fetched from `alpha vantage`.

### Running

Before running, you will have to set `alpha vantage` API key in `.env` file inside the root directory of this repository, the file should contain at least the environment variable of `ALPHAVANTAGE_API_KEY`, example:

```
PYTHONUNBUFFERED=1
ALPHAVANTAGE_API_KEY=XOMNEID0Q7OJO5E4
```

You can get your alphavantage.com API key from [here](https://www.alphavantage.co/support/#api-key).

Then you can use `docker-compose`, which will pull and start the required database and servers

```
sudo docker-compose up
```

You can retry it without `sudo` if you didn't face any permission issues.

#### Generating and revoking API keys

Using the custom `genkey` and `revokekey` commands:

```
docker-compose run web python manage.py genkey
```

Output will be like:

```
...
...
Generated API key: dNel0RwE2cv9c9fqBSok9G9Clf5ByPlZcwgtoMquiwZWT1y3DDuJTQi4QLu93KRi
```

You can test force fetching rates or getting current rate by passing this API key in `X-API-KEY` header, an example using `curl` to get current rate:

```
curl http://localhost:8000/api/v1/quotes/ -H "X-API-KEY: dNel0RwE2cv9c9fqBSok9G9Clf5ByPlZcwgtoMquiwZWT1y3DDuJTQi4QLu93KRi"
```

And to force fetching rates:

```
curl -XPOST http://localhost:8000/api/v1/quotes/ -H "X-API-KEY: dNel0RwE2cv9c9fqBSok9G9Clf5ByPlZcwgtoMquiwZWT1y3DDuJTQi4QLu93KRi"
```


To revoke this key, issue the `revokekey` command:

```
docker-compose run web python manage.py revokekey dNel0RwE2cv9c9fqBSok9G9Clf5ByPlZcwgtoMquiwZWT1y3DDuJTQi4QLu93KRi
```

### Running tests

```
docker-compose run web pytest .
```


### API documentation

Base URL is `/api/v1`
Authentication using `X-API-KEY` as a custom header with the value of a generated key.


| URL     | Method | Description                          | Response                                                                                                           | Status code |
| ------- | ------ | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ----------- |
| /quotes | GET    | Get current rate                     | JSON body, example: {"from_currency":"BTC","to_currency":"USD","rate":"49142.73000000","last_update":1629596881.0} | 200         |
| /quotes | POST   | Force fetching latest exchange rates | None                                                                                                               | 204         |


In case of errors, a JSON formatted error will be returned with a corresponding status code, e.g.:

```
{"message": "X-API-Key header is missing or not valid", "code": "authentication_error"}
```
