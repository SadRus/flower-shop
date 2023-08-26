from shop.forms import ConsultationForm


def consultation_form(_):
    return {
        'consultation_form': ConsultationForm()
    }
