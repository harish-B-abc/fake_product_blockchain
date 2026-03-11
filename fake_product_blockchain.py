from flask import Flask, request, render_template_string
import hashlib
import datetime

app = Flask(__name__)

# ================= BLOCK =================
class Block:
    def __init__(self, index, timestamp, product_id, manufacturer, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.product_id = product_id
        self.manufacturer = manufacturer
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = (
            str(self.index)
            + str(self.timestamp)
            + self.product_id
            + self.manufacturer
            + self.previous_hash
        )
        return hashlib.sha256(data.encode()).hexdigest()


# ================= BLOCKCHAIN =================
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "GENESIS", "SYSTEM", "0")

    def product_exists(self, product_id):
        for block in self.chain:
            if block.product_id == product_id:
                return True
        return False

    def add_product(self, product_id, manufacturer):
        if self.product_exists(product_id):
            return False

        prev = self.chain[-1]
        new_block = Block(
            len(self.chain),
            datetime.datetime.now(),
            product_id,
            manufacturer,
            prev.hash
        )
        self.chain.append(new_block)
        return True

    def verify_product(self, product_id):
        for block in self.chain:
            if block.product_id == product_id:
                return True, block
        return False, None


blockchain = Blockchain()

# ================= STYLE =================
STYLE = """
<style>
body {
    font-family: Arial;
    background: #f4f6f8;
}
.container {
    width: 420px;
    margin: 60px auto;
    background: white;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
h2 {
    text-align: center;
}
input, button {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
}
button {
    background: #007bff;
    color: white;
    border: none;
    cursor: pointer;
}
button:hover {
    background: #0056b3;
}
a {
    display: block;
    text-align: center;
    margin-top: 15px;
    text-decoration: none;
}
.result {
    background: #eaeaea;
    padding: 15px;
    margin-top: 15px;
    border-radius: 5px;
}
</style>
"""

# ================= HOME =================
@app.route("/")
def home():
    return render_template_string("""
    {{ style | safe }}
    <div class="container">
        <h2>🔐 Fake Product Detection</h2>
        <a href="/add"><button>🏭 Manufacturer - Add Product</button></a>
        <a href="/verify"><button>🛒 Consumer - Verify Product</button></a>
    </div>
    """, style=STYLE)

# ================= ADD PRODUCT =================
@app.route("/add", methods=["GET", "POST"])
def add_product():
    result = ""

    if request.method == "POST":
        pid = request.form["product_id"]
        manu = request.form["manufacturer"]

        if blockchain.add_product(pid, manu):
            result = f"✅ Product <b>{pid}</b> added successfully."
        else:
            result = f"❌ Product <b>{pid}</b> already exists."

    return render_template_string("""
    {{ style | safe }}
    <div class="container">
        <h2>🏭 Add Product</h2>
        <form method="POST">
            <input name="product_id" placeholder="Product ID" required>
            <input name="manufacturer" placeholder="Manufacturer Name" required>
            <button>Add to Blockchain</button>
        </form>

        {% if result %}
        <div class="result">{{ result | safe }}</div>
        {% endif %}

        <a href="/">⬅ Back to Home</a>
    </div>
    """, style=STYLE, result=result)

# ================= VERIFY PRODUCT =================
@app.route("/verify", methods=["GET", "POST"])
def verify_product():
    result = ""

    if request.method == "POST":
        pid = request.form["product_id"]
        valid, block = blockchain.verify_product(pid)

        if valid:
            result = (
                "✅ <b>GENUINE PRODUCT</b><br><br>"
                f"<b>Product ID:</b> {block.product_id}<br>"
                f"<b>Manufacturer:</b> {block.manufacturer}<br>"
                f"<b>Timestamp:</b> {block.timestamp}<br>"
                f"<b>Block Hash:</b> {block.hash}"
            )
        else:
            result = "❌ <b>FAKE PRODUCT DETECTED!</b>"

    return render_template_string("""
    {{ style | safe }}
    <div class="container">
        <h2>🛒 Verify Product</h2>
        <form method="POST">
            <input name="product_id" placeholder="Enter Product ID" required>
            <button>Verify</button>
        </form>

        {% if result %}
        <div class="result">{{ result | safe }}</div>
        {% endif %}

        <a href="/">⬅ Back to Home</a>
    </div>
    """, style=STYLE, result=result)

# ================= MAIN =================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

