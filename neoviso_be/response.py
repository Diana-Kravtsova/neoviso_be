from django.core.paginator import Page, Paginator


class Response:
    def __init__(self, model=None, message=None, errors=None):
        self.model = model
        self.message = message
        self.errors = errors


class PageResponse:
    def __init__(self, model, message, page_obj: Page, paginator: Paginator):
        self.model = model
        self.message = message
        self.page_number = page_obj.number
        self.total_pages = paginator.num_pages
        self.total_items = paginator.count
        self.has_next = page_obj.has_next()
        self.has_previous = page_obj.has_previous()

    def __dict__(self):
        return {
            'model': self.model,
            'message': self.message,
            'pageNumber': self.page_number,
            'totalPages': self.total_pages,
            'totalItems': self.total_items,
            'hasNext': self.has_next,
            'hasPrevious': self.has_previous
        }
