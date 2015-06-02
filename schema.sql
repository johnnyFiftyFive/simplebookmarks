DROP TABLE IF EXISTS Folder;

CREATE TABLE Folder (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name   TEXT    NOT NULL,
    parent INTEGER,
    FOREIGN KEY (
        parent
    )
    REFERENCES Folder (id) 
);

DROP TABLE IF EXISTS Link;

CREATE TABLE Link (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    title  TEXT    NOT NULL,
    url    TEXT    NOT NULL,
    folder INTEGER,
    FOREIGN KEY (
        folder
    )
    REFERENCES Folder (id) 
);


