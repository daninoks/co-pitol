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

from pilotCore.handlers.driver import manage_data as driver_data


class AdminUserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


# Users model:
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

    #### Extra (need_to_be_deleted)
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




# Driver models:
class Driver(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True, editable=False)  # telegram_id
    username = models.CharField(max_length=32, editable=False, **nb)
    mobile_number = models.PositiveBigIntegerField(default=0, editable=True)

    car_model = models.CharField(max_length=32, default=None, **nb)
    car_seats = models.PositiveSmallIntegerField(default=0, **nb)
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
        d, created = cls.objects.get_or_create(user_id=data.get('user_id'))
        return d, created

    @classmethod
    def get_d_by_user_id(cls, passed_user_id) -> User:
        d = cls.objects.get(user_id=passed_user_id)
        return d

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
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField(editable=False)  # telegram_id
    username = models.CharField(max_length=32, editable=False, **nb)

    ride_id = models.CharField(max_length=32, editable=False)
    departure_time = models.CharField(max_length=32, default=None, **nb)
    direction = models.TextField(default=None, **nb)

    seats_booked = models.PositiveSmallIntegerField(default=0, editable=False)
    
    car_seats = models.PositiveSmallIntegerField(default=0, editable=False)

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
    def create_new_ride_id(cls, update: Update, context: CallbackContext):
        """
        Creating new ride id:
        """
        data = extract_user_data_from_update(update)
        try:
            #print('existing RIDE_ID')
            drList = list(
                cls.objects.filter(
                    user_id=data.get('user_id')
                ).values('ride_id').order_by('ride_id')
            )
            if update.callback_query.data == driver_data.MY_RIDES_NEW_BUTTON:
                #print('new RIDE_ID')
                mr_prefix = re.search('\d*$', drList[-1].get('ride_id'))
                max_ride_id = re.sub(f'_{mr_prefix[0]}', f'_{int(mr_prefix[0]) + 1}', drList[-1].get('ride_id'))
            else:
                max_ride_id = drList[-1].get('ride_id')
        except (AttributeError, IndexError) as e:
            #print(e)
            max_ride_id = 'ORD_' + str(data.get('user_id')) + '_0'
        d, _ = Driver.get_or_create_user(update, context)
        
        du, _ = DriverUtils.get_or_create_user(update, context)
        du.new_ride_id = max_ride_id
        du.save()
        
        dr, created = cls.objects.get_or_create(
            user_id=data.get('user_id'), 
            ride_id=max_ride_id,
            car_seats=d.car_seats
        )
        return dr, created

    @classmethod
    def get_dr_by_ride_id(cls, passed_ride_id):
        dr = cls.objects.get(ride_id=passed_ride_id)
        return dr
        
    @classmethod
    def new_time(cls, ride_id: str, field_data: str) -> str:
        # dr, _ = cls.get_or_create_user(update, context)
        dr = cls.get_dr_by_ride_id(ride_id)
        
        if m := re.match('(\d{2})([:-]|(?=.))(\d{2})', field_data):
            dr.departure_time = f'{m[1]}:{m[3]}'
            dr.save()
        return dr.departure_time

    @classmethod
    def delete_ride(cls, update: Update, context: CallbackContext) -> str:
        # dr, ex = cls.get_field_by_ride_id(update, context)
        du, _ = DriverUtils.get_or_create_user(update, context)
        data = extract_user_data_from_update(update)
        dr, created = cls.objects.get_or_create(user_id=data.get('user_id'), ride_id=du.selected_ride_id)
        ride_id = dr.ride_id
        #print(dr)
        #print(created)
        if created:
            msg = f'Warning: SOmething went wrong. Field with ID: {ride_id} just created!'
        else:
            dr.delete()
            msg = f'Ride with ID: {ride_id} Deleted!'
        return msg

    @classmethod
    def edit_time(cls, update: Update, context: CallbackContext, field_data: str, ride_id: int) -> str:
        dr, _ = cls.get_user_by_ride_id(update, context)
        if m := re.match('(\d{2}[:,-]\d{2})|(\d{4})', field_data):
            m1 = re.match('\d{2}', m[0])
            dr.departure_time = f'{m1[0]}:{m1[1]}'
            dr.save()
        return dr.departure_time

    # Directions:
    @classmethod
    def add_direction(cls, ride_id: str, field_data) -> Optional[DriverRides]:
        dr = cls.get_dr_by_ride_id(ride_id)
        dr.direction = (
            f' -> {field_data}' if dr.direction is None
            else f'{dr.direction} -> {field_data}'
        )
        dr.save()
        return dr

    @classmethod
    def remove_last_direction(cls, ride_id) -> Optional[DriverRides]:
        dr = cls.get_dr_by_ride_id(ride_id)
        deleted_direction = re.sub(' -> ([a-zA-Z]\w+)$', '', dr.direction)
        dr.direction = deleted_direction
        dr.save()
        return dr




