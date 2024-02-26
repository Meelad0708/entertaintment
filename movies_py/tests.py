import django
from django.test import TestCase
from django.core.management import call_command
from graphene.test import Client
from .models import Movie, Genre
from .schema import schema

# Create your tests here.

class MovieTestCase(TestCase):
    fixtures = ['test_fixture.json'] # Uses original db for testing

    def setUp(self): # Loads the db and sets up gql client for query and mutations
        call_command('loaddata', 'test_fixture.json', verbosity=0)
        self.client = Client(schema)

    def test_movie_exists(self): # Quick test to see if the db is fetched
        movie_exists = Movie.objects.filter(title='Shutter Island').exists()
        self.assertTrue(movie_exists, 'The movie exists in test database')

    def test_create_movie_without_title(self):
        executed = self.client.execute(''' 
            mutation {
                createMovie(
                    title: "",
                    genreId: "1",  
                    rating: 5,
                    release: "2010-01-01",
                    description: "Action Movie"
                ) {
                    movie {
                        id
                        title
                        genre {
                            name
                        }
                        rating
                        release
                        description
                    }
                }
            }
        ''')
        self.assertIn('errors', executed) # checks if there are errors in output
        self.assertEqual(len(executed['errors']), 1) # checks if there is only one error
        error_msg = executed['errors'][0]['message'] # fetches the message of the error
        expected_error = 'Movie Title Cannot Be Empty'
        self.assertEqual(error_msg, expected_error) # compares the error messages to see if they are the same

    def test_create_movie_that_already_exists(self):
        executed = self.client.execute('''
            mutation {
                createMovie(
                    title: "Die Hard",
                    genreId: "1",  
                    rating: 5,
                    release: "2010-01-01",
                    description: "Action Movie"
                ) {
                    movie {
                        id
                        title
                        genre {
                            name
                        }
                        rating
                        release
                        description
                    }
                }
            }
        ''')
        self.assertIn('errors', executed)
        self.assertEqual(len(executed['errors']), 1)
        error_msg = executed['errors'][0]['message']
        expected_error = 'Movie Already Exists'
        self.assertEqual(expected_error, error_msg)


    def test_empty_genre_name(self):
        executed = self.client.execute('''
            mutation {
                createGenre(
                    name: ""
                ) {
                    genre {
                        name
                        id
                    }
                }
            }
        ''')
        self.assertIn('errors', executed)
        self.assertEqual(len(executed['errors']), 1)
        error_msg = executed['errors'][0]['message']
        expected_msg = 'Genre Name Cannot Be Empty'
        self.assertEqual(error_msg, expected_msg)

    def test_future_release_date(self):
        executed = self.client.execute('''
            mutation {
                createMovie(
                    title: "Spiderman",
                    genreId: "1",  
                    rating: 5,
                    release: "2030-01-01",
                    description: "Action Movie"
                ) {
                    movie {
                        id
                        title
                        genre {
                            name
                        }
                        rating
                        release
                        description
                    }
                }
            }
        ''')
        self.assertNotIn('errors', executed)

    def test_negative_rating(self):
        executed = self.client.execute('''
            mutation {
                createMovie(
                    title: "Home Alone",
                    genreId: "1",  
                    rating: -5,
                    release: "2010-01-01",
                    description: "Action Movie"
                ) {
                    movie {
                        id
                        title
                        genre {
                            name
                        }
                        rating
                        release
                        description
                    }
                }
            }
        ''')
        self.assertNotIn('errors', executed)



