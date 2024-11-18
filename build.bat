set PYTHONPATH=%cd%

pyinstaller --name GraphIllustrator --noconsole --onedir --add-data "style/globals.css:style/." --add-data "public/images/icon.webp:." -m src.__main__.py