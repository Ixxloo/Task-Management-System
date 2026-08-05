document.addEventListener('DOMContentLoaded', function () {

    function getCsrfToken() {
        var csrfInput = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }

    // ===================================================================
    // 1. Live search / filter / pagination — all update the table via
    //    AJAX, without ever reloading the page.
    // ===================================================================

    var filterForm = document.getElementById('filter-form');
    var searchInput = document.getElementById('search-input');
    var statusSelect = document.getElementById('status');
    var tableContainer = document.getElementById('task-table-container');
    var searchTimer = null; // holds the pending "wait a bit, then search" timer

    if (filterForm && tableContainer) {
        var listUrl = filterForm.dataset.listUrl; // e.g. "/"

        // Reads whatever is currently in the search box + status dropdown
        // and builds a query string out of it, e.g. "q=test&status=P"
        function buildParams() {
            var params = new URLSearchParams();
            var q = searchInput.value.trim();
            var status = statusSelect.value;
            if (q) params.set('q', q);
            if (status) params.set('status', status);
            return params;
        }

        // Fetches the table fragment for the given query string and
        // swaps it into the page. Also updates the address bar so the
        // Back button and page refresh still behave correctly.
        function loadTasks(params) {
            var url = listUrl + '?' + params.toString();

            fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(function (response) { return response.text(); })
            .then(function (html) {
                tableContainer.innerHTML = html;
                window.history.pushState({}, '', url);
                refreshClearButton(params);
            })
            .catch(function (error) {
                console.error('Failed to load tasks:', error);
            });
        }

        // Shows/hides the "Clear" link depending on whether any filter is active
        function refreshClearButton(params) {
            var existing = document.getElementById('clear-filters');
            var hasFilter = params.get('q') || params.get('status');

            if (hasFilter && !existing) {
                var link = document.createElement('a');
                link.href = listUrl;
                link.className = 'btn-clear';
                link.id = 'clear-filters';
                link.textContent = 'Clear';
                filterForm.appendChild(link);
            } else if (!hasFilter && existing) {
                existing.remove();
            }
        }

        // --- Live search: wait 400ms after the user stops typing, then search ---
        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(function () {
                loadTasks(buildParams());
            }, 400);
        });

        // --- Status dropdown: search immediately when changed ---
        statusSelect.addEventListener('change', function () {
            clearTimeout(searchTimer);
            loadTasks(buildParams());
        });

        // --- Search button / Enter key: search immediately, skip the reload ---
        filterForm.addEventListener('submit', function (event) {
            event.preventDefault();
            clearTimeout(searchTimer);
            loadTasks(buildParams());
        });

        // --- Clear button + pagination links: event delegation, since these
        //     elements get replaced every time the table refreshes ---
        document.addEventListener('click', function (event) {
            var clearBtn = event.target.closest('#clear-filters');
            if (clearBtn) {
                event.preventDefault();
                searchInput.value = '';
                statusSelect.value = '';
                loadTasks(new URLSearchParams());
                return;
            }

            var pageLink = event.target.closest('.js-page-link');
            if (pageLink) {
                event.preventDefault();
                var linkUrl = new URL(pageLink.href, window.location.origin);
                loadTasks(linkUrl.searchParams);
            }
        });
    }

    // ===================================================================
    // 2. Toggle task completed — checkbox AJAX (unchanged from before)
    // ===================================================================

    document.addEventListener('change', function (event) {
        var checkbox = event.target.closest('.js-toggle-complete');
        if (!checkbox) {
            return;
        }

        var url = checkbox.dataset.url;
        var pk = checkbox.dataset.pk;
        var isChecked = checkbox.checked;

        var formData = new FormData();
        formData.append('completed', isChecked ? 'true' : 'false');

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
            checkbox.checked = !isChecked;
        })
        .finally(function () {
            checkbox.disabled = false;
        });
    });

});