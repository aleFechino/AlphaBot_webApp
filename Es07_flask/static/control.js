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