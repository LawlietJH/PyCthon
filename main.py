# -*- coding: utf-8 -*-

import Semantico
import GeneraCodigo




def Main():
	
	semantico = Semantico.Semantico()
	
	TablaSimbolos, Codigo = semantico.Analiza()
	
	Salida = GeneraCodigo.Save(TablaSimbolos, Codigo)
	
	print('\n\n#================================')
	print(' Generación de Código (MASM):')
	print('#================================\n')
	print(Salida)
	print('#================================')
	
	with open('salida.txt','w') as Archivo: Archivo.write(Salida)
	Archivo.close()



if __name__ == "__main__":
	
	Main()
	

