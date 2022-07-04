# =============================================================================
# OBJETOS IMPORTANTES
# =============================================================================
# features_sud_todos                LOS VALORES (sud) DE TODAS LAS LENGUAS
# features_mundo_todos              LOS VALORES DE TODAS LAS LENGUAS
# features_sud                      LENGUAS (sud) QUE POSEEN LOS 4 FEATURES BUSCADOS(GLOTTO)
# features_sud_wcode                LENGUAS (sud) QUE POSEEN LOS 4 FEATURES BUSCADOS(ID)
# features_mundo_wcode              LENGUAS QUE POSEEN LOS 4 FEATURES BUSCADOS (ID)
# features_mundo                    LENGUAS QUE POSEEN LOS 4 FEATURES BUSCADOS(GLOTTO)
# Ubicación_Lenguas_Sudamerica      COORDENADAS DE LENGUAS (LATITUD Y LONGITUD)
# datos_lenguas                     TODOS LOS VALORES DE LOS VALUES BUSCADOS
# v                                 LENGUAS POR FAMILIAS SUDAMERICA
# D                                 LENGUAS DE LAS QUE SE TIENEN DATOS DE AREA
# areas_dict                        LENGUAS DEL WALS QUE CUMPLEN TOODOS LOS REQUISITOS

# =============================================================================
# =============================================================================

# =============================================================================
# ABRIR Y PREPARAR DATOS BASE DE WALS
# =============================================================================
import pandas as pd
## leemos los datos
## abro los value para extraer los rasgos! (Wals/values.csv)
datos_lenguas = pd.read_csv("WINDOWS/Código útil/Intentos de trabajos/Wals/values.csv",sep=',')
## nombre lenguas! (Wals/languages.csv)
lenguas_areas = pd.read_csv("WINDOWS/Código útil/Intentos de trabajos/Wals/languages.csv",sep=',',encoding='utf-8')
##Saco las lenguas que son de Sudamerica
Sudamerica = ['South America']
lenguas_sudamerica= lenguas_areas[lenguas_areas.Macroarea.isin(Sudamerica)]
lenguas_sudamerica_ID= lenguas_sudamerica[['ID','Name','Glottocode']]
# =============================================================================


# =============================================================================
# DICCIONARIO DE LAS FAMILIAS DE LAS LENGUAS QUE APARECEN EN WALS
# =============================================================================
##Esta es información de Glottocode (Wals/languages_and_dialects_geo.csv()
langs = pd.read_csv("WINDOWS/Código útil/Intentos de trabajos/Wals/languages_and_dialects_geo.csv")
macroarea1 = langs[['glottocode','macroarea']]
macroarea = macroarea1.dropna()
macroarea = macroarea1[macroarea1.glottocode.isin(list(lenguas_sudamerica_ID['Glottocode']))]
macroarea = dict(zip(macroarea['glottocode'], macroarea['macroarea']))
macroarea = {language:macroarea[language] for language in macroarea.keys() if macroarea[language] in ['South America']}
##Esta es información bajada de Glottocode (Wals/languoid.csv)
languoid = pd.read_csv('WINDOWS/Código útil/Intentos de trabajos/Wals/languoid.csv',sep=',')
id_family = languoid[['id','family_id']]
id_family = id_family.dropna()
id_family = dict(zip(id_family['id'], id_family['family_id']))
id_family = {language:id_family[language] for language in id_family.keys() if language in macroarea.keys()}

from collections import defaultdict

v = defaultdict(list)
for key, value in sorted(id_family.items()):
    v[value].append(key)
families = dict(v)
# =============================================================================

# =============================================================================
# EXTRAER LOS DATOS DE WALS EN BASE A LOS DATOS
# =============================================================================
## creamos un diccionario numero:nombre
codigo = [code for code in lenguas_sudamerica_ID['ID']]
nombre = [area for area in lenguas_sudamerica_ID['Name']]
codigo_nombre = [[codigo[i],nombre[i]] for i in range(len(codigo))]
codigo_nombre = {item[0]:item[1] for item in codigo_nombre}
Ubicación_Lenguas_Sudamerica = lenguas_areas[lenguas_areas.ID.isin(codigo)]
lenguas_sudamerica_muestra = datos_lenguas[datos_lenguas.Language_ID.isin(codigo)]
##definimos los rasgos buscados
rasgos = ["71A","112A", "113A", "143A"]

lenguas_sudamerica= datos_lenguas[datos_lenguas.Parameter_ID.isin(rasgos)]

features_pred = {}

for l in codigo_nombre.keys():
    values_l = lenguas_sudamerica[lenguas_sudamerica['Language_ID']==l]
    D=dict(zip(values_l['Parameter_ID'],values_l['Value']))
    features_pred[l]=D

rasgos_por_lengua = [len(list(features_pred[language].keys()))/float(len(set(rasgos))) for language in features_pred.keys()]


## filtramos los datos leídos

features_pred.values()
## buscamos los rasgos en común
rasgos_comunes = [list(item.keys()) for item in features_pred.values() if len(item)>3]
## intersectamos todos los conjuntos de rasgos sujetos a la condición len(item)>num_rasgos
rasgos_comunes = set(rasgos_comunes[0]).intersection(*rasgos_comunes)
## restringimos D
features_4 = {lengua:{key:features_pred[lengua][key] for key in rasgos_comunes} for lengua in features_pred.keys() if len(features_pred[lengua])>3}

features_pred_glotto_lista = []
features_pred_glotto_lista = lenguas_sudamerica_ID[lenguas_sudamerica_ID.ID.isin(list(features_4.keys()))]
features_5 = dict(zip(features_pred_glotto_lista['Glottocode'], features_4.values()))

