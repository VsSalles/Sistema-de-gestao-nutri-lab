from django.contrib import messages


def valida_campos(request, *args):
    for x in args:
        if len(x.strip()) == 0 or not x.isnumeric() :
            messages.add_message(request, messages.ERROR, 'todos os campos são numeros e obrigatorios!')
            return False
    return True
        


