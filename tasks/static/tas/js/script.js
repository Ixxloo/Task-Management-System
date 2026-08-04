// ---------------------------------------------------------------------
// Toggle Task Completed — via AJAX (no page reload)
// ---------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {

    function getCsrfToken() {
        var csrfInput = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }

    // Event delegation on 'change' (checkboxes fire 'change', not 'click', when toggled)
    document.addEventListener('change', function (event) {
        var checkbox = event.target.closest('.js-toggle-complete');
        if (!checkbox) {
            return; // change event came from something else, ignore it
        }

        var url = checkbox.dataset.url;
        var pk = checkbox.dataset.pk;
        var isChecked = checkbox.checked; // true if the box was just checked, false if unchecked

        var formData = new FormData();
        formData.append('completed', isChecked ? 'true' : 'false');

        // Disable while the request is in flight, so rapid double-clicks can't
        // fire two overlapping requests for the same task
        checkbox.disabled = true;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken(),
            },
            body: formData,
        })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Request failed with status ' + response.status);
            }
            return response.json();
        })
        .then(function (data) {
            if (!data.success) {
                return;
            }

            var statusCell = document.getElementById('status-cell-' + pk);
            var row = document.getElementById('task-row-' + pk);

            if (statusCell) {
                var pillClass = data.status_code === 'C' ? 'status-completed' : 'status-pending';
                statusCell.innerHTML =
                    '<span class="status-pill ' + pillClass + '">' + data.status_label + '</span>';
            }

            if (row) {
                row.classList.toggle('completed', data.status_code === 'C');
            }
        })
        .catch(function (error) {
            console.error('Failed to update task status:', error);
            alert('Something went wrong — please try again.');
            checkbox.checked = !isChecked; // revert the visual checkbox state since the save failed
        })
        .finally(function () {
            checkbox.disabled = false;
        });
    });

});