# =============================================================================
# MAPAS
# =============================================================================
import geopandas
##Genero mapa de sudamerica
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world = world[world['continent']=='South America']
x = Ubicación_Lenguas_Sudamerica['Longitude'].values
y = Ubicación_Lenguas_Sudamerica['Latitude'].values
codes = Ubicación_Lenguas_Sudamerica['ID'].values
pruebas={'longitud':list(x), "latitud":list(y), "codigos": list(codes)}
pruebas = pd.DataFrame.from_dict(pruebas)
pruebas.to_csv(r"WINDOWS\Código útil/pruebas.csv")
probando = pd.read_csv(r"WINDOWS\Código útil/pruebas.csv")
probando['coordinates'] = probando[['longitud','latitud']].values.tolist()
from shapely.geometry import Point
probando['coordinates'] = probando['coordinates'].apply(Point)
lenguitas = geopandas.GeoDataFrame(probando, geometry = 'coordinates')

import matplotlib.pyplot as plt

fig, ax = plt.subplots(dpi=800)
ax.set_aspect('equal')
plt.title('Languages of South America',fontsize=7)
world.plot(ax=ax, color='white', edgecolor='salmon',linewidth=0.2)
lenguitas.plot(ax=ax, cmap = 'jet', edgecolor= 'black', markersize=15)
plt.savefig(r'WINDOWS\Código útil\Intentos de trabajos\Otros\mapas/lenguas_sudamerica.jpg', format='jpg', transparent=True, bbox_inches='tight',dpi=800)

def values_per_feature(DD,f):
    DDD = {}
    for key in DD.keys():
        if f in DD[key].keys():
            DDD[key]=DD[key][f]
    return DDD

import matplotlib.pyplot as plt

dict_color = {'1':{'marker':'X','color':'m'},'2':{'marker':'o','color':'b'},'3':{'marker':'s','color':'r'},
             '4':{'marker':'D','color':'cyan'},'5':{'marker':'*','color':'yellow'},'6':{'marker':'^','color':'fuchsia'},
             '7':{'marker':'v','color':'olive'},'8':{'marker':'p','color':'lime'},'9':{'marker':'H','color':'salmon'},'14':{'marker':'X','color':'springgreen'},'15':{'marker':'X','color':'gray'}}

for rasgo in rasgos:
    
    fig, ax = plt.subplots(dpi=800)

    ax.set_aspect('equal')
    plt.title('Languages for the negation domain: feature '+ rasgo ,fontsize=5)
    world.plot(ax=ax, color='white', edgecolor='black',linewidth=0.2)
#cities.plot(ax=ax, marker='o', color='red', markersize=5)
#ax.scatter(x, y, marker="o", color='gold', alpha=1., zorder=5, s=10)
    for f in set(values_per_feature(features_pred,rasgo).values()):
        
        ax.plot([x[i] for i in [list(codes).index(language) for language in codes if language in values_per_feature(features_pred,rasgo).keys() and values_per_feature(features_pred,rasgo)[language]==f]],[y[i] for i in [list(codes).index(language) for language in codes if language in values_per_feature(features_pred,rasgo).keys() and values_per_feature(features_pred,rasgo)[language]==f]],marker=dict_color[str(f)]['marker'],color=dict_color[str(f)]['color'],linewidth=0,markersize=5,markeredgewidth=0.5,markeredgecolor='k',alpha=0.75,fillstyle='full',clip_on=True,label='value '+str(f))
    plt.legend(loc='best',fontsize=5)

    ax.set_yticks([])
    ax.set_xticks([])
    plt.savefig('WINDOWS/Código útil/Intentos de trabajos\Otros\mapas/mapa_rasgo'+ rasgo +'.jpg', format='jpg', transparent=True, bbox_inches='tight',dpi=800)
    plt.show()
# =============================================================================

# =============================================================================
# 
# =============================================================================


# =============================================================================
# cuenta=[]
# for value in features_mundo_todos.values():
#     if len(value) == 4:
#         cuenta+=['1']
# len(cuenta)
# =============================================================================
# =============================================================================
# PREPARAR LAS AREAS DE LAS LENGUAS DE SUDAMERICA QUE HAY EN WALS
# =============================================================================
##Estos datos los trabajó Ricardo(negacion/andean languages.csv)
andean_languages = pd.read_csv('WINDOWS/Código útil/Intentos de trabajos/negacion - copia/negacion/andean languages.csv', on_bad_lines='skip', sep=';')
##estos datos los trabajó Ricardo(negacion/areas.csv)
areas = pd.read_csv('WINDOWS/Código útil/Intentos de trabajos/negacion - copia/negacion/areas.csv',sep=',')
lenguas_wals = andean_languages[andean_languages.GlottoCode.isin(list(lenguas_sudamerica_ID['Glottocode']))]
areas_wals = areas[areas.correlativo.isin(list(lenguas_wals['Correlativo']))]
GlottoCode = lenguas_wals['GlottoCode']
areas_wals = areas_wals.join(GlottoCode)
lenguas = [name.lower() for name in list(areas['lengua'])]
areas_dict = {}
for i in list(areas_wals.index):
    if areas_wals.loc[i,'lengua'].lower()=='moseten':
        areas_dict['moseten']=[areas_wals.loc[i,'sub-area'].lower(),areas_wals.loc[i,'area'].lower()]
    else:
        areas_dict[areas_wals.loc[i,'GlottoCode'].lower()]=[areas_wals.loc[i,'sub-area'].lower().strip(),areas_wals.loc[i,'area'].lower().strip()]

area_dict = {language:areas_dict[language][1] for language in areas_dict.keys()}
subarea_dict = {language:areas_dict[language][0] for language in areas_dict.keys()}

##Esto es un turco porque no me funcionaba bien lo que quería hacer (Wals/features_7.csv)
features_7=pd.read_csv('WINDOWS/Código útil/Intentos de trabajos/Wals/features_7.csv')
features_8 = features_7[features_7.GlottoCode.isin(list(features_5.keys()))]
features_9 = {lengua:{key:features_5[lengua][key] for key in rasgos_comunes} for lengua in features_5.keys() if lengua in list(features_8['GlottoCode'])}
features_10 = andean_languages[andean_languages.GlottoCode.isin(list(features_8['GlottoCode']))]
features_11 = areas[areas.correlativo.isin(list(features_10['Correlativo']))]

