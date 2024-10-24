-- DROP DATABASE IF EXISTS gordys_novelties_db;
-- Just to reset everything to starting values
CREATE DATABASE gordys_novelties_db;

USE gordys_novelties_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role ENUM('user', 'admin') DEFAULT 'user'
);

CREATE TABLE gordys_novelties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item TEXT,
    price DECIMAL(10, 2),
    wholesaler TEXT,
    quantity INT,
    category TEXT
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES gordys_novelties(id)
);

-- Insert initial data into gordys_novelties
INSERT INTO gordys_novelties (item, price, wholesaler, quantity, category) VALUES 
('Settlers of Catan', 50.00, 'Mayfair Games', 3, 'board game'),
('Dragon Ball Super Monopoly', 40.00, 'USAopoly', 2, 'board game'),
('Stinky Pig', 10.00, 'Unknown', 4, 'dice game'),
('Splendor', 50.00, 'Space Cowboys', 5, 'card game'),
('Kami POP Figure', 30.00, 'Funko', 5, 'figure'),
('DC Comics Harley Quinn New 52 Bishoujo', 70.00, 'Kotobukiya', 7, 'figure'),
('King of Tokyo', 30.00, 'IELLO', 2, 'board game'),
('GBA Link Cable', 5.00, 'Hyperkin', 1, 'video game accessory'),
('Cat Headphones', 20.00, 'unknown', 2, 'audio equipment'),
('Zebra Mini Bluetooth Speaker', 40.00, 'unknown', 3, 'audio equipment'),
('Retron 3', 50.00, 'Hyperkin', 2, 'video game console'),
('Supaboy', 50.00, 'Hyperkin', 3, 'video game console'),
('Breaking Bad Monopoly', 40.00, 'USAopoly', 2, 'board game'),
('Judas Priest T-Shirt', 30.00, 'unknown', 2, 'board game'),
('Ads ICON blind box', 10.00, 'Funko', 8, 'figure');

ALTER TABLE orders ADD COLUMN status ENUM('pending', 'complete') DEFAULT 'pending';