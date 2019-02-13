
from xml.dom import minidom
import os

#=======================================================================
#=======================================================================
#=======================================================================

Contador = 0
ContadorSignos = 0


class Expresion():
	
	def __init__(self):
		
		self.izq = None
		self.der = None

#=======================================================================
#=======================================================================
#=======================================================================

class Identificador(Expresion):
	
	def __init__(self, tipo, simbolo=None):
		
		Expresion.__init__(self)
		self.nombre = "ID"
		self.tipo = tipo
		self.simb = simbolo
		
	def __str__(self): return "Identificador"
	
	def GetDatos(self): return [self.izq, self.der]
	
	def SetTipo(self, Tipo): self.tipo = Tipo
	
	def generaCodigo(self, Root): return '\tpush _' + self.simb + '\n'


class Entero(Expresion):
	
	def __init__(self, tipo, simbolo=None):
		
		Expresion.__init__(self)
		self.nombre = "ENTERO"
		self.tipo = tipo
		self.simb = simbolo
		
	def __str__(self): return "Entero"
	
	def GetDatos(self): return [self.izq, self.der]
	
	def generaCodigo(self, Root): return '\tpush ' + self.simb + '\n'


class Flotante(Expresion):
	
	def __init__(self, tipo, simbolo=None):
		
		Expresion.__init__(self)
		self.nombre = "FLOTANTE"
		self.tipo = tipo
		self.simb = simbolo
		
	def __str__(self): return "Flotante"
	
	def GetDatos(self): return [self.izq, self.der]
	
	def generaCodigo(self, Root): return '\tpush ' + self.simb + '\n'


class Cadena(Expresion):
	
	def __init__(self, tipo, simbolo=None):
		
		Expresion.__init__(self)
		self.nombre = "CADENA"
		self.tipo = tipo
		self.simb = simbolo
		
	def __str__(self): return "Cadena"
	
	def GetDatos(self): return [self.izq, self.der]
	
	def generaCodigo(self, Root): return '\tpush ' + self.simb + '\n'


#=======================================================================
#=======================================================================
#=======================================================================

class Suma(Expresion):
	
	def __init__(self, izq, der, simbolo=None):
		
		Expresion.__init__(self)
		
		self.nombre = "SUMA"
		self.tipo = 9
		self.simb = simbolo
		self.izq = izq
		self.der = der
		
	def GetDatos(self): return [self.izq, self.der]
	
	def SetTipo(self, Tipo): self.tipo = Tipo
	
	def __str__(self): return "Suma"
	
	def generaCodigo(self, Root):
		
		Codigo = ''
		
		if Root != None:
			
			Izq, Der = Root.GetDatos()
			
			Codigo  = Izq.generaCodigo(Izq)
			Codigo += Der.generaCodigo(Der)
			
			# ~ Codigo += ' ===== SUMA =====\n'
			Codigo += '\n'
			if self.simb == '+':
				Codigo += '\tpop ebx\n\tpop eax\n\tadd eax, ebx\n\tpush eax\n'
			
			elif self.simb == '-':
				Codigo += '\tpop ebx\n\tpop eax\n\tsub eax, ebx\n\tpush eax\n'
			
			# ~ Codigo += ' ===== SUMA =====\n'
			Codigo += '\n'
			
		else: return None
		
		return Codigo



class Multi(Expresion):
	
	def __init__(self, izq, der, simbolo=None):
		
		Expresion.__init__(self)
		
		self.nombre = "MULT"
		self.tipo = 10
		self.simb = simbolo
		self.izq = izq
		self.der = der
		
	def GetDatos(self): return [self.izq, self.der]
	
	def SetTipo(self, Tipo): self.tipo = Tipo
	
	def __str__(self): return "Multiplicacion"
	
	def generaCodigo(self, Root):
		
		Codigo = ''
		
		if Root != None:
			
			Izq, Der = Root.GetDatos()
			
			Codigo  = Izq.generaCodigo(Izq)
			Codigo += Der.generaCodigo(Der)
			
			# ~ Codigo += ' ===== MULT =====\n'
			Codigo += '\n'
			if self.simb == '*':
				Codigo += '\tpop ebx\n\tpop eax\n\tmul ebx\n\tpush eax\n'
			
			elif self.simb == '/':
				Codigo += '\tpop ebx\n\tpop eax\n\txor edx, edx\n\tdiv ebx\n\tpush eax\n'
			# ~ Codigo += ' ===== MULT =====\n'
			Codigo += '\n'
			
		else: return None
		
		return Codigo



