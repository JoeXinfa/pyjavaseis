from lxml import etree


def str2bool(str):
    if str.lower() in ('true', 't', 'y', 'yes', '1'):
        return True
    return False

def parset_element_is_array(text):
    if text.count('\n')>1:
        return True
    return False

def parset_element_get_value(text):
    """
    Either return the text string as a list of strings, or
    if not a list, then simply return the text string
    """
    if parset_element_is_array(text):
        return text.split()
    return text.strip()

def parse_parset_element(element):
    if not element.get('type'):
        return (None, None)

    element_type = element.get('type')
    retval = None
    value = element.text
    if element_type == 'string':
        retval = parset_element_get_value(value)

    elif element_type == 'boolean':
        retval = parset_element_get_value(value)
        if isinstance(retval, list):
            retval = map(str2bool, retval)
        else:
            retval = str2bool(retval)

    elif element_type == 'int':
        retval = parset_element_get_value(value)
        if isinstance(retval, list):
            retval = map(int, retval)
        else:
            retval = int(retval)

    elif element_type == 'double' or element_type == 'float':
        retval = parset_element_get_value(value)
        if isinstance(retval, list):
            retval = map(float, retval)
        else:
            retval = float(retval)

    elif element_type == 'long':
        retval = parset_element_get_value(value)
        if isinstance(retval, list):
            retval = map(long, retval)
        else:
            retval = long(retval)

    return (element_type, retval)

class Properties(object):
    def __init__(self, root, name):
        if not isinstance(root, etree._Element):
            raise Exception("Root argument must be of type etree._Element")
        self._root = root
        self._attributes = {}
        self._name = name

        self._parse_parset(self._root)

    def put(self, name, value, value_type=None):
        if not self._attributes.has_key(name):
            self._attributes[name] = {'value': value, 'type': value_type}

    def _parse_parset(self, parset, parent=None):
        childrens = list(parset)
        for child in childrens:
            if child.tag == 'par':
                value_type, value = parse_parset_element(child)
                if parent:
                    self._attributes[parent][child.get('name')] = {'value': value, 'type': value_type}
                else:
                    self._attributes[child.get('name')] = {'value': value, 'type': value_type}
            else: # parset
                name = child.get('name')
                self._attributes[name] = {}
                self._parse_parset(child, name)


    def _parse(self):
        children_elements = list(self._root)
        for child in children_elements:
            value_type, value = parse_parset_element(child)

            self.put(child.get('name'), value, value_type)


    def __str__(self):
        attribs = ""
        for key in self._attributes.keys():
            v = self._attributes[key]
            if isinstance(v, list):
                v = ', '.join(v)
            attribs += key
            attribs += " -> %s" % v

        import pprint
        from cStringIO import StringIO
        stream_buffer = StringIO()
        pprint.pprint(self._attributes, stream=stream_buffer)
        stream_buffer.seek(0)
        return '<%s %s>' % (self._name, stream_buffer.read())


class FileProperties(Properties):

    def __init__(self, root):
        super(FileProperties, self).__init__(root, "FileProperties")

    def get_nr_dimensions(self):
        value = self._attributes['DataDimensions']
        return value.get('value')

    def get_data_type(self):
        value = self._attributes['DataType']
        return value.get('value')

    def get_header_length_in_bytes(self):
        value = self._attributes['HeaderLengthBytes']
        return value.get('value')

    def get_javaseis_version(self):
        return self._attributes['JavaSeisVersion']['value']

    def get_logical_deltas(self):
        value = self._attributes['LogicalDeltas']
        return value.get('value')

    def get_logical_delta(self, dimension):
        return self.get_logical_deltas()[dimension]

    def get_logical_origins(self):
        value = self._attributes['LogicalOrigins']
        return value.get('value')

    def get_logical_origin(self, dimension):
        return self.get_logical_origins()[dimension]

    def is_mapped(self):
        value = self._attributes['Mapped']
        return value.get('value')

    def get_physical_deltas(self):
        value = self._attributes['PhysicalDeltas']
        return value.get('value')

    def get_physical_delta(self, dimension):
        return self.get_physical_deltas()[dimension]

    def get_physical_origins(self):
        value = self._attributes['PhysicalOrigins']
        return value.get('value')

    def get_physical_origin(self, dimension):
        return self.get_physical_origins()[dimension]

    def get_trace_format(self):
        value = self._attributes['TraceFormat']
        return value.get('value')

    def get_axis_labels(self):
        value = self._attributes['AxisLabels']
        return value.get('value')

    def get_axis_lengths(self):
        value = self._attributes['AxisLengths']
        return value.get('value')

    def get_axis_length(self, dimension):
        return self.get_axis_lengths()[dimension]

    def get_axis_units(self):
        value = self._attributes['AxisUnits']
        return value.get('value')

    def get_axis_unit(self, dimension):
        return self.get_axis_units()[dimension]

    def get_byteorder(self):
        return self._attributes['ByteOrder']['value']

    def get_comments(self):
        return self._attributes['Comments']['value']


class TraceProperties(Properties):
    def __init__(self, root):
        super(TraceProperties, self).__init__(root, "TraceProperties")


class CustomProperties(Properties):
    def __init__(self, root):
        super(CustomProperties, self).__init__(root, "CustomProperties")