import streamlit as st  
from PIL import Image 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json


st.set_page_config(
    page_title = "Segurança Pública no RJ",
    page_icon = "🛡️",
    layout = "wide",
    initial_sidebar_state = "expanded"
    
)
@st.cache_data
def carregar_dados():

    df = pd.read_csv("BaseMunicipioMensal.csv", encoding='latin1', sep=';')

    df['data_registro'] = pd.to_datetime({'year': df['ano'], 'month': df['mes'], 'day': 1})
    return df

df = carregar_dados()
pages = ["Introdução", "Panorama Geral", "Analise Temporal", "Recortes Geográficos", "Mudanças de Padrão", "Síntese"]
choice = st.sidebar.radio("Ir para", pages)

if choice == "Introdução":
    coltexto, colimagem = st.columns([3,2])
    with coltexto:
        st.title("Análise sobre Seguraça Pública no Estado do Rio de Janeiro")

        st.header("Motivação")
        st.markdown("Escolhi esse tema pois a segurança pública e criminalidade são tópicos que gosto de trabalhar e acredito que o dataset me possibilite gerar insights e visualizações interessantes. A criminalidade é um dos temas mais impactantes para o desenvolvimento socioeconômico e a qualidade de vida, ainda mais na nossa cidade/estado, portanto me atraiu a oportunidade de investigar como ela se comporta em diferentes municípios e regiões metropolitanas ao longo dos anos.")

        st.header("Objetivo")
        st.markdown("O objetivo é diagnosticar padrões de ocorrências policiais, identificar tendências de aumento ou queda em tipos específicos de crimes e avaliar a sazonalidade dos dados para fundamentar a criação do dashboard interativo.")

        st.header("Fonte dos dados")
        st.markdown("""
            * **Instituição**: Instituto de Segurança Pública do Estado do Rio de Janeiro (ISP-RJ)
            * **Fonte de Acesso**: [Portal de Dados Abertos do ISP-RJ](https://www.ispdados.rj.gov.br/estatistica.html)
            * **Dataset Utilizado**: Estatísticas de segurança: série histórica mensal por município desde 2014
        """)

    with colimagem:
        try:
            url_imagem = 'https://www.rj.gov.br/emop/sites/default/files/inline-images/Mapa%20EMOP-RJ%20com%20obras_0.jpg'
            st.image(url_imagem, caption='Mapa dos Municípios do Rio de Janeiro', use_container_width=True)
        except FileNotFoundError:
            st.error('Imagem não encontrada.')