class Asignacion(Expresion):
	
	def __init__(self, izq, der):
		
		Expresion.__init__(self)
		
		self.nombre = "ASIGNACION"
		self.tipo = 15
		self.simb = None
		self.izq = izq
		self.der = der
		self.Pila = []
		
	def GetDatos(self): return [self.izq, self.der]
	
	def SetTipo(self, Tipo): self.tipo = Tipo
	
	def __str__(self): return "Asignacion"
	
	def generaCodigo(self, Root):
		
		Codigo = ''
		
		if Root != None:
			
			Izq, Der = Root.GetDatos()
			
			Codigo += Der.generaCodigo(Der) + '\tpop eax\n'
			
			Codigo += '\tmov _' + Izq.simb + ', eax\n'
			
		else: return None
		
		return Codigo
	
	def PostOrden(self, Root, XMLroot, Padre, TablaSimbolos):
		
		v1 = None
		v2 = None
		
		if Root != None:
			
			#===========================================================
			Hijo = XMLroot.createElement(str(Root.nombre))
			
			if  Root.nombre != 'ENTERO'   and Root.nombre != 'ID'\
			and Root.nombre != 'FLOTANTE' and Root.nombre != 'CADENA'\
			and Root.nombre != 'IMPRIME'  and Root.nombre != 'EXPRESION'\
			and Root.nombre != 'ASIGNACION':
				
				Hijo.setAttribute('value', str(Root.simb))
			
			if Root.nombre == 'ENTERO'   or Root.nombre == 'ID'\
			or Root.nombre == 'FLOTANTE' or Root.nombre == 'CADENA':
				
				Hijo.appendChild(XMLroot.createTextNode(str(Root.simb)))
			
			Padre.appendChild(Hijo)
			#===========================================================
			
			Izq, Der = Root.GetDatos()
			
			v1 = self.PostOrden(Izq, XMLroot, Hijo, TablaSimbolos)
			self.PostOrden(Der, XMLroot, Hijo, TablaSimbolos)
			
			if Root.nombre == 'ID':
				
				xD = True
				for x in TablaSimbolos:
					if Root.simb == x[0]:
						if x[0] == Root.simb: Root.tipo = x[1]
						xD = False
						break
				if xD:
					self.Pila.append([Root.simb, None])
					print('\t ???','\t',Root.nombre,'\t\t',Root.simb)
					return True
			else:
				if v1 == True:
					if Der.tipo == 'i':
						self.Pila[-1][1] = 'i'
						Izq.SetTipo('i')
					elif Der.tipo == 'r':
						self.Pila[-1][1] = 'r'
						Izq.SetTipo('r')
					elif Der.tipo == 'c':
						self.Pila[-1][1] = 'c'
						Izq.SetTipo('c')
				
				if Root.nombre == 'SIGNO' and Izq != None: Root.tipo = Izq.tipo
				
				if Root.nombre == 'ASIGNACION':
					if Izq != None and Der != None:
						if   Izq.tipo == 'i' and Der.tipo == 'i': Root.tipo = 'v'
						elif Izq.tipo == 'r' and Der.tipo == 'r': Root.tipo = 'v'
						elif Izq.tipo == 'c' and Der.tipo == 'c': Root.tipo = 'v'
						else: Root.tipo = 'e'
				else:
					if Izq != None and Der != None:
						if   Izq.tipo == 'i' and Der.tipo == 'i': Root.tipo = 'i'
						elif Izq.tipo == 'r' and Der.tipo == 'r': Root.tipo = 'r'
						elif Izq.tipo == 'c' and Der.tipo == 'c': Root.tipo = 'c'
						else: Root.tipo = 'e'
			
			print('\t', Root.tipo,'\t',Root.nombre,'\t\t',Root.simb)
			
		else: return None
		
		return Root.tipo

#=======================================================================
#=======================================================================
#=======================================================================


