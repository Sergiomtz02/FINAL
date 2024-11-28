import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import numpy as np
import requests


# Definimos la lista de instrumentos financieros como una variable global
ETFs_Data = [
    {"nombre": "AZ QQQ NASDAQ 100", "descripcion": "ETF que sigue el rendimiento del índice NASDAQ 100.", "simbolo": "QQQ"},
    {"nombre": "AZ SPDR S&P 500 ETF TRUST", "descripcion": "ETF que sigue el rendimiento del índice S&P 500.", "simbolo": "SPY"},
    {"nombre": "AZ SPDR DJIA TRUST", "descripcion": "ETF que sigue el rendimiento del índice Dow Jones Industrial Average.", "simbolo": "DIA"},
    {"nombre": "AZ VANGUARD EMERGING MARKET ETF", "descripcion": "ETF de Vanguard que sigue el rendimiento de mercados emergentes.", "simbolo": "VWO"},
    {"nombre": "AZ FINANCIAL SELECT SECTOR SPDR", "descripcion": "ETF que sigue el rendimiento del sector financiero de EE.UU.", "simbolo": "XLF"},
    {"nombre": "AZ HEALTH CARE SELECT SECTOR", "descripcion": "ETF que sigue el rendimiento del sector de salud de EE.UU.", "simbolo": "XLV"},
    {"nombre": "AZ DJ US HOME CONSTRUCT", "descripcion": "ETF que sigue el rendimiento del sector de construcción de viviendas en EE.UU.", "simbolo": "ITB"},
    {"nombre": "AZ SILVER TRUST", "descripcion": "ETF que sigue el precio de la plata.", "simbolo": "SLV"},
    {"nombre": "AZ MSCI TAIWAN INDEX FD", "descripcion": "ETF que sigue el rendimiento del índice MSCI Taiwan.", "simbolo": "EWT"},
    {"nombre": "AZ MSCI UNITED KINGDOM", "descripcion": "ETF que sigue el rendimiento del índice MSCI United Kingdom.", "simbolo": "EWU"},
    {"nombre": "AZ MSCI SOUTH KOREA IND", "descripcion": "ETF que sigue el rendimiento del índice MSCI South Korea.", "simbolo": "EWY"},
    {"nombre": "AZ MSCI EMU", "descripcion": "ETF que sigue el rendimiento del índice MSCI EMU (Unión Monetaria Europea).", "simbolo": "EZU"},
    {"nombre": "AZ MSCI JAPAN INDEX FD", "descripcion": "ETF que sigue el rendimiento del índice MSCI Japan.", "simbolo": "EWJ"},
    {"nombre": "AZ MSCI CANADA", "descripcion": "ETF que sigue el rendimiento del índice MSCI Canada.", "simbolo": "EWC"},
    {"nombre": "AZ MSCI GERMANY INDEX", "descripcion": "ETF que sigue el rendimiento del índice MSCI Germany.", "simbolo": "EWG"},
    {"nombre": "AZ MSCI AUSTRALIA INDEX", "descripcion": "ETF que sigue el rendimiento del índice MSCI Australia.", "simbolo": "EWA"},
    {"nombre": "AZ BARCLAYS AGGREGATE", "descripcion": "ETF que sigue el rendimiento del índice de bonos Barclays Aggregate.", "simbolo": "AGG"}
]

# Periodos a analizar
periodos = {
    "1 Mes": "1mo",
    "3 Meses": "3mo",
    "6 Meses": "6mo",
    "1 Año": "1y",
    "3 Años": "3y",
    "5 Años": "5y",
    "10 Años": "10y",
    "YTD": "ytd"
}

# Inicializar session_state
if 'nombre_cliente' not in st.session_state:
    st.session_state.nombre_cliente = ""
if 'pestaña_actual' not in st.session_state:
    st.session_state.pestaña_actual = 0  # Comienza en la primera pestaña

# Streamlit UI
st.title("Allianz Patrimonial")

# Crear pestañas
tabs = st.tabs(["Información del Cliente", "Análisis de ETFs", "Resultados","Perfiles","Análisis de Correlación entre ETFs"])

