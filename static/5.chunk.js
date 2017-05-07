webpackJsonpac__name_([5],{

/***/ 594:
/***/ function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = __webpack_require__(10);
var Dashboard = (function () {
    function Dashboard() {
    }
    return Dashboard;
}());
Dashboard = __decorate([
    core_1.Component({
        selector: 'dashboard',
        template: __webpack_require__(645)
    })
], Dashboard);
exports.Dashboard = Dashboard;


/***/ },

/***/ 595:
/***/ function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = __webpack_require__(10);
var common_1 = __webpack_require__(43);
var router_1 = __webpack_require__(54);
var dashboard_component_ts_1 = __webpack_require__(594);
var widget_directive_1 = __webpack_require__(608);
exports.routes = [
    { path: '', component: dashboard_component_ts_1.Dashboard, pathMatch: 'full' }
];
var DashboardModule = (function () {
    function DashboardModule() {
    }
    return DashboardModule;
}());
DashboardModule.routes = exports.routes;
DashboardModule = __decorate([
    core_1.NgModule({
        imports: [common_1.CommonModule, router_1.RouterModule.forChild(exports.routes)],
        declarations: [dashboard_component_ts_1.Dashboard, widget_directive_1.Widget]
    })
], DashboardModule);
exports.DashboardModule = DashboardModule;


/***/ },

/***/ 608:
/***/ function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(jQuery) {
Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = __webpack_require__(10);
var Widget = (function () {
    function Widget(el) {
        this.$el = jQuery(el.nativeElement);
        jQuery.fn.widgster.Constructor.DEFAULTS.bodySelector = '.widget-body';
        /*
         When widget is closed remove its parent if it is .col-*
         */
        jQuery(document).on('close.widgster', function (e) {
            var $colWrap = jQuery(e.target)
                .closest('.content > .row > [class*="col-"]:not(.widget-container)');
            // remove colWrap only if there are no more widgets inside
            if (!$colWrap.find('.widget').not(e.target).length) {
                $colWrap.remove();
            }
        });
    }
    Widget.prototype.ngOnInit = function () {
        this.$el.widgster();
    };
    return Widget;
}());
Widget = __decorate([
    core_1.Directive({
        selector: '[widget]'
    }),
    __metadata("design:paramtypes", [core_1.ElementRef])
], Widget);
exports.Widget = Widget;

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(44)))

/***/ },

/***/ 645:
/***/ function(module, exports) {

module.exports = "<h1 class=\"page-title\">Dashboard <small><small>The Lucky One</small></small></h1>\r\n\r\n<div class=\"row\">\r\n  <div class=\"col-md-6\">\r\n    <section widget class=\"widget\">\r\n      <header>\r\n        <h4>\r\n          Example <span class=\"fw-semi-bold\">Widget</span>\r\n        </h4>\r\n        <div class=\"widget-controls\">\r\n          <a data-widgster=\"expand\" title=\"Expand\" href=\"#\"><i class=\"glyphicon glyphicon-chevron-up\"></i></a>\r\n          <a data-widgster=\"collapse\" title=\"Collapse\" href=\"#\"><i class=\"glyphicon glyphicon-chevron-down\"></i></a>\r\n          <a href=\"#\" data-widgster=\"close\"><i class=\"glyphicon glyphicon-remove\"></i></a>\r\n        </div>\r\n      </header>\r\n      <div class=\"widget-body\">\r\n        <img class=\"pull-left mr-sm\" src=\"assets/img/a2.png\" alt=\"Angular 4.0\" width=\"100\">\r\n        <p class=\"lead\">You are looking at a completely new version of Sing App built\r\n          with brand new <strong>Angular <em>4.0</em> Final Release</strong></p>\r\n        <p class=\"fs-mini\">Made by <a href=\"http://flatlogic.com\" target=\"_blank\">Flatlogic</a>.</p>\r\n      </div>\r\n    </section>\r\n  </div>\r\n</div>\r\n"

/***/ }

});
//# sourceMappingURL=5.map