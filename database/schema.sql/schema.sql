-- ============================================
-- ShopMetrics - E-Commerce Analytics
-- Phase 1: Journey Data Modeling
-

-- Create database
CREATE DATABASE IF NOT EXISTS shopmetrics;

-- Select database
USE shopmetrics;


-- ============================================
-- 1. USERS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    signup_date DATE
);


-- ============================================
-- 2. PRODUCTS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10,2)
);


-- ============================================
-- 3. CAMPAIGNS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id INT PRIMARY KEY,
    campaign_name VARCHAR(100),
    traffic_source VARCHAR(50)
);


-- ============================================
-- 4. SESSIONS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(50) PRIMARY KEY,
    user_id INT,
    session_start DATETIME,
    session_end DATETIME,
    traffic_source VARCHAR(50),
    device VARCHAR(50),
    city VARCHAR(100),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);


-- ============================================
-- 5. EVENTS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS events (
    event_id INT PRIMARY KEY,
    session_id VARCHAR(50),
    user_id INT,
    event_type VARCHAR(50),
    product_id INT,
    event_time DATETIME,

    FOREIGN KEY (session_id)
        REFERENCES sessions(session_id),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


-- ============================================
-- 6. ORDERS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    user_id INT,
    session_id VARCHAR(50),
    order_time DATETIME,
    total_amount DECIMAL(10,2),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (session_id)
        REFERENCES sessions(session_id)
);


-- ============================================
-- 7. ORDER ITEMS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY,
    order_id VARCHAR(50),
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);