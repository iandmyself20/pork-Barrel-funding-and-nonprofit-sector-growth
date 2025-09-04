#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import unicodedata 


# In[3]:


import numpy as np
print(np.__version__)


# In[4]:


from fuzzywuzzy import process


# In[5]:


def remove_special_and_accented_characters(df):
    cleaned_df = df.copy()
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'O':  # 'O' represents object data type (strings)
            cleaned_df[col] = cleaned_df[col].apply(lambda x: ''.join(char for char in unicodedata.normalize('NFKD', str(x)) if unicodedata.category(char) != 'Mn'))
    return cleaned_df


# # Dependent variable 1 - importing number of nonprofits 
# 
# Number of health nonprofits registered at IPEA CSOMap  Source:https://mapaosc.ipea.gov.br/base-dados

# In[304]:


Nonprofits = pd.read_excel(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\Mapa_OSC\Mapa OSC area_subarea.xlsx", engine='openpyxl' )


# In[305]:


HealthNonprofits = Nonprofits[Nonprofits['saude'] == 1]


# In[306]:


HealthNonprofits = HealthNonprofits[['dt_fundacao_osc', 'edmu_cd_municipio']]


# In[307]:


HealthNonprofits['edmu_cd_municipio'] = HealthNonprofits['edmu_cd_municipio'].astype(int)
HealthNonprofits.rename(columns={'edmu_cd_municipio':'IBGE7'}, inplace=True)


# In[308]:


# Converter a coluna dt_fundacao_osc para datetime, se necessário, e extrair o ano
HealthNonprofits['Ano'] = pd.to_datetime(HealthNonprofits['dt_fundacao_osc']).dt.year

# Pivotar o DataFrame com IBGE como índice e anos como colunas
pivot_HealthNonprofits = HealthNonprofits.pivot_table(index='IBGE7', columns='Ano', values='dt_fundacao_osc', aggfunc='count', fill_value=0)

# Substituir valores diferentes de 0 por 1
pivot_HealthNonprofits = pivot_HealthNonprofits.applymap(lambda x: 1 if x > 0 else 0)

# Resetar o índice se necessário
pivot_HealthNonprofits.reset_index(inplace=True)

# Adicionar o prefixo "OSC" antes das colunas de ano
pivot_HealthNonprofits.rename(
    columns={col: f"HealthOSC{col}" for col in pivot_HealthNonprofits.columns if isinstance(col, int)},
    inplace=True
)

# Exibir as primeiras linhas para verificar
pivot_HealthNonprofits.head()


# In[309]:


# Criar a coluna TotalOSC2015 somando OSC2015 e os valores das colunas anteriores
pivot_HealthNonprofits['TotalHealthOSC2015'] = pivot_HealthNonprofits.filter(like='HealthOSC').loc[:, :'HealthOSC2015'].sum(axis=1)

# Iterar pelos anos subsequentes para criar as colunas TotalOSC2016 até TotalOSC2020
for year in range(2016, 2021):
    pivot_HealthNonprofits[f'TotalHealthOSC{year}'] = (
        pivot_HealthNonprofits[f'TotalHealthOSC{year - 1}'] + pivot_HealthNonprofits[f'HealthOSC{year}']
    )

# Exibir as primeiras linhas do DataFrame atualizado
pivot_HealthNonprofits.head()


# In[310]:


# Somar os valores da coluna 'TotalOSC2015'
soma_2015 = pivot_HealthNonprofits['TotalHealthOSC2015'].sum()

# Exibir o resultado
print(f"A soma dos valores da coluna 'TotalHealthOSC2015' é: {soma_2015}")


# In[311]:


# Selecionar apenas as colunas desejadas
colunas_desejadas = [
    'IBGE7', 
    'HealthOSC2015', 'HealthOSC2016', 'HealthOSC2017', 'HealthOSC2018', 'HealthOSC2019', 'HealthOSC2020', 
    'TotalHealthOSC2015', 'TotalHealthOSC2016', 'TotalHealthOSC2017', 'TotalHealthOSC2018', 'TotalHealthOSC2019', 'TotalHealthOSC2020'
]

# Manter apenas as colunas selecionadas
HealthNonprofitsdf = pivot_HealthNonprofits[colunas_desejadas]

# Exibir o DataFrame final
HealthNonprofitsdf.head()


# In[312]:


# Contar o número de valores únicos na coluna IBGE
num_municipalities = pivot_HealthNonprofits['IBGE7'].nunique()

# Calcular a porcentagem em relação ao total de municípios
percentage_municipalities = (num_municipalities / 5570) * 100

# Exibir o resultado com as frases desejadas
print(f"Number of municipalities with healthnonprofits: {num_municipalities}")
print(f"Percentage to total municipalities: {percentage_municipalities:.2f}%")


# # Dependent Variable 2 - health nonprofits procedures
# 
# Number of health procedures presented by nonprofits at the System of Ambulatorial Information - SIA and System of Hospitalar Information - SIH of the Ministry of Health.
# 
# Source:https://portalfns.saude.gov.br/conheca-os-valores-para-apresentacao-de-propostas-ao-ms-em-2023/
# 

# In[50]:


ProceduresNonprofits2015 = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\MAC2015OSC.csv", delimiter=";")


# In[51]:


ProceduresNonprofits2016 = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\MAC2016OSC.csv", delimiter=";")


# In[52]:


ProceduresNonprofits2017 = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\MAC2017OSC.csv", delimiter=";")


# In[53]:


ProceduresNonprofits2018 = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\MAC2018OSC.csv", delimiter=";")


# In[54]:


ProceduresNonprofits2019 = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\MAC2019OSC.csv", delimiter=";")


# In[55]:


ProceduresNonprofits2020 = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\MAC2020OSC.csv", delimiter=";")


# In[57]:


ProceduresNonprofits2021 = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\MAC2021OSC.csv", delimiter=";")


# In[79]:


ProceduresNonprofits2021


# In[153]:


def groupby_sum_mac(df, year):
    col = f"MAC{year}"
    return df.groupby('IBGE', as_index=False)[col].sum()


# In[154]:


grouped_mac = {}

for year in range(2015, 2022):
    df_name = f"ProceduresNonprofits{year}"
    df = globals()[df_name]  # acessa o DataFrame com o nome como string
    grouped_mac[year] = groupby_sum_mac(df, year)


# In[155]:


df_mac = pd.concat([
    df.assign(Ano=year).rename(columns={f"MAC{year}": "MAC"} if f"MAC{year}" in df.columns else {})
    for year, df in grouped_mac.items()
], ignore_index=True)


# In[156]:


MACOSC = df_mac.pivot(index='IBGE', columns='Ano', values='MAC')
MACOSC.columns = [f"MAC{int(col)}" for col in MACOSC.columns]
MACOSC.reset_index(inplace=True)


# In[157]:


MACOSC


# In[158]:


MACOSC['MAC2015'] = MACOSC['MAC2015'].fillna(0).astype(int)
MACOSC['MAC2016'] = MACOSC['MAC2016'].fillna(0).astype(int)
MACOSC['MAC2017'] = MACOSC['MAC2017'].fillna(0).astype(int)
MACOSC['MAC2018'] = MACOSC['MAC2018'].fillna(0).astype(int)
MACOSC['MAC2019'] = MACOSC['MAC2019'].fillna(0).astype(int)
MACOSC['MAC2020'] = MACOSC['MAC2020'].fillna(0).astype(int)
MACOSC['MAC2021'] = MACOSC['MAC2021'].fillna(0).astype(int)


# In[159]:


MACOSC


# # Dependent Variable 3 - health nonprofits employment
# 
# Number of employees at health nonprofits - filtered by health related CNAE 8610, 8630,8650,8660. RAIS/MTE
# 
# Natureza Jurídica igual a Outros Fundação Privada, Organização Religiosa, Organização Social (OS), Outras Organizações - Associação Privada
# CNAE 2.0 Classe igual a Atividades de atendimento hospitalar, Atividades de atenção ambulatorial executadas por médicos e odontólogos, Atividades de profissionais da área de saúde, exceto médicos e odontólogos, Atividades de apoio à gestão de saúde, Atividades de assistência psicossocial e à saúde a portadores de distúrbios psíquicos, deficiência mental e dependência química, Atividades de atenção à saúde humana não especificadas anteriormente
# 
# Source: RAIS/MTE -  https://bi.mte.gov.br/bgcaged/caged_rais_vinculo_id_2021/caged_rais_vinculo_basico_2021_tab.php

# In[161]:


RAISOSC = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\Mapa_OSC\RAISOSC.csv", delimiter=";")


# In[261]:


from difflib import get_close_matches

IBGE = pd.read_csv(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\IBGE\dadosibge.csv', encoding = 'latin1', delimiter=";", index_col=False, dtype={'IBGE': np.int64,'Municipio': object})


# Normalize function: remove accents, uppercase, and trim
def normalize(text):
    if pd.isna(text):
        return ""
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.upper())
        if unicodedata.category(c) != 'Mn'
    ).strip()

