import sys

def start():
    print('''
Iniciando programa...
Ingrese 'help()' o 'help(<comando>)' para obtener ayuda.
Ingrese 'exit()' para salir.
    ''')
    consoleOptions = {          
                '__builtins__':None,
                'help':assist,
                'exit':halt,
                'create':consoleCreate,
                # 'send':consoleSend,
                # 'receive':consoleReceive,
                # 'display':consoleDisplay,
                # 'execFromFile':consoleBatch 
                }
    while True:
        try:
            req = input("> ")
            exec(req, consoleOptions)
        except Exception as e:
            print("No se pudo reconocer el comando recibido. Asegurese de no haber cometido algun error en la escritura del comando o alguno de los parametros o ingrese 'help()' para obtener mas informacion.")
            print(e)
    print("Saliendo del programa...")


def assist(fun=None):
    '''Puedes llamar a esta funcion para obtener información del programa o cualquier comando si se provee.'''
    print("was this called?")
    try:
        if(fun):
            print(fun.__doc__)
        else:
            print("Esta el la lista de comandos y demás")
    except Exception as e:
        print(e)

def halt():
    '''halt() detiene la ejecución del programa.'''
    print("Cerrando programa...")
    sys.exit(0)

def consoleCreate():
    '''<Syntax> Con esta funcion puedes crear un proceso.'''
    pass

if __name__ == "__main__":
    start()