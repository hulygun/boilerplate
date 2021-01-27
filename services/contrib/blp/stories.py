#ToDo: Documentation
import inspect
from typing import Callable

from .exceptions import StoryArgsException, StoryEmptyStepsException, StoryMixedStepsException
from .returns import Failure, Result


class Context:
    """Context class for stories"""

    def __init__(self, **entries):
        self.__dict__.update(entries)


class Story:
    """Story decorator"""

    def __init__(self, *args):
        self.args = sorted(args)

    def __call__(self, method):
        """Decorate wrapper"""
        steps = []  # steps of story

        class Collector(object):
            """Steps collector"""

            def __getattr__(self, item):
                steps.append(item)

        method(Collector())

        if not steps: raise StoryEmptyStepsException()

        def return_func(instance, **kwargs):
            if sorted(kwargs.keys()) != self.args:
                raise StoryArgsException(sorted(kwargs.keys()), self.args)
            func = inner_async if self.is_async(instance, steps) else inner
            return func(instance, **kwargs)

        async def inner_async(instance, **kwargs):
            ctx = Context(**kwargs)
            failures = []
            next_step = None
            output = None
            for step in steps:
                if next_step and step != next_step: continue
                step_result = await getattr(instance, step)(ctx)
                if isinstance(step_result, Failure): failures.append(step_result.reason)
                if isinstance(step_result, Result): output = step_result.value
                if step_result.step == False: break
                next_step = step_result.step

            return self.build_result(failures, output, ctx)

        def inner(instance, **kwargs):
            ctx = Context(**kwargs)
            failures = []
            next_step = None
            output = None
            for step in steps:
                if next_step and step != next_step: continue
                step_result = getattr(instance, step)(ctx)
                if isinstance(step_result, Failure): failures.append(step_result.reason)
                if isinstance(step_result, Result): output = step_result.value
                if step_result.step == False: break
                next_step = step_result.step

            return self.build_result(failures, output, ctx)

        return return_func

    def build_result(self, failures, output, ctx):
        attrs = {
            'is_success': not bool(failures),
            'is_failed': bool(failures),
            'value': failures or output or ctx
        }
        if failures:
            attrs.update({
                'failure_because': staticmethod(lambda reason: reason in failures)
            })
        return type(
            "Story",
            (object,),
            attrs
        )

    @staticmethod
    def is_async(instance: Callable, methods: list) -> bool:
        a = s = 0
        for method in methods:
            if inspect.iscoroutinefunction(getattr(instance, method)):
                a += 1
            else:
                s += 1
        if max(a, s) != len(methods):
            raise StoryMixedStepsException()
        return a > s


story = Story