class Relacional(Expresion):
	
	def __init__(self, izq, der, simbolo=None):
		
		Expresion.__init__(self)
		
		self.nombre = "EXPRESION"
		self.tipo = 14
		self.simb = simbolo
		self.izq = izq
		self.der = der
		
	def GetDatos(self): return [self.izq, self.der]
	
	def __str__(self): return "Expresion Relacional"
	
	def EtiquetaFalso(self): return 'Falso' + str(Contador)
		
	def EtiquetaFin(self): return 'FinComp' + str(Contador)
	
	def TipoSalto(self):
		
		if   self.simb == '<': return 'jnl'
		elif self.simb == '<=': return 'jnle'
		elif self.simb == '>': return 'jng'
		elif self.simb == '>=': return 'jnge'
		elif self.simb == '==': return 'jne'
		elif self.simb == '!=': return 'je'
	
	def generaCodigo(self, Root, Padre=None):
		
		Codigo = ''
		
		if Root != None:
			
			if Padre == None:
				
				Izq, Der = Root.GetDatos()
				
				Codigo += Izq.generaCodigo(Izq)
				Codigo += Der.generaCodigo(Der)
				
				Codigo += '\tpop ebx\n\tpop eax\n\tcmp eax, ebx\n'
				Codigo += '\t' + self.TipoSalto() + ' ' + self.EtiquetaFalso() + '\n'
				Codigo += '\tpush 1\n'
				Codigo += '\tjmp ' + self.EtiquetaFin() + '\n'
				Codigo += self.EtiquetaFalso() + ':\n'
				Codigo += '\tpush 0\n'
				Codigo += '\tjmp Else{}\n'.format(Contador)
				Codigo += self.EtiquetaFin() + ':\n'
			
			else:
				
				Izq, Der = Root.GetDatos()
				
				Codigo += Izq.generaCodigo(Izq)
				Codigo += Der.generaCodigo(Der)
				
				Codigo += '\tpop ebx\n\tpop eax\n\tcmp eax, ebx\n'
				Codigo += '\t' + self.TipoSalto() + ' ' + 'FinMientras{}\n'.format(Contador)

		else: return None
		
		return Codigo
	


class Logico(Expresion):
	
	def __init__(self, izq, der, simbolo=None):
		
		Expresion.__init__(self)
		
		self.nombre = "LOGICO"
		self.tipo = 19
		self.simb = simbolo
		self.izq = izq
		self.der = der
		
	def GetDatos(self): return [self.izq, self.der]
	
	def __str__(self): return "Expresion Logica"
	
	def generaCodigo(self, Root): return ''
	


