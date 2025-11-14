from category.models import Category

# for the category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


