
import Arbol


def Save(TablaSimbolos, Codigo):
	
	Simbolos = ''
	
	for x in TablaSimbolos:
		
		Simbolos += '\t_' + x[0] + ' dword 0\n'
		
	Cadena  = '.386\n'
	Cadena += '.model flat, stdcall\n'
	Cadena += 'option casemap:none ;labels are case-sensitive now\n\n'
	Cadena += '\tinclude \masm32\macros\macros.asm\n'
	Cadena += '\tinclude \masm32\include\masm32.inc\n'
	Cadena += '\tinclude \masm32\include\kernel32.inc\n\n'
	Cadena += '\tincludelib \masm32\lib\masm32.lib\n'
	Cadena += '\tincludelib \masm32\lib\kernel32.lib\n'
	Cadena += '.data?\n'
	Cadena += '\n'
	Cadena += '.data\n'
	Cadena += '{}'.format(Simbolos)
	Cadena += '.code\n'
	Cadena += 'inicio:\n'
	Cadena += '{}\n'.format(Codigo)
	Cadena += '\texit\n'
	Cadena += 'end inicio\n'
	
	return Cadena
	
	

