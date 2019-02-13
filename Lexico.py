# -*- coding: utf-8 -*-



import string
import sys
import os



class Lexico():
	
	ERROR			= 0
	
	IDENTIFICADOR	= 2
	ENTERO			= 3
	FLOTANTE		= 5
	CADENA			= 8
	
	OPADIC			= 9
	OPMUL			= 10
	
	DELIM			= 12
	
	OPRELACIONAL	= 14
	OPASIG			= 15
	
	NOTLOGICO		= 16
	OPLOGICO		= 19
	
	PARENTOPERT		= 11
	PARENTCIERRE	= 22
	LLAVEOPERT		= 23
	LLAVECIERRE		= 24
	CORCHETEOPERT	= 25
	CORCHETECIERRE	= 26
	COMA			= 27
	
	EOF				= 20
	
	def __init__(self, Cadena):
		
		self.cadena   = Cadena
		self.errorc   = ''
		self.pos      = 0
		self.continua = False
		self.estado   = 0
		self.simbolo  = ''
		self.c        = ''
		self.tipo     = 0
	
	def error(self):
		
		self.estado = 100
		self.errorc = self.c
		self.retroceso()
		self.continua = False
		
	def aceptacion(self, estado):
		
		self.simbolo += self.c
		self.estado   = estado
		self.continua = False
	
	def sigEstado(self, estado):
		
		self.simbolo += self.c
		self.estado = estado
	
	def sigCaracter(self):
		
		self.pos += 1
		return self.cadena[self.pos-1]
	
	def esLetraO_(self, caracter):
		
		if caracter in string.ascii_letters + '_':	# Comprueba si el Caracter esta
			return True								# en la cadenade de la 'a-z' y 'A-Z'
		else: return False							# mas el guion bajo '_'
		
	def esDigito(self, caracter):
		
		if caracter in string.digits: return True	# Comprueba si el Caracter esta
		else: return False							# en la cadenade del '0-9'
		
	def esAscii(self, caracter):
		
		if caracter in string.printable+'¡¿': return True	# Comprueba si el Caracter esta en la cadenade.
		else: return False								# Son Los 102 Caracteres Ascii Mas Usados.
		
	def esOtroTipo(self, caracter):
		
		if caracter in ['+','-','*','/','\\','%','<','>','&','|','!','=','(',')','{','}','[',']',';','#','$'] or\
		self.esDigito(caracter) or self.esAscii(caracter):
			return True
		else:
			return False
		
	def retroceso(self):
		
		self.pos -= 1
		self.continua = False
	
	
	
	def sigSimbolo(self):
		
		self.estado   = 0
		self.continua = True
		self.simbolo = ''
		
		while self.continua:
			
			# ~ print(self.estado)
			# ~ print(self.c)
			
			self.c = self.sigCaracter()
			
			if self.estado == 0:
				
				if self.c in [' ','\n','\t','\r']: 	self.aceptacion(1)
				elif self.esLetraO_(self.c):		self.sigEstado(2)
				elif self.esDigito(self.c):			self.sigEstado(3)
				elif self.c == '.':					self.sigEstado(4)
				elif self.c == '"':					self.sigEstado(6)
				elif self.c in ['+','-']:			self.aceptacion(9)
				elif self.c in ['*','/','%']:		self.aceptacion(10)
				elif self.c == ';':					self.aceptacion(12)
				elif self.c == '=':					self.sigEstado(15)
				elif self.c in ['<','>']:			self.sigEstado(13)
				elif self.c == '!':					self.aceptacion(16)
				elif self.c == '|':					self.sigEstado(17)
				elif self.c == '&':					self.sigEstado(18)
				elif self.c == '(':					self.aceptacion(11)
				elif self.c == ')':					self.aceptacion(22)
				elif self.c == '{':					self.aceptacion(23)
				elif self.c == '}':					self.aceptacion(24)
				elif self.c == '[':					self.aceptacion(25)
				elif self.c == ']':					self.aceptacion(26)
				elif self.c == ',':					self.aceptacion(27)
				elif self.c == '$':					self.aceptacion(20)
				elif self.c == '#':					self.sigEstado(32)
				else: self.error()
				
			elif self.estado == 1: pass
			
			elif self.estado == 2:
				
				if self.c in [' ','\n','\t','\r']: self.retroceso()
				elif self.esLetraO_(self.c) or self.esDigito(self.c): self.sigEstado(2)
				elif self.esOtroTipo(self.c): self.retroceso()
				else: self.error()
				
			elif self.estado == 3:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.esDigito(self.c): 		self.sigEstado(3)
				elif self.c == '.':					self.sigEstado(4)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
				
			elif self.estado == 4:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.esDigito(self.c): 		self.sigEstado(5)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
				
			elif self.estado == 5:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.esDigito(self.c): 		self.sigEstado(5)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
				
			elif self.estado == 6:
				
				if self.c == '"':					self.sigEstado(8)
				elif self.esAscii(self.c): 			self.sigEstado(7)
				elif self.c == '\\':	 			self.sigEstado(21)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
				
			elif self.estado == 7:
				
				if self.c == '"':					self.sigEstado(8)
				elif self.c == '\\':	 			self.sigEstado(21)
				elif self.esAscii(self.c): 			self.sigEstado(7)
				else: self.error()
				
			elif self.estado == 8:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
			
			elif self.estado == 9:  pass
			
			elif self.estado == 10: pass
			
			elif self.estado == 11: pass
			
			elif self.estado == 12: pass
			
			elif self.estado == 13:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.c == '=':					self.aceptacion(14)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
			
			elif self.estado == 14: pass
			
			elif self.estado == 15:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.c == '=':					self.aceptacion(14)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
			
			elif self.estado == 16:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.c == '=':					self.aceptacion(14)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
			
			elif self.estado == 17:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.c == '|':					self.aceptacion(19)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
			
			elif self.estado == 18:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.c == '&':					self.aceptacion(19)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
			
			elif self.estado == 19: pass
			
			elif self.estado == 20: pass
			
			elif self.estado == 21:
				
				if self.c in [' ','\n','\t','\r']: 	self.retroceso()
				elif self.c == '"':					self.sigEstado(7)
				elif self.esAscii(self.c):			self.sigEstado(7)
				elif self.esOtroTipo(self.c): 		self.retroceso()
				else: self.error()
			
			elif self.estado == 22: pass
			
			elif self.estado == 23: pass
			
			elif self.estado == 24: pass
			
			elif self.estado == 25: pass
			
			elif self.estado == 26: pass
			
			elif self.estado == 27: pass
			
			elif self.estado == 32:
				
				if   self.c in ['\n','$']: self.retroceso()
				
				self.sigEstado(32)
			
		
		
		if   self.estado == 1:	self.tipo = self.sigSimbolo()	# ' ','\n','\t','\r'
		elif self.estado == 2:	self.tipo = self.IDENTIFICADOR	# xD
		elif self.estado == 3:	self.tipo = self.ENTERO			# 3
		elif self.estado == 5:	self.tipo = self.FLOTANTE		# 3.1416
		elif self.estado == 8:	self.tipo = self.CADENA			# "xD"
		elif self.estado == 9:	self.tipo = self.OPADIC			# +, -
		elif self.estado == 10:	self.tipo = self.OPMUL			# *, /, %
		elif self.estado == 12:	self.tipo = self.DELIM			# ;
		elif self.estado in [13, 14]: self.tipo = self.OPRELACIONAL	# <, >, <=, >=, ==, !=
		elif self.estado == 15:	self.tipo = self.OPASIG			# =
		elif self.estado == 16: self.tipo = self.NOTLOGICO		# !
		elif self.estado == 19: self.tipo = self.OPLOGICO		# &&, ||
		elif self.estado == 11:	self.tipo = self.PARENTOPERT	# (
		elif self.estado == 22:	self.tipo = self.PARENTCIERRE	# )
		elif self.estado == 23:	self.tipo = self.LLAVEOPERT		# {
		elif self.estado == 24:	self.tipo = self.LLAVECIERRE	# }
		elif self.estado == 25:	self.tipo = self.CORCHETEOPERT	# [
		elif self.estado == 26:	self.tipo = self.CORCHETECIERRE	# ]
		elif self.estado == 27:	self.tipo = self.COMA			# ','
		elif self.estado == 20:	self.tipo = self.EOF			# $
		elif self.estado == 32:	self.tipo = self.sigSimbolo()	# # <-- Comentarios
		else: self.tipo = self.ERROR
		
		
		
		return self.tipo


