from django.apps import AppConfig


class BookshelfConfig(AppConfig):
    name = 'bookshelf'
    
    def ready(self):
        import bookshelf.signal