# Información Personal del Cliente
with tabs[0]:
    # Verificar si los datos han sido guardados
    if 'datos_guardados' in st.session_state and st.session_state.datos_guardados:
        st.header("Datos Guardados Correctamente")
        if st.button("Editar Información"):
            # Reiniciar los campos y la sesión
            st.session_state.datos_guardados = False  # Para poder editar nuevamente
            st.session_state.nombre_cliente = ""
            st.session_state.edad_cliente = 0
            st.session_state.genero_cliente = "Masculino"  # Establecer un valor predeterminado
            st.session_state.direccion_cliente = ""
            st.session_state.pais_cliente = ""
            st.session_state.nacionalidad_cliente = ""
            st.session_state.ocupacion_cliente = ""
            
    else:
        st.header("Información Personal del Cliente")
        nombre = st.text_input("Nombre:", value=st.session_state.get("nombre_cliente", ""))
        edad = st.number_input("Edad:", min_value=0, max_value=150, value=st.session_state.get("edad_cliente", 0))
        
        # Seleccionar género
        genero_opciones = ["Masculino", "Femenino", "Otro"]
        genero = st.selectbox("Género:", genero_opciones, index=genero_opciones.index(st.session_state.get("genero_cliente", "Masculino")) if st.session_state.get("genero_cliente") in genero_opciones else 0)

        direccion = st.text_input("Dirección:", value=st.session_state.get("direccion_cliente", ""))
        pais = st.text_input("País:", value=st.session_state.get("pais_cliente", ""))
        nacionalidad = st.text_input("Nacionalidad:", value=st.session_state.get("nacionalidad_cliente", ""))
        ocupacion = st.text_input("Ocupación:", value=st.session_state.get("ocupacion_cliente", ""))

        # Guardar la información del cliente
        if st.button("Guardar Información"):
            st.session_state.nombre_cliente = nombre
            st.session_state.edad_cliente = edad
            st.session_state.genero_cliente = genero
            st.session_state.direccion_cliente = direccion
            st.session_state.pais_cliente = pais
            st.session_state.nacionalidad_cliente = nacionalidad
            st.session_state.ocupacion_cliente = ocupacion
            
            # Marcar que los datos han sido guardados
            st.session_state.datos_guardados = True
             

# Análisis de ETFs (Pestaña 2)
with tabs[1]:
    # Mostrar mensaje de bienvenida con todos los datos del cliente si la información está guardada
    if st.session_state.nombre_cliente:
        st.write(f"**Bienvenido, {st.session_state.nombre_cliente}**")
        st.write(f"- **Edad**: {st.session_state.edad_cliente}")
        st.write(f"- **Género**: {st.session_state.genero_cliente}")
        st.write(f"- **Dirección**: {st.session_state.direccion_cliente}")
        st.write(f"- **País**: {st.session_state.pais_cliente}")
        st.write(f"- **Nacionalidad**: {st.session_state.nacionalidad_cliente}")
        st.write(f"- **Ocupación**: {st.session_state.ocupacion_cliente}")

    st.write("Analiza el rendimiento y riesgo de múltiples ETFs en periodos específicos.")
    
    etfs_seleccionados = st.multiselect("Selecciona ETFs para comparar:", [etf['nombre'] for etf in ETFs_Data])
    etf_symbols = [etf['simbolo'] for etf in ETFs_Data if etf['nombre'] in etfs_seleccionados]
    periodo_seleccionado = st.selectbox("Selecciona el periodo de análisis:", list(periodos.keys()))
    periodo = periodos[periodo_seleccionado]
    monto_invertir = st.number_input("Monto a invertir por ETF (USD):", min_value=0.0, step=1.0)

    # Nuevos campos para definir porcentajes optimista y pesimista
    porcentaje_optimista = st.number_input("Porcentaje de Rendimiento Optimista (%):", value=20, step=1)
    porcentaje_pesimista = st.number_input("Porcentaje de Rendimiento Pesimista (%):", value=20, step=1)

    st.header("ETFs")
    # Mostrar tabla con descripciones de los ETFs seleccionados
    if etfs_seleccionados:
        descripciones_df = pd.DataFrame({
            "Nombre del ETF": [etf["nombre"] for etf in ETFs_Data if etf["nombre"] in etfs_seleccionados],
            "Descripción": [etf["descripcion"] for etf in ETFs_Data if etf["nombre"] in etfs_seleccionados]
        })
        st.write("### Descripción de los ETFs Seleccionados")
        st.table(descripciones_df)

