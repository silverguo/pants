# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.base.exceptions import TaskError
from pants.task.task import Task


class TargetFilterTaskMixin(Task):
    """A Task mixin that provides methods to help with filtering by target type."""

    class InvalidTargetType(TaskError):
        """Indicates a target type name that is not registered or does not point to a `Target`
        type."""

    def target_types_for_alias(self, alias):
        """Returns all the target types that might be produced by the given alias.

        Normally there is 1 target type per alias, but macros can expand a single alias to several
        target types.

        :param string alias: The alias to look up associated target types for.
        :returns: The set of target types that can be produced by the given alias.
        :raises :class:`TargetFilterTaskMixin.InvalidTargetType`: when no target types correspond to
                                                                  the given `alias`.
        """
        registered_aliases = self.context.build_configuration.registered_aliases()
        target_types = registered_aliases.target_types_by_alias.get(alias, None)
        if not target_types:
            raise self.InvalidTargetType("Not a target type: {}".format(alias))
        return target_types
