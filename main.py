from src import RootWindow
import src.events as events


CONFIG = "./CONFIG"


def main():
    events.EventStream()  # Instantiating EventStream singleton
    app = RootWindow(CONFIG)

    running = True
    while running:
        running = app.launch()


if __name__ == "__main__":
    main()
