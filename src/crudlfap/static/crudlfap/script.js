$('body').on('click', '[data-target="modal"]', function(e) {
    e.preventDefault();
    $('#modal .modal-dialog').load(
        $(this).attr('href'),
        function() {
            $('#modal').modal();
        }
    );
});