def calcular_rendimiento_riesgo_sharpe(etf_symbol, period, rf=0.02):
    # Descargar datos históricos del ETF
    data = yf.Ticker(etf_symbol).history(period=period)
    if data.empty:
        return None, None

    # Calcular rendimiento total
    precio_inicial = data['Close'].iloc[0]
    precio_final = data['Close'].iloc[-1]
    rendimiento = ((precio_final / precio_inicial) - 1) * 100

    # Calcular retornos diarios y desviación estándar
    retornos_diarios = data['Close'].pct_change().dropna()
    num_dias = len(data)  # Días hábiles reales en el período
    volatilidad = retornos_diarios.std() * (252 ** 0.5) * 100  # Volatilidad anualizada

    # Ajustar la tasa libre de riesgo al período
    tasa_libre_riesgo_ajustada = (rf * num_dias / 252) * 100

    # Calcular Sharpe Ratio
    sharpe_ratio = (rendimiento - tasa_libre_riesgo_ajustada) / volatilidad if volatilidad > 0 else None

    return {
        "ETF": etf_symbol,
        "Rendimiento Total (%)": round(rendimiento, 2),
        "Riesgo (Desviación Estándar Anualizada) (%)": round(volatilidad, 2),
        "Sharpe Ratio": round(sharpe_ratio, 2) if sharpe_ratio is not None else "N/A"
    }, data['Close']



def calcular_beta(etf_symbol, benchmark_symbol='SPY', period='1y'):
    # Descargar datos históricos
    etf_data = yf.Ticker(etf_symbol).history(period=period)
    benchmark_data = yf.Ticker(benchmark_symbol).history(period=period)

    # Verificar que los datos no estén vacíos
    if etf_data.empty or benchmark_data.empty:
        return None

    # Calcular retornos diarios
    etf_returns = etf_data['Close'].pct_change().dropna()
    benchmark_returns = benchmark_data['Close'].pct_change().dropna()

    # Alinear retornos
    combined_data = pd.concat([etf_returns, benchmark_returns], axis=1, join="inner")
    combined_data.columns = ['ETF', 'Benchmark']

    # Calcular covarianza y varianza
    cov_matrix = np.cov(combined_data['ETF'], combined_data['Benchmark'])
    covariance = cov_matrix[0, 1]
    variance = cov_matrix[1, 1]

    # Calcular Beta
    beta = covariance / variance
    return round(beta, 2)


