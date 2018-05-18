import sys
import pickle
import re
import xml.etree.ElementTree as ET
clean_re = re.compile('\W+')
conectivas = "and","or","andnot"
terminos_ampliado = "headline","text","category","date"
def busquedaAmpliada():
    """
    Este código se corresponde a la busqueda ampliada de la amplación propuesta 2

    """
    print("hola")
def busquedaPosicional():
    """
    Este código se corresponde a la implementación de la busqueda posicional Ampliación propuesta 3
    """
    print("hola")
def clean_text(text):
    """
    :param text: recibe el texto a limpiar.
    :return: el texto limpio de caracteres extraños y repeticiones
    """
    text_clean = clean_re.sub(' ', text).lower()
    return text_clean
def snipped(word,texto):
    #TODO en el boletín comentan otra forma de resolverlo...
    try:
        texto = texto.lower()
        posicion = texto.index(word)
        result = texto[max(0,posicion-500):min(len(texto)-1,posicion+500)]
        #print(result)
    except:
        result =""

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
def imprimir(postingResultante,docid,word):
    """
    Imprime por consola el resultado de la busqueda de los términosself.
    :param postingResultante: posting List resultado de las operaciones sobre los términos (AND OR NOT)
    :param docid: diccionario donde para cada docid tenemos el documento al que hace referencia
    :param word: *****REVISAR!****** word para la cual se calcula el sniped
    """
    if len(postingResultante) <= 0:
        print("---------------------------")
        print("No hay resultados")
        print("---------------------------")
    if len(postingResultante) <= 2:
        for value in postingResultante:
            fileNameID = int(value[0])
            noticeID = int(value[1])-1
            fileName = docid.get(fileNameID)
            notice = listOfNotices(fileName)[noticeID]
            root = ET.fromstring(notice) #obtengo el arbol XML
            texto = root.find("TEXT").text
            titulo = root.find("TITLE").text
            print("---------------------------")
            print("Título: \n %s" %titulo)
            print("Noticia: \n %s" %clean_text(texto) )
    elif len(postingResultante) <=5:
        #TODO mostrar titular y snipped
        for value in postingResultante:
            fileNameID = int(value[0])
            noticeID = int(value[1])-1
            fileName = docid.get(fileNameID)
            notice = listOfNotices(fileName)[noticeID]
            root = ET.fromstring(notice) #obtengo el arbol XML
            texto = root.find("TEXT").text
            titulo = root.find("TITLE").text
            print("------------------------------------")
            print("Título: \n %s" %clean_text(titulo))
            texto_result = snipped(word,clean_text(texto))
            #print("hola" + texto)
            print("Noticia: \n %s" %texto_result)
    else:
        #TODO mostrar los 10 primeros
        for value in postingResultante[0:min(10,len(postingResultante))]:
            fileNameID = int(value[0])
            noticeID = int(value[1])-1
            fileName = docid.get(fileNameID)
            notice = listOfNotices(fileName)[noticeID]
            root = ET.fromstring(notice) #obtengo el arbol XML
            texto = root.find("TEXT").text
            titulo = root.find("TITLE").text
            print("-------------------------------------")
            print("Título: \n %s" %titulo)
            #print("Noticia: \n %s" %texto)
    print("El número de noticias encontradas para los terminos especificados es: %d" %len(postingResultante))
def interseccion(postList1, postList2):
    returndata = []
    i = 0
    j = 0
    while i<len(postList1) and j < len(postList2):
        #TODO hacer testing
        if postList1[i][0] == postList2[j][0] and postList1[i][1] == postList2[j][1]:
            returndata.append(postList1[i])
            i+=1
            j+=1
        elif postList1[i][0] == postList2[j][0] and postList1[i][1] < postList2[j][1] or postList1[i][0] < postList2[j][0] :
            i+=1
        elif postList1[i][0] == postList2[j][0] and postList1[i][1] > postList2[j][1] or postList1[i][0] > postList2[j][0]:
            j+=1
    return returndata
def andNotAlg(postList1,postList2):
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
        #TODO hacer testing
        if postList1[i][0] == postList2[j][0] and postList1[i][1] == postList2[j][1]:
            returndata.append(postList1[i])
            i+=1
            j+=1
        elif postList1[i][0] == postList2[j][0] and postList1[i][1] < postList2[j][1] or postList1[i][0] < postList2[j][0] :
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
    if operador == "and":
        return interseccion(post1,post2)
    elif operador == "or":
        return orAlg(post1,post2)
    elif operador == "andnot":
        return andNotAlg(post1,post2)
def andOrNot(consulta,Index,docID):
    """
    Ampliación 1: permitimos consultas del estilo term1 and term2 or term3 and not term4.
    Podemos suponer que las consultas están correctamente escritas.
    """
    print("Ejecutando la primera ampliación")
    post1 = Index.get(consulta[0])
    operador = consulta[1]
    post2 = Index.get(consulta[2])
    #print("term1:%s operador: %s term2: %s" %(consulta[0],consulta[1],consulta[2]))
    result = []
    if post1 is not None and post2 is not None or operador == "or":
        result = operadores(post1,post2,operador)
        print(result)
    for i in range(3, len(consulta)-1):
        operador = consulta[i]
        post2 = Index.get(consulta[i+1])
        #print(" operador: %s term2: %s" %(consulta[i],consulta[i+1]))
        if result is not None and post2 is not None or operador == "or":
            result = operadores(result,post2,operador)
    imprimir(result,docID,"")
def load_object(fileName):
    """
    Devuelve un objeto tras cargar el fichero
    :param fileName: fichero a cargar
    :return: objeto
    """
    with open(fileName,"rb") as fh:
        obj,obj2 = pickle.load(fh)
    return obj,obj2
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Formato incorrecto: python SAR_search nombre_fichero")
        exit()
    fileName = sys.argv[1]
    Index,docid = load_object(fileName)
    #print(Index)
    while True:
        consulta = input("Introduce la consulta: ")
        if consulta == "":
            print("Saliendo del programa...")
            exit()
        consulta = consulta.lower()
        consulta_terms = consulta.split(" ")
        if len(set(conectivas).intersection(consulta_terms)) >0:
            andOrNot(consulta_terms,Index,docid)
        else:
            result  = []
            if len(consulta_terms) == 1:
                #Si solo hay un terminos
                result = Index.get(consulta_terms[0])
                if result is None:
                    result = []
            else:
                post1 = Index.get(consulta_terms[0])
                post2 = Index.get(consulta_terms[1])
                if post1 is not None and post2 is not None:
                    result = interseccion(post1,post2)
                for i in range(2, len(consulta_terms)):
                    post2 = Index.get(consulta_terms[i])
                    if result is not None and post2 is not None:
                        result = interseccion(result,post2)
                #Result tiene la interseccion de todos los terminos de la consulta
            imprimir(result,docid,consulta_terms[0])