class ReservWhile(Expresion):
	
	def __init__(self):
		
		Expresion.__init__(self)
		
		self.nombre = "MIENTRAS"
		self.tipo = None
		self.simb = None
		self.Lista = []
		self.Pila = []
		self.Bloque = 0
		
	def SetListaHijos(self, Lista): self.Lista = Lista
	
	def SetHijo(self, Hijo): self.Lista.append(Hijo)
	
	def GetDatos(self): return self.Lista
	
	def __str__(self): return "While"
	
	def generaCodigo(self, Root):
		
		global Contador
		
		Codigo = ''
		
		if Root != None:
			
			Contador += 1
			self.Bloque = Contador
			
			Izq, Der = Root.GetDatos()
			
			Codigo += 'Mientras{}:\n'.format(Contador)
			
			Codigo += Izq.generaCodigo(Izq, Root)
			Codigo += Der.generaCodigo(Der, Root, Contador)
			
		else: return None
		
		Codigo += 'FinMientras{}:\n'.format(self.Bloque)
		
		return Codigo
	
	def PostOrden(self, Root, XMLroot, Padre, Anterior, TablaSimbolos):
		
		if Root != None:
			
			#===========================================================
			Nombre = Root.nombre
			
			Hijo = XMLroot.createElement(str(Nombre))
			
			if  Nombre != 'ENTERO'     and Nombre != 'ID'\
			and Nombre != 'FLOTANTE'   and Nombre != 'CADENA'\
			and Nombre != 'ASIGNACION' and Nombre != 'IMPRIME'\
			and Nombre != 'SI' and Nombre != 'BLOQUE' and Nombre != 'OTRO'\
			and Nombre != 'MIENTRAS':
				
				if Nombre != 'EXPRESION': Hijo.setAttribute('value', str(Root.simb))
				else:
					if Root.simb != None: Hijo.setAttribute('value', str(Root.simb))
				
			if Nombre == 'ENTERO'   or Nombre == 'ID'\
			or Nombre == 'FLOTANTE' or Nombre == 'CADENA':
				
				Hijo.appendChild(XMLroot.createTextNode(str(Root.simb)))
			
			Padre.appendChild(Hijo)
			#===========================================================
			
			
			if Nombre == 'SI' or Nombre == 'BLOQUE'\
			or Nombre == 'OTRO' or Nombre == 'MIENTRAS':
				
				for x in Root.GetDatos():
					
					if 'e' == self.PostOrden(x, XMLroot, Hijo, Nombre, TablaSimbolos): return 'e'
					
					if   Nombre == 'MIENTRAS':
						
						if x.nombre == 'EXPRESION':
							
							if   x.tipo == 'i': Root.tipo = 'i'
							elif x.tipo == 'r': Root.tipo = 'r'
							elif x.tipo == 'c': Root.tipo = 'c'
							else: Root.tipo = 'e'
						
						elif x.nombre == 'BLOQUE':
							
							if x.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
					
					elif Nombre == 'SI':
						
						if x.nombre == 'EXPRESION':
							
							if x.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
						
						elif x.nombre == 'BLOQUE':
							
							if x.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
							
						elif x.nombre == 'OTRO':
							
							if x.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
						
					elif Nombre == 'BLOQUE':
						
						if x.tipo == 'e': Root.tipo = 'e'
						else: Root.tipo = 'v'
					
					elif Nombre == 'OTRO':
						
						if x.tipo == 'e': Root.tipo = 'e'
						else: Root.tipo = 'v'
				
				if Root.GetDatos() == []:
					if Root.nombre == 'BLOQUE': Root.tipo = 'v'
					
				print('\t', Root.tipo,'\t',Nombre)
					
			else:
				
				Izq, Der = Root.GetDatos()
				
				if 'e' == self.PostOrden(Izq, XMLroot, Hijo, Nombre, TablaSimbolos): return 'e'
				if 'e' == self.PostOrden(Der, XMLroot, Hijo, Nombre, TablaSimbolos): return 'e'
				
				if Anterior == 'ASIGNACION':
					
					if Nombre == 'ID':
						
						xD = False
						
						for x in TablaSimbolos:
							if Root.simb == x[0]:
								Root.tipo = x[1]
								xD = True
								break
								
						if xD == False:
							for x in self.Pila:
								if Root.simb == x[0]:
									Root.tipo = x[1]
									xD = True
									break
								
							if xD == False:
								self.Pila.append([Root.simb, None])
								print('\t ???','\t',Nombre,'\t\t',Root.simb)
								return
					
				else:
					# ~ print(Nombre)
					
					if Nombre == 'EXPRESION':
						
						if Izq != None and Der != None:
							if Izq.tipo == 'e' or Der.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
						elif Izq != None:
							if   Izq.tipo == 'i': Root.tipo = 'i'
							elif Izq.tipo == 'r': Root.tipo = 'r'
							elif Izq.tipo == 'c': Root.tipo = 'c'
							else: Root.tipo = 'e'
					
					if Nombre == 'IMPRIME':
						if Izq != None:
							if   Izq.tipo == 'i': Root.tipo = 'v'
							elif Izq.tipo == 'r': Root.tipo = 'v'
							elif Izq.tipo == 'c': Root.tipo = 'v'
							else: Root.tipo = 'e'
					
					if Nombre == 'SIGNO' and Izq != None: Root.tipo = Izq.tipo
					
					if Nombre == 'ASIGNACION':
						
						# ~ if Izq != None: print(Izq.simb)
						# ~ if Der != None: print(Der.simb)
						PilaTemp = TablaSimbolos+ self.Pila
						if Der.tipo == 'i':
							PilaTemp[-1][1] = 'i'
							Izq.SetTipo('i')
						elif Der.tipo == 'r':
							PilaTemp[-1][1] = 'r'
							Izq.SetTipo('r')
						elif Der.tipo == 'c':
							PilaTemp[-1][1] = 'c'
							Izq.SetTipo('c')
							
					
					if Nombre == 'ID':
						
						xD = False
						for x in TablaSimbolos:
							if Root.simb == x[0]:
								Root.tipo = x[1]
								xD = True
								break
								
						if xD == False:
							for x in self.Pila:
								if Root.simb == x[0]:
									Root.tipo = x[1]
									xD = True
									break
							
							if xD == False: Root.tipo = 'e'
				
				
				if Root.nombre == 'SIGNO' and Izq != None: Root.tipo = Izq.tipo
				
				if Nombre != 'EXPRESION':
						
					if Izq != None and Der != None:
						
						if   Izq.tipo == 'i' and Der.tipo == 'i': Root.tipo = 'i'
						elif Izq.tipo == 'r' and Der.tipo == 'r': Root.tipo = 'r'
						elif Izq.tipo == 'c' and Der.tipo == 'c': Root.tipo = 'c'
						else: Root.tipo = 'e'
					
					
				
					
				print('\t', Root.tipo,'\t',Nombre,'\t\t',Root.simb)
				
		else: return None
	
		return Root.tipo



