let mascotaAEliminar = null;//guarda el id de la mascota cuando se apreta eliminar
let razaAEliminar = "";//guarda el nombre de la raza que se muestra en el modal
//mostrar modal cuando apretan "eliminar"
document.addEventListener("DOMContentLoaded", function() {//espera que cargue el html
   document.querySelectorAll(".btn-eliminar").forEach(btn => {//recorre cada boton que se llame .btn-eliminar
       btn.addEventListener("click", () => {
           mascotaAEliminar = btn.dataset.id;//guarda id de la mascota
           razaAEliminar = btn.dataset.raza;//guarda la raza


           //ponemos la raza en el texto del modal
           document.getElementById("nombreMascotaEliminar").innerText = razaAEliminar;


           //mostrar modal
           let modal = new bootstrap.Modal(document.getElementById("modalEliminar"));
           modal.show();
       });
   });
});
//cuando el usuario confirma en el modal
document.getElementById("btnConfirmarEliminar").addEventListener("click", function() {
   eliminarMascota(mascotaAEliminar);//se elimina la mascota
   bootstrap.Modal.getInstance(document.getElementById("modalEliminar")).hide();//oculta el modal
});


//funcion ajax para eliminar mascota
function eliminarMascota(id){
   let formData= new FormData();//construye el cuespo del post como si fuera un formulario real
   formData.append("id", id); //agregamos el id de la mascota
  
   //enviamos la peticion ajax a la vista
   fetch("/eliminar_mascota_ajax/",
       {
           method:"POST",
           body:formData,
           headers:{
               "X-CSRFToken": getCookie("csrftoken")//token para que django permita post
           }
       }
   )
   .then(response=>response.json())//convertimos la respuesta http en un objeto json
   .then(data=>{//manejamos la respuesta
       if (data.status==="ok"){
           alert(data.mensaje);
           //eliminamos la mascota de la lista sin recargar
           document.getElementById("fila-"+ id).remove()
       }else{
           alert("Error: "+ data.mensaje);
       }
   });
}


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



