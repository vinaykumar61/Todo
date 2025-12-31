let alliedTable = null;

$(document).ready(function () {

    // Destroy old instance (important)
    if ($.fn.DataTable.isDataTable("#tableAllied")) {
        alliedTable.clear().destroy();
    }

    alliedTable = $("#tableAllied").DataTable({
        processing: true,
        serverSide: true,
        searching: true,
        ordering: false,     // sorting off (simple)
        responsive: true,
        pageLength: 5,
        lengthMenu: [[5, 10, 25, 50], [5, 10, 25, 50]],

        ajax: {
            url: "/api_get_tasks/",
            type: "GET",
            data: function (d) {
                // optional: extra filters
                d.search_value = d.search.value;
            }
        },

        columns: [
            /* 1. TITLE */
            { data: "title" },

            /* 1. Description */
            { data: "description" },

            /* 2. DUE DATE */
            { data: "due_date" },

            /* 3. STATUS */
            {
                data: "status",
                render: function (data) {
                    let color =
                        data === "Completed" ? "green" :
                        data === "In Progress" ? "orange" : "red";

                    return `<span style="color:${color}">${data}</span>`;
                }
            },

            /* 4. ACTION BUTTONS (YOUR CONTROL) */
            {
                data: null,
                orderable: false,
                searchable: false,
                render: function (row) {
                    return `
                        <button class="btn btn-edit"
                            onclick="openEditModal(${row.id})" style="background: green; color: white;">
                            Edit
                        </button>

                        <button class="btn btn-delete"
                            onclick="deleteTask(${row.id})" style="background: red; color: white;">
                            Delete
                        </button>
                    `;
                }
            }
        ],

        language: {
            processing: "Loading data, please wait..."
        }
    });

    // ✅ Add bootstrap margin
    $("#tableAllied_wrapper").addClass("m-2");

});

function deleteTask(id) {
    Swal.fire({
        title: 'Delete?',
        text: "Are you sure, you want to Delete?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes'
    }).then(result => {
        if (result.isConfirmed) {

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax({
                type: "POST",
                url: `/api_delete_task/${id}/`,
                data: {
                    csrfmiddlewaretoken: csrf_token
                },
                success: function () {
                    Swal.fire('Deleted!', 'Task removed successfully', 'success');
                    loadTasks(currentPage);
                },
                error: function () {
                    Swal.fire('Error', 'Delete failed', 'error');
                }
            });
        }
    });
}

function openEditModal(id) {

    $.get(`/api_get_task/${id}/`, function (res) {
        showModal();
        console.log("res",res.task);
        
        let task = res.task;

        $("#edit_id").val(task.id);
        $("#edit_title").val(task.title);
        $("#edit_description").val(task.description);
        $("#edit_due_date").val(task.due_date);
        $("#edit_status").val(task.status);

    });
}

function updateTask() {

    let id = $("#edit_id").val();
    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

    let data = {
        title: $("#edit_title").val(),
        description: $("#edit_description").val(),
        due_date: $("#edit_due_date").val(),
        status: $("#edit_status").val(),
        csrfmiddlewaretoken: csrf_token
    };

    if (!data) {
        Swal.fire('Error', 'Please fill all fields', 'error');
        return;
    }

    $.post(`/api_update_task/${id}/`, data, function () {

        Swal.fire("Updated", "Task Updated Successfully", "success");

        closeModal();
        loadTasks();
    });
}

function showModal() {
    $("#editModal").show();
}

function closeModal() {
    $("#editModal").hide();
}