GlottoCode = features_10['GlottoCode']
features_11 = features_11.join(GlottoCode)
areas_dict = {}
for i in list(features_11.index):
    if features_11.loc[i,'lengua'].lower()=='moseten':
        areas_dict['moseten']=[features_11.loc[i,'sub-area'].lower(),features_11.loc[i,'area'].lower()]
    else:
        areas_dict[features_10.loc[i,'GlottoCode'].lower()]=[features_11.loc[i,'sub-area'].lower().strip(),features_11.loc[i,'area'].lower().strip()]
area_dict = {language:areas_dict[language][1] for language in areas_dict.keys()}
subarea_dict = {language:areas_dict[language][0] for language in areas_dict.keys()}
from collections import defaultdict


area_lengua = defaultdict(list)
for key, value in sorted(area_dict.items()):
    area_lengua[value].append(key)



group_area = {area:[l for l in dict(area_lengua)[area] if l in area_dict.keys()] for area in dict(area_lengua).keys()}


subarea_lengua = defaultdict(list)

for key, value in sorted(subarea_dict.items()):
    subarea_lengua[value].append(key)

group_subarea = {area:[l for l in dict(subarea_lengua)[area] if l in subarea_dict.keys()] for area in dict(subarea_lengua).keys()}



# =============================================================================



# =============================================================================
# ALEATORIEDAD
# =============================================================================

import random
from collections import defaultdict

area_random = []

keys = list(area_dict.keys())
for i in range(1000):
    values = list(area_dict.values())
    values = random.sample(values,len(values))
    d=dict(zip(keys,values))
    
    v = defaultdict(list)
    for key, value in sorted(d.items()):
        v[value].append(key)
        
    area_random+=[{area:[l for l in dict(v)[area] if l in features_9.keys()] for area in dict(v).keys()}]
    
subarea_random = []

keys = list(subarea_dict.keys())
for i in range(1000):
    values = list(subarea_dict.values())
    values = random.sample(values,len(values))
    d=dict(zip(keys,values))
    
    v = defaultdict(list)
    for key, value in sorted(d.items()):
        v[value].append(key)
        
    subarea_random+=[{area:[l for l in dict(v)[area] if l in features_9.keys()] for area in dict(v).keys()}]
    
# =============================================================================

# =============================================================================
# DEF UTILIZADAS
# =============================================================================
    
##DISTANCIA DE HAMMING

def hamming(lengua1, lengua2):
    
    ## rasgos
    features_lengua1= features_9[lengua1]
    features_lengua2= features_9[lengua2]
    
    ## hamming!
    d=0
    n=0
    for feature in features_lengua1.keys():
        if feature in features_lengua2.keys(): 
            if features_lengua1[feature] != features_lengua2[feature]:
                d += 1.0
            n += 1.0
            
    return d/n




##PARA CALCULAR LAS DISTRIBUCIONES DE LOS RASGOS
from collections import Counter

def distribucion(D):
    
    D_rasgos = {lengua:{} for lengua in D.keys()}
    for lengua in D.keys():
        for lengualengua in D.keys():
            features=list(D.values())
            features=[len(item) for item in features]
    C=dict(Counter(features))
    keys = sorted(C.keys())
    DD = {}
    for key in keys:
        x = 0
        for keykey in C.keys():
            if keykey>=key:
                x+=C[keykey]
        DD[key]=x
    return DD

hamming('onaa1245','onaa1245')
##PARA SACAR DISTANCIAS entre los grupos
import itertools

def distancias_group(dict_group):
    D = {area:{} for area in dict_group.keys()}
    for area in dict_group.keys():
        for areaarea in dict_group.keys():
            lenguas = dict_group[area]
            lenguas_comp = dict_group[areaarea]
            L = [lenguas,lenguas_comp]
            pairs = list(itertools.product(*L))
            distances = 0
            for pair in pairs:
                    distances+=hamming(pair[0],pair[1])
            if distances > 0:
                distances = distances/len(pairs)
            D[area][areaarea]=distances

    return D

# =============================================================================
def distancias_lenguas(dict_group):
    D = {lang:{} for lang in dict_group.keys() }
    for lang in list(dict_group.keys()):
        for langlang in dict_group.keys():
            lenguas = list(dict_group.keys())
            lenguas_comp = list(dict_group.keys())
            L = [lenguas,lenguas_comp]
            pairs = list(itertools.product(*L))
            distances = 0
            for pair in pairs:
                distances+=hamming3(pair[0],pair[1])
            if distances > 0:
                distances = distances/len(pairs)
            D[lang][langlang]=distances
    return D


# =============================================================================
# CALCULOS EN 2D
# =============================================================================
distancias_area = distancias_group(group_area)
distancias_area_random = [distancias_group(d) for d in area_random]
distancias_area


