--1 

CREATE OR REPLACE FUNCTION ensure_non_premium_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM NONPREMIUM WHERE email = NEW.email) THEN
        INSERT INTO NONPREMIUM(email) VALUES (NEW.email);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ensure_non_premium_status
BEFORE INSERT ON AKUN
FOR EACH ROW
EXECUTE FUNCTION ensure_non_premium_status();

--2

CREATE OR REPLACE FUNCTION ensure_non_premium_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM NONPREMIUM WHERE email = NEW.email) THEN
        INSERT INTO NONPREMIUM(email) VALUES (NEW.email);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ensure_non_premium_status
BEFORE INSERT ON AKUN
FOR EACH ROW
EXECUTE FUNCTION ensure_non_premium_status();


CREATE TRIGGER update_premium_status
BEFORE UPDATE ON TRANSACTION
FOR EACH ROW
EXECUTE FUNCTION update_premium_status();

--3

CREATE OR REPLACE FUNCTION update_premium_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.timestamp_berakhir < CURRENT_TIMESTAMP THEN
        DELETE FROM PREMIUM WHERE email = NEW.email;
        IF NOT FOUND THEN
            RAISE NOTICE 'No premium record found for email %', NEW.email;
        END IF;
        INSERT INTO NONPREMIUM(email) VALUES (NEW.email);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_premium_status
BEFORE UPDATE ON TRANSACTION
FOR EACH ROW
EXECUTE FUNCTION update_premium_status();