elif choice == "Panorama Geral":
    st.title("Panorama Geral")
    st.write("Aqui você pode explorar uma visão geral das ocorrências policiais no estado do Rio de Janeiro")

    tabs = st.tabs(["Qual categoria domina mais as ocorrências?", "Ranking geral de ocorrências mais registradas", " (Top 10) Municípios com mais ocorrências", "Concentração por Região"])

    with tabs[0]:



        st.header("Qual categoria domina mais as ocorrências?")

        nao_crimes = [
                'fmun', 'fmun_cod', 'ano', 'mes', 'regiao', 'municipio', 'delegacia', 
                'registro_ocorrencias', 'fase', 'AISP', 'RISP', 'CISP', 'mes_ano', 'data',
                'apf', 'cmp', 'aaapai', 'am', 'recuperacao_veiculos', 'encontro_cadaver', 
                'encontro_ossada', 'policiais_mortos_servico', 'pessoas_desaparecidas'
            ]
        
        cols_crime = [col for col in df.select_dtypes(include='number').columns if col not in nao_crimes]
        crimes_patrimonio = ['total_furtos', 'total_roubos', 'estelionato', 'extorsao']
        crimes_vida = ['letalidade_violenta', 'hom_doloso', 'hom_por_interv_policial', 'latrocinio', 'lesao_corp_morte','estupro']
        outros_crimes = [col for col in cols_crime if col not in (crimes_patrimonio + crimes_vida) and not col.startswith('furto_') and not col.startswith('roubo_') and not col.startswith('outros_')]

        total_patrimonio = df[crimes_patrimonio].sum().sum()
        total_vida = df[crimes_vida].sum().sum()
        total_outros = df[outros_crimes].sum().sum()

        df_categorias = pd.DataFrame({
            'Categoria': ['Crimes contra o Patrimônio', 'Crimes contra a Vida', 'Outros Crimes'],
            'Total': [total_patrimonio, total_vida, total_outros],
        })
        fig_pizza = px.pie(
            df_categorias,
            names='Categoria',
            values='Total',
            title='Proporção de Ocorrências por Categoria',
            hole=0.4,  
            color_discrete_sequence=["#0c4daf", "#0CAD24", "#AD0C0C"],  
        )
        fig_pizza.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pizza, use_container_width=True)

    with tabs[1]:
        st.header("Ranking geral de ocorrências mais registradas")
        nao_crimes = [
            'fmun', 'fmun_cod', 'ano', 'mes', 'regiao', 'municipio', 'delegacia', 
            'registro_ocorrencias', 'fase', 'AISP', 'RISP', 'CISP', 'mes_ano', 'data',
            'apf', 'cmp', 'aaapai', 'am', 'recuperacao_veiculos', 'encontro_cadaver', 
            'encontro_ossada', 'policiais_mortos_servico', 'pessoas_desaparecidas'
        ]

        cols_crime = [col for col in df.select_dtypes(include='number').columns if col not in nao_crimes]
        totais_crimes = df[cols_crime].sum().sort_values(ascending=False)

        totais_macro = totais_crimes[~totais_crimes.index.str.startswith('furto_')]
        totais_macro = totais_macro[~totais_macro.index.str.startswith('roubo_')]
        totais_macro = totais_macro.drop(['outros_roubos','outros_furtos'], errors='ignore')

        registros_totais = df['registro_ocorrencias'].sum()
        ranking_crimes = totais_macro.head(10).to_frame(name='Volume Acumulado')

        ranking_crimes['% do total geral']=(ranking_crimes/registros_totais)*100 

        df_grafico = ranking_crimes.reset_index().rename(columns={'index':'Tipo de crime'})

        df_grafico = df_grafico.sort_values(by='Volume Acumulado', ascending=False)

        fig,ax = plt.subplots(figsize=(10,6))

        sns.barplot(
            data=df_grafico,
            x='Volume Acumulado',
            y='Tipo de crime',
            palette = 'dark:#69d',
            ax=ax
        )
        for i, p in enumerate(ax.patches):
            largura_barra = p.get_width()
            porcentagem = df_grafico.iloc[i]['% do total geral']

            texto_label = f"{int(largura_barra):,}({porcentagem:.2f}%)"

            ax.text(
                largura_barra + (df_grafico['Volume Acumulado'].max() * 0.01),
                p.get_y() + p.get_height() / 2,
                texto_label,
                va='center',
                fontsize=10
            )

        ax.set_title("Ranking das 10 Ocorrências Policiais mais Registradas", fontsize=14, pad=15)
        ax.set_xlabel("Volume Acumulado")
        ax.set_ylabel("")
        sns.despine()

        ax.set_xlim(0,df_grafico['Volume Acumulado'].max()*1.15)
        st.pyplot(fig)

    with tabs[2]:
        st.header("(Top 10) Municípios com mais ocorrências")
        top10_registros = df.groupby('fmun')['registro_ocorrencias'].sum().sort_values(ascending=False).head(10)
        top10_letalidade = df.groupby('fmun')['letalidade_violenta'].sum().sort_values(ascending=False).head(10)

        df_municipios = top10_registros.reset_index().rename(columns={'fmun':'Município', 'registro_ocorrencias':'Volume Acumulado'})
        
        df_municipios = df_municipios.sort_values(by='Volume Acumulado', ascending=True)

        fig,ax = plt.subplots(figsize=(10,6))

        sns.barplot(
            data=df_municipios,
            x='Volume Acumulado',
            y='Município',
            palette = 'coolwarm',
            ax=ax
        )
        for i, p in enumerate(ax.patches):
            largura_barra = p.get_width()

            texto_label = f"{int(largura_barra):,}"
            ax.text(
                largura_barra + (df_municipios['Volume Acumulado'].max() * 0.01),
                p.get_y() + p.get_height() / 2,
                texto_label,
                va='center',
                fontsize=10
            )

        ax.set_title("Ranking dos 10 Municípios com Mais Ocorrências", fontsize=14, pad=15)
        ax.set_xlabel("Volume Acumulado")
        ax.set_ylabel("")
        sns.despine()

        ax.set_xlim(0,df_municipios['Volume Acumulado'].max()*1.15)
        st.pyplot(fig)

    with tabs[3]:
        st.header("Concentração de ocorrências por Região")
        regiao_registros = df.groupby('regiao')['registro_ocorrencias'].sum().to_frame(name='Total Registros') 
        regiao_registros['% do Estado'] = (regiao_registros['Total Registros'] / regiao_registros['Total Registros'].sum()) * 100 
        regiao_registros = regiao_registros.sort_values(by='Total Registros', ascending=False)

        df_regioes = regiao_registros.reset_index().rename(columns={'regiao':'Região', 'Total Registros':'Volume Acumulado'})

        with open("regioes_rj.geojson",encoding='utf-8') as f:
            geojson_rj = json.load(f)

        municipios_lista = []
        for feature in geojson_rj['features']:
            mun_name = feature['properties']['name']
            regiao_nome = feature['properties']['regiao_customizada']
            municipios_lista.append({'Município': mun_name, 'Região': regiao_nome})
        
        df_mapa = pd.DataFrame(municipios_lista)
        df_final = df_mapa.merge(df_regioes, on='Região', how='left')

        fig_mapa = px.choropleth(
            data_frame = df_final,
            geojson=geojson_rj,
            locations='Município',
            featureidkey='properties.name',
            color='Volume Acumulado',
            color_continuous_scale='YlOrRd',
            labels={'Volume Acumulado': 'Total de Ocorrências'},
            hover_data={'Região': True, 'Município': False},
        )
        fig_mapa.update_geos(fitbounds="locations", visible=False)
        fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        st.plotly_chart(fig_mapa, use_container_width=True)