# =============================================================================
# # =============================================================================
# # =============================================================================
# # # AREAS
# # =============================================================================
# # =============================================================================
# 
# 
# # =============================================================================
# # # ANDES
# # =============================================================================
# 
# 
# import seaborn as sns
# import matplotlib.pyplot as plt
# from scipy import stats
# 
# print(stats.ttest_1samp([d['andes']['andes'] for d in distancias_area_random], distancias_area['andes']['andes'],alternative="greater"))
# 
# fig, ax = plt.subplots(dpi=800)
# ax = sns.distplot([d['andes']['andes'] for d in distancias_area_random],kde_kws={"color": "k", "lw": 1, "label": "randomized Andes"},
#                   hist_kws={"histtype": "step", "linewidth": 1,
#                             "alpha": 1, "color": "g"})
# 
# plt.axvline(x=distancias_area['andes']['andes'],linestyle='--',color='gold',label=r'Andes')
# plt.legend(loc='best',fontsize=7)
# plt.xlabel(r'Hamming distance',fontsize=15)
# plt.ylabel(r'frequency',fontsize=15)
# plt.rcParams.update({'font.size': 10})
# plt.savefig('C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Otros/hammingsandesvsandes.jpg', format='jpg', transparent=True, bbox_inches='tight',dpi=800)
# plt.show()
# # =============================================================================
# 
# # =============================================================================
# # # AMAZONÍA     
# # =============================================================================
# 
# import seaborn as sns
# import matplotlib.pyplot as plt
# from scipy import stats
# 
# print(stats.ttest_1samp([d['amazonia']['amazonia'] for d in distancias_area_random], distancias_area['amazonia']['amazonia'],alternative="greater"))
# 
# fig, ax = plt.subplots(dpi=800)
# ax = sns.distplot([d['amazonia']['amazonia'] for d in distancias_area_random],kde_kws={"color": "k", "lw": 1, "label": "randomized Amazonia"},
#                   hist_kws={"histtype": "step", "linewidth": 1,
#                             "alpha": 1, "color": "g"})
# 
# plt.axvline(x=distancias_area['amazonia']['amazonia'],linestyle='--',color='gold',label=r'Amazonia')
# plt.legend(loc='best',fontsize=7)
# plt.xlabel(r'Hamming distance',fontsize=15)
# plt.ylabel(r'frequency',fontsize=15)
# plt.rcParams.update({'font.size': 10})
# plt.savefig('C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Otros/hammings/amazoniavsamazonia.jpg', format='jpg', transparent=True, bbox_inches='tight',dpi=800)
# plt.show()
# 
# # =============================================================================
# # =============================================================================
# # SUBAREAS
# # =============================================================================
# # =============================================================================
# 
# # =============================================================================
# # central
# # =============================================================================
# 
# distancias_subarea = distancias_group(group_subarea)
# distancias_subarea_random = [distancias_group(d) for d in subarea_random]
# import seaborn as sns
# import matplotlib.pyplot as plt
# from scipy import stats
# 
# print(stats.ttest_1samp([d['central andes']['central andes'] for d in distancias_subarea_random], distancias_subarea['central andes']['central andes'],alternative="greater"))
# 
# fig, ax = plt.subplots(dpi=800)
# ax = sns.distplot([d['central andes']['central andes'] for d in distancias_subarea_random],kde_kws={"color": "k", "lw": 1, "label": "randomized Central Andes"},
#                   hist_kws={"histtype": "step", "linewidth": 1,
#                             "alpha": 1, "color": "g"})
# 
# plt.axvline(x=distancias_subarea['central andes']['central andes'],linestyle='--',color='gold',label=r'Central Andes')
# plt.legend(loc='best',fontsize=7)
# plt.xlabel(r'Hamming distance',fontsize=15)
# plt.ylabel(r'frequency',fontsize=15)
# plt.rcParams.update({'font.size': 10})
# plt.savefig('C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Otros/mapas/centralandes.jpg', format='jpg', transparent=True, bbox_inches='tight',dpi=800)
# plt.show()
# 
# # =============================================================================
# 
# # =============================================================================
# # EL CORPUS GENERA UN ERROR PORQUE NO HAY LENGUAS DEL NORTES DE LOS ANTES QUE
# # TENGAN LOS RASGOS BUSCADOS, POR ESTO SE AÑADE ARTIFICIALMENTE 
# # =============================================================================
# 
# # =============================================================================
# # CENTRAL VS NORTE N/A
# # =============================================================================
# 
# # =============================================================================
# 
# # =============================================================================
# # CENTRAL VS SUR
# # =============================================================================
# 
# import seaborn as sns
# import matplotlib.pyplot as plt
# from scipy import stats
# 
# print(stats.ttest_1samp([d['central andes']['southern andes'] for d in distancias_subarea_random], distancias_subarea['central andes']['southern andes'],alternative="greater"))
# 
# fig, ax = plt.subplots(dpi=800)
# ax = sns.distplot([d['central andes']['southern andes'] for d in distancias_subarea_random],kde_kws={"color": "k", "lw": 1, "label": "randomized Central vs. Southern Andes"},
#                   hist_kws={"histtype": "step", "linewidth": 1,
#                             "alpha": 1, "color": "g"})
# 
# plt.axvline(x=distancias_subarea['central andes']['southern andes'],linestyle='--',color='gold',label=r'Central vs. Southern Andes')
# plt.legend(loc='best',fontsize=7)
# plt.xlabel(r'Hamming distance',fontsize=15)
# plt.ylabel(r'frequency',fontsize=15)
# plt.rcParams.update({'font.size': 10})
# plt.savefig('C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Otros/hammings/centralvssouthernandes.jpg', format='jpg', transparent=True, bbox_inches='tight',dpi=800)
# plt.show()
# =============================================================================

# =============================================================================
# =============================================================================
# =============================================================================
# Clusters
# =============================================================================
# =============================================================================

D= features_9
D_lenguas = {lengua:{} for lengua in D.keys()}

for lengua in D.keys():
    for lengua_lengua in D.keys():
        lengua_feat = D[lengua]
        lengua_lengua_feat = D[lengua_lengua]
        D_lenguas[lengua][lengua_lengua]=hamming(lengua,lengua_lengua)
X=[]
for language in D_lenguas.keys():
    X+=[list(D_lenguas[language].values())]

from sklearn.manifold import TSNE

model = TSNE(n_components=2, perplexity=15, random_state=0, metric='precomputed',square_distances=True)
X = model.fit_transform(X)
x=list(zip(*list(X)))[0]
y=list(zip(*list(X)))[1]



import matplotlib.pyplot as plt

