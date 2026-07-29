# Password Strength Checker 🔐

Evaluador de fortaleza de contraseñas con interfaz web. Analiza entropía, patrones débiles, y verifica si la contraseña ha sido expuesta en filtraciones de datos conocidas — todo sin comprometer la privacidad del usuario.

## 🎯 Características

- Cálculo de **entropía en bits** según longitud y variedad de caracteres.
- Detección de patrones débiles: secuencias de teclado (`qwerty`, `abcd`), repeticiones (`aaa`, `111`), y contraseñas comunes conocidas.
- Verificación contra filtraciones reales usando la API de **Have I Been Pwned (HIBP)**.
- Estimación del tiempo que tardaría un ataque de fuerza bruta en romper la contraseña.
- Sugerencias personalizadas para mejorar la contraseña ingresada.

## 🛠️ Tecnologías

- **Backend**: Python, Flask
- **Lógica de análisis**: expresiones regulares, cálculo de entropía con `math`
- **Integración externa**: API de Have I Been Pwned (Pwned Passwords)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Despliegue**: Render

## 🔒 Consideraciones de seguridad y privacidad

- **La contraseña nunca se almacena ni se registra en logs** — se procesa en memoria y se descarta inmediatamente después del análisis.
- La verificación contra HIBP usa el método de **k-anonimato**: solo se envían los primeros 5 caracteres del hash SHA-1 de la contraseña a la API externa, nunca la contraseña completa ni su hash completo. Esto significa que ni siquiera Have I Been Pwned puede reconstruir la contraseña real a partir de la consulta.

## 🚀 Cómo correrlo localmente

```bash
git clone https://github.com/ChristianCiber/password-strength-checker.git
cd password-strength-checker
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
```

Abre `http://127.0.0.1:5000` en tu navegador.

## 🌐 Demo en vivo

[Ver demo](https://password-strength-checker-bka7.onrender.com)

> Nota: el hosting gratuito de Render puede tardar unos segundos en "despertar" si no ha tenido tráfico reciente.

## 📁 Estructura del proyecto

password-strength-checker/
├── app.py # Rutas Flask
├── analyzer.py # Lógica de análisis: entropía, patrones, HIBP
├── templates/
│ └── index.html
├── static/
│ ├── css/style.css
│ └── js/script.js
└── requirements.txt


## 👤 Autor

**Christian Serrano** — Ingeniero en Ciberseguridad
[LinkedIn](https://www.linkedin.com/in/christian-serrano-388902425/) · [Portafolio](https://christianciber.github.io/cybersecurity-portfolio/)
