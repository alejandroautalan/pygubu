import xml.etree.ElementTree as etree


SVG_NAMESPACE = "http://www.w3.org/2000/svg"
etree.register_namespace("", SVG_NAMESPACE)


def svgload(source, fill=None) -> str:
    """Load svg from source and apply modifiers."""
    tree: etree.Element = etree.parse(source)
    root = tree.getroot()

    if fill is not None:
        # Apply fill color override if provided
        pfill = "fill"
        pstroke = "stroke"
        color_none = "none"
        has_fill = root.attrib.get(pfill, None)
        has_stroke = root.attrib.get(pstroke, None)

        if not has_fill and not has_stroke:
            # Missing color information. FA Icon?
            root.attrib[pfill] = fill
        else:
            if has_fill and has_stroke:
                # Tabler icon ?
                fill_color = root.attrib.get(pfill, color_none)
                stroke_color = root.attrib.get(pstroke, color_none)
                if fill_color == color_none and stroke_color != color_none:
                    root.attrib[pstroke] = fill
                if fill_color != color_none and stroke_color == color_none:
                    root.attrib[pfill] = fill
            if has_fill and not has_stroke:
                # bootstrap icon ?
                root.attrib[pfill] = fill
    data = etree.tostring(root, "unicode")
    return data
