import tomli

with open("pyproject.toml", "rb") as f:
    print(tomli.load(f)["project"]["version"])