elif choice == "Analise Temporal":
    st.header("Análise Temporal")
    st.write("Aqui você pode analisar a evolução das ocorrências policiais ao longo do tempo")
    tabs = st.tabs(["Série Histórica Anual, em que ano tivemos mais crimes registrados?", "Comportamento Sazonal: Que mês costumam ocorrer mais roubos e furtos?", "Digitalização do Crime"])

    with tabs[0]:
        st.header("Série Histórica Anual, em que ano tivemos mais crimes registrados?")

        tabela_anual = df.groupby('ano')[['registro_ocorrencias','letalidade_violenta']].sum().reset_index()
        tabela_anual = tabela_anual.sort_values(by='ano')
        ano_pico = tabela_anual.loc[tabela_anual['registro_ocorrencias'].idxmax(), 'ano']
        max_ocorrencias = tabela_anual['registro_ocorrencias'].max()
        col1,col2 = st.columns(2)

        with col1:
            fig_reg = px.line(tabela_anual, x='ano', y='registro_ocorrencias', markers=True, title="Total de Registros")
            st.plotly_chart(fig_reg, use_container_width=True)

        with col2:
            fig_let = px.line(tabela_anual, x='ano', y='letalidade_violenta', markers=True, title="Letalidade Violenta", color_discrete_sequence=['red'])
            st.plotly_chart(fig_let, use_container_width=True)
    with tabs[1]:
        st.header("Comportamento Sazonal: Que mês costumam ocorrer mais roubos e furtos?")
       
        tabela_sazonal = df.groupby('mes')[['total_roubos', 'total_furtos', 'furto_transeunte', 'roubo_transeunte']].sum().reset_index()


        nomes_meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                    7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'} 
        tabela_sazonal['nome_mes'] = tabela_sazonal['mes'].map(nomes_meses)


        tabela_sazonal['soma_crimes'] = tabela_sazonal['total_roubos'] + tabela_sazonal['total_furtos']
        mes_pico = tabela_sazonal.loc[tabela_sazonal['soma_crimes'].idxmax(),'nome_mes']

        st.info("Primeiro trimestre: férias de verão, mais pessoas na rua e praias, além do efeito Carnaval.")
        legendas = {
                    'total_roubos': 'Total de Roubos',
                    'total_furtos': 'Total de Furtos',
                    'furto_transeunte': 'Furto a Transeunte',
                    'roubo_transeunte': 'Roubo a Transeunte'
        }

        col1,col2 = st.columns(2)

        fig1 = px.line(
        tabela_sazonal,
        x='nome_mes',
        y=['total_roubos', 'total_furtos'],
        markers=True,
        title='Total de Roubos e Furtos',
        labels={
            'value': 'Quantidade',
            'nome_mes': 'Mês',
            'variable': 'Ocorrência'
        },
        category_orders={'nome_mes': list(nomes_meses.values())}
        )
        fig1.for_each_trace(lambda t: t.update(name=legendas[t.name]))
        col1.plotly_chart(fig1, use_container_width=True)
        fig2 = px.line(
            tabela_sazonal,
            x='nome_mes',
            y=['roubo_transeunte', 'furto_transeunte'],
            markers=True,
            title='Crimes contra Transeuntes',
            labels={
                'value': 'Quantidade',
                'nome_mes': 'Mês',
                'variable': 'Ocorrência'
            },
            category_orders={'nome_mes': list(nomes_meses.values())}
        )
        fig2.for_each_trace(lambda t: t.update(name=legendas[t.name]))
      
        col2.plotly_chart(fig2, use_container_width=True)

    with tabs [2]:
        st.header("Digitalização do Crime")
        df_digital = df.groupby('ano')[['estelionato', 'roubo_rua']].sum().reset_index()
        df_digital = df_digital.sort_values(by='ano')

        cruzamento = df_digital[df_digital['estelionato'] > df_digital['roubo_rua']]
        if not cruzamento.empty:
            ano_virada = cruzamento.iloc[0]['ano']
            st.info(f" Em **{int(ano_virada)}**, o número de registros de estelionato ultrapassou o de roubos de rua, evidenciando a migração do crime para o meio digital.")

        legendas_digital = {
        'estelionato': 'Estelionato (Fraudes/Digital)',
        'roubo_rua': 'Roubo de Rua'
        }   

        fig_digital = px.line(
            df_digital,
            x='ano',
            y=['estelionato', 'roubo_rua'],
            markers=True,
            title='Evolução Comparativa: Crime Digital vs Crime Físico',
            labels={
                'value': 'Total de Ocorrências',
                'ano': 'Ano',
                'variable': 'Categoria'
            },
            color_discrete_map={
                'estelionato': '#2ca02c', 
                'roubo_rua': '#d62728'    
            }
    )


        fig_digital.for_each_trace(lambda t: t.update(name=legendas_digital[t.name]))

        st.plotly_chart(fig_digital, use_container_width=True)
