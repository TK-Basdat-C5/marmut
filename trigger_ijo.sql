CREATE OR REPLACE FUNCTION update_playlist_attributes()
RETURNS TRIGGER AS $$
DECLARE
    total_duration INT;
    total_songs INT;
BEGIN
    -- Calculate total duration of songs in the playlist
    SELECT SUM(K.durasi) INTO total_duration 
    FROM KONTEN K
    JOIN PLAYLIST_SONG PS ON K.id = PS.id_song
    WHERE PS.id_playlist = NEW.id_playlist;

    -- Count the number of songs in the playlist
    SELECT COUNT(*) INTO total_songs 
    FROM PLAYLIST_SONG
    WHERE id_playlist = NEW.id_playlist;

    -- Update total duration and number of songs in USER_PLAYLIST table
    UPDATE USER_PLAYLIST 
    SET total_durasi = total_duration, jumlah_lagu = total_songs
    WHERE id_user_playlist = NEW.id_playlist;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_playlist_attributes
AFTER INSERT OR DELETE ON PLAYLIST_SONG
FOR EACH ROW
EXECUTE FUNCTION update_playlist_attributes();

CREATE OR REPLACE FUNCTION check_duplicate_song_playlist()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM PLAYLIST_SONG
        WHERE id_playlist = NEW.id_playlist AND id_song = NEW.id_song
    ) THEN
        RAISE EXCEPTION 'Song already exists in the playlist.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_duplicate_song_playlist
BEFORE INSERT ON PLAYLIST_SONG
FOR EACH ROW
EXECUTE FUNCTION check_duplicate_song_playlist();

CREATE OR REPLACE FUNCTION check_duplicate_downloaded_song()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM DOWNLOADED_SONG
        WHERE id_song = NEW.id_song AND email_downloader = NEW.email_downloader
    ) THEN
        RAISE EXCEPTION 'Song has already been downloaded.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_duplicate_downloaded_song
BEFORE INSERT ON DOWNLOADED_SONG
FOR EACH ROW
EXECUTE FUNCTION check_duplicate_downloaded_song();
