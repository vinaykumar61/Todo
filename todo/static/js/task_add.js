function addNewTask() {
    console.log("Inside addNewTask")
    let title = $("#title").val();
    let description = $("#description").val();
    let due_date = $("#due_date").val();
    let status = $("#status option:selected").val();
    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

    if (!title || !description || !due_date || !status) {
        Swal.fire('Error', 'Please fill all fields', 'error');
        return;
    }

    let data = {
        title: title,
        description: description,
        due_date: due_date,
        status: status,
        csrfmiddlewaretoken: csrf_token
    };

    $.ajax({
        type: "POST",
        url: "/api_create_task/",
        data: data,
        success: function (response) {
            console.log("11111111111");
            
            Swal.fire("Success", "New Task Added Successfully", "success")
                .then(() => window.location.href = "/");

            // optional: clear form
            $("#title").val("");
            $("#description").val("");
            $("#status").val("");
            $("#due_date").val("");
        },
        error: function () {
            console.log("222222222222222");
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Something went wrong!",
            });
        }
    });
}