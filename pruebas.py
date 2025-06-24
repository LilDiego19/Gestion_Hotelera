import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ruta_fondo_inicio = os.path.join(BASE_DIR, "imagenes", "fondo_inicio.png")
ruta_fondo = os.path.join(BASE_DIR, "imagenes", "fondo.png")
ruta_logo = os.path.join(BASE_DIR, "imagenes", "Logo.png")
ruta_logo2 = os.path.join(BASE_DIR, "imagenes", "logo 2.png")
ruta_logo3 = os.path.join(BASE_DIR, "imagenes", "logo 3.png")

class VentanaInicio:
    """
    Clase que representa la ventana de inicio de la aplicación.
    Muestra una interfaz visual con fondo personalizado, título y botones para iniciar o salir.
    """

    def __init__(self, master, continuar_callback):
        """
        Inicializa la ventana de inicio.

        Parámetros:
        - master: ventana raíz de Tkinter.
        - continuar_callback: función que se ejecuta al pulsar 'Iniciar', normalmente lanza la ventana principal.
        """
        self.master = master
        self.master.title("Gestión Hotelera - Inicio")
        self.master.geometry("800x500")
        self.master.resizable(False, False)

        # Fondo con imagen
        fondo_img = Image.open(ruta_fondo_inicio)
        fondo_img = fondo_img.resize((800, 500), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(fondo_img)
        fondo = Label(self.master, image=self.bg_photo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # Cuadro centrado con botones
        contenedor = Frame(self.master, bg="white", bd=0)
        contenedor.place(relx=0.5, rely=0.5, anchor="center", width=360, height=230)
        contenedor.config(highlightbackground="gray", highlightthickness=1)

        Label(contenedor, text="Gestión Hotelera", font=("Helvetica", 24, "bold"),
              bg="white", fg="#222", justify="center").pack(pady=(20, 10))

        Button(contenedor, text="Iniciar", font=("Helvetica", 14, "bold"), bg="#4CAF50",
               fg="white", width=20, height=2, relief="flat", command=self.iniciar).pack(pady=(0, 10))

        Button(contenedor, text="Salir", font=("Helvetica", 14, "bold"), bg="#f44336",
               fg="white", width=20, height=2, relief="flat", command=self.salir).pack()

        self.continuar_callback = continuar_callback

    def iniciar(self):
        """Cierra esta ventana e inicia la aplicación principal."""
        self.master.destroy()
        self.continuar_callback()

    def salir(self):
        """Pregunta al usuario si quiere salir y cierra la aplicación si confirma."""
        if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
            self.master.destroy()


class HotelManagementSystem:
    """
    Clase principal de la aplicación que representa la interfaz del sistema de gestión hotelera.
    Muestra el menú lateral con opciones como Cliente, Habitación, Incidencias y Salir,
    así como un área principal que se actualiza según la sección seleccionada.
    """

    def __init__(self, root):
        """
        Constructor que inicializa la ventana principal del sistema.

        Parámetros:
        - root: la ventana raíz de Tkinter (instancia de Tk).
        """
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1550x800+0+0")

        # Imagen superior como fondo
        img1 = Image.open(ruta_fondo)
        img1 = img1.resize((1550, 140), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1, bd=4, relief=RIDGE).place(x=0, y=0, width=1550, height=140)

        # Logo a la izquierda
        img2 = Image.open(ruta_logo)
        img2 = img2.resize((230, 140), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2, bd=4, relief=RIDGE).place(x=0, y=0, width=230, height=140)

        # Título principal
        Label(self.root, text="HOTEL MANAGEMENT SYSTEM", font=("times new roman", 40, "bold"),
              bg="black", fg="gold", bd=4, relief=RIDGE).place(x=0, y=140, width=1550, height=50)

        # Marco principal donde se organizarán los botones y el contenido dinámico
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=190, width=1550, height=620)

        # Etiqueta de menú lateral
        Label(main_frame, text="MENU", font=("times new roman", 20, "bold"), bg="black", fg="gold",
              bd=4, relief=RIDGE).place(x=0, y=0, width=230)

        # Marco para los botones del menú
        btn_frame = Frame(main_frame, bd=4, relief=RIDGE)
        btn_frame.place(x=0, y=35, width=228, height=190)

        # Botón para acceder a la gestión de clientes
        Button(btn_frame, text="CLIENTE", command=self.cust_details, width=22,
               font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0).grid(row=0, column=0, pady=1)

        # Botón para acceder a la gestión de habitaciones
        Button(btn_frame, text="HABITACIÓN", command=self.room_details, width=22,
               font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0).grid(row=1, column=0, pady=1)

        # Botón para acceder a la gestión de incidencias
        Button(btn_frame, text="INCIDENCIAS", command=self.incidencias_view, width=22,
               font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0).grid(row=3, column=0, pady=1)

        # Botón para salir de la aplicación
        Button(btn_frame, text="SALIR", command=self.root.quit, width=22,
               font=("times new roman", 14, "bold"), bg="black", fg="gold", bd=0).grid(row=4, column=0, pady=1)

        # Área a la derecha que se actualizará dinámicamente
        self.right_frame = Frame(main_frame, bd=4, relief=RIDGE)
        self.right_frame.place(x=225, y=0, width=1310, height=590)

        # Logo decorativo inferior 1
        img_logo2 = Image.open(ruta_logo2)
        img_logo2 = img_logo2.resize((230, 210), Image.Resampling.LANCZOS)
        self.photoimg_logo2 = ImageTk.PhotoImage(img_logo2)
        Label(main_frame, image=self.photoimg_logo2, bd=4, relief=RIDGE).place(x=0, y=225, width=230, height=210)

        # Logo decorativo inferior 2
        img_logo3 = Image.open(ruta_logo3)
        img_logo3 = img_logo3.resize((230, 190), Image.Resampling.LANCZOS)
        self.photoimg_logo3 = ImageTk.PhotoImage(img_logo3)
        Label(main_frame, image=self.photoimg_logo3, bd=4, relief=RIDGE).place(x=0, y=420, width=230, height=190)

    def cust_details(self):
        """
        Carga la interfaz de gestión de clientes en el área derecha.
        """
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.app = Cust_Win(self.right_frame)

    def room_details(self):
        """
        Carga la interfaz de gestión de reservas de habitación en el área derecha.
        """
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.app = Roombooking(self.right_frame)

    def incidencias_view(self):
        """
        Carga la interfaz de gestión de incidencias en el área derecha.
        """
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        self.app = Incidencias(self.right_frame)



class Cust_Win:
    """
    Clase para la gestión de clientes en la aplicación de gestión hotelera.
    Permite añadir, actualizar, eliminar, buscar y visualizar registros de clientes,
    utilizando una base de datos SQLite y una interfaz Tkinter.
    """

    def __init__(self, parent_frame):
        """
        Inicializa la interfaz de cliente y conecta la base de datos.

        Parámetros:
        - parent_frame: Frame de Tkinter donde se dibuja esta vista.
        """
        self.root = parent_frame
        self.conectar_bd()
        self.crear_tabla()

        # Título de la sección
        Label(self.root, text="Añadir datos del cliente", font=("times new roman", 18, "bold"),
              bg="black", fg="gold").place(x=0, y=0, width=1295, height=50)

        # Marco para los campos de entrada
        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Datos del Cliente",
                                    font=("Arial", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=60, width=550, height=500)

        # Lista de campos a crear
        fields = [
            ("Ref cliente", ttk.Entry),
            ("Nombre cliente", ttk.Entry),
            ("Género", ttk.Combobox),
            ("Código Postal", ttk.Entry),
            ("Móvil", ttk.Entry),
            ("Email", ttk.Entry),
            ("Nacionalidad", ttk.Entry),
            ("Tipo de Documento", ttk.Combobox),
            ("Número de Documento", ttk.Entry),
            ("Dirección", ttk.Entry)
        ]

        self.campos = {}
        for idx, (label_text, widget_type) in enumerate(fields):
            Label(labelframeleft, text=label_text, font=("Arial", 12, "bold"), padx=2, pady=6).grid(row=idx, column=0, sticky="w")
            if widget_type == ttk.Combobox:
                widget = widget_type(labelframeleft, font=("Arial", 13, "bold"), width=27, state="readonly")
                widget["values"] = ("DNI", "Pasaporte", "NIE") if "Documento" in label_text else ("Masculino", "Femenino", "Otro")
                widget.current(0)
            else:
                widget = widget_type(labelframeleft, font=("Arial", 13, "bold"), width=29)
            widget.grid(row=idx, column=1)
            self.campos[label_text] = widget

        # Botones de acción
        btn_frame = Frame(labelframeleft, bg="black")
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        Button(btn_frame, text="AÑADIR", font=("Arial", 13), bg="black", fg="gold", width=12, command=self.insertar_cliente).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="ACTUALIZAR", font=("Arial", 13), bg="black", fg="gold", width=12, command=self.actualizar_cliente).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="BORRAR", font=("Arial", 13), bg="black", fg="gold", width=12, command=self.borrar_cliente).grid(row=0, column=2, padx=5)
        Button(btn_frame, text="RESET", font=("Arial", 13), bg="black", fg="gold", width=12, command=self.reset_campos).grid(row=0, column=3, padx=5)

        self.crear_interfaz_tabla()
        self.mostrar_todos()

    def crear_interfaz_tabla(self):
        """
        Crea la tabla de visualización de clientes y los controles de búsqueda.
        """
        Table_Frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="Ver detalles y sistema de búsqueda",
                                 font=("arial", 12, "bold"))
        Table_Frame.place(x=580, y=60, width=700, height=500)

        # Controles de búsqueda
        Label(Table_Frame, font=("arial", 12, "bold"), text="Buscar por:", bg="red", fg="white").grid(row=0, column=0, sticky=W, padx=2)
        self.combo_Search = ttk.Combobox(Table_Frame, font=("arial", 12, "bold"), width=24, state="readonly")
        self.combo_Search["value"] = ("movil", "ref")
        self.combo_Search.current(0)
        self.combo_Search.grid(row=0, column=1, padx=2)
        self.txtSearch = ttk.Entry(Table_Frame, font=("arial", 13, "bold"), width=20)
        self.txtSearch.grid(row=0, column=2, padx=2)

        Button(Table_Frame, text="Buscar", font=("arial", 11, "bold"), bg="black", fg="gold", width=8, command=self.buscar_cliente).grid(row=0, column=3, padx=1)
        Button(Table_Frame, text="Mostrar", font=("arial", 11, "bold"), bg="black", fg="gold", width=8, command=self.mostrar_todos).grid(row=0, column=4, padx=1)

        # Tabla de resultados
        details_table = Frame(Table_Frame, bd=2, relief=RIDGE)
        details_table.place(x=0, y=40, width=650, height=400)

        scroll_x = ttk.Scrollbar(details_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_table, orient=VERTICAL)

        self.Cust_Details_Table = ttk.Treeview(
            details_table,
            columns=("ref", "nombre", "genero", "cod_postal", "movil", "email", "nacionalidad", "tipo_doc", "num_doc", "direccion"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Cust_Details_Table.xview)
        scroll_y.config(command=self.Cust_Details_Table.yview)
        self.Cust_Details_Table.pack(fill=BOTH, expand=1)

        # Configura cabeceras y anchos de columna
        headers = {
            "ref": "Referencia",
            "nombre": "Nombre",
            "genero": "Género",
            "cod_postal": "Código postal",
            "movil": "Móvil",
            "email": "Correo electrónico",
            "nacionalidad": "Nacionalidad",
            "tipo_doc": "Tipo de documento",
            "num_doc": "Nº documento",
            "direccion": "Dirección"
        }
        for col, texto in headers.items():
            self.Cust_Details_Table.heading(col, text=texto)
            self.Cust_Details_Table.column(col, width=120)

        self.Cust_Details_Table["show"] = "headings"
        self.Cust_Details_Table.bind("<Double-1>", self.seleccionar_fila)

    def seleccionar_fila(self, event):
        """
        Carga los datos de una fila seleccionada en los campos del formulario.
        """
        item = self.Cust_Details_Table.focus()
        valores = self.Cust_Details_Table.item(item, "values")
        if valores:
            for (clave, campo), valor in zip(self.campos.items(), valores):
                if isinstance(campo, ttk.Combobox):
                    campo.set(valor)
                else:
                    campo.delete(0, END)
                    campo.insert(0, valor)

    def buscar_cliente(self):
        """
        Busca clientes en la base de datos según el campo seleccionado y el texto introducido.
        """
        campo = self.combo_Search.get()
        valor = self.txtSearch.get()
        self.cursor.execute(f"SELECT * FROM clientes WHERE {campo} LIKE ?", (f"%{valor}%",))
        filas = self.cursor.fetchall()
        self.Cust_Details_Table.delete(*self.Cust_Details_Table.get_children())
        for fila in filas:
            self.Cust_Details_Table.insert("", END, values=fila)

    def mostrar_todos(self):
        """
        Muestra todos los registros de clientes existentes en la tabla.
        """
        self.cursor.execute("SELECT * FROM clientes")
        filas = self.cursor.fetchall()
        self.Cust_Details_Table.delete(*self.Cust_Details_Table.get_children())
        for fila in filas:
            self.Cust_Details_Table.insert("", END, values=fila)

    def conectar_bd(self):
        """
        Establece la conexión con la base de datos SQLite.
        """
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor()

    def crear_tabla(self):
        """
        Crea la tabla de clientes si no existe en la base de datos.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                ref TEXT PRIMARY KEY,
                nombre TEXT,
                genero TEXT,
                cod_postal TEXT,
                movil TEXT,
                email TEXT,
                nacionalidad TEXT,
                tipo_doc TEXT,
                num_doc TEXT,
                direccion TEXT
            )
        """)
        self.conn.commit()

    def insertar_cliente(self):
        """
        Inserta un nuevo cliente en la base de datos tras validar todos los campos.
        """
        datos = [campo.get() for campo in self.campos.values()]
        email = datos[5].strip()
        movil = datos[4]
        tipo_doc = self.campos["Tipo de Documento"].get()
        num_doc = datos[8]

        import re

        # Validaciones
        patron_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(patron_email, email):
            messagebox.showerror("Error", "Correo electrónico no válido")
            return

        if not movil.isdigit() or not (9 <= len(movil) <= 15):
            messagebox.showerror("Error", "Número de móvil no válido")
            return

        if tipo_doc == "DNI" and not re.match(r"^\d{8}[A-Z]$", num_doc):
            messagebox.showerror("Error", "DNI no válido")
            return

        if tipo_doc in ("Pasaporte", "NIE") and not re.match(r"^[A-Z]\d{7}[A-Z]$", num_doc):
            messagebox.showerror("Error", f"{tipo_doc} no válido")
            return

        if not datos[0]:
            messagebox.showerror("Error", "Referencia obligatoria")
            return

        try:
            self.cursor.execute("INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", datos)
            self.conn.commit()
            messagebox.showinfo("Éxito", "Cliente añadido correctamente")
            self.mostrar_todos()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Aviso", "El cliente ya existe")

    def actualizar_cliente(self):
        """
        Actualiza los datos de un cliente existente en la base de datos.
        """
        ref = self.campos["Ref cliente"].get()
        if not ref:
            messagebox.showerror("Error", "Referencia obligatoria para actualizar")
            return

        self.cursor.execute("SELECT * FROM clientes WHERE ref = ?", (ref,))
        if not self.cursor.fetchone():
            messagebox.showwarning("Aviso", "Cliente no encontrado")
            return

        datos = [campo.get() for campo in self.campos.values()][1:] + [ref]
        self.cursor.execute("""
            UPDATE clientes SET
                nombre=?, genero=?, cod_postal=?, movil=?, email=?, nacionalidad=?,
                tipo_doc=?, num_doc=?, direccion=?
            WHERE ref=?
        """, datos)
        self.conn.commit()
        messagebox.showinfo("Actualizado", "Datos actualizados correctamente")
        self.mostrar_todos()

    def borrar_cliente(self):
        """
        Elimina un cliente de la base de datos tras confirmación del usuario.
        """
        ref = self.campos["Ref cliente"].get()
        if not ref:
            messagebox.showerror("Error", "Referencia obligatoria para borrar")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres borrar este cliente?"):
            self.cursor.execute("DELETE FROM clientes WHERE ref = ?", (ref,))
            self.conn.commit()
            messagebox.showinfo("Borrado", "Cliente eliminado correctamente")
            self.reset_campos()
            self.mostrar_todos()

    def reset_campos(self):
        """
        Limpia todos los campos del formulario.
        """
        for campo in self.campos.values():
            if isinstance(campo, ttk.Combobox):
                campo.current(0)
            else:
                campo.delete(0, END)


