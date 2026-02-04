# Simulador de Beneficio Tributario I+D (Ley 20.241) 🇨🇱

Este proyecto es una herramienta interactiva desarrollada en **Python** y **Streamlit** diseñada para ayudar a empresas chilenas (especialmente Startups y EBCT) a proyectar el ahorro real en flujo de caja al acogerse al incentivo tributario a la Investigación y Desarrollo (I+D) de Corfo.

## 🧠 El Problema: El Ahorro No es Directamente el 35%
Un error común es pensar que el beneficio reduce el costo del proyecto en un 35% lineal. Sin embargo, dado que el monto utilizado como **Crédito Fiscal** no puede deducirse simultáneamente como **Gasto Aceptado**, el beneficio neto real depende de la tasa de impuesto de la empresa.

### Metodología de Cálculo
El simulador aplica la siguiente lógica financiera para determinar el ahorro neto ($A_n$) sobre la inversión ($I$):

$$A_n = I \cdot 0,35 \cdot (1 - t)$$

Donde:
* **t = 12,5%**: Tramo Pyme (Pro Pyme General). **Ahorro Real: 30,6%**
* **t = 25,0%**: Régimen Pro Pyme. **Ahorro Real: 26,2%**
* **t = 27,0%**: Régimen General. **Ahorro Real: 25,5%**

## 🚀 Instalación y Uso Local

Si deseas ejecutar este simulador en tu máquina local, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/carlos-ojeda01/simulador-incentivo-tributario-corfo.git
   cd simulador-incentivo-tributario-corfo