class ReservIf(Expresion):
	
	def __init__(self):
		
		Expresion.__init__(self)
		
		self.nombre = "SI"
		self.tipo = None
		self.simb = None
		self.Lista = []
		self.Pila = []
		self.PilaElse = []
		self.BloqueElse = False
		self.Bloque = 0
		
	def SetListaHijos(self, Lista): self.Lista = Lista
	
	def SetHijo(self, Hijo): self.Lista.append(Hijo)
	
	# ~ def SetPila(self, TablaSimbolos): self.Pila = TablaSimbolos
	
	def GetDatos(self): return self.Lista
	
	def __str__(self): return "If"
	
	def generaCodigo(self, Root, Padre=None):
		
		global Contador
		
		Codigo = ''
		
		if Root != None:
			
			Contador += 1
			self.Bloque = Contador
			
			for x in Root.GetDatos():
				
				if str(x) == 'Bloque': Codigo += x.generaCodigo(x, Cnt=Contador)
				else: Codigo += x.generaCodigo(x)
			
		else: return None
		
		Codigo += 'FinElse{}:\n'.format(self.Bloque)
		
		return Codigo
	
	def PostOrden(self, Root, XMLroot, Padre, Anterior, TablaSimbolos):
		
		if Root != None:
			xD = None
			#===========================================================
			Nombre = Root.nombre
			
			Hijo = XMLroot.createElement(str(Nombre))
			
			if  Nombre != 'ENTERO'     and Nombre != 'ID'\
			and Nombre != 'FLOTANTE'   and Nombre != 'CADENA'\
			and Nombre != 'ASIGNACION' and Nombre != 'IMPRIME'\
			and Nombre != 'SI' and Nombre != 'BLOQUE' and Nombre != 'OTRO'\
			and Nombre != 'MIENTRAS':
				
				if Nombre != 'EXPRESION': Hijo.setAttribute('value', str(Root.simb))
				else:
					if Root.simb != None: Hijo.setAttribute('value', str(Root.simb))
				
			if Nombre == 'ENTERO'   or Nombre == 'ID'\
			or Nombre == 'FLOTANTE' or Nombre == 'CADENA':
				
				Hijo.appendChild(XMLroot.createTextNode(str(Root.simb)))
			
			Padre.appendChild(Hijo)
			#===========================================================
			
			if Nombre == 'SI' or Nombre == 'BLOQUE'\
			or Nombre == 'OTRO' or Nombre == 'MIENTRAS':
				
				for x in Root.GetDatos():
					
					if 'e' == self.PostOrden(x, XMLroot, Hijo, Nombre, TablaSimbolos): return 'e'
					
					if   Nombre == 'MIENTRAS':
						
						if x.nombre == 'EXPRESION':
							
							if   x.tipo == 'i': Root.tipo = 'i'
							elif x.tipo == 'r': Root.tipo = 'r'
							elif x.tipo == 'c': Root.tipo = 'c'
							else: Root.tipo = 'e'
						
						elif x.nombre == 'BLOQUE':
							
							if x.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
					
					elif Nombre == 'SI':
						
						if x.nombre == 'EXPRESION':
							
							if x.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
						
						elif x.nombre == 'BLOQUE':
							
							if x.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
							
						elif x.nombre == 'OTRO':
							
							if x.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
						
					elif Nombre == 'BLOQUE':
						
						if x.tipo == 'e': Root.tipo = 'e'
						else: Root.tipo = 'v'
					
					elif Nombre == 'OTRO':
						
						if x.tipo == 'e': Root.tipo = 'e'
						else: Root.tipo = 'v'
				
				if Root.GetDatos() == []:
					if Root.nombre == 'BLOQUE': Root.tipo = 'v'
					
				print('\t', Root.tipo,'\t',Nombre)
					
			else:
				
				Izq, Der = Root.GetDatos()
				
				if 'e' == self.PostOrden(Izq, XMLroot, Hijo, Nombre, TablaSimbolos): return 'e'
				if 'e' == self.PostOrden(Der, XMLroot, Hijo, Nombre, TablaSimbolos): return 'e'
				
				if Anterior == 'ASIGNACION':
					
					if Nombre == 'ID':
						
						xD = False
						
						for x in TablaSimbolos:
							if Root.simb == x[0]:
								Root.tipo = x[1]
								xD = True
								break
								
						if xD == False:
							for x in self.Pila:
								if Root.simb == x[0]:
									Root.tipo = x[1]
									xD = True
									break
								
							if xD == False:
								self.Pila.append([Root.simb, None])
								print('\t ???','\t',Nombre,'\t\t',Root.simb)
								return
					
				else:
					# ~ print(Nombre)
					
					if Nombre == 'EXPRESION':
						
						if Izq != None and Der != None:
							if Izq.tipo == 'e' or Der.tipo == 'e': Root.tipo = 'e'
							else: Root.tipo = 'v'
						elif Izq != None:
							if   Izq.tipo == 'i': Root.tipo = 'i'
							elif Izq.tipo == 'r': Root.tipo = 'r'
							elif Izq.tipo == 'c': Root.tipo = 'c'
							else: Root.tipo = 'e'
					
					if Nombre == 'IMPRIME':
						if Izq != None:
							if   Izq.tipo == 'i': Root.tipo = 'v'
							elif Izq.tipo == 'r': Root.tipo = 'v'
							elif Izq.tipo == 'c': Root.tipo = 'v'
							else: Root.tipo = 'e'
					
					if Nombre == 'SIGNO' and Izq != None: Root.tipo = Izq.tipo
					
					if Nombre == 'ASIGNACION':
						
						# ~ if Izq != None: print(Izq.simb)
						# ~ if Der != None: print(Der.simb)
						PilaTemp = TablaSimbolos+ self.Pila
						if Der.tipo == 'i':
							PilaTemp[-1][1] = 'i'
							Izq.SetTipo('i')
						elif Der.tipo == 'r':
							PilaTemp[-1][1] = 'r'
							Izq.SetTipo('r')
						elif Der.tipo == 'c':
							PilaTemp[-1][1] = 'c'
							Izq.SetTipo('c')
							
					
					if Nombre == 'ID':
						
						xD = False
						for x in TablaSimbolos:
							if Root.simb == x[0]:
								Root.tipo = x[1]
								xD = True
								break
								
						if xD == False:
							for x in self.Pila:
								if Root.simb == x[0]:
									Root.tipo = x[1]
									xD = True
									break
							
							if xD == False: Root.tipo = 'e'
				
				
				if Root.nombre == 'SIGNO' and Izq != None: Root.tipo = Izq.tipo
				
				if Nombre != 'EXPRESION':
						
					if Izq != None and Der != None:
						
						if   Izq.tipo == 'i' and Der.tipo == 'i': Root.tipo = 'i'
						elif Izq.tipo == 'r' and Der.tipo == 'r': Root.tipo = 'r'
						elif Izq.tipo == 'c' and Der.tipo == 'c': Root.tipo = 'c'
						else: Root.tipo = 'e'
					
					
				
					
				print('\t', Root.tipo,'\t',Nombre,'\t\t',Root.simb)
				
		else: return None
		
		return Root.tipo


