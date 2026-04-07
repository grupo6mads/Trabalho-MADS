# -*- coding: utf-8 -*-
"""Restaurantes_Notebook.ipynb

#Gestão de Rating

#Este Script Serve para gerir os dados de múltiplos restaurantes
- **Dados Restaurantes (Nome, NIF, Preço, Avaliação, Tipo, Rating)**
- **Calcula o Rating**
- **Alterar o Preço e Avaliação.**
- **Grafico para mostrar o Histórico do Rating**
- **Grafico para mostrar o Histórico atemporal do Rating**

# Bibliotecas
"""

import datetime
import matplotlib.pyplot as plt
import pandas as pd
import folium

"""# Armazenar"""

# Lista para armazenar os dados das restaurantes
restaurantes = {}
# Lista para armazenar dados históricos (preço e avaliação ao longo do tempo)
historico_dados = []
# Lista para armazenar os dados dos clientes
clientes = {}
# Lista para armazenar os dados dos menus
menus = {}
# Lista para armazenar os dados do pedidos
pedidos = []

"""# Função Gerir Restaurantes"""

def add_restaurante(nome, nif, preco, avaliacao, tipo, localizacao, lat, lon):
    """ Adiciona uma nova restaurante garantindo integridade dos dados """
    if nif in restaurantes:
        print("Erro: O NIF introduzido já se encontra registado no sistema!")
        return
    if len(nif) > 15:
        print("Erro: O NIF deve ter no máximo 15 caracteres.")
        return
    if preco <= 0 or avaliacao <= 0:
        print("Erro: Preço e avaliação devem conter valores positivos.")
        return
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        print("Erro: Coordenadas inválidas.")
        return

    restaurantes[nif] = {
    "Nome": nome,
    "NIF": nif,
    "Preco": preco,
    "Tipo": tipo,
    "Avaliacão": avaliacao, # Alterado para 'Avaliacão' com cedilha
    "Rating": rating(preco, avaliacao),
    "CriadoEm": datetime.datetime.now(),
    "Localizacao": localizacao,
    "Lat": lat,
    "Lon": lon,
    }
    print(f"Restaurante adicionado com sucesso! Nome: {nome}, NIF: {nif}")

def rating(preco, avaliacao):
    """ Calcula o Rating do restaurante com base na avaliação e no preço, sendo que quanto
    mais alta for a a avaliação e mais baixo o preço, melhor o rating"""
    rating = (avaliacao * 10) / preco
    return rating

def add_dados(nome, nif, preco, avaliacao, data_hora, localizacao, lat, lon):
    """ Inserção de dados para preços e avaliações com a utilização do NIF"""

    # Verificação do NIF
    if nif not in restaurantes:
        print(f"Erro: NIF '{nif}' não está registado.")
        return

    # Verificar Nome
    if nome != restaurantes[nif]["Nome"]:
      print(f"XABLAu")
      return

    # Preço e avaliaçºao
    if preco <= 0 or avaliacao <= 0:
        print("Erro: Preço e avaliação devem ser positivos.")
        return

    # Interpretar a data inserida
    if data_hora is None:
        data_obj = datetime.datetime.now()
        data_str = data_obj.strftime("%Y-%m-%d %H:%M:%S")
    else:
        try:
            data_obj = datetime.datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
            data_str = data_hora
        except ValueError:
            print("Erro: Formato inválido. Use 'YYYY-MM-DD HH:MM:SS'.")
            return

    # Verificar se a data é anterior à criação do restaurante
    data_criacao = restaurantes[nif].get("CriadoEm")
    if data_criacao and data_obj < data_criacao:
        print(f"Erro: A data fornecida ({data_str}) é anterior à data de criação do restaurante ({data_criacao.strftime('%Y-%m-%d %H:%M:%S')}).")
        return

    # Registar no histórico
    historico_dados.append({
        "Nome": nome,
        "NIF": nif,
        "Preco": preco,
        "Avaliacão": avaliacao,
        "Rating": rating(preco, avaliacao),
        "Timestamp": data_str,
        "Localizacao": localizacao,
        "Lat": lat,
        "Lon": lon

    })
    print(f"Dados atualizados para {nome} (NIF: {nif}) em {data_str}")

"""# Função Gerir Clientes

"""

def add_cliente(nome, id_cliente):
    """Adiciona um cliente ao sistema"""
    if id_cliente in clientes:
        print("Erro: Cliente já existe.")
        return

    clientes[id_cliente] = {
        "Nome": nome,
        "ID": id_cliente,
        "CriadoEm": datetime.datetime.now()
    }
    print(f"Cliente '{nome}' adicionado com sucesso.")

