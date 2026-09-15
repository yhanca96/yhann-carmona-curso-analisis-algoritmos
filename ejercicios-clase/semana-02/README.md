Semana 02 — Entorno de trabajo en Python

El entorno virtual se creó una sola vez en la raíz del repositorio con python -m venv venv y se activa con venv\Scripts\Activate.ps1 en Windows (o source venv/bin/activate en macOS/Linux); el prompt debe mostrar (venv) mientras está activo, y deactivate lo cierra.

Con el entorno activado se instaló matplotlib (pip install matplotlib) y se generó requirements.txt en la raíz con pip freeze > requirements.txt.

Para reproducir este entorno en otra máquina: clonar el repositorio, crear un venv nuevo, activarlo e instalar todo con pip install -r requirements.txt. Esto deja exactamente las mismas librerías y versiones usadas aquí, sin tocar el Python global del sistema.
