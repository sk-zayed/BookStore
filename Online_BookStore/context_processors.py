from .models import Book

def filter_cat(request):
    bookcat=[]
    for b in Book.objects.all():
        bookcat.append(b.category)
    bookcat=list(set(bookcat))
    if "Old" in bookcat:
        bookcat.remove("Old")
    return {"category":bookcat}