"""# Função Gerir Menus

"""

def add_menu(id_menu, nome):
    """Cria um menu (catálogo de opções)"""

    if id_menu in menus:
        print("Erro: Menu já existe.")
        return

    menus[id_menu] = {
        "Nome": nome,
        "Itens": []
    }

    print(f"Menu '{nome}' criado com sucesso.")
def add_item_menu(id_menu, nome_item, preco):
    """Adiciona um item (prato) a um menu"""

    if id_menu not in menus:
        print("Erro: Menu não existe.")
        return

    if preco <= 0:
        print("Erro: Preço inválido.")
        return

    menus[id_menu]["Itens"].append({
        "Nome": nome_item,
        "Preco": preco
    })

    print(f"Item '{nome_item}' adicionado ao menu.")
def historico_restaurante(nif):
    """Mostra histórico de pedidos de um restaurante"""
    hist = [p for p in pedidos if p["Restaurante"] == nif]

    if not hist:
        print("Sem histórico.")
        return

    df = pd.DataFrame(hist)
    print(df)

"""# Função para Associar Menus a Restaurantes"""

def add_menu_restaurante(nif, id_menu):
    """Associa um menu a um restaurante"""
    if nif not in restaurantes:
        print("Erro: Restaurante não existe.")
        return

    if id_menu not in menus:
        print("Erro: Menu não existe.")
        return

    if "Menus" not in restaurantes[nif]:
        restaurantes[nif]["Menus"] = []

    restaurantes[nif]["Menus"].append(id_menu)
    print("Menu associado ao restaurante com sucesso.")

"""# Função de adição de pedidos por Cliente"""

def add_pedido(id_cliente, nif_restaurante, id_menu, index_item):
    """Regista pedido com base num item de um menu de um restaurante"""

    # Validações básicas
    if id_cliente not in clientes:
        print("Erro: Cliente não existe.")
        return

    if nif_restaurante not in restaurantes:
        print("Erro: Restaurante não existe.")
        return

    if id_menu not in menus:
        print("Erro: Menu não existe.")
        return

    # validar se o menu pertence ao restaurante
    if "Menus" not in restaurantes[nif_restaurante] or id_menu not in restaurantes[nif_restaurante]["Menus"]:
        print("Erro: Este menu não pertence ao restaurante.")
        return

    itens = menus[id_menu]["Itens"]

    if not itens:
        print("Erro: Menu sem itens.")
        return

    if index_item < 0 or index_item >= len(itens):
        print("Erro: Item inválido.")
        return

    item = itens[index_item]

    # Pedido mais completo (melhor para histórico e análise)
    pedido = {
        "Cliente_ID": id_cliente,
        "Cliente_Nome": clientes[id_cliente]["Nome"],

        "Restaurante_NIF": nif_restaurante,
        "Restaurante_Nome": restaurantes[nif_restaurante]["Nome"],

        "Menu_ID": id_menu,
        "Menu_Nome": menus[id_menu]["Nome"],

        "Item_Nome": item["Nome"],
        "Preco": item["Preco"],

        "Data": datetime.datetime.now()
    }

    pedidos.append(pedido)
    print("Pedido registado com sucesso.")

"""# Funções para Listas"""

def list_restaurantes():
    """ Lista todos os restaurantes registados """
    if not restaurantes:
        print("Nenhum restaurante registado.")
        return

    df = pd.DataFrame([{**{"NIF": nif}, **dados} for nif, dados in restaurantes.items()])
    df = df[["Nome", "NIF", "Preco", "Avaliacao", "Tipo", "Rating", "Localizacao", "Lat","Lon"]]
    print(df)

def list_by_rating_decrescente():
    """ Lista restaurantes ordenadas pelo rating de forma decrescente """
    df = pd.DataFrame([{**{"NIF": nif}, **dados} for nif, dados in restaurantes.items()]).sort_values(by="Rating", ascending=False)
    df = df[["Nome", "NIF", "Preco", "Avaliacao", "Tipo", "Rating", "Localizacao", "Lat","Lon"]]
    print(df)

def list_by_crit_rating():
    """ Lista restaurantes com rating fora da faixa saudável (Rating > 25 ou < 18.5) """
    df = pd.DataFrame([{**{"NIF": nif}, **dados} for nif, dados in restaurantes.items()]).sort_values(by="Rating", ascending=False)
    df = df[["Nome", "NIF", "Preco", "Avaliacao", "Tipo", "Rating", "Localizacao", "Lat","Lon"]]
    df_crit = df[(df["Rating"] > 25) | (df["Rating"] < 18.5)]
    print(df_crit)
