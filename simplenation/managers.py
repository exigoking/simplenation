from django.db import models
from django.db.models import Q


class FavouriteManager(models.Manager):

    def favorees_for_user(self, user):
        favorees = []
        qs = self.filter(favoror=user)
        for favourite in qs:
                favorees.append(favourite.favoree)

        return favorees
 

    def remove(self, user1, user2):
        favourites = self.filter(favoror=user1, favoree=user2)
        if favourites:
            favourites.delete()
            return 0

        return 1

    def is_favoree(self, user1, user2):
        return self.filter(Q(favoror=user1, favoree=user2)).count() > 0

    def favoree_count(self, user):
        return self.filter(Q(favoror=user)).count()



class ChallengeManager(models.Manager):

    def challengees_for_user(self, user, term):
        challengees = []
        qs = self.filter(challenger = user, term = term)
        for challenge in qs:
            challengees.append(challenge.challengee)

        return challengees

    def challengees_for_term(self, term):
        challengees = []
        qs = self.filter(term = term)
        for challenge in qs:
            challengees.append(challenge.challengee)

        return challengees

    def challengers_for_term(self, term):
        challengers = []
        qs = self.filter(term = term)
        for challenge in qs:
            challengers.append(challenge.challenger)

        return challengers

    def subjects_for_user(self, user):
        subjects = []
        qs = self.filter(challengee = user)
        for challenge in qs:
            subjects.append(challenge.subject)

        return subjects

    def been_challenged(self, user1, user2, term):
        return self.filter(Q(challenger=user1, challengee=user2, subject = term)).count() > 0

    def remove_challenge(self, user1, user2, term):
        challenges = self.filter(Q(challenger=user1, challengee=user2, subject = term))
        if challenges:
            challenges.delete()
            return 0

        return 1


class NotificationManager(models.Manager):

    def check_notifications(self, receiver, last_time_checked):
        notifications = []
        qs = self.filter(receiver = receiver).order_by('-created_at')
            
        if qs:
            for notification in qs:

                if notification.created_at > last_time_checked:
                    notifications.append(notification)
                else:
                    break

        else:
            notifications = None

        return notifications

    def unseen_notifications(self, receiver):
        notifications = self.filter(receiver = receiver, seen = False).order_by('-created_at')
        return notifications

    def recent_notifications(self, receiver):
        notifications = self.filter(receiver = receiver).order_by('-created_at')[:50]
        return notifications


class LikeManager(models.Manager):

    def likers_for_definition(self, definition):
        return self.filter(definition=definition)

    def has_liked(self, user, definition):
        return self.filter(Q(user=user, definition=definition)).count() > 0

    def is_upvote(self, user, definition):
        like = self.filter(Q(user=user, definition=definition))
        if like:
            return like.upvote
        return False

    def is_downvote(self, user, definition):
        like = self.filter(Q(user=user, definition=definition))
        if like:
            return like.downvote
        return False

class TermVoteManager(models.Manager):

    def voters_for_definition(self, term):
        return self.filter(term=term)

    def has_voted(self, user, term):
        return self.filter(Q(user=user, term=term)).count() > 0

    def is_upvote(self, user, term):
        like = self.filter(Q(user=user, term=term))
        if like:
            return like.upvote
        return False

    def is_downvote(self, user, term):
        like = self.filter(Q(user=user, term=term))
        if like:
            return like.term
        return False


        

        


    

