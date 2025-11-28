from category.models import Category

# for the category

def menu_links(request):
    links = Category.objects.filter(parent=None)
    return dict(links=links)


