# Cine_HTTP_final

This is a simple HTTP project built with Node.js

## Prerequisites

Make sure you have the following installed on your machine:

- Node.js (version >= 10.x.x)
- npm (version >= 6.x.x)

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Pirate-Emperor/Cine_HTTP_final.git
cd Cine_HTTP_final
```

Install the required npm packages:

```bash
npm install
```

## Usage

Start the server with the following command:

```bash
npm start
```

The server will be running on `http://localhost:3000`.

You can access the following endpoints:

- `GET /`: returns a welcome message.
- `GET /users`: returns a list of users.
- `POST /users`: creates a new user (provide user data in request body).

## Development

To run the project in development mode, use:

```bash
npm run dev
```

This will start the server using `nodemon` so that it automatically restarts whenever you make changes to the code.

## Testing

To run the tests, use:

```bash
npm test
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

