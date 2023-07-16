import click
from pykinect_recorder.main_window import MainWindow
import qdarktheme
from PySide6.QtWidgets import QApplication


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


# @click.command(help="pykinect")
# @click.option("--open", is_flag=True)
# def check(open):
#     if open:
#         # run()


def main():
    app = QApplication()
    qdarktheme.setup_theme()
    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    main()
