from django.urls import path
import financial.views

urlpatterns = [

    path(
        'financial/transactions/<transaction_id>/delete/', financial.views.delete_transaction,
        {}, 'delete_transaction'),
    path('financial/transactions/<transaction_id>/edit/', financial.views.edit_transaction, {}, 'edit_transaction'),
    path('financial/transactions/add/', financial.views.add_transaction, {}, 'add_transaction'),
    path('financial/transactions/', financial.views.transactions, {}, 'transactions'),
]