for rasgo in rasgos:
    
    cmap = plt.get_cmap('RdBu')
    
    fig, ax = plt.subplots(dpi=800)
    
    for i in range(len(x)):
        ax.annotate(list(D.keys())[i], weight='demi', color='k', xy=(x[i],y[i]), fontsize=4, alpha=0.65)
    #    ax.annotate(labels[i], weight='demi', color='r', xy=(x[i]-1.5,y[i]-1.5), fontsize=4, alpha=0.85)
    
    ax.plot([x[i] for i in [list(D.keys()).index(language) for language in D.keys()]],[y[i] for i in [list(D.keys()).index(language) for language in D.keys()]],'o',color='gold',markersize=5,markeredgewidth=0.5,markeredgecolor='k',alpha=0.75,fillstyle='full',clip_on=True)
    
    #ax.plot([x[i] for i in [list(L.keys()).index(language) for language in L.keys() if family[language] in ['Mayan','Otomanguean']]],[y[i] for i in [list(L.keys()).index(language) for language in L.keys() if family[language] in ['Mayan','Otomanguean']]],'X',color='m',markersize=6,markeredgewidth=0.5,markeredgecolor='k',alpha=0.75,fillstyle='full',clip_on=True,label='Maya+Otomangue')
    #ax.plot([x[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='South America']],[y[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='South America']],'H',color='orange',markersize=5,markeredgewidth=0.5,markeredgecolor=None,alpha=0.85,fillstyle='full',clip_on=True,label='South America')
    #ax.plot([x[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='North America']],[y[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='North America']],'o',color='lime',markersize=5,markeredgewidth=0.5,markeredgecolor=None,alpha=0.85,fillstyle='full',clip_on=True,label='North America')
    
    plt.grid(False)
    plt.title('Clustering for domain '+str(rasgo),fontsize=10)
    ax.set_yticks([])
    ax.set_xticks([])
    #plt.legend(loc='best',fontsize=7)
    plt.ylabel(r'dimension 2',fontsize=10)
    plt.xlabel(r'dimension 1',fontsize=10)
    plt.rcParams.update({'font.size': 10})
    plt.savefig('C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Otros/2D/PCA_'+str(rasgo)+'.jpg', format='jpg', transparent=True, bbox_inches='tight',dpi=800)
    plt.show()

import matplotlib.pyplot as plt
for rasgo in rasgos:
    cmap = plt.get_cmap('RdBu')
    
    fig, ax = plt.subplots(dpi=800)
    
    for i in range(len(x)):
        ax.annotate(list(D.keys())[i], weight='demi', color='k', xy=(x[i],y[i]), fontsize=4, alpha=0.65)
    #    ax.annotate(labels[i], weight='demi', color='r', xy=(x[i]-1.5,y[i]-1.5), fontsize=4, alpha=0.85)
    
    ax.plot([x[i] for i in [list(D.keys()).index(language) for language in D.keys()]],[y[i] for i in [list(D.keys()).index(language) for language in D.keys()]],'o',color='gold',markersize=5,markeredgewidth=0.5,markeredgecolor='k',alpha=0.75,fillstyle='full',clip_on=True)
    
    #ax.plot([x[i] for i in [list(L.keys()).index(language) for language in L.keys() if family[language] in ['Mayan','Otomanguean']]],[y[i] for i in [list(L.keys()).index(language) for language in L.keys() if family[language] in ['Mayan','Otomanguean']]],'X',color='m',markersize=6,markeredgewidth=0.5,markeredgecolor='k',alpha=0.75,fillstyle='full',clip_on=True,label='Maya+Otomangue')
    #ax.plot([x[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='South America']],[y[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='South America']],'H',color='orange',markersize=5,markeredgewidth=0.5,markeredgecolor=None,alpha=0.85,fillstyle='full',clip_on=True,label='South America')
    #ax.plot([x[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='North America']],[y[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='North America']],'o',color='lime',markersize=5,markeredgewidth=0.5,markeredgecolor=None,alpha=0.85,fillstyle='full',clip_on=True,label='North America')
    
    plt.grid(False)
    plt.title('Clustering for domain '+str(rasgo),fontsize=10)
    ax.set_yticks([])
    ax.set_xticks([])
    #plt.legend(loc='best',fontsize=7)
    plt.ylabel(r'dimension 2',fontsize=10)
    plt.xlabel(r'dimension 1',fontsize=10)
    plt.rcParams.update({'font.size': 10})
    plt.savefig('WINDOWS/Código útil/Intentos de trabajos/Otros/2D/PCA_'+str(rasgo)+'.jpg', format='jpg', transparent=True, bbox_inches='tight',dpi=800)
    plt.show()
# =============================================================================
# 
# =============================================================================

# =============================================================================

# =============================================================================
# 
# =============================================================================

from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

range_n_clusters = [2, 4]
S = []
for n_clusters in range_n_clusters:
    
    cluster = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
    labels = cluster.labels_
    silhouette_avg = silhouette_score(X, labels)
    S.append(silhouette_avg)
    print("For n_clusters =", n_clusters,"The average silhouette_score is :", silhouette_avg)

fig, ax = plt.subplots(dpi=800)

ax.plot(range_n_clusters, S, linewidth=0.5, marker='o',color='orange',markersize=5,markeredgecolor='k',markeredgewidth=1,fillstyle='full',clip_on=True)
plt.xlabel(r'number of clusters',fontsize=12)
plt.ylabel(r'silhoutte coefficient',fontsize=12)
plt.rcParams.update({'font.size': 10})
plt.savefig('C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Otros/2D/pca_evaluacion_custering.pdf', format='pdf', transparent=True, bbox_inches='tight',dpi=800)
plt.show()
# =============================================================================
# =============================================================================
#Guardamos las variables importantes
features_sud_todos= features_pred
features_sud_wcode=features_4
features_sud=features_5
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================

# =============================================================================
# Análisis WALS mundo
# =============================================================================

