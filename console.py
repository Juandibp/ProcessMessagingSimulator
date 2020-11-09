import sys
import pprint
from config import *
from process import *

controller = None

configuration = None


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
    "implicit": "implicito",
    "lenMsg":"tamaño de cola de mensajes",
    "lenProcesses":"número máximo de procesos"
}



def start():
    global controller, configuration

    conf = consoleStartingSequence()

    configuration =config(conf["send"], conf["recieve"], conf["addressing"], conf["format"], conf["queueMethod"], conf["lenMsg"], conf["lenProcesses"])

    controller = ProcessController(configuration)

    while True:
        try:
            req = input("> ")
            exec(req, consoleOptions)
        except Exception as e:
            print("No se pudo reconocer el comando recibido. Asegurese de no haber cometido algun error en la escritura del comando o alguno de los parametros o ingrese 'help()' para obtener mas informacion.")
            print(e)


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
        if min != None and min > selected:
            print("La seleccion tiene que ser mayor o igual que " + str(min) + ". Intente de nuevo.")
            return reqNumberInput(min, max)
        if max != None and max < selected:
            print("La seleccion tiene que ser menor o igual que " + str(max) + ". Intente de nuevo.")
            return reqNumberInput(min, max)
        return selected
    except:
        print("La seleccion que hizo no es valida. Intente de nuevo.")
        return reqNumberInput(min, max)

def reqTypeValue(t:type, message:str):
    '''Esta funcion interna le pide al usuario un valor del tipo 't'.'''
    while True:
        try:
            inputVal = t(input(message))
            if inputVal < 0:
                print("Este valor no puede ser negativo. ")
            else:
                return inputVal 
        except:
            print("El valor ingresado no es un '" +t.__name__+ "'.")

def consoleStartingSequence():
    '''Esta funcion permite seleccionar la configuracion inicial del programa'''

    print('\nAntes de iniciar necesitamos hacer las configuraciones iniciales.')

    configOptions = {
        "send": ["blocking", "non-blocking"],
        "recieve": ["blocking","non-blocking","arrival-test"],
        "addressing": {
            "direct": {
                # "send":"send",
                "recieve":["explicit", "implicit"]
            },
            "indirect":"indirect",
        },
        "format":{
            "length":{ #no worries
                "fixed":int,
                "dynamic":"dynamic"
            }
        },
        "queueMethod":["fifo","priority"],
        "lenMsg":int,
        "lenProcesses":int
    }
    selectedOptions = {}
    for (key, value) in configOptions.items():
        if isinstance(value, type):
            print( "\nPara configurar el '"+userTerms[key]+"' se necesita un valor de tipo '" + value.__name__)
            selectedOptions[key] = reqTypeValue(value,"Ingrese el valor a continuación: ")
        else:
            print("\nEstas son las opciones para configurar el " + userTerms[key])
            if isinstance(value, list):
                for i in range(len(value)):
                    print("~|",i, userTerms[value[i]])            
                sel = reqNumberInput(0, len(value) - 1)
                selectedOptions[key] = value[sel]
            elif isinstance(value, dict):
                selectedOptions[key] = getOptionPath(value, [key])
    print("\nEsta es la configuración seleccionada:\n")
    pprint.pprint(selectedOptions)
    print("\nIniciando programa..."+
          "\nIngrese 'help()' o 'help(<comando>)' para obtener ayuda."+
          "\nIngrese 'exit()' para salir.\n")
    return selectedOptions

def consoleBatch(path: str, instructionLimit = -1):
    '''execFromFile(<path> [, <limit>]) Esta funcionalidad permite ejecutar un bloque de comandos desde un archivo de texto dado por 'path', \
        opcionalmente se puede especificar un limite de cantidad de instrucciones a ejecutar.'''
    l = 0
    try:
        f = open(path)
        for line in f:
            l += 1
            if line and instructionLimit:
                opt = consoleOptions.copy()
                opt["execFromFile"] = None #no queremos que desde un archivo se puedan ejecutar otros archivos
                instructionLimit -= 1
                exec(line, opt)
            elif instructionLimit:
                continue
            else:
                break
    except FileNotFoundError:
        print("Parece que el archivo no se encontró o no existe.")
    except Exception as e:
        print("La instrucción en la línea " + str(l) + " no se pudo ejecutar. Revise que el comando y los parámetros sean correctos o escriba 'help()' o 'help(<comando>)' para más ayuda.")

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
    elif isinstance(value, type):
        route.append(key)
        print("Se necesita un valor de tipo '" +value.__name__+ "' para configurar el " + " ".join(list(map(userTerms.get, route)))+".")
        inputVal = reqTypeValue(int, "Ingrese el valor a continuación: ")
        route.append(inputVal)
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

def consoleCreate(name:str):
    '''create(nombre:str) Con esta funcion puedes crear un proceso con el nombre dado como parámetro.'''    
    try:
        controller.addProcess(Process(name))
    except Exception as e:
        print("Algo salio mal: " + str(e))

def consoleSend(sender, receiver, msg, priority = 0):
    '''send(sender:str, receiver:str, msg:str, priority:int = 0) Esta funcionalidad te permite mandar un mensaje enviado por el proceso con id sender para el proceso con id receiver. En caso de que la disciplina de colas lo contemple, se puede ingresar la prioridad del mensaje.'''
    if isinstance(configuration.format[-1], int):
        if len(msg) > configuration.format[-1]:
            print("El mensaje ingresado debe ser de una longitud menor o igual que " + configuration.format[-1] + ". Por favor intente de nuevo.")
            return
    controller.send(sender, receiver, msg, priority)

def consoleReceive(sender, receiver):
    '''receive(sender, receiver) Esta funcion permite recibir un mensaje como receiver eviado por sender.'''
    controller.receive(sender, receiver)

def consoleDisplay():
    #TODO display
    '''display() Muestra el estado actual de la aplicacion. Esto incluye la configuracion, el mailbox, el estado de los procesos y los mensajes en cola.'''
    pass


consoleOptions = {          
            '__builtins__':None,
            'help':assist,
            'exit':halt,
            'create':consoleCreate,
            'batch':consoleBatch,
            'send':consoleSend,
            'receive':consoleReceive,
            'display':consoleDisplay,
            }

if __name__ == "__main__":
    start()