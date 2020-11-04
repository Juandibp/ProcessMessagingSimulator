import sys
import pprint

userTerms = {
    "send":"metodo de envio",
    "recieve":"metodo de recepcion",
    "addressing": "direccionamiento",
    "direct":"directo",
    "indirect":"indirecto",
    "blocking":"blocking",
    "non-blocking":"non-blocking",
    "arrival-test":"prueba de llegada",
    "static":"estatico",
    "dynamic":"dinamico",
    "format":"formato",
    "content":"contenido",
    "length":"largo de mensajes",
    "queueMethod":"metodo de manejo de colas",
    "fifo":"primero que entra, primero que sale",
    "priority":"prioridad",
    "fixed":"fijo",
    "explicit": "explicito",
    "implicit": "implicito"
}

def start():
    config = consoleStartingSequence()
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
    try:
        if(fun):
            print(fun.__doc__)
        else:
            # TODO Que esto en realidad imprima la lista de comandos :v
            print("Esta el la lista de comandos y demás")
    except Exception as e:
        print(e)

def reqNumberInput(min:int = None , max:int = None) -> int:
    '''Esta funcion interna le pide al usuario un numero'''
    try:
        selected = int(input("Seleccione una opcion: "))
        if min and min > selected:
            print("La seleccion tiene que ser mayor o igual que " + str(min) + ". Intente de nuevo.")
            return reqNumberInput(min, max)
        if max and max < selected:
            print("La seleccion tiene que ser menor o igual que " + str(max) + ". Intente de nuevo.")
            return reqNumberInput(min, max)
        return selected
    except:
        print("La seleccion que hizo no es valida. Intente de nuevo.")
        return reqNumberInput(min, max)

def consoleStartingSequence():
    '''Esta funcion permite seleccionar la configuracion inicial del programa'''

    print('\nAntes de iniciar necesitamos hacer las configuraciones iniciales.')

    configOptions = {
        "send": ["blocking", "non-blocking"],
        "recieve": ["blocking","non-blocking","arrival-test"],
        "addressing": {
            "direct": {
                "send":"send",
                "recieve":["explicit", "implicit"]
            },
            "indirect":["static","dynamic"],
        },
        "format":{
            "content":"content",
            "length":["fixed","dynamic"]
        },
        "queueMethod":["fifo","priority"]
    }
    selectedOptions = {}
    for (key, value) in configOptions.items():
        print("\nEstas son las opciones para configurar el " + userTerms[key])
        if isinstance(value, list):
            for i in range(len(value)):
                print("~|",i, userTerms[value[i]])            
            sel = reqNumberInput(0, len(value) - 1)
            selectedOptions[key] = value[sel]
        elif isinstance(value, dict):
            selectedOptions[key] = getOptionPath(value, [key])
    print("Esta es la configuración seleccionada:")
    pprint.pprint(selectedOptions)
    print("\nIniciando programa..."+
          "\nIngrese 'help()' o 'help(<comando>)' para obtener ayuda."+
          "\nIngrese 'exit()' para salir.\n")
    return "hola"


def getOptionPath(opt:dict, route:list = []) -> list:
    '''Recorre un diccionario devolviendo una ruta a un elemento.'''
    itms = list(opt.items())
    for i in range(len(itms)):
        # primero tiene que elegir cual de los valores quiere, hay que imprimirlos
        print("~|",i,userTerms[itms[i][0]])
    selected = reqNumberInput(0, len(itms) - 1)
    (key, value) = itms[selected]
    if isinstance(value, str):
        route.append(value)
        return route[1:]
    else:
        route.append(key)
        #ej:   ¿Que tipo de chica sentada en la rama incrustada en el palo sembrado en el hoyo a la orilla del mar quiere?
        print("¿Qué tipo de "+ " ".join(list(map(userTerms.get, route))) +" quiere?")
        if isinstance(value, list):
            # habria que imprimirles las opciones
            for i in range(len(value)):
                print("~|",i,userTerms[value[i]])
            selItem = reqNumberInput(0,len(value) - 1)
            route.append(value[selItem]) 
            return route[1:]
        elif isinstance(value, dict):
            return getOptionPath(value, route) 

def halt():
    '''Detiene la ejecución del programa.'''
    print("Cerrando programa...")
    sys.exit(0)

def consoleCreate():
    '''<Syntax> Con esta funcion puedes crear un proceso.'''
    pass

if __name__ == "__main__":
    start()