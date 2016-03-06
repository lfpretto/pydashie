(function() {
    console.log("Yeah! The dashboard has started!");
    Dashing.updateLayout = function() {
        var newData;
        newData = JSON.stringify(Dashing.getWidgetPositions());
        if (newData !== Dashing.currentWidgetPositions) {
            Dashing.currentWidgetPositions = newData;
            console.log(newData);
            $.ajax({
                url: '/update',
                type: 'POST',
                dataType: "json",
                contentType: 'application/json',
                data: newData, // or $('#myform').serializeArray()
                //success: function() { alert('POST completed'); }
            });
        }
    }

  Dashing.on('ready', function() {
    var contentWidth;
    Dashing.widget_margins || (Dashing.widget_margins = [3, 3]);
    Dashing.widget_base_dimensions || (Dashing.widget_base_dimensions = [300, 320]);
    Dashing.numColumns || (Dashing.numColumns = 4);
    contentWidth = (Dashing.widget_base_dimensions[0] + (Dashing.widget_margins[0] * 3)) * Dashing.numColumns;
    return Batman.setImmediate(function() {
      $('.gridster').width(contentWidth);
      return $('.gridster ul:first').gridster({
        widget_margins: Dashing.widget_margins,
        widget_base_dimensions: Dashing.widget_base_dimensions,
        avoid_overlapped_widgets: !Dashing.customGridsterLayout,
        resize: {
            stop : Dashing.updateLayout,
            enabled: true
        },
        draggable: {
          stop: function() {
            Dashing.showGridsterInstructions;
            Dashing.updateLayout();
          },
          start: function() {
            return Dashing.getWidgetPositions();
          }
        }
      });
    });
  });

}).call(this);