##Esto corresponde a los mismos valores de Wals(Wals/values.csv)
datos_lenguas = pd.read_csv("C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Wals/values.csv",sep=',')
##Esto corresponde a los datos de lsa lenguas de Wals (Wals/values.csv)
lenguas_areas = pd.read_csv("C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Wals/languages.csv",sep=',',encoding='utf-8')
##Saco las lenguas que son de Sudamerica
lenguas_ID= lenguas_areas[['ID','Name','Glottocode']]
## creamos un diccionario numero:nombre
codigo = [code for code in lenguas_ID['ID']]
nombre = [area for area in lenguas_ID['Name']]
codigo_nombre = [[codigo[i],nombre[i]] for i in range(len(codigo))]
codigo_nombre = {item[0]:item[1] for item in codigo_nombre}
Ubicación_Lenguas = lenguas_areas[lenguas_areas.ID.isin(codigo)]
datos_lenguas = datos_lenguas[datos_lenguas.Language_ID.isin(codigo)]
##definimos los rasgos buscados
rasgos = ["71A","112A", "113A", "143A"]

lenguas_areas= datos_lenguas[datos_lenguas.Parameter_ID.isin(rasgos)]

features_pred = {}

for l in codigo_nombre.keys():
    values_l = lenguas_areas[lenguas_areas['Language_ID']==l]
    D=dict(zip(values_l['Parameter_ID'],values_l['Value']))
    features_pred[l]=D

rasgos_por_lengua = [len(list(features_pred[language].keys()))/float(len(set(rasgos))) for language in features_pred.keys()]


## filtramos los datos leídos

features_pred.values()
## buscamos los rasgos en común
rasgos_comunes = [list(item.keys()) for item in features_pred.values() if len(item)>3]
## intersectamos todos los conjuntos de rasgos sujetos a la condición len(item)>num_rasgos
rasgos_comunes = set(rasgos_comunes[0]).intersection(*rasgos_comunes)
## restringimos D
features_4 = {lengua:{key:features_pred[lengua][key] for key in rasgos_comunes} for lengua in features_pred.keys() if len(features_pred[lengua])>3}

features_pred_glotto_lista = []
features_pred_glotto_lista = lenguas_ID[lenguas_ID.ID.isin(list(features_4.keys()))]
features_5 = dict(zip(features_pred_glotto_lista['Glottocode'], features_4.values()))

features_mundo_todos = features_pred
features_mundo_wcode=features_4
features_mundo=features_5

# =============================================================================
# Clusters con lenguas de sudamerica
# =============================================================================
def hamming3(lengua1, lengua2):
    
    ## rasgos
    features_lengua1= features_sud[lengua1]
    features_lengua2= features_sud[lengua2]
    
    ## hamming!
    d=0
    n=0
    for feature in features_lengua1.keys():
        if feature in features_lengua2.keys(): 
            if features_lengua1[feature] != features_lengua2[feature]:
                d += 1.0
            n += 1.0
            
    return d/n

features_sud_nombre = dict(zip(features_pred_glotto_lista['Name'], features_sud.values()))
# =============================================================================
# features_pred_glotto_lista = lenguas_ID[lenguas_ID.Glottocode.isin(list(features_sud.keys()))]
# dict(zip(features_pred_glotto_lista['Name'], features_sud.values())) 
# =============================================================================
D= features_sud_nombre

D_lenguas = {lengua:{} for lengua in D.keys()}
def hamming_nombre(lengua1, lengua2):
    
    ## rasgos
    features_lengua1= features_sud_nombre[lengua1]
    features_lengua2= features_sud_nombre[lengua2]
    
    ## hamming!
    d=0
    n=0
    for feature in features_lengua1.keys():
        if feature in features_lengua2.keys(): 
            if features_lengua1[feature] != features_lengua2[feature]:
                d += 1.0
            n += 1.0
            
    return d/n

for lengua in D.keys():
    for lengua_lengua in D.keys():
        lengua_feat = D[lengua]
        lengua_lengua_feat = D[lengua_lengua]
        D_lenguas[lengua][lengua_lengua]=hamming_nombre(lengua,lengua_lengua)
X=[]
for language in D_lenguas.keys():
    X+=[list(D_lenguas[language].values())]

from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
model = TSNE(n_components=2, perplexity=15, random_state=0, metric='precomputed',square_distances=True)
X = model.fit_transform(X)
x=list(zip(*list(X)))[0]
y=list(zip(*list(X)))[1]

kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
labels = kmeans.labels_
labels_dict=dict(zip(list(D.keys()),labels))
x=list(zip(*list(X)))[0]
y=list(zip(*list(X)))[1]
import matplotlib.pyplot as plt

   
cmap = plt.get_cmap('RdBu')

fig, ax = plt.subplots(dpi=800)

for i in range(len(x)):
    ax.annotate(list(D.keys())[i], weight='demi', color='k', xy=(x[i],y[i]), fontsize=4, alpha=0.65)
#    ax.annotate(labels[i], weight='demi', color='r', xy=(x[i]-1.5,y[i]-1.5), fontsize=4, alpha=0.85)

