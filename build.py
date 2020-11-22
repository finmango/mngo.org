#!/bin/env python
import json
import shutil
from pathlib import Path
from string import Template


def render(tpl_path: Path, **config) -> str:
    with open(tpl_path, "r") as fd:
        tpl = Template(fd.read())
        return tpl.substitute(**config)


if __name__ == "__main__":

    # Process the arguments from the config.json file
    with open("config.json", "r") as fd:
        config = json.load(fd)

    # Make sure that the public folder is empty
    public = Path(__file__).parent / "public"
    if public.exists():
        shutil.rmtree(public)

    # Create the public folder
    public.mkdir()

    # Add favicon.ico to the public folder
    shutil.copy("favicon.ico", public / "favicon.ico")

    # Publish the output under the /public folder as 404.html to catch all routes
    with open(public / "404.html", "w") as fd:
        fd.write(render("index.tpl.html", **config))

    # Publish our custom 404 page under the /public folder
    with open(public / "not-found.html", "w") as fd:
        fd.write(render("not-found.tpl.html", **config))

    # Publish the QR code generator into the /public/admin folder
    (public / "admin").mkdir()
    shutil.copy("mango.png", public / "admin" / "mango.png")
    shutil.copy("qrgen.html", public / "admin" / "qrgen.html")
    shutil.copy("favicon.ico", public / "admin" / "favicon.ico")