# Normalize columns
RAISOSC['UF'] = RAISOSC['UF'].astype(str)
IBGE['UF'] = IBGE['UF'].astype(str)
RAISOSC['MUNICIPIO_NORM'] = RAISOSC['MUNICIPIO'].apply(normalize)
IBGE['MUNICIPIO_NORM'] = IBGE['MUNICIPIO'].apply(normalize)

# Fuzzy matching function
def find_closest_municipio(row, ibge_df, cutoff=0.4):
    uf = row['UF']
    municipio = row['MUNICIPIO_NORM']
    
    # Filter IBGE by UF
    candidatos = ibge_df[ibge_df['UF'] == uf]['MUNICIPIO_NORM'].tolist()
    
    match = get_close_matches(municipio, candidatos, n=1, cutoff=cutoff)
    return match[0] if match else None

# Apply fuzzy matching to RAISOSC
RAISOSC['MUNICIPIO_MATCH_NORM'] = RAISOSC.apply(
    lambda row: find_closest_municipio(row, IBGE, cutoff=0.4), axis=1
)

# Merge to bring in the IBGE code using normalized names
RAISOSC_COM_IBGE = pd.merge(
    RAISOSC,
    IBGE[['UF', 'MUNICIPIO_NORM', 'IBGE']],  # include IBGE code explicitly
    how='left',
    left_on=['UF', 'MUNICIPIO_MATCH_NORM'],
    right_on=['UF', 'MUNICIPIO_NORM']
)

# Preview the result
print(RAISOSC_COM_IBGE[['UF', 'MUNICIPIO', 'MUNICIPIO_MATCH_NORM', 'IBGE']].head())


# In[294]:


