from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Value, Func, Count, ExpressionWrapper
from django.db.models.functions import Concat
from django.db.models.aggregates import Sum, Avg, Count, Min, Max
from store.models import Product, Customer, Collection, Order, OrderItem

from django.db import connection


from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem


def say_hello(request):
    # here all is not necessary since order_by also returns the query_set
    # query_set = Product.objects.all().order_by('unit_price')
    # query_set = Product.objects.order_by('unit_price')
    # product = Product.objects.filter(pk=0)
    # product = get_object_or_404(Product, pk=0)
    # query_set = Product.objects.filter(unit_price__gt=90)
    # query_set = Product.objects.filter(unit_price__gte=90)
    # query_set = Product.objects.filter(unit_price__range=(70, 80))
    # query_set = Product.objects.filter(collection__id__range=(1, 2, 3))
    # query_set = Product.objects.filter(collection__id=1)
    # query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(title__istartswith='coffee')

    # query_set = Product.objects.filter(last_update__year=2021).order_by('title')
    # query_set = Product.objects.filter(description__isnull=True)

    # query_set = Product.objects.filter(inventory__lt=10)

    # For Customers
    # query_set = Customer.objects.all().filter(email__icontains='.com').reverse()          #reverse the order_by

    # for Collection
    # query_set = Collection.objects.filter(featured_product__isnull=True)

    # for Order
    # query_set = Order.objects.filter(customer__id=1)

    # for OrderItem
    # query_set = OrderItem.objects.filter(product__collection__id=3)

    # complex queries
    # product: inventory < 10 AND price < 20
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)

    # products: inventory < 10 OR price < 20
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # query_set = Product.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__lt=20)) #negate

    # product: inventory == unit_price
    # query_set = Product.objects.filter(inventory=F('unit_price'))
    # query_set = Product.objects.filter(inventory=F('collection__id')) # related field(fk)

    # sorting
    # query_set = Customer.objects.all().filter(email__icontains='.com').reverse()
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price') # same as above, sort asc then return/eval a obj
    # product = Product.objects.latest('unit_price') # same as above, sort desc then return/eval a obj

    # limiting results
    # query_set = Product.objects.all()[0:5]
    # query_set = Product.objects.all()[5:10]

    # selecting field to query
    # query_set = Product.objects.values('id', 'title', 'collection__title') # returns a dict
    # query_set = Product.objects.values_list('id', 'title', 'collection__title') # return tuples

    # query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    # IMP selecting related objects
    # select_related(1) # collection
    # prefetch_related(n) # promotions
    # query_set = Product.objects.select_related('promotions').all()
    # query_set = Product.objects.prefetch_related('promotions').all()
    # query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()

    # query_set = Order.objects.prefetch_related('orderitem_set__product').select_related('customer',).order_by('-placed_at')[:5]

    # aggregates
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    # result = Product.objects.filter(collection__id=1).aggregate(count=Count('id'), min_price=Min('unit_price'))

    # annotating objects
    # query_set = Customer.objects.annotate(is_new=Value(True))
    # query_set = Customer.objects.annotate(new_id=F('id') + 1)

    # db functions

    # query_set = Customer.objects.annotate(
    #     # CONCAT
    #     full_name=Func(F'first_name', Value(
    #         ' '), F'last_name', function='CONCAT')
    # )

    # query_set = Customer.objects.annotate(
    #     # CONCAT of db fns
    #     full_name=Concat('first_name', Value(' '), 'last_name')
    # )

    # grouping data
    # query_set = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )

    # expression wrapper
    # discounted_price = ExpressionWrapper(
    #     F('unit_price') * 0.8, output_field=DecimalField())
    # query_set = Product.objects.annotate(
    #     discounted_price=discounted_price
    # )

    # querying generic relationships
    # content_type = ContentType.objects.get_for_model(Product)
    # query_set = TaggedItem.objects.select_related('tag').filter(
    #     content_type=content_type,
    #     object_id=1
    # )

    # custom managers

    # TaggedItem.objects.get_tags_for(Product, 1)  # see tags app.models

    # collection = Collection(title='Video Games',
    #                         featured_product=Product(pk=1))
    # collection.save()

    # updating
    # collection = Collection(pk=11)
    # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()

    # collection = Collection.objects.get(pk=11)
    # Collection.objects.filter(pk=11).update(featured_product=None) # django orm sets all fields null first/doesn't preserve by def. so

    # deleting
    # collection = Collection(pk=11)
    # collection.delete()

    # collection = Collection.objects.filter(id__gt=5).delete()

    # executing raw SQL

    # query = Product.objects.raw('SELECT * FROM store_product')

    # cursor = connection.cursor()
    # cursor.execute('SELECT, INSERT, UPDATE, DELETE etc.')
    # cursor.close()
    # with connection.cursor() as cursor:
    #     cursor.execute('SQLstmts')
    #     cursor.callproc('get_customers', [1, 2, 'a']) # stored procedure

    return render(request, 'playground/base.html', context={'name': 'karan'})
