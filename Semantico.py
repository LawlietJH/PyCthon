# -*- coding: utf-8 -*-

from xml.dom import minidom
import Sintactico
import Arbol


class Semantico():
	
	def __init__(self):
		
		self.TablaSimbolos = []
		self.Codigo = ''
		self.Salida = 1
		
		self.Troot = minidom.Document()
		self.Root = self.Troot.createElement('PROGRAMA')
		self.Troot.appendChild(self.Root)
		
		self.sintactico = Sintactico.Sintactico()
		
	
	def Analiza(self):
		
		self.sintactico.analiza()
		
		print('\n\n')
		
		for x in self.sintactico.ListaArboles:
			
			self.Codigo += '\n\n\t; {} =======\n\n'.format(str(x))
			
			if str(x) == 'If' or str(x) == 'While':
				
				# ~ x.SetPila(self.TablaSimbolos)
				if x.PostOrden(x, self.Troot, self.Root, None, self.TablaSimbolos) == 'e':
					self.Salida = 0
					for y in x.Pila: self.TablaSimbolos.append(y)
					break
			else:
				if x.PostOrden(x, self.Troot, self.Root, self.TablaSimbolos) == 'e':
					self.Salida = 0
					for y in x.Pila: self.TablaSimbolos.append(y)
					break
			
			self.Codigo += x.generaCodigo(x)
			
			# ~ if str(x) == 'If' or str(x) == 'While':
				
				# ~ Arbol.Contador += 10
			
			for y in x.Pila: self.TablaSimbolos.append(y)
			
			print('\n\n')
		
		print('\n')
		for x in self.TablaSimbolos: print(x)
		
		print('\n\n\n\t Salida: ', self.Salida)
		# ~ Archivo = open('salida.txt','w')
		# ~ Cadena = Archivo.write(str(self.Salida))
		# ~ Archivo.close()
		
		xml_str = self.Troot.toprettyxml(indent='').replace('<?xml version="1.0" ?>\n','')
		
		# ~ with open('salida.xml','w') as File: File.write(xml_str); File.close()
		
		return self.TablaSimbolos, self.Codigo


