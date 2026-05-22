from flask import Flask, jsonify, request, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL 연결 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234', # 본인의 비밀번호로 변경
    'database': 'shop_db',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """데이터베이스 커넥션을 반환합니다."""
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    # 프론트엔드 HTML 페이지를 렌더링합니다.
    return render_template('index.html')

# [READ] 전체 상품 조회 API
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) # dictionary=True로 설정하면 dict 형태로 결과 반환
        cursor.execute("SELECT * FROM products ORDER BY id DESC")
        products = cursor.fetchall()
        return jsonify(products), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# [CREATE] 상품 등록 API
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"message": "필수 입력 값이 누락되었습니다."}), 400
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO products (name, price, description) VALUES (%s, %s, %s)"
        values = (data['name'], data['price'], data.get('description', ''))
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "상품이 등록되었습니다.", "id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# [UPDATE] 상품 수정 API
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "UPDATE products SET name = %s, price = %s, description = %s WHERE id = %s"
        values = (data['name'], data['price'], data.get('description', ''), product_id)
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"message": "상품 정보가 수정되었습니다."}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# [DELETE] 상품 삭제 API
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM products WHERE id = %s"
        cursor.execute(sql, (product_id,))
        conn.commit()
        return jsonify({"message": "상품이 삭제되었습니다."}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)