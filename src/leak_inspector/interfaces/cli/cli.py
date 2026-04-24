import typer

app = typer.Typer()


@app.command()
def auth():
    print("Autenticating process...")
    typer.secho("Autenticación exitosa", fg=typer.colors.GREEN)
    typer.secho("Token generado")


@app.command()
def scan():
    print("🔍 Escaneo iniciado")


@app.command()
def report():
    print("📊 Reporte generado")
