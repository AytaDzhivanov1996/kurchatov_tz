from django.shortcuts import render, redirect

from bakery.sqlalchemy_db import OrderItemSQLAlchemy, OrderSQLAlchemy, ProductSQLAlchemy, Session


session = Session()

def index(request):
    return render(request, 'bakery/main.html')

def create_order(request):
    session = Session()

    if request.method == 'POST':
        person_name = request.POST.get('person_name')
        new_order = OrderSQLAlchemy(person_name=person_name)
        session.add(new_order)
        session.commit()

        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        for product_id, quantity in zip(product_ids, quantities):
            product = session.query(ProductSQLAlchemy).filter_by(id=product_id).first()
            if product and int(quantity) > 0:
                order_item = OrderItemSQLAlchemy(order=new_order, product=product, quantity=int(quantity))
                session.add(order_item)

        session.commit()
        session.close()
        return redirect('order_list')

    products = session.query(ProductSQLAlchemy).all()
    session.close()

    return render(request, 'bakery/create_order.html', {'products': products})


def order_list(request):
    session = Session()

    orders = session.query(OrderSQLAlchemy).all()

    for order in orders:
        order.total_cook_time()

    session.close()

    return render(request, 'bakery/order_list.html', {'orders': orders})
