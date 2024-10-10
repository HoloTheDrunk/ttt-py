from datetime import datetime as dt

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    @staticmethod
    def log(msg: str):
        with open("log", "a") as file:
            file.write(f'[{dt.now().strftime("%H:%M:%S")}] {msg}\n') 
