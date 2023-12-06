class Artist:
    artistID: int
    name: str
    imageURL: str

    def __init__(self, artistID: int, name: str, imageURL: str) -> None:
        self.artistID = artistID
        self.name = name
        self.imageURL = imageURL
