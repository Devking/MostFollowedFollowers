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

# Note that we're currently limited to 300 followers due to request limit
username = "WellsLucasSanto"
username = "NoThisIsPatchan"
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

# Get user's follower list (follower's IDs)
# Currently we add all the followers to a very long list
# A potentially better way would be to check their followers as we go
# 15 requests per 15 minute window (aka 15,000 max followers)
followers_endpoint = "https://api.twitter.com/2/users/" + user_id + "/followers"
headers = {'Authorization': 'Bearer ' + BEARER_TOKEN}
next_token = None
params = {'max_results': 1000}
follower_ids = []

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
data = response['data']
for user in data:
  follower_ids.append(user['id'])

while (next_token):
  params['pagination_token'] = next_token
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
  data = response['data']
  for user in data:
    follower_ids.append(user['id'])

# Iterate through the followers
# 300 requests per 15-minute window (aka 300 max followers)
print("Number of followers: " + len(follower_ids))
top_followers = []
for follower_user_id in follower_ids:
  follower_id_endpoint = "https://api.twitter.com/2/users/" + follower_user_id
  headers = {'Authorization': 'Bearer ' + BEARER_TOKEN}
  params = {'user.fields': 'public_metrics'}
  response = requests.get(follower_id_endpoint, headers=headers, params=params)
  if response.status_code != 200:
    print(top_followers) # Print the top followers up to this point
    raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
  response = response.json()
  follower_count = response['data']['public_metrics']['followers_count']
  username = response['data']['username']
  if len(top_followers) < 11:
    top_followers.append(User(follower_user_id, username, follower_count))
    top_followers.sort()
  else:
    if follower_count > top_followers[0].followers:
      top_followers.append(User(follower_user_id, username, follower_count))
      top_followers.sort()
      top_followers.pop(0)

print(top_followers)
