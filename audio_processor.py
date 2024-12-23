import multiprocessing

def process_tracks(tracks):

    procs = []

    for index, track in enumerate(tracks):
        proc = multiprocessing.Process(target=get_processed_tracks, args=(index, tracks))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    return tracks




def get_processed_tracks(index, tracks):
    tracks[index] = tracks[index]