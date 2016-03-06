(function() {
  Dashing.gridsterLayout = function(positions) {
    var index, widget, widgets, _i, _len, _results;
    Dashing.customGridsterLayout = true;
    positions = positions.replace(/^"|"$/g, '');
    positions = $.parseJSON(positions);
    widgets = $("[data-row^=]");
    _results = [];
    for (index = _i = 0, _len = widgets.length; _i < _len; index = ++_i) {
      widget = widgets[index];
      $(widget).attr('data-row', positions[index].row);
      _results.push($(widget).attr('data-col', positions[index].col));
    }
    return _results;
  };

  Dashing.getWidgetPositions = function() {
    return $(".gridster ul:first").gridster().data('gridster').serialize();
  };

  Dashing.showGridsterInstructions = function() {
    var newWidgetPositions;
    newWidgetPositions = Dashing.getWidgetPositions();
    if (JSON.stringify(newWidgetPositions) !== JSON.stringify(Dashing.currentWidgetPositions)) {
      Dashing.currentWidgetPositions = newWidgetPositions;
      $('#save-gridster').slideDown();
      return $('#gridster-code').text("<script type='text/javascript'>\n $(function() {\n \ \ Dashing.gridsterLayout('" + (JSON.stringify(Dashing.currentWidgetPositions)) + "')\n });\n </script>");
    }
  };

  $(function() {
    $('#save-gridster').leanModal();
    return $('#save-gridster').click(function() {
      return $('#save-gridster').slideUp();
    });
  });

}).call(this);
