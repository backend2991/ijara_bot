from django.contrib import admin

from .models import Register, Book, Comment, Bookimage

class RegisterAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name', 'year', 'email']
    search_fields = ['username', 'last_name', 'first_name', 'year']

admin.site.register(Register, RegisterAdmin)

admin.site.register(Bookimage)

class BookAdminInline(admin.StackedInline):
    model = Bookimage
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'author', 'nashriyot']
    search_fields = ['name']
    inlines = [BookAdminInline,]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'book', 'created_at'] 
    list_filter = ['created_at', 'full_name']           
    search_fields = ['text', 'full_name']  



