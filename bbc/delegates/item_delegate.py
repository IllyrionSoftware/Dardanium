import sys

from constants import COLOR_PICKER_TITLE, UI_ICON_PATH
from handlers.db_handler import DataBaseHandler
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QIcon, QStandardItem
from PySide6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStyledItemDelegate,
    QWidget,
)


class ColorPicker(QColorDialog):
    def __init__(self, color, parent=None):
        """
        Initialize the ColorPicker.
        """
        super().__init__(parent)

        self.setWindowTitle(COLOR_PICKER_TITLE)
        self.setWindowIcon(QIcon(UI_ICON_PATH))

        self.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
        self.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
        self.setCurrentColor(QColor(color))

    def showEvent(self, event):
        super().showEvent(event)
        self.show()


class StandardItemDelegate(QStandardItem):
    def data(self, role=Qt.ItemDataRole.DisplayRole):
        """
        Return the data for the given role.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            return ""

        return super().data(role)


class ItemDelegate(QStyledItemDelegate):
    commitData = Signal(QWidget)

    def __init__(self, table_name, parent=None):
        """
        Initialize the ItemDelegate.
        """
        super().__init__(parent)
        self._db_handler = DataBaseHandler()
        self._table_name = table_name

    def createEditor(self, parent, option, index):
        """
        Create an editor widget for the given index.
        """
        cell_value = index.data(Qt.ItemDataRole.EditRole)

        if index.column() in (0, 1):
            return None

        if index.column() == 2:
            value_in_column_1 = index.sibling(index.row(), 1).data()
            if value_in_column_1 == "Structure":
                editor = QPushButton(parent)
                if cell_value is not None:
                    editor.setText("Select")
                    editor.setStyleSheet("font-style: italic;")
                return editor

            elif value_in_column_1 in (
                "Length",
                "Height",
                "Thickness",
                "Pen thickness",
                "Fill pattern angle",
                "Fill pattern scale",
                "Fill opacity",
            ):
                editor = QDoubleSpinBox(parent)
                max_double_value = sys.float_info.max
                editor.setDecimals(0)
                if value_in_column_1 == "Fill pattern angle":
                    editor.setRange(0, 360)
                    editor.setSuffix(" °")
                    return editor

                elif value_in_column_1 == "Pen thickness":
                    editor.setRange(0, 10)
                    return editor

                elif value_in_column_1 == "Fill pattern scale":
                    editor.setRange(0, 100)
                    return editor

                elif value_in_column_1 == "Fill opacity":
                    editor.setRange(0, 100)
                    editor.setSuffix(" %")
                    return editor
                else:
                    editor.setRange(0, max_double_value)
                    editor.setSuffix(" mm")
                    return editor

            elif value_in_column_1 in ("Area", "Perimeter"):
                editor = QLabel(parent)
                decimals = 0
                if value_in_column_1 == "Area":
                    suffix = " m2"
                    text = "{:.{}f}{}".format(float(cell_value), decimals, suffix)
                    editor.setText(text)
                    return editor

                elif value_in_column_1 == "Perimeter":
                    suffix = " m1"
                    text = "{:.{}f}{}".format(float(cell_value), decimals, suffix)
                    editor.setText(text)
                    return editor

            elif value_in_column_1 in ("Fill color", "Pen color"):
                editor = QPushButton(parent)
                rgb_tuple = tuple(map(int, cell_value.split(",")))
                color = QColor(*rgb_tuple)
                editor.setText(cell_value)
                luminance = (
                    0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()
                ) / 255
                text_color = "black" if luminance > 0.5 else "white"
                editor.setStyleSheet(
                    f"""
                    background-color: {color.name()};
                    border-radius: 1px;
                    border: 1px solid grey;
                    padding: 5px;
                    font-weight: bold;
                    color: {text_color};
                    """
                )
                editor.clicked.connect(lambda: self.open_color_picker(index))
                return editor

            elif value_in_column_1 == "Fill":
                editor = QWidget(parent)
                layout = QHBoxLayout(editor)
                layout.setContentsMargins(0, 0, 0, 0)

                checkbox = QCheckBox()
                checkbox.setChecked(bool(cell_value))
                layout.addWidget(checkbox)
                layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                return editor

            elif value_in_column_1 in ("Pen style", "Fill pattern"):
                editor = QComboBox(parent)
                editor.addItems(cell_value)
                editor.setCurrentIndex(0)
                return editor

            else:
                editor = QLabel(parent)

        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """
        Set the data to be displayed and edited by the editor from the data model.
        """
        if isinstance(editor, QDoubleSpinBox):
            value = index.model().data(index, role=Qt.ItemDataRole.EditRole)
            editor.setValue(float(value))

        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        """
        Set the data to be displayed and edited by the editor from the data model.
        """
        if isinstance(editor, QDoubleSpinBox):
            value = editor.value()
            model.setData(index, value, role=Qt.ItemDataRole.EditRole)
            self.commit_editor_data(index, value, model)

        else:
            super().setModelData(editor, model, index)

    def open_color_picker(self, index, model):
        """
        Open a color picker dialog.
        """
        cell_value = index.data(Qt.ItemDataRole.EditRole)
        color_picker = ColorPicker(cell_value)
        if color_picker.exec() == QColorDialog.Accepted:  # type: ignore
            selected_color = color_picker.currentColor()
            rgb_value = f"{selected_color.red()},{selected_color.green()},{selected_color.blue()}"
            index.model().setData(index, rgb_value, role=Qt.ItemDataRole.EditRole)
            # FIXME:Argument missing for parameter "model"
            self.commit_editor_data(index, rgb_value, model)

    def commit_editor_data(self, index, value, model):
        """
        Commit the data from the editor to the model and update the database.
        """
        row = index.row()
        column_1 = index.sibling(row, 1).data()
        column_0 = index.sibling(row, 0).data()

        model.setData(index, value, role=Qt.ItemDataRole.EditRole)
        self._db_handler.update_data(self._table_name, column_0, column_1, value)
