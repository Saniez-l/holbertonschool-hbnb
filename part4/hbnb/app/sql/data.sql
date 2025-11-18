INSERT INTO users (
    id, first_name, last_name, email, password, is_admin
)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2a$12$pPIznr1L5mygg2OnvyUKWeqU/xeUIswVVg4WxSEW618zqwQCjZVka',
    1
);


INSERT INTO amenities (id, name) VALUES
('1de40f87-4c01-47ce-a788-6562f06f32d4', 'WiFi'),
('4f2987a7-c3c5-4a2f-932d-dbc68defe119', 'Swimming Pool'),
('6a98acf9-a4e9-4673-b0a7-cfe1107a9b1b', 'Air Conditioning');