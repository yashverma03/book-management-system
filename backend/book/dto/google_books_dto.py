from rest_framework import serializers


class GoogleBooksDto(serializers.Serializer):
    q = serializers.CharField(
        required=True,
        help_text='Full-text search query string. Examples: "flowers", "flowers+inauthor:keyes"'
    )
    maxResults = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=40,
        default=10,
        help_text='Maximum number of results to return (1-40, default: 10)'
    )
    startIndex = serializers.IntegerField(
        required=False,
        min_value=0,
        default=0,
        help_text='Index of the first result to return (default: 0)'
    )
    filter = serializers.ChoiceField(
        required=False,
        choices=['ebooks', 'free-ebooks', 'paid-ebooks', 'partial'],
        help_text='Filter search results by volume type and availability'
    )
    printType = serializers.ChoiceField(
        required=False,
        choices=['all', 'books', 'magazines'],
        help_text='Restrict to books or magazines (default: all)'
    )
    orderBy = serializers.ChoiceField(
        required=False,
        choices=['relevance', 'newest'],
        help_text='Sort search results (default: relevance)'
    )
    langRestrict = serializers.CharField(
        required=False,
        max_length=10,
        help_text='Restrict results to books with this language code (e.g., "en", "es", "fr")'
    )
    projection = serializers.ChoiceField(
        required=False,
        choices=['full', 'lite'],
        help_text='Restrict information returned to a set of selected fields (default: full)'
    )