class ReservElse(Expresion):
	
	def __init__(self):
		
		Expresion.__init__(self)
		
		self.nombre = "OTRO"
		self.tipo = None
		self.simb = None
		self.Lista = []
		
	def SetListaHijos(self, Lista): self.Lista = Lista
	
	def SetHijo(self, Hijo): self.Lista.append(Hijo)
	
	def GetDatos(self): return self.Lista
	
	def __str__(self): return "Else"
	
	def generaCodigo(self, Root):
		
		Codigo = ''
		
		if Root != None:
			
			for x in Root.GetDatos():
				
				Codigo += x.generaCodigo(x)
			
		else: return None
		
		return Codigo
		


class ReservPrint(Expresion):
	
	def __init__(self, izq):
		
		Expresion.__init__(self)
		
		self.nombre = "IMPRIME"
		self.tipo = None
		self.simb = None
		self.izq = izq
		self.der = None
		self.Pila = []
		
	def GetDatos(self): return [self.izq, self.der]
	
	def __str__(self): return "Print"
	
	def generaCodigo(self, Root):
		
		Codigo = ''
		
		if Root != None:
			
			Izq, Der = Root.GetDatos()
			
			Codigo  = Izq.generaCodigo(Izq)
			
			Codigo += '\tpop eax\n\tprint str$(eax)\n'
			Codigo += '\tprint chr$(10)\n'
			
		else: return None
		
		return Codigo
		
		
	
	def PostOrden(self, Root, XMLroot, Padre, TablaSimbolos):
		
		if Root != None:
			
			#===========================================================
			Nombre = Root.nombre
			
			Hijo = XMLroot.createElement(str(Nombre))
			
			if  Nombre != 'ENTERO'     and Nombre != 'ID'\
			and Nombre != 'FLOTANTE'   and Nombre != 'CADENA'\
			and Nombre != 'ASIGNACION' and Nombre != 'IMPRIME'\
			and Nombre != 'SI' and Nombre != 'BLOQUE' and Nombre != 'OTRO'\
			and Nombre != 'MIENTRAS':
				
				# ~ print(Nombre, Root.simb, (Nombre == 'EXPRESION' and Root.simb != None))
				
				if Nombre != 'EXPRESION': Hijo.setAttribute('value', str(Root.simb))
				else:
					if Root.simb != None: Hijo.setAttribute('value', str(Root.simb))
				
			if Nombre == 'ENTERO'   or Nombre == 'ID'\
			or Nombre == 'FLOTANTE' or Nombre == 'CADENA':
				
				Hijo.appendChild(XMLroot.createTextNode(str(Root.simb)))
			
			Padre.appendChild(Hijo)
			#===========================================================
			
			Izq, Der = Root.GetDatos()
			
			self.PostOrden(Izq, XMLroot, Hijo, TablaSimbolos)
			self.PostOrden(Der, XMLroot, Hijo, TablaSimbolos)
			
			if Root.nombre == 'ID':
				xD = False
				for x in TablaSimbolos:
					if x[0] == Root.simb:
						Root.tipo = x[1]
						xD = True
				if xD == False: Root.tipo = 'e'
			
			if Root.nombre == 'SIGNO' and Izq != None: Root.tipo = Izq.tipo
			
			if Izq != None and Der != None:
				if   Izq.tipo == 'i' and Der.tipo == 'i': Root.tipo = 'i'
				elif Izq.tipo == 'r' and Der.tipo == 'r': Root.tipo = 'r'
				elif Izq.tipo == 'c' and Der.tipo == 'c': Root.tipo = 'c'
				else: Root.tipo = 'e'
			
			if Root.nombre == 'EXPRESION':
				if Izq != None:
					if   Izq.tipo == 'i': Root.tipo = 'i'
					elif Izq.tipo == 'r': Root.tipo = 'r'
					elif Izq.tipo == 'c': Root.tipo = 'c'
					else: Root.tipo = 'e'
			
			if Root.nombre == 'IMPRIME':
				if Izq != None:
					if   Izq.tipo == 'i': Root.tipo = 'v'
					elif Izq.tipo == 'r': Root.tipo = 'v'
					elif Izq.tipo == 'c': Root.tipo = 'v'
					else: Root.tipo = 'e'
			
			print('\t', Root.tipo,'\t',Root.nombre,'\t\t',Root.simb)
			
		else: return None
		
		return Root.tipo


