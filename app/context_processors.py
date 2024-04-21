

def context_variables(request):
    if request.user.is_authenticated:
        user = request.user
        return {
            'user': user,
            'total_credit': user.get_total_credit or 0,
            'total_debit': user.get_total_debit or 0,
            'total': user.get_total_income or 0

        }
    return {
        'user': None,
        'total_credit': 0,
        'total_debit': 0,
        'total': 0
    }
