import os
import uvicorn


if __name__ == '__main__':
    os.environ['BUILD'] = 'dev'
    host = '127.0.0.1' if 'HOST' not in os.environ else os.environ['HOST']

    uvicorn.run(
        'main:app',
        host=host,
        port=5000,
        log_config='log_config.json',
        log_level='info',
        reload=True,
    )
