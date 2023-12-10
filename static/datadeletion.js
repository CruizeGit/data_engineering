const checkboxes = document.querySelectorAll('.checkbox');
const deleteBtn = document.getElementById('delete-btn');

deleteBtn.addEventListener('click', () => {
  const selectedIds = [];

  checkboxes.forEach(checkbox => {
    if (checkbox.checked) {
      const id = parseInt(checkbox.dataset.id);
      selectedIds.push(id);
    }
  });

  if (selectedIds.length > 0) {
    //AJAX POST request through FETCH API to delete selected records
    const deleteUrl = '/delete_budgets';
    const data = { 'selected_ids': selectedIds };

    fetch(deleteUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
      if (responseData.success) {
        // Update the table with deleted records
        updateTable(selectedIds);
      } else {
        console.error('Error deleting records:', responseData.error);
      }
    })
    .catch(error => {
      console.error('Error sending AJAX request:', error);
    });
  } else {
    // No records selected for deletion
    alert('Please select records to delete');
  }
});

function updateTable(selectedIds) {
    // Remove rows corresponding to deleted records
    console.log("Code goes into this")
    const tableRows = document.querySelectorAll('tbody tr');

    for (let i = 0; i < tableRows.length; i++) {
      const row = tableRows[i];
      const id = parseInt(row.querySelector('.checkbox').dataset.id); // Corrected line
      console.log("Code goes into this")

      if (selectedIds.includes(id)) {
        row.parentNode.removeChild(row);
        console.log("Code goes into this")
      }
    }
  }

