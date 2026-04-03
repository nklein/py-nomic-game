from .players import relevant_player_login

from .json_utils import safe_seq

from .decision import AcceptDecision, RejectDecision, DeferDecision

from .vote_count import tally_votes_on_pr_head_for_relevant_users, tally_accepts_proportion_of_voters, tally_rejects_proportion_of_voters

from .datetime_utils import str2datetime

from functools import reduce


def augmented_pull_requests_by_updated_at_as_datetime(a):
    return str2datetime(a.get('pull_request').get('updated_at'))

def sort_list_of_agumented_by_pull_request_updated_at(list_of_augmented):
    return sorted(safe_seq(list_of_augmented).copy(), key=augmented_pull_requests_by_updated_at_as_datetime)

def reject_if_not_from_relevant_user(augmented):
    if relevant_player_login(augmented.get('pull_request').get('user').get('login')):
        return None
    else:
        return RejectDecision(augmented.get('id'),
                              'Will not accept pull-request from user <%s>' % (
                                  augmented.get('pull_request').get('user').get('login')
                              ))

def reject_if_half_voted_to_reject(augmented):
    proportion = tally_rejects_proportion_of_voters(tally_votes_on_pr_head_for_relevant_users(augmented))
    if 1/2 <= proportion:
        return RejectDecision(augmented.get('id'),
                              'More than half (%s) of the eligible voters rejected' % (
                                  proportion
                              ))
    else:
        return None

def find_reject(found, augmented):
    return found \
        or reject_if_not_from_relevant_user(augmented) \
        or reject_if_half_voted_to_reject(augmented) \
        or None

def accept_if_majority_voted_to_accept(augmented):
    proportion = tally_accepts_proportion_of_voters(tally_votes_on_pr_head_for_relevant_users(augmented))
    if 1/2 < proportion:
        return AcceptDecision(augmented.get('id'),
                              'More than half (%s) of the eligible voters accepted' % (
                                  proportion
                              ))
    else:
        return None

def find_accept(found, augmented):
  return found \
    or accept_if_majority_voted_to_accept(augmented) \
    or None

def decide(list_of_augmented):
  sorted_list = sort_list_of_agumented_by_pull_request_updated_at(list_of_augmented)

  return reduce(find_reject, sorted_list, None) \
    or reduce(find_accept, sorted_list, None) \
    or DeferDecision()
