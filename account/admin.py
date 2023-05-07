from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'first_name','last_name', 'phone_number', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
    ('User Credentials', {'fields': ('email', 'password', 'phone_number')}),
    ('Personal info', {'fields': ('first_name','last_name',)}),
    ('Permissions', {'fields': ('is_admin',)}),
)
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'first_name','last_name', 'phone_number', 'password', 'confirm_password'),
      }),
  )
  search_fields = ('email',)
  ordering = ('id','email')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)