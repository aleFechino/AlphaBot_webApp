/*
avanti=document.getElementById("btn_avanti")
indietro=document.getElementById("btn_indietro")
stop=document.getElementById("btn_stop")
destra=document.getElementById("btn_destra")
sinistra=document.getElementById("btn_sinistra")

avanti.addEventListener("click", ()=>{
    fetch("/control", {
        method:"POST",
        body:"AVANTISSIMO="
    })
});
*/

// control.js
const avanti = document.getElementById("btn_avanti");
const indietro = document.getElementById("btn_indietro");
const stop = document.getElementById("btn_stop");
const destra = document.getElementById("btn_destra");
const sinistra = document.getElementById("btn_sinistra");

// Funzione per inviare comandi al server
function inviaComando(comando) {
    const formData = new FormData();
    formData.append(comando, "");
    
    fetch("/control", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .catch(error => console.error('Errore:', error));
}

// Gestione eventi tastiera
let tastiPremuti = new Set();

document.addEventListener("keydown", (event) => {
    // Evita la ripetizione se il tasto è già premuto
    if (tastiPremuti.has(event.key)) {
        return;
    }
    tastiPremuti.add(event.key);
    
    switch(event.key) {
        case "ArrowUp":
        case "w":
        case "W":
            event.preventDefault();
            avanti.classList.add("active");
            inviaComando("Avanti");
            break;
        case "ArrowDown":
        case "s":
        case "S":
            event.preventDefault();
            indietro.classList.add("active");
            inviaComando("Indietro");
            break;
        case "ArrowLeft":
        case "a":
        case "A":
            event.preventDefault();
            sinistra.classList.add("active");
            inviaComando("Sinistra");
            break;
        case "ArrowRight":
        case "d":
        case "D":
            event.preventDefault();
            destra.classList.add("active");
            inviaComando("Destra");
            break;
        case " ":
        case "Spacebar":
            event.preventDefault();
            stop.classList.add("active");
            inviaComando("Stop");
            break;
    }
});

document.addEventListener("keyup", (event) => {
    tastiPremuti.delete(event.key);
    
    // Rimuovi lo stile "active" dai bottoni
    switch(event.key) {
        case "ArrowUp":
        case "w":
        case "W":
            avanti.classList.remove("active");
            inviaComando("Stop");
            break;
        case "ArrowDown":
        case "s":
        case "S":
            indietro.classList.remove("active");
            inviaComando("Stop");
            break;
        case "ArrowLeft":
        case "a":
        case "A":
            sinistra.classList.remove("active");
            inviaComando("Stop");
            break;
        case "ArrowRight":
        case "d":
        case "D":
            destra.classList.remove("active");
            inviaComando("Stop");
            break;
        case " ":
        case "Spacebar":
            stop.classList.remove("active");
            break;
    }
});

// Aggiungi feedback visivo per i click dei bottoni
avanti.addEventListener("click", (e) => {
    e.preventDefault();
    inviaComando("Avanti");
});

indietro.addEventListener("click", (e) => {
    e.preventDefault();
    inviaComando("Indietro");
});

sinistra.addEventListener("click", (e) => {
    e.preventDefault();
    inviaComando("Sinistra");
});

destra.addEventListener("click", (e) => {
    e.preventDefault();
    inviaComando("Destra");
});

stop.addEventListener("click", (e) => {
    e.preventDefault();
    inviaComando("Stop");
});