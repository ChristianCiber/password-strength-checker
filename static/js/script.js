// ===== Mostrar/ocultar contraseña =====
document.getElementById("toggle-visibility").addEventListener("click", function () {

    let input = document.getElementById("password");

    if (input.type === "password") {
        input.type = "text";
        this.textContent = "🙈";
    } else {
        input.type = "password";
        this.textContent = "👁";
    }

});


function analizar() {

    let password = document.getElementById("password").value;
    let message = document.getElementById("message");
    let resultado = document.getElementById("resultado");

    if (!password) {
        message.innerHTML = "Escribe una contraseña primero.";
        resultado.classList.add("resultado-oculto");
        return;
    }

    message.innerHTML = "Analizando...";
    resultado.classList.add("resultado-oculto");

    fetch("/check", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            password: password
        })

    })

    .then(response => response.json())

    .then(data => {

        if (data.error) {
            message.innerHTML = data.error;
            return;
        }

        message.innerHTML = "";

        mostrarResultado(data);

    })

    .catch(error => {
        message.innerHTML = "Error al analizar la contraseña";
    });

}


function mostrarResultado(data) {

    let resultado = document.getElementById("resultado");

    document.getElementById("puntaje-numero").textContent = data.puntaje;
    document.getElementById("puntaje-categoria").textContent = data.categoria;

    let barra = document.getElementById("barra-relleno");
    barra.style.width = data.puntaje + "%";

    barra.className = "barra-relleno";
    if (data.puntaje < 20) {
        barra.classList.add("nivel-muy-debil");
    } else if (data.puntaje < 40) {
        barra.classList.add("nivel-debil");
    } else if (data.puntaje < 60) {
        barra.classList.add("nivel-aceptable");
    } else if (data.puntaje < 80) {
        barra.classList.add("nivel-fuerte");
    } else {
        barra.classList.add("nivel-muy-fuerte");
    }

    document.getElementById("valor-entropia").textContent = data.entropia_bits + " bits";
    document.getElementById("valor-tiempo").textContent = data.tiempo_estimado_crackeo;
    document.getElementById("valor-longitud").textContent = data.longitud + " caracteres";
    document.getElementById("valor-filtracion").textContent = data.alerta_filtracion;

    let listaProblemas = document.getElementById("lista-problemas");
    let seccionProblemas = document.getElementById("seccion-problemas");

    listaProblemas.innerHTML = "";

    if (data.problemas.length === 0) {
        seccionProblemas.style.display = "none";
    } else {
        seccionProblemas.style.display = "block";
        data.problemas.forEach(problema => {
            listaProblemas.innerHTML += `<li>${problema}</li>`;
        });
    }

    let listaSugerencias = document.getElementById("lista-sugerencias");
    listaSugerencias.innerHTML = "";

    data.sugerencias.forEach(sugerencia => {
        listaSugerencias.innerHTML += `<li>${sugerencia}</li>`;
    });

    resultado.classList.remove("resultado-oculto");

}