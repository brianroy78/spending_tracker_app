import importlib
from sys import argv


def run(script_name):
    mod = importlib.import_module(f"scripts.{script_name}")
    runner = getattr(mod, "run")
    runner(*argv[2:])


if __name__ == "__main__":
    run(argv[1])
