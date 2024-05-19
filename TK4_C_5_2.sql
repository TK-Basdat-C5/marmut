CREATE OR REPLACE FUNCTION update_user_playlist_attributes() RETURNS TRIGGER AS $$
BEGIN
    -- Update total_durasi and jumlah_lagu for the playlist
    UPDATE user_playlist
    SET 
        total_durasi = (
            SELECT COALESCE(SUM(konten.durasi), 0)
            FROM playlist_song 
            JOIN song ON playlist_song.id_song = song.id_konten
            JOIN konten ON song.id_konten = konten.id
            WHERE playlist_song.id_playlist = NEW.id_playlist
        ),
        jumlah_lagu = (
            SELECT COUNT(*)
            FROM playlist_song
            WHERE playlist_song.id_playlist = NEW.id_playlist
        )
    WHERE user_playlist.id_playlist = NEW.id_playlist;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_user_playlist_attributes_trigger
AFTER INSERT OR DELETE ON playlist_song
FOR EACH ROW
EXECUTE FUNCTION update_user_playlist_attributes();


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
