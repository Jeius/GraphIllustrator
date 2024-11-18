set PYTHONPATH=%cd%

pyinstaller --name GraphIllustrator --noconsole --onedir --add-data "style/globals.css:style/." --add-data "favicon.ico:." src/__main__.py