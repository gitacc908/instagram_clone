OFF = 1
FROM_ALL = 2
FROM_FOLLOWING = 3


LIKE = (
    (OFF, 'Выкл'),
    (FROM_FOLLOWING, 'От людей, на которых вы подписаны'), 
    (FROM_ALL, 'От всех')
    )

COMMENT = (
    (OFF, 'Выкл'),
    (FROM_FOLLOWING, 'От людей, на которых вы подписаны'), 
    (FROM_ALL, 'От всех')
    )

COMMENT_LIKE = (
    (FROM_FOLLOWING, 'От людей, на которых вы подписаны'), 
    (FROM_ALL, 'От всех')
    )

FOLLOW_REQUEST = (
    (OFF, 'Выкл'),
    (FROM_ALL, 'От всех')
    )