ax.plot([x[i] for i in [list(D.keys()).index(language) for language in D.keys() if labels_dict[language]!=1]],[y[i] for i in [list(D.keys()).index(language) for language in D.keys() if labels_dict[language]!=1]],'o',color='gold',markersize=5,markeredgewidth=0.5,markeredgecolor='k',alpha=0.75,fillstyle='full',clip_on=True,label='cluster 0')
ax.plot([x[i] for i in [list(D.keys()).index(language) for language in D.keys() if labels_dict[language]==1]],[y[i] for i in [list(D.keys()).index(language) for language in D.keys() if labels_dict[language]==1]],'H',color='cyan',markersize=5,markeredgewidth=0.5,markeredgecolor='k',alpha=0.75,fillstyle='full',clip_on=True,label='cluster 1')
#ax.plot([x[i] for i in [list(L.keys()).index(language) for language in L.keys() if family[language] in ['Mayan','Otomanguean']]],[y[i] for i in [list(L.keys()).index(language) for language in L.keys() if family[language] in ['Mayan','Otomanguean']]],'X',color='m',markersize=6,markeredgewidth=0.5,markeredgecolor='k',alpha=0.75,fillstyle='full',clip_on=True,label='Maya+Otomangue')
#ax.plot([x[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='South America']],[y[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='South America']],'H',color='orange',markersize=5,markeredgewidth=0.5,markeredgecolor=None,alpha=0.85,fillstyle='full',clip_on=True,label='South America')
#ax.plot([x[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='North America']],[y[i] for i in [list(G.nodes()).index(language) for language in G.nodes() if language in id_family.keys() and macroarea[glotto_iso[language]]=='North America']],'o',color='lime',markersize=5,markeredgewidth=0.5,markeredgecolor=None,alpha=0.85,fillstyle='full',clip_on=True,label='North America')

plt.grid(False)
plt.title('Low dimensional representation of languages of South america',fontsize=10)
ax.set_yticks([])
ax.set_xticks([])
#plt.legend(loc='best',fontsize=7)
plt.ylabel(r'dimension 2',fontsize=10)
plt.xlabel(r'dimension 1',fontsize=10)
plt.rcParams.update({'font.size': 10})
plt.savefig('C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Otros/2D/PCA_Sudamerica.jpg', format='jpg', transparent=True, bbox_inches='tight',dpi=800)
plt.show()

# =============================================================================
# Pruebas con distancias
# =============================================================================

# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Analizar por qué no funciona
# =============================================================================
# dict_group=features_sud
# D = {lang:{} for lang in dict_group.keys() }
# for lang in list(dict_group.keys()):
#     for langlang in dict_group.keys():
#         lenguas = list(dict_group.keys())
#         lenguas_comp = list(dict_group.keys())
#         L = [lenguas,lenguas_comp]
#         pairs = list(itertools.product(*L))
#         for pair in pairs:
#             for lang, v in D.items():
#                 D[lang][langlang] = hamming3(pair[0],pair[1])
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
def hamming4(glotto1,glotto2):
    d = 0
    n = 0
    language1 = features_sud[glotto1]
    language2 = features_sud[glotto2]
    for feat in language1.keys():
        if feat in language2.keys():
            if language1[feat] != language2[feat]:
                d += 1.0
            n += 1.0
    if n==0:
        return n,-1
    else:
        return n,d/n
import networkx as nx
import numpy as np
D = {lengua:{} for lengua in features_sud.keys()}
for lengua in features_sud.keys():
    for lengualengua in features_sud.keys():
        n, H = hamming4(lengua,lengualengua)
        if lengualengua in id_family.keys() and lengua in id_family.keys() and H!=-1:
    
                if n>=4:
                    D[lengua][lengualengua]=H
G=nx.Graph()
for key in D.keys():
    for keykey in D[key].keys():
        if G.has_edge(key,keykey)==False:
            G.add_edge(key,keykey,weight=D[key][keykey])
            
edges = np.mean([item[2]['weight'] for item in list(G.edges(data=True))])
edges_std = np.std([item[2]['weight'] for item in list(G.edges(data=True))])
FAM = {node:id_family[node] for node in G.nodes() if node in id_family.keys()}
v = defaultdict(list)
for key, value in sorted(FAM.items()):
    v[value].append(key)
FAM = dict(v)
FAM = {key:len(FAM[key]) for key in FAM.keys()}
[len(G.nodes()),FAM,edges,edges_std]

# =============================================================================
# =============================================================================
# # 
# =============================================================================
# =============================================================================
features_pred = features_sud
from backbone_network import get_graph_backbone

## grafos!!!
import networkx as nx

def GRAPH_knn(num_rasgos,k):
    
    D = {lengua:{} for lengua in features_pred.keys()}
    for lengua in features_pred.keys():
        for lengualengua in features_pred.keys():
            n,H = hamming4(lengua,lengualengua)
            #if lengualengua in id_family.keys() and lengua in id_family.keys() and id_family[lengua] in F and id_family[lengualengua] in F and H!=-1:    
            if lengualengua in id_family.keys() and lengua in id_family.keys() and H!=-1: 
                if n>=num_rasgos:
                    D[lengua][lengualengua]=1-H
                    
    G=nx.Graph()
    for key in D.keys():
        D_ordered = list({k: v for k, v in sorted(D[key].items(), key=lambda item: item[1],reverse=True)}.items())[1:k+1]
        D_ordered = [item[0] for item in D_ordered]
        for keykey in D_ordered:
            if G.has_edge(key,keykey)==False:
                G.add_edge(key,keykey,weight=D[key][keykey])
    
    return G

graphs = {}
graph_list = []
for num_rasgos in range(1,111):
    G=GRAPH_knn(num_rasgos,5)
    G=get_graph_backbone(G)
    graphs[num_rasgos]=G
    graph_list.append(G)
    
import matplotlib.cm as cm

