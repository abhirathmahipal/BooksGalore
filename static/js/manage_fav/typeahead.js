var book_results = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
    url: '/search/book/%QUERY',
    wildcard: '%QUERY'
    }
});

$('#typeahead-add-book').typeahead(null, {
    name: 'searchbook',
    displayKey: 'isbn',
    source: book_results,
    templates: {
        suggestion: function (searchbook) {
            return '<div>' + searchbook.title + '</div>';
        }
    }
});