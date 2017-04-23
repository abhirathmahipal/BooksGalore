(function () {
    'use strict';

    angular
        .module("booksgalore")
        .controller("favourite_controller", favourite_controller);

    favourite_controller.$inject = ["$scope", "favourite_service"];

    function favourite_controller($scope, favourite_service) {
        var vm = this;

        vm.page = null;
        vm.next_page = next_page;
        vm.previous_page = previous_page;

        function load_data(page) {
            vm.page = favourite_service.get_page_data(page)
                .then(function(response) {
                    vm.page = response.data;
                });
        }

        function init() {
            load_data(1); // loading page 1
        }

        function next_page() {
            load_data(vm.page.current + 1);
        }

        function previous_page() {
            load_data(vm.page.current - 1);
        }
        init();
    }
})();