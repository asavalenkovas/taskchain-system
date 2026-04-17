import hashlib
import json

from django.utils import timezone

from .models import Block


def calculate_hash(index, timestamp, event_type, event_data, prev_hash):
    block_data = {
        "index": index,
        "timestamp": timestamp.isoformat(),
        "event_type": event_type,
        "event_data": event_data,
        "prev_hash": prev_hash,
    }

    block_string = json.dumps(block_data, sort_keys=True)
    return hashlib.sha256(block_string.encode("utf-8")).hexdigest()


def create_block(event_type, event_data):
    last_block = Block.objects.order_by("-index").first()

    if last_block:
        index = last_block.index + 1
        prev_hash = last_block.hash
    else:
        index = 0
        prev_hash = "0" * 64

    timestamp = timezone.now()
    block_hash = calculate_hash(index, timestamp, event_type, event_data, prev_hash)

    block = Block.objects.create(
        index=index,
        created_at=timestamp,
        prev_hash=prev_hash,
        hash=block_hash,
        event_type=event_type,
        event_data=event_data,
    )

    return block

def verify_chain():
    blocks = Block.objects.order_by("index")

    if not blocks.exists():
        return True, "Chain is empty"

    previous_block = None

    for block in blocks:
        recalculated_hash = calculate_hash(
            index=block.index,
            timestamp=block.created_at,
            event_type=block.event_type,
            event_data=block.event_data,
            prev_hash=block.prev_hash,
        )

        if block.hash != recalculated_hash:
            return False, f"Hash mismatch at block {block.index}"

        if previous_block is not None:
            if block.prev_hash != previous_block.hash:
                return False, f"Broken chain at block {block.index}"

        else:
            if block.prev_hash != "0" * 64:
                return False, "Invalid genesis block"

        previous_block = block

    return True, "Chain is valid"

