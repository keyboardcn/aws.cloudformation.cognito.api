import json
import urllib.request

def lambda_handler(event, context):
    coin = "bitcoin"
    currency = "usd"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"

    try:
        with urllib.request.urlopen(url) as response:
            result = json.loads(response.read())
            price = result[coin][currency]
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "coin": coin,
                    "currency": currency,
                    "price": price
                })
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
