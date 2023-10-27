import qdarktheme
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from handlers.events_handler import EventsHandler
from handlers.matrix_handler import MainUIMatrixConfig, MatrixHandler
from interfaces.configs.ui_configs import MainUIConfig
from interfaces.modules.status_bar_module import StatusBarModule
from interfaces.modules.tool_bar_module import ToolBarModule


class MainUIModule(QMainWindow):
    """A class to handle the UI."""

    def __init__(self) -> None:
        """Initialize the MainUI."""
        super().__init__()
        qdarktheme.setup_theme("auto")

        self._main_module_0 = MatrixHandler(MainUIMatrixConfig.Matrix)

        self._events_handler = EventsHandler()

        self.setup_ui()

    def setup_ui(self) -> None:
        """Setup the UIs."""
        self.setup_window()
        self.setStatusBar(StatusBarModule(MainUIConfig.STATUSBAR))
        self.addToolBar(ToolBarModule(MainUIConfig.TOOLBAR))
        self.setup_central_widget()
        self.setup_visibility()
        self._events_handler.quit_on_key_press_event(self)

    def setup_window(self) -> None:
        """Set up the main window properties."""
        self.setWindowTitle(MainUIConfig.TITLE)
        self.setWindowIcon(QIcon(MainUIConfig.ICON))
        self.resize(*MainUIConfig.INIT_SIZE)
        self.setContentsMargins(*MainUIConfig.MARGINS)

    def setup_central_widget(self) -> None:
        """Set up the central widget."""
        self._main_modules_stack = QStackedWidget(self)
        self._main_modules_stack.addWidget(self._main_module_0)
        self.setCentralWidget(self._main_modules_stack)

    def setup_visibility(self) -> None:
        """Set up initial visibility."""
        self.show() if MainUIConfig.INIT_VISIBILITY else self.hide()
