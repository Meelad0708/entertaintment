import graphene
from graphene_django import DjangoObjectType
from .models import Genre, Movie
from .queries import GenreType, MovieType
class CreateGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(GenreType)

    def mutate(self, info, name):
        genre = Genre.objects.create(name=name)
        return CreateGenre(genre=genre)

class CreateMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        genre_id = graphene.ID(required=True)
        rating = graphene.Int(required=True)
        release = graphene.Date(required=True)
        description = graphene.String()

    movie = graphene.Field(MovieType)

    def mutate(self, info, title, genre_id, rating, release, description):
        genre = Genre.objects.get(pk=genre_id)
        movie = Movie.objects.create(title=title, genre=genre, rating=rating, release=release, description=description)
        return CreateMovie(movie=movie)
