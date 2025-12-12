document.addEventListener("DOMContentLoaded", function() {

    // -----------------------------
    // ABRIR SEGUIMIENTO
    document.querySelectorAll(".btn-ver-seguimiento").forEach(btn=>{
        btn.addEventListener("click", ()=>{
            let url = btn.dataset.url;

            fetch(url, { headers: {"X-Requested-With": "XMLHttpRequest"} })
                .then(response => response.json())
                .then(data=>{
                    document.getElementById("contenidoSeguimiento").innerHTML = data.html;

                    let modal = new bootstrap.Modal(document.getElementById("modalSeguimiento"));
                    modal.show();
                });
        });
    });
let idAEliminar = null;
let urlAEliminar = null;
let tipoAEliminar = null;

// Captura click en botones eliminar
document.addEventListener("click", function(e) {
    if (e.target.classList.contains("btn-eliminar")) {
        idAEliminar = e.target.dataset.id;
        urlAEliminar = e.target.dataset.url;
        tipoAEliminar = e.target.dataset.tipo; // "vacuna" o "observacion"

        let modal = new bootstrap.Modal(document.getElementById("modalEliminar"));
        modal.show();
    }
});

// Confirmar eliminación
document.getElementById("btnConfirmarEliminar").addEventListener("click", function() {
    eliminarObjeto(idAEliminar, urlAEliminar);
    bootstrap.Modal.getInstance(document.getElementById("modalEliminar")).hide();
});

function eliminarObjeto(id, url){
    let formData = new FormData();
    formData.append("id", id);

    fetch(url, {
        method: "POST",
        body: formData,
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    })
    .then(r => r.json())
    .then(data => {
        if(data.status === "ok"){
            alert(data.mensaje);
            document.getElementById(`${tipoAEliminar}-${id}`)?.remove(); // ahora sí elimina la fila correcta
        } else {
            alert("Error: "+data.mensaje);
        }
    });
}


});
document.addEventListener("click", async function(e) {

    // Cuando aprietan un btn-modificar o btn-crear
    if (e.target.classList.contains("btn-modificar")) {

        let url = e.target.dataset.url;

        let response = await fetch(url);
        let html = await response.text();

        // Pongo el formulario dentro del modal
        document.getElementById("bodyModalFormulario").innerHTML = html;

        // Abro el modal
        let modal = new bootstrap.Modal(document.getElementById("modalFormulario"));
        modal.show();
    }
});
document.addEventListener("click", async function(e) {

    // Si apretan GUARDAR dentro del modal de formulario
    if (e.target.id === "btnGuardarFormulario") {

        let form = document.querySelector("#bodyModalFormulario form");
        if (!form) return;

        let url = form.action;
        let formData = new FormData(form);

        let response = await fetch(url, {
            method: "POST",
            body: formData,
            headers: {"X-CSRFToken": getCookie("csrftoken")}
        });

        let data = await response.json();

        if (data.status === "ok") {
            alert(data.mensaje);
        
            // Cerrar modal primero
            bootstrap.Modal.getInstance(document.getElementById("modalFormulario")).hide();
        
            // Recargar el seguimiento
            let idMascota = formData.get("id"); // asegurate que sea el id de la mascota
            let btn = document.querySelector(`.btn-ver-seguimiento[data-id="${idMascota}"]`);
            if (btn) btn.click();
        }
    }
});

//TOKEN CSRF
//busca una cookie por nombre y devuelve el valor
function getCookie(name){
   let cookieValue=null;
   if(document.cookie && document.cookie!==""){
       const cookies=document.cookie.split(";");//separa las cookies
       for (let i=0; i<cookies.length;i++){//recorremos cada una
           const cookie=cookies[i].trim();//quitamos espacios
           if (cookie.substring(0,name.length +1)===(name+"=")){//comprobamos si empiezan por "name="
               cookieValue=decodeURIComponent(cookie.substring(name.length+1));
               break;//si la encontramos guardamos y salimos
           }
       }
   }
   return cookieValue;//devuelve el valor o null si no la encuentra
}


