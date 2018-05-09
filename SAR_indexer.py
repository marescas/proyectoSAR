import sys
import xml.etree.ElementTree as ET
import os
import re
import pickle
clean_re = re.compile('\W+')
def clean_text(text):
    """
    :param text: recibe el texto a limpiar.
    :return: el texto limpio de caracteres extraños y repeticiones
    """
    text_clean = clean_re.sub(' ', text).lower()
    return text_clean
def listOfDocs(coleccion_noticias):
    """
    :param coleccion_noticias: recibe el nombre del directorio donde estan las n_noticias
    :return lista de documentos
    """
    nomFiles = os.listdir(coleccion_noticias)
    nomFilesDefinitivo = []
    for fileName in nomFiles:
        nomFilesDefinitivo.append(coleccion_noticias+fileName)
    return nomFilesDefinitivo
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
def anadirTermino(Index, termino, docID, noticeID):
    """
    Añade el término al índice con el identificador del documento y el identificador de la noticia como tupla
    """
    posicion = (docID,noticeID)
    if Index.get(termino) is None:
        Index[termino] = []
    Index[termino].append(posicion)

def saveObject(object1,object2,outputFile):
    """
    Guarda el objeto en el fichero
    :param object: objeto a guardar
    :param outputFile: Fichero en el que se guardará el objeto
    """
    with open(outputFile,"wb") as fh:
        object = (object1,object2)
        pickle.dump(object,fh)
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Error: El formato esperado es: python SAR_indexer dir_colección_noticias nombre_índice")
        exit()
    docID = {}
    indiceDoc = 1
    Index =  {}
    coleccion_noticias = sys.argv[1] #directorio donde está la coleccion de noticias
    nombre_indice = sys.argv[2] #nombre del fichero del índice
    docs = listOfDocs(coleccion_noticias) #Obtengo la lista de documentos
    for filename in docs:
        docID[indiceDoc] = filename #para cada fichero guardo su docID en el diccionario
        notices = listOfNotices(filename) #obtengo la lista de noticias de ese documento
        indiceNoticia = 1
        for r in notices:
            root = ET.fromstring(r) #obtengo el arbol XML
            texto_limpio = clean_text(root.find("TEXT").text) #limpio el texto de la noticia
            terminos = list(set(texto_limpio.split(" "))) #obtengo los terminos de la noticia
            for term in terminos:
                anadirTermino(Index,term,indiceDoc,indiceNoticia) #añadimos el término a la posting list
            indiceNoticia +=1 #incrementamos el identificador de la noticia en el documento
        indiceDoc+=1 #incrementamos el identificador del documento
    saveObject(Index,docID,nombre_indice)
    print("Guardado con éxito en el fichero %s" %nombre_indice)
