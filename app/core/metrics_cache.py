from collections import defaultdict

user_event_counter = defaultdict(int)

def increment_user_event(user_id: int):
    user_event_counter[user_id] += 1

def get_user_event_count(user_id: int):
    return user_event_counter[user_id]
