import config

print("OPENAI_API_KEY:", config.OPENAI_API_KEY is not None)

try:
    config.validate_config()
    print("SUCCESS: API key loaded correctly!")
    print("Key starts with:", config.OPENAI_API_KEY[:6] + "******")
except Exception as e:
    print("ERROR:", e)
