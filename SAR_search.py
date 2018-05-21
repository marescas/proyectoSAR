import sys
import pickle
import re
import xml.etree.ElementTree as ET
clean_re = re.compile('\W+')
conectivas = "and","or","andnot","not","ornot"
terminos_ampliado = "headline","text","category","date"

def clean_text(text):
    """
    :param text: recibe el texto a limpiar.
    :return: el texto limpio de caracteres extraños y repeticiones
    """
    text_clean = clean_re.sub(' ', text).lower()
    return text_clean

def snipped(word,texto):
    try:
        aux = texto.lower().split()
        posicion = aux.index(word)
        result = aux[max(0,posicion-3):min(len(aux)-1,posicion+4)]
        result = " ".join(result)
    except:
        result = ""
    return result

def listOfNotices(filename):
    """
    :param fileName: recibe el nombre del fichero a procesar
    :return: lista con las noticias
    """
    with open(filename) as f:
        listaProcesada = []
        listxml = f.read().split("</DOC>")
        for element in listxml:
            listaProcesada.append(element+"</DOC>")
    return listaProcesada[0:-1]

def imprimir(postingResultante,docid,words):
    """
    Imprime por consola el resultado de la busqueda de los términosself.
    :param postingResultante: posting List resultado de las operaciones sobre los términos (AND OR NOT)
    :param docid: diccionario donde para cada docid tenemos el documento al que hace referencia
    :param words: palabras para las cuales se calcula el snipped
    """
    if len(postingResultante) <= 0:
        print("\n------------------------------------")
        print("\nNo hay resultados")
        print("\n------------------------------------")
    if len(postingResultante) <= 2:
        for value in postingResultante:
            fileNameID = int(value[0])
            noticeID = int(value[1])-1
            fileName = docid.get(fileNameID)
            notice = listOfNotices(fileName)[noticeID]
            root = ET.fromstring(notice) #obtengo el arbol XML
            texto = root.find("TEXT").text
            titulo = root.find("TITLE").text
            print("\n------------------------------------")
            print("\nTítulo: \n %s" %titulo)
            print("\nNoticia: \n %s" %clean_text(texto) )
    elif len(postingResultante) <=5:
        for value in postingResultante:
            fileNameID = int(value[0])
            noticeID = int(value[1])-1
            fileName = docid.get(fileNameID)
            notice = listOfNotices(fileName)[noticeID]
            root = ET.fromstring(notice) #obtengo el arbol XML
            texto = root.find("TEXT").text
            titulo = root.find("TITLE").text
            print("\n------------------------------------")
            print("\nTítulo: \n %s" %clean_text(titulo))
            texto_result = ""
            for w in words:
                snip = snipped(w,clean_text(texto))
                if snip != "":
                    texto_result = texto_result + "\n" + snip
            print("\nNoticia: \n %s" %texto_result)
    else:
        for value in postingResultante[0:min(10,len(postingResultante))]:
            fileNameID = int(value[0])
            noticeID = int(value[1])-1
            fileName = docid.get(fileNameID)
            notice = listOfNotices(fileName)[noticeID]
            root = ET.fromstring(notice) #obtengo el arbol XML
            texto = root.find("TEXT").text
            titulo = root.find("TITLE").text
            print("\n-------------------------------------")
            print("\nTítulo: \n %s" %titulo)
    print("\n--------------------------------------------------------------------------")
    print("El número de noticias encontradas para los terminos especificados es: %d" %len(postingResultante))
    print("--------------------------------------------------------------------------\n")

def interseccion(postList1, postList2):
    returndata = []
    i = 0
    j = 0
    while i<len(postList1) and j < len(postList2):
        if postList1[i][0] == postList2[j][0] and postList1[i][1] == postList2[j][1]:
            returndata.append(postList1[i])
            i+=1
            j+=1
        elif postList1[i][0] == postList2[j][0] and postList1[i][1] < postList2[j][1] or postList1[i][0] < postList2[j][0] :
            i+=1
        elif postList1[i][0] == postList2[j][0] and postList1[i][1] > postList2[j][1] or postList1[i][0] > postList2[j][0]:
            j+=1
    return returndata

def andnotAlg(postList1,postList2):
    """
    Devuelve una lista con los resultados de la operación postList1 and not postList2
    """
    returndata = []
    i = 0
    j = 0
    while i<len(postList1) and j < len(postList2):
        if postList1[i][0] == postList2[j][0] and postList1[i][1] == postList2[j][1]:
            i+=1
            j+=1
        elif postList1[i][0] == postList2[j][0] and postList1[i][1] < postList2[j][1] or postList1[i][0] < postList2[j][0] :
            returndata.append(postList1[i])
            i+=1
        else:
            j+=1
    for iPost1 in range(i,len(postList1)):
        returndata.append(postList1[iPost1])
    return returndata

