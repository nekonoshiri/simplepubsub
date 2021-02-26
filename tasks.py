import invoke


@invoke.task()
def check(c):
    """Run formatting, linting and testing."""
    c.run("isort tinypubsub tests")
    c.run("black tinypubsub tests")
    c.run("flake8 tinypubsub tests")
    c.run("mypy tinypubsub tests")
    c.run("pytest tests")
