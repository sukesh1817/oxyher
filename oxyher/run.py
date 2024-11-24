from app import create_app
app = create_app()


if __name__=="__main__":
    app.run(debug=True, use_debugger=False,use_reloader=True, port=1000)
