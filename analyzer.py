import re
import math
import hashlib
import requests


CONTRASENAS_COMUNES = {
    "123456", "123456789", "qwerty", "password", "12345",
    "12345678", "111111", "1234567", "sunshine", "iloveyou",
    "admin", "welcome", "monkey", "login", "abc123",
    "starwars", "123123", "dragon", "passw0rd", "master",
    "hello", "freedom", "whatever", "qazwsx", "trustno1"
}

SECUENCIAS = [
    "0123456789", "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiop", "asdfghjkl", "zxcvbnm"
]


def calcular_entropia(password):
    tamano_alfabeto = 0

    if re.search(r'[a-z]', password):
        tamano_alfabeto += 26
    if re.search(r'[A-Z]', password):
        tamano_alfabeto += 26
    if re.search(r'[0-9]', password):
        tamano_alfabeto += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        tamano_alfabeto += 32

    if tamano_alfabeto == 0:
        return 0

    entropia = len(password) * math.log2(tamano_alfabeto)
    return round(entropia, 2)


def detectar_secuencias(password):
    password_lower = password.lower()

    for secuencia in SECUENCIAS:
        for i in range(len(secuencia) - 3):
            fragmento = secuencia[i:i + 4]
            if fragmento in password_lower:
                return True

    return False


def detectar_repeticiones(password):
    return bool(re.search(r'(.)\1{2,}', password))


def verificar_filtracion_hibp(password):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefijo = sha1_hash[:5]
    sufijo = sha1_hash[5:]

    try:
        respuesta = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefijo}",
            timeout=3
        )
        respuesta.raise_for_status()

        for linea in respuesta.text.splitlines():
            hash_sufijo, conteo = linea.split(":")
            if hash_sufijo == sufijo:
                return int(conteo)

        return 0

    except requests.RequestException:
        return None


def calcular_tiempo_crackeo(entropia):
    intentos_por_segundo = 10_000_000_000
    combinaciones = 2 ** entropia
    segundos = combinaciones / intentos_por_segundo / 2

    if segundos < 1:
        return "Instantáneo"
    elif segundos < 60:
        return f"{segundos:.0f} segundos"
    elif segundos < 3600:
        return f"{segundos / 60:.0f} minutos"
    elif segundos < 86400:
        return f"{segundos / 3600:.0f} horas"
    elif segundos < 31536000:
        return f"{segundos / 86400:.0f} días"
    elif segundos < 31536000 * 100:
        return f"{segundos / 31536000:.0f} años"
    else:
        return "Más de un siglo"


def analizar_password(password):

    if not password:
        return {"error": "La contraseña no puede estar vacía"}

    problemas = []
    sugerencias = []

    longitud = len(password)

    if longitud < 8:
        problemas.append("Es demasiado corta")
        sugerencias.append("Usa al menos 12 caracteres")
    elif longitud < 12:
        sugerencias.append("Considera usar 12+ caracteres para mayor seguridad")

    tiene_minuscula = bool(re.search(r'[a-z]', password))
    tiene_mayuscula = bool(re.search(r'[A-Z]', password))
    tiene_numero = bool(re.search(r'[0-9]', password))
    tiene_simbolo = bool(re.search(r'[^a-zA-Z0-9]', password))

    if not tiene_mayuscula:
        problemas.append("No tiene letras mayúsculas")
        sugerencias.append("Agrega al menos una letra mayúscula")

    if not tiene_minuscula:
        problemas.append("No tiene letras minúsculas")
        sugerencias.append("Agrega al menos una letra minúscula")

    if not tiene_numero:
        problemas.append("No tiene números")
        sugerencias.append("Agrega al menos un número")

    if not tiene_simbolo:
        problemas.append("No tiene símbolos especiales")
        sugerencias.append("Agrega símbolos como !@#$%&*")

    es_comun = password.lower() in CONTRASENAS_COMUNES

    if es_comun:
        problemas.append("Está entre las contraseñas más usadas del mundo")
        sugerencias.append("Evita contraseñas genéricas o predecibles")

    tiene_secuencia = detectar_secuencias(password)
    if tiene_secuencia:
        problemas.append("Contiene secuencias predecibles (abc, 123, qwerty)")
        sugerencias.append("Evita secuencias de teclado o numéricas")

    tiene_repeticion = detectar_repeticiones(password)
    if tiene_repeticion:
        problemas.append("Contiene caracteres repetidos consecutivos")
        sugerencias.append("Evita repetir el mismo carácter varias veces seguidas")

    entropia = calcular_entropia(password)
    tiempo_crackeo = calcular_tiempo_crackeo(entropia)

    veces_filtrada = verificar_filtracion_hibp(password)

    if veces_filtrada is None:
        alerta_filtracion = "No se pudo verificar (sin conexión a la API)"
    elif veces_filtrada > 0:
        alerta_filtracion = f"Encontrada en {veces_filtrada:,} filtraciones de datos conocidas"
        problemas.append("Esta contraseña ya fue filtrada públicamente")
        sugerencias.append("Cámbiala de inmediato si la usas en algún servicio")
    else:
        alerta_filtracion = "No aparece en filtraciones conocidas"

    puntaje = min(100, round((entropia / 80) * 100))

    if es_comun or (veces_filtrada and veces_filtrada > 0):
        puntaje = min(puntaje, 15)

    if tiene_secuencia or tiene_repeticion:
        puntaje = max(0, puntaje - 15)

    if puntaje < 20:
        categoria = "Muy débil"
    elif puntaje < 40:
        categoria = "Débil"
    elif puntaje < 60:
        categoria = "Aceptable"
    elif puntaje < 80:
        categoria = "Fuerte"
    else:
        categoria = "Muy fuerte"

    return {
        "puntaje": puntaje,
        "categoria": categoria,
        "entropia_bits": entropia,
        "tiempo_estimado_crackeo": tiempo_crackeo,
        "longitud": longitud,
        "alerta_filtracion": alerta_filtracion,
        "problemas": problemas,
        "sugerencias": sugerencias if sugerencias else ["¡Tu contraseña luce sólida!"]
    }