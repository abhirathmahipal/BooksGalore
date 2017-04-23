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
        vm.delete_book = delete_book;

        function load_page(page) {
            favourite_service.get_page_data(page)
                .then(function(response) {
                    vm.page = response.data;
                });
        }

        function init() {
            load_page(1); // loading page 1
        }

        function next_page() {
            load_page(vm.page.current + 1);
        }

        function previous_page() {
            load_page(vm.page.current - 1);
        }

        function delete_book(isbn) {
            favourite_service.delete_book(isbn)
                .then(function(response) {
                    if (response.status == 200)
                        load_page(vm.page.current);
                });             
        }

        init();
    }
})();