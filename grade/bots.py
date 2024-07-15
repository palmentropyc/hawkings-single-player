from .models import Bot

def create_bot(data):
    print("Creating new bot with data:", data)
    try:
        new_bot = Bot.objects.create(
            type=data['type'],
            stack=data['stack'],
            user=data['user']
        )
        print(f"New bot created with ID: {new_bot.id}")
        return new_bot
    except Exception as e:
        print(f"Error in create_bot: {str(e)}")
        raise