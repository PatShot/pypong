from src.app import App
from src.view import view

from src.clock import TickingClock

def main():
    main_app = App()
    main_app.on_execute()
    # clk = TickingClock((145, 266))
    # print(clk.get_position())
    # view()

if __name__ == "__main__": main()
    