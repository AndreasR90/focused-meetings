from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from main import app

html_content = open("dist/index.html").read().replace("\n", "")
app.mount("/js", StaticFiles(directory="dist/js"), name="js")
app.mount("/css", StaticFiles(directory="dist/css"), name="css")
app.mount("/img", StaticFiles(directory="dist/img"), name="img")


@app.get("/")
def index():
    return HTMLResponse(html_content)
