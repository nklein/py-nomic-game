
from .players import relevant_player_login, relevant_player_count

from .json_utils import safe_seq

from .datetime_utils import str2datetime

ACCEPT = 'ACCEPT'
REJECT = 'REJECT'

def review_submitted_at_as_datetime(r):
    return str2datetime(r.get('submitted_at'))

def sort_reviews_by_summitted_at(list_of_reviews):
  return sorted(safe_seq(list_of_reviews).copy(), key=review_submitted_at_as_datetime)

def collect_votes_on_pr_head(augmented):
    head_sha = augmented.get('pull_request').get('head').get('sha')
    most_recent_vote_by_user = {}
    possible_votes = [ACCEPT, REJECT]

    for review in sort_reviews_by_summitted_at(augmented.get('reviews') or []):
        if (review.get('commit_id') == head_sha):
            try:
                vote = possible_votes[ possible_votes.index(review.get('body')) ]

                most_recent_vote_by_user[review.get('user').get('login')] = vote
            except ValueError:
                pass

    return most_recent_vote_by_user


def tally_votes_on_pr_head_for_relevant_users (augmented):
    accepts = 0
    rejects = 0
    voters = relevant_player_count()

    all_votes = collect_votes_on_pr_head(augmented)

    for user, vote in all_votes.items():
        if relevant_player_login(user):
            if vote == ACCEPT:
                accepts += 1
            elif vote == REJECT:
                rejects += 1

    return { 'accepts': accepts, 'rejects': rejects, 'voters': voters, }

def tally_accepts_proportion_of_voters(tally):
    return tally.get('accepts') / tally.get('voters')

def tally_rejects_proportion_of_voters(tally):
    return tally.get('rejects') / tally.get('voters')
