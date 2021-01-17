import os
from dotenv import load_dotenv
import requests

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

# user_a = User(1, "Bob", 100);
# user_b = User(2, "Alice", 300);

# print(user_a)
# print(user_b)
# print(user_a < user_b)

# people = [user_b, user_a]
# print(people)
# people.sort()
# print(people)
# people.pop(0)
# print(people)

load_dotenv()
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

username = "WellsLucasSanto"
print("Getting most followed followers for: " + username)

# Get user's id
username_endpoint = "https://api.twitter.com/2/users/by/username/" + username
headers = {'Authorization': 'Bearer ' + BEARER_TOKEN}
response = requests.get(username_endpoint, headers=headers)
if response.status_code != 200:
  raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
response = response.json()
user_id = response['data']['id']
print("User ID is " + user_id)

# Get user's follower list
followers_endpoint = "https://api.twitter.com/2/users/" + user_id + "/followers"
headers = {'Authorization': 'Bearer ' + BEARER_TOKEN}
params = {'max_results': 1000}
response = requests.get(followers_endpoint, headers=headers, params=params)
if response.status_code != 200:
  raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
response = response.json()
meta = response['meta']
result_count = meta['result_count']
next_token = meta['next_token']
print(response)

while (next_token):
  params = {'max_results': 1000, 'pagination_token': next_token}
  response = requests.get(followers_endpoint, headers=headers, params=params)
  if response.status_code != 200:
    raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
  response = response.json()
  meta = response['meta']
  result_count = meta['result_count']
  if ('next_token' in meta):
    next_token = meta['next_token']
  else:
    next_token = None
  print(response)

# Iterate through the user's followers
# For each user, check their follower count (using the API)
  # GET https://api.twitter.com/2/users/:id
  # user.fields=public_metrics      public_metric.followers_count
# Populate the list of top 10 accounts as you iterate (using sort and pop)
# Return the list
