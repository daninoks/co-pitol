from django.contrib import admin


# from pilotCore.forms import ProfileForm
# from pilotCore.models import Profile
# from pilotCore.models import Message

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django_project.settings import DEBUG

from pilotCore.models import User, Driver, Order, DriverRides, DriverUtils


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name',
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot"
    ]
    list_filter = ['is_blocked_bot', ]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']


# Driver models:
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'mobile_number',
        'car_model', 'car_seats', 'car_color', 'car_number',
        'registred'
    ]
    list_filter = ['registred', ]

@admin.register(DriverRides)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user_id', 'username',
        'ride_id', 'departure_time', 'direction',
        'seats_booked'
    ]

@admin.register(DriverUtils)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'last_msg_id', 'myrides_page', 'selected_ride_id'
    ]





# Order models:
@admin.register(Order)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'order_id', 'real_name', 'username', 'phone_number',
        'departure_time', 'travel_direction', 'seats',
        'comment', 'status', 'pointed'
    ]
    list_filter = ['status', 'departure_time']
    search_fields = ('order_id', 'departure_time', 'travel_direction')


    # def broadcast(self, request, queryset):
    #     """ Select users via check mark in django-admin panel, then select "Broadcast" to send message"""
    #     user_ids = queryset.values_list('user_id', flat=True).distinct().iterator()
    #     if 'apply' in request.POST:
    #         broadcast_message_text = request.POST["broadcast_text"]
    #
    #         if DEBUG:  # for test / debug purposes - run in same thread
    #             for user_id in user_ids:
    #                 _send_message(
    #                     user_id=user_id,
    #                     text=broadcast_message_text,
    #                 )
    #             self.message_user(request, f"Just broadcasted to {len(queryset)} users")
    #         else:
    #             broadcast_message.delay(text=broadcast_message_text, user_ids=list(user_ids))
    #             self.message_user(request, f"Broadcasting of {len(queryset)} messages has been started")
    #
    #         return HttpResponseRedirect(request.get_full_path())
    #     else:
    #         form = BroadcastForm(initial={'_selected_action': user_ids})
    #         return render(
    #             request, "admin/broadcast_message.html", {'form': form, 'title': u'Broadcast message'}
    #         )
