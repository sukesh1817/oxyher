$(document).ready(function() {
    let timeout;

    $('#search-query').on('input', function() {
        const query = $(this).val();
        
        clearTimeout(timeout); // Clear the previous timeout
        timeout = setTimeout(() => { // Set a new timeout
            if (query.length === 0) {
                $('#search-results').empty(); // Clear results if input is empty
                return;
            }

            $.ajax({
                url: '/products/search',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ query: query }),
                success: function(response) {
                    $('#search-results').empty();
                    if (response.length > 0) {
                        response.forEach(item => {
                            const highlightedName = item.name.replace(new RegExp(query, 'gi'), (match) => `<strong>${match}</strong>`);
                            $('#search-results').append(`<li>${highlightedName}</li>`);
                        });
                    } else {
                        $('#search-results').append('<li class="no-results">No results found</li>');
                    }
                }
            });
        }, 300); // Delay in milliseconds
    });

    $(document).on('click', function(event) {
        // Check if the click is outside the search input or results list
        if (!$(event.target).closest('#search-query, #search-results').length) {
            $('#search-results').hide();  // Hide the results list
        }
    });

    // Show the results when interacting with the search box
    $('#search-query').on('input', function() {
        const query = $(this).val();
        
        if (query.length > 0) {
            $('#search-results').show();  // Show results if input has text
        }
    });
});