class DriverUtils(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True, editable=False)      # telegram_id
    last_msg_id = models.PositiveBigIntegerField(default=0, editable=False)
    myrides_page = models.PositiveSmallIntegerField(default=0, editable=False)
    selected_ride_id = models.CharField(max_length=32, editable=False)
    new_ride_id = models.CharField(max_length=32, null=True, editable=False)

    @classmethod
    def get_or_create_user(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        data = extract_user_data_from_update(update)
        du, created = cls.objects.get_or_create(user_id=data["user_id"])
        return du, created

    @classmethod
    def set_last_msg_id(cls, update: Update, context: CallbackContext) -> Optional[int]:
        du, _ = cls.get_or_create_user(update, context)
        du.last_msg_id = update.callback_query.message.message_id
        du.save()
        return du.last_msg_id

    @classmethod
    def set_myride_page(cls, duObj: object, pages: int, inc_value: int) -> Optional[int]:
        page = scrolling_row.scroll_layout_model_page(duObj, 'myrides_page', pages, inc_value)
        return page




# Customer models:
class Customer(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True, editable=False)  # telegram_id
    username = models.CharField(default=None, max_length=32, editable=False, **nb)
    real_name= models.CharField(default=None, max_length=32, editable=False, **nb)
    mobile_number = models.BigIntegerField(default=0, editable=True)

    CSTMR_ACCEPTED = 'ACCEPTED'
    CSTMR_PENDING = 'PENDING'
    CSTMR_BANNED = 'BANNED'
    CSTMR_STATE = [
        (CSTMR_ACCEPTED, 'Accepted'),
        (CSTMR_PENDING, 'Pending'),
        (CSTMR_BANNED, 'Banned')
    ]
    registred = models.CharField(
        max_length=8,
        choices=CSTMR_STATE,
        default=CSTMR_PENDING
    )

    @classmethod
    def get_or_create_user(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        data = extract_user_data_from_update(update)
        c, created = cls.objects.get_or_create(user_id=data["user_id"])
        return c, created

    @classmethod
    def update_field(cls, update: Update, context: CallbackContext, field: dict) -> Optional[Driver]:
        c, _ = cls.get_or_create_user(update, context)
        setattr(c, field.get('name'), field.get('data'))
        c.save()
        return c



class CustomerRides(CreateUpdateTracker):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField(editable=False)  # telegram_id
    username = models.CharField(max_length=32, editable=False, **nb)

    ride_from = models.TextField(default=None, **nb)
    ride_to = models.TextField(default=None, **nb)

    ride_id_booked = models.CharField(default=None, null=True, max_length=32, editable=False)
    seats_booked = models.PositiveSmallIntegerField(default=1, editable=False)

    CRIDE_OPEN = 'OPEN'
    CRIDE_CLOSED = 'CLOSED'
    CRIDE_STATE = [
        (CRIDE_OPEN, 'Open'),
        (CRIDE_CLOSED, 'Closed')
    ]
    status = models.CharField(
        max_length=6,
        choices=CRIDE_STATE,
        default=CRIDE_OPEN
    )

    @classmethod
    def get_or_create_user(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        data = extract_user_data_from_update(update)
        du, created = cls.objects.get_or_create(user_id=data["user_id"])
        return du, created


class CustomerUtils(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True, editable=False)      # telegram_id
    last_msg_id = models.PositiveBigIntegerField(default=0, editable=False)
    myrides_page = models.PositiveSmallIntegerField(default=0, editable=False)
    selected_ride_id = models.CharField(max_length=32, editable=False)

    @classmethod
    def get_or_create_user(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        data = extract_user_data_from_update(update)
        du, created = cls.objects.get_or_create(user_id=data["user_id"])
        return du, created

    @classmethod
    def set_last_msg_id(cls, update: Update, context: CallbackContext) -> Optional[int]:
        du, _ = cls.get_or_create_user(update, context)
        du.last_msg_id = update.callback_query.message.message_id
        du.save()
        return du.last_msg_id

    @classmethod
    def set_myride_page(cls, duObj: object, pages: int, inc_value: int) -> Optional[int]:
        page = scrolling_row.scroll_layout_model_page(duObj, 'myrides_page', pages, inc_value)
        return page









# Orders models:
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
