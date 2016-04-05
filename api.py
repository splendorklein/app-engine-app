# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""

import random
import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, Game, Score
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm,\
    ScoreForms, GameForms, UserForm, UserForms, MovesForm
from utils import get_by_urlsafe
from word import wordlist
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
SCORE_REQUEST = endpoints.ResourceContainer(
   limit= messages.IntegerField(1))

MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'


wordlistlen = len(wordlist)

@endpoints.api(name='hangman', version='v1')
class HangManApi(remote.Service):
    """Game API"""
    

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    def pickaWord(self):
        """pick a word from the list for the game """
        targetnum=random.choice(range(0, wordlistlen))
        a = wordlist[targetnum]
        b = ""
        for i in range(len(a)):
          b = b + "*"
        return [a,b]

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        if request.attempts > 14:
          raise endpoints.BadRequestException('At most 14 attempts!')
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        try:
            target = self.pickaWord()
            game = Game.new_game(user.key, request.attempts, target[0], target[1],
              ['{} created a new game'.format(user.name),])
        except:
            print 'mark 1: something wrong with creating a new game'

        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.
        taskqueue.add(url='/tasks/cache_average_attempts')
        return game.to_form('Good luck playing Hangman!')

    

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=MovesForm,
                      path='game/{urlsafe_game_key}/history',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Return the current game history."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)

        if game:
            form = MovesForm()
            form.moves = game.moves
            return form
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game/delete/{urlsafe_game_key}',
                      name='delete_game',
                      http_method='POST')
    def delete_game(self, request):
        """delete the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
          if not game.game_over:
                game.key.delete()
                return StringMessage(message='Game deleted!')
          else:
            raise endpoints.BadRequestException('Game already over!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=GameForms,
                      path='game/user/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all of an individual User's games"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        games = Game.query(Game.user == user.key)
        return GameForms(games=[game.to_form("") for game in games])

    @endpoints.method(response_message=UserForms,
                      path='user/rankings',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Returns rankings of all Users"""
        users = User.query()
        if not users:
            raise endpoints.NotFoundException('No User exists!')
        for user in users:
          scores = Score.query(Score.user == user.key).fetch()
          p = 0
          if scores:
            count = len(scores)
            
            for score in scores:
                p += score.score
            p = p / count
          user.performance = p
          user.put()

        users = User.query().order(-User.performance)

        
        return UserForms(users=[user.to_form() for user in users])

    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message and 
        updates a game's history"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over!')

        game.attempts_remaining -= 1
        
        if len(request.guess) != 1:
            raise endpoints.BadRequestException('Only one letter each guess!')

        targettem = list(game.target)
        currenttem = list(game.current)
        guessresult = False
        for i in range(len(targettem)):
            if targettem[i] == request.guess.lower():
                currenttem[i] = request.guess.lower()
                guessresult = True
        newcurrent = ""
        for l in currenttem:
            newcurrent += l

        game.current = newcurrent
        game.put()

        if newcurrent == game.target:
              game.moves.append("made a guess: '{}', result: {}, You win!"
                .format(request.guess,newcurrent))
              game.put()
              game.end_game(True)
              return game.to_form('You win!')

        if guessresult:
            game.moves.append("made a guess: '{}', result: {}, Bingo!"
                .format(request.guess, newcurrent))
            msg = 'Bingo!'
        else:
            game.moves.append("made a guess: '{}', result: {}, You missed!!"
                .format(request.guess, newcurrent))
            msg = 'You missed!'

        if game.attempts_remaining < 1:
            game.end_game(False)
            return game.to_form(msg + ' Game over!')
        else:
            game.put()
            return game.to_form(msg)




    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=SCORE_REQUEST,
                      response_message=ScoreForms,
                      path='hightscores',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Return highest scores"""
        scores = Score.query()
        scores = scores.order(-Score.score)

        if request.limit > 0 :
          scores = scores.fetch(request.limit)


        return ScoreForms(items=[score.to_form() for score in scores])    


    @endpoints.method(request_message=USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(response_message=StringMessage,
                      path='games/average_attempts',
                      name='get_average_attempts_remaining',
                      http_method='GET')
    def get_average_attempts(self, request):
        """Get the cached average moves remaining"""
        return StringMessage(message=memcache.get(MEMCACHE_MOVES_REMAINING) or '')

    @staticmethod
    def _cache_average_attempts():
        """Populates memcache with the average moves remaining of Games"""
        games = Game.query(Game.game_over == False).fetch()
        if games:
            count = len(games)
            total_attempts_remaining = sum([game.attempts_remaining
                                        for game in games])
            average = float(total_attempts_remaining)/count
            memcache.set(MEMCACHE_MOVES_REMAINING,
                         'The average moves remaining is {:.2f}'.format(average))


api = endpoints.api_server([HangManApi])
