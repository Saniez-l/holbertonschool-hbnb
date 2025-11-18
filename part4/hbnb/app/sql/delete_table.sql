PRAGMA foreign_keys = OFF;

DELETE FROM reviews;
DELETE FROM place_amenity;
DELETE FROM places;
DELETE FROM amenities;
DELETE FROM users;

PRAGMA foreign_keys = ON;
