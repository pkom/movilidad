# coding: utf8
# intente algo como
import modulo_ldap

def index(): return dict(message="hello from services.py")

def call():
    session.forget()
    return service()

@service.json
def getEstadisticas():
    fields = ['id','nombre','usuario','equipo','fecha','hora']  
    rows = []
    if request.vars._search == 'true':
        searching = True
    else:
        searching = False    
    page = int(request.vars.page) or 0
    pagesize = int(request.vars.rows) or 0   
    limitby = (page * pagesize - pagesize,page * pagesize)
    
    if (request.vars.sord == 'asc' and request.vars.sidx == 'id'):
        orderby = db.estadisticas.id
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'id'):
        orderby = ~db.estadisticas.id
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'usuario'):
        orderby = (db.usuarios.nombre_usuario | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'usuario'):
        orderby = (~db.usuarios.nombre_usuario | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'equipo'):
        orderby = (db.equipos.nombre_equipo | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'equipo'):
        orderby = (~db.equipos.nombre_equipo | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'fecha'):
        orderby = (db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'fecha'):
        orderby = (~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'hora'):
        orderby = db.estadisticas.hora
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'hora'):
        orderby = ~db.estadisticas.hora
    else:
        order = ~orderby
    
    queries=[]
    queries.append(db.estadisticas.id_usuario == db.usuarios.id)
    queries.append(db.estadisticas.id_aula_equipo == db.aulasequipos.id)
    queries.append(db.aulasequipos.id_aula == db.aulas.id)
    queries.append(db.aulasequipos.id_equipo == db.equipos.id)    
    
    if searching:
        if request.vars.fecha:
            fecha = request.vars.fecha
            queries.append(db.estadisticas.fecha == fecha)
        if request.vars.hora:
            hora = request.vars.hora
            queries.append(db.estadisticas.hora >= hora)            
        if request.vars.nombre:
            #debemos tener en cuenta los posibles usuarios que contienen ese nombre
            lista = modulo_ldap.dame_uids_usuario(request.vars.nombre.lower())            
            q = []
            for usu in lista:
                q.append(db.usuarios.nombre_usuario.lower().like(usu))
            qu = reduce(lambda a,b:(a|b),q)
            queries.append(qu) 
        if request.vars.usuario:
            usuario = '%'+request.vars.usuario.lower()+'%'
            queries.append(db.usuarios.nombre_usuario.lower().like(usuario))                 
        if request.vars.equipo:    
            equipo = '%'+request.vars.equipo.lower()+'%'
            queries.append(db.equipos.nombre_equipo.lower().like(equipo)) 
    query = reduce(lambda a,b:(a&b),queries)

    for r in db(query).select(db.estadisticas.ALL, db.aulasequipos.ALL, db.usuarios.ALL, db.aulas.ALL, db.equipos.ALL, limitby=limitby, orderby=orderby):
        vals = []
        for f in fields:
            if f == 'nombre':
                nombreusuario = modulo_ldap.dame_nombre_usuario(r.usuarios.nombre_usuario)
                vals.append(nombreusuario)
            elif f == 'usuario':
                usuario = r.usuarios.nombre_usuario
                vals.append(usuario)
            elif f == 'equipo':
                equipo = r.equipos.nombre_equipo
                vals.append(equipo)
            else:
                rep = db.estadisticas[f].represent
                if rep:
                    vals.append(rep(r.estadisticas[f]))
                else:
                    vals.append(r.estadisticas[f])
        rows.append(dict(id=r.estadisticas.id,cell=vals))
    total = db(query).count()    
    if total <= pagesize:
        pages = 1
    else:   
        pages = int(total/pagesize)
        if total % pagesize <> 0:
            pages += 1
    data = dict(total=pages,page=page,records=total,rows=rows)
    return data
    
