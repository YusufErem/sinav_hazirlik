from django.contrib import admin

# Register your models here.
from main_app.models import Category, Question

admin.site.register(Category)
admin.site.register(Question)
#     notes = request.POST.get('notes')
#         mistake_reason = request.POST.get('mistake_reason')
#         question = Question(user=request.user, category=category, question_image=question_image, answer_image=answer_image, notes=notes, mistake_reason=mistake_reason)
#         question.save()
#         return redirect('home')
#     context = {'categories': categories}
#     return render(request, 'add_question.html', context)
#