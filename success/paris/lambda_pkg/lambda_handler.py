from src.paris_agent import run

def handler(event, context):
    prompt = event.get("prompt", "Hello Lambda from Paris")
    return {
        "statusCode": 200,
        "body": run(prompt)
    }