# Dicionário completo com os 85 municípios e seus códigos IBGE para correção manual
correcoes_manuais.update({
    ('PE', 'BEZERROS'): 2601508,
    ('PE', 'BREJINHO'): 2601607,
    ('PE', 'BUIQUE'): 2601904,
    ('PE', 'CABO DE SANTO AGOSTINHO'): 2602506,
    ('PE', 'CAMARAGIBE'): 2602902,
    ('PE', 'CARUARU'): 2604106,
    ('PE', 'CATENDE'): 2604502,
    ('PE', 'ESCADA'): 2605202,
    ('PE', 'GARANHUNS'): 2606002,
    ('PE', 'GOIANA'): 2606309,
    ('PE', 'IGARASSU'): 2606507,
    ('PE', 'ITAIBA'): 2607604,
    ('PE', 'ILHA DE ITAMARACA'): 2607604,
    ('PE', 'JABOATAO DOS GUARARAPES'): 2607901,
    ('PE', 'LIMOEIRO'): 2609105,
    ('PE', 'MORENO'): 2611606,
    ('PE', 'NAZARE DA MATA'): 2612307,
    ('PE', 'OLINDA'): 2609600,
    ('PE', 'OURICURI'): 2609907,
    ('PE', 'PALMARES'): 2610004,
    ('PE', 'PAULISTA'): 2610707,
    ('PE', 'PESQUEIRA'): 2610905,
    ('PE', 'PETROLANDIA'): 2611002,
    ('PE', 'PETROLINA'): 2611101,
    ('PE', 'POCAO'): 2611200,
    ('PE', 'RECIFE'): 2611606,
    ('PE', 'RIBEIRAO'): 2611804,
    ('PE', 'SALGUEIRO'): 2612000,
    ('PE', 'SAO LOURENCO DA MATA'): 2612406,
    ('PE', 'SERRA TALHADA'): 2613909,
    ('PE', 'SURUBIM'): 2614501,
    ('PE', 'TIMBAUBA'): 2615607,
    ('PE', 'VERTENTES'): 2616001,
    ('PE', 'VICENCIA'): 2616100,
    ('PE', 'VITORIA DE SANTO ANTAO'): 2616308,
    ('SE', 'AQUIDABA'): 2800308,
    ('SE', 'ARACAJU'): 2800100,
    ('SE', 'CAPELA'): 2801306,
    ('SE', 'ESTANCIA'): 2802106,
    ('SE', 'FREI PAULO'): 2802403,
    ('SE', 'ITABAIANA'): 2802908,
    ('SE', 'ITABAIANINHA'): 2803005,
    ('SE', 'JAPOATA'): 2803203,
    ('SE', 'LAGARTO'): 2803500,
    ('SE', 'LARANJEIRAS'): 2803609,
    ('SE', 'MACAMBIRA'): 2803708,
    ('SE', 'NOSSA SENHORA DA GLORIA'): 2804201,
    ('SE', 'SAO CRISTOVAO'): 2806702,
    ('BA', 'ALAGOINHAS'): 2900702,
    ('BA', 'ALCOBACA'): 2900801,
    ('BA', 'AMARGOSA'): 2901007,
    ('BA', 'AMELIA RODRIGUES'): 2901106,
    ('BA', 'ANTAS'): 2901205,
    ('BA', 'BARRA'): 2903003,
    ('BA', 'BARRA DA ESTIVA'): 2903102,
    ('BA', 'BARREIRAS'): 2903201,
    ('BA', 'BOM JESUS DA LAPA'): 2903904,
    ('BA', 'CACHOEIRA'): 2905009,
    ('BA', 'CACULE'): 2905108,
    ('BA', 'CAETITE'): 2905207,
    ('BA', 'CAMACAN'): 2905205,
    ('BA', 'CAMACARI'): 2905304,
    ('BA', 'CAMPO FORMOSO'): 2905502,
    ('BA', 'CANDEIAS'): 2906005,
    ('BA', 'CAPIM GROSSO'): 2906823,
    ('BA', 'CATU'): 2907201,
    ('BA', 'CONCEICAO DO ALMEIDA'): 2908209,
    ('BA', 'CONCEICAO DO COITE'): 2908308,
    ('BA', 'CONDE'): 2908605,
    ('BA', 'CONDEUBA'): 2908704,
    ('BA', 'CRUZ DAS ALMAS'): 2909801,
    ('BA', 'ESPLANADA'): 2910502,
    ('BA', 'EUCLIDES DA CUNHA'): 2910700,
    ('BA', 'EUNAPOLIS'): 2910726,
    ('BA', 'FEIRA DE SANTANA'): 2910809,
    ('BA', 'GANDU'): 2911203,
    ('BA', 'GUANAMBI'): 2911708,
    ('BA', 'IBIRAPUA'): 2912300,
    ('BA', 'IBIRATAIA'): 2912409,
    ('BA', 'IBITIARA'): 2912508,
    ('BA', 'IGUAI'): 2912805,
    ('BA', 'ILHEUS'): 2913605,
    ('BA', 'IPIAU'): 2914009,
    ('BA', 'IRECE'): 2914603,
    ('BA', 'ITABUNA'): 2914801,
    ('BA', 'ITACARE'): 2915006,
    ('BA', 'ITAJUIPE'): 2915105,
    ('BA', 'ITAMBE'): 2915204,
    ('BA', 'ITANHEM'): 2915303,
    ('BA', 'ITAPARICA'): 2915402,
    ('BA', 'ITAPETINGA'): 2915600,
    ('BA', 'ITORORO'): 2916400,
    ('BA', 'JACOBINA'): 2917309,
    ('BA', 'JAGUAQUARA'): 2917408,
    ('BA', 'JAGUARARI'): 2917507,
    ('BA', 'JEQUIE'): 2918000,
    ('BA', 'JUAZEIRO'): 2918406,
    ('BA', 'LAURO DE FREITAS'): 2919206,
    ('BA', 'MAIRI'): 2919701,
    ('BA', 'MARAU'): 2919925,
    ('BA', 'MIGUEL CALMON'): 2921005,
    ('BA', 'MORRO DO CHAPEU'): 2921500,
    ('BA', 'MUCURI'): 2921906,
    ('BA', 'MUTUIPE'): 2922300,
    ('BA', 'NAZARE'): 2922706,
    ('BA', 'NOVA VICOSA'): 2923001,
    ('BA', 'OLINDINA'): 2923308,
    ('BA', 'PARAMIRIM'): 2923704,
    ('BA', 'POCOES'): 2924405,
    ('BA', 'POJUCA'): 2924504,
    ('BA', 'PORTO SEGURO'): 2925204,
    ('BA', 'PRADO'): 2925303,
    ('BA', 'QUIJINGUE'): 2925501,
    ('BA', 'RIACHAO DO JACUIPE'): 2925808,
    ('BA', 'RIBEIRA DO POMBAL'): 2926002,
    ('BA', 'RODELAS'): 2926309,
    ('BA', 'RUY BARBOSA'): 2927000,
    ('BA', 'SALVADOR'): 2927406,
    ('BA', 'SANTO AMARO'): 2928107,
    ('BA', 'SANTO ANTONIO DE JESUS'): 2928404,
    ('BA', 'SANTO ESTEVAO'): 2928802,
    ('BA', 'SAO DOMINGOS'): 2928901,
    ('BA', 'SAO FELIX'): 2929008,
    ('BA', 'SAPEACU'): 2929107,
    ('BA', 'SEABRA'): 2929206,
    ('BA', 'SENHOR DO BONFIM'): 2929404,
    ('BA', 'SERRINHA'): 2929503,
    ('BA', 'SIMOES FILHO'): 2929602,
    ('BA', 'TEIXEIRA DE FREITAS'): 2931350,
    ('BA', 'TEODORO SAMPAIO'): 2931400,
    ('BA', 'UBAIRA'): 2932002,
    ('BA', 'UBAITABA'): 2932101,
    ('BA', 'VALENCA'): 2932457,
    ('BA', 'VARZEA NOVA'): 2932556,
    ('BA', 'VERA CRUZ'): 2932606,
    ('BA', 'VITORIA DA CONQUISTA'): 2933307,
    ('BA', 'XIQUE-XIQUE'): 2933604,
    ('ES', 'AFONSO CLAUDIO'): 3200102,
    ('ES', 'AGUIA BRANCA'): 3200136,
    ('ES', 'ALEGRE'): 3200201,
    ('ES', 'ALFREDO CHAVES'): 3200300,
    ('ES', 'ANCHIETA'): 3200409,
    ('ES', 'ARACRUZ'): 3200607,
    ('ES', 'ATILIO VIVACQUA'): 3200706,
    ('ES', 'BARRA DE SAO FRANCISCO'): 3200904,
    ('ES', 'BOA ESPERANCA'): 3201001,
    ('ES', 'CACHOEIRO DE ITAPEMIRIM'): 3201209,
    ('ES', 'CARIACICA'): 3201308,
    ('ES', 'CASTELO'): 3201407,
    ('ES', 'COLATINA'): 3201506,
    ('ES', 'DOMINGOS MARTINS'): 3201803,
    ('ES', 'ECOPORANGA'): 3201902,
    ('ES', 'GUACUI'): 3202106,
    ('ES', 'GUARAPARI'): 3202205,
    ('ES', 'IBATIBA'): 3202304,
    ('ES', 'ICONHA'): 3202403,
    ('ES', 'ITAGUACU'): 3202502,
    ('ES', 'ITAPEMIRIM'): 3202601,
    ('ES', 'ITARANA'): 3202650,
    ('ES', 'IUNA'): 3202809,
    ('ES', 'JOAO NEIVA'): 3203138,
    ('ES', 'LINHARES'): 3203203,
    ('ES', 'MARATAIZES'): 3203328,
    ('ES', 'MARECHAL FLORIANO'): 3203344,
    ('ES', 'MIMOSO DO SUL'): 3203401,
    ('ES', 'MONTANHA'): 3203500,
    ('ES', 'MUNIZ FREIRE'): 3203609,
    ('ES', 'NOVA VENECIA'): 3203906,
    ('ES', 'PANCAS'): 3204003,
    ('ES', 'PEDRO CANARIO'): 3204052,
    ('ES', 'PIUMA'): 3204102,
    ('ES', 'RIO NOVO DO SUL'): 3204359,
    ('ES', 'SANTA LEOPOLDINA'): 3204508,
    ('ES', 'SANTA MARIA DE JETIBA'): 3204557,
    ('ES', 'SANTA TERESA'): 3204607,
    ('ES', 'SAO GABRIEL DA PALHA'): 3204706,
    ('ES', 'SAO MATEUS'): 3204805,
    ('ES', 'SERRA'): 3205000,
    ('ES', 'VARGEM ALTA'): 3205034,
    ('ES', 'VENDA NOVA DO IMIGRANTE'): 3205067,
    ('ES', 'VIANA'): 3205105,
    ('ES', 'VILA VELHA'): 3205204,
    ('ES', 'VITORIA'): 3205303,
    ('GO', 'AGUAS LINDAS DE GOIAS'): 5200258,
    ('GO', 'ANAPOLIS'): 5201108,
    ('GO', 'ANICUNS'): 5201306,
    ('GO', 'APARECIDA DE GOIANIA'): 5201405,
    ('GO', 'BURITI ALEGRE'): 5203906,
    ('GO', 'CALDAS NOVAS'): 5204508,
    ('GO', 'CATALAO'): 5205109,
    ('GO', 'CERES'): 5205406,
    ('GO', 'CHAPADAO DO CEU'): 5205471,
    ('GO', 'FIRMINOPOLIS'): 5207808,
    ('GO', 'FORMOSA'): 5208004,
    ('GO', 'GOIANDIRA'): 5208400,
    ('GO', 'GOIANESIA'): 5208509,
    ('GO', 'GOIANIA'): 5208707,
    ('GO', 'GOIAS'): 5209101,
    ('GO', 'GUAPO'): 5209408,
    ('GO', 'INHUMAS'): 5209903,
    ('GO', 'IPORA'): 5210109,
    ('GO', 'ITUMBIARA'): 5211503,
    ('GO', 'JARAGUA'): 5211800,
    ('GO', 'JATAI'): 5211909,
    ('GO', 'LUZIANIA'): 5212501,
    ('GO', 'MINACU'): 5213103,
    ('GO', 'MORRINHOS'): 5213707,
    ('GO', 'NAZARIO'): 5214002,
    ('GO', 'NEROPOLIS'): 5214507,
    ('GO', 'PADRE BERNARDO'): 5215603,
    ('GO', 'PALMELO'): 5215900,
    ('GO', 'PARANAIGUARA'): 5216403,
    ('GO', 'PARAUNA'): 5216601,
    ('GO', 'PIRACANJUBA'): 5217104,
    ('GO', 'PIRENOPOLIS'): 5217203,
    ('GO', 'PIRES DO RIO'): 5217302,
    ('GO', 'PORANGATU'): 5218003,
    ('GO', 'POSSE'): 5218300,
    ('GO', 'QUIRINOPOLIS'): 5218607,
    ('GO', 'RIO VERDE'): 5218805,
    ('GO', 'SANTA HELENA DE GOIAS'): 5219704,
    ('GO', 'SAO LUIS DE MONTES BELOS'): 5219803,
    ('GO', 'SAO MIGUEL DO ARAGUAIA'): 5219902,
    ('GO', 'TRINDADE'): 5221403,
    ('GO', 'URUACU'): 5221601,
    ('GO', 'VALPARAISO DE GOIAS'): 5222203,
})