with tabs[2]:
    if st.button("Calcular y Comparar Rendimiento, Riesgo, Sharpe Ratio y Beta"):
        if etf_symbols:
            resultados = []
            datos_graficos = pd.DataFrame()

            for etf in etf_symbols:
                # Cálculo de Rendimiento, Riesgo y Sharpe Ratio
                resultado, data_periodo = calcular_rendimiento_riesgo_sharpe(etf, periodo, rf=0.02)

                # Cálculo de Beta
                beta = calcular_beta(etf, benchmark_symbol='SPY', period=periodo)

                if resultado:
                    # Agregar Beta a los resultados
                    resultado["Beta"] = beta
                    resultados.append(resultado)

                    # Guardar datos históricos para gráficos
                    if data_periodo is not None:
                        datos_graficos[etf] = data_periodo

            if resultados:
                resultados_df = pd.DataFrame(resultados)

                # Redondear todos los valores numéricos a 2 decimales
                resultados_df = resultados_df.round(2)

                # Guardar resultados en session_state
                st.session_state.resultados_df = resultados_df

                # Mostrar resultados en tabla
                st.write("### Resultados Comparativos de Rendimiento, Riesgo, Sharpe Ratio y Beta:")
                st.dataframe(resultados_df)

                # **Explicación interactiva**
                with st.expander("¿Qué significan estas métricas?"):
                    st.markdown("""
                    - **Rendimiento Total (%)**: El cambio porcentual del valor del ETF durante el período analizado.
                    - **Riesgo (Volatilidad)**: Mide qué tan variable es el precio del ETF. Valores más altos indican mayor riesgo.
                    - **Sharpe Ratio**: Relación entre el rendimiento adicional y el riesgo asumido. Un Sharpe Ratio alto es mejor.
                    - **Beta**: Mide la relación del ETF con el mercado (representado por SPY):
                        - **Beta > 1**: Más volátil que el mercado.
                        - **Beta < 1**: Menos volátil que el mercado.
                        - **Beta = 1**: Se mueve igual que el mercado.
                    """)

                # Comparación de Escenarios
                escenarios_dfs = []

                for res in resultados:
                    rendimiento_total = res["Rendimiento Total (%)"]
                    retorno_inversion = (monto_invertir * rendimiento_total) / 100

                    # Escenarios usando los porcentajes seleccionados por el usuario
                    rendimiento_optimista = rendimiento_total + porcentaje_optimista
                    rendimiento_neutro = rendimiento_total
                    rendimiento_pesimista = rendimiento_total - porcentaje_pesimista

                    # Calcular retornos para cada escenario
                    escenarios_dfs.append({
                        "ETF": res["ETF"],
                        "Optimista": round((monto_invertir * rendimiento_optimista) / 100, 2),
                        "Neutro": round(retorno_inversion, 2),
                        "Pesimista": round((monto_invertir * rendimiento_pesimista) / 100, 2)
                    })

                # Crear DataFrame para los escenarios y redondear valores
                escenarios_df = pd.DataFrame(escenarios_dfs).round(2)
                st.write("### Tabla de Comparación de Retornos Estimados en Diferentes Escenarios")
                st.dataframe(escenarios_df)

                # **Explicación interactiva para escenarios**
                with st.expander("¿Qué significan estos escenarios?"):
                    st.markdown("""
                    - **Optimista**: Supone que el ETF tiene un rendimiento superior al histórico por un porcentaje adicional definido.
                    - **Neutro**: Usa el rendimiento histórico calculado para estimar ganancias.
                    - **Pesimista**: Supone que el ETF tiene un rendimiento inferior al histórico por un porcentaje definido.
                    """)

                # Gráfico de los escenarios
                fig_escenarios = px.bar(
                    escenarios_df.melt(id_vars="ETF", var_name="Escenario", value_name="Retorno Estimado (USD)"),
                    x="ETF",
                    y="Retorno Estimado (USD)",
                    color="Escenario",
                    barmode="group",
                    text="Retorno Estimado (USD)",
                    title="Comparación de Retornos Estimados por ETF y Escenario"
                )
                fig_escenarios.update_traces(texttemplate='%{text:.2f}')  # Mostrar valores en el gráfico con 2 decimales
                st.plotly_chart(fig_escenarios)

                # Gráfica de todos los precios de cierre en una sola gráfica
                datos_graficos.reset_index(inplace=True)
                datos_graficos = datos_graficos.melt(id_vars=["Date"], var_name="ETF", value_name="Precio de Cierre")
                fig = px.line(datos_graficos, x="Date", y="Precio de Cierre", color="ETF",
                              title=f"Comparación de Precios de Cierre de ETFs Seleccionados en {periodo_seleccionado}",
                              labels={"Date": "Fecha", "Precio de Cierre": "Precio de Cierre (USD)"})
                fig.update_layout(template="plotly_dark", title_font=dict(size=20), title_x=0.5)
                st.plotly_chart(fig)

                # Gráfico de Volatilidad de los ETFs (lineal)
                fig_volatilidad = px.bar(resultados_df, x="ETF", y="Riesgo (Desviación Estándar Anualizada) (%)",
                                         text="Riesgo (Desviación Estándar Anualizada) (%)",
                                         title="Volatilidad de los ETFs Seleccionados",
                                         labels={"Riesgo (Desviación Estándar Anualizada) (%)": "Volatilidad (%)"})
                fig_volatilidad.update_traces(texttemplate='%{text:.2f}')
                st.plotly_chart(fig_volatilidad)

                # Gráfico de Rendimiento de los ETFs (lineal)
                fig_rendimiento = px.bar(resultados_df, x="ETF", y="Rendimiento Total (%)",
                                         text="Rendimiento Total (%)",
                                         title="Rendimiento Total de los ETFs Seleccionados",
                                         labels={"Rendimiento Total (%)": "Rendimiento (%)"})
                fig_rendimiento.update_traces(texttemplate='%{text:.2f}')
                st.plotly_chart(fig_rendimiento)

                # Gráfico de Sharpe Ratio
                st.write("### Gráfico de Sharpe Ratio:")
                fig_sharpe = px.bar(resultados_df, x="ETF", y="Sharpe Ratio",
                                    text="Sharpe Ratio",
                                    title="Comparación de Sharpe Ratio de los ETFs Seleccionados",
                                    labels={"Sharpe Ratio": "Sharpe Ratio"})
                fig_sharpe.update_traces(texttemplate='%{text:.2f}')
                st.plotly_chart(fig_sharpe)

                # Gráfico de Beta
                st.write("### Gráfico de Beta:")
                fig_beta = px.bar(resultados_df, x="ETF", y="Beta",
                                  text="Beta",
                                  title="Comparación de Beta de los ETFs Seleccionados",
                                  labels={"Beta": "Beta"})
                fig_beta.update_traces(texttemplate='%{text:.2f}')
                st.plotly_chart(fig_beta)
            else:
                st.write("No se encontraron resultados para los ETFs seleccionados.")

 
    
