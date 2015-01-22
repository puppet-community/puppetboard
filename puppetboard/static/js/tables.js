// Generated by CoffeeScript 1.6.3
(function() {
  var $;

  $ = jQuery;

  $(function() {});

  $('.nodes').tablesorter({
    headers: {
      4: {
        sorter: false
      }
    },
    sortList: [[1, 0]]
  });

  $('.facts').tablesorter({
    sortList: [[0, 0]]
  });

  $('.dashboard').tablesorter({
    headers: {
        2: { sorter: false }
    },
    sortList: [[0, 1]]
  });

  $('.catalog').tablesorter({
    sortList: [[0, 0]]
  })

  $('input.filter-table').parent('div').removeClass('hide');

  $("input.filter-table").on("keyup", function(e) {
    var ev, rex;
    rex = new RegExp($(this).val(), "i");
    $(".searchable tr").hide();
    $(".searchable tr").filter(function() {
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
