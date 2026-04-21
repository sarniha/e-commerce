# 🛒 E-Commerce Backend API

A RESTful e-commerce backend built with **FastAPI** and **Pydantic**, featuring full CRUD operations, flexible filtering by query parameters, and robust data validation.

---

## 🚀 Features

- **Full CRUD Operations** — Create, Read, Update, and Delete for products, orders, and more
- **Query & Parameter Filtering** — Filter products by category, price range, availability, and other attributes via query parameters
- **Data Validation** — Request/response validation using Pydantic models
- **Fast & Async** — Built on FastAPI for high-performance async request handling
- **Auto-generated Docs** — Interactive Swagger UI and ReDoc available out of the box

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [Pydantic](https://docs.pydantic.dev/) | Data validation & serialization |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| Python 3.10+ | Language |

---

## 📁 Project Structure

```
e-commerce/
├── main.py               # App entry point
├── routers/              # Route handlers (products, orders, users, etc.)
├── models/               # Pydantic models / schemas
├── database.py           # Database connection & setup
├── requirements.txt      # Project dependencies
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/sarniha/e-commerce.git
cd e-commerce

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI** → [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc** → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔌 API Endpoints

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products` | Get all products |
| `GET` | `/products/{id}` | Get product by ID |
| `GET` | `/products?category=electronics&min_price=100` | Filter products by query params |
| `POST` | `/products` | Create a new product |
| `PUT` | `/products/{id}` | Update a product |
| `DELETE` | `/products/{id}` | Delete a product |

### Query Parameters (Filtering)

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | `string` | Filter by product category |
| `min_price` | `float` | Minimum price filter |
| `max_price` | `float` | Maximum price filter |
| `in_stock` | `bool` | Filter by stock availability |
| `sort_by` | `string` | Sort field (e.g. `price`, `name`) |

---

## ✅ Validation

All incoming data is validated using **Pydantic** models. Invalid requests return a structured `422 Unprocessable Entity` response with detailed error messages.

Example product schema:

```python
class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str
    in_stock: bool = True
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
