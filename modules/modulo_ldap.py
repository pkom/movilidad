#!/usr/bin/env python
# coding: utf8
from gluon import *
import ldap

def dame_nombre_usuario(usuario):
    conexionldap = ldap.initialize('ldap://ldap.maestrojuancalero')
    nombre = conexionldap.search_s("ou=People,dc=instituto,dc=extremadura,dc=es",
                                    ldap.SCOPE_SUBTREE,
                                    "uid="+usuario, ['cn'])
    if not nombre:
        return usuario
    else:
        return nombre[0][1]['cn'][0]

def dame_uids_usuario(nombre):
    conexionldap = ldap.initialize('ldap://ldap.maestrojuancalero')
    lista = conexionldap.search_s("ou=People,dc=instituto,dc=extremadura,dc=es",
                                    ldap.SCOPE_SUBTREE,
                                    "cn=*"+nombre+"*", ['uid'])
    return [tupla[1]['uid'][0] for tupla in lista]
