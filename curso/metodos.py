from PySide2.QtWidgets import QTableWidgetItem
from sqlite3 import connect


class Metodos():
    def __init__(self):
        super(Metodos, self).__init__()
        self.db_name = 'trabajadores.db'

    def run_query(self, query, parameter=()):
        try:
            with connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query, parameter)
                result = cursor.fetchall()
                conn.commit()
            return result
        except IndexError as e:
            print(e)
        finally:
            conn.close()

    def print_in_TableWidget(self, tablewidget: object, headerlabels: list, result: list):
        tablewidget.setColumnCount(len(headerlabels))
        tablewidget.setRowCount(len(result))
        tablewidget.setHorizontalHeaderLabels(headerlabels)
        for row in range(len(result)):
            for column in range(len(result[0])):
                tablewidget.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(result[row][column]))
                )

    def generate_Header_labels(self, table: str,) -> list:
        labels = self.run_query(
            'select name from pragma_table_info(?)',
            (table,)
        )
        return [i[0] for i in labels]

    def add_registry(self, tableName: str, values: tuple):
        count_values = ',?' * len(values)
        self.run_query(f'insert into {tableName} values(null{count_values})', values)

    def delete_registry(self, tableName: str, values: tuple):
        query = f'delete from {tableName} where id=?'
        self.run_query(query, values)

    def update_registry(self, tableName: str, id: int, values: tuple):
        fields = "=?, ".join([i for i in self.generate_Header_labels(tableName) if i != 'ID'])
        query = f'update {tableName} set {fields}=? where id={id}'
        self.run_query(query, values)
