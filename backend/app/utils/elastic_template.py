def elastic_template_convertor(template) -> dict:
    return {
        'id': str(template['_id']),
        'table_name': template['table_name'],
        'method': template['method'],
        'templates': template['templates']
    }


def elastic_validation_convertor(template) -> dict:
    return {
        'templates': template['templates']
    }