const itemsPerPage = 5;
    const rows = Array.from(document.querySelectorAll("tbody > tr"));
    const serialNoCells = Array.from(document.querySelectorAll("tbody > tr > td.serial-no"));

    let currentPage = 0;

    function showPage(page) {
        const startIndex = page * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const serialNumberStart = page * itemsPerPage + 1;
        const serialNumberEnd = (page + 1) * itemsPerPage;

        // Update serial numbers and hide/show rows
        rows.forEach((row, index) => {
            // Update the Serial No column in the row
            const serialNumber = serialNumberStart + index;

            serialNoCells[index].textContent = serialNumber;

            // Show the row if it's within the range
            if (index >= startIndex && index < endIndex) {
                row.style.display = "table-row";
            } else {
                row.style.display = "none";
            }
        });

        // Enable or disable the "Previous" and "Next" buttons based on the current page
        const prevButton = document.getElementById("prevButton");
        const nextButton = document.getElementById("nextButton");
        prevButton.disabled = page === 0;
        nextButton.disabled = endIndex >= rows.length;
    }

    // Event listeners for the "Previous" and "Next" buttons
    const prevButton = document.getElementById("prevButton");
    const nextButton = document.getElementById("nextButton");

    prevButton.addEventListener("click", () => {
        if (currentPage > 0) {
            showPage(--currentPage);
        }
    });

    nextButton.addEventListener("click", () => {
        if (currentPage < Math.ceil(rows.length / itemsPerPage) - 1) {
            showPage(++currentPage);
        }
    });

    // Initial page
    showPage(currentPage);