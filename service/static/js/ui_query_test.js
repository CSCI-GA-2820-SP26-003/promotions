$(function () {
    const API_BASE_URL = "/api/promotions";

    const PROMOTION_TYPE_MAP = {
        "1": "PERCENT_OFF",
        "2": "BUY_N_GET_ONE",
        "3": "FIXED_DISCOUNT",
        "4": "FREE_SHIPPING"
    };

    function update_form_data(res) {
        $("#promotion_promotion_id").val(res.id);
        $("#promotion_name").val(res.name);
        $("#promotion_promotion_type").val(res.promotion_type);
        $("#promotion_value").val(res.value);
        $("#promotion_start_date").val(res.start_date);
        $("#promotion_end_date").val(res.end_date);
        if (res.active == true) {
            $("#promotion_active").val("True");
        } else {
            $("#promotion_active").val("False");
        }
    }

    function clear_form_data() {
        $("#promotion_name").val("");
        $("#promotion_promotion_type").val("");
        $("#promotion_value").val("");
        $("#promotion_start_date").val("");
        $("#promotion_end_date").val("");
        $("#promotion_active").val("");
    }

    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    function do_search(preserve_message) {
        let name = $("#promotion_name").val();
        let promotion_type = $("#promotion_promotion_type").val();
        let value = $("#promotion_value").val();
        let active = $("#promotion_active").val();

        let params = [];
        if (name) { params.push("name=" + encodeURIComponent(name)); }
        if (promotion_type) {
            // Backend expects the enum name (e.g., PERCENT_OFF), not the numeric value
            let type_name = PROMOTION_TYPE_MAP[promotion_type] || promotion_type;
            params.push("promotion_type=" + encodeURIComponent(type_name));
        }
        if (value) { params.push("value=" + encodeURIComponent(value)); }
        if (active) { params.push("active=" + encodeURIComponent(active)); }

        let ajax = $.ajax({
            type: "GET",
            url: `${API_BASE_URL}?${params.join("&")}`,
            contentType: "application/json",
            data: "",
        });
        ajax.done(function (res) {
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">';
            table += "<thead><tr>";
            table += '<th class="col-md-1">ID</th>';
            table += '<th class="col-md-4">Name</th>';
            table += '<th class="col-md-4">Description</th>';
            table += '<th class="col-md-3">Promotion Type</th>';
            table += '<th class="col-md-3">Value</th>';
            table += '<th class="col-md-3">Active</th>';
            table += "</tr></thead><tbody>";
            let firstPromotion = null;
            for (let i = 0; i < res.length; i++) {
                let promotion = res[i];
                table += `<tr id="row_${i}">
                    <td>${promotion.id}</td>
                    <td>${promotion.name}</td>
                    <td>${promotion.description || ""}</td>
                    <td>${promotion.promotion_type}</td>
                    <td>${promotion.value}</td>
                    <td>${promotion.active}</td>
                </tr>`;
                if (i === 0) { firstPromotion = promotion; }
            }
            table += "</tbody></table>";
            $("#search_results").append(table);
            if (firstPromotion) { update_form_data(firstPromotion); }
            // Only update flash message if caller didn't set one to preserve
            if (!preserve_message) {
                flash_message("Success");
            }
        });
        ajax.fail(function (res) {
            flash_message(res.responseJSON?.message || "Search failed");
        });
    }

    $("#create-btn").click(function () {
        try {
            let promotion_type = $("#promotion_promotion_type").val();
            let active = $("#promotion_active").val();
            let data = {
                name: $("#promotion_name").val(),
                promotion_type: Number(promotion_type),
                value: parseInt($("#promotion_value").val()),
                start_date: $("#promotion_start_date").val(),
                end_date: $("#promotion_end_date").val(),
                active: active ? active.toLowerCase() === "true" : undefined,
            };
            let ajax = $.ajax({
                type: "POST",
                url: API_BASE_URL,
                contentType: "application/json",
                data: JSON.stringify(data),
            });
            ajax.done(function (res) {
                $("#search_results").empty();
                let table = '<table class="table table-striped" cellpadding="10">';
                table += '<thead><tr>';
                table += '<th class="col-md-1">ID</th>';
                table += '<th class="col-md-4">Name</th>';
                table += '<th class="col-md-4">Description</th>';
                table += '<th class="col-md-3">Promotion Type</th>';
                table += '<th class="col-md-3">Value</th>';
                table += '<th class="col-md-3">Active</th>';
                table += '</tr></thead><tbody>';
                table += '<tr id="row_0"><td>' + res.id + '</td><td>' + res.name + '</td><td>' + (res.description || "") + '</td><td>' + res.promotion_type + '</td><td>' + res.value + '</td><td>' + res.active + '</td></tr>';
                table += '</tbody></table>';
                $("#search_results").append(table);
                flash_message("Promotion created successfully.");
            });
            ajax.fail(function (res) {
                flash_message("Create failed: " + (res.responseJSON?.message || res.responseText || res.status));
            });
        } catch (err) {
            flash_message("Create error: " + err.message);
        }
    });

    $("#update-btn").click(function () {
        let promotion_id = $("#promotion_promotion_id").val();
        let data = {
            name: $("#promotion_name").val(),
            promotion_type: Number($("#promotion_promotion_type").val()),
            value: Number($("#promotion_value").val()),
            start_date: $("#promotion_start_date").val(),
            end_date: $("#promotion_end_date").val(),
            active: $("#promotion_active").val()
                ? $("#promotion_active").val().toLowerCase() === "true"
                : undefined
        };
        let ajax = $.ajax({
            type: "PUT",
            url: `${API_BASE_URL}/${promotion_id}`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function (res) {
            flash_message(res.responseJSON?.message || "Update failed");
        });
    });

    $("#retrieve-btn").click(function () {
        let promotion_id = $("#promotion_promotion_id").val();
        let ajax = $.ajax({
            type: "GET",
            url: `${API_BASE_URL}/${promotion_id}`,
            contentType: "application/json",
            data: "",
        });
        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function (res) {
            clear_form_data();
            flash_message(res.responseJSON?.message || "Retrieve failed");
        });
    });

    $("#delete-btn").click(function () {
        let promotion_id = $("#promotion_promotion_id").val();
        let ajax = $.ajax({
            type: "DELETE",
            url: `${API_BASE_URL}/${promotion_id}`,
            contentType: "application/json",
            data: "",
        });
        ajax.done(function () {
            clear_form_data();
            flash_message("Promotion deleted successfully.");
        });
        ajax.fail(function () {
            flash_message("Server error!");
        });
    });

    $("#clear-btn").click(function () {
        $("#promotion_promotion_id").val("");
        $("#flash_message").empty();
        $("#search_results").empty();
        clear_form_data();
    });

    $("#search-btn").click(function () {
        do_search();
    });

    $("#activate-btn").click(function () {
        let promotion_id = $("#promotion_promotion_id").val();
        let ajax = $.ajax({
            type: "PUT",
            url: `${API_BASE_URL}/${promotion_id}/activate`,
            contentType: "application/json",
            data: "",
        });
        ajax.done(function (res) {
            update_form_data(res);
            flash_message("Success");
        });
        ajax.fail(function (res) {
            flash_message(res.responseJSON?.message || "Activate failed");
        });
    });
});