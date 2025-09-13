$(document).ready(function() {
    $('.toggle-column').change(function() {
        const columnIndex = $(this).data('column'); // column index 1-based
        const isChecked = $(this).is(':checked');

        // Toggle header
        $('table thead th:nth-child(' + columnIndex + ')').toggle(isChecked);

        // Toggle body cells
        $('table tbody tr').each(function() {
            $(this).find('td:nth-child(' + columnIndex + ')').toggle(isChecked);
        });
    });
});


