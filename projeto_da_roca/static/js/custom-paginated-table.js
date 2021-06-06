$(function() {
    // Function that displays rows for a specific page.
    function displayRows(index) {
        var start = (index - 1) * rowsPerPage;
        var end = start + rowsPerPage;
        
        // Hide all rows.
        rows.hide();
        
        // Show the proper rows for this page.
        rows.slice(start, end).show();
    }

    const rowsPerPage = 5;
    const rows = $(".custom_table tbody tr");
    const rowsCount = rows.length;
    const pageCount = Math.ceil(rowsCount / rowsPerPage); // avoid decimals
    const numbers = $("#numbers");
    
    // Generate the pagination.
    for (var i = 0; i < pageCount; i++) {
        numbers.append("<li><a href=\"#\">" + (i+1) + "</a></li>");
    }
        
    // Mark the first page link as active.
    $("#numbers li:first-child a").addClass("active");

    // Display the first set of rows.
    displayRows(1);
    
    // On pagination click.
    $("#numbers li a").click(function(e) {
        var $this = $(this);
        
        e.preventDefault();
        
        // Remove the active class from the links.
        $("#numbers li a").removeClass("active");
        
        // Add the active class to the current link.
        $this.addClass("active");
        
        // Show the rows corresponding to the clicked page ID.
        displayRows($this.text());
    });

    $("#custom_table-search").on("keyup", function(event) {
        var filter = $(event.target)[0].value.toUpperCase();
        if (filter) {
            var tr = document.querySelector(".custom_table tbody").getElementsByTagName("tr");

            // Loop through all table rows, and hide those who don"t match the search query
            for (var i = 0; i < tr.length; i++) {
                const tdNome = tr[i].getElementsByTagName("td")[1];
                const tdEmail = tr[i].getElementsByTagName("td")[2];
                if (tdNome || tdEmail) {
                    const txtValueNome = tdNome.textContent || tdNome.innerText;
                    const txtValueEmail = tdEmail.textContent || tdEmail.innerText;
                    if (txtValueNome.toUpperCase().indexOf(filter) > -1 ||
                        txtValueEmail.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }
            }
        } else {
            displayRows(1);
        }
    });
});