PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
	first_name VARCHAR(50) NOT NULL, 
	last_name VARCHAR(50) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(128) NOT NULL, 
	is_admin BOOLEAN, 
	id VARCHAR(36) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO users VALUES('admin','admin','admin@test.com','$2b$12$e9PD7zm2zKZU0ByYfvaZyOmHKSYDtTDSEzCh5qatMDufjU9ienjQW',1,'c5bcd80a-29a2-4077-9718-e7a86af067cc','2025-11-22 10:38:38.089136','2025-11-22 10:38:38.089144');
INSERT INTO users VALUES('priam','demally','test@test.com','$2b$12$1VuEOHVJh49HLsx6tUOTle.LAXNzZPCKzGC9SGcXB2s5U0gXBOBsG',1,'cb52243e-9f49-454d-92d6-db00cc7348d0','2025-11-22 10:39:27.494541','2025-11-22 10:39:27.494548');
INSERT INTO users VALUES('sarah','wacquiez','test1@test.com','$2b$12$sNr2MuLeme3GIpvXbg8j5eGSe/80PTDOVXov29AsQYPYL3gMwi176',1,'10790d7f-a86b-4181-b2a8-326166a8535e','2025-11-22 10:39:47.059288','2025-11-22 10:39:47.059292');
INSERT INTO users VALUES('mus','chermat','test1e@test.com','$2b$12$M16Kb3tgdWgCfkM8urHoHO59o0wAxK0bvWVJ04IkXnF8Z0cYKqM6G',1,'d0d75396-7245-4928-a4da-8332b938f225','2025-11-22 10:40:13.129544','2025-11-22 10:40:13.129550');
INSERT INTO users VALUES('chris','saniez','teste1e@test.com','$2b$12$IM79nvXTrLCntYJEUKp8zOhXJA0iDOZ4gSeBQTOlF21x2ehkMmTxC',1,'995a734b-9e77-47a5-a549-fd40427a9df3','2025-11-22 10:41:09.591827','2025-11-22 10:41:09.591832');
CREATE TABLE amenities (
	name VARCHAR(50) NOT NULL, 
	id VARCHAR(36) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO amenities VALUES('Wifi','aeb17667-aa6a-4bee-bab1-4e8df4816afc','2025-11-22 10:44:34.239192','2025-11-22 10:44:34.239196');
INSERT INTO amenities VALUES('Clim','5717b10e-65f7-4d5a-ac55-56327af86089','2025-11-22 10:44:52.527471','2025-11-22 10:44:52.527476');
INSERT INTO amenities VALUES('Piscine','c692255e-7c2e-4372-b0aa-9be20ed90aa1','2025-11-22 10:45:02.204844','2025-11-22 10:45:02.204848');
INSERT INTO amenities VALUES('Parking','282c7c61-ae86-407e-8b88-63ba90b3724c','2025-11-22 10:45:12.671266','2025-11-22 10:45:12.671270');
INSERT INTO amenities VALUES('Petit-déjeuner','56a5c07a-f27b-4bcd-a829-75be93897576','2025-11-22 10:45:25.669423','2025-11-22 10:45:25.669428');
CREATE TABLE places (
	title VARCHAR(100) NOT NULL, 
	description VARCHAR(50), 
	price FLOAT NOT NULL, 
	latitude FLOAT NOT NULL, 
	longitude FLOAT NOT NULL, 
	owner_id VARCHAR NOT NULL, 
	id VARCHAR(36) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, image_url VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);
INSERT INTO places VALUES('Winchester Mystery House','Located in San Jose, California, the Winchester Mystery House is a labyrinthine mansion built by Sarah Winchester, heir to the Winchester rifles. The house is famous for its staircases that lead nowhere, doors opening into walls, and endless corridors. According to legend, Sarah Winchester designed this house to appease the spirits of the victims of Winchester rifles. Visitors report hearing mysterious footsteps and seeing shadows in the hallways.',50.0,37.3181999999999973,-121.950000000000002,'c5bcd80a-29a2-4077-9718-e7a86af067cc','f0c4a41f-899b-47f4-bae9-478f5e0248c6','2025-11-22 11:07:23.076681','2025-11-22 11:07:23.076687','images/winchesterHouse.png');
INSERT INTO places VALUES('Amityville Horror House','Located in Amityville, Long Island, this house became infamous after the 1974 DeFeo family murders. When the Lutz family moved in the following year, they reported extreme paranormal events including slamming doors, flying objects, and unseen presences. Audio and video recordings from the Lutzes captured strange voices and unexplained movements, further cementing the house’s terrifying reputation.',105.0,40.6664999999999992,-73.4141999999999939,'c5bcd80a-29a2-4077-9718-e7a86af067cc','c5bbd94a-dc8b-46ec-9097-c97baf517014','2025-11-22 16:36:57.206054','2025-11-22 16:36:57.206062','images/amityvilleHouse.png');
INSERT INTO places VALUES('Poveglia Haunted Island','Located near Venice, Italy, Poveglia Island served as a quarantine site for plague victims and later as a psychiatric hospital. Thousands of people died on the island, and legends say their spirits remain. Visitors have reported screams, ghostly apparitions, and eerie shadows lurking at night.',130.0,45.3870000000000004,12.3209999999999997,'c5bcd80a-29a2-4077-9718-e7a86af067cc','09e234ed-d64e-4734-a9e7-a28928407a52','2025-11-22 16:50:31.976890','2025-11-22 16:50:31.976898','images/poveglia.png');
INSERT INTO places VALUES('Borley Rectory','Located in Essex, England, Borley Rectory is considered the most haunted house in England, built on an old cemetery. Reported phenomena include a ghostly nun, footsteps, and mysterious letters. Paranormal investigators have recorded unexplained sounds and witnessed ghostly apparitions.',90.0,51.8489999999999966,0.850999999999999978,'c5bcd80a-29a2-4077-9718-e7a86af067cc','55476c5f-326b-47d9-9e8d-2197d7500d9c','2025-11-22 16:59:08.824536','2025-11-22 16:59:08.824544','images/borleyRectory.png');
INSERT INTO places VALUES('Stanley Hotel','Located in Estes Park, Colorado, the Stanley Hotel inspired Stephen King for ''The Shining''. Built in 1909, it is known for ghostly apparitions, unexplained noises, and rooms where objects move on their own. Visitors also report strange voices and eerie sensations in the hallways.',120.0,40.3701999999999969,-105.573300000000003,'c5bcd80a-29a2-4077-9718-e7a86af067cc','c693de07-4527-4374-b19f-550e8309be07','2025-11-22 17:09:12.286711','2025-11-22 17:09:12.286722','images/stanley_hotel.png');
CREATE TABLE place_amenity (
	place_id VARCHAR NOT NULL, 
	amenity_id VARCHAR NOT NULL, 
	PRIMARY KEY (place_id, amenity_id), 
	FOREIGN KEY(place_id) REFERENCES places (id), 
	FOREIGN KEY(amenity_id) REFERENCES amenities (id)
);
INSERT INTO place_amenity VALUES('f0c4a41f-899b-47f4-bae9-478f5e0248c6','c692255e-7c2e-4372-b0aa-9be20ed90aa1');
INSERT INTO place_amenity VALUES('f0c4a41f-899b-47f4-bae9-478f5e0248c6','5717b10e-65f7-4d5a-ac55-56327af86089');
INSERT INTO place_amenity VALUES('c5bbd94a-dc8b-46ec-9097-c97baf517014','aeb17667-aa6a-4bee-bab1-4e8df4816afc');
INSERT INTO place_amenity VALUES('c5bbd94a-dc8b-46ec-9097-c97baf517014','282c7c61-ae86-407e-8b88-63ba90b3724c');
INSERT INTO place_amenity VALUES('09e234ed-d64e-4734-a9e7-a28928407a52','56a5c07a-f27b-4bcd-a829-75be93897576');
INSERT INTO place_amenity VALUES('55476c5f-326b-47d9-9e8d-2197d7500d9c','282c7c61-ae86-407e-8b88-63ba90b3724c');
INSERT INTO place_amenity VALUES('55476c5f-326b-47d9-9e8d-2197d7500d9c','5717b10e-65f7-4d5a-ac55-56327af86089');
INSERT INTO place_amenity VALUES('c693de07-4527-4374-b19f-550e8309be07','c692255e-7c2e-4372-b0aa-9be20ed90aa1');
INSERT INTO place_amenity VALUES('c693de07-4527-4374-b19f-550e8309be07','282c7c61-ae86-407e-8b88-63ba90b3724c');
INSERT INTO place_amenity VALUES('c693de07-4527-4374-b19f-550e8309be07','aeb17667-aa6a-4bee-bab1-4e8df4816afc');
CREATE TABLE reviews (
	text VARCHAR NOT NULL, 
	rating INTEGER NOT NULL, 
	place_id VARCHAR(60) NOT NULL, 
	user_id VARCHAR(60) NOT NULL, 
	id VARCHAR(36) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(place_id) REFERENCES places (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO reviews VALUES('A fascinating and eerie experience! The house is full of mysterious passageways and quirky architecture. A must-see for anyone visiting San Jose.',5,'f0c4a41f-899b-47f4-bae9-478f5e0248c6','995a734b-9e77-47a5-a549-fd40427a9df3','cf2d4b49-272f-49a9-a581-ec6e180b8b3b','2025-11-23 21:21:10.755338','2025-11-23 21:21:10.755346');
INSERT INTO reviews VALUES('An eerie and unforgettable experience. The island’s dark history is palpable, and the atmosphere is truly haunting. A must-see for thrill-seekers!',5,'09e234ed-d64e-4734-a9e7-a28928407a52','10790d7f-a86b-4181-b2a8-326166a8535e','72a8abf7-4c85-4dee-b0a2-746ebf65917e','2025-11-24 00:01:23.603045','2025-11-24 00:01:23.603054');
COMMIT;
