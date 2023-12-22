class UsuarioDAO:
    def __init__(self):
        self.usuarios = {}  # Este diccionario almacena los usuarios

    def registrar_usuario(self, nombre, rut, contrasena, tipo_usuario):
        # Asumiendo que no se permiten RUT duplicados
        if rut in self.usuarios:
            raise ValueError("El RUT ya está registrado")
        self.usuarios[rut] = {
            'nombre': nombre,
            'rut': rut,
            'contrasena': contrasena,
            'tipo_usuario': tipo_usuario
        }
    def obtener_estudiantes(self):
        # Suponiendo que los usuarios están almacenados en un diccionario
        # y cada usuario tiene un campo 'tipo_usuario' que indica su rol
        return [usuario for usuario in self.usuarios.values() if usuario['tipo_usuario'] == 'Estudiante']


    def obtener_usuarios_por_tipo(self, tipo_usuario):
        return [usuario for usuario in self.usuarios.values() if usuario['tipo_usuario'] == tipo_usuario]

    def validar_usuario(self, rut, contrasena):
        """
        Valida si un usuario con el RUT y contraseña dados existe.
        Devuelve True si el usuario existe y la contraseña es correcta, de lo contrario False.
        """
        usuario = self.usuarios.get(rut)
        if usuario and usuario['contrasena'] == contrasena:
            return True
        return False