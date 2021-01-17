class User:
  def __init__(self, id, username, followers):
    self.id = id
    self.username = username
    self.followers = followers

  def __str__(self):
    return "User: {} ID: {} Followers: {}".format(self.username, self.id, self.followers)

  def __repr__(self):
    return "<User: {}, ID: {}, Followers: {}>".format(self.username, self.id, self.followers)

  def __lt__(self, other):
    return self.followers < other.followers

user_a = User(1, "Bob", 100);
user_b = User(2, "Alice", 300);

print(user_a)
print(user_b)
print(user_a < user_b)

people = [user_b, user_a]
print(people)
people.sort()
print(people)
people.pop(0)
print(people)

# Get username
# Get user's id using the API
  # GET https://api.twitter.com/2/users/by/username/:username
  # My ID is 161051718
# Get user's follower list using the API (repeat this step due to pagination)
  # GET https://api.twitter.com/2/users/:id/followers
  # Returns an object with property "data" that's an array of users
  # Each user has id and username fields I should keep
  # Also returns property "meta" with "next_token" to use for the next API call
# Iterate through the user's followers
# For each user, check their follower count (using the API)
  # GET https://api.twitter.com/2/users/:id
  # user.fields=public_metrics      public_metric.followers_count
# Populate the list of top 10 accounts as you iterate (using sort and pop)
# Return the list
