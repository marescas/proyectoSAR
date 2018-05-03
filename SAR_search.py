import sys
import pickle
def imprimir(postingResultante,docid):
    print("El número de noticias encontradas para los terminos especificados es: %d" %len(postingResultante))
    print(postingResultante)
def interseccion(postList1, postList2):
    returndata = []
    i = 0
    j = 0
    while i<len(postList1) and j < len(postList2):
        if postList1[i][0] == postList2[j][0]:
            returndata.append(postList1[i])
            i+=1
            j+=1
        elif postList1[i][0] > postList2[j][0]:
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
    while True:
        consulta = input("Introduce la consulta")
        if consulta == "":
            print("Saliendo del programa...")
            exit()
        consulta_terms = consulta.split()
        result  = []
        if len(consulta_terms) == 1:
            #Si solo hay un terminos
            result = Index.get(consulta[0])
        else:
            post1 = Index.get(consulta[0])
            post2 = Index.get(consulta[1])
            if post1 is not None and post2 is not None:
                result = interseccion(post1,post2)
            for i in range(2, len(consulta_terms)):
                post2 = Index.get(consulta[i])
                if result is not None and post2 is not None:
                    result = interseccion(result,post2)
            #Result tiene la interseccion de todos los terminos de la consulta
        imprimir(result,docid)