def plotG(num_rasgos,labels=None):
    fig, ax = plt.subplots(dpi=1080)
    G=graphs[num_rasgos]
    
    #G=nx.maximum_spanning_tree(G,weight='weight')
    #partition = community_louvain.best_partition(G,weight='none',partition={key:id_family[key] for key in G.nodes()})
    #print('número de comunidades: '+str(len(set(partition.values()))))
    #print('modularidad: '+str(community_louvain.modularity(partition, G)))
    print('número de nodos: '+str(len(G)))
    
    pos = nx.nx_pydot.graphviz_layout(G)#nx.kamada_kawai_layout(G)
    ## 
    nodesA = [node for node in G.nodes() if id_family[node]=='araw1281']
    nodesM = [node for node in G.nodes() if id_family[node]=='maya1287']
    nodesQ = [node for node in G.nodes() if id_family[node]=='quec1387']
    nodesP = [node for node in G.nodes() if id_family[node]=='pano1259']
    nodesO = [node for node in G.nodes() if id_family[node]=='otom1299']
    nodesT = [node for node in G.nodes() if id_family[node]=='tupi1275']
    nodesN = [node for node in G.nodes() if id_family[node]=='nucl1710']
    nodesC = [node for node in G.nodes() if id_family[node]=='cari1283']
    nodesU = [node for node in G.nodes() if id_family[node]=='utoa1244']
    nodesCh= [node for node in G.nodes() if id_family[node]=='chib1249']
    nodesB= [node for node in G.nodes() if id_family[node]=='barb1265']
    nodesAy= [node for node in G.nodes() if id_family[node]=='ayma1253']
    #nodesAr= [node for node in G.nodes() if id_family[node]=='arau1255']
    nodesCho= [node for node in G.nodes() if id_family[node]=='chon1288']
    nodesMa= [node for node in G.nodes() if id_family[node]=='mata1289']
    nodesGu= [node for node in G.nodes() if id_family[node]=='guai1249']
    nodesZa= [node for node in G.nodes() if id_family[node]=='zamu1243']

    nodesnonA = [node for node in G.nodes() if id_family[node] not in ['zamu1243','guai1249','mata1289','chon1288','araw1281','quec1387','pano1259','tupi1275','nucl1710','cari1283','chib1249','barb1265','ayma1253']]#,'arau1255']]
    
    if labels is None:
        #nx.draw_networkx_labels(G,pos,labels,alpha=0.95,font_size=5,font_color='k',font_family='monospace')
 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesA, node_size = 40, node_color='orange',node_shape='H',alpha=0.95, linewidths=0.1,label='araw1281') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesM, node_size = 40, node_color='m',node_shape='X', alpha=0.95,linewidths=0.1,label='maya1287') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesQ, node_size = 40, node_color='b',node_shape='o',alpha=0.95, linewidths=0.1,label='quec1387') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesP, node_size = 40, node_color='r',node_shape='s',alpha=0.95, linewidths=0.1,label='pano1259') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesO, node_size = 40, node_color='cyan',node_shape='D',alpha=0.95, linewidths=0.1,label='otom1299') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesT, node_size = 40, node_color='yellow',node_shape='*',alpha=0.95, linewidths=0.1,label='tupi1275') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesN, node_size = 40, node_color='green',node_shape='^',alpha=0.95, linewidths=0.1,label='nucl1710') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesC, node_size = 40, node_color='olive',node_shape='v',alpha=0.95, linewidths=0.1,label='cari1283') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesU, node_size = 40, node_color='lime',node_shape='p',alpha=0.95, linewidths=0.1,label='utoa1244') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesCh, node_size = 40, node_color='crimson',node_shape='<',alpha=0.95, linewidths=0.1,label='chib1249') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesB, node_size = 40, node_color='chocolate',node_shape='>',alpha=0.95, linewidths=0.1,label='barb1265') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesAy, node_size = 40, node_color='slategrey',node_shape='d',alpha=0.95, linewidths=0.1,label='ayma1253') 
        #nx.draw_networkx_nodes(G, pos, nodelist=nodesAr, node_size = 40, node_color='fuchsia',node_shape='8',markeredgecolor='k',alpha=0.95,fillstyle='full', linewidths=0.1,label='arau1255') 
        ##
        nx.draw_networkx_nodes(G, pos, nodelist=nodesCho, node_size = 40, node_color='palegreen',node_shape='h',alpha=0.95, linewidths=0.1,label='chon1288') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesMa, node_size = 40, node_color='steelblue',node_shape='p',alpha=0.95, linewidths=0.1,label='mata1289') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesGu, node_size = 40, node_color='salmon',node_shape='*',alpha=0.95, linewidths=0.1,label='guai1249') 
        nx.draw_networkx_nodes(G, pos, nodelist=nodesZa, node_size = 40, node_color='gold',node_shape='s',alpha=0.95, linewidths=0.1,label='zamu1243') 

        nx.draw_networkx_nodes(G, pos, nodelist=nodesnonA, node_size = 10, node_color='k',alpha=0.25,linewidths=0.1,label='Others') 
        nx.draw_networkx_edges(G, pos, alpha=0.5,width=0.15,edge_color='lightblue')
    else:
        colors = set(labels.values())
        colors_select = ['gold','magenta','yellow','lime','purple','red','mediumblue']
        colors_list = []
        for node in labels.keys():
            colors_list+=[colors_select[labels[node]]]
        nx.draw_networkx_nodes(G, pos, node_size = 40, node_color=colors_list,alpha=0.95,fillstyle='none',linewidths=0.1) 
        nx.draw_networkx_edges(G, pos, alpha=0.5,width=0.15,edge_color='lightblue')
        
    plt.title(str(num_rasgos)+' features'+' and '+str(len(G))+' languages',fontsize=10)
    if labels is None:
        plt.legend(loc='best',fontsize=5)
        plt.savefig('C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Wals/grafos/SA_graph_'+str(num_rasgos)+'.pdf', format='pdf', transparent=True, bbox_inches='tight',dpi=1080)
    else:
        s = len(set(list(labels.values())))
        plt.savefig('C:/Users/fneir/OneDrive/Escritorio/Código útil/Intentos de trabajos/Wals/grafos'+str(s)+'_labeled_graph_'+str(num_rasgos)+'.pdf', format='pdf', transparent=True, bbox_inches='tight',dpi=1080)
    
    plt.axis('on')
    plt.show()
    
plotG(4)

# =============================================================================
# =============================================================================
# NUEVOS CLUSTERS
# =============================================================================
# =============================================================================

# =============================================================================
# =============================================================================
# Distribuciones por rasgo
# =============================================================================
# =============================================================================
