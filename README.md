# Rates API
An API server to query current BTC/USD exchange rate, actual rates are fetched from `alpha vantage`.

### Running

`docker-compose` will pull and start the required database and servers:

```
docker-compose up
```

You can retry it with `sudo` if you face any permission issues.

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


TO revoke this key, issue the `revokekey` command:

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

