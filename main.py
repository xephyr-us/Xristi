from src import RootWindow
from utils import ioutils


CONFIG = f"{ioutils.get_cwd()}/CONFIG"


def main():
    app = RootWindow(CONFIG)
    running = True
    while running:
        running = app.launch()


if __name__ == "__main__":
    main()