elif choice == "Recortes Geográficos":
    st.header("Recortes Geográficos")
    st.write("Aqui você pode analisar a distribuição dos crimes em diferentes áreas geográficas.")
    tabs = st.tabs(["Foco Rio de Janeiro", "Grande Niterói", "Evolução de Roubo de Veículos: comparando a Capital e a Grande Niterói ao longo do tempo"])

    with tabs[0]:
        st.header("Rnaking das Ocorrências Policiais no Município do Rio de Janeiro")
        df_rio = df[df['fmun'] == 'Rio de Janeiro']
        nao_crimes = [
                'fmun', 'fmun_cod', 'ano', 'mes', 'regiao', 'municipio', 'delegacia', 
                'registro_ocorrencias', 'fase', 'AISP', 'RISP', 'CISP', 'mes_ano', 'data',
                'apf', 'cmp', 'aaapai', 'am', 'recuperacao_veiculos', 'encontro_cadaver', 
                'encontro_ossada', 'policiais_mortos_servico', 'pessoas_desaparecidas'
            ]
    
        cols_crime = [col for col in df.select_dtypes(include='number').columns if col not in nao_crimes]

        rio_crimes = df_rio[cols_crime].sum().reset_index()
        rio_crimes.columns = ['Tipo de Crime', 'Volume Acumulado']

       
        rio_crimes = rio_crimes[~rio_crimes['Tipo de Crime'].isin(['outros_roubos', 'outros_furtos'])]
        rio_top10 = rio_crimes.sort_values(by='Volume Acumulado', ascending=False).head(10)

      
        rio_top10['Tipo de Crime'] = rio_top10['Tipo de Crime'].str.replace('_', ' ').str.title()

       
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots(figsize=(10, 5))

        
        sns.barplot(
            data=rio_top10,
            x='Volume Acumulado',
            y='Tipo de Crime',
            palette='Reds_r', 
            ax=ax
        )

       
        ax.bar_label(ax.containers[0], fmt='{:,.0f}', padding=5, fontsize=10)

       
        ax.set_title("Top 10 Ocorrências Mais Registradas no Rio de Janeiro", fontsize=14, pad=15)
        ax.set_xlabel("Total de Ocorrências", fontsize=11)
        ax.set_ylabel("")
        sns.despine(bottom=True, left=True) 

        st.pyplot(fig)

        rio_interv = df_rio['hom_por_interv_policial'].sum()
        rio_letalidade = df_rio['letalidade_violenta'].sum()
        rio_outras = rio_letalidade - rio_interv
        rio_prop = (rio_interv / rio_letalidade) * 100

        st.subheader("Raio-X da Letalidade Violenta")

        col1, col2, col3 = st.columns(3)

        col1.metric("Letalidade Violenta (Total)", f"{rio_letalidade:,.0f}")
        col2.metric("Mortes por Intervenção Policial", f"{rio_interv:,.0f}")
        col3.metric("Proporção de Intervenção", f"{rio_prop:.1f}%")

        df_prop = pd.DataFrame({
            'Categoria': ['Intervenção Policial', 'Outras Causas Violentas'],
            'Total': [rio_interv, rio_outras]
        })

       
        fig_donut = px.pie(
            df_prop,
            names='Categoria',
            values='Total',
            hole=0.6,
            color='Categoria',
            color_discrete_map={
                'Intervenção Policial': '#d62728', 
                'Outras Causas Violentas': "#5c0303" 
            }
        )

        fig_donut.update_traces(textinfo='percent+label', textposition='inside')
        fig_donut.update_layout(showlegend=False, margin=dict(t=30, b=10, l=10, r=10))

        st.plotly_chart(fig_donut, use_container_width=True)

    with tabs[1]:
        st.header("Foco na região da Grande Niterói: Niterói, São Gonçalo, Itaboraí, Maricá")
        cidades_gn = ['Niterói', 'São Gonçalo', 'Maricá', 'Itaboraí']
        df_gn = df[df['fmun'].isin(cidades_gn)]

        gn_comp = df_gn.groupby('fmun')[['registro_ocorrencias', 'total_roubos', 'total_furtos', 'letalidade_violenta','estelionato','hom_doloso']].sum() #Agrupando por município
        gn_comp = gn_comp.sort_values(by='registro_ocorrencias', ascending=False)
        gn_grafico = gn_comp.drop(columns=['registro_ocorrencias']).reset_index()

     
        gn_melt = gn_grafico.melt(id_vars='fmun', var_name='Tipo de Crime', value_name='Total')

      
        gn_melt['Tipo de Crime'] = gn_melt['Tipo de Crime'].str.replace('_', ' ').str.title()

      
        fig_gn = px.bar(
            gn_melt,
            x='fmun',
            y='Total',
            color='Tipo de Crime',
            barmode='group', 
            text_auto='.0s', 
        )

        fig_gn.update_layout(
            xaxis_title="",
            yaxis_title="Volume de Ocorrências",
            legend_title="Categoria",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) 
        )

        st.plotly_chart(fig_gn, use_container_width=True)
    with tabs[2]:
        st.header("Evolução de Roubo de Veículos: comparando a Capital e a Grande Niterói ao longo do tempo")
        df_veh = df[df['regiao'].isin(['Capital', 'Grande Niterói'])]

        veh_evol = pd.pivot_table(
            df_veh, 
            values=['roubo_veiculo', 'furto_veiculos'], 
            index='ano', 
            columns='regiao', 
            aggfunc='sum'
        ) 
        st.info(
            " Até 2021, ambas as regiões seguiam a mesma tendência. "
            "A partir de 2022, a Grande Niterói consolida uma queda contínua, enquanto a Capital volta a oscilar para cima."
        )
        veh_agg = df_veh.groupby(['ano', 'regiao'])['roubo_veiculo'].sum().reset_index()


        col1, col2 = st.columns(2)


        with col1:
            dados_cap = veh_agg[veh_agg['regiao'] == 'Capital']
            fig_cap = px.line(
                dados_cap, x='ano', y='roubo_veiculo', 
                markers=True, title="Roubos na Capital",
                color_discrete_sequence=['#d62728'] # Vermelho
            )
            fig_cap.update_layout(xaxis_title="Ano", yaxis_title="Total de Roubos")
            st.plotly_chart(fig_cap, use_container_width=True)

        with col2:
            dados_gn = veh_agg[veh_agg['regiao'] == 'Grande Niterói']
            fig_gn = px.line(
                dados_gn, x='ano', y='roubo_veiculo', 
                markers=True, title="Roubos na Grande Niterói",
                color_discrete_sequence=['#1f77b4'] # Azul
            )
            fig_gn.update_layout(xaxis_title="Ano", yaxis_title="")
            st.plotly_chart(fig_gn, use_container_width=True)
