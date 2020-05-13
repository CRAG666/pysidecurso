        self.ui.Btn_Guardar.clicked.connect(self.Save)

    def Save(self):
        data = [self.ui.Le_Nombre, self.ui.Le_Apellidos, self.ui.Le_Email, self.ui.Le_Rol, self.ui.Le_Sueldo]
        values = [i.text() for i in data]
        if not self.Mtos.isempy(values):
            values[4] = int(values[4])
            self.Mtos.add_registry("Usuarios", tuple(values))
        for d in data:
            d.clear()
        self.Mtos.print_in_TableWidget(self.ui.Tw_Registros,self.Mtos.generate_Header_labels("Usuarios"),self.Mtos.run_query('select * from Usuarios'))