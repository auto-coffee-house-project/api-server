from telegram.models import User

__all__ = ('upsert_user',)


def upsert_user(
        id_: int,
        first_name: str,
        last_name: str,
        username: str,
) -> tuple[User, bool]:
    return User.objects.update_or_create(
        id=id_,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
        }
    )