def orAlg(postList1,postList2):
    """
    Devuelve una lista con los resultados de la operación postList1 or postList2
    """
    returndata = []
    i = 0
    j = 0
    while i<len(postList1) and j < len(postList2):
        if postList1[i][0] == postList2[j][0] and postList1[i][1] == postList2[j][1]:
            returndata.append(postList1[i])
            i+=1
            j+=1
        elif postList1[i][0] == postList2[j][0] and postList1[i][1] < postList2[j][1] or postList1[i][0] < postList2[j][0]:
            returndata.append(postList1[i])
            i+=1
        elif postList1[i][0] == postList2[j][0] and postList1[i][1] > postList2[j][1] or postList1[i][0] > postList2[j][0]:
            returndata.append(postList2[j])
            j+=1
    for iPost1 in range(i,len(postList1)) :
        returndata.append(postList1[iPost1])
    for iPost2 in range(j,len(postList2)) :
        returndata.append(postList2[iPost2])
    return returndata

def operadores(post1,post2,operador):
    if post2 == None:
        post2 = []
    if operador == "and":
        return interseccion(post1,post2)
    elif operador == "or":
        return orAlg(post1,post2)
    elif operador == "andnot":
        return andnotAlg(post1,post2)
    elif operador == "ornot":
        return orAlg(postList1,andnotAlg(Universe,postList2))

def andOrNot(consulta,docID):
    """
    Ampliación 1: permitimos consultas del estilo term1 and term2 or term3 andnot term4.
    Podemos suponer que las consultas están correctamente escritas.
    """
    aux = list(consulta) # Copiamos "consulta" a "aux"
    if aux[0] == "not": # Si la primera palabra es "not"...
        try:
            aux.pop(0) # Eliminamos el "not" inicial
            # Y añadimos la postingList negada de la primera palabra
            postL = getIndex(aux.pop(0))
            if postL == None:
                postL = []
            result = andnotAlg(Universe,postL)
        except:
            result = []
    else:
        # Añadimos la postingList de la primera palabra
        result = getIndex(aux.pop(0))
    for i in range(0,len(aux)):
        # El resto de "not" actuarán como "andnot"
        if aux[i] != "andnot":
            aux[i] = aux[i].replace("not","andnot")
    # Ahora pasamos a ampliar (o disminuir) el "result" con el resto de la consulta.
    i = 0
    while i < len(aux):
        if aux[i] in conectivas:
            result = operadores(result,getIndex(aux[i+1]),aux[i])
            i = i+2
        else:
            result = operadores(result,getIndex(aux[i]),"and")
            i = i+1
    imprimir(result,docID,list(set(consulta) - set(conectivas)))

def getIndex(word):
    """
    Ampliación 2: obtiene las referencias de los ficheros en la cual aparece
    esa palabra para el campo indicado (headline,text,category,date).
    Supondremos que está bien escrito.
    """
    words = word.split(":")
    if len(words) == 1:
        return Index.get(word)
    else:
        if words[0] == "headline":
            return IndexHeadLine.get(words[1])
        elif words[0] == "text":
            return Index.get(words[1])
        elif words[0] == "category":
            return IndexCategory.get(words[1])
        elif words[0] == "date":
            return IndexDate.get(words[1])

def load_object(fileName):
    """
    Devuelve un objeto tras cargar el fichero
    :param fileName: fichero a cargar
    :return: objeto
    """
    with open(fileName,"rb") as fh:
        obj1,obj2,obj3,obj4,obj5,obj6 = pickle.load(fh)
    return obj1,obj2,obj3,obj4,obj5,obj6

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: El formato esperado es 'python SAR_search.py nombre_fichero'")
        exit()
    fileName = sys.argv[1]
    Index,docid,IndexHeadLine,IndexDate,IndexCategory,Universe = load_object(fileName)
    while True:
        consulta = input("\nIntroduce la consulta: ")
        if consulta == "":
            print("\nSaliendo del programa...\n")
            exit()
        consulta = consulta.lower()
        consulta = consulta.replace(' and not ', ' andnot ')
        consulta = consulta.replace(' or not ', ' ornot ')
        consulta = consulta.replace(' and ', ' ')
        consulta_terms = consulta.split()
        # En caso de que haya alguna conectiva, entramos en el método andOrNot
        if len(set(conectivas).intersection(consulta_terms)) > 0:
            andOrNot(consulta_terms,docid)
        else:
            result  = []
            if len(consulta_terms) == 1:
                #Si solo hay un término
                result = getIndex(consulta_terms[0])
                if result is None:
                    result = []
            elif len(consulta_terms) == 0:
                result = []
            else:
                post1 = getIndex(consulta_terms[0])
                post2 = getIndex(consulta_terms[1])
                if post1 is not None and post2 is not None:
                    result = interseccion(post1,post2)
                for i in range(2, len(consulta_terms)):
                    post2 = getIndex(consulta_terms[i])
                    if result is not None and post2 is not None:
                        result = interseccion(result,post2)
                # "result" tiene la interseccion de todos los terminos de la consulta
            imprimir(result,docid,consulta_terms)
