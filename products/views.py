from django.shortcuts import render
from .models import Product, Color, Category, Brand
from django.views.generic import DetailView


def catalog(request):
    # Получаем параметры из GET-запроса
    query = request.GET.get('q')
    сategory_name = request.GET.get('department')
    color = request.GET.get('color')
    size = request.GET.get('size')
    sort_price = request.GET.get('sort_price')
    gender = request.GET.get('gender')
    brand_name = request.GET.get('brand')

    # Формируем начальный QuerySet
    products = Product.objects.all()

    # Фильтрация по категории
    if сategory_name:
        try:
            сategory = Category.objects.get(name=сategory_name)
            products = products.filter(category=сategory)
        except Category.DoesNotExist:
            # Если категория не существует, выполнить редирект на shop-grid.html
            return render(request, 'products/shop.html', {'products': products})

    # Фильтрация по гендеру
    if gender:
        products = products.filter(gender=gender)

    # Фильтрация по бренду
    if brand_name:
        try:
            brand = Brand.objects.get(name=brand_name)
            products = products.filter(brand=brand)
        except Brand.DoesNotExist:
            # Если бренд не существует, игнорируем фильтрацию по бренду
            pass

    # Фильтрация по поиску
    if query:
        # Фильтрация продуктов по названию, регистронезависимо
        products = products.filter(name__icontains=query)

    # Фильтрация по цвету (с приведением к нижнему регистру)
    if color:
        try:
            color_instance = Color.objects.get(name__iexact=color)
            products = products.filter(color=color_instance)
        except Color.DoesNotExist:
            # Если цвет не существует, игнорируем фильтрацию по цвету
            pass

    # Фильтрация по размеру
    if size:
        products = products.filter(size__iexact=size)

    # Сортировка по цене
    if sort_price == 'low':
        products = products.order_by('price')
    elif sort_price == 'high':
        products = products.order_by('-price')

    # Получаем все цвета из базы данных
    colors = Color.objects.all()
    # Получаем все бренды из базы данных
    brands = Brand.objects.all()

    # Отправляем отфильтрованный и отсортированный список, а также цвета и бренды в контекст шаблона
    context = {'products': products, 'colors': colors, 'brands': brands}
    return render(request, 'products/shop.html', context)


def sort_by_price(request):
    sort_price = request.GET.get('sort_price', '')
    if sort_price == 'low':
        products = Product.objects.all().order_by('price')
    elif sort_price == 'high':
        products = Product.objects.all().order_by('-price')
    else:
        products = Product.objects.all()

    return render(request, 'products/shop.html', {'products': products})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/shop-details.html'
    context_object_name = 'products'