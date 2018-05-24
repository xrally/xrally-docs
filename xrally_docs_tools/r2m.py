# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from docutils import frontend
from docutils import nodes
from docutils.parsers import rst
from docutils import utils


class NewDocument(object):
    def __init__(self):
        self._children = []

    @classmethod
    def from_rst(cls, text):
        self = cls()

        parser = rst.Parser()
        settings = frontend.OptionParser(
            components=(rst.Parser,)).get_default_values()
        document = utils.new_document(text, settings)
        parser.parse(text, document)

        self._children.extend(self._parse_elements(document.children))
        return self

    def format(self):
        return "\n\n".join(self._children)

    def _parse_paragraph(self, element):
        return "".join(self._parse_elements(element.children))

    def _parse_quote(self, element):
        elements = []
        for elem in self._parse_elements(element.children):
            if elem.startswith("```") and elem.endswith("```"):
                # it is code-block with external redundant indent
                elements.append(elem)
            else:
                elements.append("> %s" % elem)
        return "\n\n".join(elements)

    def _parse_note(self, element):
        # need to join first to take care about new lines in paragraph items
        text = "\n\n".join(self._parse_elements(element.children))
        return "!!! note\n    %s" % "\n    ".join(text.split("\n"))

    def _parse_list(self, element, form="bulleted"):
        if form not in ("bulleted", "enumerated", "definitions"):
            raise ValueError("Cannot parse %s list." % form)
        elements = []
        children = element.children

        if form == "definitions":
            # it can be a case when the empty line is missed after list
            # title and list items, let's check
            first_element = children[0]
            definition_elem = first_element.children[1]

            # if definition startswith * and if it is not text in
            # italics style, it is a bulleted list
            if (isinstance(definition_elem.children[0], nodes.paragraph)
                    and definition_elem.children[0].astext().startswith("*")
                    and not isinstance(definition_elem.children[0].children[0],
                                       nodes.emphasis)):
                form = "bulleted"
                elements.append(self._parse_paragraph(first_element))
                elements.append("\n")
                children = children[1:]
            elif (isinstance(definition_elem.children[0],
                             nodes.enumerated_list)):
                form = "bulleted"
                # add title
                elements.append(self._parse_paragraph(
                    first_element.children[0]))
                children = definition_elem.children[0].children
            # check the last char of first line
            elif first_element.astext().split("\n")[0][-1] in ":.":
                # term should not ends with these chars. it is not definitions
                # add title
                term = first_element.children[0]
                definition = first_element.children[1]
                elements.append(self._parse_paragraph(term.children[0]))
                elements.append(
                    "\n\n".join(self._parse_elements(definition.children)))
                return "\n\n".join(elements)

            else:
                import pdb;pdb.set_trace()

        for i, elem in enumerate(children):
            if form == "enumerated":
                line_id = "%s. " % i
            else:
                line_id = "- "
            intend = " " * len(line_id)
            separator = "\n%s" % intend

            if form == "definitions":
                term = elem.children[0].astext()
                line_id += "**%s**\n" % term

                paragraph = self._parse_paragraph(elem.children[1])
            else:
                paragraph = self._parse_paragraph(elem)
            paragraph = separator.join(paragraph.split("\n"))
            elements.append("%s%s" % (line_id, paragraph))

        return "\n".join(elements)

    def _parse_section(self, element):
        # find the level of section
        level = 1
        _elem = element
        while not isinstance(_elem.parent, nodes.document):
            level += 1
            _elem = _elem.parent

        # first element should be a title
        title = element.children[0].astext()
        sep = "#" * level
        page = [sep + " " + title,
                "\n\n".join(self._parse_elements(element.children[1:]))]

        return "\n\n".join(page)

    def _parse_reference(self, element):
        # the reference can be a link itself or a label for the link.
        # In second case, the next element should be a target note
        index = element.parent.children.index(element)
        if index + 1 < len(element.parent.children):
            link = element.parent.children[index + 1]
            if isinstance(link, nodes.target):
                return "[%s](%s)" % (element.astext(),
                                     link.attributes["refuri"])
        return "<%s>" % element.astext()

    def _parse_elements(self, raw_elements):
        elements = []
        for elem in raw_elements:
            if isinstance(elem, nodes.Text):
                elements.append(elem.astext())
            elif isinstance(elem, nodes.problematic):
                if elem.astext() == "`":
                    # hi amaretsky
                    elements.append("'")
                else:
                    raise Exception()
            elif (isinstance(elem, nodes.literal)
                    # NOTE: title_reference is actually wrong usage of literal
                    or isinstance(elem, nodes.title_reference)):
                elements.append("`%s`" % elem.astext())
            elif isinstance(elem, nodes.strong):
                elements.append("**%s**" % elem.astext())
            elif isinstance(elem, nodes.emphasis):
                elements.append("*%s*" % elem.astext())
            elif isinstance(elem, nodes.paragraph):
                elements.append(self._parse_paragraph(elem))
            elif isinstance(elem, nodes.literal_block):
                elem_classes = elem.attributes.get("classes")
                if elem_classes[0] == "code":
                    elements.append("```%(type)s\n%(code-block)s\n```" % {
                        "type": elem_classes[1],
                        "code-block": elem.astext()
                    })
                else:
                    raise Exception()
            elif isinstance(elem, nodes.bullet_list):
                elements.append(self._parse_list(elem))
            elif isinstance(elem, nodes.block_quote):
                elements.append(self._parse_quote(elem))
            elif isinstance(elem, nodes.note):
                elements.append(self._parse_note(elem))
            elif isinstance(elem, nodes.enumerated_list):
                elements.append(self._parse_list(elem, form="enumerated"))
            elif isinstance(elem, nodes.definition_list):
                elements.append(self._parse_list(elem, form="definitions"))
            elif isinstance(elem, nodes.reference):
                elements.append(self._parse_reference(elem))
            elif isinstance(elem, nodes.target):
                # ignore. previous element should be a reference
                pass
            elif isinstance(elem, nodes.system_message):
                # it is message from the rst parser. do nothing with it
                pass
            elif isinstance(elem, nodes.section):
                elements.append(self._parse_section(elem))
            elif isinstance(elem, nodes.comment):
                elements.append("<!-- %s -->" % elem.astext())
            else:
                import pdb;pdb.set_trace()
        return elements


def convert(text):
    """Convert reStructuredText to MarkDown format"""
    return NewDocument.from_rst(text).format()
