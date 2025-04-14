import os
from configparser import ConfigParser
import pulumi

# Leer claves desde config
config = pulumi.Config()
aws_access_key_id = config.require("aws_access_key_id")
aws_secret_access_key = config.require("aws_secret_access_key")

# Crear archivo de credenciales
credentials_path = "/home/ubuntu/.aws/credentials"
os.makedirs(os.path.dirname(credentials_path), exist_ok=True)

parser = ConfigParser()
parser["default"] = {
    "aws_access_key_id": aws_access_key_id,
    "aws_secret_access_key": aws_secret_access_key
}
with open(credentials_path, "w") as f:
    parser.write(f)

pulumi.export("archivo_credenciales", credentials_path)