@service.json
def getPaginasVisitadas():
    fields = ['Sitio','Connect','Bytes','%Bytes','En Caché','Fuera de Caché','Tiempo transcurrido','Milisegundos','%Tiempo']  
    rows = []
    if request.vars._search == 'true':
        searching = True
    else:
        searching = False    
    page = int(request.vars.page) or 0
    pagesize = int(request.vars.rows) or 0   
    limitby = (page * pagesize - pagesize,page * pagesize)
    
    if (request.vars.sord == 'asc' and request.vars.sidx == 'id'):
        orderby = db.estadisticas.id
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'id'):
        orderby = ~db.estadisticas.id
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'usuario'):
        orderby = (db.usuarios.nombre_usuario | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'usuario'):
        orderby = (~db.usuarios.nombre_usuario | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'equipo'):
        orderby = (db.equipos.nombre_equipo | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'equipo'):
        orderby = (~db.equipos.nombre_equipo | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'fecha'):
        orderby = (db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'fecha'):
        orderby = (~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'hora'):
        orderby = db.estadisticas.hora
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'hora'):
        orderby = ~db.estadisticas.hora
    else:
        order = ~orderby
    
    queries=[]
    queries.append(db.estadisticas.id_usuario == db.usuarios.id)
    queries.append(db.estadisticas.id_aula_equipo == db.aulasequipos.id)
    queries.append(db.aulasequipos.id_aula == db.aulas.id)
    queries.append(db.aulasequipos.id_equipo == db.equipos.id)    
    
    if searching:
        if request.vars.fecha:
            fecha = request.vars.fecha
            queries.append(db.estadisticas.fecha == fecha)
        if request.vars.hora:
            hora = request.vars.hora
            queries.append(db.estadisticas.hora >= hora)            
        if request.vars.nombre:
            #debemos tener en cuenta los posibles usuarios que contienen ese nombre
            lista = modulo_ldap.dame_uids_usuario(request.vars.nombre.lower())            
            q = []
            for usu in lista:
                q.append(db.usuarios.nombre_usuario.lower().like(usu))
            qu = reduce(lambda a,b:(a|b),q)
            queries.append(qu) 
        if request.vars.usuario:
            usuario = '%'+request.vars.usuario.lower()+'%'
            queries.append(db.usuarios.nombre_usuario.lower().like(usuario))                 
        if request.vars.equipo:    
            equipo = '%'+request.vars.equipo.lower()+'%'
            queries.append(db.equipos.nombre_equipo.lower().like(equipo)) 
    query = reduce(lambda a,b:(a&b),queries)

    for r in db(query).select(db.estadisticas.ALL, db.aulasequipos.ALL, db.usuarios.ALL, db.aulas.ALL, db.equipos.ALL, limitby=limitby, orderby=orderby):
        vals = []
        for f in fields:
            if f == 'nombre':
                nombreusuario = modulo_ldap.dame_nombre_usuario(r.usuarios.nombre_usuario)
                vals.append(nombreusuario)
            elif f == 'usuario':
                usuario = r.usuarios.nombre_usuario
                vals.append(usuario)
            elif f == 'equipo':
                equipo = r.equipos.nombre_equipo
                vals.append(equipo)
            else:
                rep = db.estadisticas[f].represent
                if rep:
                    vals.append(rep(r.estadisticas[f]))
                else:
                    vals.append(r.estadisticas[f])
        rows.append(dict(id=r.estadisticas.id,cell=vals))
    total = db(query).count()    
    if total <= pagesize:
        pages = 1
    else:   
        pages = int(total/pagesize)
        if total % pagesize <> 0:
            pages += 1
    data = dict(total=pages,page=page,records=total,rows=rows)
    return data
    
@service.json
def getPaginaVisitadaHoras():
    fields = ['Hora']  
    rows = []
    if request.vars._search == 'true':
        searching = True
    else:
        searching = False    
    page = int(request.vars.page) or 0
    pagesize = int(request.vars.rows) or 0   
    limitby = (page * pagesize - pagesize,page * pagesize)
    
    if (request.vars.sord == 'asc' and request.vars.sidx == 'id'):
        orderby = db.estadisticas.id
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'id'):
        orderby = ~db.estadisticas.id
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'usuario'):
        orderby = (db.usuarios.nombre_usuario | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'usuario'):
        orderby = (~db.usuarios.nombre_usuario | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'equipo'):
        orderby = (db.equipos.nombre_equipo | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'equipo'):
        orderby = (~db.equipos.nombre_equipo | ~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'fecha'):
        orderby = (db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'fecha'):
        orderby = (~db.estadisticas.fecha | ~db.estadisticas.hora)
    elif (request.vars.sord == 'asc' and request.vars.sidx == 'hora'):
        orderby = db.estadisticas.hora
    elif (request.vars.sord == 'desc' and request.vars.sidx == 'hora'):
        orderby = ~db.estadisticas.hora
    else:
        order = ~orderby
    
    queries=[]
    queries.append(db.estadisticas.id_usuario == db.usuarios.id)
    queries.append(db.estadisticas.id_aula_equipo == db.aulasequipos.id)
    queries.append(db.aulasequipos.id_aula == db.aulas.id)
    queries.append(db.aulasequipos.id_equipo == db.equipos.id)    
    
    if searching:
        if request.vars.fecha:
            fecha = request.vars.fecha
            queries.append(db.estadisticas.fecha == fecha)
        if request.vars.hora:
            hora = request.vars.hora
            queries.append(db.estadisticas.hora >= hora)            
        if request.vars.nombre:
            #debemos tener en cuenta los posibles usuarios que contienen ese nombre
            lista = modulo_ldap.dame_uids_usuario(request.vars.nombre.lower())            
            q = []
            for usu in lista:
                q.append(db.usuarios.nombre_usuario.lower().like(usu))
            qu = reduce(lambda a,b:(a|b),q)
            queries.append(qu) 
        if request.vars.usuario:
            usuario = '%'+request.vars.usuario.lower()+'%'
            queries.append(db.usuarios.nombre_usuario.lower().like(usuario))                 
        if request.vars.equipo:    
            equipo = '%'+request.vars.equipo.lower()+'%'
            queries.append(db.equipos.nombre_equipo.lower().like(equipo)) 
    query = reduce(lambda a,b:(a&b),queries)

    for r in db(query).select(db.estadisticas.ALL, db.aulasequipos.ALL, db.usuarios.ALL, db.aulas.ALL, db.equipos.ALL, limitby=limitby, orderby=orderby):
        vals = []
        for f in fields:
            if f == 'nombre':
                nombreusuario = modulo_ldap.dame_nombre_usuario(r.usuarios.nombre_usuario)
                vals.append(nombreusuario)
            elif f == 'usuario':
                usuario = r.usuarios.nombre_usuario
                vals.append(usuario)
            elif f == 'equipo':
                equipo = r.equipos.nombre_equipo
                vals.append(equipo)
            else:
                rep = db.estadisticas[f].represent
                if rep:
                    vals.append(rep(r.estadisticas[f]))
                else:
                    vals.append(r.estadisticas[f])
        rows.append(dict(id=r.estadisticas.id,cell=vals))
    total = db(query).count()    
    if total <= pagesize:
        pages = 1
    else:   
        pages = int(total/pagesize)
        if total % pagesize <> 0:
            pages += 1
    data = dict(total=pages,page=page,records=total,rows=rows)
    return data
