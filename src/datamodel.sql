CREATE TABLE torrent (
    hash        CHAR(40)        NOT NULL PRIMARY KEY,
    name        VARCHAR
);

CREATE TABLE top (
    date        TIMESTAMP       NOT NULL PRIMARY KEY,
    name        VARCHAR
);

CREATE TABLE top_entry (
    id              INTEGER     NOT NULL PRIMARY KEY,
    torrent_hash    CHAR(40)    NOT NULL,
    top_date        TIMESTAMP   NOT NULL,
    rank            INTEGER     NOT NULL,
    dlcount         INTEGER     NOT NULL,
    
    FOREIGN KEY(torrent_hash) REFERENCES torrent(hash),
    FOREIGN KEY(top_date) REFERENCES top(date)
);
