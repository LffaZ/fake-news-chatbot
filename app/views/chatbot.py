from django.shortcuts import render, redirect
from django.http import JsonResponse

from app.forms import UserQueryForm
from app.models import UserQuery
from app.services.rag_service import vectorstore, generate_answer
import app.services.classifier as clf

def chatbot(request):
    if request.method == "POST":
        form = UserQueryForm(request.POST)

        if form.is_valid():
            try:
                user_query = form.save(commit=False)
                user_query.answer = ""
                user_query.save()

                query_text = user_query.question
                label = clf.classify(query_text)

                docs = vectorstore.similarity_search(
                    query_text,
                    k=3
                )

                retrieved_docs = [
                    {
                        "content": d.page_content,
                        "metadata": d.metadata
                    }
                    for d in docs
                ]

                answer = generate_answer(
                    query_text,
                    docs
                )

                user_query.answer = answer
                user_query.retrieved_docs = retrieved_docs
                user_query.label = label
                user_query.save()

                return JsonResponse({
                    "success": True,
                    "answer": answer
                })

            except Exception as e:
                return JsonResponse({
                    "success": False,
                    "error": str(e)
                })

    return render(
        request,
        "index.html",
        {
            "form": UserQueryForm()
        }
    )

def show(request):  
    userQueries = UserQuery.objects.all()  
    return render(request,"show.html",{'userqueries':userQueries})  
def destroy(request, id):  
    UserQuery = UserQuery.objects.get(id=id)  
    UserQuery.delete()  
    return redirect("/show")