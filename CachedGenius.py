from __future__ import annotations

# Standard
import typing
import json

# External
import lyricsgenius

# Internal
from MinimalSongData import MinimalSongData
from Artist import Artist

from CustomLogger import logger


class CachedGenius:
    def __init__(self, geniusClient: lyricsgenius.Genius, cache: list[MinimalSongData], forceOffline: bool = False) -> None:
        self.geniusClient = geniusClient
        self.cachedSongs = cache
        self.forceOffline = forceOffline

    def searchLyrics(self, lyrics: str) -> list[MinimalSongData]:
        results = self.searchCached(lambda song: lyrics.lower() in song.lyrics.lower())

        logger.debug(f"{len(results)} results are found in the cache.")

        if results or self.forceOffline:
            return results

        self.searchLyricsViaAPI(lyrics)

        return self.searchCached(lambda song: lyrics.lower() in song.lyrics.lower())

    def searchCached(self, checker: typing.Callable[[MinimalSongData], bool]) -> list[MinimalSongData]:
        results: list[MinimalSongData] = []

        for song in self.cachedSongs:
            if checker(song):
                results.append(
                    MinimalSongData(
                        song.songID,
                        self.clean(song.lyrics),
                        song.featuredArtists,
                        song.primaryArtist,
                        song.fullTitle,
                        song.releaseDateComponents
                    )
                )

        return results

    def searchLyricsViaAPI(self, lyrics: str, pageNR: int | None = None) -> None:
        if self.forceOffline:
            raise Exception("Cannot use the API offline. Please disable --force-offline.")

        rawData = self.geniusClient.search_lyrics(lyrics, per_page=50, page=pageNR)

        for section in rawData["sections"]:
            for hit in section["hits"]:
                result = hit["result"]

                primaryArtist = result["primary_artist"]
                artistID = primaryArtist["id"]
                artistName = primaryArtist["name"]
                artistImage = primaryArtist["image_url"]
                songID = result["id"]

                featuredArtists = [
                    Artist(
                        artist["id"],
                        artist["name"],
                        artist["image_url"]
                    )
                    for artist in hit["result"]["featured_artists"]
                ]

                actualLyrics = self.geniusClient.lyrics(song_url=result["url"])

                msd = MinimalSongData(
                    songID,
                    self.clean(actualLyrics),
                    featuredArtists,
                    Artist(
                        artistID,
                        artistName,
                        artistImage
                    ),
                    hit["result"]["full_title"],
                    hit["result"]["release_date_components"]
                )

                self.cachedSongs.append(msd)

    @staticmethod
    def loadFromCache(genius: lyricsgenius.Genius, forceOffline: bool = False) -> CachedGenius:
        with open("lyricsCache.json", "rb") as handle:
            dumpedData = json.loads(handle.read())

        fullCache = set()

        for song in dumpedData:
            fullCache.add(MinimalSongData(
                song["songID"],
                song["lyrics"],
                [
                    Artist(
                        artist["id"],
                        artist["name"],
                        artist["imageURL"]
                    )
                    for artist in song["featuredArtists"]
                ],
                Artist(
                    song["primaryArtist"]["id"],
                    song["primaryArtist"]["name"],
                    song["primaryArtist"]["imageURL"]
                ),
                song["fullTitle"],
                song["releaseDateComponents"]
            ))

        logger.debug(f"Loaded {len(fullCache)} songs")

        return CachedGenius(genius, list(fullCache), forceOffline)

    def clean(self, lyrics: str) -> str:
        new_lines = ""
        
        for line in lyrics.splitlines(True):
            if "[" not in line or line.startswith("["):
                new_lines += line
                continue
            new_lines += "\n" + line[line.index("["):]

        if new_lines.endswith("Embed"):
            new_lines = new_lines[:-5]

        return new_lines

    def save(self) -> None:
        dumpableData = []
        songIDs = []

        for song in self.cachedSongs:
            if song.songID in songIDs:
                continue

            songIDs.append(song.songID)

            dumpableData.append({
                "songID": song.songID,
                "lyrics": song.lyrics,
                "featuredArtists": [
                    {
                        "id": artist.artistID,
                        "name": artist.name,
                        "imageURL": artist.imageURL
                    }
                    for artist in song.featuredArtists
                ],
                "primaryArtist": {
                    "id": song.primaryArtist.artistID,
                    "name": song.primaryArtist.name,
                    "imageURL": song.primaryArtist.imageURL
                },
                "fullTitle": song.fullTitle,
                "releaseDateComponents": song.releaseDateComponents
            })

        with open("lyricsCache.json", "w") as handle:
            json.dump(dumpableData, handle)
