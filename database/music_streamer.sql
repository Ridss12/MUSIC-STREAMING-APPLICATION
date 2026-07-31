CREATE DATABASE IF NOT EXISTS music_streamer;

USE music_streamer;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    profile_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(100) NOT NULL,
    artist_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Albums (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    album_name VARCHAR(150) NOT NULL,
    artist_id INT,
    cover_image VARCHAR(255),
    release_date DATE,

    FOREIGN KEY (artist_id)
        REFERENCES Artists(artist_id)
        ON DELETE SET NULL
);

CREATE TABLE Songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    artist_id INT,
    album_id INT,
    genre VARCHAR(50),
    mood VARCHAR(50),
    duration INT,
    audio_url VARCHAR(500) NOT NULL,
    cover_image VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (artist_id)
        REFERENCES Artists(artist_id)
        ON DELETE SET NULL,

    FOREIGN KEY (album_id)
        REFERENCES Albums(album_id)
        ON DELETE SET NULL
);

CREATE TABLE Playlists (
    playlist_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    playlist_name VARCHAR(150) NOT NULL,
    description TEXT,
    cover_image VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE PlaylistSongs (
    playlist_song_id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (playlist_id)
        REFERENCES Playlists(playlist_id)
        ON DELETE CASCADE,

    FOREIGN KEY (song_id)
        REFERENCES Songs(song_id)
        ON DELETE CASCADE,

    UNIQUE (playlist_id, song_id)
);

CREATE TABLE LikedSongs (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (song_id)
        REFERENCES Songs(song_id)
        ON DELETE CASCADE,

    UNIQUE (user_id, song_id)
);

CREATE TABLE ListeningHistory (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (song_id)
        REFERENCES Songs(song_id)
        ON DELETE CASCADE
);

CREATE TABLE Downloads (
    download_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (song_id)
        REFERENCES Songs(song_id)
        ON DELETE CASCADE,

    UNIQUE (user_id, song_id)
);

CREATE TABLE UserPreferences (
    preference_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    favorite_genre VARCHAR(100),
    favorite_artist VARCHAR(100),
    preferred_language VARCHAR(50),
    preferred_theme VARCHAR(20) DEFAULT 'dark',

    FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE MoodHistory (
    mood_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    selected_mood VARCHAR(50) NOT NULL,
    selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
);
