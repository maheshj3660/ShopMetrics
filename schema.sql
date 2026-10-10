USE shopmetrics;

-- ============================================
-- SAMPLE USERS
-- ============================================

INSERT INTO users (user_id, signup_date) VALUES
(1, '2026-09-01'),
(2, '2026-09-02'),
(3, '2026-09-03'),
(4, '2026-09-04'),
(5, '2026-09-05');


-- ============================================
-- SAMPLE PRODUCTS
-- ============================================

INSERT INTO products (product_id, product_name, category, price) VALUES
(101, 'Laptop', 'Electronics', 55000.00),
(102, 'Wireless Mouse', 'Electronics', 800.00),
(103, 'Keyboard', 'Electronics', 1500.00),
(104, 'Headphones', 'Electronics', 2500.00),
(105, 'USB Cable', 'Accessories', 500.00);


-- ============================================
-- SAMPLE CAMPAIGNS
-- ============================================

INSERT INTO campaigns (campaign_id, campaign_name, traffic_source) VALUES
(1, 'Google Ads', 'Google'),
(2, 'Instagram Campaign', 'Instagram'),
(3, 'Email Campaign', 'Email');


-- ============================================
-- SAMPLE SESSIONS
-- ============================================

INSERT INTO sessions
(session_id, user_id, session_start, session_end, traffic_source, device, city)
VALUES
('S001', 1, '2026-09-10 10:00:00', '2026-09-10 10:15:00', 'Google', 'Mobile', 'Pune'),
('S002', 2, '2026-09-10 11:00:00', '2026-09-10 11:20:00', 'Instagram', 'Mobile', 'Mumbai'),
('S003', 3, '2026-09-10 12:00:00', '2026-09-10 12:30:00', 'Google', 'Desktop', 'Pune'),
('S004', 4, '2026-09-10 13:00:00', '2026-09-10 13:10:00', 'Email', 'Mobile', 'Nashik'),
('S005', 5, '2026-09-10 14:00:00', '2026-09-10 14:25:00', 'Instagram', 'Desktop', 'Mumbai');


-- ============================================
-- SAMPLE EVENTS
-- ============================================

INSERT INTO events
(event_id, session_id, user_id, event_type, product_id, event_time)
VALUES

-- Session 1: Product viewed → Cart → Order
(1, 'S001', 1, 'page_view', NULL, '2026-09-10 10:01:00'),
(2, 'S001', 1, 'product_view', 101, '2026-09-10 10:03:00'),
(3, 'S001', 1, 'add_to_cart', 101, '2026-09-10 10:05:00'),
(4, 'S001', 1, 'order', 101, '2026-09-10 10:12:00'),

-- Session 2: Product viewed → Cart → No order
(5, 'S002', 2, 'page_view', NULL, '2026-09-10 11:01:00'),
(6, 'S002', 2, 'product_view', 102, '2026-09-10 11:05:00'),
(7, 'S002', 2, 'add_to_cart', 102, '2026-09-10 11:10:00'),

-- Session 3: Product viewed → Order
(8, 'S003', 3, 'page_view', NULL, '2026-09-10 12:01:00'),
(9, 'S003', 3, 'product_view', 103, '2026-09-10 12:05:00'),
(10, 'S003', 3, 'order', 103, '2026-09-10 12:20:00'),

-- Session 4: Only page view
(11, 'S004', 4, 'page_view', NULL, '2026-09-10 13:01:00'),

-- Session 5: Product viewed → Cart → No order
(12, 'S005', 5, 'page_view', NULL, '2026-09-10 14:01:00'),
(13, 'S005', 5, 'product_view', 104, '2026-09-10 14:05:00'),
(14, 'S005', 5, 'add_to_cart', 104, '2026-09-10 14:10:00');


-- ============================================
-- SAMPLE ORDERS
-- ============================================

INSERT INTO orders
(order_id, user_id, session_id, order_time, total_amount)
VALUES
('O001', 1, 'S001', '2026-09-10 10:12:00', 55000.00),
('O002', 3, 'S003', '2026-09-10 12:20:00', 1500.00);


-- ============================================
-- SAMPLE ORDER ITEMS
-- ============================================

INSERT INTO order_items
(order_item_id, order_id, product_id, quantity, price)
VALUES
(1, 'O001', 101, 1, 55000.00),
(2, 'O002', 103, 1, 1500.00);