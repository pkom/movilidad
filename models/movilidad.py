db.define_table('aulas',
    Field('id','integer'),
    Field('nombre_aula','string'),
    migrate=False)

#--------
db.define_table('aulasequipos',
    Field('id','integer'),
    Field('id_aula','integer'),
    Field('id_equipo','integer'),
    Field('mac','string'),
    Field('ip','string'),
    migrate=False)

#--------
db.define_table('equipos',
    Field('id','integer'),
    Field('nombre_equipo','string'),
    migrate=False)

#--------
db.define_table('estadisticas',
    Field('id','integer'),
    Field('id_usuario','integer'),
    Field('id_aula_equipo','integer'),
    Field('fecha','string'),
    Field('hora','string'),
    migrate=False)

#--------
db.define_table('usuarios',
    Field('id','integer'),
    Field('nombre_usuario','string'),
    migrate=False)
