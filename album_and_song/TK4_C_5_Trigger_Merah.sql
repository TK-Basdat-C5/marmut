-- Memperbarui durasi saat Menambahkan atau Menghapus Episode dalam Podcast:
-- Ketika Podcaster menambahkan atau menghapus episode dalam suatu podcast, 
-- sistem dapat memperbarui atribut durasi dari podcast tersebut dalam tabel KONTEN. 

CREATE OR REPLACE FUNCTION update_podcast_duration()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE KONTEN
    SET durasi = (
        SELECT COALESCE(SUM(durasi), 0) 
        FROM EPISODE
        WHERE id_konten_podcast = NEW.id_konten_podcast
    )
    WHERE id = NEW.id_podcast;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER trigger_add_delete_episode
AFTER INSERT OR DELETE ON EPISODE
FOR EACH ROW
EXECUTE FUNCTION update_podcast_duration();

-- Memperbarui Atribut Durasi dan Jumlah Lagu:
-- Ketika lagu ditambahkan atau dihapus dari album, diperlukan pembaruan
-- atribut total_durasi dan jumlah_lagu dari tabel ALBUM.

CREATE OR REPLACE FUNCTION update_album_info()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE ALBUM
    SET total_durasi = (
        SELECT COALESCE(SUM(K.durasi), 0)
        FROM SONG S, KONTEN K
        WHERE S.id_konten = K.id AND S.id_album = NEW.id_album
    ),
        jumlah_lagu = (
        SELECT COUNT(*)
        FROM SONG S
        WHERE S.id_album = NEW.id_album
    )
    WHERE id = NEW.id_album;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER trigger_add_delete_song
AFTER INSERT OR DELETE ON SONG
FOR EACH ROW
EXECUTE FUNCTION update_album_info();