
import requests
import re
from bs4 import BeautifulSoup

def getScrapping(nombre):
    url="https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q="
    # nombre=input("INGRESE EL NOMBRE")
    nombre=nombre.split()
    # apellido=input("INGRESE EL APELLIDO")
    for nom in nombre:
        url=url+nom+"+"
    url=url[:-1]
    source  = requests.get(url)
    # print(url)
    soup=BeautifulSoup(source.text,"lxml")
    # print(soup.div.h4.a["href"]) #,{"class": ["gs_r"]})
    busqueda=soup.div.h4.a["href"]
    #MOSTRAR LOS ARTICULOS , SUS CITACIONES Y TOTAL DE CITACIONES
    source2  = requests.get("https://scholar.google.com"+busqueda)
    soup2=BeautifulSoup(source2.text,"lxml")
    # TOTAL_CITACIONES=soup2.find_all('td',{"class":["gsc_rsb_std"]})[0].string
    ARTICULOS=soup2.find_all('td',{"class":["gsc_a_t"]})
    nombre_articulos=[]
    for ARTICULO in ARTICULOS:
        # print(ARTICULO.a.string)
        nombre_articulos.append(ARTICULO.a.string)
    citacionesporarticulo=[]
    citaciones=soup2.find_all('a',{"class":["gsc_a_ac gs_ibl"]})
    for citacion in citaciones:
        # print(citacion.string)
        cita=citacion.string
        if(citacion.string==None):
            cita=0
        citacionesporarticulo.append(cita)

    anioporarticulo=[]
    Anios=soup2.find_all('span',{"class":["gsc_a_h gsc_a_hc gs_ibl"]})
    for anio in Anios:
        # print(anio.string)
        anioc=anio.string
        if(anio.string==None):
            anioc=0
        citacionesporarticulo.append(anioc)
    # print(soup2.find_all('td',{"class":["gsc_a_t"]}))
    articulofinal=[]
    articulofinal=nombre_articulos+citacionesporarticulo+anioporarticulo
    artfinal=[]
    n=int(len(articulofinal)/3)
    # print(n)
    art=[]
    for i in range(n):
        for j in range(i,len(articulofinal),n):
            art.append(articulofinal[j])
        artfinal.append(art)
        art=[]
    # print (artfinal)
    return artfinal
    