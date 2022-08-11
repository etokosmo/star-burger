from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
                .filter(availability=True)
                .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):

    def unprocessed(self):
        unprocessed_orders = self.exclude(status=Order.DONE).order_by('-status', 'registrated_at')
        return unprocessed_orders

    def get_available_restaurants(self):
        for order in self:
            products = [order_elements.product for order_elements in
                        order.order_elements.select_related('product')]

            product_restaurants = {}
            for product in products:
                restaurants = [item.restaurant for item in
                               product.menu_items.filter(
                                   availability=True).select_related(
                                   'restaurant')]
                product_restaurants[product] = restaurants
            order.restaurants = set.intersection(
                *[set(restaurants) for restaurants in
                  product_restaurants.values()])
        return self


class Order(models.Model):
    UNPROCCESSED = 'UP'
    IN_WORK = 'IW'
    IN_DELIVERY = 'ID'
    DONE = 'DN'
    STATUS_CHOICES = [
        (UNPROCCESSED, 'Необработанный'),
        (IN_WORK, 'Готовится'),
        (IN_DELIVERY, 'Доставка'),
        (DONE, 'Выполнен'),
    ]
    PAYMENT_CHOICES = [
        ('CARD', 'Электронно'),
        ('CASH', 'Наличностью'),
    ]
    firstname = models.CharField(verbose_name="Имя", max_length=50)
    lastname = models.CharField(verbose_name="Фамилия", max_length=50)
    phonenumber = PhoneNumberField(
        verbose_name="Номер телефона",
        db_index=True
    )
    address = models.CharField(
        verbose_name="Адрес",
        max_length=100,
        db_index=True
    )
    status = models.CharField(
        verbose_name="Статус заказа",
        max_length=2,
        choices=STATUS_CHOICES,
        default='Необработанный',
        db_index=True
    )
    payment = models.CharField(
        verbose_name="Способ оплаты",
        max_length=4,
        choices=PAYMENT_CHOICES,
        blank=True,
        null=True,
        db_index=True
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True
    )
    registrated_at = models.DateTimeField(
        verbose_name="Время регистрации заказа",
        default=timezone.now,
        db_index=True
    )
    called_at = models.DateTimeField(
        verbose_name="Время подтверждения заказа",
        blank=True,
        null=True,
        db_index=True
    )
    delivered_at = models.DateTimeField(
        verbose_name="Заказ доставлен в",
        blank=True,
        null=True,
        db_index=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Готовящий ресторан',
        related_name='orders',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.address}"


class OrderElements(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        related_name='order_elements',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Количество товара",
        related_name='order_elements',
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество товара",
        validators=[MinValueValidator(1)]
    )
    price_in_order = models.DecimalField(
        verbose_name="Стоимость в заказе",
        max_digits=10,
        decimal_places=1,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.product} {self.order}'
