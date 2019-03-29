

$("#upload").fileinput({
    language: 'zh',
    allowedFileExtensions: ['jpg','gif','png','jpeg'],
    uploadUrl: 'http://127.0.0.1:5000/hello/upload/',
    uploadAsync: true,
    browseClass: "btn btn-primary",
    enctype: 'multipart/form-data',
    maxFileCount: 1
})

$("#upload").on("fileuploaded",
    function (event,data,previewId,index) {
        alert(data);

    }
    )