class Separador(Expresion):
	
	def __init__(self, izq, der):
		
		Expresion.__init__(self)
		
		self.nombre = "Separador"
		self.tipo = None
		self.izq = izq
		self.der = der
		
	def GetDatos(self): return [self.izq, self.der]
	
	def __str__(self): return "Separador"
	
	def generaCodigo(self, Root): return ''
	


class Signo(Expresion):
	
	def __init__(self, izq, simbolo=None):
		
		Expresion.__init__(self)
		
		self.nombre = "SIGNO"
		self.tipo = None
		self.simb = simbolo
		self.izq = izq
		self.der = None
		
	def GetDatos(self): return [self.izq, self.der]
	
	def generaCodigo(self, Root):
		
		global ContadorSignos
		
		Codigo = ''
		
		if Root != None:
			
			Izq, Der = Root.GetDatos()
			
			Codigo += Izq.generaCodigo(Izq)
			
			ContadorSignos += 1
			
			if self.simb == '+':
				
				Codigo += '\t;#========={}=========\n'.format(self.simb)
				Codigo += '\tpop eax\n'
				Codigo += '\tcmp eax, 0\n'
				Codigo += '\tjnl FinSigno{}\n'.format(ContadorSignos)
				Codigo += '\tpush eax\n'
				Codigo += '\tpop ebx\n'
				Codigo += '\tmov eax, -1\n'
				Codigo += '\tmul ebx\n'
				Codigo += 'FinSigno{}:\n'.format(ContadorSignos)
				Codigo += '\tpush eax\n'
				Codigo += '\t;#===================\n'
				
			else:
					
				Codigo += '\t;#========={}=========\n'.format(self.simb)
				Codigo += '\tpop eax\n'
				Codigo += '\tcmp eax, 0\n'
				Codigo += '\tjl FinSigno{}\n'.format(ContadorSignos)
				Codigo += '\tpush eax\n'
				Codigo += '\tpop ebx\n'
				Codigo += '\tmov eax, -1\n'
				Codigo += '\tmul ebx\n'
				Codigo += 'FinSigno{}:\n'.format(ContadorSignos)
				Codigo += '\tpush eax\n'
				Codigo += '\t;#===================\n'
				
		else: return None
		
		return Codigo
	
	def __str__(self): return "Signo"
	


