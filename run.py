from Flask_Project import app

# Check if run.py file is executed directly and not imported.
if __name__ == '__main__':
    app.run(debug=True)
