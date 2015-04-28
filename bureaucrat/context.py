from __future__ import absolute_import

import logging
import json

LOG = logging.getLogger(__name__)

class ContextError(Exception):
    """Context error."""

#TODO: consider merging with FlowExpression (localprops smell like private to FlowExpression)
class Context(object):
    """Represents execution context."""

    def __init__(self, parent=None):
        """Initialize context."""

        self._parent = parent
        self._props = {}

    def parse(self, element):
        """Parse context XML element.

        :param element: context XML Element
        :type element: xml.etree.ElementTree.Element
        """

        self._props = {}
        for child in element:
            if child.tag == 'property':
                proptype = child.attrib["type"]
                value = None
                key = child.attrib["name"]
                if proptype == 'int':
                    value = int(child.text)
                elif proptype == 'float':
                    value = float(child.text)
                elif proptype == 'str':
                    value = unicode(child.text)
                elif proptype == 'bool':
                    value = bool(int(child.text))
                elif proptype == 'json':
                    value = json.loads(child.text)
                else:
                    raise ContextError("Unknown property type in the " + \
                                       "definition: '%s'" % proptype)
                self._props[key] = value

    def get(self, key):
        """Return property's value in the current context."""

        try:
            value = self._props[key]
        except KeyError:
            if self._parent is None:
                raise ContextError("No such property defined in the global" + \
                                   " context: %s" % key)
            else:
                value = self._parent.get(key)

        return value

    def set(self, key, value):
        """Set value of the property in the current context."""

        if self._parent is not None and key in self._parent._props.keys():
            self._parent.set(key, value)
        else:
            self._props[key] = value

    def update(self, props):
        """Update context with the given property values."""

        for key, value in props.items():
            self.set(key, value)

    def as_dictionary(self):
        """Return current context as dictionary."""

        props = {}

        if self._parent is not None:
            props = self._parent.as_dictionary()

        props.update(self._props)

        return props

    @property
    def localprops(self):
        return self._props

    @localprops.setter
    def localprops(self, props):
        self._props = props