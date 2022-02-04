$(document).ready(function (e) {
    $('#upload').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles').files.length;

        if (ins < 1) {
            $('#msg').html('<span style="color:red">ທ່ານຕ້ອງເລຶອກໄຟຣຕ້ອງການກວດສອບ</span>');
            return;
        }

        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles').files[x]);
        }

        $.ajax({
            url: '/uploadfile', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            beforeSend: function () {
                $("#remove").html('<img src="/static/default/loading.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">')
            },
            success: function (data) {
                $("#remove").html(data.result)
                //document.getElementById("done").style.display = 'block';

            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            },
            complete: function () {
                $.ajax({
                    url: '/predictdata',
                    beforeSend: function () {
                        $("#presult").html('<img src="/static/default/result.gif" class="rounded mx-auto d-block img-thumbnail img-fluid">')
                    },
                    success: function (data) {
                        $("#presult").html(data.result)
                        document.getElementById("download_csv").style.display = 'inline-block';
                    },
                });
            }
        });
        return false;
    });

    $('#upload_train').on('click', function () {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles').files.length;
        if (ins < 1) {
            $('#msg').html('<span style="color:red">ທ່ານຕ້ອງເລຶອກໄຟຣຕ້ອງການຝຶກແມ່ແບບ</span>');
            return;
        }

        for (var x = 0; x < ins; x++) {
            form_data.append("files[]", document.getElementById('multiFiles').files[x]);
        }

        $.ajax({
            url: '/uploadfiletrain', // point to server-side URL
            dataType: 'json', // what to expect back from server
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'post',
            beforeSend: function () {
                $("#remove").html('<div align="center"><img src="/static/default/train.gif" style="width: 500px"></div>')
            },
            success: function (data) {
                $("#remove").html(data.result)
                //document.getElementById("done").style.display = 'block';
            },
            error: function (response) {
                $('#msg').html(response.message); // display error response
            },
            complete: function () {
                $("#remove").html('<div align="center"><img src="/static/default/train.gif" style="width: 500px"></div>')

                console.log("Hello");
                setTimeout(() => {
                    console.log("World!");
                    $.ajax({
                        url: '/traindata',
                        success: function (data) {
                            $("#remove").html(data.result)
                        },
                    });
                }, 6000);

            }
        });
        return false;
    });

});