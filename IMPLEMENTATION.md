# py-nomic-game Implementation

Caveat: Take this document with a grain of salt.
It was written to describe the initial implementation before any pull-requests are merged.
There is a high-likelihood that pull-requests will change
either the implementation or this document without changing both.

The object of this nomic game is to have the code in this repository decide that you are the winner.

The implementation receives an array of open pull requests for this repository on standard input
and outputs a single JSON response decision on standard output.

**Important Things to Note About The Initial Implementation:**
* If your GitHub login name is not one of the ones in the `players` array, your pull requests will be ignored.
* If your GitHub login name is not one of the ones in the `players` array, your votes on other pull requests will be ignored.
* If your vote on a pull request is on a revision that is no longer the head of the pull request, your vote no longer counts.
* Voting on a pull request is, regrettably, tricky. (See the [**How to Vote** section](#how-to-vote) below.)

## [How to Vote]

Unfortunately, GitHub has a mechanism whereby a reviewer can mark a pull request as approve.
They do not, however, have a mechanism by which a reviewer can mark a pull request as rejected.

Furthermore, pull-request comments are not easy to order against commits.
Reviews, on the other hand, are tied to a particular commit.

To eliminate ambiguity about whether something is accepted or rejected, this code requires a review comment that is precisely (as in, string-compare) equivalent to the text `ACCEPT` or the text `REJECT` to consider it a vote.

To avoid abuse where one pushes a malicious modification to a pull-request after everyone has
voted to approve it, only review comments are considered by the initial implementation here.

To submit a review, you should navigate to the pull request on the GitHub website.
From there, you can click on the `Files changed` tab.
There is a green button on the right side of the top of the tab that reads **Submit review**.
Click on it.
It will open a drop-down form.
Enter either `ACCEPT` or `REJECT` (with no newlines or spaces or any other text).
Make sure you have `Comment` selected from the radio buttons.
Then, press the **Submit review** button at the bottom of the drop-down form.

## Implementation in More Depth

### [Decision Classes]

There are decision classes implemented in `src/decision.py`.
They all have a method called `toJson()` which will convert them to a JSON object appropriate for standard output.

The decision classes that the initial implementation will emit to standard output are:
* `AcceptDecision( augmented.id, <nullable-string> )`
* `RejectDecision( augmented.id, <nullable-string> )`
* `DeferDecision()`

To win, it would be convenient for you to emit this message:
* `WinnerDecision( <name-of-winner>, <nullable-string> )`

The initial implementation **never** creates a winner decision.

### How the Initial Implementation Makes Decisions

The decision logic is implemented in the `decide()` function in `src/decide.py`.

That function takes the array of "augmented pull requests" (see the [**Augmented Pull Requests** section](#augmented-pull-requests) below).
It makes a shallow copy of the array and sorts the items by the `item.pull_request.updated_at` timestamps.
The sorting is from oldest to newest.

Given the sorted array:
* it goes through to find the first one that it wants to reject,
* if it didn't find one to reject, it goes through to find one to accept,
* and if it still hasn't found anything, it emits a defer decision.

The `src/players.py` contains an array of `players` and defines a function:

    relevant_player_login(login) => the player object in the players list with that login

#### When to reject a pull request

The `find_reject(...)` function is used with `reduce(...)` to return the first
instance in the array of augmented pull requests that should be rejected.

The implementation will reject any pull request that was made by a user with a login
that garners a falsey return from `relevant_player_login(...)`.

If it hasn't rejected an augmented pull request for that reason, it tallies up
the `ACCEPT` or `REJECT` votes from relevant players on the `HEAD` of the pull request.
If half or more of the relevant players have voted to `REJECT`, the pull request is rejected.
*Note:* 50% of the relevant players voting `REJECT` will kill a pull request.

#### When to accept a pull request

The `find_accept(...)` function is used with `reduce(...)` to return the first
instance in the list of augmented pull requests that should be accepted.

The code tallies up the `ACCEPT` or `REJECT` votes from relevant players on the `HEAD` of the pull request.
If more than half of the relevant players have voted to `ACCEPT`, the pull request is accepted.
*Note:* 50% of the relevant players voting `ACCEPT` is not enough to approve a pull request.


#### How votes are tallied

The votes are tallied by sorting the `augmented_pull_request.reviews` array by their `submitted_at`
timestamp from oldest to newest.

If a particular review is from a user login that garners a falsey return from `relevant_user_login(...)`, the
review is ignored.

If a particular review is for a revision that is no longer the head of the pull-request, the review is ignored.

If the review is not **exactly** the text `ACCEPT` or the text `REJECT`, the review is ignored.

From what's left, the code collects the most recent `ACCEPT` or `REJECT` by user login.
It then counts the number of `ACCEPT` votes and the number of `REJECT` votes.

When determining proportions, the numerator is either the number of `ACCEPT` votes
or the number of `REJECT` votes whilst the denominator is the number
returned by the `relevant_player_count()` function in `src/players.py`.

## [Augmented Pull Requests]

The supervisor gives this code a list of augmented pull requests on standard input.

An augmented pull request is:
* an `id` number (unique during this run) for the augmented pull request,
* the `pull_request` returned by the [*Get a pull request* GitHub API](https://docs.github.com/en/rest/pulls/pulls?apiVersion=2026-03-10#get-a-pull-request),
* the list of `reviews` on the pull request returned by the [*List reviews for a pull request* GitHub API](https://docs.github.com/en/rest/pulls/reviews?apiVersion=2026-03-10#list-reviews-for-a-pull-request),
* the list of `comments` on the pull request returned by the [*List issue comments* GitHub API](https://docs.github.com/en/rest/issues/comments?apiVersion=2026-03-10#list-issue-comments) (Note: all pull requests are issues, but not all issues are pull requests), and
* the list of `commits` on the pull request returned by [*List commits on a pull request* GitHub API](https://docs.github.com/en/rest/pulls/pulls?apiVersion=2026-03-10#list-commits-on-a-pull-request).

These are all wrapped together in a JSON object.

    {
      "id": id-number,
      "pull_request": pull-request-object,
      "reviews": array-of-reviews-or-null,
      "comments": array-of-comments-or-null,
      "commits": array-of-commits-or-null
    }