with tabs[3]:  # Cuarta pestaña: Perfil de Inversión
    st.header("💼 Perfiles 📊")

    # Verificar si hay datos calculados
    if 'resultados_df' not in st.session_state or st.session_state.resultados_df is None:
        st.warning("⚠️ Aún no se han calculado los datos de los ETFs. Ve a la pestaña 'Resultados' y calcula primero los resultados.")
    else:
        resultados_df = st.session_state.resultados_df

        # Selección del perfil de inversión
        st.write("### Selecciona tu perfil:")
        perfil = st.radio("🔍 Elige tu perfil:", ["Conservador", "Agresivo", "Óptimo"])

        # Explicación adicional
        with st.expander("ℹ️ ¿Cómo se calculan estos perfiles?"):
            st.markdown("""
            - **Conservador**:
              - Minimiza el riesgo (volatilidad) para proteger el capital.
              - Selecciona los activos con menor desviación estándar anualizada.
            - **Agresivo**:
              - Maximiza el rendimiento total sin priorizar el riesgo.
              - Selecciona los activos con el mayor porcentaje de rendimiento total.
            - **Óptimo**:
              - Maximiza el retorno ajustado al riesgo (Sharpe Ratio).
              - Selecciona los activos más eficientes en términos de rendimiento por unidad de riesgo asumido.
            """)

        # Configuración del portafolio según el perfil seleccionado
        if perfil == "Conservador":
            st.write("### 🌿 Perfil Conservador")
            st.markdown("""
            - **Objetivo**: Minimizar el riesgo y proteger el capital.
            - **Criterio**: Selección de activos con el menor riesgo (volatilidad).
            """)
            portafolio = resultados_df.sort_values("Riesgo (Desviación Estándar Anualizada) (%)").head(5)
        elif perfil == "Agresivo":
            st.write("### 🚀 Perfil Agresivo")
            st.markdown("""
            - **Objetivo**: Maximizar el rendimiento sin considerar el riesgo.
            - **Criterio**: Selección de activos con el mayor rendimiento total.
            """)
            portafolio = resultados_df.sort_values("Rendimiento Total (%)", ascending=False).head(5)
        elif perfil == "Óptimo":
            st.write("### ⚖️ Perfil Óptimo")
            st.markdown("""
            - **Objetivo**: Maximizar el retorno ajustado al riesgo.
            - **Criterio**: Selección de activos con el mayor Sharpe Ratio.
            """)
            portafolio = resultados_df.sort_values("Sharpe Ratio", ascending=False).head(5)

        # Mostrar el portafolio generado
        st.write(f"### Portafolio para el Perfil: **{perfil}**")
        st.markdown("🗂️ Estos son los ETFs seleccionados según el perfil elegido:")
        st.dataframe(portafolio[["ETF", "Rendimiento Total (%)", "Riesgo (Desviación Estándar Anualizada) (%)", "Sharpe Ratio", "Beta"]])

        # Gráfico comparativo de métricas relevantes
        st.write("### 📊 Comparación de Métricas del Portafolio")
        col1, col2 = st.columns(2)

        with col1:
            fig_rendimiento = px.bar(
                portafolio,
                x="ETF",
                y="Rendimiento Total (%)",
                title="🎯 Rendimiento Total (%) por ETF",
                labels={"Rendimiento Total (%)": "Rendimiento (%)"},
                color="Rendimiento Total (%)",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_rendimiento, use_container_width=True)

        with col2:
            fig_riesgo = px.bar(
                portafolio,
                x="ETF",
                y="Riesgo (Desviación Estándar Anualizada) (%)",
                title="⚠️ Riesgo (Volatilidad) por ETF",
                labels={"Riesgo (Desviación Estándar Anualizada) (%)": "Riesgo (%)"},
                color="Riesgo (Desviación Estándar Anualizada) (%)",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_riesgo, use_container_width=True)

        # Gráfico de Sharpe Ratio
        st.write("### 🔍 Sharpe Ratio por ETF")
        fig_sharpe = px.bar(
            portafolio,
            x="ETF",
            y="Sharpe Ratio",
            title="🔍 Sharpe Ratio por ETF",
            labels={"Sharpe Ratio": "Sharpe Ratio"},
            color="Sharpe Ratio",
            color_continuous_scale="Plasma"
        )
        st.plotly_chart(fig_sharpe, use_container_width=True)

