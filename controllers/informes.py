# coding: utf8
# intente algo como
def index(): return dict(message="hello from informes.py")

def informepuesto():
    if not request.args(0):
        mensaje = 'No se ha indicado identificador de sesión'
    else:    
        #import urllib2
        #import base64
        import socket
        from datetime import datetime
        
        estadistica = db((db.estadisticas.id == request.args(0)) &
                   (db.estadisticas.id_aula_equipo == db.aulasequipos.id) &
                   (db.aulasequipos.id_equipo == db.equipos.id)).select().first()
        
        nombrequipo = estadistica.equipos.nombre_equipo
        
        if nombrequipo.find('-o') != -1:
            #es un terminal ligero, hay que buscar el profesor
            nombrepro = nombrequipo[:nombrequipo.find("-")]+'-pro'
            ip = db((db.equipos.nombre_equipo == nombrepro) &
                          (db.equipos.id == db.aulasequipos.id_equipo)).select().first().aulasequipos.ip
        else:    
            ip = estadistica.aulasequipos.ip
        if ip == "127.0.0.1" or ip == "127.0.1.1":
            #no está bien registrada la IP de la máquina, voy a consultar al dns
            try:
                ip = socket.gethostbyname(nombrequipo)
            except:
                pass
        ipparsed = ip.replace('.', '_')
        fecha = datetime.strptime(estadistica.estadisticas.fecha, "%y/%m/%d")
        fechastr = fecha.strftime("%Y%b%d-%Y%b%d")
        stringurl = "http://ldap/squid-reports/Daily/"+fechastr+"/"+ipparsed+"/"+ipparsed+".html"
        redirect(stringurl)
        #peticion = urllib2.Request(stringurl)
        #base64string = base64.encodestring('%s:%s' % ('ldap', 'ldap')).replace('\n', '')
        #peticion.add_header("Authorization", "Basic %s" % base64string)   
        #resultado = XML(urllib2.urlopen(peticion).read())
    return dict(resultado=resultado,nombrequipo=nombrequipo,ip=ip,fecha=estadistica.estadisticas.fecha)
