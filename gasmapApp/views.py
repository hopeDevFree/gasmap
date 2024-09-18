from datetime import datetime

from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

import requests
from .models import Item, User

from .forms import ItemForm

from django import forms

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.openstreetmap.org',
    'DNT': '1'
}

FUEL_TYPES = [
    {"id": "1-x", "description": "Benzina"},
    {"id": "1-1", "description": "Benzina (Self)"},
    {"id": "1-0", "description": "Benzina (Servito)"},
    {"id": "2-x", "description": "Gasolio"},
    {"id": "2-1", "description": "Gasolio (Self)"},
    {"id": "2-0", "description": "Gasolio (Servito)"},
    {"id": "3-x", "description": "Metano"},
    {"id": "3-1", "description": "Metano (Self)"},
    {"id": "3-0", "description": "Metano (Servito)"},
    {"id": "4-x", "description": "GPL"},
    {"id": "4-1", "description": "GPL (Self)"},
    {"id": "4-0", "description": "GPL (Servito)"},
    {"id": "323-x", "description": "L-GNC"},
    {"id": "323-1", "description": "L-GNC (Self)"},
    {"id": "323-0", "description": "L-GNC (Servito)"},
    {"id": "324-x", "description": "GNL"},
    {"id": "324-1", "description": "GNL (Self)"},
    {"id": "324-0", "description": "GNL (Servito)"}
]


def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gasmapApp:item_list')
    else:
        form = ItemForm()
    return render(request, 'gasmapApp/item_form.html', {'form': form})


def search_station(request):
    results = []
    count = 0

    print("test")

    address = request.POST.get('address')
    fuel_type = request.POST.get('fuel_type')
    order_by = request.POST.get('order_by', 'asc')

    addresses = Item.objects.distinct()
    fuel_types = FUEL_TYPES
    if address is not None and fuel_type is not None:
        item = get_object_or_404(Item, id=address)

        payload = {
            "points": [
                {
                    "lat": item.lat,
                    "lng": item.lon
                }
            ],
            "fuelType": fuel_type,
            "priceOrder": order_by,
            "radius": 5
        }

        response = requests.post('https://carburanti.mise.gov.it/ospzApi/search/zone', json=payload, headers=headers)

        results = response.json().get('results', [])

        for result in results:
            result['insertDate'] = datetime.fromisoformat(result['insertDate'])
            temp_fuels = {}
            for fuel in result['fuels']:
                if fuel['name'] not in temp_fuels:
                    temp_fuels[fuel['name']] = {'self_service': [], 'served': []}

                if fuel['isSelf']:
                    temp_fuels[fuel['name']]['self_service'].append(fuel)
                else:
                    temp_fuels[fuel['name']]['served'].append(fuel)

            result['fuels'] = list(temp_fuels.items())

        count = len(results)

    return render(request, 'gasmapApp/search_form.html', {
        'addresses': addresses,
        'results': results,
        'fuel_types': fuel_types,
        'count': count
    })


"""   
{
 'fuels': [
     {'id': 79488732, 'price': 1.637, 'name': 'Benzina', 'fuelId': 1, 'isSelf': False}, 
     {'id': 79488731, 'price': 1.637, 'name': 'Benzina', 'fuelId': 1, 'isSelf': True},
     {'id': 79488734, 'price': 1.553, 'name': 'Gasolio', 'fuelId': 2, 'isSelf': False},
     {'id': 79488733, 'price': 1.553, 'name': 'Gasolio', 'fuelId': 2, 'isSelf': True},
     {'id': 79488735, 'price': 0.629, 'name': 'GPL', 'fuelId': 4, 'isSelf': False}], 
 },
"""


def item_list(request):
    items = Item.objects.all()
    return render(request, 'gasmapApp/item_list.html', {'items': items})


def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('gasmapApp:item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'gasmapApp/item_form.html', {'form': form})


def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('gasmapApp:item_list')
    return render(request, 'gasmapApp/item_confirm_delete.html', {'item': item})


@require_POST
def search_address(request):
    query = request.POST.get('address', '')
    results = []

    if query and len(query) > 2:
        try:
            response = requests.get('https://nominatim.openstreetmap.org/search', params={
                'q': query,
                'countrycodes': 'it',
                'format': 'json',
                'addressdetails': 1,
                'limit': 5
            }, headers=headers)
            response.raise_for_status()
            data = response.json()
            results = [{'display_name': item['display_name'], 'lat': float(item['lat']), 'lon': float(item['lon'])} for
                       item in data]
        except requests.RequestException as e:
            print(f"Error: {e}")
            response = requests.get('https://ifconfig.me')
            print(response.text)
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Headers: {e.response.headers}")
            print(f"Response Text: {e.response.text}")

    return render(request, 'gasmapApp/item_form.html', {'results': results})


def add_station(request):
    return redirect('gasmapApp:item_list')


def signup(request):
    return render(request, 'registration/signup.html')


def home(request):
    return render(request, 'gasmapApp/home.html')


def check_user(request):
    if request.method == 'POST':
        id_user = request.POST.get('id_user')

        try:
            user = User.objects.get(id=id_user)
        except User.DoesNotExist:

            user = User(id=id_user)
            user.save()

        return render(request, 'gasmapApp/home.html', {'user': user})

    return HttpResponse('Metodo non supportato', status=405)
