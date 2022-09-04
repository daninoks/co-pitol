from __future__ import annotations

import re

from typing import Union, Optional, Tuple

from telegram import Update
from telegram.ext import CallbackContext

from django_project.settings import DEBUG
from django.db import models
from django.db.models import QuerySet, Manager, Max

from pilotCore.handlers.utils.info import extract_user_data_from_update
from pilotCore.handlers.utils import scrolling_row
from pilotCore.handlers.order import broadcast
from utils.models import CreateUpdateTracker, nb, CreateTracker, GetOrNoneManager


class AdminUserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)



class User(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True, editable=False)  # telegram_id
    username = models.CharField(max_length=32, editable=False, **nb)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", **nb)
    deep_link = models.CharField(max_length=64, **nb)

    is_blocked_bot = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    objects = GetOrNoneManager()  # user = User.objects.get_or_none(user_id=<some_id>)
    admins = AdminUserManager()  # User.admins.all()

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def get_user_and_created(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data.get('user_id'), defaults=data)

        if created:
            # Save deep_link to User model
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data.get('user_id')).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext) -> User:
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> Optional[User]:
        """ Search user in DB, return User or None if not found """
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @classmethod
    def set_banned_true(cls, username_or_user_id: Union[str, int]) -> Optional[User]:
        """ Search user in DB, return User or None if not found """
        # username = str(username_or_user_id).replace("@", "").strip().lower()
        u = cls.get_user_by_username_or_user_id(username_or_user_id)
        u.is_blocked_bot = True
        u.save()
        return u

    @classmethod
    def set_banned_false(cls, username_or_user_id: Union[str, int]) -> Optional[User]:
        """ Search user in DB, return User or None if not found """
        # username = str(username_or_user_id).replace("@", "").strip().lower()
        u = cls.get_user_by_username_or_user_id(username_or_user_id)
        u.is_blocked_bot = False
        u.save()
        return u

    @property
    def invited_users(self) -> QuerySet[User]:
        return User.objects.filter(deep_link=str(self.user_id), created_at__gt=self.created_at)

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"



class Driver(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True, editable=False)  # telegram_id
    username = models.CharField(max_length=32, editable=False, **nb)
    mobile_number = models.PositiveBigIntegerField(editable=True, default=0)

    # work_hours = models.CharField(max_length=32, default=None, **nb)
    # direction = models.TextField(default=None, **nb)

    car_model = models.CharField(max_length=32, default=None, **nb)
    car_seats = models.PositiveSmallIntegerField(default=0)
    car_color = models.CharField(max_length=32, default=None, **nb)
    car_number = models.CharField(max_length=32,default=None, **nb)

    DRVR_ACCEPTED = 'ACCEPTED'
    DRVR_PENDING = 'PENDING'
    DRVR_BANNED = 'BANNED'
    DRVR_STATE = [
        (DRVR_ACCEPTED, 'Accepted'),
        (DRVR_PENDING, 'Pending'),
        (DRVR_BANNED, 'Banned')
    ]
    registred = models.CharField(
        max_length=8,
        choices=DRVR_STATE,
        default=DRVR_PENDING
    )

    @classmethod
    def get_or_create_user(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        d, exists = cls.objects.get_or_create(user_id=data.get('user_id'))
        return d, exists

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext) -> User:
        data = extract_user_data_from_update(update)
        d = cls.objects.filter(order_id=data.get('user_id')).first()
        return d

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> Optional[User]:
        """ Search user in DB, return User or None if not found """
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @classmethod
    def update_field(cls, update: Update, context: CallbackContext, field: dict) -> Optional[Driver]:
        d, _ = cls.get_or_create_user(update, context)
        setattr(d, field.get('name'), field.get('data'))
        d.save()
        return d




