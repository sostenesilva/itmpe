from rolepermissions.roles import AbstractUserRole

class Controle(AbstractUserRole):
    avaliable_permissions = {
        'adicionar':True,
        'remover':True,
        'visualizar':True,
        'editar':True,
        'enviar':True
    }

class Administração(AbstractUserRole):
    name = 'Administração'
    avaliable_permissions = {
    }

class Finanças(AbstractUserRole):
    name = 'Finanças'
    avaliable_permissions = {
    }

class Educação(AbstractUserRole):
    avaliable_permissions = {
    }

class Saúde(AbstractUserRole):
    avaliable_permissions = {
    }

class Assistência_Social(AbstractUserRole):
    avaliable_permissions = {
    }

class Agricultura(AbstractUserRole):
    avaliable_permissions = {
    }
class Meio_Ambiente(AbstractUserRole):
    avaliable_permissions = {
    }
class Cidade(AbstractUserRole):
    avaliable_permissions = {
    }
class Turismo(AbstractUserRole):
    avaliable_permissions = {
    }
class Obras(AbstractUserRole):
    avaliable_permissions = {
    }
class Controladoria(AbstractUserRole):
    avaliable_permissions = {
    }

