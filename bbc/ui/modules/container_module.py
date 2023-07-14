from PySide6.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class ContainerModule(QWidget):
    def __init__(self, module_layout_type, margins=None, alignment=None, parent=None):
        super().__init__(parent)
        self.setup_module(module_layout_type, margins, alignment)

    def setup_module(self, module_layout_type, margins, alignment):
        layout = self._get_layout(module_layout_type)
        layout.setContentsMargins(*margins) if margins else layout.setContentsMargins(
            0, 0, 0, 0
        )
        layout.setAlignment(alignment) if alignment else None
        self.setLayout(layout)

    def _get_layout(self, module_layout_type):
        layouts = {
            "VBox": QVBoxLayout(),
            "HBox": QHBoxLayout(),
            "Grid": QGridLayout(),
        }
        layout = layouts.get(module_layout_type)
        if layout is None:
            raise ValueError(f"Invalid layout type: {module_layout_type}")
        return layout

    def add_spacer(self):
        layout = self.layout()
        if isinstance(layout, (QVBoxLayout, QHBoxLayout)):
            layout.addStretch()
        elif isinstance(layout, QGridLayout):
            empty_spacer = QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            row = layout.rowCount()
            layout.addItem(empty_spacer, row, 0, 1, layout.columnCount())
        else:
            raise TypeError(
                "Spacer can only be added to QVBoxLayout, QHBoxLayout, QFormLayout, or QGridLayout."
            )

    def add_module(
        self,
        module,
        row=None,
        column=None,
        rowspan=None,
        columnspan=None,
        alignment=None,
    ):
        """
        Add a module to the container.
        """
        layout = self.layout()
        if isinstance(layout, QGridLayout):
            self._add_module_to_grid_layout(
                layout, module, row, column, rowspan, columnspan, alignment
            )

        else:
            layout.addWidget(module)

    def _add_module_to_grid_layout(
        self, layout, module, row, column, rowspan, columnspan, alignment
    ):
        """
        Add a module to a QGridLayout.
        """
        if module is None or row is None or column is None:
            raise ValueError("module, row, and column indices must be specified.")

        if rowspan == "auto":
            rowspan = layout.rowCount()

        if columnspan == "auto":
            columnspan = layout.columnCount()

        if alignment is not None:
            if rowspan is not None and columnspan is not None:
                layout.addWidget(module, row, column, rowspan, columnspan, alignment)
            else:
                layout.addWidget(module, row, column, alignment)
        else:
            if rowspan is not None and columnspan is not None:
                layout.addWidget(module, row, column, rowspan, columnspan)
            else:
                layout.addWidget(module, row, column)
