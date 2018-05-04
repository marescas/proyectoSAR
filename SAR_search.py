import sys
import pickle
import xml.etree.ElementTree as ET
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
def imprimir(postingResultante,docid):
    print("El número de noticias encontradas para los terminos especificados es: %d" %len(postingResultante))
    if len(postingResultante) <= 0:
        return
    if len(postingResultante) <= 2:
        for value in postingResultante:
            fileNameID = int(value[0])
            noticeID = int(value[1])-1
            fileName = docid.get(fileNameID)
            notice = listOfNotices(fileName)[noticeID]
            root = ET.fromstring(notice) #obtengo el arbol XML
            texto = root.find("TEXT").text
            titulo = root.find("TITLE").text
            print("Título: \n %s" %titulo)
            print("Noticia: \n %s" %texto)
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
            print("Título: \n %s" %titulo)
            #print("Noticia: \n %s" %texto)
    else:
        #TODO mostrar los 10 primeros
        for value in postingResultante:
            fileNameID = int(value[0])
            noticeID = int(value[1])-1
            fileName = docid.get(fileNameID)
            notice = listOfNotices(fileName)[noticeID]
            root = ET.fromstring(notice) #obtengo el arbol XML
            texto = root.find("TEXT").text
            titulo = root.find("TITLE").text
            print("Título: \n %s" %titulo)
            #print("Noticia: \n %s" %texto)



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
        elif postList1[i][0] > postList2[j][0] or postList1[i][1] > postList2[j][1]:
            j+=1
        else:
            i+=1
    return returndata

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
    print(Index)
    while True:
        consulta = input("Introduce la consulta: ")
        if consulta == "":
            print("Saliendo del programa...")
            exit()
        consulta_terms = consulta.split(" ")
        print(consulta_terms)
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
        imprimir(result,docid)
