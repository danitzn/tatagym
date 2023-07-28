$(document).ready(function() {
    // Función para actualizar la lista de últimas marcaciones
    function actualizarUltimasMarcaciones() {
      $.ajax({
        url: '/obtener_ultimas_marcaciones/',  // URL de la vista que obtiene las últimas marcaciones
        type: 'GET',
        dataType: 'json',
        success: function(data) {
          // Limpiar la lista actual de últimas marcaciones
          $('#ultimas_marcaciones').empty();
  
          // Iterar sobre los datos recibidos y agregar cada marcación a la lista
          for (var i = 0; i < data.length; i++) {
            var marcacion = data[i].fields;
            var listItem = '<li>' + marcacion.fecha + ' - ' + marcacion.cedula + ' - ' + marcacion.tipo + '</li>';
            $('#ultimas_marcaciones').append(listItem);
          }
        },
        error: function(error) {
          console.log('Error al obtener las últimas marcaciones:', error);
        }
      });
    }
  
    // Llamar a la función de actualización al cargar la página
    actualizarUltimasMarcaciones();
  
    // Actualizar la lista cada 10 segundos (10000 milisegundos)
    setInterval(actualizarUltimasMarcaciones, 10000);
  });