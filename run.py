from app import create_app

from dotenv import load_dotenv


load_dotenv('.env')


app = create_app()

if __name__ == '__main__':
    #print(dict(app.config))
    app.config['PREFERRED_URL_SCHEME']='https'
    app.config['SERVER_NAME']='127.0.0.1:5555'
    # for i in dict(app.config).items():
    #     print(i)
    app.run() 

