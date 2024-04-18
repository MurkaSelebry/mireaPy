from faker import Faker
import random



fake = Faker('ru_RU')
# Создаем список фиктивных данных для каждой таблицы
drivers = [{"name_first": fake.first_name(), "name_second": fake.last_name(), "phone": fake.phone_number(), "email": fake.email(), "number_license": fake.random_int(min=1000000000, max=9999999999)} for _ in range(10)]
fares = [{"title": fake.word(), "description": fake.sentence()} for _ in range(10)]
cars = [{"brand": fake.word(), "model": fake.word(), "year_release": fake.year(), "color": fake.color_name(), "number_plate": fake.random_int(min=1000000000, max=9999999999)} for _ in range(10)]
clients = [{"name_first": fake.first_name(), "name_second": fake.last_name(), "phone": fake.phone_number(), "email": fake.email()} for _ in range(10)]
orders = [{"id_client": random.randint(1, 10), "id_driver": random.randint(1, 10), "address_source": fake.address(), "address_target": fake.address(), "id_fare": random.randint(1, 10)} for _ in range(10)]
order_details = [{"date_order": fake.date_time(), "payment_type": random.choice(['cash', 'card']), "cost": fake.random_int(min=10, max=100), "status": random.choice(['delivery', 'progress', 'done'])} for _ in range(10)]
rates = [{"id_order": random.randint(1, 10), "id_driver": random.randint(1, 10), "id_client": random.randint(1, 10), "rate_client": fake.random_int(min=1, max=5), "rate_driver": fake.random_int(min=1, max=5)} for _ in range(10)]

print(cars)