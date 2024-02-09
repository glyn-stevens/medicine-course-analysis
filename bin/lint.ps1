"`nisort:"
poetry run isort .

"`nblack:"
poetry run black -t py310 -l 79 medicine

"`nflake8:"
poetry run flake8 . --max-line-length=99
