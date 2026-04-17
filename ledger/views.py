from django.shortcuts import render
from .models import Block
from .services import verify_chain


def home(request):
    return render(request, "home.html")


def chain_status(request):
    is_valid, message = verify_chain()
    return render(request, "chain_status.html", {
        "is_valid": is_valid,
        "message": message,
    })

def block_list(request):
    blocks = Block.objects.filter(
        event_type__in=["TASK_CREATED", "TASK_STATUS_CHANGED"]
    ).order_by("-index")[:40]

    return render(request, "block_list.html", {"blocks": blocks})


def block_detail(request, index):
    block = Block.objects.filter(index=index).first()
    if not block:
        return render(request, "block_detail.html", {"error": "Block not found"})