correcoes_manuais


# Aplicar correções manuais
def corrigir_ibge(row):
    chave = (row['UF'], row['MUNICIPIO'])
    return correcoes_manuais.get(chave, row['IBGE'])

RAISOSC_COM_IBGE['IBGE'] = RAISOSC_COM_IBGE.apply(corrigir_ibge, axis=1)


# In[295]:


RAISOSC_COM_IBGE


# In[296]:


# Filtrar as linhas que não conseguiram encontrar o código IBGE
sem_ibge = RAISOSC_COM_IBGE[RAISOSC_COM_IBGE['IBGE'].isna()]

# Visualizar as colunas principais
colunas_interesse = ['UF', 'MUNICIPIO', 'MUNICIPIO_NORM_x', 'MUNICIPIO_MATCH_NORM']
print(sem_ibge[colunas_interesse].head(60))  # Mostra os 20 primeiros


# In[265]:


# Verifica quais colunas vieram do merge
print(ajuste_direto.columns)

# Se 'IBGE_y' estiver presente, ela é a coluna correta
col_ibge_novo = 'IBGE_y' if 'IBGE_y' in ajuste_direto.columns else 'IBGE'

# Conta os novos matches encontrados
print(f"Novos matches encontrados diretamente: {ajuste_direto[col_ibge_novo].notna().sum()}")

# Atualiza os valores ausentes no RAISOSC_COM_IBGE
RAISOSC_COM_IBGE['IBGE'] = RAISOSC_COM_IBGE['IBGE'].fillna(ajuste_direto[col_ibge_novo])


# In[299]:


colunas_desejadas = ['IBGE', 'RAISOSC2015', 'RAISOSC2016', 'RAISOSC2017',
                     'RAISOSC2018', 'RAISOSC2019', 'RAISOSC2020', 'RAISOSC2021']

RAISOSCFINAL = RAISOSC_COM_IBGE[colunas_desejadas].copy()


RAISOSCFINAL['IBGE'] = RAISOSCFINAL['IBGE'].astype(int)


# In[300]:


RAISOSCFINAL


# # Dependent Variable 4 - Number of health facilities
# 
# Quantidade por Ano/mês compet. segundo Município. Natureza Jurídica: 306-9 Fundação Privada, 307-7 Serviço Social Autônomo, 322-0 Organização Religiosa, 330-1 Organização Social (OS), 399-9 Associação Privada
# Período: Jan/2014, Jan/2015, Jan/2016, Jan/2017, Jan/2018, Jan/2019, Jan/2020, Jan/2021, Jan/2022, Jan/2023
#     
# Source: http://tabnet.datasus.gov.br/cgi/deftohtm.exe?cnes/cnv/estabbr.def

# In[244]:


CNESOSC = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\CNESosc.csv", delimiter=";")


# In[245]:


CNESOSC


# # Independent variable - paid health amendments to the federal budget - healthpork
# 
# National Health Fund transfer for individual ammendments - only OSC and only public: source: FNS Freedom of Information Access Law - FOIA 25072.017079/2024-71

# In[163]:


# Caminho do arquivo Excel
file_path = r"G:\Meu Drive\Doutorado\Disciplinas\Dados\Recursos\SEI_25072017079202471___Instrumentos_2015_a_2023___detalhe_CNES_e_EMENDAS_Versao_28032024 (1).xlsx"

# Ler apenas a aba "INSTRUMENTOS 2015 a 2023"
Maindf = pd.read_excel(file_path, sheet_name="INSTRUMENTOS 2015 a 2023", engine="openpyxl")
CNESinfo = pd.read_excel(file_path, sheet_name="CNES", engine="openpyxl")


# In[164]:


total_PAIDMaindf = Maindf['VL_PAGO'].sum()

# Exibir os resultados com as frases desejadas
print(f"Total paidMaindf : {total_PAIDMaindf}")


# In[165]:


print(Maindf['PROPOSTA'].duplicated().sum())


# In[166]:


# Realizar a junção dos DataFrames
Healthpork = Maindf.merge(
    CNESinfo[['NR_PROPOSTA', 'TIPO_NAT_JURIDICA']],  # Seleciona as colunas necessárias de CNESinfo
    left_on='PROPOSTA',  # Coluna de Maindf
    right_on='NR_PROPOSTA',  # Coluna de CNESinfo
    how='left'  # Mantém todos os registros de Maindf
)

Healthpork = Healthpork.drop_duplicates(subset='PROPOSTA')


# In[167]:


Healthpork['PaidType'] = np.where(
    Healthpork['TIPO_NAT_JURIDICA'] == 'ENTIDADES SEM FINS LUCRATIVOS',  # Condição
    'PaidNonprofit',  # Valor se a condição for verdadeira
    'PaidPublic'  # Valor se a condição for falsa
)


# In[168]:


Healthpork


# In[169]:


total_PAIDHealthpork = Healthpork['VL_PAGO'].sum()

# Exibir os resultados com as frases desejadas
print(f"Total paid : {total_PAIDHealthpork}")


# In[170]:


# Verificar duplicatas criadas após o merge
print(Healthpork['PROPOSTA'].duplicated().sum())


# In[171]:


# Certificar-se de que a coluna VL_PAGO é numérica (convertendo para inteiro)
Healthpork['VL_PAGO'] = pd.to_numeric(Healthpork['VL_PAGO'], errors='coerce').fillna(0).astype(int)

# Pivotar o DataFrame
pivot_Healthpork = Healthpork.pivot_table(
    index=['CO_MUNICIPIO_IBGE'],  # Índices do pivot
    columns=['ANO','PaidType'],
    values='VL_PAGO',  # Valores a serem somados
    aggfunc='sum',  # Soma os valores
    fill_value=0  # Preencher valores ausentes com 0
)

# Resetar o índice para tornar o DataFrame mais legível (opcional)
pivot_Healthpork.reset_index(inplace=True)


# In[172]:


pivot_Healthpork


# In[173]:


# Verificar se o cabeçalho tem dois níveis e combinar apenas os válidos
if isinstance(pivot_Healthpork.columns, pd.MultiIndex):
    pivot_Healthpork.columns = [
        f"PAGOFNSPUB{col[0]}" if col[1] == "PaidPublic" else
        f"PAGOFNSOSC{col[0]}" if col[1] == "PaidNonprofit" else None
        for col in pivot_Healthpork.columns
    ]   
    
pivot_Healthpork.reset_index(inplace=True)
pivot_Healthpork.columns = pivot_Healthpork.columns.map(lambda x: 'IBGE' if x is None else x)


# In[174]:


pivot_Healthpork


# In[177]:


# Selecionar as colunas que começam com 'PAGOFNSPUB' e 'PAGOFNSOSC'
pub_columns = [col for col in pivot_Healthpork.columns if col.startswith('PAGOFNSPUB')]
osc_columns = [col for col in pivot_Healthpork.columns if col.startswith('PAGOFNSOSC')]

# Somar os valores das colunas selecionadas
total_pagofnspub = pivot_Healthpork[pub_columns].sum().sum()
total_pagofnsosc = pivot_Healthpork[osc_columns].sum().sum()

# Calcular o total combinado
total_paid = total_pagofnspub + total_pagofnsosc

# Exibir os resultados
print(f"Total PAGOFNSPUB: {total_pagofnspub}")
print(f"Total PAGOFNSOSC: {total_pagofnsosc}")
print(f"Total Paid (Combined): {total_paid}")


# In[179]:


# Inicializar um dicionário para armazenar os resultados anuais
percentages = {}

# Iterar por todos os anos disponíveis no DataFrame
for year in range(2015, 2024):  # De 2015 a 2023
    pub_column = f'PAGOFNSPUB{year}'
    osc_column = f'PAGOFNSOSC{year}'
    
    if pub_column in pivot_Healthpork.columns and osc_column in pivot_Healthpork.columns:
        # Calcular os totais para o ano
        total_pub = pivot_Healthpork[pub_column].sum()
        total_osc = pivot_Healthpork[osc_column].sum()
        total = total_pub + total_osc
        
        # Calcular o percentual de PAGOFNSOSC sobre o total
        percentage = (total_osc / total) * 100 if total > 0 else 0
        
        # Armazenar o resultado no dicionário
        percentages[year] = percentage

# Exibir o percentual de 2023
percentage_2023 = percentages[2023]
print(f"Percentual de PAGOFNSOSC2023 sobre o total: {percentage_2023:.2f}%")

# Exibir os percentuais de todos os anos
print("\nPercentuais de PAGOFNSOSC sobre o total por ano:")
for year, percentage in percentages.items():
    print(f"{year}: {percentage:.2f}%")


# In[181]:


# Calculate the average percentage for 2015 to 2020
percentage_sum = 0
count = 0

# Iterating over the years from 2015 to 2020
for year in range(2015, 2021):  # 2015 to 2020
    pub_column = f'PAGOFNSPUB{year}'
    osc_column = f'PAGOFNSOSC{year}'
    
    if pub_column in pivot_Healthpork.columns and osc_column in pivot_Healthpork.columns:
        # Calculate the totals for the year
        total_pub = pivot_Healthpork[pub_column].sum()
        total_osc = pivot_Healthpork[osc_column].sum()
        total = total_pub + total_osc
        
        # Calculate the percentage of PAGOFNSOSC over the total
        percentage = (total_osc / total) * 100 if total > 0 else 0
        
        # Add to the sum and count
        percentage_sum += percentage
        count += 1

# Calculate the average percentage
average_percentage = percentage_sum / count if count > 0 else 0

# Display the average percentage
print(f"Average percentage of PAGOFNSOSC from 2015 to 2020: {average_percentage:.2f}%")


# In[182]:


# Calcular o somatório de PAGOFNSOSC de 2015 a 2020
sum_pagofnsosc = 0
count = 0

# Iterando sobre os anos de 2015 a 2020
for year in range(2015, 2021):  # 2015 a 2020
    osc_column = f'PAGOFNSOSC{year}'
    
    if osc_column in pivot_Healthpork.columns:
        # Somar os valores de PAGOFNSOSC para o ano
        sum_pagofnsosc += pivot_Healthpork[osc_column].sum()
        count += 1

# Calcular a média dividindo o somatório por 5 (número de anos de 2015 a 2020)
average_payment = sum_pagofnsosc / 5 if count > 0 else 0

# Exibir o resultado
print(f"Average USD payment by year: {average_payment:.2f}")


# # Control variables -  pib and other info: population and pib percapita
# 
# Municipality Identification info: source: IBGE https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/23701-divisao-territorial-brasileira.html?=&t=acesso-ao-produto
# 
# Population: source IBGE https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?=&t=resultados
# 
# Economic indicators: source: IBGE https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html?=&t=downloads
# 

# In[183]:


