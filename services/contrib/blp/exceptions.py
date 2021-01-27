class StoryArgsException(Exception):
    def __init__(self, get_args, expected_args):
        message = 'get collection {} is not equals for expected {}'.format(get_args, expected_args)
        super().__init__(message)


class StoryMixedStepsException(Exception):
    def __init__(self):
        super().__init__('Expected mixed func collection. Don`t use common and async method togather')


class StoryEmptyStepsException(Exception):
    def __init__(self):
        super().__init__('No steps found in the story')