class DriverRides(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True, editable=False)  # telegram_id
    username = models.CharField(max_length=32, editable=False, **nb)

    ride_id = models.PositiveIntegerField(default=0, editable=False)
    departure_time = models.CharField(max_length=32, default=None, **nb)
    direction = models.TextField(default=None, **nb)

    seats_booked = models.PositiveSmallIntegerField(default=0, editable=False)

    RIDE_OPEN = 'OPEN'
    RIDE_CLOSED = 'CLOSED'
    RIDE_STATE = [
        (RIDE_OPEN, 'Open'),
        (RIDE_CLOSED, 'Closed')
    ]
    status = models.CharField(
        max_length=6,
        choices=RIDE_STATE,
        default=RIDE_OPEN
    )

    @classmethod
    def get_or_create_user(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        drList = list(cls.objects.filter(user_id=data.get('user_id')).order_by('ride_id').last().values('ride_id'))
        max_ride_id = drList[0].get('ride_id') + 1
        dr, exists = cls.objects.get_or_create(user_id=data.get('user_id'), ride_id=max_ride_id)
        return dr, exists

    @classmethod
    def get_user_by_ride_id(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        du, _ = DriverUtils.get_or_create_user(update, context)
        ride_id = du.selected_ride_id
        dr, exists = cls.objects.get_or_create(user_id=data.get('user_id'), ride_id=ride_id)
        return dr, exists

    @classmethod
    def new_time(cls, update: Update, context: CallbackContext, field_data: str, ride_id: int) -> str:
        dr, _ = cls.get_or_create_user(update, context)
        if m := re.match('(\d{2}[:,-]\d{2})|(\d{4})', field_data):
            m1 = re.match('\d{2}', m[0])
            dr.departure_time = f'{m1[0]}:{m1[1]}'
            dr.save()
        return dr.departure_time

    @classmethod
    def edit_time(cls, update: Update, context: CallbackContext, field_data: str, ride_id: int) -> str:
        dr, _ = cls.get_user_by_ride_id(update, context)
        if m := re.match('(\d{2}[:,-]\d{2})|(\d{4})', field_data):
            m1 = re.match('\d{2}', m[0])
            dr.departure_time = f'{m1[0]}:{m1[1]}'
            dr.save()
        return dr.departure_time



    # @classmethod
    # def add_direction(cls, field_data, update: Update, context: CallbackContext) -> Optional[DriverRides]:
    #     dr, _ = cls.get_or_create_user(update, context)
    #     dr.direction = (
    #         f' -> {field_data}' if dr.direction is None
    #         else f'{dr.direction} -> {field_data}'
    #     )
    #     dr.save()
    #     return dr
    #
    # @classmethod
    # def remove_direction(cls, field_data, update: Update, context: CallbackContext) -> Optional[DriverRides]:
    #     dr, _ = cls.get_or_create_user(update, context)
    #     deleted_direction = re.sub(f'-> {field_data}', '', dr.direction)
    #     dr.direction = deleted_direction
    #     dr.save()
    #     return dr
    #
    # @classmethod
    # def remove_last_direction(cls, update: Update, context: CallbackContext) -> Optional[DriverRides]:
    #     dr, _ = cls.get_or_create_user(update, context)
    #     deleted_direction = re.sub(' -> ([a-zA-Z]\w+)$', '', dr.direction)
    #     dr.direction = deleted_direction
    #     dr.save()
    #     return dr



class DriverUtils(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True, editable=False)      # telegram_id
    mess_deleted = models.PositiveSmallIntegerField(default=0, editable=False)      # number deleted Messages after entry_points to conversation
    # new_orders_num = models.PositiveSmallIntegerField(default=0, editable=False)
    # new_orders_page = models.PositiveSmallIntegerField(default=0, editable=False)
    # my_orders_num = models.PositiveSmallIntegerField(default=0, editable=False)
    # my_orders_page = models.PositiveSmallIntegerField(default=0, editable=False)
    last_msg_id = models.PositiveBigIntegerField(default=0, editable=False)
    myrides_page = models.PositiveSmallIntegerField(default=0, editable=False)
    selected_ride_id = models.PositiveIntegerField(default=0, editable=False)

    @classmethod
    def get_or_create_user(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        data = extract_user_data_from_update(update)
        du, exists = cls.objects.get_or_create(user_id=data["user_id"])
        return du, exists

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> DriverUtils:
        """ Search user in DB, return User or None if not found """
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()
        # return cls.objects.filter(user_id=int(username_or_user_id)).first()

    # @classmethod
    # def reset_counter(cls, update: Update, context: CallbackContext) -> None:
    #     du, _ = cls.get_or_create_user(update, context)
    #     du.mess_deleted = 0
    #     du.save()
    #
    # @classmethod
    # def inc_counter(cls, update: Update, context: CallbackContext) -> Optional[DriverUtils]:
    #     du, _  = cls.get_or_create_user(update, context)
    #     du.mess_deleted += 1
    #     du.save()
    #     return du

    # @classmethod
    # def set_new_orders_page(cls, update: Update, context: CallbackContext, value: int) -> Optional[int]:
    #     du, _ = cls.get_or_create_user(update, context)
    #     page = scrolling_row.scroll_layout_model_page(du, 'new_orders_page', 'new_orders_num', value)
    #     return page
    #
    # @classmethod
    # def set_new_orders_num(cls, update: Update, context: CallbackContext, value: int) -> Optional[int]:
    #     du, _ = cls.get_or_create_user(update, context)
    #     page = scrolling_row.scroll_layout_model_pages(du, 'new_orders_page', 'new_orders_num', value)
    #     return page
    #
    # @classmethod
    # def set_my_orders_page(cls, update: Update, context: CallbackContext, value: int) -> Optional[int]:
    #     du, _ = cls.get_or_create_user(update, context)
    #     page = scrolling_row.scroll_layout_model_page(du, 'my_orders_page', 'my_orders_num', value)
    #     return page
    #
    # @classmethod
    # def set_my_orders_num(cls, update: Update, context: CallbackContext, value: int) -> Optional[int]:
    #     du, _ = cls.get_or_create_user(update, context)
    #     page = scrolling_row.scroll_layout_model_pages(du, 'my_orders_page', 'my_orders_num', value)
    #     return page

    @classmethod
    def set_last_msg_id(cls, update: Update, context: CallbackContext) -> Optional[int]:
        du, _ = cls.get_or_create_user(update, context)
        du.last_msg_id = update.callback_query.message.message_id
        du.save()
        return du.last_msg_id

    @classmethod
    def set_myride_page(cls, update: Update, context: CallbackContext, pages: int, inc_value: int) -> Optional[int]:
        du, _ = cls.get_or_create_user(update, context)
        page = scrolling_row.scroll_layout_model_page(du, 'myrides_page', pages, value)
        return page



class Order(CreateUpdateTracker):
    order_id = models.PositiveIntegerField(default=0, editable=False)
    real_name = models.CharField(max_length=32, default=None, **nb)
    username = models.CharField(max_length=32, default=None, **nb)
    phone_number = models.PositiveIntegerField(default=None)
    departure_time = models.CharField(max_length=32, default=None, **nb)
    travel_direction = models.TextField(default=None, **nb)
    seats = models.PositiveSmallIntegerField(default=None)
    comment = models.TextField(default=None, **nb)

    ORD_OPEN = 'OPEN'
    ORD_PENDING = 'PENDING'
    ORD_CLOSED = 'CLOSED'
    ORDER_STATE = [
        (ORD_OPEN, 'Open'),
        (ORD_PENDING, 'Pending'),
        (ORD_CLOSED, 'Closed')
    ]
    status = models.CharField(
        max_length=7,
        choices=ORDER_STATE,
        default=ORD_OPEN
    )
    pointed = models.PositiveBigIntegerField(default=None,  **nb)    # driver_id


    def save(cls, *args, **kw):
        if cls.order_id == 0:
            # oders_count = Order.objects.count()
            # double check(issues in upper case):
            orders_len = len(list(Order.objects.values('order_id')))
            cls.order_id = orders_len + 1
            cathcer = broadcast.broadcast_new_order(cls, Driver, DriverUtils)
        return super(Order, cls).save(*args, **kw)

    @classmethod
    def get_order(cls, ord_id: int) -> Optional[Order]:
        o = cls.objects.filter(order_id=ord_id).first()
        return o

    @classmethod
    def link_order(cls, update: Update, context: CallbackContext, order_id: int) -> Optional[Order]:
        data = extract_user_data_from_update(update)
        o = cls.get_order(order_id)
        o.pointed = data["user_id"]
        o.status = cls.ORD_PENDING
        o.save()
        return o

    @classmethod
    def unlink_order(cls, update: Update, context: CallbackContext, order_id: int) -> Optional[Order]:
        data = extract_user_data_from_update(update)
        o = cls.get_order(order_id)
        o.pointed = None
        o.status = cls.ORD_OPEN
        o.save()
        return o
