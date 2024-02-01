$(document).ready(function () {
    $('#dev-table').DataTable({        
      'dom': 'Rlfrtip',
      'colReorder': {
          'allowReorder': false
      },
      // 'autoWidth': true,
      "lengthMenu": [ 5, 10, 20, 50, 100,200,500,1000,2000,5000,10000 ],
      "pageLength": 1000,
      "search": {
        "search": ""
      }
    });
  });