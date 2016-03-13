(function() {
    console.log("Yeah! pyDashing running !!");

    /*
    Batman.Filters.dashize = function(str) {
        return str.charAt(0).toLowerCase() + str.slice(1);
    };
    */
    Batman.helpers.underscore = function(str) {
        console.log(str);
        return str.charAt(0).toLowerCase() + str.slice(1);
    };

    Dashing.updateLayout = function() {
        if(Dashing.allowRefresh >= 0) Dashing.allowRefresh = 2;
        console.log(Dashing.currentWidgetPositions);
        $.ajax({
            url: '/update',
            type: 'POST',
            dataType: "json",
            contentType: 'application/json',
            data: Dashing.currentWidgetPositions,
        })
        .done(function() {
        console.log($('#saving-message'));
           $('#saving-message').html("Saved.");
        })
        .fail(function() {
        console.log($('#saving-message'));
            $('#saving-message').html("Error saving layout.");
        });
    }

    Dashing.changeLayout = function() {
        var newData;
        newData = JSON.stringify(Dashing.getWidgetPositions());
        if (newData !== Dashing.currentWidgetPositions) {
            Dashing.currentWidgetPositions = newData;
            $('#save-gridster').slideDown();
            if(Dashing.allowRefresh >= 0) Dashing.allowRefresh = 0;
        }
    }

      $(function() {
        return $('#save-gridster').click(function() {
            Dashing.updateLayout();
        });
      });

  Dashing.on('ready', function() {
    var contentWidth;
    Dashing.widget_margins || (Dashing.widget_margins = [3, 3]);
    Dashing.widget_base_dimensions || (Dashing.widget_base_dimensions = [300, 320]);
    Dashing.numColumns || (Dashing.numColumns = 4);
    Dashing.allowRefresh = 1;
    contentWidth = (Dashing.widget_base_dimensions[0] + (Dashing.widget_margins[0] * 3)) * Dashing.numColumns;
    return Batman.setImmediate(function() {
      $('.gridster').width(contentWidth);
      return $('.gridster ul:first').gridster({
        widget_margins: Dashing.widget_margins,
        widget_base_dimensions: Dashing.widget_base_dimensions,
        avoid_overlapped_widgets: !Dashing.customGridsterLayout,
        extra_rows: 1,
        serialize_params: function($w, wgd) {
            //console.log('serialize');
            //console.log($w)
            //console.log(wgd)
            var wID = $w.find('div').attr('data-id');
            var wColor = $w.find('div').css('background-color');
            return {id: wID, color: wColor, col: wgd.col, row: wgd.row, x: wgd.size_x, y: wgd.size_y }
        },
        resize: {
            stop: Dashing.changeLayout,
            enabled: true
        },
        draggable: {
          stop: Dashing.changeLayout,
          start: function() {
            return Dashing.getWidgetPositions();
          }
        }
      });
    });
  });

}).call(this);

