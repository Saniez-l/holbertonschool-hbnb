-- Tests for CRUD methods
-- CREATE tests begin here
-- Creates Users
-- Commande lanch test: sqlite3 part3/hbnb/instance/development.db < part3/hbnb/app/sql/crud_tests.sql
INSERT INTO
    users (
        id,
        first_name,
        last_name,
        email,
        password,
        is_admin
    )
VALUES
    (
        LOWER(HEX(RANDOMBLOB(16))),
        'John',
        'Doe',
        'john.doe@example.com',
        '$2a$12$fJJObLxy/O4pTiv4.n839etfSomYkgtwNgQRhK.oJ0hFZqYfFV0zS',
        false
    ),
    (
        LOWER(HEX(RANDOMBLOB(16))),
        'Alice',
        'Smith',
        'alice.smith@example.com',
        '$2a$12$MQYx0wuPN0oUnqTS/VhIJO1Tl1l9huPVcUzzZ9lnTSFYRUyDYpvM.',
        false
    );

-- Verify users were created
SELECT
    *
FROM
    users;

-- Creates a Place
-- Simulates 'find user by email' method
INSERT INTO
    places (
        id,
        title,
        description,
        price,
        latitude,
        longitude,
        owner_id
    )
VALUES
    (
        LOWER(HEX(RANDOMBLOB(16))),
        'Cozy Beach House',
        'Clean, comfortable spot.',
        175.00,
        36.738,
        -112.47,
        (
            SELECT
                id
            FROM
                users
            WHERE
                email = 'john.doe@example.com'
        )
    );

-- Verify Place was created successfully
SELECT
    *
FROM
    places;

-- Create additional Amenities
INSERT INTO
    amenities (id, name)
VALUES
    (LOWER(HEX(RANDOMBLOB(16))), 'Dishwasher'),
    (LOWER(HEX(RANDOMBLOB(16))), 'Barbecue');

-- Verify Amenities were created successfully
SELECT
    *
FROM
    amenities;

-- Link Amenities to a Place
INSERT INTO
    place_amenity (place_id, amenity_id)
SELECT
    places.id,
    amenities.id
FROM
    places,
    amenities
WHERE
    places.title = 'Cozy Beach House'
    AND amenities.name IN ('WiFi', 'Dishwasher', 'Barbecue');

-- Verify amenities and place were linked correctly
SELECT
    *
FROM
    place_amenity;

-- Create a Review (from Alice about John's place)
INSERT INTO
    reviews (id, text, rating, user_id, place_id)
VALUES
    (
        LOWER(HEX(RANDOMBLOB(16))),
        'Very clean and comfortable place!',
        5,
        (
            SELECT
                id
            FROM
                users
            WHERE
                email = 'alice.smith@example.com'
        ),
        (
            SELECT
                id
            FROM
                places
            WHERE
                title = 'Cozy Beach House'
        )
    );

-- Verify Review was posted successfully
SELECT
    *
FROM
    reviews;

-- READ tests begin here
-- List all Users and their owned Places
-- Displays (null) if none owned
SELECT
    users.first_name,
    users.last_name,
    places.title
FROM
    users
    LEFT JOIN places ON users.id = places.owner_id;

-- Get all Reviews for a Place
SELECT
    places.title,
    reviews.text,
    reviews.rating,
    users.first_name,
    users.last_name
FROM
    reviews
    JOIN places ON reviews.place_id = places.id
    JOIN users ON reviews.user_id = users.id;

-- List all Amenities of a Place
SELECT
    places.title,
    amenities.name
FROM
    place_amenity
    JOIN places ON place_amenity.place_id = places.id
    JOIN amenities ON place_amenity.amenity_id = amenities.id;

-- UPDATE tests start here
-- Update a User's name
UPDATE users
SET
    first_name = 'Paul'
WHERE
    email = 'john.doe@example.com';

-- Verify User was updated successfully
SELECT
    *
FROM
    users;

-- Update the price of a Place
UPDATE places
SET
    price = 250.00
WHERE
    title = 'Cozy Beach House';

-- Verify Place was updated successfully
SELECT
    *
FROM
    places;

-- Update the rating in a Review
UPDATE reviews
SET
    rating = 4
WHERE
    text LIKE '%comfortable%';

-- Verify Review was updated successfully
SELECT
    *
FROM
    reviews;

-- DELETE tests begin here
-- Delete an Amenity (will remove from place_amenity due to cascade)
DELETE FROM amenities
WHERE
    name = 'Barbecue';

-- Verify Amenity was deleted successfully
SELECT
    *
FROM
    amenities;

-- Delete a place
-- (will remove related reviews &
-- place_amenity due to Cascade)
DELETE FROM places
WHERE
    title = 'Cozy Beach House';

-- Verify Place was deleted successfully
SELECT
    *
FROM
    places;

-- Deletes a Review
-- '0 rows affected' as the only Review created
-- was removed due to cascade from Place deletion
DELETE FROM reviews
WHERE
    text LIKE '%comfortable%';

-- Verify Review was deleted successfully
SELECT
    *
FROM
    reviews;

-- Verify place_amenity was deleted successfully
-- through Cascade, not a DELETE action
SELECT
    *
FROM
    place_amenity;