import logging
import os
import pymongo
import csv


class Configure:
    KgMusicCollection = "kg_music_collection"
    HOST = "36.155.71.152"
    PORT = 27017
    DB = "mediaSource"
    Username = "mediaSource"
    Pwd = "mediaSource123"
    SingerFile = "singer_top100.txt"
    TargetFile = "result.csv"


class MusicProcessor:
    def __init__(self):
        conn = pymongo.MongoClient(host=Configure.HOST, port=Configure.PORT,
                                   username=Configure.Username, password=Configure.Pwd, authSource=Configure.DB)
        self.db = conn[Configure.DB]

    def get_song_bysingers(self):
        logging.debug('get_song_by_singers')
        self.music_process()

    def music_process(self):
        with open(Configure.SingerFile, encoding='utf-8')as sf:
            with open(Configure.TargetFile, "w") as tf:
                cw = csv.writer(tf, delimiter='\t')
                cw.writerow(["singer", "song"])
                for singer in sf:
                    logging.debug("singer: ".format(singer))
                    songs = self.get_song_bysinger(singer.strip('\n'))
                    logging.debug(songs)
                    for song in songs:
                        cw.writerow([singer.strip('\n'), song])

    def get_song_bysinger(self, singer):
        logging.debug('get_song_by_singer singer:'.format(singer))
        dbdata = self.db[Configure.KgMusicCollection].find({"singer_name": singer}, {"song_name": 1}).limit(5)
        logging.debug("dbdata:".format(dbdata))
        songs=set() 
        for song in dbdata:
            s= song['song_name'].split(" (")[0]
            songs.add(s)
        return songs


def main():
    mp = MusicProcessor()
    mp.get_song_bysingers()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    main()
