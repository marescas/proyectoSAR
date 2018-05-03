import sys
import pickle
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
    filename = sys.argv[1]
    Index,docid = load_object(fileName)
    while True:
        consulta = input("Introduce la consulta")
        if consulta == "":
            print("Saliendo del programa...")
            exit()
        consulta_terms = consulta.split()
        result  = []
        for i in range(0, len(consulta_terms)-1):
            print(consulta_terms[i],consulta_terms[i+1])
