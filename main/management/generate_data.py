from django.core.management.base import BaseCommand
from main.models import Client, Car, Sale, BODY_TYPE_CHOICES, DRIVE_UNIT_CHOICES, GEARBOX_CHOICES, FUEL_TYPE_CHOICES
import random
from django.utils import timezone

CAR_MODELS_IMAGES = {
            "BMW X7": 'bmw_x7.jpg',
            "GEELY MONJARO": 'geely_monjaro.jpg',
            "MB Gelendewagen": 'gelandewagen.jpg',
            "HYUNDAI Sonata": 'hyundai_sonata.jpg',
            "LEXUS LX600": 'lexus_lx600.jpg',
            "MB S-Class": 'mb_s_classe.jpg',
            "TOYOTA Camry": 'toyota_camry.jpg',
            "TOYOTA Prius": 'toyota_prius.jpeg',
            "LADA Vesta": 'vesta_sw_cross.jpg',
            "VOLVO XC90": 'volvo_xc90.jpg',
        }


class Command(BaseCommand):
    help = 'Создает тестовые данные для моделей Client, Car и Sale'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=3, help='Количество записей для каждой модели (по умолчанию 3)')

    def handle(self, *args, **options):
        count = options['count']

        # Создание тестовых клиентов
        for i in range(count):
            Client.objects.create(
                name=random.choice(["Иван", "Петр", "Стапан", "Николай", "Федор"]),
                last_name=random.choice(["Иванов", "Петров", "Кузнецов", "Голубев", "Нечаев"]),
                middle_name=random.choice(["Иванович", "Петрович", "Аркадьевич", "Николаевич", "Федорович"]),
                date_of_birth=timezone.now() - timezone.timedelta(days=random.randint(3650, 10000)),
                phone_number=f'+420{random.randint(1000000, 9999999)}'
            )

        # Создание тестовых автомобилей
        for i in range(count):
            car_model = random.choice(list(CAR_MODELS_IMAGES.keys()))
            car_year = 2023 - i
            car_color = random.choice(['Серебристый', 'Белый', 'Черный', 'Синий', 'Красный'])
            car_mileage = random.randint(5000, 150000)
            car_volume = random.choice([1.6, 1.8, 2.0])
            car_body_type = random.choice(BODY_TYPE_CHOICES)
            car_drive_unit = random.choice(DRIVE_UNIT_CHOICES)
            car_gearbox = random.choice(GEARBOX_CHOICES)
            car_fuel_type = random.choice(FUEL_TYPE_CHOICES)
            car_price = random.randint(1000000, 3500000)
            car_image = CAR_MODELS_IMAGES[car_model]

            Car.objects.create(
                model=car_model,
                year=car_year,
                color=car_color,
                mileage=car_mileage,
                volume=car_volume,
                body_type=car_body_type[0],
                drive_unit=car_drive_unit[0],
                gearbox=car_gearbox[0],
                fuel_type=car_fuel_type[0],
                price=car_price,
                image=car_image
            )

        # Создание тестовых продаж
        for i in range(count * 2):
            client = random.choice(Client.objects.all())
            car = random.choice(Car.objects.all())
            Sale.objects.create(
                client=client,
                car=car,
                created_at=timezone.now() - timezone.timedelta(days=random.randint(1, 365))
            )

        self.stdout.write(f'Создано {count} записей для каждой модели.')