elif choice == "Mudanças de Padrão":
    st.header("Mudanças de Padrão")
    st.write("Aqui você pode analisar mudanças de padrão nas ocorrências policiais ao longo do tempo.")
    tabs = st.tabs(["Impacto da Pandemia", "Índice de Recuperação de Bens e Ação Policial, o quão eficiente é a polícia na recuperação de bens?"])

    with tabs[0]:
        st.header("Impacto da Pandemia")
        condicoes = [
        df['ano'].isin([2018, 2019]),
        df['ano'].isin([2020, 2021]),
        df['ano'].isin([2022, 2023])
        ]
     
        escolhas = ['1. Pré-Pandemia (18-19)', '2. Pandemia (20-21)', '3. Pós-Pandemia (22-23)']
        df['periodo_pandemia'] = np.select(condicoes, escolhas, default='Outros')#criando uma nova coluna no datset que identifica se aquele ano faz parte de algum dos períodos, se fizer ele atribui um valor do array de escolhas 

        df_pandemia = df[df['periodo_pandemia'] != 'Outros']
        evolucao_anos = (
            df_pandemia.groupby('ano')[['roubo_em_coletivo', 'roubo_transeunte']]
            .sum()
            .reset_index()
        )

      
        df_melt = evolucao_anos.melt(
            id_vars='ano',
            value_vars=['roubo_em_coletivo', 'roubo_transeunte'],
            var_name='Tipo de Crime',
            value_name='Total',
        )

        df_melt['Tipo de Crime'] = df_melt['Tipo de Crime'].map(
            {'roubo_em_coletivo': 'Roubo em Coletivo', 'roubo_transeunte': 'Roubo a Transeunte'}
        )

       
        fig_linha = px.line(
            df_melt,
            x='ano',
            y='Total',
            color='Tipo de Crime',
            markers=True,
            title='Evolução Anual com Divisão dos Períodos',
            labels={'ano': 'Ano', 'Total': 'Total de Registros'},
        )

        
        fig_linha.add_vrect(
            x0=2017.5,
            x1=2019.5,
            fillcolor='blue',
            opacity=0.08,
            line_width=0,
            annotation_text='Pré-Pandemia',
            annotation_position='top left',
        )
        fig_linha.add_vrect(
            x0=2019.5,
            x1=2021.5,
            fillcolor='red',
            opacity=0.12,
            line_width=0,
            annotation_text='Pandemia',
            annotation_position='top left',
        )
        fig_linha.add_vrect(
            x0=2021.5,
            x1=2023.5,
            fillcolor='green',
            opacity=0.08,
            line_width=0,
            annotation_text='Pós-Pandemia',
            annotation_position='top left',
        )

        st.plotly_chart(fig_linha, use_container_width=True)
    with tabs[1]:
        st.header("Índice de Recuperação de Bens e Ação Policial, o quão eficiente é a polícia na recuperação de bens?")
        df_policia = df.groupby('ano')[['roubo_veiculo', 'furto_veiculos', 'recuperacao_veiculos', 'apf', 'cmp']].sum().reset_index()
        df_policia['taxa recuperacao veiculos (%)'] = (df_policia['recuperacao_veiculos'] / (df_policia['roubo_veiculo'] + df_policia['furto_veiculos'])) * 100

        col1, col2 = st.columns(2)
        with col1:
            fig_recuperacao = px.line(
            df_policia, 
            x='ano', 
            y='taxa recuperacao veiculos (%)',
            markers=True,
            title='Efetividade na Recuperação de Veículos',
            labels={'ano': 'Ano'}
            )
            
           
            fig_recuperacao.add_hline(
                y=50, 
                line_dash="dash", 
                line_color="green", 
                annotation_text="Marco de 50%", 
                annotation_position="top right"
            )
            
            fig_recuperacao.update_yaxes(range=[0, 100]) 
            st.plotly_chart(fig_recuperacao, use_container_width=True)
        with col2:
          
            df_prisoes = df_policia[['ano', 'apf', 'cmp']].melt(
                id_vars='ano', 
                var_name='Tipo de Prisão', 
                value_name='Total'
            )
            
            df_prisoes['Tipo de Prisão'] = df_prisoes['Tipo de Prisão'].map({
                'apf': 'Prisão em Flagrante (Reativa)', 
                'cmp': 'Mandado de Prisão (Investigativa)'
            })

            fig_prisoes = px.line(
                df_prisoes, 
                x='ano', 
                y='Total',
                color='Tipo de Prisão',
                markers=True,
                title='Perfil de Ação Policial: Flagrante vs Investigação',
                color_discrete_sequence=['#ff7f0e', '#1f77b4'],
                labels={'ano': 'Ano'}
            )
            
            fig_prisoes.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_prisoes, use_container_width=True)