class Roombooking:
    def __init__(self, root):
        self.root = root
        self.conectar_bd()
        self.crear_tabla()

        lbl_title = Label(self.root, text="DETALLES DE RESERVA DE HABITACIÓN",
                          font=("times new roman", 18, "bold"), bg="black", fg="gold")
        lbl_title.place(x=0, y=0, width=1295, height=50)

        labelframeleft = LabelFrame(self.root, bd=2, relief=RIDGE, text="Datos de la Reserva",
                                    font=("arial", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=50, width=535, height=520)

        # Campos
        self.datos = {}
        labels = [
            ("Contacto del Cliente", "entry"),
            ("Nº de Personas", "entry"),
            ("Fecha de Entrada", "date"),
            ("Fecha de Salida", "date"),
            ("Habitación", "combo", ["Estándar", "Familiar", "Suite"]),
            ("Comida", "combo", ["Desayuno", "Media pensión", "Pensión completa"]),
            ("Nº de Días", "entry"),
            ("Impuesto Pagado", "entry"),
            ("Subtotal", "entry"),
            ("Costo Total", "entry"),
            ("Ver Habitaciones", "button")
        ]



        for idx, (label, tipo, *extra) in enumerate(labels):
            Label(labelframeleft, text=label + ":", font=("arial", 11, "bold")).grid(row=idx, column=0, sticky=W,
                                                                                     padx=5, pady=5)

            if tipo == "entry":
                entry = Entry(labelframeleft, width=25, font=("arial", 11))
            elif tipo == "combo":
                entry = ttk.Combobox(labelframeleft, values=extra[0], state="readonly", font=("arial", 11), width=23)
                entry.current(0)
            elif tipo == "date":
                entry = DateEntry(labelframeleft, width=22, font=("arial", 11), date_pattern='dd-mm-yyyy',
                                  showweeknumbers=False)
                entry.bind("<<DateEntrySelected>>", lambda e: self.calcular_dias())
            elif tipo == "button":
                entry = Button(labelframeleft, text="Ver Habitaciones", font=("arial", 10, "bold"),
                               bg="black", fg="gold", width=22, command=self.mostrar_plano_habitaciones)
            else:
                entry = Entry(labelframeleft, width=25, font=("arial", 11))

            entry.grid(row=idx, column=1, padx=5)

            if tipo != "button":
                self.datos[label] = entry

        # ✅ Ahora sí puedes asociar eventos, porque self.datos ya existe:
        self.datos["Habitación"].bind("<<ComboboxSelected>>", lambda e: self.calcular_precio_total())
        self.datos["Comida"].bind("<<ComboboxSelected>>", lambda e: self.calcular_precio_total())
        self.datos["Nº de Personas"].bind("<FocusOut>", lambda e: self.calcular_precio_total())

        # Botón buscar
        Button(labelframeleft, text="Buscar", font=("arial", 10, "bold"), bg="black", fg="gold", width=8,
               command=self.buscar_datos_cliente).grid(row=0, column=2, padx=0)

        # Botones CRUD
        botones = [
            ("Añadir", self.insertar_reserva),
            ("Actualizar", self.actualizar_reserva),
            ("Eliminar", self.eliminar_reserva),
            ("Reset", self.reset_campos)
        ]

        # Boton FACTURA
        Button(labelframeleft, text="FACTURA", font=("arial", 11, "bold"), bg="darkgreen", fg="white", width=10,
               command=self.generar_factura_pdf).place(x=410,y = 460)

        for i, (texto, cmd) in enumerate(botones):
            Button(labelframeleft, text=texto, font=("arial", 11, "bold"), bg="black", fg="gold", width=10,
                   command=cmd).place(x=10 + i * 100, y=460)

        # Tabla a la derecha
        frame_tabla = Frame(self.root, bd=2, relief=RIDGE)
        frame_tabla.place(x=560, y=150, width=720, height=405)

        scroll_x = Scrollbar(frame_tabla, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame_tabla, orient=VERTICAL)

        self.reserva_tabla = ttk.Treeview(frame_tabla,
                                          columns=("contacto", "personas", "checkin", "checkout", "habitacion",
                                                   "comida", "dias", "impuesto", "subtotal", "total"),

                                          xscrollcommand=scroll_x.set,
                                          yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.reserva_tabla.xview)
        scroll_y.config(command=self.reserva_tabla.yview)
        self.reserva_tabla.pack(fill=BOTH, expand=1)

        for col in self.reserva_tabla["columns"]:
            self.reserva_tabla.heading(col, text=col.capitalize())
            self.reserva_tabla.column(col, width=100)

        self.reserva_tabla["show"] = "headings"
        self.reserva_tabla.bind("<Double-1>", self.seleccionar_fila)

        self.mostrar_reservas()

    def conectar_bd(self):
        self.conn = sqlite3.connect("reservas.db")
        self.cursor = self.conn.cursor()



    def crear_tabla(self):
        #self.cursor.execute("DROP TABLE IF EXISTS reservas")  # <-- Elimina la tabla si existe

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                contacto TEXT PRIMARY KEY,
                personas TEXT,
                checkin TEXT,
                checkout TEXT,
                habitacion TEXT,
                comida TEXT,
                dias TEXT,
                impuesto TEXT,
                subtotal TEXT,
                total TEXT
            )
        """)
        self.conn.commit()

    def on_fecha_cambiada(self, event=None):
        self.calcular_dias()

    def validar_fechas(self):
        try:
            entrada = self.datos["Fecha de Entrada"].get_date()
            salida = self.datos["Fecha de Salida"].get_date()
            if entrada > salida:
                messagebox.showerror("Error", "La fecha de entrada debe ser anterior o igual a la de salida.")
                return False
        except Exception as e:
            messagebox.showerror("Error de fecha", f"Ocurrió un error al validar fechas: {e}")
            return False
        return True

    def insertar_reserva(self):
        if not self.validar_fechas():
            return

        orden_campos = [
            "Contacto del Cliente",
            "Nº de Personas",
            "Fecha de Entrada",
            "Fecha de Salida",
            "Habitación",
            "Comida",
            "Nº de Días",
            "Impuesto Pagado",
            "Subtotal",
            "Costo Total"
        ]

        try:
            contacto = self.datos["Contacto del Cliente"].get().strip()
            if not contacto:
                messagebox.showerror("Error", "El contacto del cliente es obligatorio.")
                return

            habitacion_id = self.datos["Habitación"].get().strip()
            if not habitacion_id or not habitacion_id.split()[0].isdigit():
                messagebox.showerror("Error", "Selecciona una habitación válida desde el plano.")
                return

            # ✅ Formato de fechas correcto para SQLite
            entrada_date = self.datos["Fecha de Entrada"].get_date()
            salida_date = self.datos["Fecha de Salida"].get_date()
            entrada = entrada_date.strftime("%Y-%m-%d")
            salida = salida_date.strftime("%Y-%m-%d")

            # ✅ Verificar solapamientos
            self.cursor.execute("""
                SELECT * FROM reservas
                WHERE habitacion = ?
                AND (
                    date(checkin) <= ? AND date(checkout) >= ?
                )
            """, (habitacion_id, salida, entrada))

            if self.cursor.fetchone():
                messagebox.showerror("Error", f"❌ La habitación '{habitacion_id}' ya está reservada entre esas fechas.")
                return

            # Obtener el resto de campos
            datos = [
                contacto,
                self.datos["Nº de Personas"].get(),
                entrada,  # usamos fecha en formato YYYY-MM-DD
                salida,
                habitacion_id,
                self.datos["Comida"].get(),
                self.datos["Nº de Días"].get(),
                self.datos["Impuesto Pagado"].get(),
                self.datos["Subtotal"].get(),
                self.datos["Costo Total"].get()
            ]

            self.cursor.execute("""
                INSERT INTO reservas
                (contacto, personas, checkin, checkout, habitacion, comida, dias, impuesto, subtotal, total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, datos)

            self.conn.commit()
            self.mostrar_reservas()
            messagebox.showinfo("Éxito", "✅ Reserva guardada correctamente.")

        except sqlite3.IntegrityError:
            messagebox.showwarning("Duplicado", "Ya existe una reserva con ese contacto.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo insertar la reserva:\n{e}")

    def mostrar_reservas(self):
        self.cursor.execute("SELECT * FROM reservas")
        filas = self.cursor.fetchall()
        self.reserva_tabla.delete(*self.reserva_tabla.get_children())
        for fila in filas:
            self.reserva_tabla.insert("", END, values=fila)

    def seleccionar_fila(self, event):
        item = self.reserva_tabla.focus()
        valores = self.reserva_tabla.item(item, "values")

        campos_ordenados = [
            "Contacto del Cliente",
            "Nº de Personas",
            "Fecha de Entrada",
            "Fecha de Salida",
            "Habitación",
            "Comida",
            "Nº de Días",
            "Impuesto Pagado",
            "Subtotal",
            "Costo Total"
        ]

        if valores and len(valores) == len(campos_ordenados):
            for campo, valor in zip(campos_ordenados, valores):
                widget = self.datos.get(campo)
                if widget:
                    if isinstance(widget, DateEntry):
                        try:
                            fecha_dt = datetime.strptime(valor, "%d-%m-%Y").date()
                            widget.set_date(fecha_dt)
                        except Exception as e:
                            messagebox.showwarning("Advertencia", f"No se pudo cargar la fecha {valor}")
                    elif isinstance(widget, ttk.Combobox):
                        widget.set(valor)
                    else:
                        widget.delete(0, END)
                        widget.insert(0, valor)

    def actualizar_reserva(self):
        orden_campos = [
            "Contacto del Cliente",
            "Nº de Personas",
            "Fecha de Entrada",
            "Fecha de Salida",
            "Habitación",
            "Comida",
            "Nº de Días",
            "Impuesto Pagado",
            "Subtotal",
            "Costo Total"
        ]

        try:
            datos = [self.datos[campo].get() for campo in orden_campos]
        except KeyError as e:
            messagebox.showerror("Error", f"Falta el campo: {e}")
            return

        contacto = datos[0]

        self.cursor.execute("SELECT * FROM reservas WHERE contacto = ?", (contacto,))
        if not self.cursor.fetchone():
            messagebox.showerror("Error", "Reserva no encontrada.")
            return

        try:
            self.cursor.execute("""
                UPDATE reservas SET
                    personas=?, checkin=?, checkout=?, habitacion=?, comida=?, dias=?, impuesto=?, subtotal=?, total=?
                WHERE contacto=?
            """, datos[1:] + [contacto])

            self.conn.commit()
            self.mostrar_reservas()
            messagebox.showinfo("Éxito", "Reserva actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la reserva:\n{e}")

    def eliminar_reserva(self):
        contacto = self.datos["Contacto del Cliente"].get()
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar esta reserva?"):
            self.cursor.execute("DELETE FROM reservas WHERE contacto=?", (contacto,))
            self.conn.commit()
            self.mostrar_reservas()
            self.reset_campos()

    def reset_campos(self):
        for key, campo in self.datos.items():
            if isinstance(campo, DateEntry):
                campo.set_date(datetime.today().date())
            elif isinstance(campo, ttk.Combobox):
                campo.current(0)
            else:
                campo.delete(0, END)

    def buscar_datos_cliente(self):
        contacto = self.datos["Contacto del Cliente"].get()

        if not contacto:
            messagebox.showwarning("Aviso", "Por favor, introduce un número de contacto.")
            return

        try:
            conn = sqlite3.connect("clientes.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE movil=?", (contacto,))
            cliente = cursor.fetchone()
            conn.close()

            if cliente:
                messagebox.showinfo("Cliente encontrado", "✅ Cliente correcto.")
            else:
                if messagebox.askyesno("Cliente no encontrado",
                                       "❌ Cliente no registrado. ¿Deseas ir a la pestaña de clientes para añadirlo?"):
                    self.root.event_generate("<<CambiarAPestanaClientes>>")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo acceder a los datos del cliente: {e}")

    def calcular_dias(self):
        try:
            entrada = self.datos["Fecha de Entrada"].get_date()
            salida = self.datos["Fecha de Salida"].get_date()
            dias = (salida - entrada).days
            if dias < 0:
                dias = 0
            self.datos["Nº de Días"].delete(0, END)
            self.datos["Nº de Días"].insert(0, str(dias))
            self.calcular_precio_total()
        except Exception as e:
            print("Error al calcular días:", e)

    def mostrar_plano_habitaciones(self):
        ventana = Toplevel(self.root)
        ventana.title("Plano de Habitaciones")
        ventana.geometry("750x550")  # un poco más grande

        try:
            entrada = self.datos["Fecha de Entrada"].get_date().strftime("%Y-%m-%d")
            salida = self.datos["Fecha de Salida"].get_date().strftime("%Y-%m-%d")
        except Exception:
            messagebox.showerror("Error", "Selecciona fechas válidas antes de ver habitaciones.")
            ventana.destroy()
            return

        frame_canvas = Frame(ventana)
        frame_canvas.pack(fill=BOTH, expand=1)

        canvas = Canvas(frame_canvas, bg="white")
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = Scrollbar(frame_canvas, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Frame para el contenido, dentro del canvas
        contenido = Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=contenido, anchor="nw")

        # Ahora añade las habitaciones como antes, pero en el Frame contenido
        for planta in range(3):  # Planta 1 = 100, Planta 2 = 200, etc.
            Label(contenido, text=f"Planta {planta + 1}", font=("arial", 11, "bold"), bg="white").grid(row=planta * 5,
                                                                                                       column=0, pady=5)
            for i in range(10):  # Habitaciones por planta
                numero = (planta + 1) * 100 + i + 1
                tipo = self.obtener_tipo_habitacion(i + 1)
                habitacion_id = f"{numero} {tipo}"
                disponible = self.habitacion_disponible(habitacion_id, entrada, salida)
                color = "green" if disponible else "red"

                btn = Button(
                    contenido,
                    text=habitacion_id,
                    bg=color,
                    width=10,
                    height=3,
                    command=lambda t=habitacion_id: self.datos["Habitación"].set(t),
                    state=NORMAL if disponible else DISABLED
                )
                # Ajusta la posición de la cuadrícula según tus necesidades
                btn.grid(row=planta * 5 + (i // 5) + 1, column=i % 5 + 1, padx=5, pady=5)


        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def obtener_tipo_habitacion(self, numero):
        # 5 estándar (1-5), 4 familiar (6-9), 1 suite (10) por planta
        pos = (numero - 1) % 10
        if pos < 5:
            return "Estándar"
        elif pos < 9:
            return "Familiar"
        else:
            return "Suite"

    def habitacion_disponible(self, habitacion_id, entrada, salida):
        try:
            self.cursor.execute("""
                SELECT 1 FROM reservas 
                WHERE habitacion = ? 
                AND (
                    date(checkin) <= date(?) AND date(checkout) >= date(?)
                )
            """, (habitacion_id, salida, entrada))
            resultado = self.cursor.fetchone()
            return resultado is None  # Si no hay reservas, está libre
        except Exception as e:
            print("Error al comprobar disponibilidad:", e)
            return False

    def calcular_precio_total(self):
        try:
            dias_str = self.datos["Nº de Días"].get()
            personas_str = self.datos["Nº de Personas"].get()

            if not dias_str.isdigit() or not personas_str.isdigit():
                return  # Campos vacíos o inválidos

            dias = int(dias_str)
            personas = int(personas_str)

            precios_habitacion = {
                "Estándar": 80,
                "Familiar": 120,
                "Suite": 180
            }

            precios_comida = {
                "Desayuno": 8,
                "Media pensión": 18,
                "Pensión completa": 30
            }

            habitacion = self.datos["Habitación"].get()
            comida = self.datos["Comida"].get()

            # ✅ Extrae solo el tipo: "Estándar" desde "101 Estándar"
            tipo_habitacion = habitacion.split()[-1]
            precio_habitacion = precios_habitacion.get(tipo_habitacion, 0)
            precios_comida = precios_comida.get(comida, 0)

            subtotal = (precio_habitacion * dias) + (precios_comida * personas * dias)

            impuesto = subtotal * 0.10
            total = subtotal + impuesto

            self.datos["Subtotal"].delete(0, END)
            self.datos["Subtotal"].insert(0, f"{subtotal:.2f}")

            self.datos["Impuesto Pagado"].delete(0, END)
            self.datos["Impuesto Pagado"].insert(0, f"{impuesto:.2f}")

            self.datos["Costo Total"].delete(0, END)
            self.datos["Costo Total"].insert(0, f"{total:.2f}")

        except Exception as e:
            print("Error al calcular precio total:", e)
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    import os

    def generar_factura_pdf(self):
        contacto = self.datos["Contacto del Cliente"].get()

        if not contacto:
            messagebox.showwarning("Advertencia", "Debes introducir el contacto del cliente.")
            return

        self.cursor.execute("SELECT * FROM reservas WHERE contacto=?", (contacto,))
        reserva = self.cursor.fetchone()

        if not reserva:
            messagebox.showerror("Error", "No se encontró ninguna reserva con ese contacto.")
            return

        # Desempaquetar los datos
        contacto, personas, checkin, checkout, habitacion, comida, dias, impuesto, subtotal, total = reserva

        nombre_archivo = f"factura_{contacto}.pdf"
        c = canvas.Canvas(nombre_archivo, pagesize=A4)
        width, height = A4

        c.setTitle("Factura de Reserva")
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "FACTURA DE RESERVA - HOTEL")

        c.setFont("Helvetica", 12)
        lineas = [
            f"Contacto del Cliente: {contacto}",
            f"Nº de Personas: {personas}",
            f"Fecha de Entrada: {checkin}",
            f"Fecha de Salida: {checkout}",
            f"Habitación: {habitacion}",
            f"Régimen de Comida: {comida}",
            f"Nº de Días: {dias}",
            f"Subtotal: {subtotal} €",
            f"Impuesto: {impuesto} €",
            f"Total: {total} €"
        ]

        y = height - 100
        for linea in lineas:
            c.drawString(50, y, linea)
            y -= 25

        c.drawString(50, y - 20, "Gracias por su reserva. ¡Le esperamos!")

        c.save()
        messagebox.showinfo("Factura generada", f"Factura guardada como '{nombre_archivo}'")


class Incidencias:
    """
    Clase que gestiona la interfaz y operaciones de incidencias en la aplicación hotelera.
    Permite registrar, mostrar, eliminar y actualizar el estado de incidencias.
    """

    def __init__(self, parent_frame):
        """
        Inicializa la interfaz de la sección de incidencias, incluyendo formularios, botones y tabla de historial.

        Parámetro:
        - parent_frame: marco padre donde se mostrará la vista.
        """
        self.root = parent_frame
        self.root.configure(bg="white")

        # Variables para los campos del formulario
        self.id_var = StringVar()
        self.habitacion_var = StringVar()
        self.descripcion_var = StringVar()
        self.estado_var = StringVar(value="Pendiente")

        # Título principal
        Label(self.root, text="Gestión de Incidencias", font=("times new roman", 18, "bold"),
              bg="black", fg="gold").pack(fill=X)

        # Subtítulo informativo
        Label(self.root, text="Aquí irá el panel de incidencias...", font=("arial", 14)).pack(pady=50)

        # Encabezado del formulario
        Label(self.root, text="Registro de Incidencias", font=("times new roman", 20, "bold"), fg="red",
              bg="white").place(x=5, y=0)

        # Formulario de entrada de datos
        frame_form = LabelFrame(self.root, text="Nueva Incidencia", font=("arial", 12, "bold"), bg="white", bd=2,
                                relief=RIDGE)
        frame_form.place(x=5, y=50, width=500, height=250)

        # Campos del formulario
        Label(frame_form, text="ID Incidencia", font=("arial", 11, "bold"), bg="white").grid(row=0, column=0, padx=10,
                                                                                             pady=10, sticky=W)
        Entry(frame_form, textvariable=self.id_var, font=("arial", 11), width=30).grid(row=0, column=1)

        Label(frame_form, text="Habitación", font=("arial", 11, "bold"), bg="white").grid(row=1, column=0, padx=10,
                                                                                          pady=10, sticky=W)
        Entry(frame_form, textvariable=self.habitacion_var, font=("arial", 11), width=30).grid(row=1, column=1)

        Label(frame_form, text="Descripción", font=("arial", 11, "bold"), bg="white").grid(row=2, column=0, padx=10,
                                                                                           pady=10, sticky=W)
        Entry(frame_form, textvariable=self.descripcion_var, font=("arial", 11), width=30).grid(row=2, column=1)

        Label(frame_form, text="Estado", font=("arial", 11, "bold"), bg="white").grid(row=3, column=0, padx=10, pady=10,
                                                                                      sticky=W)
        combo_estado = ttk.Combobox(frame_form, textvariable=self.estado_var, values=["Pendiente", "Resuelta"],
                                    state="readonly", font=("arial", 11), width=28)
        combo_estado.grid(row=3, column=1)

        # Botones de acción
        btn_frame = Frame(frame_form, bg="white")
        btn_frame.place(x=10, y=170, width=470, height=70)

        Button(btn_frame, text="Registrar", command=self.agregar_incidencia, font=("arial", 11, "bold"), bg="black",
               fg="gold", width=10).grid(row=0, column=0, padx=10)
        Button(btn_frame, text="Eliminar", command=self.eliminar_incidencia, font=("arial", 11, "bold"), bg="black",
               fg="gold", width=10).grid(row=0, column=1, padx=10)
        Button(btn_frame, text="Reset", command=self.reset_campos, font=("arial", 11, "bold"), bg="black", fg="gold",
               width=10).grid(row=0, column=2, padx=10)
        Button(btn_frame, text="Marcar como Resuelta", command=self.marcar_resuelta,
               font=("arial", 11, "bold"), bg="black", fg="gold", width=22).grid(row=1, column=0, columnspan=3, pady=5)

        # Tabla de historial de incidencias
        frame_tabla = LabelFrame(self.root, text="Historial de Incidencias", font=("arial", 12, "bold"), bg="white",
                                 bd=2, relief=RIDGE)
        frame_tabla.place(x=520, y=50, width=750, height=400)

        # Scrollbars para la tabla
        scroll_x = Scrollbar(frame_tabla, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame_tabla, orient=VERTICAL)

        self.tabla = ttk.Treeview(frame_tabla, columns=("ID", "Habitación", "Descripción", "Estado"),
                                  xscrollcommand=scroll_x.set,
                                  yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.tabla.xview)
        scroll_y.config(command=self.tabla.yview)

        # Filtro por estado
        Label(self.root, text="Filtrar por estado:", font=("arial", 11, "bold"), bg="white").place(x=520, y=460)
        self.filtro_estado_var = StringVar(value="Todos")
        combo_filtro = ttk.Combobox(self.root, textvariable=self.filtro_estado_var,
                                    values=["Todos", "Pendiente", "Resuelta"],
                                    state="readonly", font=("arial", 10), width=18)
        combo_filtro.place(x=660, y=460)
        combo_filtro.bind("<<ComboboxSelected>>", lambda e: self.mostrar_incidencias())

        # Configurar columnas de la tabla
        for col in ("ID", "Habitación", "Descripción", "Estado"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150)

        self.tabla["show"] = "headings"
        self.tabla.pack(fill=BOTH, expand=1)
        self.tabla.bind("<Double-1>", self.seleccionar_fila)

        # Inicializar base de datos y cargar datos
        self.conectar_bd()
        self.crear_tabla()
        self.mostrar_incidencias()

    def conectar_bd(self):
        """Conecta con la base de datos SQLite de reservas."""
        self.conn = sqlite3.connect("reservas.db")
        self.cursor = self.conn.cursor()

    def crear_tabla(self):
        """Crea la tabla de incidencias si no existe."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidencias (
                id TEXT PRIMARY KEY,
                habitacion TEXT,
                descripcion TEXT,
                estado TEXT
            )
        """)
        self.conn.commit()

    def agregar_incidencia(self):
        """Registra una nueva incidencia con los datos introducidos."""
        id_ = self.id_var.get()
        hab = self.habitacion_var.get()
        desc = self.descripcion_var.get()
        est = self.estado_var.get()

        if not id_ or not hab or not desc:
            messagebox.showwarning("Campos incompletos", "Por favor rellena todos los campos.")
            return

        try:
            self.cursor.execute("INSERT INTO incidencias VALUES (?, ?, ?, ?)", (id_, hab, desc, est))
            self.conn.commit()
            self.mostrar_incidencias()
            messagebox.showinfo("Éxito", "Incidencia registrada.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe una incidencia con este ID.")

    def eliminar_incidencia(self):
        """Elimina la incidencia con el ID especificado."""
        id_ = self.id_var.get()
        if not id_:
            messagebox.showwarning("Aviso", "Introduce el ID de la incidencia a eliminar.")
            return
        self.cursor.execute("DELETE FROM incidencias WHERE id=?", (id_,))
        self.conn.commit()
        self.mostrar_incidencias()
        self.reset_campos()

    def mostrar_incidencias(self):
        """Muestra todas las incidencias o filtra por estado."""
        self.tabla.delete(*self.tabla.get_children())
        filtro = getattr(self, "filtro_estado_var", StringVar(value="Todos")).get()
        if filtro == "Todos":
            self.cursor.execute("SELECT * FROM incidencias")
        else:
            self.cursor.execute("SELECT * FROM incidencias WHERE estado=?", (filtro,))
        for fila in self.cursor.fetchall():
            self.tabla.insert("", END, values=fila)

    def seleccionar_fila(self, event):
        """Carga los datos de la fila seleccionada en el formulario."""
        item = self.tabla.focus()
        valores = self.tabla.item(item, "values")
        if valores:
            self.id_var.set(valores[0])
            self.habitacion_var.set(valores[1])
            self.descripcion_var.set(valores[2])
            self.estado_var.set(valores[3])

    def reset_campos(self):
        """Limpia todos los campos del formulario."""
        self.id_var.set("")
        self.habitacion_var.set("")
        self.descripcion_var.set("")
        self.estado_var.set("Pendiente")

    def marcar_resuelta(self):
        """Marca una incidencia como resuelta si existe."""
        id_ = self.id_var.get()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona o introduce el ID de una incidencia.")
            return

        self.cursor.execute("SELECT * FROM incidencias WHERE id=?", (id_,))
        if not self.cursor.fetchone():
            messagebox.showerror("Error", "No se encontró ninguna incidencia con ese ID.")
            return

        self.cursor.execute("UPDATE incidencias SET estado='Resuelta' WHERE id=?", (id_,))
        self.conn.commit()
        self.mostrar_incidencias()
        self.estado_var.set("Resuelta")
        messagebox.showinfo("Actualizado", "✅ Incidencia marcada como resuelta.")


