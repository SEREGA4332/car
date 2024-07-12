from django.http import Http404
from django.shortcuts import render

from main.models import Car


def home(request):
	template_name = 'home.html'
	return render(request, template_name, {})


def cars_list_view(request):
	# получите список авто
	cars = Car.objects.all()
	query = request.GET.get('q', '')
	if query:
		cars = cars.filter(model__icontains=query)
	context = {'cars': cars}
	template_name = 'main/list.html'
	return render(request, template_name, context)  # передайте необходимый контекст


def car_details_view(request, car_id):
	# получите авто, если же его нет, выбросьте ошибку 404
	try:
		car = Car.objects.get(pk=car_id)
		context = {'car': car}
		template_name = 'main/details.html'
		return render(request, template_name, context)  # передайте необходимый контекст
	except Car.DoesNotExist:
		raise Http404('Car not found')


def sales_by_car(request, car_id):
	try:
		# получите авто и его продажи
		car = Car.objects.get(pk=car_id)
		sales = car.sale_set.all()
		context = {'car': car, 'sales': sales}
		template_name = 'main/sales.html'
		return render(request, template_name, context)  # передайте необходимый контекст
	except Car.DoesNotExist:
		raise Http404('Car not found')