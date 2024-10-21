CREATE DATABASE gordys_novelties_db;

USE gordys_novelties_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role ENUM('user', 'admin') DEFAULT 'user'
);

CREATE TABLE gordys_novelties (
    id INT PRIMARY KEY,
    item TEXT,
    price INT,
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
INSERT INTO gordys_novelties VALUES 
(1, 'Settlers of Catan', 50, 'Mayfair Games', 3, 'board game'),
(2, 'Dragon Ball Super Monopoly', 40, 'USAopoly', 2, 'board game'),
(3, 'Stinky Pig', 10, 'Unknown', 4, 'dice game'),
(4, 'Splendor', 50, 'Space Cowboys', 5, 'card game'),
(5, 'Kami POP Figure', 30, 'Funko', 5, 'figure'),
(6, 'DC Comics Harley Quinn New 52 Bishoujo', 70, 'Kotobukiya', 7, 'figure'),
(7, 'King of Tokyo', 30, 'IELLO', 2, 'board game'),
(8, 'GBA Link Cable', 5, 'Hyperkin', 1, 'video game accessory'),
(9, 'Cat Headphones', 20, 'unknown', 2, 'audio equipment'),
(10, 'Zebra Mini Bluetooth Speaker', 40, 'unknown', 3, 'audio equipment'),
(11, 'Retron 3', 50, 'Hyperkin', 2, 'video game console'),
(12, 'Supaboy', 50, 'Hyperkin', 3, 'video game console'),
(13, 'Breaking Bad Monopoly', 40, 'USAopoly', 2, 'board game'),
(14, 'Judas Priest T-Shirt', 30, 'unknown', 2, 'board game'),
(15, 'Ads ICON blind box', 10, 'Funko', 8, 'figure');