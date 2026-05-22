-- 데이터베이스 생성 및 선택
CREATE DATABASE IF NOT EXISTS shop_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shop_db;

-- 테이블 생성 (DDL)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 샘플 데이터 삽입
INSERT INTO products (name, price, description) VALUES
('기계식 키보드', 120000, '갈축 무선 기계식 키보드입니다.'),
('버티컬 마우스', 89000, '손목 터널 증후군 예방을 위한 마우스입니다.'),
('4K 모니터', 350000, '32인치 고해상도 IPS 모니터입니다.');