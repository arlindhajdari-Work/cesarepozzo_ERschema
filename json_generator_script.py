import csv
import json
from collections import defaultdict

def process_csv_to_tiddlers(csv_file_path, output_json_path):
    # Read the CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    tiddlers = []
    current_entity = None
    attributes = []
    one_to_one_relations = []
    many_relations = []
    in_relations_section = False

    for row in rows:
        # Skip empty rows
        if not row or not any(row):
            continue

        # Detect entity headers (they appear as single column rows)
        if len(row) == 1 and row[0] and not row[0].startswith(('Con uno entita', 'Con varie entita')):
            # Save previous entity if exists
            if current_entity:
                tiddler = create_tiddler(current_entity, attributes, one_to_one_relations, many_relations)
                tiddlers.append(tiddler)

            # Start new entity
            current_entity = row[0].strip()
            attributes = []
            one_to_one_relations = []
            many_relations = []
            in_relations_section = False

        # Detect relations sections
        elif len(row) == 1 and row[0].startswith('Con uno entita'):
            in_relations_section = 'one-to-one'
        elif len(row) == 1 and row[0].startswith('Con varie entita'):
            in_relations_section = 'many'

        # Process attribute rows (two columns)
        elif len(row) >= 2 and row[0] and row[1]:
            field_name = row[0].strip().rstrip(':')
            db_field = row[1].strip().strip('{}').strip()

            if not in_relations_section:
                if field_name and db_field:
                    attributes.append(field_name)
            else:
                # Process relationship entries
                if in_relations_section == 'one-to-one' and ':' in db_field:
                    rel_name, rel_entity = db_field.split(':', 1)
                    one_to_one_relations.append(rel_entity.strip())
                elif in_relations_section == 'many' and db_field.startswith('{') and db_field.endswith('}'):
                    rel_entity = db_field.strip('{}').strip()
                    many_relations.append(rel_entity)

    # Add the last entity
    if current_entity:
        tiddler = create_tiddler(current_entity, attributes, one_to_one_relations, many_relations)
        tiddlers.append(tiddler)

    # Write to JSON file
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(tiddlers, f, indent=2, ensure_ascii=False)

def create_tiddler(entity, attributes, one_to_one_relations, many_relations):
    # Format attributes with ** prefix
    attributes_text = '\n'.join(f'**{attr}' for attr in attributes)

    # Combine all relations
    all_relations = one_to_one_relations + many_relations
    relations_text = '\n'.join(f'[[{rel}]]' for rel in all_relations)

    # Combine text content
    text_content = f"{attributes_text}\n\n{relations_text}" if attributes_text or relations_text else ""

    return {
        "title": entity,
        "tags": "ENTITY CRM",
        "text": text_content
    }

# Example usage
if __name__ == "__main__":
    input_csv = "mergelabelsCesare.csv"  # Replace with your actual CSV file path
    output_json = "tiddlymap_import.json"
    process_csv_to_tiddlers(input_csv, output_json)
    print(f"Tiddlers JSON file generated at: {output_json}")