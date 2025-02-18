import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Cargar datos desde Google Sheets
def cargar_datos():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdoYbngv7jBofQIEtnuoeylBn0o0TEY8NiPOZ43VmLvz7AGfmNFdveUB_DVLIRC2bJVZnO4XI0vqdb/pub?output=csv"
    return pd.read_csv(url)

# Llamar a la función que carga los datos
df = cargar_datos()

# Definir la meta de recaudación y el costo por bombero
meta = 42108664
costo_por_bombero = meta / 33  # Costo de equipar a un bombero

# Calcular total recaudado
total_recaudado = df["monto recaudado"].sum()

# Calcular el porcentaje de avance
porcentaje_avance = (total_recaudado / meta) * 100

# Calcular la cantidad de bomberos equipados
bomberos_equipados = total_recaudado / costo_por_bombero

# Mostrar los datos en la app
st.title("Avance de la Colecta")

# Mostrar la cantidad de bomberos equipados con un solo decimal en color rojo
st.markdown(f"<h3 style='color:red;'>Bomberos equipados: {bomberos_equipados:.1f}</h3>", unsafe_allow_html=True)

# Mostrar el monto recaudado y lo que falta
st.metric(
    label="Monto Recaudado",
    value=f"${total_recaudado:,.2f}",
    delta=f"${meta - total_recaudado:,.2f} faltan",
)

# Crear el medidor circular para mostrar el porcentaje de avance
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=porcentaje_avance,
    title={"text": "Porcentaje Recaudado", "font": {"size": 20}},
    number={"suffix": "%", "font": {"size": 30}},  # Aquí se agrega el símbolo %
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "green"},
        "steps": [
            {"range": [0, 25], "color": "red"},
            {"range": [25, 50], "color": "yellow"},
            {"range": [50, 75], "color": "orange"},
            {"range": [75, 100], "color": "green"},
        ],
    }
))

# Mostrar el medidor circular
st.plotly_chart(gauge, use_container_width=True, key=f"gauge_chart_{int(porcentaje_avance)}")

# Agregar el texto al pie de la página con negritas
st.markdown("""
    ---
    **Asociación de Bomberos Voluntarios de El Hoyo**  
    Colecta Solidaria 2025 destinada a la compra de elementos de protección personal contra incendios forestales e interfase.  
    Síguenos en Instagram: [@bomberoseh](https://www.instagram.com/bomberoseh)  
    Facebook: [Bomberos Voluntarios El Hoyo](https://www.facebook.com/bomberosvoluntarioselhoyo)  

    **Correo de contacto:** [contacto@bomberoseh.org](mailto:contacto@bomberoseh.org)

    **Realiza tu donación:** [Haz tu donación aquí](https://www.transferlink.com/donacion)
""")

