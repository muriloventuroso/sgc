from django.urls import path
import board.views

urlpatterns = [
    path('<congregation_id>', board.views.bulletin_board, {}, 'bulletin_board'),
]
