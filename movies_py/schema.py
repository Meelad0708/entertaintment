import graphene
from graphene_django import DjangoObjectType
from .models import Genre, Movie
from .queries import GenreType, MovieType, Query
from .mutation import CreateGenre, CreateMovie


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'rating', 'release', 'description')

class Mutation(graphene.ObjectType):
    create_genre = CreateGenre.Field()
    create_movie = CreateMovie.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


