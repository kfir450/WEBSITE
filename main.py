from WEBSITE import create_app

app=create_app()
## this line makes it so it run the if we run it and not if we just import it
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


