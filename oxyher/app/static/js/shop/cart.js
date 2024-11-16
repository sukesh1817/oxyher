
$(document).ready(function () {

    if ($("#t").val() > 0 && $("#t").val() != undefined) {
        if ($("#t").val() == 1) {
            $("#tot").html($("#t").val() + " Item")
            $("#i_tot").html(" Item - " + $("#t").val())
        } else {
            $("#tot").html($("#t").val() + " Items")
            $("#i_tot").html(" Items - " + $("#t").val())
        }
    }


    // Handle quantity changes
    $('[id^="decrease-quantity-"], [id^="increase-quantity-"]').click(function () {
        const index = this.id.split('-').pop(); // Extracts the index from the button ID
        let quantityDisplay = $('#quantity-display-' + index);
        let quantity = parseInt(quantityDisplay.val());
        var p_id = $(this).data('id');


        if ($(this).hasClass('decrease-quantity')) {
            if (quantity > 1) {
                quantity--;
                quantityDisplay.val(quantity);
            }
        } else if ($(this).hasClass('increase-quantity')) {
            quantity++;
            quantityDisplay.val(quantity);

        }

        $.ajax({
            url: 'https://api.oxyher.com/c/shop/cart/update_cart/',
            type: 'POST',
            contentType: 'application/json', // Make sure this is included
            data: JSON.stringify({ p_id: p_id, q: quantity }),
            xhrFields: {
                withCredentials: true // Include cookies in cross-origin requests
            },
            success: function (response) {
                // alert(response.message);
            },
            error: function (xhr) {
                // alert(xhr.responseJSON ? xhr.responseJSON.error : 'An error occurred'); // Added check for responseJSON
            }
        });
    });

    // Handle delete button click
    // $('.btn-danger').click(function () {
    //     const productRow = $(this).closest('.row.border-bottom');
    //     var p_id = $(this).data('id');
    //     productRow.fadeOut(300, function () {
    //         $(this).remove();
    //         $.ajax({
    //             url: 'https://api.oxyher.com/c/shop/cart/update_cart/',
    //             type: 'POST',
    //             contentType: 'application/json', 
    //             data: JSON.stringify({ rem_id: p_id }),
    //             xhrFields: {
    //                 withCredentials: true 
    //             },
    //             success: function (response) {
    //             },
    //             error: function (xhr) {
    //             }
    //         });
    //     });
    // });

    $('.l').on('input', function () {
        if ($(this).val() < 1) {
            $(this).val(1);
        } else {
            var p_id = $(this).data('id');
            var quantity = $(this).val();
        }
        $.ajax({
            url: 'https://api.oxyher.com/c/shop/cart/update_cart/',
            type: 'POST',
            contentType: 'application/json', // Make sure this is included
            data: JSON.stringify({ p_id: p_id, q: quantity }),
            xhrFields: {
                withCredentials: true // Include cookies in cross-origin requests
            },
            success: function (response) {
                // alert(response.message);
            },
            error: function (xhr) {
                // alert(xhr.responseJSON ? xhr.responseJSON.error : 'An error occurred'); // Added check for responseJSON
            }
        });
    });

    // Event listener for opening the delete dialog
    $('.btn-danger').on('click', function () {
        const $main = $(this).closest('.main');
        const displayName = $main.find('h5').text();
        const productUrl = $main.find('img').attr('src');
        const productId = $(this).data('id');

        // Set product information in the dialog
        $("#p_nam").html(displayName);
        $("#dig_img").attr('src', productUrl);
        $("#del_p").val(productId);

        // Show the dialog
        $('#dialog')[0].showModal();
    });

    // Event listener for closing the dialog (No button)
    $('#no_ew').on('click', function () {
        $('#dialog')[0].close();
    });

    // Event listener for confirming deletion (Yes button)
    $('#yes_jnd').on('click', function () {
        const productId = $("#del_p").val();
        const $productRow = $("#" + productId);

        // Optionally, add loading state to Yes button
        $(this).prop('disabled', true).text('Deleting...');

        // Animate fade out of product row, then send AJAX request
        $productRow.fadeOut(300, function () {
            $.ajax({
                url: 'https://api.oxyher.com/c/shop/cart/update_cart/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ rem_id: productId }),
                xhrFields: {
                    withCredentials: true
                },
                success: function (response) {
                    window.location.reload();
                    // Optionally, show success feedback to the user
                },
                error: function (xhr) {
                    // Error handling: re-enable Yes button and alert user

                    $('#yes_jnd').prop('disabled', false).text('Yes');
                },
                complete: function () {
                    // Always close the dialog and re-enable the button
                    $('#dialog')[0].close();
                    $('#yes_jnd').prop('disabled', false).text('Yes');
                }
            });

            // Remove the product row from DOM after fade out
            $productRow.remove();
        });
    });


});