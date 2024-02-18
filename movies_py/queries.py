import graphene
from graphene_django import DjangoObjectType
from .models import Genre, Movie


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie  # Corrected typo: 'nodel' -> 'model'
        fields = ('id', 'title', 'genre', 'rating', 'release', 'description')


class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    movies_by_genre = graphene.List(MovieType, genre=graphene.String(required=True))

    def resolve_all_movies(self, info):
        return Movie.objects.all()

    def resolve_movies_by_genre(self, info, genre):
        try:
            return Movie.objects.filter(genre__name=genre)
        except Genre.DoesNotExist:
            return 'Genre Does Not Exist'