# Agregar una pestaña nueva para el análisis de correlación
with tabs[4]:  # Suponiendo que es la quinta pestaña
    st.header("📊 Análisis de Correlación entre ETFs")

    # Descripción de la funcionalidad
    st.write("Selecciona los ETFs y el período para analizar su correlación y generar una matriz de correlación.")
    
    # Selección de ETFs
    etfs_seleccionados = st.multiselect(
        "Selecciona los ETFs para analizar:", 
        [etf["simbolo"] for etf in ETFs_Data],
        default=["QQQ", "SPY", "DIA"]
    )

    # Selección del período de análisis
    periodo = st.selectbox(
        "Selecciona el período de análisis:", 
        ["1 Mes", "3 Meses", "6 Meses", "1 Año", "3 Años", "5 Años"]
    )
    periodo_mapping = {
        "1 Mes": "1mo",
        "3 Meses": "3mo",
        "6 Meses": "6mo",
        "1 Año": "1y",
        "3 Años": "3y",
        "5 Años": "5y"
    }
    periodo_seleccionado = periodo_mapping[periodo]

    # Función para calcular matriz de correlación
    def calcular_matriz_correlacion(etfs, periodo):
        precios_cierre = {}

        # Descargar datos históricos para cada ETF seleccionado
        for etf in etfs:
            datos = yf.Ticker(etf).history(period=periodo)
            if not datos.empty:
                precios_cierre[etf] = datos['Close']
            else:
                st.warning(f"No se encontraron datos para el ETF: {etf}")

        # Crear DataFrame de precios de cierre
        precios_df = pd.DataFrame(precios_cierre)

        # Calcular retornos diarios
        retornos_diarios = precios_df.pct_change().dropna()

        # Calcular la matriz de correlación
        matriz_correlacion = retornos_diarios.corr()

        return matriz_correlacion

    # Calcular y mostrar matriz de correlación
    if st.button("Calcular correlación"):
        if len(etfs_seleccionados) < 2:
            st.warning("Por favor, selecciona al menos 2 ETFs para analizar.")
        else:
            st.write(f"### Matriz de Correlación para los ETFs seleccionados ({periodo})")
            matriz_correlacion = calcular_matriz_correlacion(etfs_seleccionados, periodo_seleccionado)
            
            # Mostrar heatmap
            fig = px.imshow(
                matriz_correlacion,
                labels=dict(x="ETF", y="ETF", color="Correlación"),
                x=matriz_correlacion.columns,
                y=matriz_correlacion.columns,
                color_continuous_scale="Viridis",
                title="Heatmap de Correlación entre ETFs"
            )
            st.plotly_chart(fig, use_container_width=True)

    # Explicación adicional sobre la matriz de correlación
    with st.expander("ℹ️ ¿Qué significa la matriz de correlación?"):
        st.markdown("""
        ### ¿Qué es la correlación?
        - La **correlación** mide qué tan similares son los movimientos de dos ETFs:
            - **1 (correlación positiva perfecta)**: Si un ETF sube, el otro también sube en la misma proporción.
            - **0 (sin correlación)**: Los movimientos de los ETFs no están relacionados; pueden subir, bajar o mantenerse sin seguir un patrón común.
            - **-1 (correlación negativa perfecta)**: Si un ETF sube, el otro baja en la misma proporción.

        ### ¿Por qué es importante?
        - **Diversificación**:
            - Al invertir en ETFs con **baja correlación** (cercana a 0) o **correlación negativa** (menor a 0), reduces el riesgo general del portafolio.
            - Ejemplo: Si un ETF pierde valor, otro ETF no relacionado puede mantener su valor o incluso ganar.
        - **Concentración de riesgos**:
            - ETFs con **alta correlación** (cercana a 1) se comportan de manera similar. Si uno baja, es probable que el otro también lo haga.

        ### ¿Cómo leer el heatmap?
        - Los colores representan la **fuerza de la relación**:
            - **Tonos claros**: Correlación alta, positiva o negativa (muy relacionados).
            - **Tonos oscuros**: Correlación baja o cercana a 0 (poco relacionados).
        - Busca combinaciones de ETFs con colores oscuros para diversificar y reducir riesgos.
        """)














