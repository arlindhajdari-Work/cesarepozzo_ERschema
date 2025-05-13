
import csv
import json

def process_csv_to_tiddlers(csv_file_path, output_json_path):
    """
    Process the CSV file and generate TiddlyWiki-compatible JSON with TiddlyMap support
    """
    tiddlers = []
    current_entity = None
    attributes = []
    one_to_one_relations = []
    many_relations = []
    in_relations_section = False
    relation_type = None

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            # Skip empty rows
            if not row or not any(row):
                continue

            # Entity header detection (single column)
            if len(row) == 1 and row[0].strip() and not any(x in row[0] for x in ['Con uno entita', 'Con varie entita', 'IndietroSu']):        
                # Save previous entity if exists
                if current_entity:
                    tiddlers.append(create_tiddler(current_entity, attributes, one_to_one_relations, many_relations))

                # Start new entity
                current_entity = row[0].strip()
                attributes = []
                one_to_one_relations = []
                many_relations = []
                in_relations_section = False
                relation_type = None
                continue
                                                                                                                                               
            # Detect relations sections
            if len(row) == 1 and 'Con uno entita' in row[0]:
                in_relations_section = True
                relation_type = 'one_to_one'
                continue
            elif len(row) == 1 and 'Con varie entita' in row[0]:
                in_relations_section = True
                relation_type = 'many_to_many'
                continue

            # Process attribute rows (two columns)
            if len(row) >= 2 and row[0].strip() and row[1].strip():
                if not in_relations_section:
                    # Regular attribute
                    field_name = row[0].strip().rstrip(':')
                    db_field = row[1].strip().strip('{}').strip()
                    if field_name and db_field:
                        attributes.append(field_name)
                else:
                    # Relationship entry
                    if relation_type == 'one_to_one':
                        if ':' in row[1]:
                            rel_entity = row[1].split(':')[-1].strip('{}').strip()
                            one_to_one_relations.append(rel_entity)
                    elif relation_type == 'many_to_many':
                        rel_entity = row[1].strip('{}').strip()
                        if rel_entity and rel_entity != 'IndietroSu':
                            many_relations.append(rel_entity)

    # Add the last entity if exists
    if current_entity:
        tiddlers.append(create_tiddler(current_entity, attributes, one_to_one_relations, many_relations))

    # Write to JSON file
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(tiddlers, f, indent=2, ensure_ascii=False)

def create_tiddler(entity, attributes, one_to_one_relations, many_relations):
    """
    Create a Tiddler dictionary for the given entity
    """
    # Format attributes with ** prefix
    attributes_text = '\n'.join(f'**{attr}' for attr in attributes if attr)

    # Combine all relations
    all_relations = one_to_one_relations + many_relations
    relations_text = '\n'.join(f'[[{rel}]]' for rel in all_relations if rel)

    # Combine text content
    text_content = ""
    if attributes_text:
        text_content += attributes_text
    if relations_text:
        if text_content:
            text_content += '\n\n'
        text_content += relations_text

    return {
        "title": entity,
        "tags": ["ENTITY", "CRM"],
        "text": text_content
    }

# Example usage
if __name__ == "__main__":
    input_csv = "mergelabelsCesare.csv"  # Your input CSV file
    output_json = "tiddlymap_importv2.json"  # Output JSON file for TiddlyWiki
                                                                                                                                               
    process_csv_to_tiddlers(input_csv, output_json)                                                                                            
    print(f"Successfully generated TiddlyWiki JSON file at: {output_json}")