def listar_clientes():
    """Lista todos os clientes registados"""

    if not clientes:
        print("Não existem clientes registados.")
        return

    df = pd.DataFrame(clientes.values())
    print(df)
def listar_pedidos_cliente(id_cliente):
    """Lista todos os pedidos de um cliente"""

    if id_cliente not in clientes:
        print("Erro: Cliente não existe.")
        return

    pedidos_cliente = [p for p in pedidos if p["Cliente"] == id_cliente]

    if not pedidos_cliente:
        print("Este cliente não tem pedidos.")
        return

    df = pd.DataFrame(pedidos_cliente)
    print(df)
def listar_menus():
    """Lista todos os menus com os seus itens"""

    if not menus:
        print("Não existem menus.")
        return

    for id_menu, menu in menus.items():
        print(f"\nMenu {id_menu} - {menu['Nome']}")

        if not menu["Itens"]:
            print("  (sem itens)")
        else:
            for i, item in enumerate(menu["Itens"], 1):
                print(f"  {i}. {item['Nome']} - {item['Preco']}€")
def listar_menus_restaurante(nif):
    """Lista menus e itens de um restaurante"""

    if nif not in restaurantes:
        print("Erro: Restaurante não existe.")
        return

    if "Menus" not in restaurantes[nif]:
        print("Sem menus.")
        return

    for id_menu in restaurantes[nif]["Menus"]:
        menu = menus[id_menu]

        print(f"\nMenu: {menu['Nome']}")

        for i, item in enumerate(menu["Itens"], 1):
            print(f"  {i}. {item['Nome']} - {item['Preco']}€")

"""# Funções para Análise de Dados"""

def tabela_avaliacao():
    """ Demonstra uma tabela com a avaliação de todos os restaurantes registados """
    df = pd.DataFrame([{**{"NIF": nif}, **dados} for nif, dados in restaurantes.items()])
    df = df[["Nome", "NIF", "Avaliacao"]]
    print(df)

def tabela_preco():
    """ Demonstra uma tabela com o preço de todos os restaurantes registados """
    df = pd.DataFrame([{**{"NIF": nif}, **dados} for nif, dados in restaurantes.items()])
    df = df[["Nome", "NIF", "Preco"]]
    print(df)

