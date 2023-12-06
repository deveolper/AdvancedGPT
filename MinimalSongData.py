from Artist import Artist


class MinimalSongData:
    songID: int
    lyrics: str
    featuredArtists: list[Artist]
    primaryArtist = Artist
    fullTitle: str
    releaseDateComponents: dict[str, int]

    def __init__(
        self,
        songID: int,
        lyrics: str,
        featuredArtists: list[Artist],
        primaryArtist: Artist,
        fullTitle: str,
        releaseDateComponents: dict[str, int]
    ) -> None:
        self.songID = songID
        self.lyrics = lyrics
        self.featuredArtists = featuredArtists
        self.primaryArtist = primaryArtist
        self.fullTitle = fullTitle
        self.releaseDateComponents = releaseDateComponents

    def __str__(self) -> str:
        return (
            f"SongID: {self.songID}\n"
            f"Title: {self.fullTitle}\n"
            f"Primary Artist: {self.primaryArtist.name}\n"
            f"Featured Artists: {[artist.name for artist in self.featuredArtists]}\n"
            f"Release Date: {'-'.join(str(k) for k in (self.releaseDateComponents or {'': 'Unknown'}).values())}\n"
            f"Lyrics:\n{self.lyrics}"
        )
