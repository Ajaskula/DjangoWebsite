from django.shortcuts import render, redirect, get_object_or_404
from .models import SVGImage, Rectangle
from django.http import HttpResponse
from django.template import loader
from .forms import RectangleForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

def home(request):
    image_list = SVGImage.objects.all()
    user_id = request.user.id
    context = {
        "user_id": user_id,
        "image_list": image_list,
    }
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # zwykły użytkownik
            template = loader.get_template('polls/admin_loggedin.html')
            # return HttpResponse(template, render(context, request))
            return HttpResponse(template.render(context, request))
        else:
            # admin
            # return HttpResponse(template, render(context, request))
            template = loader.get_template("polls/user_loggedin.html")
            return HttpResponse(template.render(context, request))
    # gość
    else:
        template = loader.get_template('polls/not_loggedin.html')
        return HttpResponse(template.render(context, request))


def manage_rectangle(request, image_id):
    # Pobranie obiektu SVGImage
    user = User.objects.get(id=3)
    svgimage = get_object_or_404(SVGImage, id=image_id)
    form = RectangleForm()
    # mam listę wszystkich otrzymanch przez użytkownika prostokątów
    svg_images = user.svgimage_set.all()
    # image = svg_images.get
    
    if request.method == 'POST':
        if 'add' in request.POST:
            # Obsługa dodawania prostokąta
            form = RectangleForm(request.POST)
            # jeśli chce dodać
            if form.is_valid():
                rectangle = form.save(commit=False)
                rectangle.svg_image = svgimage
                image_id = request.POST.get('image_id')
                # rectangle.svg_image = get_object_or_404(SVGImage, id=image_id)
                rectangle.save()
                render(request, 'polls/manage.html', {'image':svgimage,'form':form})
                # return redirect('')  # Zastąp 'nazwa_widoku' odpowiednią nazwą widoku
                # template = loader.get_template("polls/manage.html")
                # return HttpResponse(template.render(context, request))
        elif 'remove' in request.POST:
            rectangle_id = request.POST.get('rectangle_id')
            if rectangle_id:
                # Usunięcie prostokąta o podanym id
                rectangle = get_object_or_404(Rectangle, id=rectangle_id)
                svgimage.del_rectangle(rectangle_id)
                render(request, 'polls/manage.html', {'image':svgimage,'form':form})
    else:
        # Obsługa żądania GET, wyświetlenie formularza
        form = RectangleForm()
    return render(request, 'polls/manage.html', {'form': form, 'image': svgimage})
def manage_my_pictures(request, user_id):
    user = User.objects.get(id=user_id)
    # svgimage = get_object_or_404(SVGImage, id=image_id)
    form = RectangleForm()
    # mam listę wszystkich otrzymanch przez użytkownika prostokątów
    svg_images = user.svgimage_set.all()
    # image = svg_images.get
    
    if request.method == 'POST':
        if 'add' in request.POST:
            # Obsługa dodawania prostokąta
            form = RectangleForm(request.POST)
        #     # jeśli chce dodać
            if form.is_valid():
                rectangle = form.save(commit=False)
                image_id = int(request.POST.get('image_id'))
                # # image_id = request.POST.get('image_id').id
                # if image_id != 1:
                #     return HttpResponse(request, f"Jest image_id = {image_id}")
                # rectangle.svg_image = svg_images[image_id]
                # image_id = request.POST.get('image_id')
                rectangle.svg_image = get_object_or_404(SVGImage, id=image_id)
                rectangle.save()
                return render(request, 'polls/manage_my.html', {'svg_images':svg_images,'form':form})
                # return redirect('')  # Zastąp 'nazwa_widoku' odpowiednią nazwą widoku
                # template = loader.get_template("polls/manage.html")
                # return HttpResponse(template.render(context, request))
        elif 'remove' in request.POST:
            image_id = request.POST.get('image_id')
            rectangle_id = request.POST.get('rectangle_id')
            if rectangle_id:
                # Usunięcie prostokąta o podanym id
                svgimage = get_object_or_404(SVGImage, id=image_id)
                rectangle = get_object_or_404(Rectangle, id=rectangle_id)
                svgimage.del_rectangle(rectangle_id)
                return render(request, 'polls/manage_my.html', {'form': form, 'svg_images': svg_images})
    else:
        # Obsługa żądania GET, wyświetlenie formularza
        # form = RectangleForm()
        return render(request, 'polls/manage_my.html', {'form': form, 'svg_images': svg_images})


# def show_given_images(request, user_id):

# def show_image_list(request):
#     image_list = SVGImage.objects.all()
#     template = loader.get_template("polls/svg_image_detail.html")
#     context = {
#         "image_list": image_list,
#     }
#     return HttpResponse(template.render(context, request))



# inne widoki
# def image(request):
#     latest
def show_images(request):
    images = SVGImage.objects.all()
    return render(request, 'polls/show_images.html', {'images': images})

def detail(request, image_id):
    try:
        image = SVGImage.objects.get(id=image_id)
    except SVGImage.DoesNotExist:
        image = None

    return render(request, 'polls/detail.html', {'image': image})

def results(request, question_id):
    response = "You're looking at the results of qustion %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


# widok, który pozwala na dodatnie prostokąta do rysunku
def add_rectangle(request, svg_image_id):
    # template = loader.get_template("polls/svg_image_detail.html")
    if request.method == 'POST':
        svg_image = SVGImage.objects.get(pk=svg_image_id)
        x = request.POST['rectangle_x']
        y = request.POST['rectangle_y']
        width = request.POST['rectangle_width']
        height = request.POST['rectangle_height']
        fill = request.POST.get('rectangle_fill', 'black') 
        rectangle = Rectangle.objects.create(x=x, y=y, width=width, height=height, fill=fill)
        svg_image.rectangles.add(rectangle)
        return redirect('svg_image_detail', pk=svg_image_id)  # przekierowanie do widoku, nie do szablonu
    else:
        return render(request, 'error.html', {'error': 'Method not allowed'})

# widok, który pozwala na usunięcie prostokąta z rysunku
def delete_rectangle(request, svg_image_id, rectangle_id):
    if request.method == 'POST':
        rectangle = Rectangle.objects.get(pk=rectangle_id)
        rectangle.delete()
        return redirect('svg_image_detail', pk=svg_image_id)
    else:
        return render(request, 'error.html', {'error': 'Method not allowed'})
