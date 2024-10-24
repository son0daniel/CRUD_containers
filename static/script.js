function filterTable(columnIndex) {
    const input = document.querySelectorAll('.filter-input')[columnIndex];
    const filter = input.value.toUpperCase();
    const rows = document.querySelectorAll('#table-row tr');

    rows.forEach(row => {
        const cell = row.getElementsByTagName('td')[columnIndex];
        if (cell) {
            const cellText = cell.textContent.toUpperCase();
            row.style.display = cellText.includes(filter) ? '' : 'none';
        }
    });
}

function sortTable(columnIndex){
    const table = document.getElementById("table");
    const rows = Array.from(table.rows).slice(1);
    const isAscending = table.rows[0].cells[columnIndex].classList.toggle("ascending");

    rows.sort((rowA, rowB) => {
    const textA = rowA.cells[columnIndex].textContent;
    const textB = rowB.cells[columnIndex].textContent;

    if (isAscending) {
        return textA.localeCompare(textB);
    } else {
        return textB.localeCompare(textA);
    }
});

rows.forEach(row => table.tBodies[0].appendChild(row));
}