import sys
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QMessageBox
from Ui_trabajadores import Ui_Dialog
from metodos import Metodos


class trabajadores (QDialog):
    def __init__(self):
        super(trabajadores, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.Mtos = Metodos()
        self.headerUsuarios = self.Mtos.generate_Header_labels('Usuarios')
        self.update_tb()
        self.ui.Btn_Guardar.clicked.connect(self.save)
        self.ui.Btn_Eliminar.clicked.connect(self.delete)

    def update_tb(self):
        todos_registros = self.Mtos.run_query('select * from Usuarios')
        self.Mtos.print_in_TableWidget(
            self.ui.Tw_Registros,
            self.headerUsuarios,
            todos_registros)

    def save(self):
        data = [le
                for le in self.findChildren(QLineEdit)
                if le.objectName() != "Le_Buscar"]
        values = [i.text() for i in data]
        if all(values):
            values[4] = int(values[4])
            self.Mtos.add_registry("Usuarios", tuple(values))
            self.update_tb()
            for i in data:
                i.clear()
        else:
            print("No se ingresaron todos los datos")

    def delete(self):
        row, id = self.current_item()
        if id:
            res = QMessageBox.question(self, "Correcto", f'Elimina {id} ?')
            if res == 16384:
                self.ui.Tw_Registros.removeRow(row)
                self.Mtos.delete_registry("Usuarios", (id,))
        else:
            QMessageBox.information(self, "No selección", "No selecciono Nada")

    def current_item(self):
        if self.ui.Tw_Registros.selectedItems():
            row = self.ui.Tw_Registros.currentRow()
            id = self.ui.Tw_Registros.item(row, 0).text()
            return row, id
        return -1, False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = trabajadores()
    myapp.show()
    sys.exit(app.exec_())
