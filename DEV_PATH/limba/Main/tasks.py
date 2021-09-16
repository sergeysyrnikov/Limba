from celery import shared_task

"""test function"""
@shared_task()
def test_function():
    try:
        print("Check function!")
    except (Exception, ValueError):
        print("Check exception!")
