# Clothing Store API

## Dependencies
1. Virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run.py:
```bash
python run.py
```

## Postman

### Brands
- GET http://127.0.0.1:5000/api/v1/marcas
- GET http://127.0.0.1:5000/api/v1/marcas/{id}
- POST http://127.0.0.1:5000/api/v1/marcas
  ```json
  {"nombre": "Nike"}
  ```
- PUT http://127.0.0.1:5000/api/v1/marcas/{id}
  ```json
  {"nombre": "Adidas"}
  ```
- DELETE http://127.0.0.1:5000/api/v1/marcas/{id}

### Pieces
- GET http://127.0.0.1:5000/api/v1/prendas
- GET http://127.0.0.1:5000/api/v1/prendas/{id}
- POST http://127.0.0.1:5000/api/v1/prendas
  ```json
  {"nombre": "Camiseta", "inventario": 100, "marca_id": "ID_DE_MARCA"}
  ```
- PUT http://127.0.0.1:5000/api/v1/prendas/{id}
  ```json
  {"nombre": "Camiseta", "inventario": 90, "marca_id": "ID_DE_MARCA"}
  ```
- DELETE http://127.0.0.1:5000/api/v1/prendas/{id}

### Sales
- GET http://127.0.0.1:5000/api/v1/ventas
- GET http://127.0.0.1:5000/api/v1/ventas/{id}
- POST http://127.0.0.1:5000/api/v1/ventas
  ```json
  {"cantidad": 5, "prenda_id": "ID_DE_PRENDA", "marca_id": "ID_DE_MARCA"}
  ```
- PUT http://127.0.0.1:5000/api/v1/ventas/{id}
  ```json
  {"cantidad": 3, "prenda_id": "ID_DE_PRENDA", "marca_id": "ID_DE_MARCA"}
  ```
- DELETE http://127.0.0.1:5000/api/v1/ventas/{id}

### Reports
- GET http://127.0.0.1:5000/api/v1/reportes/marcas-con-ventas
- GET http://127.0.0.1:5000/api/v1/reportes/prendas-vendidas-con-inventario
- GET http://127.0.0.1:5000/api/v1/reportes/cinco-marcas-mas-vendidas
```
