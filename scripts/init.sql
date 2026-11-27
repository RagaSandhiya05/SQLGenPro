-- SQLGenPro: Food Delivery Database

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY,
    restaurant_name VARCHAR(150) NOT NULL,
    cuisine VARCHAR(100),
    city VARCHAR(100),
    rating DECIMAL(2,1)
);

CREATE TABLE menu_items (
    item_id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(restaurant_id),
    item_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    restaurant_id INTEGER REFERENCES restaurants(restaurant_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    total_amount DECIMAL(10,2)
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    item_id INTEGER REFERENCES menu_items(item_id),
    quantity INTEGER NOT NULL,
    subtotal DECIMAL(10,2)
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    amount DECIMAL(10,2)
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    restaurant_id INTEGER REFERENCES restaurants(restaurant_id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample users
INSERT INTO users (name, email, city) VALUES
('Arun', 'arun@example.com', 'Coimbatore'),
('Priya', 'priya@example.com', 'Chennai'),
('Karthik', 'karthik@example.com', 'Bangalore'),
('Divya', 'divya@example.com', 'Coimbatore'),
('Rahul', 'rahul@example.com', 'Chennai');

-- Sample restaurants
INSERT INTO restaurants
(restaurant_name, cuisine, city, rating) VALUES
('Spice Garden', 'Indian', 'Coimbatore', 4.5),
('Urban Bites', 'Continental', 'Chennai', 4.2),
('Pizza Corner', 'Italian', 'Bangalore', 4.0),
('Green Bowl', 'Healthy', 'Coimbatore', 4.7);

-- Sample menu items
INSERT INTO menu_items
(restaurant_id, item_name, category, price) VALUES
(1, 'Paneer Biryani', 'Main Course', 220),
(1, 'Chicken Biryani', 'Main Course', 280),
(2, 'Pasta Alfredo', 'Main Course', 250),
(2, 'Veg Burger', 'Fast Food', 150),
(3, 'Margherita Pizza', 'Pizza', 300),
(3, 'Farmhouse Pizza', 'Pizza', 380),
(4, 'Quinoa Bowl', 'Healthy', 200),
(4, 'Avocado Salad', 'Healthy', 180);

-- Sample orders
INSERT INTO orders
(user_id, restaurant_id, order_date, status, total_amount) VALUES
(1, 1, '2026-11-01 12:30:00', 'Delivered', 500),
(2, 2, '2026-11-02 13:00:00', 'Delivered', 400),
(3, 3, '2026-11-03 19:30:00', 'Delivered', 680),
(4, 4, '2026-11-04 11:00:00', 'Delivered', 380),
(5, 1, '2026-11-05 20:00:00', 'Pending', 280),
(1, 2, '2026-11-06 14:00:00', 'Delivered', 250),
(3, 4, '2026-11-07 12:00:00', 'Delivered', 200);

-- Order items
INSERT INTO order_items
(order_id, item_id, quantity, subtotal) VALUES
(1, 1, 1, 220),
(1, 2, 1, 280),
(2, 3, 1, 250),
(2, 4, 1, 150),
(3, 5, 1, 300),
(3, 6, 1, 380),
(4, 7, 1, 200),
(4, 8, 1, 180),
(5, 2, 1, 280),
(6, 3, 1, 250),
(7, 7, 1, 200);

-- Payments
INSERT INTO payments
(order_id, payment_method, payment_status, amount) VALUES
(1, 'UPI', 'Paid', 500),
(2, 'Card', 'Paid', 400),
(3, 'UPI', 'Paid', 680),
(4, 'Cash', 'Paid', 380),
(5, 'UPI', 'Pending', 280),
(6, 'Card', 'Paid', 250),
(7, 'UPI', 'Paid', 200);

-- Reviews
INSERT INTO reviews
(user_id, restaurant_id, rating, comment) VALUES
(1, 1, 5, 'Excellent food'),
(2, 2, 4, 'Good experience'),
(3, 3, 4, 'Nice pizza'),
(4, 4, 5, 'Healthy and delicious'),
(5, 1, 3, 'Could improve delivery');