class Expre(Expresion):
	
	def __init__(self, izq, simbolo=None):
		
		Expresion.__init__(self)
		
		self.nombre = "EXPRESION"
		self.tipo = None
		self.simb = simbolo
		self.izq = izq
		self.der = None
		
	def GetDatos(self): return [self.izq, self.der]
	
	def __str__(self): return "Expresion"
	
	def generaCodigo(self, Root):
		
		Codigo = ''
		
		if Root != None:
			
			Izq, Der = Root.GetDatos()
			
			Codigo += Izq.generaCodigo(Izq)
			
		else: return None
		
		return Codigo
	


class Bloque(Expresion):
	
	def __init__(self):
		
		Expresion.__init__(self)
		
		self.nombre = "BLOQUE"
		self.tipo = None
		self.simb = None
		self.Lista = []
		
	def SetListaHijos(self, Lista): self.Lista = Lista
	
	def SetHijo(self, Hijo): self.Lista.append(Hijo)
	
	def GetDatos(self): return self.Lista
	
	def __str__(self): return "Bloque"
	
	def generaCodigo(self, Root, Padre=None, Cnt=None):
		
		Codigo = ''
		
		if Root != None:
			
			for x in Root.GetDatos():
				
				Codigo += x.generaCodigo(x)
				
			if Padre == None: Codigo += '\tjmp FinElse{}\n'.format(Cnt)
			else: Codigo += '\tjmp Mientras{}\n'.format(Cnt)
			
		else: return None
		
		if Padre == None:
			Codigo += 'Else{}:\n'.format(Cnt)
			
		return Codigo
	



