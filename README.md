# Luxury Watch Store API

پیاده‌سازی تمرین Django + Django REST Framework.

## راه‌اندازی در Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations store
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

پنل ادمین: http://127.0.0.1:8000/admin/

## APIها

- `GET /api/products/` — فهرست محصولات همراه نام برند و دسته‌بندی
- `GET /api/products/<slug>/` — جزئیات محصول، تصاویر، رنگ‌ها و کامنت‌ها؛ هر درخواست click_count را یک واحد زیاد می‌کند
- `GET /api/luxury-special/` — محصولات ویژه و لوکس موجود به همراه میانگین قیمت همان مجموعه
- `GET /api/me/wishlist/` — علاقه‌مندی‌های کاربر واردشده (Session یا Basic Auth)

برای endpoint علاقه‌مندی‌ها ابتدا یک Customer برای کاربر در پنل ادمین بسازید و رکوردهای WishList را اضافه کنید.

## نکات طراحی و بهینه‌سازی

- `BaseModel` و `SluggedMixinModel` به صورت abstract model تعریف شده‌اند.
- همه مدل‌ها timestampهای `created_at` و `updated_at` دارند.
- ارتباط‌های ForeignKey در لیست با `select_related` واکشی می‌شوند.
- روابط چندتایی جزئیات با `prefetch_related` واکشی می‌شوند.
- Wishlist روابط Product و Customer و User را با `select_related` واکشی می‌کند.
- میانگین قیمت محصولات لوکس با یک `aggregate(Avg(...))` محاسبه می‌شود.
- افزایش `click_count` با `F()` به شکل اتمیک در دیتابیس انجام می‌شود. `annotate` و `aggregate` برای محاسبه مقادیر هستند و ابزار مناسب افزایش شمارنده نیستند.

## نکته

برای تمرین و توسعه، `DEBUG=True` و SQLite تنظیم شده‌اند. قبل از انتشار واقعی، تنظیمات امنیتی و دیتابیس production را تغییر دهید.
