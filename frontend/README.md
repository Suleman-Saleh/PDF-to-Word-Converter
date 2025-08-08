# PDF to Word Converter Frontend

This is the user interface for the PDF to Word Converter. It is a modern, responsive web application built with React and styled with Tailwind CSS, designed to provide a seamless user experience for uploading files and managing the conversion process.

## Features

- **File Upload Interface:** A clean and intuitive UI with both drag-and-drop and a standard file browser for PDF uploads.
- **Conversion Progress:** Real-time feedback and status updates during the file upload and conversion process.
- **OCR Toggle:** An option to enable or disable Optical Character Recognition (OCR), providing flexibility for different types of PDFs.
- **Responsive Design:** The layout is fully responsive, ensuring optimal usability on desktop, tablet, and mobile devices.
- **Custom Notifications:** Uses a custom modal for user feedback and error messages, avoiding intrusive browser alerts.

## Technologies

- **React:** A JavaScript library for building component-based user interfaces.
- **Tailwind CSS:** A utility-first CSS framework that enables rapid and consistent styling.
- **JavaScript (ES6+):** For all application logic, including state management and API calls.
- **fetch API:** Used for making asynchronous HTTP requests to the backend service.

## Prerequisites

- **Node.js:** Version 14 or higher.
- **npm or yarn:** A package manager for JavaScript dependencies.

## Installation

Navigate to the frontend directory:

```bash
cd frontend
```

Install the required Node.js dependencies from package.json:

```bash
npm install
# or
yarn install
```

## Running the Application

Start the development server:

```bash
npm start
# or
yarn start
```

The application will launch in your default web browser, typically at `http://localhost:3000`.

## File Structure

The project follows a standard React application structure:

- `src/`: Contains all the source code for the React components, logic, and styling.
- `App.js`: The main root component of the application.
- `index.js`: The entry point for the React application, which mounts the App component to the DOM.
- `public/`: Stores static assets such as the main `index.html` file and images.
- `package.json`: Lists the project's dependencies and defines scripts for running the application.
- `tailwind.config.js`: The configuration file for Tailwind CSS.

## API Integration

The frontend communicates with the backend API using a POST request to the `/convert` endpoint. It sends the PDF file and the OCR toggle state to the server and handles the returned `.docx` file as a blob, triggering a download.

## Troubleshooting

### Common Issues:

**Cannot connect to the backend:**
- Ensure the backend server is running on `http://localhost:8000`.
- Check for CORS errors in the browser console.

**`npm start` fails:**
- Make sure all dependencies are installed by running `npm install`.
- Verify that Node.js and npm are correctly installed and configured in your system's PATH.