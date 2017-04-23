(function () {
    'use strict'

    angular
        .module("booksgalore")
        .factory("favourite_service", favourite_service);

    favourite_service.$inject = ["$http"];

    function favourite_service($http) {
        
        return {
            get_page_data: get_page_data,
            delete_book: delete_book
        };

        function get_page_data(page) {
            return $http.post("/manage/page/" + page);
        }

        function delete_book(isbn) {
            return $http.delete("/manage/delete/" + isbn);
        }
    }
})();