/**
 * Sorts an HTML Table
 *
 * @param {HTMLTableElement} table - the table to sort
 * @param {number} column - the index of the column to sort
 * @param {boolean} asc - determines if the sorting will be in ascending or descending
 *
*/

function sortTableByColumn(table, column, asc = true) {
    console.log("Sorting table...");

    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll('tr'));

    // Sort each row
    const sortedRows = rows.sort((a, b) => {
      const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
      const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();

      if (column === 0) { // Assuming column 0 corresponds to the date
        const aColDate = new Date(aColText);
        const bColDate = new Date(bColText);

        return aColDate > bColDate ? 1 * dirModifier : -1 * dirModifier;
      } else if (column === 2) { // Assuming column 2 corresponds to the category
        const aColTextLower = aColText.toLowerCase();
        const bColTextLower = bColText.toLowerCase();

        return aColTextLower.localeCompare(bColTextLower) * dirModifier;
    } else if (column == 3) { // For other columns, assuming they are numeric
        const aColValue = parseFloat(aColText);
        const bColValue = parseFloat(bColText);

        return aColValue > bColValue ? 1 * dirModifier : -1 * dirModifier;
      }
    });

    // Remove all existing TRs from the table
    while (tBody.firstChild) {
      tBody.removeChild(tBody.firstChild);
    }

    // Re-add the newly sorted rows
    tBody.append(...sortedRows);

    // Remember how the column is currently sorted
    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    const thToToggle = table.querySelector(`th:nth-child(${column + 1})`);
    thToToggle.classList.toggle("th-sort-asc", asc);
    thToToggle.classList.toggle("th-sort-desc", !asc);

    console.log("Table sorted!");
  }

  // Applying to every column header
  document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM content loaded!");

    document.querySelectorAll(".table-sortable th").forEach(headerCell => {
      headerCell.addEventListener("click", () => {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.from(headerCell.parentElement.children).indexOf(headerCell);

        // Check if the clicked column is one of the allowed columns
        const isSortableColumn = [0, 2, 3].includes(headerIndex);

        if (isSortableColumn) {
          // Get the current sorting direction from the class
          const currentIsAscending = headerCell.classList.contains("th-sort-asc");

          // Toggle the sorting direction
          const newIsAscending = !currentIsAscending;

          // Sort the table
          sortTableByColumn(tableElement, headerIndex, newIsAscending);

          // Update the class based on the new sorting direction
          tableElement.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
          headerCell.classList.toggle("th-sort-asc", newIsAscending);
          headerCell.classList.toggle("th-sort-desc", !newIsAscending);
        }
      });
    });
  });
