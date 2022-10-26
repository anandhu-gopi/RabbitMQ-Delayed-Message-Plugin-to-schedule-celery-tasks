from queues import DelayedTaskDeliveryKit, get_delayed_task_delivery_kit
from tasks import add

if __name__ == "__main__":

    delayed_task_delivery_kit: DelayedTaskDeliveryKit = get_delayed_task_delivery_kit(
        destination_queue_name="add-tasks"
    )
    add.apply_async(
        # kwargs: eqivalent to calling add(a=1,b=2)
        kwargs={"a": 1, "b": 3},
        exchange=delayed_task_delivery_kit.destination_exchange,
        routing_key=delayed_task_delivery_kit.routing_key,
        # setting 10 second (10000 millisecond) delay
        # refer: https://stackoverflow.com/a/35449483
        headers={"x-delay": 10000},
    )
