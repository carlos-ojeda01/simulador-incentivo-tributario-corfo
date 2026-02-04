import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador Beneficio I+D Corfo", layout="wide")
st.title("🧪 Simulador de Beneficio Tributario I+D")

# --- 1. ENTRADAS ---
with st.sidebar:
    st.header("Configuración de Parámetros")
    ventas = st.number_input("Ventas Totales ($)", value=20000000, step=1000000, min_value=0)
    st.caption(f"Monto: **${ventas:,.0f}**")
    
    gastos_operacionales = st.number_input("Gastos Operacionales (sin I+D) ($)", value=7000000, step=500000, min_value=0)
    st.caption(f"Monto: **${gastos_operacionales:,.0f}**")
    
    gasto_id = st.number_input("Inversión en I+D ($)", value=3000000, step=1000000, min_value=0)
    st.caption(f"Monto: **${gasto_id:,.0f}**")
    
    regimenes = {
        "Pro-Pyme Transitorio (12.5%)": 0.125,
        "Pro-Pyme General (25%)": 0.25,
        "Régimen General (27%)": 0.27
    }
    regimen_seleccionado = st.selectbox("Régimen Tributario", options=list(regimenes.keys()))
    tasa_impuesto = regimenes[regimen_seleccionado]

# --- 2. CÁLCULOS ---
# Escenario Sin Beneficio (El 100% del I+D es deducible bajo Art. 31 LIR)
base_imponible_sin = ventas - gastos_operacionales - gasto_id
impuesto_sin = max(0, base_imponible_sin * tasa_impuesto)
flujo_sin = ventas - gastos_operacionales - gasto_id - impuesto_sin

# Escenario Con Beneficio (Ley 20.241)
gasto_aceptado_id = gasto_id * 0.65  # El 65% se va a gasto aceptado
credito_id = gasto_id * 0.35        # El 35% es crédito directo al impuesto

base_imponible_con = ventas - gastos_operacionales - gasto_aceptado_id
impuesto_teorico = max(0, base_imponible_con * tasa_impuesto)

# El crédito se aplica contra el impuesto determinado. No hay devolución de excedentes.
impuesto_final_con = max(0, impuesto_teorico - credito_id)
remanente_credito = max(0, credito_id - impuesto_teorico)

flujo_con = ventas - gastos_operacionales - gasto_id - impuesto_final_con

# --- 3. COMPARATIVA ---
ahorro_monetario = flujo_con - flujo_sin
incremento_liquidez = (ahorro_monetario / flujo_sin) * 100 if flujo_sin > 0 else 0
tasa_recuperacion_efectiva = (ahorro_monetario / gasto_id) * 100 if gasto_id > 0 else 0

# Mostrar métricas clave
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ahorro Neto en Caja", f"${ahorro_monetario:,.0f}")
col2.metric("Incremento de Liquidez", f"{incremento_liquidez:.2f}%")
col3.metric("Recuperación de Inversión", f"{tasa_recuperacion_efectiva:.1f}%", 
            help="Es el ahorro incremental neto que genera Corfo comparado con declarar el I+D como gasto común. Representa el 'Cash Back' real sobre tu inversión.")
col4.metric("Impuesto Final", f"${impuesto_final_con:,.0f}", delta=f"-{impuesto_sin - impuesto_final_con:,.0f}")

if remanente_credito > 0:
    st.info(f"💡 **Nota:** Existe un excedente de crédito de **${remanente_credito:,.0f}** que no pudo usarse este año y queda disponible para el futuro.")

# --- 4. ANÁLISIS DE OPTIMIZACIÓN ---
st.divider()
st.subheader("🎯 Optimización Tributaria")

utilidad_pre_id = max(0, ventas - gastos_operacionales)
inversion_optima = (utilidad_pre_id * tasa_impuesto) / (0.35 + 0.65 * tasa_impuesto)

col_opt1, col_opt2 = st.columns(2)

with col_opt1:
    st.write(f"Para tu nivel de utilidad actual, la inversión en I+D que reduce tu impuesto a **exactamente cero** es:")
    st.subheader(f"${inversion_optima:,.0f}")

with col_opt2:
    if abs(gasto_id - inversion_optima) <= 1:
        st.success("🎉 ¡Felicidades! Tu inversión en I+D está en el punto de equilibrio perfecto para maximizar el beneficio tributario este año.")
    elif gasto_id > inversion_optima:
        st.warning(f"Tu inversión actual supera el punto de equilibrio tributario. Estás acumulando crédito para ejercicios futuros.")
    else:
        espacio_adicional = inversion_optima - gasto_id
        st.success(f"Podrías invertir hasta **${espacio_adicional:,.0f}** adicionales en I+D este año sin pagar un peso de impuesto.")

# --- 5. ESTADOS FINANCIEROS COMPARATIVOS ---
st.divider()

st.subheader("📋 Estado de Resultados")
df_er = pd.DataFrame({
    "Concepto": [
        "Ventas",
        "Gastos Operacionales",
        "Gasto I+D Deducible",
        "Base Imponible",
        "Impuesto Determinado",
        "Crédito I+D Aplicado",
        "Utilidad Neta"
    ],
    "Sin Beneficio": [
        ventas,
        -gastos_operacionales,
        -gasto_id,
        base_imponible_sin,
        -impuesto_sin,
        0,
        base_imponible_sin - impuesto_sin
    ],
    "Con Beneficio": [
        ventas,
        -gastos_operacionales,
        -gasto_aceptado_id,
        base_imponible_con,
        -impuesto_teorico,
        min(credito_id, impuesto_teorico),
        base_imponible_con - impuesto_final_con
    ]
})
st.table(df_er.style.format({col: "${:,.0f}" for col in ["Sin Beneficio", "Con Beneficio"]}))

st.divider()

st.subheader("💰 Flujo de Caja")
df_fc = pd.DataFrame({
    "Concepto": [
        "Ingresos por Ventas",
        "Egresos Operacionales",
        "Inversión Real I+D",
        "Pago de Impuesto",
        "Flujo de Caja Neto"
    ],
    "Sin Beneficio": [
        ventas,
        -gastos_operacionales,
        -gasto_id,
        -impuesto_sin,
        flujo_sin
    ],
    "Con Beneficio": [
        ventas,
        -gastos_operacionales,
        -gasto_id,
        -impuesto_final_con,
        flujo_con
    ]
})
st.table(df_fc.style.format({col: "${:,.0f}" for col in ["Sin Beneficio", "Con Beneficio"]}))
