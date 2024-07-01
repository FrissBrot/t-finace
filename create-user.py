import hashlib
import dbfunctions as db

username = "1"
email = "1"
password = "1"

password_hash = hashlib.sha256(password.encode()).hexdigest()

print(password_hash)
query = ('INSERT INTO "user" ("username", "mail", "password", "active", "fullAccess") VALUES (\'%s\', \'%s\', \'%s\', true, true)'% (username,email,password_hash))
db.executeWithoutFetch(query)