def historico_rating(nif):
    """ Mostra gráfico de histórico de rating com datas exatas inseridas """
    import matplotlib.dates as mdates

    df = pd.DataFrame(historico_dados)
    df_restaurante = df[df["NIF"] == nif].copy()

    if df_restaurante.empty:
        print(f"Nenhum dado encontrado para o NIF '{nif}'.")
        return

    # Converter e ordenar
    df_restaurante["Timestamp"] = pd.to_datetime(df_restaurante["Timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    df_restaurante = df_restaurante.sort_values("Timestamp")

    nome = restaurantes[nif]["Nome"]

    # Configurar figura
    plt.figure(figsize=(10, 5))
    plt.plot(df_restaurante["Timestamp"], df_restaurante["Rating"], marker='o', linestyle='-', color="#007acc", label="Rating")

    # Formatação eixos
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    # Estética
    plt.title(f"Histórico de Rating de {nome} (NIF: {nif})", fontsize=14, weight="bold")
    plt.xlabel("Data e Hora", fontsize=12)
    plt.ylabel("Rating", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.legend()
    plt.show()

def historico_rating_atemporal(nif):
    """ Mostra gráfico de Rating por ordem de inserção (atemporal) """
    df = pd.DataFrame(historico_dados)
    df_restaurante = df[df["NIF"] == nif].copy()

    if df_restaurante.empty:
        print(f"Sem dados para o NIF '{nif}'.")
        return

    nome = restaurantes[nif]["Nome"]

    # Gerar eixo X baseado na ordem de inserção
    df_restaurante = df_restaurante.sort_values(by="Timestamp")
    df_restaurante.reset_index(drop=True, inplace=True)
    df_restaurante["Ordem"] = df_restaurante.index + 1

    plt.figure(figsize=(10, 5))
    plt.plot(df_restaurante["Ordem"], df_restaurante["Rating"], marker='o', linestyle='-', color="#007acc", label="Rating")
def listar_menus_restaurante(nif):
    """Lista menus e itens de um restaurante"""

    if nif not in restaurantes:
        print("Erro: Restaurante não existe.")
        return

    if "Menus" not in restaurantes[nif]:
        print("Sem menus.")
        return

    for id_menu in restaurantes[nif]["Menus"]:
        menu = menus[id_menu]

        print(f"\nMenu: {menu['Nome']}")

        for i, item in enumerate(menu["Itens"], 1):
            print(f"  {i}. {item['Nome']} - {item['Preco']}€")


    plt.title(f"Evolução de Rating (ordem de inserção) - {nome} (NIF: {nif})", fontsize=14, weight="bold")
    plt.xlabel("Medição", fontsize=12)
    plt.ylabel("Rating", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(df_restaurante["Ordem"])
    plt.tight_layout()
    plt.legend()
    plt.show()

"""# Integridade"""

def testar_integridade():
    """Testa integridade dos dados do sistema"""
    erros = []

    print("Verificando integridade de restaurantes...")

    for nif, dados in restaurantes.items():
        if len(nif) > 15:
            erros.append(f"NIF '{nif}' tem mais de 15 caracteres.")

        campos_esperados = ["Nome", "Preco", "Avaliacão", "Tipo", "Rating"]
        for campo in campos_esperados:
            if campo not in dados:
                erros.append(f"Campo '{campo}' ausente para NIF '{nif}'.")

        # Verificar valores
        preco = dados.get("Preco", 0)
        avaliacao = dados.get("Avaliacão", 0) # Corrigido para 'Avaliacão' com cedilha
        rating_registrado = dados.get("Rating", 0)
        rating_calculado = rating(preco, avaliacao)

        if not isinstance(preco, (int, float)) or preco <= 0:
            erros.append(f"Preco inválido para NIF '{nif}'.")

        if not isinstance(avaliacao, (int, float)) or avaliacao <= 0:
            erros.append(f"Avaliação inválida para NIF '{nif}'.")

        if abs(rating_registrado - rating_calculado) > 0.1:
            erros.append(f"Rating divergente para NIF '{nif}': registrado={rating_registrado}, calculado={rating_calculado}")

    print("Verificando integridade do histórico de dados...")

    for idx, entrada in enumerate(historico_dados):
        nif = entrada.get("NIF")
        nome = entrada.get("Nome")
        preco = entrada.get("Preco")
        avaliacao = entrada.get("Avaliacão") # Corrigido para 'Avaliacão' com cedilha
        rating_val = entrada.get("Rating")
        ts = entrada.get("Timestamp")

        if nif not in restaurantes:
            erros.append(f"Histórico #{idx}: NIF '{nif}' não cadastrado.")

        elif restaurantes[nif]["Nome"] != nome:
            erros.append(f"Histórico #{idx}: Nome '{nome}' não corresponde ao NIF '{nif}'.")

        if abs(rating(preco, avaliacao) - rating_val) > 0.1:
            erros.append(f"Histórico #{idx}: Rating inconsistente.")

        # Verifica timestamp
        try:
            datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        except:
            erros.append(f"Histórico #{idx}: Timestamp inválido '{ts}'.")

    if not erros:
        print("Todos os dados estão consistentes.")
    else:
        print(f"Foram encontrados {len(erros)} problemas:")
        for erro in erros:
            print(erro)



"""# Mapa"""

def mapa_restaurantes(zona):
    """Mostra no mapa os restaurantes de uma zona"""

    filtrados = []

    for nif, r in restaurantes.items():
        if (
            "Localizacao" in r and
            "Lat" in r and
            "Lon" in r and
            r["Localizacao"].lower() == zona.lower()
        ):
            filtrados.append(r)

    if not filtrados:
        print("Sem restaurantes nesta zona.")
        return

    # Centro do mapa
    centro = [filtrados[0]["Lat"], filtrados[0]["Lon"]]

    mapa = folium.Map(
    location=centro,
    zoom_start=13,
    tiles="CartoDB positron",
    min_zoom=5,   # impede zoom demasiado afastado
    max_zoom=18,   # controla zoom máximo

    max_bounds=True  # impede arrastar infinito
)

    # Adicionar restaurantes
    for r in filtrados:

        popup_text = f"""
        <b>{r['Nome']}</b><br>
        Tipo: {r['Tipo']}<br>
        Rating: {r['Rating']}
        """

        folium.Marker(
            location=[r["Lat"], r["Lon"]],
            popup=popup_text,
            tooltip=r["Nome"],
            icon=folium.Icon(color="blue", icon="cutlery", prefix="fa")
        ).add_to(mapa)

    return mapa
