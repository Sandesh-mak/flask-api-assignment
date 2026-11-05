import secrets


keys = [secrets.token_hex(16) for _ in range(3)]

print("--- Generated API Keys ---")
for idx, key in enumerate(keys, start=1):
    print(f"Consumer {idx} Key: {key}")