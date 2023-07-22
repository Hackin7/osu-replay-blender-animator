from .osrparse import Replay, parse_replay_data
# pip3 install osrparse

def read_replay_file(filepath):
    # parse from a path
    replay = Replay.from_path(filepath)
    # a replay has various attributes
    r = replay
    data = []
    for rr in r.replay_data:
        if rr.time_delta > 20: print(rr)
        #t.goto(rr.x/1, rr.y/1)
        data.append([rr.x, rr.y, rr.time_delta, int(rr.keys)]) #, rr.key])
    return data
