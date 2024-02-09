$TARGER_DIR="medicine"

"`nisort:"
poetry run isort $TARGER_DIR

"`nblack:"
poetry run black -t py310 -l 99 $TARGER_DIR

"`nflake8:"
poetry run flake8 $TARGER_DIR --max-line-length=99

"`nmypy tests:"
poetry run mypy $TARGER_DIR --ignore-missing-imports --check-untyped-defs
