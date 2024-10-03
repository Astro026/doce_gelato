

class user:
    def __init__(self, usuario, senha,id,cargo) -> None:
        self.usuario = usuario
        self.senha = senha
        self.id = id
        self.cargo = cargo
        self.flag_returne = False

    def ver_requisitos(self, cargo_requisitado):
        if self.cargo == cargo_requisitado:
            print('GESTOR')
            self.flag_returne = True
            return self.flag_returne
        else: 
            self.flag_returne = False
            print('Voce não possue permisão suficinte')
            return self.flag_returne