from osrparse import Replay, parse_replay_data
# pip3 install osrparse

# parse from a path
replay = Replay.from_path("../replay.osr")

# a replay has various attributes
r = replay
print(r.mode, r.game_version, r.beatmap_hash, r.username,
    r.replay_hash, r.count_300, r.count_100, r.count_50, 
    r.count_geki, r.count_miss, r.score, r.max_combo, r.perfect, 
    r.mods, r.life_bar_graph, r.timestamp, r.replay_data, 
    r.replay_id, r.rng_seed)

# parse the replay data from api v1's /get_replay endpoint
#lzma_string = retrieve_from_api()
#replay_data = parse_replay_data(lzma_string)
# replay_data is a list of ReplayEvents

print(r.replay_data[0])

import turtle
#t = turtle.Turtle()

#turtle.tracer(0,0)
#t.speed(10)
#t.speed(0)

data = []
for rr in r.replay_data:
  if rr.time_delta > 20: print(rr)
  #t.goto(rr.x/1, rr.y/1)
  data.append([rr.x, rr.y, rr.time_delta, int(rr.keys)]) #, rr.key])

with open("data.txt", "w") as f:
  f.write(str(data))
