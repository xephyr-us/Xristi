
import os

from src import RootWindow
from utils import ioutils


CONFIG_NAME = "CONFIG"
CONFIG_PATH = os.path.join(ioutils.get_cwd(), CONFIG_NAME)


def main():
    app = RootWindow(CONFIG_PATH)
    running = True
    while running:
        running = app.launch()


if __name__ == "__main__":
    main()
