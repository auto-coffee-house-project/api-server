from core.exceptions import ApplicationError


class ClientAlreadyHasMainGiftError(ApplicationError):
    default_code = 'CLIENT_ALREADY_HAS_MAIN_GIFT'


class GiftExpiredError(ApplicationError):
    default_code = 'GIFT_EXPIRED'
