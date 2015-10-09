// Generated by CoffeeScript 1.10.0
(function() {
  var $;

  $ = jQuery;

  $(function() {});

  $('input.filter-list').parent('div').removeClass('hide');

  $("input.filter-list").on("keyup", function(e) {
    var ev, rex;
    rex = new RegExp($(this).val(), "i");
    $(".searchable li").hide();
    $(".searchable li").filter(function() {
      return rex.test($(this).text());
    }).show();
    if (e.keyCode === 27) {
      $(e.currentTarget).val("");
      ev = $.Event("keyup");
      ev.keyCode = 13;
      $(e.currentTarget).trigger(ev);
      return e.currentTarget.blur();
    }
  });

}).call(this);
