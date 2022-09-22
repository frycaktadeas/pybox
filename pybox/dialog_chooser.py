from dialog_darwin import DialogDarwin
import platform


def get_object():
    system = platform.uname().system.lower()
    if system == "darwin":
        return DialogDarwin()

    else:
        raise Exception("Not implemented yet, Linux and Windows support expected in few days")


if __name__ == "__main__":
    get_object()
