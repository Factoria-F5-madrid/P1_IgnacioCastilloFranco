# 🚕 Proyecto Python: Taxímetro Digital (Proyecto nº1 del Bootcamp de IA de Factoria F5 [Promocion 2025])

![Banner Proyectos](https://github.com/user-attachments/assets/bc6e34f7-4031-43dd-8cfc-805c935ba3c4)

## 📝 Descripción del Programa

Este programa Taxímetro CLI (Interfaz de Línea de Comandos) está escrito en Python. Permite al conductor de un taxi gestionar de manera precisa y eficiente el cobro de los trayectos a realizar. 

### 🟢 Nivel Esencial

- El programa permite iniciar y finalizar trayectos, pausando el viaje en cualquier punto del trayecto. En cualquier momento del trayecto el viajero puede solicitar al conductor la pausa del viaje (y la parada del vehículo porque necesite realizar alguna gestión personal fuera del mismo). Durante el viaje, la tarifa a pagar es más baja mientras éste está pausado.
- Logs de ejecución (persistentes en fichero)
- Interfaz de línea de comandos con colores y formato mejorado
- Tarifas diferenciadas: 2 céntimos/segundo (parado) y 5 céntimos/segundo (en movimiento)

## 🚀 Instrucciones de Ejecución

### Prerrequisitos
- Python 3.6 o superior
- Terminal compatible con ANSI escape sequences (la mayoría de terminales modernos)
- Tamaño de terminal recomendado: 80x24 o mayor

### Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Factoria-F5-madrid/P1_IgnacioCastilloFranco.git
   cd P1_IgnacioCastilloFranco
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Las dependencias incluyen:
   - `blessed`: Para capacidades avanzadas de terminal
   - `colorlog`: Para logging con colores
   - `wcwidth`: Para manejo de caracteres Unicode

3. **Ejecutar el programa:**
   ```bash
   python main.py
   ```

### 📋 Comandos Disponibles

Una vez iniciado el programa, puedes usar los siguientes comandos:

- **`start`** - Iniciar un nuevo viaje
- **`moving`** - Cambiar a tarifa de movimiento (5 céntimos/segundo)
- **`stopped`** - Cambiar a tarifa de parada (2 céntimos/segundo)
- **`status`** - Ver estado actual y tarifa acumulada
- **`finish`** - Finalizar viaje y mostrar total a pagar
- **`help`** - Mostrar pantalla de ayuda
- **`exit`** - Salir del programa

### 💡 Ejemplo de Uso

```
➤ Enter a command: start
🚀 Trip started!
📍 Initial state: STOPPED
⏰ Start time: 14:30:15

➤ Enter a command: moving
🔄 State changed to: MOVING
🚗 Taxi moving - Rate: 5 cents/second

➤ Enter a command: status
📊 CURRENT TAXIMETER STATUS
🚦 State: MOVING
⏱️  Elapsed time: 45.2 seconds
💰 Current total: 2.26€
📈 Current rate: 5 cents per second

➤ Enter a command: finish
🏁 TRIP FINISHED
⏱️  Total duration: 60.5 seconds
💰 TOTAL TO PAY: 3.03€
⏰ End time: 14:31:15
```

### 📝 Logs

El programa genera automáticamente archivos de log con el formato:
`taximeter_YYYYMMDD_HHMMSS.log`

Estos archivos contienen un registro detallado de todas las operaciones realizadas durante la sesión.

## 🛠️ Capturas de pantalla

- Enlace al tablero Kanban utilizado para la organización del proyecto: https://github.com/orgs/Factoria-F5-madrid/projects/3
