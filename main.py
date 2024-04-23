from src import RootWindow


CONFIG = "CONFIG"


def main():
    app = RootWindow()
    running = True
    while running:
        running = app.launch()


if __name__ == "__main__":
    main()
