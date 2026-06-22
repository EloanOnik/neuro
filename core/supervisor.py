

class Supervisor():
    def __init__(self, restart_limit, restart_window):
        restart_limit: int = 3
        restart_window: float = 60.0