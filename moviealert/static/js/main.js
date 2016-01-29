$(function() {
  $("#txtSearch").autocomplete({
    source: "/get_city/",
    minLength: 3,
  });
});
