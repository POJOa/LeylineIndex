webpackJsonpac__name_([6],{

/***/ 591:
/***/ function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = __webpack_require__(10);
var ownership_service_1 = __webpack_require__(593);
var AnotherPage = (function () {
    function AnotherPage(ownershipService) {
        this.ownershipService = ownershipService;
    }
    AnotherPage.prototype.genFile = function () {
        this.ownershipService.genFile();
    };
    AnotherPage.prototype.fileCheck = function (sid) {
        this.ownershipService.fileCheck(sid);
    };
    AnotherPage.prototype.cnameCheck = function (sid) {
        this.ownershipService.cnameCheck(sid);
    };
    AnotherPage.prototype.metaCheck = function (sid) {
        this.ownershipService.metaCheck(sid);
    };
    return AnotherPage;
}());
AnotherPage = __decorate([
    core_1.Component({
        selector: 'another',
        template: __webpack_require__(644),
        providers: [ownership_service_1.OwnershipService],
    }),
    __metadata("design:paramtypes", [ownership_service_1.OwnershipService])
], AnotherPage);
exports.AnotherPage = AnotherPage;


/***/ },

/***/ 592:
/***/ function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = __webpack_require__(10);
var common_1 = __webpack_require__(43);
var router_1 = __webpack_require__(54);
var another_component_ts_1 = __webpack_require__(591);
var angular2_jwt_1 = __webpack_require__(369);
var http_1 = __webpack_require__(72);
var login_module_1 = __webpack_require__(366);
exports.routes = [
    { path: '', component: another_component_ts_1.AnotherPage, pathMatch: 'full' }
];
var AnotherModule = (function () {
    function AnotherModule() {
    }
    return AnotherModule;
}());
AnotherModule = __decorate([
    core_1.NgModule({
        imports: [common_1.CommonModule, router_1.RouterModule.forChild(exports.routes)],
        declarations: [another_component_ts_1.AnotherPage],
        providers: [
            {
                provide: angular2_jwt_1.AuthHttp,
                useFactory: login_module_1.authHttpServiceFactory,
                deps: [http_1.Http, http_1.RequestOptions]
            }
        ]
    })
], AnotherModule);
exports.AnotherModule = AnotherModule;


/***/ },

/***/ 593:
/***/ function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = __webpack_require__(10);
__webpack_require__(374);
var angular2_jwt_1 = __webpack_require__(369);
var OwnershipService = OwnershipService_1 = (function () {
    function OwnershipService(http) {
        this.http = http;
        this.fileUrl = 'http://localhost:5000/owned/gen';
        this.ownershipUrl = 'http://localhost:5000/owned/';
    }
    OwnershipService.prototype.genFile = function () {
        return this.http.get(this.fileUrl).toPromise().then(function (r) { return OwnershipService_1.downloadFile(r._body); });
    };
    OwnershipService.downloadFile = function (data) {
        var blob = new Blob([data], { type: 'text/plain' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.target = '_blank';
        a.download = data + '.txt';
        document.body.appendChild(a);
        a.click();
    };
    OwnershipService.prototype.fileCheck = function (id) {
        return this.http.get(this.ownershipUrl + id + '/file')
            .toPromise()
            .then(function (response) { return response.json(); })
            .catch(OwnershipService_1.handleError);
    };
    OwnershipService.prototype.cnameCheck = function (id) {
        return this.http.get(this.ownershipUrl + id + '/cname')
            .toPromise()
            .then(function (response) { return response.json(); })
            .catch(OwnershipService_1.handleError);
    };
    OwnershipService.prototype.metaCheck = function (id) {
        return this.http.get(this.ownershipUrl + id + '/meta')
            .toPromise()
            .then(function (response) { return response.json(); })
            .catch(OwnershipService_1.handleError);
    };
    OwnershipService.handleError = function (error) {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    };
    return OwnershipService;
}());
OwnershipService = OwnershipService_1 = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [angular2_jwt_1.AuthHttp])
], OwnershipService);
exports.OwnershipService = OwnershipService;
var OwnershipService_1;


/***/ },

/***/ 644:
/***/ function(module, exports) {

module.exports = "<h1 class=\"page-title\">Another Page <small>Just like that</small></h1>\n\n<div class=\"widget-container\">\n  <br>\n  <br>\n  <br>\n  <br>\n  <br>\n  <br>\n\n  <button (click)=\"genFile()\" class=\"btn btn-default\">download file</button>\n\n  <br>\n  <br>\n  <br>\n  <br>\n  <br>\n  <br>\n\n  <button (click)=\"fileCheck('5901c55e1bf170cff3e6968f')\" class=\"btn btn-default\">ownership file check</button>\n\n  <br>\n  <br>\n  <br>\n  <br>\n  <br>\n  <br>\n\n  <button (click)=\"cnameCheck('5901c55e1bf170cff3e6968f')\" class=\"btn btn-default\">cname check</button>\n\n  <br>\n  <br>\n  <br>\n  <br>\n  <br>\n  <br>\n\n  <button (click)=\"metaCheck('5901c55e1bf170cff3e6968f')\" class=\"btn btn-default\">meta check</button>\n\n  <div>Some page content. Feel free to place whatever you want here</div>\n</div>\n"

/***/ }

});
//# sourceMappingURL=6.map