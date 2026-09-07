from decimal import Decimal
from app.db import init_db, SessionLocal
from app.models import Product, Customer, OwnerPreference

def seed():
    init_db()
    with SessionLocal() as db:
        if db.query(Product).count() == 0:
            products = [
                Product(name="Aashirvaad Atta 5kg", sku="ATT-AASH-5", unit="packet", quantity=20, reorder_level=5,
                        cost_price=Decimal("210"), sell_price=Decimal("245"), mrp=Decimal("250"), gst_rate=Decimal("5"), hsn="1101", loose=False),
                Product(name="Tata Salt 1kg", sku="SALT-TATA-1", unit="packet", quantity=35, reorder_level=8,
                        cost_price=Decimal("20"), sell_price=Decimal("28"), mrp=Decimal("30"), gst_rate=Decimal("5"), hsn="2501", loose=False),
                Product(name="Amul Butter 100g", sku="BUT-AMUL-100", unit="packet", quantity=18, reorder_level=5,
                        cost_price=Decimal("50"), sell_price=Decimal("58"), mrp=Decimal("62"), gst_rate=Decimal("12"), hsn="0405", loose=False),
                Product(name="Fortune Sunflower Oil 1L", sku="OIL-FORT-1", unit="litre", quantity=22, reorder_level=6,
                        cost_price=Decimal("110"), sell_price=Decimal("125"), mrp=Decimal("130"), gst_rate=Decimal("5"), hsn="1512", loose=False),
                Product(name="Maggi 70g", sku="MAGGI-70", unit="packet", quantity=60, reorder_level=15,
                        cost_price=Decimal("12"), sell_price=Decimal("14"), mrp=Decimal("14"), gst_rate=Decimal("12"), hsn="1902", loose=False),
                Product(name="Parle-G", sku="PARLEG", unit="packet", quantity=40, reorder_level=10,
                        cost_price=Decimal("8"), sell_price=Decimal("10"), mrp=Decimal("10"), gst_rate=Decimal("5"), hsn="1905", loose=False),
                Product(name="Surf Excel", sku="SURF-EXCEL", unit="packet", quantity=15, reorder_level=4,
                        cost_price=Decimal("45"), sell_price=Decimal("55"), mrp=Decimal("58"), gst_rate=Decimal("18"), hsn="3402", loose=False),
                Product(name="Rice", sku="RICE-LOOSE", unit="kg", quantity=100, reorder_level=20,
                        cost_price=Decimal("42"), sell_price=Decimal("50"), mrp=Decimal("50"), gst_rate=Decimal("0"), hsn="1006", loose=True),
                Product(name="Sugar", sku="SUGAR-LOOSE", unit="kg", quantity=70, reorder_level=15,
                        cost_price=Decimal("38"), sell_price=Decimal("45"), mrp=Decimal("45"), gst_rate=Decimal("0"), hsn="1701", loose=True),
                Product(name="Toor Dal", sku="DAL-TOOR", unit="kg", quantity=45, reorder_level=10,
                        cost_price=Decimal("110"), sell_price=Decimal("125"), mrp=Decimal("125"), gst_rate=Decimal("0"), hsn="0713", loose=True),
            ]
            db.add_all(products)
        if db.query(Customer).count() == 0:
            db.add_all([Customer(name="Ramesh", phone="9000000001"), Customer(name="Priya", phone="9000000002")])
        db.commit()
    print("Database seeded.")

if __name__ == "__main__":
    seed()
