document.addEventListener('DOMContentLoaded', function () {
  var searchInput = document.querySelector('.search-input');
  var searchForm = document.querySelector('.search-filter-row');
  if (searchInput && searchForm) {
    searchInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') searchForm.submit();
    });
  }
  var sortSelect = document.getElementById('sort-events');
  if (sortSelect) {
    sortSelect.addEventListener('change', function () {
      var url = new URL(window.location.href);
      url.searchParams.set('sort', this.value);
      window.location.href = url.toString();
    });
  }
});
