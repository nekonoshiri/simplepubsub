import invoke


@invoke.task
def lint(c):
    c.run("isort .")
    c.run("black .")
    c.run("flake8")
    c.run("mypy simplepubsub tests")
    c.run("pydocstyle simplepubsub")


@invoke.task
def test(c):
    c.run("pytest tests")


@invoke.task
def cov(c):
    c.run("pytest --cov=simplepubsub --cov-branch tests")


@invoke.task
def docs(c):
    c.run("sphinx-apidoc -f -o ./docs/autodoc simplepubsub")
    c.run("make -C docs html")