dadosibge = pd.read_csv(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\IBGE\dadosibge.csv', encoding = 'latin1', delimiter=";", index_col=False, dtype={'IBGE': np.int64,'Municipio': object})
dadosibge['IBGE'] = dadosibge['IBGE'].astype(int)
dadosibge['IBGE7'] = dadosibge['IBGE7'].astype(int)
dadosibge['MUNICIPIO'] = dadosibge['MUNICIPIO'].astype(str)


# In[184]:


dadosibge['MunHierarchy'] = np.select(
    [
        dadosibge['Centrolocal'] == 1,
        dadosibge['CentroSubregional'] == 1,
        dadosibge['CapitalRegional'] == 1,
        dadosibge['CentroZona'] == 1,
              dadosibge['Nucleo'] == 1
    ],
    [
        'Local center',
        'Subregional center',
        'Regional Capital',
        'Zone center',
        'Core'
    ],
    default='No Category'  # You can set a default value if none of the conditions are met
)


# In[189]:


Pop = pd.read_csv(r"G:\Meu Drive\Doutorado\Disciplinas\Dados\IBGE\Populacao2015a2021.csv", engine = 'python',  delimiter=";", index_col=False, dtype={'IBGE7': np.int64})
Pop['IBGE7'] = Pop['IBGE7'].astype(int)


# In[192]:


Pop


# In[396]:


Eco = pd.read_csv(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\IBGE\Eco2015to2021.csv',    delimiter=";")
Eco.columns = Eco.columns.str.strip()
Eco['IBGE7'] = Eco['IBGE7'].astype(int)


# In[397]:


Eco


# # Control variable - poverty
# 
#   
# 
# Poverty: source CADUNICO https://api.pgi.gov.br/api/1/serie/209482.json
# 
#         

# In[195]:


Cadunico =  pd.read_csv(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\Cadúnico\CadUnico.csv', engine = 'python',  delimiter=";", index_col=False, dtype={'IBGE': np.int64})
Cadunico['IBGE'] = Cadunico['IBGE'].astype(int)


# In[196]:


Cadunico


# # Control variable - resources from other sources - federal government funding to health nonprofits
# 
# To obtain federal disbursements to nonpprofits unrelated to porkbarrel, it was perfomed a filter on a database that informs all federal government expenditures called Siga. Source: https://www12.senado.leg.br/orcamento/sigabrasil

# In[197]:


Siga2015 = pd.read_csv('G:\Meu Drive\Doutorado\Disciplinas\Paper_december\Siga2015.csv',  engine = 'python',  delimiter=";", index_col=False,  dtype={'Emenda': object,'Empenhado': object, 'Pago': object,'Favorecido (Cod)':object})
Siga2015['Ano'] = 2015


# In[198]:


Siga2016 = pd.read_csv('G:\Meu Drive\Doutorado\Disciplinas\Paper_december\Siga2016.csv',  engine = 'python',  delimiter=";", index_col=False,  dtype={'Emenda': object,'Empenhado': object, 'Pago': object,'Favorecido (Cod)':object})
Siga2016['Ano'] = 2016


# In[199]:


Siga2017 = pd.read_csv('G:\Meu Drive\Doutorado\Disciplinas\Paper_december\Siga2017.csv',  engine = 'python',  delimiter=";", index_col=False,  dtype={'Emenda': object,'Empenhado': object, 'Pago': object,'Favorecido (Cod)':object})
Siga2017['Ano'] = 2017


# In[200]:


Siga2018 = pd.read_csv('G:\Meu Drive\Doutorado\Disciplinas\Paper_december\Siga2018.csv',  engine = 'python',  delimiter=";", index_col=False,   dtype={'Emenda': object,'Empenhado': object, 'Pago': object,'Favorecido (Cod)':object})
Siga2018['Ano'] = 2018


# In[201]:


Siga2019 = pd.read_csv('G:\Meu Drive\Doutorado\Disciplinas\Paper_december\Siga2019.csv',  engine = 'python',  delimiter=";", index_col=False,  dtype={'Emenda': object,'Empenhado': object, 'Pago': object,'Favorecido (Cod)':object})
Siga2019['Ano'] = 2019


# In[202]:


Siga2020 = pd.read_csv('G:\Meu Drive\Doutorado\Disciplinas\Paper_december\Siga2020.csv', engine='python', delimiter=";", index_col=False, dtype={'Emenda': object, 'Empenhado': object, 'Pago': object, 'Favorecido (Cod)': object})
Siga2020['Ano'] = 2020


# In[203]:


SIGABASE1 = pd.concat([Siga2015,Siga2016,Siga2017,Siga2018,Siga2019,Siga2020], ignore_index=True, axis=0)


# In[204]:


SIGABASE1


# In[205]:


def transform_value(value):
    # Check if the value is a string
    if isinstance(value, str):
        # Split the string based on the comma and take the first part
        integer_part = value.split(',')[0]
        return int(integer_part.replace('.', ''))
    else:
        # If the value is already an integer, return it as is
        return value


# In[206]:


SIGABASE1['Pago'] = SIGABASE1['Pago'].apply(transform_value)


# In[207]:


IPEAoscmap = pd.read_csv(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\Mapa_OSC\Mapa OSC area_subarea.csv',  engine = 'python',  delimiter=";", index_col=False)


# In[208]:


IPEAoscmap['tx_razao_social_osc'] = IPEAoscmap['tx_razao_social_osc'].astype(str)


# In[209]:


SIGABASE1['Favorecido'] = SIGABASE1['Favorecido'].astype(str)


# In[210]:


Siga = SIGABASE1[SIGABASE1['Favorecido'].isin(IPEAoscmap['tx_razao_social_osc'])]


# In[211]:


Siga.rename(columns={'Localidade (Favorecido).Localidade.Localidade (Cod)': 'IBGE7'}, inplace=True)


# In[212]:


Sigafiltered = Siga[Siga['Órgão (Cod/Desc)'] == '36000 - MINISTÉRIO DA SAÚDE']


# In[213]:


Sigafiltered2 = Sigafiltered[Sigafiltered['Resultado EOF (Cod/Desc)'] != '6 - DESP. PRIM. DISC. (EMENDAS INDIVIDUAIS)']


# In[214]:


filtered_indices = Sigafiltered2['Órgão (Cod/Desc)'] == '36000 - MINISTÉRIO DA SAÚDE'
Sigafiltered2.loc[filtered_indices, 'Pago'] = Sigafiltered2.loc[filtered_indices, 'Pago'].apply(transform_value)


# In[215]:


Sigafiltered2group = Sigafiltered2.groupby(['Ano','IBGE7'])['Pago'].sum().reset_index()
print("Sum after grouping:", Sigafiltered2group['Pago'].sum())


# In[216]:


Sigafiltered2group = Sigafiltered2group.pivot_table(
    index='IBGE7',
    columns=['Ano'],
    values=['Pago'],
    aggfunc='sum',
    fill_value=0
)


# In[217]:


Sigafiltered2group.columns = Sigafiltered2group.columns.map(lambda x: ''.join(map(str, x)))


# In[218]:


Sigafiltered2group = Sigafiltered2group.reset_index()


# In[219]:


Sigafiltered2group.fillna(0, inplace=True)


# In[220]:


Sigafiltered2group['IBGE7'] = Sigafiltered2group['IBGE7'].astype(int)


# In[221]:


rename_dict3 = {
    'Pago2015': 'fedgovfunding2015',
    'Pago2016': 'fedgovfunding2016',
    'Pago2017': 'fedgovfunding2017',
    'Pago2018': 'fedgovfunding2018',
    'Pago2019': 'fedgovfunding2019',
    'Pago2020': 'fedgovfunding2020',
    
}


# In[222]:


Sigafiltered2group.rename(columns=rename_dict3, inplace=True)


# In[223]:


Sigafiltered2group


# # Control Variable - Associational nonprofits  (social capital)
# 
# Source: https://mapaosc.ipea.gov.br/base-dados excludes Healthnonprofits and keeps only associations cd_natureza_juridica_osc = 3069 - Private Associations

# In[6]:


OSCTOTAL = pd.read_csv(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\Mapa_OSC\Mapa OSC area_subarea.csv', engine = 'python',  delimiter=";", index_col=False, dtype={'IBGE7': np.int64})
OSCTOTAL = OSCTOTAL[OSCTOTAL['saude'] != 1]
OSCTOTAL = OSCTOTAL[OSCTOTAL['cd_natureza_juridica_osc'] == 3069]
OSCTOTAL.dropna(subset=['edmu_cd_municipio'], inplace=True)
OSCTOTAL.rename(columns={'edmu_cd_municipio': 'IBGE7'}, inplace=True)
OSCTOTAL['IBGE7'] = OSCTOTAL['IBGE7'].astype(int)


# In[7]:


OSCTOTAL['ano_fund'] = OSCTOTAL['dt_fundacao_osc'].astype(str).str[-4:]


# In[8]:


OSCTOTAL['ano_fund'] = pd.to_numeric(OSCTOTAL['ano_fund'])


# In[9]:


# Funções para contar os registros antes de cada ano específico
def count_before_2015(x):
    return (x < 2015).sum()

def count_before_2016(x):
    return (x < 2016).sum()

def count_before_2017(x):
    return (x < 2017).sum()

def count_before_2018(x):
    return (x < 2018).sum()

def count_before_2019(x):
    return (x < 2019).sum()

def count_before_2020(x):
    return (x < 2020).sum()

def count_before_2021(x):
    return (x < 2021).sum()

# Agora aplicar essas funções no agrupamento
OSCTOTALgrouped = OSCTOTAL.groupby(['IBGE7']).agg({
    'ano_fund': [
        count_before_2015,
        count_before_2016,
        count_before_2017,
        count_before_2018,
        count_before_2019,
        count_before_2020,
        count_before_2021
    ]
})

# Exibir os resultados agrupados
print(OSCTOTALgrouped.head())


# In[10]:


OSCTOTALgrouped.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in OSCTOTALgrouped.columns.values]


# In[11]:


OSCTOTALgrouped.reset_index(inplace=True)


# In[12]:


OSCTOTALgrouped


# In[13]:


rename_dict2 = {
    'ano_fund_count_before_2015': 'OSC2014',
    'ano_fund_count_before_2015': 'OSC2014',
    'ano_fund_count_before_2016': 'OSC2015',
    'ano_fund_count_before_2017': 'OSC2016',
    'ano_fund_count_before_2018': 'OSC2017',
    'ano_fund_count_before_2019': 'OSC2018',
    'ano_fund_count_before_2020': 'OSC2019',
    'ano_fund_count_before_2021': 'OSC2020',
    'IBGE7': 'IBGE7'
   
}


# In[14]:


OSCTOTALgrouped.rename(columns=rename_dict2, inplace=True)


# In[15]:


OSCTOTALgrouped.fillna(0, inplace=True)


# In[16]:


OSCTOTALgrouped.reset_index(drop=True, inplace=True)


# In[17]:


OSCTOTALgrouped


# In[19]:


df_sp = OSCTOTALgrouped[OSCTOTALgrouped["IBGE7"] == 3550308]
print(df_sp)


# #  Control variable: Healthplan coverage
# Source: http://www.ans.gov.br/anstabnet/cgi-bin/tabnet?dados/tabnet_02.def

# In[236]:


Healthplan = pd.read_csv(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\depen_plano_saude.csv', encoding = 'latin1', delimiter=";", index_col=False, dtype={'IBGE': np.int64,'Municipio': object})


# In[237]:


Healthplan


# #  Control variable: Municipalities total expenses with nonprofits
# Source: Tesouro Nacional Finbra. It is not possible to only use the values paid do health nonprofits.

# In[238]:


FinbraPagoOSC2015 = pd.read_excel(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\Recursos\FinbraPagoOSC2015.xlsx')
FinbraPagoOSC2016 = pd.read_excel(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\Recursos\FinbraPagoOSC2016.xlsx')
FinbraPagoOSC2017 = pd.read_excel(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\Recursos\FinbraPagoOSC2017.xlsx')
FinbraPagoOSC2018 = pd.read_excel(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\Recursos\FinbraPagoOSC2018.xlsx')
FinbraPagoOSC2019 = pd.read_excel(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\Recursos\FinbraPagoOSC2019.xlsx')
FinbraPagoOSC2020 = pd.read_excel(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\Recursos\FinbraPagoOSC2020.xlsx')


# In[377]:


from pandas import Int64Dtype

# Para cada DataFrame, primeiro garanta que os dados sejam numéricos
FinbraPagoOSC2015['FinbrapagoOSC2015'] = pd.to_numeric(FinbraPagoOSC2015['FinbrapagoOSC2015'], errors='coerce').astype(Int64Dtype())
FinbraPagoOSC2016['FinbrapagoOSC2016'] = pd.to_numeric(FinbraPagoOSC2016['FinbrapagoOSC2016'], errors='coerce').astype(Int64Dtype())
FinbraPagoOSC2017['FinbrapagoOSC2017'] = pd.to_numeric(FinbraPagoOSC2017['FinbrapagoOSC2017'], errors='coerce').astype(Int64Dtype())
FinbraPagoOSC2018['FinbrapagoOSC2018'] = pd.to_numeric(FinbraPagoOSC2018['FinbrapagoOSC2018'], errors='coerce').astype(Int64Dtype())
FinbraPagoOSC2019['FinbrapagoOSC2019'] = pd.to_numeric(FinbraPagoOSC2019['FinbrapagoOSC2019'], errors='coerce').astype(Int64Dtype())
FinbraPagoOSC2020['FinbrapagoOSC2020'] = pd.to_numeric(FinbraPagoOSC2020['FinbrapagoOSC2020'], errors='coerce').astype(Int64Dtype())


# In[378]:


FinbraPagoOSC2020


# # Joining variables

# In[347]:


Dataset = pd.merge(dadosibge, Pop, how = 'left', on = 'IBGE7')


# In[348]:


Dataset['IBGE7'] = Dataset['IBGE7'].astype(int)
HealthNonprofitsdf['IBGE7'] = HealthNonprofitsdf['IBGE7'].astype(int)


Dataset1 = pd.merge(Dataset, HealthNonprofitsdf, how = 'left', on = 'IBGE7')


# In[349]:


Dataset1


# In[350]:


Dataset1A = pd.merge(Dataset1, CNESOSC, how = 'left', on = 'IBGE')


# In[351]:


Dataset1B = pd.merge(Dataset1A, RAISOSCFINAL, how = 'left', on = 'IBGE')


# In[352]:


Dataset1C = pd.merge(Dataset1B, MACOSC, how = 'left', on = 'IBGE')


# In[398]:


Dataset1C['IBGE'] = Dataset1C['IBGE'].astype(int)
pivot_Healthpork['IBGE'] = pivot_Healthpork['IBGE'].astype(int)

Dataset2 = pd.merge(Dataset1C, pivot_Healthpork, how = 'left', on = 'IBGE')


# In[399]:


Dataset2['IBGE7'] = Dataset2['IBGE7'].astype(int)
Dataset3 = pd.merge(Dataset2, Eco, how = 'left', on = 'IBGE7')


# In[400]:


Dataset4 = pd.merge(Dataset3, Cadunico, how = 'left', on = 'IBGE')


# In[401]:


Dataset5 = pd.merge(Dataset4, Sigafiltered2group, how = 'left', on = 'IBGE7')


# In[402]:


Dataset6 = pd.merge(Dataset5, OSCTOTALgrouped, how = 'left', on = 'IBGE7')


# In[403]:


Dataset6


# In[404]:


Dataset6['IBGE7'] = Dataset6['IBGE7'].astype(int)
FinbraPagoOSC2015['IBGE'] = FinbraPagoOSC2015['IBGE'].astype(int)
FinbraPagoOSC2016['IBGE'] = FinbraPagoOSC2016['IBGE'].astype(int)
FinbraPagoOSC2017['IBGE'] = FinbraPagoOSC2017['IBGE'].astype(int)
FinbraPagoOSC2018['IBGE'] = FinbraPagoOSC2018['IBGE'].astype(int)
FinbraPagoOSC2019['IBGE'] = FinbraPagoOSC2019['IBGE'].astype(int)
FinbraPagoOSC2020['IBGE'] = FinbraPagoOSC2020['IBGE'].astype(int)


# In[405]:


Dataset7 = pd.merge(Dataset6, FinbraPagoOSC2015, how='left', left_on='IBGE7', right_on='IBGE')


# In[406]:


Dataset8 = pd.merge(Dataset7, FinbraPagoOSC2016, how='left', left_on='IBGE7', right_on='IBGE')


# In[407]:


Dataset8 = Dataset8.drop('IBGE', axis=1)
Dataset8 = Dataset8.rename(columns={'IBGE_x': 'IBGE'})


# In[408]:


Dataset9= pd.merge(Dataset8, FinbraPagoOSC2017, how='left', left_on='IBGE7', right_on='IBGE')


# In[409]:


Dataset10 = pd.merge(Dataset9, FinbraPagoOSC2018, how='left', left_on='IBGE7', right_on='IBGE')


# In[410]:


Dataset10 = Dataset10.drop('IBGE_y', axis=1)
Dataset10 = Dataset10.rename(columns={'IBGE_x': 'IBGE'})


# In[411]:


Dataset11 = pd.merge(Dataset10, FinbraPagoOSC2019, how='left', left_on='IBGE7', right_on='IBGE')


# In[412]:


Dataset12 = pd.merge(Dataset11, FinbraPagoOSC2020, how='left', left_on='IBGE7', right_on='IBGE')


# In[413]:


Dataset12 = Dataset12.drop('IBGE', axis=1)
Dataset12 = Dataset12.drop('IBGE_y', axis=1)
Dataset12 = Dataset12.rename(columns={'IBGE_x': 'IBGE'})


# In[414]:


ibge_columns = [col for col in Dataset12.columns if col == 'IBGE']

# Keep the first 'IBGE' column
Dataset12 = Dataset12.loc[:, ~Dataset12.columns.duplicated()]


# In[415]:


Dataset12


# In[416]:


Healthplan['IBGE'] = Healthplan['IBGE'].astype(int)
Dataset13 = pd.merge(Dataset12, Healthplan, how='left', left_on='IBGE', right_on='IBGE')


# In[417]:


# Fill all NaN values with 0
Dataset13 = Dataset13.fillna(0)

# Convert all numeric columns to int
Dataset13 = Dataset13.apply(pd.to_numeric, errors='ignore', downcast='integer')


# In[418]:


Dataset13


# In[419]:


csv_file_path = r"C:\Users\lunav\Downloads\Dataset13.csv"

Dataset13.to_csv(csv_file_path, index=False)


# # Suplementary analyisis: Nonprofit profile - health facility analysis
# joining Ministry of Health LAI and IPEA to know the foundation date

# In[675]:


Healthfacility = Maindf.merge(
    CNESinfo[['NR_PROPOSTA', 'TIPO_NAT_JURIDICA','NO_RAZAO_SOCIAL','CO_CNES']],  # Seleciona as colunas necessárias de CNESinfo
    left_on='PROPOSTA',  # Coluna de Maindf
    right_on='NR_PROPOSTA',  # Coluna de CNESinfo
    how='left'  # Mantém todos os registros de Maindf
)

Healthfacility = Healthfacility.drop_duplicates(subset='PROPOSTA')


# In[681]:


filtered_Healthfacility = Healthfacility[Healthfacility['TIPO_NAT_JURIDICA'] == 'ENTIDADES SEM FINS LUCRATIVOS']


# In[682]:


filtered_Healthfacility


# In[684]:


# Sum the values in the 'VL_PAGO' column
total_vl_pago = filtered_Healthfacility['VL_PAGO'].sum()

# Display the total sum
print(f"Total VL_PAGO paid value to nonprofits: {total_vl_pago}")


# In[687]:


# Count unique values in the 'CO_CNES' column
unique_co_cnes = filtered_Healthfacility['CO_CNES'].nunique()

# Count unique values in the 'NO_RAZAO_SOCIAL' column
unique_no_razao_social = filtered_Healthfacility['NO_RAZAO_SOCIAL'].nunique()

# Display the results
print(f"Unique values in 'CO_CNES' number of nonprofit health facilities funded with pork barrel: {unique_co_cnes}")
print(f"Unique values in 'NO_RAZAO_SOCIAL - Number of nonprofits funded with pork barrel': {unique_no_razao_social}")


# In[690]:


# Certificar-se de que a coluna VL_PAGO é numérica (convertendo para inteiro)
filtered_Healthfacility['VL_PAGO'] = pd.to_numeric(filtered_Healthfacility['VL_PAGO'], errors='coerce').fillna(0).astype(int)

# Pivotar o DataFrame
pivot_filtered_Healthfacility = filtered_Healthfacility.pivot_table(
    index=['CO_MUNICIPIO_IBGE','NO_RAZAO_SOCIAL'],  # Índices do pivot
    columns=['ANO'],
    values='VL_PAGO',  # Valores a serem somados
    aggfunc='sum',  # Soma os valores
    fill_value=0  # Preencher valores ausentes com 0
)

# Resetar o índice para tornar o DataFrame mais legível (opcional)
pivot_filtered_Healthfacility.reset_index(inplace=True)


# In[691]:


pivot_filtered_Healthfacility


# In[692]:


# Create a function to count how many years (2015 to 2020) have a value greater than zero for each 'NO_RAZAO_SOCIAL'
pivot_filtered_Healthfacility['Years_with_value'] = pivot_filtered_Healthfacility.iloc[:, 3:9].apply(lambda row: (row > 0).sum(), axis=1)

# Display the DataFrame with the new column
print(pivot_filtered_Healthfacility[['NO_RAZAO_SOCIAL', 'Years_with_value']].head())


# In[693]:


# Count how many 'NO_RAZAO_SOCIAL' have 'Years_with_value' >= 4
count_4_or_more = (pivot_filtered_Healthfacility['Years_with_value'] >= 4).sum()

# Display the result
print(f"Number of NO_RAZAO_SOCIAL with 4 or more years with value: {count_4_or_more}")


# In[700]:


# Create a function to count how many years (2015 to 2020) have a value greater than zero for each 'NO_RAZAO_SOCIAL'
pivot_filtered_Healthfacility['Years_with_value'] = pivot_filtered_Healthfacility.iloc[:, 3:9].apply(lambda row: (row > 0).sum(), axis=1)

# Count how many unique 'CO_MUNICIPIO_IBGE' values are there in the DataFrame
unique_ibge_count = pivot_filtered_Healthfacility['CO_MUNICIPIO_IBGE'].nunique()

# Display the result
print(f"Number of unique 'CO_MUNICIPIO_IBGE' number of municipalities that received nonprofit pork barrel: {unique_ibge_count}")


# In[702]:


# Create a function to count how many years (2015 to 2020) have a value greater than zero for each 'NO_RAZAO_SOCIAL'
pivot_filtered_Healthfacility['Years_with_value'] = pivot_filtered_Healthfacility.iloc[:, 3:9].apply(lambda row: (row > 0).sum(), axis=1)

# Filter the DataFrame for rows where 'Years_with_value' >= 4
filtered_df = pivot_filtered_Healthfacility[pivot_filtered_Healthfacility['Years_with_value'] >= 4]

# Count how many unique 'CO_MUNICIPIO_IBGE' values have 'Years_with_value' >= 4
unique_ibge_count = filtered_df['CO_MUNICIPIO_IBGE'].nunique()

# Display the result
print(f"Number of unique 'CO_MUNICIPIO_IBGE' with 'Years_with_value' >= 4 0 Number of municipalities that nonprofits received pork barrel for more than 4 years: {unique_ibge_count}")


# In[712]:


# Calculate the overall average of 'VL_PAGO'
overall_average_vl_pago = filtered_Healthfacility['VL_PAGO'].mean()

# Display the result
print(f"Overall average VL_PAGO R$: {overall_average_vl_pago}")


# In[711]:


# Select the columns for the years 2015 to 2020
year_columns = pivot_filtered_Healthfacility.columns[3:9]  # Adjust based on your DataFrame's structure

# Calculate the overall average for the selected years (2015 to 2020)
overall_average_years_2015_2020 = pivot_filtered_Healthfacility[year_columns].mean().mean()

# Display the result
print(f"Overall average VL_PAGO for years 2015 to 2020 R$: {overall_average_years_2015_2020}")


# In[704]:


# Calculate the average 'VL_PAGO' by 'NO_RAZAO_SOCIAL'
average_vl_pago = filtered_Healthfacility.groupby('NO_RAZAO_SOCIAL')['VL_PAGO'].mean()

# Display the result
print(average_vl_pago.head())


# In[706]:


# Calculate the average 'VL_PAGO' by 'NO_RAZAO_SOCIAL'
average_vl_pago = filtered_Healthfacility.groupby('NO_RAZAO_SOCIAL')['VL_PAGO'].mean()

# Sort the averages in descending order and get the top 10
top_10_no_razao_social = average_vl_pago.sort_values(ascending=False).head(10)

# Display the top 10
print(top_10_no_razao_social)


# In[ ]:




