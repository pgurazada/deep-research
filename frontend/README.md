# Deep Research Frontend

This project is a React application that interfaces with a FastAPI backend to conduct deep research using web search. The application allows users to input queries, view results, and access a history of previous interactions.

## Project Structure

```
deep-research-frontend
├── public
│   └── index.html          # Main HTML file for the React application
├── src
│   ├── api
│   │   └── fastapi.ts     # API functions to interact with the FastAPI server
│   ├── components
│   │   ├── ResearchInput.tsx    # Component for user input
│   │   ├── ResearchResult.tsx    # Component to display results
│   │   └── ResearchHistory.tsx    # Component to show query history
│   ├── pages
│   │   └── Home.tsx       # Main page component
│   ├── App.tsx            # Main application component
│   ├── index.tsx          # Entry point for the React application
│   └── styles
│       └── App.css        # CSS styles for the application
├── package.json            # npm configuration file
├── tsconfig.json           # TypeScript configuration file
└── README.md               # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd deep-research-frontend
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Run the application:**
   ```
   npm start
   ```

4. **Access the application:**
   Open your browser and navigate to `http://localhost:3000`.

## Usage

- Use the input field to enter your research queries.
- View the results displayed below the input field.
- Access the history of previous queries and results.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.