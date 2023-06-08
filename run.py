from app import create_app

# Create the Flask app
app = create_app()

# Set up any additional configurations
# For example, you can set the debug mode to True for development
app.config['DEBUG'] = True

# Start the Flask app
if __name__ == '__main__':
    app.run()
