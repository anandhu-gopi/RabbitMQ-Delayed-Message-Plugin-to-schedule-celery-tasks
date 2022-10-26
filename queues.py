"""Queues module provides the queues and exchanges for the celery tasks."""

from typing import NamedTuple

from kombu import Exchange, Queue


class DelayedTaskDeliveryKit(NamedTuple):
    destination_queue: Queue
    destination_exchange: Exchange
    routing_key: str


def get_delayed_task_delivery_kit(
    destination_queue_name: str,
) -> DelayedTaskDeliveryKit:
    """
    For getting the utils using which we can schedule celery tasks.

    Publish tasks with the custom header x-delay expressing a delay time
    for the task in milliseconds.The message will be delivered to the
    respective queues after x-delay milliseconds.


    (For setting 'x-delay' header,
    see: https://stackoverflow.com/questions/35449234/how-could-i-send-a-delayed-message-in-rabbitmq-using-the-rabbitmq-delayed-messag )

    """
    # To use the delayed-messaging feature,
    # declare an exchange with the type x-delayed-message
    destination_exchange = Exchange(
        destination_queue_name,
        type="x-delayed-message",
        # x-delayed-type arguments that can be passed during exchange.declare.
        # here we have used "direct" as exchange type. That means the plugin
        # will have the same routing behavior shown by the direct exchange.
        arguments={"x-delayed-type": "direct"},
    )
    destination_queue = Queue(
        destination_queue_name,
        exchange=destination_exchange,
        routing_key=destination_queue_name,
    )
    return DelayedTaskDeliveryKit(
        destination_queue=destination_queue,
        destination_exchange=destination_exchange,
        routing_key=destination_queue_name,
    )
