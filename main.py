from WEBSITE import create_app

app=create_app()
## this line makes it so it run the if we run it and not if we just import it
if __name__=='__main__':
    app.run(debug=True)#debug mean every change to the code restarting the web

