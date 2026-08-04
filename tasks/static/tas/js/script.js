// ---------------------------------------------------------------------
// Mark Task as Completed — via AJAX (no page reload)
// ---------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {

    // Grabs the CSRF token Django put in the hidden form in base.html.
    // Django requires this on every POST request, or it rejects it as 403 Forbidden.
    function getCsrfToken() {
        var csrfInput = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }

    // Event delegation: instead of attaching a click listener to every single
    // "mark complete" button (there could be many, and new ones could appear
    // after pagination), we attach ONE listener to the whole document and
    // check if the clicked element matches what we care about.
    document.addEventListener('click', function (event) {
        var button = event.target.closest('.js-mark-complete');
        if (!button) {
            return; // click was on something else entirely, ignore it
        }

        event.preventDefault(); // stop the browser from following the link's href (no reload)

        var url = button.dataset.url;   // e.g. "/complete/7"
        var pk = button.dataset.pk;     // e.g. "7"

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',   // tells Django this is an AJAX call
                'X-CSRFToken': getCsrfToken(),           // Django's CSRF protection requires this header on POST
            }
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

            // Update the Status cell for this specific row
            var statusCell = document.getElementById('status-cell-' + pk);
            if (statusCell) {
                statusCell.innerHTML =
                    '<span class="status-pill status-completed">' + data.status_label + '</span>';
            }

            // Remove the "mark complete" checkmark button — task is done, no need to show it anymore
            button.remove();
        })
        .catch(function (error) {
            console.error('Failed to mark task complete:', error);
            alert('Something went wrong — please try again.');
        });
    });

});