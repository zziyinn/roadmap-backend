# 1. 导入 Flask 和 jsonify
from flask import Flask, jsonify

# 2. 创建 Flask 应用对象（核心）
app = Flask(__name__)

# 3. 定义一个路由（API endpoint），这是 RESTful 的关键
@app.route('/api/hello', methods=['GET'])  # pattern 模式：URL + HTTP方法
def hello_world():
    return jsonify(message="Hello, World!")  # 返回 JSON 格式的响应

# 4. 启动 Flask 服务
if __name__ == '__main__':
    app.run(debug=True)
