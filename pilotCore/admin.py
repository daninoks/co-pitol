from django.contrib import admin


# from pilotCore.forms import ProfileForm
# from pilotCore.models import Profile
# from pilotCore.models import Message

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django_project.settings import DEBUG

from pilotCore.models import User, Driver, PrevMess


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name',
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", ]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'work_hours', 'direction',
        'car_model', 'car_seats', 'car_color', 'car_number'
    ]


@admin.register(PrevMess)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'mess_deleted',
    ]




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
