import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, how are you doing today?"
tokens = enc.encode(text)
print(f"Tokens: {tokens}")

# Decode the tokens back to text
decoded_text = enc.decode(tokens)
print(f"Decoded Text: {decoded_text}")
