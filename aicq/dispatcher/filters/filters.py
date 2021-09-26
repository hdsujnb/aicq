import abc
import typing

class Filter(abc.ABC):

    @abc.abstractmethod
    async def check(self, *args):
        pass

async def execute_filter(filter: Filter, *args):
    result = await filter.check(*args)
    return result

async def execute_filters(data: dict, filters: typing.List[Filter], *args):
    for filter in filters:
        result = await execute_filter(filter, *args)
        if isinstance(result, bool):
            if result is False:
                return False
            else:
                continue

        elif isinstance(result, dict):
            data.update(result)

        else:
            continue

    return data