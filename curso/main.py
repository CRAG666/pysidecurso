import sys
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QMessageBox
from Ui_trabajadores import Ui_Dialog
from metodos import Metodos
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator, QValidator


class trabajadores (QDialog):
    def __init__(self):
        super(trabajadores, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.Mtos = Metodos()
        self.data = [
            le
            for le in self.findChildren(QLineEdit)
            if le.objectName() != "Le_Buscar"]
        self.current_id = 0
        self.headerUsuarios = self.Mtos.generate_Header_labels('Usuarios')
        self.update_tb()
        self.ui.Btn_Guardar.clicked.connect(self.save)
        self.ui.Btn_Eliminar.clicked.connect(self.delete)
        self.ui.Btn_Editar.clicked.connect(self.edit)
        self.ui.Btn_Actualizar.setEnabled(False)
        self.ui.Btn_Actualizar.clicked.connect(lambda: self.save(True))
        self.ui.Btn_Buscar.clicked.connect(lambda: self.update_tb(self.ui.Le_Buscar.text()))
        only_text = QRegExpValidator(QRegExp('^[A-Za-z]{3,20}'))
        self.ui.Le_Nombre.setValidator(only_text)
        self.ui.Le_Apellidos.setValidator(only_text)
        self.ui.Le_Rol.setValidator(only_text)
        email = QRegExpValidator(QRegExp("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"))
        self.ui.Le_Email.setValidator(email)
        only_numbers = QRegExpValidator(QRegExp('^[0-9]{3,10}'))
        self.ui.Le_Sueldo.setValidator(only_numbers)
        for le in self.data:
            le.textChanged.connect(self.check_changes)
            le.textChanged.emit(le.text())

    def check_changes(self,*args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QValidator.Acceptable:
            color = '#59cf8f'
        else:
            color = '#fe3e23'
        sender.setStyleSheet('QLineEdit{ background-color:'+color+'}')

    def update_tb(self, searchkey=''):
        query = 'select * from Usuarios'
        if searchkey and searchkey != '*':
            query = f"select * from Usuarios where \
            ID like '{searchkey}' or \
            Nombre like '{searchkey}%' or \
            Apellidos like '{searchkey}%'"
        resultado = self.Mtos.run_query(query)
        self.Mtos.print_in_TableWidget(
            self.ui.Tw_Registros,
            self.headerUsuarios,
            resultado)

    def save(self, update=False):
        values = [i.text() for i in self.data]
        if all(values):
            values[4] = int(values[4])
            if update:
                self.Mtos.update_registry("Usuarios", self.current_id, tuple(values))
                self.ui.Btn_Actualizar.setEnabled(False)
                self.ui.Btn_Guardar.setEnabled(True)
            else:
                self.Mtos.add_registry("Usuarios", tuple(values))
            self.update_tb()
            for i in self.data:
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

    def edit(self):
        row, id = self.current_item()
        if id:
            res = QMessageBox.question(self, "Correcto", f'Editar {id} ?')
            if res == 16384:
                for i, le in enumerate(self.data, start=1):
                    le.setText(self.ui.Tw_Registros.item(row, i).text())
                self.current_id = id
                self.ui.Btn_Actualizar.setEnabled(True)
                self.ui.Btn_Guardar.setEnabled(False)
                self.ui.Tw_Registros.removeRow(row)
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
