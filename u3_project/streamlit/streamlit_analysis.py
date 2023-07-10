import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import pandas as pd
import networkx as nx
from pyvis.network import Network
import numpy as np

st.title('Análise dos Filmes Originais Netflix ')
st.markdown("""O objetivo do dataset é "brincar" um pouco com os dados, avaliando principalmente as relações dos filmes de gênero Thriller.""")

df = pd.read_csv("https://raw.githubusercontent.com/nataly-enne/network_analysis/main/u3_project/dataset/NetflixOriginals.csv", encoding = "ISO-8859-1")

st.write("Amostra dos dados: ")

st.table(df.head())

st.write("""
Neste dataset os nós representam os filmes, enquanto as arestas representam possíveis relações ou conexões entre esses filmes. 
         Abaixo algumas relações serão mostradas como, por exemplo, a relação por pontuação IMDB.
""")


st.set_option('deprecation.showPyplotGlobalUse', False)


# criando um grafo "normal"
C = nx.Graph()

C.add_nodes_from(df['Title'], ntype='movie')

# add arestas ao grafo com base na coluna genero
for index, row in df.iterrows():
    title = row['Title']
    genres = row['Genre'].split('/')
    for genre in genres:
        C.add_edge(title, genre)

st.markdown("## Grafo")
pos = nx.spring_layout(C, seed=42)
nx.draw(C, with_labels=False, node_color='lightblue', edge_color='gray', pos=pos)
nx.draw_networkx_labels(C, pos, font_size=6)
st.pyplot()

# histograma de distribuição de grau
st.markdown("## Histograma de Distribuição Empírica de Grau")
degree_sequence = [d for n, d in C.degree()]

plt.hist(degree_sequence, bins='auto', alpha=0.7, rwidth=0.85)

plt.xlabel('Grau')
plt.ylabel('Frequência')
plt.title('Histograma de Distribuição Empírica de Grau')

st.pyplot()

# matriz de adjacência
st.markdown("## Matriz de adjacência para os filmes que possuem gênero de ação")

action_genre = 'Action'

# filtra apenas para o gênero de ação
df_filtered = df[df['Genre'].str.contains(action_genre)]

all_genres = set()
for genres in df_filtered['Genre']:
    split_genres = genres.split('/')
    for genre in split_genres:
        all_genres.add(genre)

all_genres = sorted(all_genres)

# cria a matriz de adjacência
adjacency_matrix = np.zeros((len(df_filtered), len(all_genres)), dtype=int)

for i, genres in enumerate(df_filtered['Genre']):
    split_genres = genres.split('/')
    for genre in split_genres:
        j = all_genres.index(genre)
        adjacency_matrix[i, j] = 1

adjacency_df = pd.DataFrame(adjacency_matrix, columns=all_genres)

plt.imshow(adjacency_df.values, cmap='YlGnBu')

# configura os rótulos dos eixos x e y
plt.xticks(ticks=range(len(all_genres)), labels=all_genres, rotation=45)
plt.yticks(ticks=range(len(df_filtered)), labels=df_filtered['Title'])

plt.colorbar()
st.pyplot()


st.markdown("## Relação entre os filmes com base na pontuação do IMDB")

G = nx.Graph()

# faixas de pontuação
faixas = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]

# percorre o dataset e adiciona os nós das faixas de pontuação ao grafo
for faixa in faixas:
    G.add_node(faixa)

# percorre o dataset e adiciona as arestas entre os filmes/séries da mesma faixa de pontuação
for i in range(len(df)):
    pontuacao = df.loc[i, 'IMDB Score']
    for faixa in faixas:
        if faixa[0] <= pontuacao < faixa[1]:
            G.add_edge(faixa, df.loc[i, 'Title'])
            break

pos = nx.spring_layout(G)

node_colors = ['#FF0000', '#FFA500', '#FFFF00', '#00FF00', '#00FFFF']

# plot do grafo
plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, nodelist=faixas, node_color=node_colors, node_size=1000)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

for i, faixa in enumerate(faixas):
    plt.scatter([], [], c=node_colors[i], label=f'{faixa[0]}-{faixa[1]}')
plt.legend(title='Faixas de Pontuação')

plt.title('Relação entre Pontuação IMDB e Filmes')
plt.tight_layout()
st.pyplot()

# engeinvector centrality
st.markdown("## Engeinvector centrality utilizando a faixa em relação ao IMDB Score")

