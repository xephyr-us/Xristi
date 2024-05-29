
import os

from src import RootWindow
from utils import ioutils


REL_CONFIF_PATH = "./CONFIG"
ABS_CONFIG_PATH = os.path.join(ioutils.get_cwd(), REL_CONFIF_PATH)


def main():
    app = RootWindow(ABS_CONFIG_PATH)
    running = True
    while running:
        running = app.launch()


if __name__ == "__main__":
    main()