elif choice == "Síntese":
    st.header("Síntese")
    st.write("Aqui você pode analisar a síntese de alguns insights obtidos.")
    st.markdown("Consolidação dos principais padrões criminais e direcionamentos estratégicos identificados na análise do ISP-RJ.")

    st.success(
        "**Mudança no Perfil Criminal**\n\n"
        "A janela de 2018–2020 marcou uma transição clara do crime físico (rua) para o crime digital (estelionato). "
        "Essa migração foi fortemente favorecida pela digitalização bancária e a criação do PIX.", 
        icon="💻"
    )

    st.error(
        "**Hotspots Geográficos e Alocação de Recursos**\n\n"
        "O município do Rio de Janeiro lidera isolado, registrando **4.435.884 ocorrências a mais** que o segundo colocado "
        "no ranking estadual, justificando a maior demanda por investimentos. Na região da Grande Niterói, **São Gonçalo** "
        "é o principal ponto crítico, apresentando as maiores taxas de roubo e violência.", 
        icon="📍"
    )

    st.info(
        "**Sazonalidade Preventiva**\n\n"
        "O primeiro trimestre é o período de maior vulnerabilidade para roubos e furtos. O planejamento de segurança e o "
        "policiamento devem ser maximizados nesta época para absorver o impacto do turismo de verão, praias e Carnaval.", 
        icon="🏖️"
    )

    st.warning(
        "**Perfil de Ação Policial**\n\n"
        "A queda expressiva no cumprimento de mandados de prisão (CMP), contrastando com o alto volume de prisões em flagrante (APF), "
        "sugere uma segurança pública altamente reativa. Há uma necessidade de retomada do foco em inteligência e investigação "
        "para acabar com a raiz das operações criminosas.",
        icon="🚓"
    )