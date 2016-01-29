$.curCSS = function (element, attrib, val) {
    $(element).css(attrib, val);
};
$(function() {
  $("#txtSearch").autocomplete({
    source: "/get_city/",
    minLength: 3,
  });
});
