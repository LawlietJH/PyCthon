# -*- coding: utf-8 -*-

import Lexico
import Arbol
import string
import sys
import os

class Sintactico():
	
	def __init__(self):
		
		with open('entrada.txt','r') as Archivo: self.Cadena = Archivo.read()+'$'
		Archivo.close()
		
		#===============================================================
		self.Suma			= Arbol.Suma
		self.Multi			= Arbol.Multi
		self.Asign			= Arbol.Asignacion
		
		self.ReservIf		= Arbol.ReservIf
		self.ReservPrint	= Arbol.ReservPrint
		self.Separador		= Arbol.Separador
		self.Signo			= Arbol.Signo
		self.ExpresionArb	= Arbol.Expre
		self.Bloque			= Arbol.Bloque
		self.ReservElse		= Arbol.ReservElse
		self.ReservWhile	= Arbol.ReservWhile
		
		self.Logico			= Arbol.Logico
		self.Relacional		= Arbol.Relacional
		
		self.Identi			= Arbol.Identificador
		self.Entero			= Arbol.Entero
		self.Flotante		= Arbol.Flotante
		self.CadenaArb		= Arbol.Cadena
		#===============================================================
		
		self.ListaArbolesBloque = [[],[],[],[],[]]		# Permite Anidación de hasta 5 niveles.
		self.ListaArboles = []
		self.ArbolActual = []
		self.ArbolPila = []
		
		self.lexico = Lexico.Lexico(self.Cadena)
		self.Cadena = ''
		self.PalabReserv = ['if', 'else', 'do','while', 'print']
		
		self.BloqueActivo = [False, False, False, False, False]		# Permite Anidación de hasta 5 niveles.
	
	def Resultado(self, Salida):
		
		if Salida == 0:
			print('\n\n\n\t Error Sintáctico: ', Salida)
			
			for x in range(5):
				self.lexico.sigSimbolo()
				print(self.lexico.simbolo,end='')
			Archivo = open('salida.txt','w')
			Cadena = Archivo.write(str(Salida))
			Archivo.close()
	
	def error(self):
		
		self.Resultado(0)
		sys.exit()
		
	def analiza(self):
		
		self.lexico.sigSimbolo()
		
		self.A()
		self.Comprueba(20)
	
	def Comprueba(self, Tipo):
		
		if self.lexico.tipo == Tipo:
			
			try: self.lexico.sigSimbolo()
			except: self.Resultado(1)
			
		else: self.error()
	
	
	def A(self):
		
		xD = True
		
		if self.lexico.tipo == 2 and self.lexico.simbolo in self.PalabReserv:
			
			while xD:
				
				xD = False
				
				if self.lexico.simbolo == 'if':
					
					self.If()
					xD = True
					
				if self.lexico.simbolo == 'do':
					
					self.DoWhile()
					xD = True
					
				if self.lexico.simbolo == 'while':
					
					self.While()
					xD = True
					
				if self.lexico.simbolo == 'for':
					
					self.For()
					xD = True
					
				if self.lexico.simbolo == 'print':
					
					self.Print()
					xD = True
		
		self.Asignacion()
		
	
	def Asignacion(self, Bool=True):
		
		#===============================================================
		Simbolo = None
		#===============================================================
		
		if self.lexico.tipo == 2:
			
			#================================================================
			R = self.Identi(None, self.lexico.simbolo)
			#================================================================
			
			self.lexico.sigSimbolo()
			
			self.Comprueba(15)
			
			#================================================================
			P = self.Expresion()
			P = self.Asign(R,P)
			
			if self.BloqueActivo[0]:
				
				if   self.BloqueActivo[4]: self.ListaArbolesBloque[4].append(P)
				elif self.BloqueActivo[3]: self.ListaArbolesBloque[3].append(P)
				elif self.BloqueActivo[2]: self.ListaArbolesBloque[2].append(P)
				elif self.BloqueActivo[1]: self.ListaArbolesBloque[1].append(P)
				elif self.BloqueActivo[0]: self.ListaArbolesBloque[0].append(P)
				
			else: self.ListaArboles.append(P)
			
			#================================================================
			
			if Bool:
				
				self.Comprueba(12)
				self.A()
	
	
	def If(self):
		
		self.lexico.sigSimbolo()
		
		self.Comprueba(11)
		#===============================================================
		P = self.ComparacionLogica()
		R = self.ReservIf()
		R.SetHijo(P)
		#===============================================================
		self.Comprueba(22)
		
		if self.lexico.tipo == 23:
			
			#===============================================================
			
			if   self.BloqueActivo[0] == False: self.BloqueActivo[0] = True
			elif self.BloqueActivo[1] == False: self.BloqueActivo[1] = True
			elif self.BloqueActivo[2] == False: self.BloqueActivo[2] = True
			elif self.BloqueActivo[3] == False: self.BloqueActivo[3] = True
			elif self.BloqueActivo[4] == False: self.BloqueActivo[4] = True
			
			B = self.Bloque()
			#===============================================================
			
			self.lexico.sigSimbolo()
			self.A()
			self.Comprueba(24)
			
			#===============================================================
			if self.BloqueActivo[0]:
			
				if self.BloqueActivo[4]:
					
					B.SetListaHijos(self.ListaArbolesBloque[4])
					self.BloqueActivo[4] = False
					self.ListaArbolesBloque[4] = []
					
				elif self.BloqueActivo[3]:
					
					B.SetListaHijos(self.ListaArbolesBloque[3])
					self.BloqueActivo[3] = False
					self.ListaArbolesBloque[3] = []
					
				elif self.BloqueActivo[2]:
					
					B.SetListaHijos(self.ListaArbolesBloque[2])
					self.BloqueActivo[2] = False
					self.ListaArbolesBloque[2] = []
					
				elif self.BloqueActivo[1]:
					
					B.SetListaHijos(self.ListaArbolesBloque[1])
					self.BloqueActivo[1] = False
					self.ListaArbolesBloque[1] = []
					
				elif self.BloqueActivo[0]:
					
					B.SetListaHijos(self.ListaArbolesBloque[0])
					self.BloqueActivo[0] = False
					self.ListaArbolesBloque[0] = []
			
			R.SetHijo(B)
			#===============================================================
		else:
			
			#===============================================================
			if   self.BloqueActivo[0] == False: self.BloqueActivo[0] = True
			elif self.BloqueActivo[1] == False: self.BloqueActivo[1] = True
			elif self.BloqueActivo[2] == False: self.BloqueActivo[2] = True
			elif self.BloqueActivo[3] == False: self.BloqueActivo[3] = True
			elif self.BloqueActivo[4] == False: self.BloqueActivo[4] = True
			B = self.Bloque()
			#===============================================================
			
			if self.lexico.simbolo == 'print': self.Print()
			else:
				self.Asignacion(False)
				self.Comprueba(12);
			
			#===============================================================
			if self.BloqueActivo[0]:
			
				if self.BloqueActivo[4]:
					
					B.SetListaHijos(self.ListaArbolesBloque[4])
					self.BloqueActivo[4] = False
					self.ListaArbolesBloque[4] = []
					
				elif self.BloqueActivo[3]:
					
					B.SetListaHijos(self.ListaArbolesBloque[3])
					self.BloqueActivo[3] = False
					self.ListaArbolesBloque[3] = []
					
				elif self.BloqueActivo[2]:
					
					B.SetListaHijos(self.ListaArbolesBloque[2])
					self.BloqueActivo[2] = False
					self.ListaArbolesBloque[2] = []
					
				elif self.BloqueActivo[1]:
					
					B.SetListaHijos(self.ListaArbolesBloque[1])
					self.BloqueActivo[1] = False
					self.ListaArbolesBloque[1] = []
					
				elif self.BloqueActivo[0]:
					
					B.SetListaHijos(self.ListaArbolesBloque[0])
					self.BloqueActivo[0] = False
					self.ListaArbolesBloque[0] = []
			
			R.SetHijo(B)
			#===============================================================
			
		if self.lexico.simbolo == 'else':
			
			self.lexico.sigSimbolo()
			
			if self.lexico.tipo == 23:
					
				if   self.BloqueActivo[0] == False: self.BloqueActivo[0] = True
				elif self.BloqueActivo[1] == False: self.BloqueActivo[1] = True
				elif self.BloqueActivo[2] == False: self.BloqueActivo[2] = True
				elif self.BloqueActivo[3] == False: self.BloqueActivo[3] = True
				elif self.BloqueActivo[4] == False: self.BloqueActivo[4] = True
				
				E = self.ReservElse()
				
				self.lexico.sigSimbolo()
				self.A()
				self.Comprueba(24)
			
				#===============================================================
				
				if self.BloqueActivo[0]:
				
					if self.BloqueActivo[4]:
						
						E.SetListaHijos(self.ListaArbolesBloque[4])
						self.BloqueActivo[4] = False
						self.ListaArbolesBloque[4] = []
						
					elif self.BloqueActivo[3]:
						
						E.SetListaHijos(self.ListaArbolesBloque[3])
						self.BloqueActivo[3] = False
						self.ListaArbolesBloque[3] = []
						
					elif self.BloqueActivo[2]:
						
						E.SetListaHijos(self.ListaArbolesBloque[2])
						self.BloqueActivo[2] = False
						self.ListaArbolesBloque[2] = []
						
					elif self.BloqueActivo[1]:
						
						E.SetListaHijos(self.ListaArbolesBloque[1])
						self.BloqueActivo[1] = False
						self.ListaArbolesBloque[1] = []
						
					elif self.BloqueActivo[0]:
						
						E.SetListaHijos(self.ListaArbolesBloque[0])
						self.BloqueActivo[0] = False
						self.ListaArbolesBloque[0] = []
					
				#===============================================================
				
			else:
				
				#===============================================================
				if   self.BloqueActivo[0] == False: self.BloqueActivo[0] = True
				elif self.BloqueActivo[1] == False: self.BloqueActivo[1] = True
				elif self.BloqueActivo[2] == False: self.BloqueActivo[2] = True
				elif self.BloqueActivo[3] == False: self.BloqueActivo[3] = True
				elif self.BloqueActivo[4] == False: self.BloqueActivo[4] = True
				E = self.ReservElse()
				#===============================================================
				
				if self.lexico.simbolo == 'print': self.Print()
				else:
					self.Asignacion(False)
					self.Comprueba(12);
				
				#===============================================================
				
				if self.BloqueActivo[0]:
				
					if self.BloqueActivo[4]:
						
						E.SetListaHijos(self.ListaArbolesBloque[4])
						self.BloqueActivo[4] = False
						self.ListaArbolesBloque[4] = []
						
					elif self.BloqueActivo[3]:
						
						E.SetListaHijos(self.ListaArbolesBloque[3])
						self.BloqueActivo[3] = False
						self.ListaArbolesBloque[3] = []
						
					elif self.BloqueActivo[2]:
						
						E.SetListaHijos(self.ListaArbolesBloque[2])
						self.BloqueActivo[2] = False
						self.ListaArbolesBloque[2] = []
						
					elif self.BloqueActivo[1]:
						
						E.SetListaHijos(self.ListaArbolesBloque[1])
						self.BloqueActivo[1] = False
						self.ListaArbolesBloque[1] = []
						
					elif self.BloqueActivo[0]:
						
						E.SetListaHijos(self.ListaArbolesBloque[0])
						self.BloqueActivo[0] = False
						self.ListaArbolesBloque[0] = []
					
				#===============================================================
				
			#===============================================================
			R.SetHijo(E)
			#===============================================================
			
		#===============================================================
		if self.BloqueActivo[0]:
			
			if   self.BloqueActivo[4]: self.ListaArbolesBloque[4].append(R)
			elif self.BloqueActivo[3]: self.ListaArbolesBloque[3].append(R)
			elif self.BloqueActivo[2]: self.ListaArbolesBloque[2].append(R)
			elif self.BloqueActivo[1]: self.ListaArbolesBloque[1].append(R)
			elif self.BloqueActivo[0]: self.ListaArbolesBloque[0].append(R)
			
		else: self.ListaArboles.append(R)
		#===============================================================
	
	
	def While(self):
		
		self.lexico.sigSimbolo()
		
		self.Comprueba(11)
		#===============================================================
		P = self.ComparacionLogica()
		W = self.ReservWhile()
		W.SetHijo(P)
		#===============================================================
		self.Comprueba(22)
		
		if self.lexico.tipo == 23:
			
			#===============================================================
			
			if   self.BloqueActivo[0] == False: self.BloqueActivo[0] = True
			elif self.BloqueActivo[1] == False: self.BloqueActivo[1] = True
			elif self.BloqueActivo[2] == False: self.BloqueActivo[2] = True
			elif self.BloqueActivo[3] == False: self.BloqueActivo[3] = True
			elif self.BloqueActivo[4] == False: self.BloqueActivo[4] = True
			
			B = self.Bloque()
			#===============================================================
			
			self.lexico.sigSimbolo()
			self.A()
			self.Comprueba(24)
			
			#===============================================================
			if self.BloqueActivo[0]:
			
				if self.BloqueActivo[4]:
					
					B.SetListaHijos(self.ListaArbolesBloque[4])
					self.BloqueActivo[4] = False
					self.ListaArbolesBloque[4] = []
					
				elif self.BloqueActivo[3]:
					
					B.SetListaHijos(self.ListaArbolesBloque[3])
					self.BloqueActivo[3] = False
					self.ListaArbolesBloque[3] = []
					
				elif self.BloqueActivo[2]:
					
					B.SetListaHijos(self.ListaArbolesBloque[2])
					self.BloqueActivo[2] = False
					self.ListaArbolesBloque[2] = []
					
				elif self.BloqueActivo[1]:
					
					B.SetListaHijos(self.ListaArbolesBloque[1])
					self.BloqueActivo[1] = False
					self.ListaArbolesBloque[1] = []
					
				elif self.BloqueActivo[0]:
					
					B.SetListaHijos(self.ListaArbolesBloque[0])
					self.BloqueActivo[0] = False
					self.ListaArbolesBloque[0] = []
			
			W.SetHijo(B)
			#===============================================================
		
		#===============================================================
		if self.BloqueActivo[0]:
			
			if   self.BloqueActivo[4]: self.ListaArbolesBloque[4].append(W)
			elif self.BloqueActivo[3]: self.ListaArbolesBloque[3].append(W)
			elif self.BloqueActivo[2]: self.ListaArbolesBloque[2].append(W)
			elif self.BloqueActivo[1]: self.ListaArbolesBloque[1].append(W)
			elif self.BloqueActivo[0]: self.ListaArbolesBloque[0].append(W)
			
		else: self.ListaArboles.append(W)
		#===============================================================
	
	
	def DoWhile(self):
		
		self.lexico.sigSimbolo()
		
		self.Comprueba(23)
		self.A()
		self.Comprueba(24)
		
		if self.lexico.simbolo == 'while':
			
			self.lexico.sigSimbolo()
			self.Comprueba(11)
			self.ComparacionLogica()
			self.Comprueba(22)
			self.Comprueba(12)
			
		else: self.error()
	
	
	def For(self):
		
		self.lexico.sigSimbolo()
		
		self.Comprueba(11)
		self.Asignacion(False)
		self.Comprueba(12)
		
		if (self.lexico.tipo == 2 or self.lexico.tipo == 3 or self.lexico.tipo == 5) and not self.lexico.tipo in self.PalabReserv:
			
			self.lexico.sigSimbolo()
			
			if self.lexico.tipo == 14:
				
				self.lexico.sigSimbolo()
				
				if (self.lexico.tipo == 2 or self.lexico.tipo == 3 or self.lexico.tipo == 5) and not self.lexico.tipo in self.PalabReserv: self.lexico.sigSimbolo()
					
		self.Comprueba(12)
		
		self.Asignacion(False)
		
		self.Comprueba(22)
		
		if self.lexico.tipo == 23:
			
			self.lexico.sigSimbolo()
			self.A()
			self.Comprueba(24)
		
	
	def Expresion(self, Bool=True):	# Permite Recursividad
		
		#================================================================
		P = None
		Q = None
		Tipo = None
		xD = False
		Sign = False
		ArbolPila = []
		#================================================================
		
		if self.lexico.tipo == 9:
			
			Sign = self.lexico.simbolo
			self.lexico.sigSimbolo()
			
		if self.lexico.tipo == 11:
			
			self.lexico.sigSimbolo()
			#================================================================
			P = self.Expresion()
			ArbolPila.append(P)
			#================================================================
			self.Comprueba(22)
			xD = True
		
		# 2 = IDENTIFICADOR; 3 = ENTERO; 5 = FLOTANTE; 8 = CADENA = "Hola xD"
		if self.lexico.tipo == 2 or self.lexico.tipo == 3\
		or self.lexico.tipo == 5 or self.lexico.tipo == 8\
		or xD == True:
			
			if xD == False:
				
				#================================================================
				if   self.lexico.tipo == 2: P = self.Identi(None, self.lexico.simbolo)
				elif self.lexico.tipo == 3: P = self.Entero('i', self.lexico.simbolo)
				elif self.lexico.tipo == 5: P = self.Flotante('r', self.lexico.simbolo)
				elif self.lexico.tipo == 8: P = self.CadenaArb('c', self.lexico.simbolo)
				ArbolPila.append(P)
				#================================================================
				
				self.lexico.sigSimbolo()
				
			else: xD = False
			
			#================================================================
			if Sign != False:
				P = self.Signo(P, Sign)
				ArbolPila.pop()
				ArbolPila.append(P)
			Sign = False
			#================================================================
			
			while self.lexico.tipo == 9 or self.lexico.tipo == 10:
				
				#================================================================
				Tipo = (self.lexico.tipo, self.lexico.simbolo)
				
				ArbolPila.append(Tipo)
				#================================================================
				
				self.lexico.sigSimbolo()
				
				if self.lexico.tipo == 9:
					
					Sign = self.lexico.simbolo
					self.lexico.sigSimbolo()
					
				if self.lexico.tipo == 11:
					
					self.lexico.sigSimbolo()
					
					#================================================================
					Q = self.Expresion()
					ArbolPila.append(Q)
					#================================================================
					self.Comprueba(22)
					xD = True
				
				if self.lexico.tipo == 2 or self.lexico.tipo == 3\
				or self.lexico.tipo == 5 or self.lexico.tipo == 8\
				or xD == True:
					
					if xD == False:
						
						#================================================================
						if   self.lexico.tipo == 2:  Q = self.Identi(None, self.lexico.simbolo)
						elif self.lexico.tipo == 3:  Q = self.Entero('i', self.lexico.simbolo)
						elif self.lexico.tipo == 5:  Q = self.Flotante('r', self.lexico.simbolo)
						elif self.lexico.tipo == 8:  Q = self.CadenaArb('c', self.lexico.simbolo)
						ArbolPila.append(Q)
						#================================================================
						
						self.lexico.sigSimbolo()
						
						
					else: xD = False
					
				else: self.error()
				
				#================================================================
				if Sign != False:
					Q = self.Signo(Q, Sign)
					ArbolPila.pop()
					ArbolPila.append(Q)
				Sign = False
				
				if Bool:
					if   Tipo[0] == 9:  P = self.Suma(P, Q, Tipo[1])
					elif Tipo[0] == 10: P = self.Multi(P, Q, Tipo[1])
				#================================================================
				
		if Bool == False:	
			
			# ~ print('\n')
			
			ArbolPila = ArbolPila[::-1]
			
			P = ArbolPila.pop(0)
			
			# ~ print(P)
			
			if ArbolPila != []:
				
				Operador = ArbolPila.pop(0)
				Valor1   = ArbolPila.pop(0)
				
				# ~ print(Operador)
				# ~ print(Valor1)
				if   Operador[0] == 9:  P = self.Suma( Valor1, P, Operador[1])
				elif Operador[0] == 10: P = self.Multi(Valor1, P, Operador[1])
				
				Cont = 0
				for x in ArbolPila:
					
					# ~ print(x)
					
					if Cont % 2 == 0: Operador = x
					elif Cont % 2 == 1:
						
						Valor1 = x
						
						if   Operador[0] == 9:  P = self.Suma( Valor1, P, Operador[1])
						elif Operador[0] == 10: P = self.Multi(Valor1, P, Operador[1])
						
					Cont += 1
			
		return P
	
	
	
	def Print(self):
		
		self.lexico.sigSimbolo()
		
		self.Comprueba(11)
		
		#===============================================================
		P = self.Expresion()
		P = self.ExpresionArb(P)
		#===============================================================
		
		self.Comprueba(22)
		
		#===============================================================
		P = self.ReservPrint(P)
		
		if self.BloqueActivo[0]:
			
			if   self.BloqueActivo[4]: self.ListaArbolesBloque[4].append(P)
			elif self.BloqueActivo[3]: self.ListaArbolesBloque[3].append(P)
			elif self.BloqueActivo[2]: self.ListaArbolesBloque[2].append(P)
			elif self.BloqueActivo[1]: self.ListaArbolesBloque[1].append(P)
			elif self.BloqueActivo[0]: self.ListaArbolesBloque[0].append(P)
			
		else: self.ListaArboles.append(P)
		#===============================================================
		
		self.Comprueba(12)
	
	
	def ComparacionLogica(self):
		
		#================================================================
		P = self.ComparacionRelacional()
		#================================================================
		
		while self.lexico.tipo == 19:
			
			self.lexico.sigSimbolo()
			#================================================================
			Q = self.ComparacionRelacional()
			P = self.Logico(P, Q)
			#================================================================
		
		#================================================================
		return P
		#================================================================
	
	
	def ComparacionRelacional(self):
		
		#================================================================
		P = None
		Q = None
		Simbolo = None
		
		P = self.Expresion()
		#================================================================
		
		if self.lexico.tipo == 16:
			
			Simbolo = self.lexico.simbolo
			self.lexico.sigSimbolo()
			
			Simbolo += self.lexico.simbolo
			self.Comprueba(15)
			
			#================================================================
			Q = self.Expresion()
			P = self.Relacional(P, Q, Simbolo)
			#================================================================
		
		elif self.lexico.tipo == 14:
			
			Simbolo = self.lexico.simbolo
			
			self.lexico.sigSimbolo()
			
			#================================================================
			Q = self.Expresion()
			P = self.Relacional(P, Q, Simbolo)
			#================================================================
				
		#================================================================
		return P
		#================================================================
	
	
	def P(self): os.system('Pause > Nul')


