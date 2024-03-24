# PlayListify

Welcome to PlayListify App, a cutting-edge platform designed to transform your viewing experience. Built on FastAPI and NoSQL technology, this application offers a seamless and personalized video streaming experience like never before.

## Features

- **Personalized User Profiles:** Create custom user profiles tailored to your preferences, allowing for a personalized experience every time you log in.
  
- **Secure Authentication:** Protect your data with advanced authentication mechanisms, ensuring your information remains safe and secure.

- **Seamless Playback:** Enjoy uninterrupted playback with resumable video functionality, allowing you to pick up right where you left off.

- **Effortless Search:** Find your favorite content effortlessly with our intuitive search engine, enabling you to discover new videos and explore a vast library of content.

- **User-Generated Content:** Add your favorite videos from YouTube directly to your personal library, giving you access to a diverse range of content.

- **Custom Playlists:** Create personalized playlists to organize and enjoy your videos your way, making it easy to access and enjoy your favorite content.

## Getting Started

To get started with PlayListify App, follow these steps:

1. **Installation:** Clone this repository to your local machine and install the required dependencies using `pip install -r requirements.txt`.

2. **Configuration:** Configure your environment variables, database connections, and any other settings required for your deployment environment. Add the folder `unencrypted` to the root of your project directory.

3. **Add Database Secrets:** Place the `astradbsecrets.zip` file containing your database secrets inside the `unencrypted` folder. **Do not add the `unencrypted` folder or `astradbsecrets.zip` file to GitHub**. Make sure to add them to your `.gitignore` file to prevent accidental commits.

4. **Run the Application:** Start the FastAPI server by running `uvicorn app.main:app --reload` from the command line. Your app will be accessible at `http://127.0.0.1:8000`.

5. **Run with Docker:** Build the Docker image using the provided Dockerfile. Run the container with the following command:

`docker run -d -p 8000:8000 playlistify-app`

6. **Sign Up:** Create a new user account to access the full range of features offered by the application.

7. **Explore and Enjoy:** Once logged in, explore the various features of the application, add videos to your library, create playlists, and start streaming your favorite content.

## License

This project is licensed under the [MIT License](LICENSE), allowing for free use, modification, and distribution of the codebase.

## Support

If you encounter any issues or have any questions about PlayListify App, please don't hesitate to reach out to us at svaru2306@gmail.com

Thank you for choosing PlayListify App. We hope you enjoy your viewing experience!