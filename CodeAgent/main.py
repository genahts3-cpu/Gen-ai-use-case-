"""Entry point for the demo application."""
from utils import greet


def main() -> None:
    name = input("Enter your name: ").strip() or "World"
    print(greet(name))


if __name__ == "__main__":
    main()