import threading
import time
import random
from datetime import datetime, timedelta
from faker import Faker

class Simulador:
    def __init__(self, app):
        # Referencia a la aplicación principal (HotelManagementSystem)
        self.app = app
        # Generador de datos falsos en español
        self.faker = Faker("es_ES")
        # Contador de iteraciones para generar identificadores únicos
        self.contador = 1

    def generar_dni(self):
        # Genera un DNI válido con letra correspondiente
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        num = random.randint(10000000, 99999999)
        letra = letras[num % 23]
        return f"{num}{letra}"

    def generar_pasaporte_o_nie(self):
        # Genera un número aleatorio para pasaporte o NIE
        return f"{self.faker.random_uppercase_letter()}{self.faker.random_number(digits=7)}{self.faker.random_uppercase_letter()}"

    def generar_habitacion_valida(self):
        # Devuelve una habitación aleatoria con formato "número tipo"
        planta = random.randint(1, 3)
        posicion = random.randint(1, 10)
        numero = planta * 100 + posicion

        if posicion <= 5:
            tipo = "Estándar"
        elif posicion <= 9:
            tipo = "Familiar"
        else:
            tipo = "Suite"

        return f"{numero} {tipo}"

    def iniciar(self):
        # Función principal para iniciar la simulación en segundo plano

        def insertar_datos():
            inicio = time.time()
            duracion = 20 * 60  # Duración total de la simulación: 20 minutos
            intervalo = 15  # Tiempo entre iteraciones: 15 segundos

            while time.time() - inicio < duracion:
                print(f"[{self.contador}] Insertando cliente y reserva...")

                # ---------- CREACIÓN DE CLIENTE ----------
                self.app.cust_details()  # Carga la vista de clientes
                cliente = self.app.app
                campos = cliente.campos

                # Generación de datos aleatorios
                nombre = self.faker.name()
                movil = self.faker.msisdn()[0:9]
                email = self.faker.email()
                direccion = self.faker.street_address()
                nacionalidad = self.faker.current_country()
                cp = self.faker.postcode()
                doc_tipo = random.choice(["DNI", "Pasaporte", "NIE"])
                num_doc = self.generar_dni() if doc_tipo == "DNI" else self.generar_pasaporte_o_nie()
                ref = f"AUTO{self.contador:04d}"

                # Rellenado automático de campos
                campos["Ref cliente"].delete(0, "end")
                campos["Ref cliente"].insert(0, ref)
                campos["Nombre cliente"].delete(0, "end")
                campos["Nombre cliente"].insert(0, nombre)
                campos["Género"].set(random.choice(["Masculino", "Femenino", "Otro"]))
                campos["Código Postal"].delete(0, "end")
                campos["Código Postal"].insert(0, cp)
                campos["Móvil"].delete(0, "end")
                campos["Móvil"].insert(0, movil)
                campos["Email"].delete(0, "end")
                campos["Email"].insert(0, email)
                campos["Nacionalidad"].delete(0, "end")
                campos["Nacionalidad"].insert(0, nacionalidad)
                campos["Tipo de Documento"].set(doc_tipo)
                campos["Número de Documento"].delete(0, "end")
                campos["Número de Documento"].insert(0, num_doc)
                campos["Dirección"].delete(0, "end")
                campos["Dirección"].insert(0, direccion)

                # Guardado en la base de datos
                cliente.insertar_cliente()

                # ---------- CREACIÓN DE RESERVA ----------
                self.app.room_details()  # Carga la vista de reservas
                reserva = self.app.app
                datos = reserva.datos

                # Asignación de cliente y datos de reserva
                datos["Contacto del Cliente"].delete(0, "end")
                datos["Contacto del Cliente"].insert(0, movil)

                personas = random.randint(1, 4)
                datos["Nº de Personas"].delete(0, "end")
                datos["Nº de Personas"].insert(0, str(personas))

                entrada = datetime.today() + timedelta(days=random.randint(0, 3))
                salida = entrada + timedelta(days=random.randint(1, 5))
                datos["Fecha de Entrada"].set_date(entrada)
                datos["Fecha de Salida"].set_date(salida)

                habitacion_id = self.generar_habitacion_valida()
                datos["Habitación"].set(habitacion_id)

                datos["Comida"].set(random.choice(["Desayuno", "Media pensión", "Pensión completa"]))

                # Cálculo automático de días y precios
                reserva.calcular_dias()
                reserva.insertar_reserva()

                # Contador para el siguiente cliente
                self.contador += 1
                time.sleep(intervalo)

            print("✅ Finalizado: Clientes y reservas")

        # Inicia el hilo en segundo plano
        threading.Thread(target=insertar_datos, daemon=True).start()

# Ejecución principal si el archivo se ejecuta directamente
if __name__ == "__main__":
    def lanzar_app_principal():
        # Lanza la interfaz principal de gestión hotelera
        root_app = Tk()
        app = HotelManagementSystem(root_app)
        # Botón para lanzar el simulador automático
        Button(root_app, text="Iniciar Test Aleatorio", font=("Arial", 12), bg="black", fg="gold",
               command=lambda: Simulador(app).iniciar()).place(x=1100, y=10)
        root_app.mainloop()

    # Interfaz de bienvenida
    root_inicio = Tk()
    app_inicio = VentanaInicio(root_inicio, continuar_callback=lanzar_app_principal)
    root_inicio.mainloop()
