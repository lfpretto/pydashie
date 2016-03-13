(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  Dashing.DashingInternal = (function(_super) {
    __extends(DashingInternal, _super);
    function DashingInternal() {
      return DashingInternal.__super__.constructor.apply(this, arguments);
    }
    DashingInternal.accessor('internal',  function() {
        if (this.get('updatedAt') != DashingInternal.lastCall) {
            var action = this.get('action')
            if (action=='reload') {
                if (Dashing.allowRefresh==1) {
                        window.location.reload();
                }
                if (Dashing.allowRefresh==2) {
                    Dashing.allowRefresh=1;
                }
            }
            DashingInternal.lastCall = this.get('updatedAt');
        }
        return DashingInternal.lastCall;
    });
    return DashingInternal;
  })(Dashing.Widget);

}).call(this);
