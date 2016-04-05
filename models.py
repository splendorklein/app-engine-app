"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""


from datetime import date
from protorpc import messages
from google.appengine.ext import ndb



class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()
    performance = ndb.FloatProperty(required=True, default=0)
    
    def to_form(self):
            """Returns a Form representation of the USER"""
            form = UserForm()
            form.name = self.name
            form.email = self.email
            form.performance = self.performance
 
            return form


class UserForm(messages.Message):
    """userForm for outbound user state information"""
    name = messages.StringField(1, required=True)
    email = messages.StringField(2)
    performance = messages.FloatField(3,required=True)


class UserForms(messages.Message):
    """userForms for outbound users' state information"""
    users = messages.MessageField(UserForm, 1, repeated=True)

class MovesForm(messages.Message):
    """Form for outbound game history information"""
    moves = messages.StringField(1, repeated=True)


class Game(ndb.Model):
    """Game object"""
    target = ndb.StringProperty(required=True)
    current = ndb.StringProperty(required=True)
    attempts_allowed = ndb.IntegerProperty(required=True)
    attempts_remaining = ndb.IntegerProperty(required=True, default=5)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    moves = ndb.StringProperty(repeated=True)

    @classmethod
    def new_game(cls, user, attempts, targetword, currentword, message):
        """Creates and returns a new game"""
 
        game = Game(user=user,
                    target=targetword,
                    current=currentword,
                    moves=message,
                    attempts_allowed=attempts,
                    attempts_remaining=attempts,
                    game_over=False)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.currentword = self.current
        form.game_over = self.game_over
        form.message = message
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      score=(len(self.target) + 14 - self.attempts_remaining))
                      
        score.put()





class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    score = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), score=self.score)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    currentword = messages.StringField(3, required=True)
    game_over = messages.BooleanField(4, required=True)
    message = messages.StringField(5, required=True)
    user_name = messages.StringField(6, required=True)

class GameForms(messages.Message):
    """GameForms for outbound games' state information"""
    games = messages.MessageField(GameForm, 1, repeated=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)

    attempts = messages.IntegerField(2, default=5)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    guess = messages.StringField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    score = messages.IntegerField(4, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)




