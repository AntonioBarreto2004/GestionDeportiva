
function mostrarVistaPrevia(input) {
    var fileInput = input;
    var imagenPreview = $('#imagen-preview');
    var imagenPreviewImg = $('#imagen-preview-img');

    if (fileInput.files && fileInput.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            imagenPreviewImg.attr('src', e.target.result);
            imagenPreview.show();
        };
        reader.readAsDataURL(fileInput.files[0]);
    } else {
        imagenPreview.hide();
    }
}
