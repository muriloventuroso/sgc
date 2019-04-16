from django.urls import path
import financial.views

urlpatterns = [

    path(
        'transactions/<transaction_id>/delete/', financial.views.delete_transaction,
        {}, 'delete_transaction'),
    path('transactions/<transaction_id>/edit/', financial.views.edit_transaction, {}, 'edit_transaction'),
    path('transactions/add/', financial.views.add_transaction, {}, 'add_transaction'),
    path('transactions/', financial.views.transactions, {}, 'transactions'),
    path('pdf/', financial.views.generate_pdf, {}, 'generate_pdf_financial'),
]
