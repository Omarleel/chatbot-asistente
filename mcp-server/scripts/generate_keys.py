from fastmcp.server.auth.providers.bearer import RSAKeyPair

key_pair = RSAKeyPair.generate()

# Convertir SecretStr -> str
private_key_str = key_pair.private_key.get_secret_value()
public_key_str = key_pair.public_key

# Escribir a archivos
with open("private_key.pem", "w") as f:
    f.write(private_key_str)

with open("public_key.pem", "w") as f:
    f.write(public_key_str)

print("✅ Keys written to private_key.pem and public_key.pem!")
