import requests
import xml.etree.ElementTree as ET

def fetch_ena_sample_metadata(sample_id: str) -> dict:
    """
    Fetch metadata for a given ENA sample accession (SAMEA*, ERS*, etc.)
    using the ENA Browser XML API.
    Returns a flat dictionary suitable for a pandas DataFrame.
    """
    url = f"https://www.ebi.ac.uk/ena/browser/api/xml/{sample_id}?includeLinks=false"
    r = requests.get(url)
    r.raise_for_status()
    xml_text = r.text

    root = ET.fromstring(xml_text)
    flat = {"accession": sample_id}

    sample_elem = root.find(".//SAMPLE")
    if sample_elem is None:
        flat["error"] = "No SAMPLE element found"
        return flat

    # Basic metadata (attributes and children)
    for attr, value in sample_elem.attrib.items():
        flat[attr.lower()] = value

    for tag in ["TITLE", "DESCRIPTION"]:
        elem = sample_elem.find(tag)
        if elem is not None and elem.text:
            flat[tag.lower()] = elem.text.strip()

    # Taxonomy info
    taxon_id = sample_elem.find(".//TAXON_ID")
    sci_name = sample_elem.find(".//SCIENTIFIC_NAME")
    if taxon_id is not None:
        flat["taxon_id"] = taxon_id.text.strip()
    if sci_name is not None:
        flat["scientific_name"] = sci_name.text.strip()

    # Parse SAMPLE_ATTRIBUTES
    for sa in sample_elem.findall(".//SAMPLE_ATTRIBUTE"):
        tag_el = sa.find("TAG")
        val_el = sa.find("VALUE")
        if tag_el is not None and val_el is not None:
            # print(tag_el.text, val_el.text)
            tag = tag_el.text.strip().lower().replace(" ", "_").replace("(", "").replace(")", "") if tag_el.text is not None else ""
            flat[tag] = val_el.text.strip() if val_el.text is not None else ""

    return flat