eigenvector_centrality = nx.eigenvector_centrality(G)

plt.figure(figsize=(5, 5))

color_map = [eigenvector_centrality[node] for node in G.nodes()]

pos = nx.spring_layout(G, seed=42)
cmap = plt.cm.viridis  
nx.draw(G, with_labels=False, pos=pos, node_color=color_map, edge_color='gray', cmap=cmap)
nx.draw_networkx_labels(G, pos, font_size=6)

sm = cm.ScalarMappable(cmap=cmap)
sm.set_array([])
cbar = plt.colorbar(sm)
cbar.set_label('Eigenvector Centrality')
st.pyplot()

# degree centrality

st.markdown("## Centralidade de grau para cada nó no grafo")
degree_centrality = nx.degree_centrality(C)

plt.figure(figsize=(10, 10))

color_map = [degree_centrality[node] for node in C.nodes()]

pos = nx.spring_layout(C, seed=42)
cmap = mpl.colormaps['rainbow']
nx.draw(C, with_labels=False, pos=pos, node_color=color_map, edge_color='gray', cmap=cmap)
nx.draw_networkx_labels(C, pos, font_size=6)

sm = cm.ScalarMappable(cmap=cmap)
sm.set_array([])
cbar = plt.colorbar(sm)
cbar.set_label('Degree Centrality')
st.pyplot()

# closeness centrality

st.markdown("## Aqui vemos a a centralidade de proximidade do grafo todo")

closeness_centrality = nx.closeness_centrality(C)

plt.figure(figsize=(5, 5))

color_map = [closeness_centrality[node] for node in C.nodes()]

pos = nx.spring_layout(C, seed=42)
cmap = plt.cm.viridis  
nx.draw(C, with_labels=False, pos=pos, node_color=color_map, edge_color='gray', cmap=cmap)
nx.draw_networkx_labels(C, pos, font_size=6)

sm = cm.ScalarMappable(cmap=cmap)
sm.set_array([])
cbar = plt.colorbar(sm)
cbar.set_label('Closeness Centrality')
st.pyplot()

# betweenness centrality

st.markdown("## Visualizando nós por Betweenness Centrality")
st.write("Aqui vemos o cálculo da importância de um nó como intermediário nas conexões entre outros pares de nós no grafo.")
st.write("Além disso, é possível ver que o gênero \'Comedy\' possui a maior centralidade de intermediação")

betweenness_centrality = nx.betweenness_centrality(C)

plt.figure(figsize=(5, 5))

color_map = [betweenness_centrality[node] for node in C.nodes()]

pos = nx.spring_layout(C, seed=42)
cmap = plt.cm.viridis  
nx.draw(C, with_labels=False, pos=pos, node_color=color_map, edge_color='gray', cmap=cmap)
nx.draw_networkx_labels(C, pos, font_size=6)

sm = cm.ScalarMappable(cmap=cmap)
sm.set_array([])
cbar = plt.colorbar(sm)
cbar.set_label('Betweenness Centrality')
st.pyplot()

# grafo pizza

st.markdown("## Distribuição de filmes do Gênero Thriller contra o Comedy")
st.write("O percentual de filmes Comedy (90%) é cerca de nove vezes maior que o de Thriller (10%)")

C = nx.Graph()

C.add_nodes_from(df['Title'], ntype='movie')

# add arestas ao grafo com base na coluna genero
for index, row in df.iterrows():
    title = row['Title']
    genres = row['Genre'].split('/')
    for genre in genres:
        C.add_edge(title, genre)

thriller_count = sum(1 for node in C.nodes() if 'Thriller' in node)
comedy_count = sum(1 for node in C.nodes() if 'Comedy' in node)

values = [thriller_count, comedy_count]

labels = ['Thriller', 'Comedy']

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)

#  aspecto para 'equal' para garantir que seja um círculo
ax.axis('equal')

ax.set_title('Porcentagem de Filmes - Thriller vs Comedy')

st.pyplot()


# pyviz
st.markdown("## Visualização do Pyviz")

# cria uma instância da classe network
nt = Network('1000px', '1000px', notebook=True, bgcolor="#222222", font_color="white", filter_menu=True)

for node in df['Title']:
    nt.add_node(node, label=node)

nt.barnes_hut()
nt.show("graph.html")

HtmlFile = open("graph.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code, height = 500)