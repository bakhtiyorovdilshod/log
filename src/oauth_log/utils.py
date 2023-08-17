def log_helper(log) -> dict:
    print(f'log={log}')
    message = log['message']
    return {
        'id': str(log['_id']),
        'method': message['method'],
        'table_name': message['table_name'],
        'user_id': message['user_id'],
        'data': message['data']
    }